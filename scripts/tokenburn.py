#!/usr/bin/env python3
"""
tokenburn — Claude Code token & cost analytics
Usage: python3 tokenburn.py [--today|--week|--30d|--month]
"""

import json
import os
import sys
import glob
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import re
import shutil

# ── Pricing per million tokens ──────────────────────────────────────────────
PRICING = {
    'claude-opus-4-6':              {'input': 15.00, 'output': 75.00, 'cache_write': 18.75, 'cache_read': 1.50},
    'claude-opus-4-5':              {'input': 15.00, 'output': 75.00, 'cache_write': 18.75, 'cache_read': 1.50},
    'claude-sonnet-4-6':            {'input':  3.00, 'output': 15.00, 'cache_write':  3.75, 'cache_read': 0.30},
    'claude-sonnet-4-5':            {'input':  3.00, 'output': 15.00, 'cache_write':  3.75, 'cache_read': 0.30},
    'claude-haiku-4-5':             {'input':  0.80, 'output':  4.00, 'cache_write':  1.00, 'cache_read': 0.08},
    'claude-haiku-4-5-20251001':    {'input':  0.80, 'output':  4.00, 'cache_write':  1.00, 'cache_read': 0.08},
}
DEFAULT_PRICING = {'input': 3.00, 'output': 15.00, 'cache_write': 3.75, 'cache_read': 0.30}

# ── ANSI ────────────────────────────────────────────────────────────────────
R   = '\033[0m'
B   = '\033[1m'
DIM = '\033[2m'
YEL = '\033[33m'
CYN = '\033[36m'
GRN = '\033[32m'
MAG = '\033[35m'
BLU = '\033[34m'
RED = '\033[31m'
WHT = '\033[97m'
ORG = '\033[38;5;214m'

NO_COLOR = not sys.stdout.isatty()

def c(code, text):
    return text if NO_COLOR else f'{code}{text}{R}'

# ── Helpers ─────────────────────────────────────────────────────────────────

def calc_cost(model, usage):
    p = PRICING.get(model, DEFAULT_PRICING)
    M = 1_000_000
    return (
        usage.get('input_tokens', 0)                 * p['input']       / M +
        usage.get('output_tokens', 0)                * p['output']      / M +
        usage.get('cache_creation_input_tokens', 0)  * p['cache_write'] / M +
        usage.get('cache_read_input_tokens', 0)      * p['cache_read']  / M
    )

def fmt_cost(cost):
    if cost == 0:
        return '$0.0000'
    if cost >= 100:
        return f'${cost:,.0f}'
    if cost >= 1:
        return f'${cost:.2f}'
    return f'${cost:.4f}'

def period_start(arg):
    now = datetime.now(timezone.utc)
    if arg == '--week':
        return now - timedelta(days=7)
    if arg == '--30d':
        return now - timedelta(days=30)
    if arg == '--month':
        return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # default: today
    return now.replace(hour=0, minute=0, second=0, microsecond=0)

def project_label(cwd):
    if not cwd:
        return 'unknown'
    home = os.path.expanduser('~')
    path = cwd.replace(home, '~')
    parts = [p for p in path.split('/') if p]
    return '/'.join(parts[-2:]) if len(parts) >= 2 else path

def bar_chart(value, max_value, width=14):
    """Unicode gradient bar."""
    if max_value == 0 or value == 0:
        return ' ' * width
    ratio = value / max_value
    total_eighths = int(ratio * width * 8)
    full_blocks = total_eighths // 8
    remainder = total_eighths % 8
    blocks = ' ▏▎▍▌▋▊▉█'
    s = '█' * full_blocks
    if full_blocks < width:
        s += blocks[remainder]
        s += ' ' * (width - full_blocks - 1)
    s = s[:width]
    if NO_COLOR:
        return s
    if ratio > 0.65:
        clr = ORG
    elif ratio > 0.30:
        clr = YEL
    else:
        clr = BLU
    return f'{clr}{s}{R}'

def extract_bash_cmd(input_dict):
    """Get the first word of a bash command."""
    cmd = input_dict.get('command', '') if isinstance(input_dict, dict) else ''
    if not cmd:
        return None
    first = cmd.strip().split()[0] if cmd.strip() else None
    if first in ('sudo', 'env', 'npx', 'yarn', 'pnpm'):
        parts = cmd.strip().split()
        return parts[1] if len(parts) > 1 else first
    return first

def model_label(model):
    aliases = {
        'claude-sonnet-4-6': 'Sonnet 4.6',
        'claude-sonnet-4-5': 'Sonnet 4.5',
        'claude-haiku-4-5':  'Haiku 4.5',
        'claude-haiku-4-5-20251001': 'Haiku 4.5',
        'claude-opus-4-6':   'Opus 4.6',
        'claude-opus-4-5':   'Opus 4.5',
    }
    return aliases.get(model, model)

def classify_activity(tools, bash_cmds):
    """Heuristic session activity classification."""
    tool_set = set(tools)
    bash_text = ' '.join(bash_cmds).lower()
    if 'Agent' in tool_set:
        return 'Delegation'
    if any(k in bash_text for k in ['jest', 'pytest', 'vitest', 'test', 'mocha', 'rspec']):
        return 'Testing'
    if any(k in bash_text for k in ['deploy', 'vercel', 'docker', 'fly ', 'heroku', 'npm run build', 'yarn build']):
        return 'Build/Deploy'
    if any(t in tool_set for t in ['Edit', 'Write']) and any(t in tool_set for t in ['Read', 'Bash', 'Grep']):
        return 'Coding'
    if any(t in tool_set for t in ['Edit', 'Write']):
        return 'Feature Dev'
    if any(t in tool_set for t in ['Read', 'Grep', 'Glob']) and 'Edit' not in tool_set:
        return 'Exploration'
    if 'Bash' in tool_set:
        return 'Debugging'
    if 'WebSearch' in tool_set or 'WebFetch' in tool_set:
        return 'Exploration'
    return 'Conversation'

# ── Data loading ─────────────────────────────────────────────────────────────

def load_data(since: datetime):
    projects_dir = os.path.expanduser('~/.claude/projects/')
    files = glob.glob(os.path.join(projects_dir, '**', '*.jsonl'), recursive=True)

    # Accumulators
    by_day     = defaultdict(lambda: {'cost': 0.0, 'msgs': 0})
    by_project = defaultdict(lambda: {'cost': 0.0, 'msgs': 0})
    by_model   = defaultdict(lambda: {'cost': 0.0, 'calls': 0})
    by_tool    = defaultdict(int)
    by_bash    = defaultdict(int)
    by_mcp     = defaultdict(int)

    # For activity: per session accumulation
    session_data = defaultdict(lambda: {'tools': [], 'bash_cmds': [], 'cost': 0.0, 'msgs': 0, 'one_shot': False})

    total_cost  = 0.0
    total_msgs  = 0

    for filepath in files:
        try:
            with open(filepath, 'r', errors='replace') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    if obj.get('type') != 'assistant':
                        continue

                    ts_str = obj.get('timestamp', '')
                    if not ts_str:
                        continue
                    try:
                        ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                    except ValueError:
                        continue

                    if ts < since:
                        continue

                    msg   = obj.get('message', {})
                    model = msg.get('model', 'unknown')
                    usage = msg.get('usage', {})
                    cwd   = obj.get('cwd', '')
                    sid   = obj.get('sessionId', 'unknown')
                    day   = ts.strftime('%m-%d')
                    proj  = project_label(cwd)

                    cost = calc_cost(model, usage)

                    # Aggregate
                    by_day[day]['cost'] += cost
                    by_day[day]['msgs'] += 1
                    by_project[proj]['cost'] += cost
                    by_project[proj]['msgs'] += 1
                    by_model[model]['cost']  += cost
                    by_model[model]['calls'] += 1
                    total_cost += cost
                    total_msgs += 1

                    # Tools used in this message
                    content = msg.get('content', [])
                    for block in content:
                        if not isinstance(block, dict):
                            continue
                        btype = block.get('type', '')
                        if btype == 'tool_use':
                            tool_name = block.get('name', 'unknown')
                            by_tool[tool_name] += 1
                            session_data[sid]['tools'].append(tool_name)
                            if tool_name == 'Bash':
                                cmd = extract_bash_cmd(block.get('input', {}))
                                if cmd:
                                    by_bash[cmd] += 1
                                    session_data[sid]['bash_cmds'].append(cmd)
                        elif btype == 'server_tool_use':
                            name = block.get('name', 'mcp')
                            by_mcp[name] += 1

                    session_data[sid]['cost']  += cost
                    session_data[sid]['msgs']  += 1

        except (IOError, OSError):
            continue

    # Build activity breakdown from sessions
    by_activity = defaultdict(lambda: {'cost': 0.0, 'turns': 0, 'one_shots': 0})
    for sid, sd in session_data.items():
        activity = classify_activity(sd['tools'], sd['bash_cmds'])
        by_activity[activity]['cost']     += sd['cost']
        by_activity[activity]['turns']    += sd['msgs']
        if sd['msgs'] == 1:
            by_activity[activity]['one_shots'] += 1

    return {
        'total_cost':   total_cost,
        'total_msgs':   total_msgs,
        'by_day':       dict(by_day),
        'by_project':   dict(by_project),
        'by_model':     dict(by_model),
        'by_tool':      dict(by_tool),
        'by_bash':      dict(by_bash),
        'by_mcp':       dict(by_mcp),
        'by_activity':  dict(by_activity),
    }

# ── Rendering ────────────────────────────────────────────────────────────────

ANSI_RE = re.compile(r'\033\[[^m]*m')

def strip_ansi(s):
    return ANSI_RE.sub('', s)

def vlen(s):
    """Visible length of a string (ignores ANSI escape codes)."""
    return len(strip_ansi(s))

def pad_to(s, width):
    """Pad string s to visible width, accounting for ANSI codes."""
    pad = width - vlen(s)
    return s + ' ' * max(0, pad)

def box_line(inner, color, inner_width):
    """Wrap inner content (may contain ANSI) in box borders at fixed visible width."""
    side = c(color, '│')
    return side + pad_to(inner, inner_width) + side

def box_top(inner_width, color):
    return c(color, '┌' + '─' * inner_width + '┐')

def box_bot(inner_width, color):
    return c(color, '└' + '─' * inner_width + '┘')

def render_daily(by_day, max_cost, iw=40):
    """iw = inner width (chars between the │ borders)."""
    days = sorted(by_day.keys())[-10:]
    lines = [box_top(iw, CYN)]
    for day in days:
        d = by_day[day]
        b        = bar_chart(d['cost'], max_cost, 8)
        cost_str = c(YEL, f"{fmt_cost(d['cost']):>8}")
        cnt_str  = c(WHT, f"{d['msgs']:>5}")
        inner = f" {b} {day}  {cost_str}  {cnt_str} "
        lines.append(box_line(inner, CYN, iw))
    lines.append(box_bot(iw, CYN))
    return lines

def render_projects(by_project, max_cost, iw=46):
    items = sorted(by_project.items(), key=lambda x: -x[1]['cost'])[:8]
    lines = [box_top(iw, MAG)]
    for proj, d in items:
        b        = bar_chart(d['cost'], max_cost, 8)
        label    = proj[:22]
        cost_str = c(YEL, f"{fmt_cost(d['cost']):>8}")
        cnt_str  = c(WHT, f"{d['msgs']:>5}")
        inner = f" {b} {label:<22}  {cost_str}  {cnt_str} "
        lines.append(box_line(inner, MAG, iw))
    lines.append(box_bot(iw, MAG))
    return lines

def render_activity(by_activity, iw=48):
    items    = sorted(by_activity.items(), key=lambda x: -x[1]['cost'])
    max_cost = max((v['cost'] for v in by_activity.values()), default=1)
    lines    = [box_top(iw, YEL)]
    lines.append(box_line(' ' + c(B + YEL, 'By Activity'), YEL, iw))
    subhdr = f"{'':25}{c(DIM,'cost'):>4}   {'turns':>5}   {'1-shot':>6}"
    lines.append(box_line(' ' + subhdr, YEL, iw))
    for act, d in items:
        b        = bar_chart(d['cost'], max_cost, 8)
        turns    = d['turns']
        ones     = d['one_shots']
        pct      = f"{int(ones/turns*100)}%" if turns > 0 else '-'
        cost_str = c(YEL, f"{fmt_cost(d['cost']):>8}")
        act_clr  = CYN if d['cost'] > max_cost * 0.3 else WHT
        pct_clr  = GRN if ones > 0 else DIM
        inner = (f" {b} {c(act_clr, f'{act:<14}')}"
                 f"  {cost_str}  {turns:>5}  {c(pct_clr, f'{pct:>6}')}")
        lines.append(box_line(inner, YEL, iw))
    lines.append(box_bot(iw, YEL))
    return lines

def render_models(by_model, iw=46):
    items    = sorted(by_model.items(), key=lambda x: -x[1]['cost'])
    max_cost = max((v['cost'] for v in by_model.values()), default=1)
    lines    = [box_top(iw, MAG)]
    lines.append(box_line(' ' + c(B + MAG, 'By Model'), MAG, iw))
    subhdr = f"{'':25}{c(DIM,'cost'):>4}   {'calls':>6}"
    lines.append(box_line(' ' + subhdr, MAG, iw))
    for model, d in items:
        b        = bar_chart(d['cost'], max_cost, 8)
        label    = model_label(model)[:20]
        cost_str = c(YEL, f"{fmt_cost(d['cost']):>8}")
        inner    = f" {b} {label:<20}  {cost_str}  {d['calls']:>6}"
        lines.append(box_line(inner, MAG, iw))
    lines.append(box_bot(iw, MAG))
    return lines

def render_tools(by_tool, iw=36):
    items     = sorted(by_tool.items(), key=lambda x: -x[1])[:12]
    max_calls = max(by_tool.values(), default=1)
    lines     = [box_top(iw, CYN)]
    lines.append(box_line(' ' + c(B + CYN, 'Core Tools'), CYN, iw))
    subhdr = f"{'':25}{c(DIM,'calls'):>5}"
    lines.append(box_line(' ' + subhdr, CYN, iw))
    for tool, calls in items:
        b     = bar_chart(calls, max_calls, 8)
        inner = f" {b} {tool:<14}  {calls:>6}"
        lines.append(box_line(inner, CYN, iw))
    lines.append(box_bot(iw, CYN))
    return lines

def render_bash(by_bash, iw=36):
    items     = sorted(by_bash.items(), key=lambda x: -x[1])[:12]
    max_calls = max(by_bash.values(), default=1)
    lines     = [box_top(iw, GRN)]
    lines.append(box_line(' ' + c(B + GRN, 'Shell Commands'), GRN, iw))
    subhdr = f"{'':25}{c(DIM,'calls'):>5}"
    lines.append(box_line(' ' + subhdr, GRN, iw))
    for cmd, calls in items:
        b     = bar_chart(calls, max_calls, 8)
        inner = f" {b} {cmd:<14}  {calls:>6}"
        lines.append(box_line(inner, GRN, iw))
    lines.append(box_bot(iw, GRN))
    return lines

def render_mcp(by_mcp, iw=90):
    lines = [box_top(iw, MAG)]
    lines.append(box_line(' ' + c(B + MAG, 'MCP Servers'), MAG, iw))
    if not by_mcp:
        lines.append(box_line(' ' + c(DIM, 'No MCP usage'), MAG, iw))
    else:
        items = sorted(by_mcp.items(), key=lambda x: -x[1])[:5]
        for name, calls in items:
            inner = f"  {name:<30}  {calls:>6} calls"
            lines.append(box_line(inner, MAG, iw))
    lines.append(box_bot(iw, MAG))
    return lines

def side_by_side(left, right, gap=2):
    max_len = max(len(left), len(right))
    left  += [''] * (max_len - len(left))
    right += [''] * (max_len - len(right))
    return [l + ' ' * gap + r for l, r in zip(left, right)]

def render(data, period_label):
    term_width = shutil.get_terminal_size((120, 40)).columns

    total_cost = data['total_cost']
    total_msgs = data['total_msgs']
    by_day     = data['by_day']
    by_project = data['by_project']
    by_model   = data['by_model']
    by_tool    = data['by_tool']
    by_bash    = data['by_bash']
    by_mcp     = data['by_mcp']
    by_activity= data['by_activity']

    max_cost_day  = max((v['cost'] for v in by_day.values()),     default=1)
    max_cost_proj = max((v['cost'] for v in by_project.values()), default=1)
    max_cost_all  = max(max_cost_day, max_cost_proj)

    print()
    # ── Header ────────────────────────────────────────────────────────────
    title  = f"  {c(B+WHT, 'tokenburn')}  {c(DIM, '—')}  {c(YEL, fmt_cost(total_cost))} total  {c(DIM, '·')}  {c(WHT, str(total_msgs))} messages  {c(DIM, '·')}  {c(CYN, period_label)}"
    print(title)
    print(c(DIM, '  ' + '─' * min(60, term_width - 4)))
    print()

    # ── Row 1: Daily + Projects ───────────────────────────────────────────
    daily   = render_daily(by_day, max_cost_all)
    projects= render_projects(by_project, max_cost_all)
    row1 = side_by_side(daily, projects, gap=2)
    for line in row1:
        print('  ' + line)
    print()

    # ── Row 2: Activity + Models ──────────────────────────────────────────
    activity = render_activity(by_activity)
    models   = render_models(by_model)
    row2 = side_by_side(activity, models, gap=2)
    for line in row2:
        print('  ' + line)
    print()

    # ── Row 3: Tools + Bash ───────────────────────────────────────────────
    tools = render_tools(by_tool)
    bash  = render_bash(by_bash)
    row3 = side_by_side(tools, bash, gap=2)
    for line in row3:
        print('  ' + line)
    print()

    # ── MCP ───────────────────────────────────────────────────────────────
    mcp = render_mcp(by_mcp)
    for line in mcp:
        print('  ' + line)
    print()

    # ── Footer ────────────────────────────────────────────────────────────
    footer_items = [
        ('--today',  '1 today'),
        ('--week',   '2 week'),
        ('--30d',    '3 thirty days'),
        ('--month',  '4 month'),
    ]
    footer = '  ' + c(DIM, '  ·  '.join(
        f"{c(YEL, item[1])}" for item in footer_items
    ))
    print(footer)
    print()

# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    arg = '--today'
    for a in sys.argv[1:]:
        if a in ('--today', '--week', '--30d', '--month'):
            arg = a

    period_labels = {
        '--today': 'today',
        '--week':  'last 7 days',
        '--30d':   'last 30 days',
        '--month': 'this month',
    }

    since = period_start(arg)
    label = period_labels[arg]

    print(c(DIM, f"  Loading usage data ({label})…"), end='\r', flush=True)
    data = load_data(since)
    print(' ' * 40, end='\r')  # clear loading line

    render(data, label)

if __name__ == '__main__':
    main()
