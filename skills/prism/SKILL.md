---
name: prism
description: UI/UX design intelligence, accessibility, performance, SEO, and data visualization — domain expertise for web and app developers. Includes 67 UI styles, 25 chart types, font pairing, and UX guidelines.
type: domain
---

# Frontend Excellence

## Overview

**Core principle:** Great UIs are not accidents — they are the result of deliberate design decisions grounded in visual language, accessibility, performance, and data communication.

This skill provides **UI/UX intelligence** for web and app developers: style selection, chart selection, typography, accessibility, performance, and SEO.

**Announce at start:** "I'm using the PRISM skill for UI/UX design patterns."

---

## Entry Point — First 5 Minutes

When invoked, determine what type of frontend work is needed before applying patterns:

```
FRONTEND CONTEXT ASSESSMENT:

"What are you building or fixing?"
A) New UI / design system from scratch
B) Existing UI — adding a feature
C) Dashboard / data visualization
D) Landing page / marketing site
E) Mobile app (React Native / Flutter)
F) Accessibility audit / fix
G) Performance problem (slow LCP, CLS, INP)
H) Debugging a visual bug

→ Go to the relevant section.
```

**Type → Section mapping:**
- A → UI Style Selection → Design System Quick-Start
- B → follow existing style, check Anti-Pattern Database
- C → Data Visualization (chart selection) + Dashboard Styles
- D → Landing Page Styles + SEO Checklist
- E → Responsive Design + Touch guidelines
- F → Accessibility Checklist
- G → Performance Budget → Performance Checklist
- H → run `hunter`, then Anti-Pattern Database

**After identifying type, confirm two things:**
1. "Who is the primary user — general public, internal team, or technical users?"
2. "What is the primary metric — conversion, engagement, readability, or real-time data?"

These two answers determine style choice and chart selection throughout.

---

## UI Style Selection

### Style Decision Framework

Before writing any UI code, identify:

1. **Industry** — Finance, Healthcare, Tech/SaaS, E-commerce, Creative, Lifestyle, Government
2. **Audience** — Age, tech literacy, accessibility needs
3. **Mood** — Professional/trustworthy, playful/energetic, premium/luxury, technical
4. **Platform** — Web app, landing page, dashboard, mobile, AR/VR

### Style Catalogue (67 Styles)

#### General Styles

| Style | Primary Colors | Key Characteristics | Best For |
|-------|---------------|---------------------|----------|
| **Minimalism / Swiss** | Monochrome, Black, White | Clean, spacious, functional, high contrast | Documentation, SaaS, portfolios |
| **Neumorphism** | Soft pastels, grey | Soft 3D embossed, rounded corners 12-16px | iOS apps, personal dashboards |
| **Glassmorphism** | Translucent white, vibrant accents | Frosted glass, blurred background, layered | Hero sections, cards, sidebars |
| **Brutalism** | Primary colors (Red, Blue, Yellow) | Raw, stark, high contrast, sharp corners | Bold agencies, art platforms |
| **3D & Hyperrealism** | Navy, Forest Green, Gold | WebGL/Three.js, realistic textures | Product showcases, marketing |
| **Vibrant & Block-based** | Neon Green, Electric Purple | Bold, geometric shapes, energetic | Entertainment, gaming, Gen Z |
| **Dark Mode (OLED)** | Deep Black, Midnight Blue | Eye-friendly, power-efficient | Developer tools, media apps |
| **Accessible & Ethical** | High contrast primaries | WCAG AAA, large text, keyboard nav | Healthcare, government, enterprise |
| **Claymorphism** | Pastel (Peach, Baby Blue, Mint) | Soft 3D, chunky, toy-like, bubbly | Kids apps, playful onboarding |
| **Aurora UI** | Blue-Orange, Purple-Yellow gradients | Northern Lights mesh gradient, vibrant | AI products, creative tools |
| **Retro-Futurism** | Neon Blue, Hot Pink, Cyan | 80s aesthetic, CRT scanlines, synthwave | Music apps, nostalgia brands |
| **Flat Design** | Bright solids (Red, Orange, Blue) | 2D, no shadows, clean lines | Material design, Google-style apps |
| **Skeuomorphism** | Realistic wood, leather, metal | Texture, depth, real-world metaphors | Audio tools, creative software |
| **Liquid Glass** | Iridescent, translucent | Flowing glass, morphing, fluid effects | Premium product sites, Apple-style |
| **Motion-Driven** | Bold colors emphasizing movement | Animation-heavy, micro-interactions | Storytelling, marketing sites |
| **Micro-interactions** | Subtle color shifts | Small animations, gesture-based, tactile | Form UX, banking apps |
| **Inclusive Design** | WCAG AAA contrast, symbol-based | Color-blind friendly, haptic | Universal apps, public services |
| **Zero Interface** | Neutral, subtle feedback | Voice-first, gesture-based, AI-driven | Smart home, conversational UI |
| **Neubrutalism** | Yellow, Red, Blue, Black borders | Bold borders, hard shadows, Gen Z | Startups, Figma-style tools |
| **Bento Box Grid** | Neutral + brand accent | Modular cards, Apple-style | Feature showcases, portfolios |
| **Y2K Aesthetic** | Hot Pink, Cyan, Silver | Chrome, metallic, iridescent | Fashion, nostalgia, gen-Z brands |
| **Cyberpunk UI** | Matrix Green, Magenta, Cyan | Neon on dark, HUD, glitch, dystopian | Gaming, sci-fi, crypto |
| **Organic Biophilic** | Forest Green, Earth Brown | Nature shapes, sustainable, flowing | Wellness, eco brands |
| **AI-Native UI** | AI Purple, Success Green | Chatbot, conversational, minimal chrome | AI assistants, LLM products |
| **Memphis Design** | Hot Pink, Yellow, Teal | 80s, postmodern, geometric shapes | Creative agencies, lifestyle |
| **Vaporwave** | Pink, Cyan, Mint, Purple | Synthwave, nostalgic, glitch | Music, art, aesthetic brands |
| **Exaggerated Minimalism** | Black, White, single accent | Oversized type, high contrast, statement | Luxury fashion, editorial |
| **Kinetic Typography** | Flexible, high contrast | Motion text, animated type, typing effect | Intro screens, marketing |
| **Swiss Modernism 2.0** | Black, White, single accent | Grid system, modular, international style | Architecture, editorial |
| **HUD / Sci-Fi FUI** | Neon Cyan, Holographic Blue | Futuristic, wireframe, neon, transparency | Data platforms, defense UI |
| **Pixel Art** | NES Palette, brights | Retro, 8-bit, gaming, blocky | Games, indie tools |
| **Spatial UI (VisionOS)** | Frosted Glass, vibrant accents | Depth, immersion, translucent, gaze | AR/VR, Apple Vision Pro |
| **E-Ink / Paper** | Off-White, Ink Black | Paper-like, high contrast, calm | Reading apps, e-readers |
| **Bauhaus** | Red, Blue, Yellow, Black | Geometric, constructivist, hard shadows | Architecture, education |

#### Landing Page Styles

| Style | When to Use |
|-------|-------------|
| **Hero-Centric** | Brand awareness, large visual impact needed |
| **Conversion-Optimized** | Lead gen, single CTA, form-focused |
| **Feature-Rich Showcase** | SaaS product with many features |
| **Minimal & Direct** | Visual-centric products, white space heavy |
| **Social Proof-Focused** | Testimonials prominent, B2B trust-building |
| **Interactive Product Demo** | Embedded mockup, step-by-step guide |
| **Trust & Authority** | Certificates, credentials, case studies |
| **Storytelling-Driven** | Narrative flow, emotional messaging |

#### Dashboard Styles

| Style | When to Use |
|-------|-------------|
| **Data-Dense** | Multiple charts, KPI cards, minimal padding |
| **Executive** | High-level KPIs, at-a-glance summary |
| **Real-Time Monitoring** | Live updates, status indicators, alerts |
| **Heat Map** | Intensity visualization, time patterns |
| **Drill-Down Analytics** | Hierarchical exploration, expandable |
| **Comparative Analysis** | Side-by-side metrics, period comparisons |
| **Predictive Analytics** | Forecast lines, confidence intervals |
| **Financial** | Revenue metrics, P&L, budget tracking |
| **Sales Intelligence** | Deal pipeline, territory performance |

---

## Data Visualization — Chart Selection

**Rule: Choose chart based on what the data needs to communicate, not aesthetics.**

| Data Type | Chart | When to Use |
|-----------|-------|-------------|
| Trend over time | **Line** | Time axis; observe rise/fall/rate of change |
| Compare categories | **Bar** | Rank discrete values, ≤15 categories |
| Part-to-whole | **Pie / Donut** | ≤5 categories; dominant segment vs rest |
| Correlation / clusters | **Scatter** | Two continuous variables, find relationships |
| Intensity across 2D grid | **Heat Map** | Activity by hour×day, density patterns |
| Geographic distribution | **Choropleth Map** | Regional data, spatial insight |
| Sequential funnel / drop-off | **Funnel** | Conversion stages, multi-step process |
| KPI vs target | **Gauge** | Single metric against threshold |
| Forecast with uncertainty | **Line + Confidence Band** | Historical + predicted with ranges |
| Anomaly detection | **Line + Highlights** | Monitor for outliers, spikes, dips |
| Hierarchical proportions | **Treemap** | Size relationships within hierarchy |
| Flow between nodes | **Sankey** | Multi-source, multi-target distribution |
| Cumulative changes | **Waterfall** | P&L, how components add to final total |
| Multi-variable comparison | **Radar / Spider** | 5–8 attributes, compare entities |
| Financial OHLC | **Candlestick** | Trading context, Open/High/Low/Close |
| Network topology | **Network Graph** | Social graphs, system dependencies |
| Statistical distribution | **Box Plot** | Spread, median, outliers across groups |
| Multiple KPIs compact | **Bullet** | Space-constrained dashboards |
| Percentage progress | **Waffle** | What fraction of whole is filled |
| Nested proportions | **Sunburst** | Hierarchy + relative size together |
| Root cause decomposition | **Decomposition Tree** | Drill into metric contributors |
| Real-time streaming | **Streaming Area** | IoT/ops data ≥1Hz, live monitoring |
| Text sentiment | **Word Cloud** | NLP output, text corpus exploration |
| Process flow analysis | **Process Map** | Event logs, bottleneck visualization |
| 3D spatial / scientific | **3D Scatter / Surface** | Z-axis carries essential information |

---

## Typography — Font Pairing

### Pairing Strategies

**Serif + Sans (Luxury / Editorial)**
- `Playfair Display` + `Inter` — Premium, fashion, high-end e-commerce
- `EB Garamond` + `Lato` — Legal, academic, formal
- `Cormorant` + `Nunito Sans` — Ultra-luxury, editorial

**Sans + Sans (Modern / Professional)**
- `Poppins` + `Open Sans` — SaaS, corporate, balanced
- `Space Grotesk` + `DM Sans` — Tech startups, developer tools
- `Inter` alone — Universal system font, maximum compatibility

**Display + Body (Impact)**
- `Bebas Neue` + `Source Sans 3` — Sports, action, marketing
- `Clash Display` + `Cabinet Grotesk` — Bold agencies

**Developer / Technical**
- `JetBrains Mono` + `IBM Plex Sans` — Developer tools, terminals
- `Fira Code` + `Source Sans 3` — Code editors, technical docs

**Domain Defaults**

| Domain | Heading | Body |
|--------|---------|------|
| Tech / SaaS | Space Grotesk | DM Sans |
| Finance / Banking | IBM Plex Sans | IBM Plex Sans |
| Healthcare | Figtree | Noto Sans |
| Legal | EB Garamond | Lato |
| E-commerce | Poppins | Open Sans |
| Creative Agency | Clash Display | Cabinet Grotesk |
| Education | Nunito | Open Sans |
| Accessibility-first | Atkinson Hyperlegible | Atkinson Hyperlegible |
| Multilingual | Noto (family) | Noto (family) |

### Typography Rules

```css
/* Core rules */
body { line-height: 1.5; }           /* Minimum; 1.6-1.75 for body text */
p { max-width: 65ch; }               /* 65-75 characters per line */
h1 { font-size: clamp(2rem, 5vw, 4rem); }  /* Fluid type scaling */
* { font-display: swap; }            /* Prevent FOIT */
```

---

## Accessibility (WCAG 2.1 AA Minimum)

### Contrast Requirements

| Text Type | Minimum Ratio | Target |
|-----------|--------------|--------|
| Normal text (<18px) | 4.5:1 | 7:1 (AAA) |
| Large text (≥18px bold, ≥24px) | 3:1 | 4.5:1 |
| UI components / graphics | 3:1 | 4.5:1 |
| Decorative / disabled | No requirement | — |

### Checklist

```markdown
## Accessibility Pre-Delivery Checklist

### Vision
- [ ] Color contrast ≥ 4.5:1 for all text (tool: axe, Colour Contrast Analyser)
- [ ] Color NOT the only means of conveying info (add icon/label alongside)
- [ ] Descriptive alt text on all images (empty alt="" for decorative)
- [ ] All text is readable without color

### Keyboard & Screen Reader
- [ ] All interactive elements reachable by Tab key
- [ ] Focus ring visible on all interactive elements
- [ ] Logical tab order matches visual order
- [ ] ARIA labels on icon-only buttons
- [ ] aria-live regions for dynamic content updates
- [ ] Errors announced via aria-live="polite"

### Semantic Structure
- [ ] Single <h1> per page, heading hierarchy (h1→h2→h3, no skips)
- [ ] Landmark regions: <header>, <nav>, <main>, <footer>
- [ ] Form inputs have <label> (for= or aria-labelledby)
- [ ] Error messages below relevant fields (not just top-of-form)

### Touch & Motor
- [ ] Touch targets ≥ 44×44px
- [ ] ≥ 8px gap between adjacent touch targets
- [ ] No hover-only interactions (touch equivalent exists)
- [ ] Confirmation dialog for destructive actions

### Motion
- [ ] Animations respect prefers-reduced-motion
- [ ] No infinite animations except loaders
- [ ] Animation duration: 150–300ms
```

---

## Performance Budget

### Core Web Vitals Targets

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5–4s | > 4s |
| INP (Interaction to Next Paint) | < 200ms | 200–500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1–0.25 | > 0.25 |

### Bundle Size Targets

| Asset | Budget | Technique |
|-------|--------|-----------|
| JS (initial) | < 300KB gzipped | Code splitting, tree shaking |
| CSS | < 50KB gzipped | Purge unused, critical CSS inline |
| Images | WebP/AVIF, lazy loaded | `loading="lazy"`, `srcset` |
| Fonts | ≤ 2 font files | `font-display: swap`, preload |
| Total page weight | < 1MB | Audit with Lighthouse |

### Performance Checklist

```markdown
## Performance Pre-Delivery Checklist

- [ ] Images: WebP/AVIF format, correct srcset, loading="lazy" below fold
- [ ] LCP image: preloaded with <link rel="preload">
- [ ] JS: route-based code splitting (dynamic import)
- [ ] JS: tree-shaking verified (no dead code)
- [ ] CSS: critical CSS inlined, rest deferred
- [ ] Fonts: font-display: swap, preconnect to fonts.googleapis.com
- [ ] Bundle: analyzed with bundle-analyzer or rollup-visualizer
- [ ] Cache: cache-control headers set for static assets
- [ ] Lighthouse score: Performance ≥ 90
```

---

## Responsive Design

### Breakpoints (Mobile-First)

```css
/* Mobile first — start with base (320-375px) */
/* sm: */ @media (min-width: 640px)  { }  /* Large phone */
/* md: */ @media (min-width: 768px)  { }  /* Tablet */
/* lg: */ @media (min-width: 1024px) { }  /* Desktop */
/* xl: */ @media (min-width: 1280px) { }  /* Large desktop */
/* 2xl:*/ @media (min-width: 1536px) { }  /* Ultra-wide */
```

### Responsive Rules

```markdown
- [ ] Tested at 320px (min), 375px, 414px, 768px, 1024px, 1440px
- [ ] No horizontal scroll at any breakpoint
- [ ] Images scale responsively (max-width: 100%)
- [ ] Body font ≥ 16px at all sizes (prevents iOS zoom)
- [ ] viewport meta: <meta name="viewport" content="width=device-width, initial-scale=1">
- [ ] Touch targets scale up on mobile (≥44px)
- [ ] Fixed elements don't obscure content (use dvh for mobile viewport)
- [ ] Text line length capped: 65-75ch desktop, 45-55ch mobile
```

---

## SEO Checklist

```markdown
## SEO Pre-Delivery Checklist

### Meta Tags
- [ ] <title> tag: 50-60 characters, includes primary keyword
- [ ] <meta name="description">: 120-158 characters
- [ ] Open Graph: og:title, og:description, og:image (1200×630px), og:url
- [ ] Twitter Card: twitter:card, twitter:title, twitter:description, twitter:image

### Structured Data
- [ ] JSON-LD for: Organization, WebPage, BreadcrumbList (at minimum)
- [ ] Product pages: Product schema with price, availability
- [ ] Blog posts: Article schema with author, publishDate

### Technical SEO
- [ ] Canonical URL on every page
- [ ] robots.txt present and correct
- [ ] XML sitemap generated and submitted
- [ ] All internal links use crawlable <a href> (not JS-only)
- [ ] 404 page returns HTTP 404 status

### Core Web Vitals
- [ ] Lighthouse SEO score ≥ 90
- [ ] No broken links (internal or external)
- [ ] Images have descriptive alt text (also for SEO)
```

---

## UX Guidelines Summary

### Animation
- Max 1–2 animated elements per view
- Duration: 150–300ms (use CSS custom properties)
- Always honor `prefers-reduced-motion: reduce`
- Reserve infinite animation for loading states only

### Forms
- Every input paired with visible `<label>`
- Error messages below the relevant field (not top-of-form only)
- Validate on blur, not on every keystroke
- Required fields marked with text (not just `*`)
- Support browser autofill (`autocomplete` attributes)
- Show password toggle on password inputs

### Feedback
- Operations >300ms: show spinner or skeleton
- Toast messages auto-dismiss after 3–5 seconds
- Multi-step flows: show progress indicator
- Empty states: helpful message + action button
- Errors: explain what went wrong + recovery path

### Navigation
- Sticky headers: account for fixed element overlap
- Active state clearly visible on current page/section
- Back button always works (URL reflects state)
- Breadcrumbs for hierarchies >2 levels deep

---

## Anti-Pattern Database

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Color-only error indication | Fails color-blind users | Add icon + text label |
| Hover-only interactions | Fails touch devices | Add tap equivalent |
| Missing focus ring | Fails keyboard users | `outline: 2px solid currentColor; outline-offset: 2px` |
| Auto-playing video/audio | Disruptive | Default to muted, user-triggered |
| Fixed font size in px | Breaks user font preferences | Use rem units |
| Layout shift on load | High CLS, jarring | Reserve space for async content |
| Infinite scroll without position restore | Can't navigate back | Add URL pagination anchor |
| Disabled button with no tooltip | User doesn't know why | Explain why it's disabled |
| Form submits on Enter in multi-field form | Accidental submission | Only submit on explicit click |
| Modal without focus trap | Focus escapes to background | Trap focus within modal |
| Aggressive redirect (no 404) | Hides broken links | Return proper 404 status |
| Low contrast placeholder text | Invisible on mobile | Min 3:1 contrast for placeholders |

---

## Design System Quick-Start

When starting a UI project, establish these in order:

```markdown
## Design Tokens (establish first)
1. Color palette: primary, secondary, neutral, semantic (error/warning/success/info)
2. Typography scale: base (16px), sm, md, lg, xl, 2xl, 3xl, 4xl
3. Spacing scale: 4px base unit → 4, 8, 12, 16, 24, 32, 48, 64, 96, 128
4. Border radius: none, sm(4px), md(8px), lg(12px), xl(16px), full
5. Shadow scale: none, sm, md, lg, xl
6. Breakpoints: 640, 768, 1024, 1280, 1536

## Component Priority Order
1. Button (variants: primary, secondary, ghost, danger)
2. Input + Label + Error
3. Card
4. Modal/Dialog
5. Navigation (header + sidebar or top nav)
6. Table
7. Form
```

---

## Integration with Superpowers

**Used with:**

| Skill | Integration |
|-------|-------------|
| `forge` | Write Playwright/Cypress a11y tests before component code |
| `hunter` | Debug CLS, LCP, INP regressions with performance profiler |
| `sentinel` | Run Lighthouse + axe before claiming UI work done |
| `chronicle` | Store successful design patterns per domain/industry |
| `architect` | Use style catalogue for visual direction questions |

---

## Final Checklist

Before claiming frontend work complete:

- [ ] UI style chosen and documented (from 67 styles catalogue)
- [ ] Charts match data type (from 25 chart types guide)
- [ ] Font pairing applied from domain defaults
- [ ] Color contrast passes 4.5:1 minimum
- [ ] All interactive elements keyboard-accessible
- [ ] Touch targets ≥ 44×44px
- [ ] `prefers-reduced-motion` respected
- [ ] LCP < 2.5s, CLS < 0.1 (measured with Lighthouse)
- [ ] Bundle size within budget (JS < 300KB)
- [ ] Meta tags and Open Graph complete
- [ ] Responsive tested at 320px, 768px, 1440px
- [ ] Anti-pattern review passed
