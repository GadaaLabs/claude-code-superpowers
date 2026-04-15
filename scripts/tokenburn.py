#!/usr/bin/env python3
"""
tokenburn — Claude Code token & cost analytics
Interactive TUI (curses) when run in a terminal.
Static ANSI output when piped (e.g. via Claude's Bash tool).

Keys: 1 today  2 week  3 month  q quit
Direct use: python3 tokenburn.py [today|week|month]
"""

import curses
import json
import os
import sys
import glob
import math
from datetime import datetime, timedelta, timezone
from collections import defaultdict

# ── Pricing (per million tokens) ─────────────────────────────────────────────
PRICING = {
    'claude-opus-4-6':           {'input': 15.00, 'output': 75.00, 'cw': 18.75, 'cr': 1.50},
    'claude-opus-4-5':           {'input': 15.00, 'output': 75.00, 'cw': 18.75, 'cr': 1.50},
    'claude-sonnet-4-6':         {'input':  3.00, 'output': 15.00, 'cw':  3.75, 'cr': 0.30},
    'claude-sonnet-4-5':         {'input':  3.00, 'output': 15.00, 'cw':  3.75, 'cr': 0.30},
    'claude-haiku-4-5':          {'input':  0.80, 'output':  4.00, 'cw':  1.00, 'cr': 0.08},
    'claude-haiku-4-5-20251001': {'input':  0.80, 'output':  4.00, 'cw':  1.00, 'cr': 0.08},
}
DEFAULT_P = {'input': 3.00, 'output': 15.00, 'cw': 3.75, 'cr': 0.30}

PERIODS      = ['today', 'week', 'month']
PERIOD_LABEL = {'today': 'Today', 'week': '7 Days', 'month': 'This Month'}

# Activity → color pair (defined in setup_colors)
ACTIVITY_CP = {
    'Conversation':  'dim',
    'Coding':        'cyan',
    'Exploration':   'cyan',
    'Planning':      'green',
    'Brainstorming': 'magenta',
    'Delegation':    'yellow',
    'Debugging':     'orange',
    'Feature Dev':   'green',
    'General':       'dim',
    'Testing':       'green',
    'Refactoring':   'green',
    'Build/Deploy':  'green',
}

# ── Data helpers ──────────────────────────────────────────────────────────────

def calc_cost(model, usage):
    p = PRICING.get(model, DEFAULT_P)
    M = 1_000_000
    return (usage.get('input_tokens', 0)                * p['input']  / M +
            usage.get('output_tokens', 0)               * p['output'] / M +
            usage.get('cache_creation_input_tokens', 0) * p['cw']     / M +
            usage.get('cache_read_input_tokens', 0)     * p['cr']     / M)

def period_since(period):
    now = datetime.now(timezone.utc)
    if period == 'week':  return now - timedelta(days=7)
    if period == 'month': return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return now.replace(hour=0, minute=0, second=0, microsecond=0)

def fmt_cost(cost):
    if cost == 0:      return '$0.0000'
    if cost >= 10000:  return f'${cost:,.0f}'
    if cost >= 1000:   return f'${cost:,.0f}'
    if cost >= 100:    return f'${cost:.0f}'
    if cost >= 1:      return f'${cost:.2f}'
    return f'${cost:.4f}'

def fmt_num(n):
    if n >= 1_000_000_000: return f'{n/1_000_000_000:.1f}B'
    if n >= 1_000_000:     return f'{n/1_000_000:.1f}M'
    if n >= 1_000:         return f'{n/1_000:.1f}K'
    return str(n)

def project_label(cwd):
    if not cwd: return 'unknown'
    parts = cwd.replace(os.path.expanduser('~'), '~').split('/')
    return '/'.join(parts[-2:]) if len(parts) >= 2 else cwd

def model_label(m):
    return {
        'claude-opus-4-6': 'Opus 4.6',   'claude-opus-4-5': 'Opus 4.5',
        'claude-sonnet-4-6': 'Sonnet 4.6', 'claude-sonnet-4-5': 'Sonnet 4.5',
        'claude-haiku-4-5': 'Haiku 4.5',  'claude-haiku-4-5-20251001': 'Haiku 4.5',
    }.get(m, m)

def classify(tools, bash_cmds):
    ts  = set(tools)
    bc  = ' '.join(bash_cmds).lower()
    if 'Agent' in ts: return 'Delegation'
    if any(k in bc for k in ['jest','pytest','vitest','mocha','rspec']): return 'Testing'
    if any(k in bc for k in ['deploy','vercel','docker','heroku','npm run build','yarn build']): return 'Build/Deploy'
    if any(t in ts for t in ['Edit','Write']) and any(t in ts for t in ['Read','Bash','Grep']): return 'Coding'
    if any(t in ts for t in ['Edit','Write']): return 'Feature Dev'
    if any(t in ts for t in ['Read','Grep','Glob']) and not ts & {'Edit','Write'}: return 'Exploration'
    if 'WebSearch' in ts or 'WebFetch' in ts: return 'Exploration'
    if 'Bash' in ts: return 'Debugging'
    if not ts: return 'Conversation'
    return 'General'

# ── Data loading ──────────────────────────────────────────────────────────────

def load_data(period):
    since = period_since(period)
    files = glob.glob(os.path.join(os.path.expanduser('~/.claude/projects'), '**', '*.jsonl'), recursive=True)

    by_day     = defaultdict(lambda: {'cost': 0.0, 'calls': 0})
    by_project = defaultdict(lambda: {'cost': 0.0, 'sessions': set()})
    by_model   = defaultdict(lambda: {'cost': 0.0, 'calls': 0})
    by_tool    = defaultdict(int)
    by_mcp     = defaultdict(int)
    sessions   = defaultdict(lambda: {'tools': [], 'cmds': [], 'cost': 0.0})
    total      = {'cost': 0.0, 'calls': 0, 'in': 0, 'out': 0, 'cached': 0, 'written': 0}

    for fp in files:
        try:
            for line in open(fp, errors='replace'):
                line = line.strip()
                if not line: continue
                try:    obj = json.loads(line)
                except: continue
                if obj.get('type') != 'assistant': continue
                ts_str = obj.get('timestamp', '')
                if not ts_str: continue
                try:    ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                except: continue
                if ts < since: continue

                msg   = obj.get('message', {})
                model = msg.get('model', 'unknown')
                usage = msg.get('usage', {})
                cwd   = obj.get('cwd', '')
                sid   = obj.get('sessionId', '?')
                day   = ts.strftime('%m-%d')
                proj  = project_label(cwd)
                cost  = calc_cost(model, usage)

                by_day[day]['cost']      += cost
                by_day[day]['calls']     += 1
                by_project[proj]['cost'] += cost
                by_project[proj]['sessions'].add(sid)
                by_model[model]['cost']  += cost
                by_model[model]['calls'] += 1
                total['cost']    += cost
                total['calls']   += 1
                total['in']      += usage.get('input_tokens', 0)
                total['out']     += usage.get('output_tokens', 0)
                total['cached']  += usage.get('cache_read_input_tokens', 0)
                total['written'] += usage.get('cache_creation_input_tokens', 0)

                for block in msg.get('content', []):
                    if not isinstance(block, dict): continue
                    btype = block.get('type', '')
                    if btype == 'tool_use':
                        t = block.get('name', '?')
                        by_tool[t] += 1
                        sessions[sid]['tools'].append(t)
                        if t == 'Bash':
                            raw = (block.get('input') or {}).get('command', '')
                            parts = (raw or '').strip().split()
                            if parts: sessions[sid]['cmds'].append(parts[0])
                    elif btype == 'server_tool_use':
                        by_mcp[block.get('name', 'mcp')] += 1
                sessions[sid]['cost'] += cost
        except: continue

    by_activity = defaultdict(lambda: {'cost': 0.0, 'turns': 0})
    for sd in sessions.values():
        act = classify(sd['tools'], sd['cmds'])
        by_activity[act]['cost']  += sd['cost']
        by_activity[act]['turns'] += 1

    total_tok = total['in'] + total['cached'] + total['written']
    cache_hit = (total['cached'] / total_tok * 100) if total_tok > 0 else 0

    return {
        'total':       total,
        'cache_hit':   cache_hit,
        'sessions':    len(sessions),
        'by_day':      dict(sorted(by_day.items())),
        'by_project':  {k: {'cost': v['cost'], 'sessions': len(v['sessions'])} for k, v in by_project.items()},
        'by_model':    dict(by_model),
        'by_tool':     dict(by_tool),
        'by_mcp':      dict(by_mcp),
        'by_activity': dict(by_activity),
    }

# ═══════════════════════════════════════════════════════════════════════════════
# ── CURSES TUI ────────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

# Color pair names → index
_CP = {}

def setup_colors():
    curses.start_color()
    curses.use_default_colors()
    has256 = curses.COLORS >= 256

    pairs = {
        'orange':  (214 if has256 else curses.COLOR_YELLOW, -1),
        'cyan':    (curses.COLOR_CYAN,    -1),
        'green':   (curses.COLOR_GREEN,   -1),
        'magenta': (curses.COLOR_MAGENTA, -1),
        'yellow':  (curses.COLOR_YELLOW,  -1),
        'white':   (curses.COLOR_WHITE,   -1),
        'dim':     (8 if has256 else curses.COLOR_BLACK, -1),
        'red':     (curses.COLOR_RED,     -1),
        'blue':    (curses.COLOR_BLUE,    -1),
    }
    for i, (name, (fg, bg)) in enumerate(pairs.items(), start=1):
        curses.init_pair(i, fg, bg)
        _CP[name] = i

def cp(name, bold=False, dim=False):
    attr = curses.color_pair(_CP.get(name, _CP['white']))
    if bold: attr |= curses.A_BOLD
    if dim:  attr |= curses.A_DIM
    return attr

def saddstr(win, y, x, text, attr=0):
    """Safe addstr — clips to window bounds."""
    if not text: return
    h, w = win.getmaxyx()
    if y < 0 or y >= h or x < 0 or x >= w - 1: return
    text = text[:max(0, w - x - 1)]
    try: win.addstr(y, x, text, attr)
    except curses.error: pass

def draw_box(win, y, x, h, w, color, title=''):
    """Draw a rounded-corner box with colored border and optional title."""
    a = cp(color, bold=True)
    try:
        win.addch(y,     x,     curses.ACS_ULCORNER, a)
        win.addch(y,     x+w-1, curses.ACS_URCORNER, a)
        win.addch(y+h-1, x,     curses.ACS_LLCORNER, a)
        win.addch(y+h-1, x+w-1, curses.ACS_LRCORNER, a)
        for i in range(1, w-1):
            win.addch(y,     x+i, curses.ACS_HLINE, a)
            win.addch(y+h-1, x+i, curses.ACS_HLINE, a)
        for i in range(1, h-1):
            win.addch(y+i, x,     curses.ACS_VLINE, a)
            win.addch(y+i, x+w-1, curses.ACS_VLINE, a)
    except curses.error: pass
    if title:
        saddstr(win, y, x+2, f' {title} ', a)

def draw_bar(win, y, x, value, max_val, width=14):
    """Gradient bar: blue → yellow → orange."""
    if max_val <= 0 or value <= 0: return
    filled = max(1, int((value / max_val) * width))
    t = max(1, width // 3)
    for i in range(min(filled, width)):
        color = 'blue' if i < t else ('yellow' if i < t * 2 else 'orange')
        try: win.addch(y, x+i, ord('█'), cp(color, bold=True))
        except curses.error: pass

# ── Panel renderers ───────────────────────────────────────────────────────────

BAR_W = 14  # width of bar charts

def _subhdr(win, y, x, w, cols):
    """Right-align column headers inside a panel."""
    txt = '  '.join(cols)
    saddstr(win, y, x + w - len(txt) - 2, txt, cp('dim'))

def panel_daily(win, y, x, h, w, data):
    draw_box(win, y, x, h, w, 'cyan', 'Daily Activity')
    items  = list(sorted(data['by_day'].items()))[-max(1, h-4):]
    max_c  = max((v['cost']  for v in data['by_day'].values()), default=1)
    _subhdr(win, y+1, x, w, ['cost', 'calls'])
    for i, (day, d) in enumerate(items):
        r = y + 2 + i
        if r >= y + h - 1: break
        draw_bar(win, r, x+1, d['cost'], max_c, BAR_W)
        saddstr(win, r, x+BAR_W+2, day, cp('white'))
        saddstr(win, r, x+w-14, fmt_cost(d['cost']), cp('orange', bold=True))
        saddstr(win, r, x+w-6,  str(d['calls']),     cp('white'))

def panel_projects(win, y, x, h, w, data):
    draw_box(win, y, x, h, w, 'green', 'By Project')
    items = sorted(data['by_project'].items(), key=lambda v: -v[1]['cost'])
    max_c = max((v['cost'] for v in data['by_project'].values()), default=1)
    _subhdr(win, y+1, x, w, ['cost', 'sess'])
    for i, (proj, d) in enumerate(items[:h-4]):
        r = y + 2 + i
        if r >= y + h - 1: break
        draw_bar(win, r, x+1, d['cost'], max_c, BAR_W)
        label = proj[:w - BAR_W - 16]
        saddstr(win, r, x+BAR_W+2, label,              cp('white'))
        saddstr(win, r, x+w-14,    fmt_cost(d['cost']), cp('orange', bold=True))
        saddstr(win, r, x+w-5,     str(d['sessions']),  cp('white'))

def panel_models(win, y, x, h, w, data):
    draw_box(win, y, x, h, w, 'magenta', 'By Model')
    items = sorted(data['by_model'].items(), key=lambda v: -v[1]['cost'])
    max_c = max((v['cost'] for v in data['by_model'].values()), default=1)
    _subhdr(win, y+1, x, w, ['cost', 'calls'])
    for i, (model, d) in enumerate(items[:h-4]):
        r = y + 2 + i
        if r >= y + h - 1: break
        draw_bar(win, r, x+1, d['cost'], max_c, BAR_W)
        label    = model_label(model)
        cost_clr = 'orange' if d['cost'] == max(v['cost'] for v in data['by_model'].values()) else 'white'
        saddstr(win, r, x+BAR_W+2, label,             cp('white'))
        saddstr(win, r, x+w-14,    fmt_cost(d['cost']), cp(cost_clr, bold=(cost_clr=='orange')))
        saddstr(win, r, x+w-6,     str(d['calls']),     cp('white'))

def panel_activity(win, y, x, h, w, data):
    draw_box(win, y, x, h, w, 'yellow', 'By Activity')
    items = sorted(data['by_activity'].items(), key=lambda v: -v[1]['cost'])
    max_c = max((v['cost'] for v in data['by_activity'].values()), default=1)
    _subhdr(win, y+1, x, w, ['cost', 'turns'])
    for i, (act, d) in enumerate(items[:h-4]):
        r = y + 2 + i
        if r >= y + h - 1: break
        draw_bar(win, r, x+1, d['cost'], max_c, BAR_W)
        aclr = ACTIVITY_CP.get(act, 'white')
        saddstr(win, r, x+BAR_W+2, act,              cp(aclr))
        saddstr(win, r, x+w-14,    fmt_cost(d['cost']), cp('orange', bold=True))
        saddstr(win, r, x+w-6,     str(d['turns']),     cp('white'))

def panel_tools(win, y, x, h, w, data):
    draw_box(win, y, x, h, w, 'cyan', 'Core Tools')
    items = sorted(data['by_tool'].items(), key=lambda v: -v[1])
    max_c = max(data['by_tool'].values(), default=1)
    _subhdr(win, y+1, x, w, ['calls'])
    for i, (tool, calls) in enumerate(items[:h-4]):
        r = y + 2 + i
        if r >= y + h - 1: break
        draw_bar(win, r, x+1, calls, max_c, BAR_W)
        saddstr(win, r, x+BAR_W+2, tool,       cp('white'))
        saddstr(win, r, x+w-7,     str(calls),  cp('white'))

def panel_mcp(win, y, x, h, w, data):
    draw_box(win, y, x, h, w, 'magenta', 'MCP Servers')
    _subhdr(win, y+1, x, w, ['calls'])
    if not data['by_mcp']:
        saddstr(win, y+2, x+2, 'No MCP usage', cp('dim'))
        return
    items = sorted(data['by_mcp'].items(), key=lambda v: -v[1])
    max_c = max(data['by_mcp'].values(), default=1)
    for i, (name, calls) in enumerate(items[:h-4]):
        r = y + 2 + i
        if r >= y + h - 1: break
        draw_bar(win, r, x+1, calls, max_c, BAR_W)
        saddstr(win, r, x+BAR_W+2, name,      cp('white'))
        saddstr(win, r, x+w-7,     str(calls), cp('white'))

# ── Header & footer ───────────────────────────────────────────────────────────

def draw_header(win, period, data):
    total = data['total']

    # Period tab bar
    x = 2
    for p in PERIODS:
        label = PERIOD_LABEL[p]
        if p == period:
            saddstr(win, 0, x, f'[ {label} ]', cp('white', bold=True))
            x += len(label) + 4
        else:
            saddstr(win, 0, x, label, cp('dim'))
            x += len(label) + 3

    # Title line
    saddstr(win, 1, 2, 'CodeBurn', cp('orange', bold=True))
    saddstr(win, 1, 12, PERIOD_LABEL[period], cp('dim'))

    # Stats line
    cost_s  = fmt_cost(total['cost'])
    calls_s = f"{total['calls']:,}"
    sess_s  = str(data['sessions'])
    cache_s = f"{data['cache_hit']:.0f}%"
    saddstr(win, 2, 2, cost_s,     cp('orange', bold=True))
    saddstr(win, 2, 2+len(cost_s), f' cost   ', cp('white'))
    cx = 2+len(cost_s)+8
    saddstr(win, 2, cx, calls_s, cp('white', bold=True))
    saddstr(win, 2, cx+len(calls_s), ' calls   ', cp('white'))
    cx += len(calls_s)+9
    saddstr(win, 2, cx, sess_s, cp('white', bold=True))
    saddstr(win, 2, cx+len(sess_s), ' sessions   ', cp('white'))
    cx += len(sess_s)+12
    saddstr(win, 2, cx, cache_s, cp('white', bold=True))
    saddstr(win, 2, cx+len(cache_s), ' cache hit', cp('white'))

    # Token counts
    tok = (f"{fmt_num(total['in'])} in   {fmt_num(total['out'])} out   "
           f"{fmt_num(total['cached'])} cached   {fmt_num(total['written'])} written")
    saddstr(win, 3, 2, tok, cp('dim'))

def draw_footer(win):
    h, w = win.getmaxyx()
    parts = [
        ('<>',     'dim',    ' switch   '),
        ('q',      'dim',    ' quit   '),
        ('1',      'yellow', ' today   '),
        ('2',      'yellow', ' week   '),
        ('3',      'yellow', ' month'),
    ]
    # calculate total visible length
    total_len = sum(len(k)+len(rest) for k, _, rest in parts)
    x = max(0, (w - total_len) // 2)
    for key, kclr, rest in parts:
        saddstr(win, h-1, x, key,  cp(kclr, bold=True))
        x += len(key)
        saddstr(win, h-1, x, rest, cp('white'))
        x += len(rest)

# ── Main draw ─────────────────────────────────────────────────────────────────

HEADER_H = 5   # rows 0-4
FOOTER_H = 1

def draw_all(win, period, data):
    win.erase()
    h, w = win.getmaxyx()

    avail = h - HEADER_H - FOOTER_H
    if avail < 6:
        saddstr(win, 0, 0, 'Terminal too small', cp('red'))
        win.refresh()
        return

    # Panel heights — split 3 rows, give activity extra if possible
    ph = [avail // 3] * 3
    ph[0] += avail - sum(ph)  # give remainder to row 0

    lw = w // 2
    rw = w - lw

    draw_header(win, period, data)

    ry = [HEADER_H, HEADER_H + ph[0], HEADER_H + ph[0] + ph[1]]

    panel_daily(win,    ry[0], 0,  ph[0], lw, data)
    panel_projects(win, ry[0], lw, ph[0], rw, data)

    panel_models(win,   ry[1], 0,  ph[1], lw, data)
    panel_activity(win, ry[1], lw, ph[1], rw, data)

    panel_tools(win, ry[2], 0,  ph[2], lw, data)
    panel_mcp(win,   ry[2], lw, ph[2], rw, data)

    draw_footer(win)
    win.refresh()

# ── App loop ──────────────────────────────────────────────────────────────────

def run_tui(stdscr):
    setup_colors()
    curses.curs_set(0)
    stdscr.timeout(200)

    period = 'week'

    # Show loading
    stdscr.erase()
    saddstr(stdscr, 0, 2, 'CodeBurn', cp('orange', bold=True) if _CP else 0)
    saddstr(stdscr, 1, 2, 'Loading data…')
    stdscr.refresh()
    data = load_data(period)

    while True:
        draw_all(stdscr, period, data)
        key = stdscr.getch()
        if key in (ord('q'), ord('Q'), 27):
            break
        elif key == ord('1'):
            period = 'today';  data = load_data(period)
        elif key == ord('2'):
            period = 'week';   data = load_data(period)
        elif key == ord('3'):
            period = 'month';  data = load_data(period)
        elif key == curses.KEY_RESIZE:
            stdscr.erase()

# ═══════════════════════════════════════════════════════════════════════════════
# ── STATIC ANSI OUTPUT (for non-TTY / Claude Bash tool) ──────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

R    = '\033[0m'
BOLD = '\033[1m'
DIM  = '\033[2m'

ANSI = {
    'orange':  '\033[38;5;214m',
    'cyan':    '\033[36m',
    'green':   '\033[32m',
    'magenta': '\033[35m',
    'yellow':  '\033[33m',
    'white':   '\033[97m',
    'dim':     '\033[2m',
    'red':     '\033[31m',
    'blue':    '\033[34m',
    'reset':   R,
}

ACT_ANSI = {
    'Conversation': ANSI['dim'],
    'Coding':       ANSI['cyan'],
    'Exploration':  ANSI['cyan'],
    'Planning':     ANSI['green'],
    'Brainstorming':ANSI['magenta'],
    'Delegation':   ANSI['yellow'],
    'Debugging':    ANSI['orange'],
    'Feature Dev':  ANSI['green'],
    'General':      ANSI['dim'],
    'Testing':      ANSI['green'],
    'Refactoring':  ANSI['green'],
    'Build/Deploy': ANSI['green'],
}

import re as _re
_ANSI_RE = _re.compile(r'\033\[[^m]*m')

def _vlen(s): return len(_ANSI_RE.sub('', s))
def _pad(s, w): return s + ' ' * max(0, w - _vlen(s))
def _col(name, text, bold=False):
    return f"{BOLD if bold else ''}{ANSI.get(name,'')}{text}{R}"

def _ansi_bar(value, max_val, width=14):
    if max_val <= 0 or value <= 0: return ' ' * width
    filled = max(1, int((value / max_val) * width))
    t = max(1, width // 3)
    bar = ''
    for i in range(min(filled, width)):
        clr = 'blue' if i < t else ('yellow' if i < t*2 else 'orange')
        bar += f"{ANSI[clr]}█{R}"
    bar += ' ' * max(0, width - filled)
    return bar

def _box_top(iw, clr):
    return f"{ANSI[clr]}┌{'─'*iw}┐{R}"
def _box_bot(iw, clr):
    return f"{ANSI[clr]}└{'─'*iw}┘{R}"
def _box_row(content, iw, clr):
    side = f"{ANSI[clr]}│{R}"
    return side + _pad(content, iw) + side

def static_output(period, data):
    import shutil
    TW = shutil.get_terminal_size((120, 40)).columns
    total = data['total']

    # ── Header ────────────────────────────────────────────────────────────────
    print()
    # Period tabs
    tabs = ''
    for p in PERIODS:
        label = PERIOD_LABEL[p]
        tabs += (f"  {BOLD}{label}{R}" if p == period else f"  {_col('dim', label)}")
    print(f"  {tabs}")
    print()

    # Title
    cost_s  = fmt_cost(total['cost'])
    calls_s = f"{total['calls']:,}"
    sess_s  = str(data['sessions'])
    cache_s = f"{data['cache_hit']:.0f}%"
    print(f"  {_col('orange', 'CodeBurn', bold=True)}  {_col('dim', PERIOD_LABEL[period])}")
    print(f"  {_col('orange', cost_s, bold=True)} cost   "
          f"{BOLD}{calls_s}{R} calls   {BOLD}{sess_s}{R} sessions   "
          f"{BOLD}{cache_s}{R} cache hit")
    tok = (f"{_col('dim', fmt_num(total['in'])+' in')}   "
           f"{_col('dim', fmt_num(total['out'])+' out')}   "
           f"{_col('dim', fmt_num(total['cached'])+' cached')}   "
           f"{_col('dim', fmt_num(total['written'])+' written')}")
    print(f"  {tok}")
    print()

    # ── Panel helpers ─────────────────────────────────────────────────────────
    # Each panel pair: left and right rendered to line lists, then zipped

    half   = TW // 2 - 2
    iw     = half - 2   # inner width (between │ borders)
    bw     = 14         # bar width
    BW14   = bw

    def make_panel_daily():
        items = list(sorted(data['by_day'].items()))[-10:]
        max_c = max((v['cost']  for v in data['by_day'].values()), default=1)
        lines = [_box_top(iw, 'cyan')]
        # title embedded in top border
        lines[0] = f"{ANSI['cyan']}┌─ {BOLD}{_col('cyan','Daily Activity')}{ANSI['cyan']} {'─'*(iw-18)}┐{R}"
        lines.append(_box_row(f"  {'cost':>10}  {'calls':>5}", iw, 'cyan'))
        for day, d in items:
            bar   = _ansi_bar(d['cost'], max_c, BW14)
            cost  = _col('orange', f"{fmt_cost(d['cost']):>10}", bold=True)
            calls = f"{d['calls']:>5}"
            row   = f" {bar} {day}  {cost}  {calls}"
            lines.append(_box_row(row, iw, 'cyan'))
        lines.append(_box_bot(iw, 'cyan'))
        return lines

    def make_panel_projects():
        items = sorted(data['by_project'].items(), key=lambda v: -v[1]['cost'])[:8]
        max_c = max((v['cost'] for v in data['by_project'].values()), default=1)
        lines = [f"{ANSI['green']}┌─ {BOLD}{_col('green','By Project')}{ANSI['green']} {'─'*(iw-14)}┐{R}"]
        lines.append(_box_row(f"  {'cost':>10}  {'sess':>5}", iw, 'green'))
        for proj, d in items:
            bar   = _ansi_bar(d['cost'], max_c, BW14)
            label = proj[:iw - BW14 - 20]
            cost  = _col('orange', f"{fmt_cost(d['cost']):>10}", bold=True)
            sess  = f"{d['sessions']:>5}"
            row   = f" {bar} {label:<{iw-BW14-20}}  {cost}  {sess}"
            lines.append(_box_row(row, iw, 'green'))
        lines.append(_box_bot(iw, 'green'))
        return lines

    def make_panel_models():
        items = sorted(data['by_model'].items(), key=lambda v: -v[1]['cost'])
        max_c = max((v['cost'] for v in data['by_model'].values()), default=1)
        lines = [f"{ANSI['magenta']}┌─ {BOLD}{_col('magenta','By Model')}{ANSI['magenta']} {'─'*(iw-12)}┐{R}"]
        lines.append(_box_row(f"  {'cost':>10}  {'calls':>5}", iw, 'magenta'))
        for model, d in items:
            bar   = _ansi_bar(d['cost'], max_c, BW14)
            label = f"{model_label(model):<16}"
            clr   = 'orange' if d['cost'] == max_c else 'white'
            cost  = _col(clr, f"{fmt_cost(d['cost']):>10}", bold=(clr=='orange'))
            calls = f"{d['calls']:>5}"
            row   = f" {bar} {label}  {cost}  {calls}"
            lines.append(_box_row(row, iw, 'magenta'))
        lines.append(_box_bot(iw, 'magenta'))
        return lines

    def make_panel_activity():
        items = sorted(data['by_activity'].items(), key=lambda v: -v[1]['cost'])
        max_c = max((v['cost'] for v in data['by_activity'].values()), default=1)
        lines = [f"{ANSI['yellow']}┌─ {BOLD}{_col('yellow','By Activity')}{ANSI['yellow']} {'─'*(iw-15)}┐{R}"]
        lines.append(_box_row(f"  {'cost':>10}  {'turns':>5}", iw, 'yellow'))
        for act, d in items:
            bar   = _ansi_bar(d['cost'], max_c, BW14)
            aclr  = ACT_ANSI.get(act, ANSI['white'])
            label = f"{aclr}{act:<14}{R}"
            cost  = _col('orange', f"{fmt_cost(d['cost']):>10}", bold=True)
            turns = f"{d['turns']:>5}"
            row   = f" {bar} {label}  {cost}  {turns}"
            lines.append(_box_row(row, iw, 'yellow'))
        lines.append(_box_bot(iw, 'yellow'))
        return lines

    def make_panel_tools():
        items = sorted(data['by_tool'].items(), key=lambda v: -v[1])[:12]
        max_c = max(data['by_tool'].values(), default=1)
        lines = [f"{ANSI['cyan']}┌─ {BOLD}{_col('cyan','Core Tools')}{ANSI['cyan']} {'─'*(iw-14)}┐{R}"]
        lines.append(_box_row(f"  {'calls':>5}", iw, 'cyan'))
        for tool, calls in items:
            bar = _ansi_bar(calls, max_c, BW14)
            row = f" {bar} {tool:<16}  {calls:>5}"
            lines.append(_box_row(row, iw, 'cyan'))
        lines.append(_box_bot(iw, 'cyan'))
        return lines

    def make_panel_mcp():
        lines = [f"{ANSI['magenta']}┌─ {BOLD}{_col('magenta','MCP Servers')}{ANSI['magenta']} {'─'*(iw-15)}┐{R}"]
        lines.append(_box_row(f"  {'calls':>5}", iw, 'magenta'))
        if not data['by_mcp']:
            lines.append(_box_row(f" {_col('dim','No MCP usage')}", iw, 'magenta'))
        else:
            items = sorted(data['by_mcp'].items(), key=lambda v: -v[1])[:10]
            max_c = max(data['by_mcp'].values(), default=1)
            for name, calls in items:
                bar = _ansi_bar(calls, max_c, BW14)
                row = f" {bar} {name:<20}  {calls:>5}"
                lines.append(_box_row(row, iw, 'magenta'))
        lines.append(_box_bot(iw, 'magenta'))
        return lines

    def print_pair(left, right, gap=2):
        n = max(len(left), len(right))
        left  += [''] * (n - len(left))
        right += [''] * (n - len(right))
        for l, r in zip(left, right):
            print('  ' + l + ' ' * gap + r)

    print_pair(make_panel_daily(),    make_panel_projects())
    print()
    print_pair(make_panel_models(),   make_panel_activity())
    print()
    print_pair(make_panel_tools(),    make_panel_mcp())
    print()

    # Footer
    footer = (f"  {_col('dim','<>')} switch   "
              f"{_col('dim','q')} quit   "
              f"{_col('yellow','1',bold=True)} today   "
              f"{_col('yellow','2',bold=True)} week   "
              f"{_col('yellow','3',bold=True)} month")
    hw = TW // 2
    print(' ' * max(0, hw - 25) + footer)
    print()

# ═══════════════════════════════════════════════════════════════════════════════
# ── Entry point ───────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    period = 'week'
    for a in sys.argv[1:]:
        a = a.lower().lstrip('-')
        if a == 'today':            period = 'today'
        elif a in ('week', '7d'):   period = 'week'
        elif a in ('month', '30d'): period = 'month'

    is_tty = sys.stdout.isatty()

    if is_tty and '--static' not in sys.argv:
        # Full interactive TUI
        try:
            curses.wrapper(run_tui)
        except KeyboardInterrupt:
            pass
    else:
        # Static ANSI output (for Claude's Bash tool or piped output)
        sys.stderr.write(f'  Loading tokenburn data ({PERIOD_LABEL[period]})…\r')
        sys.stderr.flush()
        data = load_data(period)
        sys.stderr.write(' ' * 45 + '\r')
        static_output(period, data)

if __name__ == '__main__':
    main()
