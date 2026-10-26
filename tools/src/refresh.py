"""«Жарық» design: a light, calm blue palette over the whole site (light and dark), no ornament band,
a new logo mark, rounded buttons and cards, vertical lab steps joined by a line, a focus ring on the
answer card, segmented «Кеңес / Мысал / Дереккөз» tabs and a floating bottom dock (the progress bar
markup stays). Only CSS and the logo change: no markup, no script.
--accent-ink is the dark accent for text; text on an accent background uses --on-accent.
Usage: python3 -I refresh.py in.html out.html   (run after account.py, before seo.py)"""
import sys
from urllib.parse import quote

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('refresh anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

def mark(tile, ink):
    """Logo: an open book on a rounded tile, the spine as a bookmark."""
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
           '<rect width="32" height="32" rx="9" fill="%s"/>'
           '<g fill="none" stroke="%s" stroke-width="1.9" stroke-linejoin="round" stroke-linecap="round">'
           '<path d="M7 10.2c3.2-1.1 6.3-.8 9 1.2 2.7-2 5.8-2.3 9-1.2v12.2c-3.2-1.1-6.3-.8-9 1.2-2.7-2-5.8-2.3-9-1.2z"/>'
           '<path d="M16 11.4v12.2"/></g>'
           '<path d="M19.5 9.6v5.2l1.6-1.2 1.6 1.2V9.3" fill="%s"/></svg>') % (tile, ink, ink)
    return 'url("data:image/svg+xml,%s")' % quote(svg, safe='')

LIGHT = """--bg: #F5F6FA; --surface: #FFFFFF; --surface-2: #EEF0F6; --line: #E1E4EE; --line-strong: #CDD2E0;
    --ink: #0F1729; --ink-2: #556070; --accent: #3A56E4; --accent-hover: #2B43C0; --accent-soft: #E9EDFF; --accent-ink: #2A3FB8;
    --on-accent: #FFFFFF; --ok: #17673A; --ok-soft: #E3F4EA; --stage-empty: #E1E4EE;
    --gold: var(--accent); --gold-ink: var(--accent-ink); --gold-soft: var(--accent-soft);
    --radius: 12px; --radius-lg: 16px;
    --shadow-sm: 0 1px 2px rgba(15, 23, 41, .05); --shadow: 0 6px 20px rgba(15, 23, 41, .08); --shadow-dock: 0 10px 30px rgba(15, 23, 41, .12);
    --orn-band: none; --orn-motif: none; --brand-mark: %s; color-scheme: light;""" % mark('#3A56E4', '#FFFFFF')
DARK = """--bg: #0D1220; --surface: #151B2B; --surface-2: #1C2438; --line: #2A3349; --line-strong: #3A4560;
    --ink: #E7EBF5; --ink-2: #A3ADC2; --accent: #8FA8FF; --accent-hover: #B0C1FF; --accent-soft: #1E2A52; --accent-ink: #B9C8FF;
    --on-accent: #0D1220; --ok: #6FD39A; --ok-soft: #15301F; --stage-empty: #2A3349;
    --gold: var(--accent); --gold-ink: var(--accent-ink); --gold-soft: var(--accent-soft);
    --shadow-sm: none; --shadow: 0 0 0 1px rgba(255, 255, 255, .04); --shadow-dock: 0 10px 30px rgba(0, 0, 0, .45);
    --brand-mark: %s; color-scheme: dark;""" % mark('#8FA8FF', '#0D1220')

CSS = r"""
<style id="refresh">
  /* «ЖАРЫҚ» — palette, logo, rounded controls, lab steps, answer focus, segmented tabs, bottom dock */
  :root { %(light)s }
  @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { %(dark)s } }
  :root[data-theme="dark"] { %(dark)s }
  body { background: var(--bg); color: var(--ink); }

  /* No ornament band */
  .topbar::after, .wl-top::after { content: none; display: none; }
  .topbar { padding-bottom: 0; box-shadow: none; }

  /* Logo */
  .brand-mark { border-radius: 9px; }

  /* Buttons and fields */
  .btn { border-radius: var(--radius); border-color: var(--line-strong); }
  .btn:hover { background: var(--surface-2); }
  .chip[aria-pressed="true"] { color: var(--on-accent); }
  .btn.primary { background: var(--accent); border-color: var(--accent); color: var(--on-accent); box-shadow: 0 1px 2px rgba(58, 86, 228, .25); }
  .btn.primary:hover { background: var(--accent-hover); border-color: var(--accent-hover); filter: none; }
  .btn:focus-visible, .tab:focus-visible, select:focus-visible, input:focus-visible, textarea:focus-visible, summary:focus-visible,
  .step-btn:focus-visible, .lab-panel-tabs button:focus-visible, .wl-card:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
  input[type=text], input[type=search], select, textarea { border-radius: var(--radius); border-color: var(--line-strong); }
  input:focus, select:focus, textarea:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
  .help-btn .help-q { background: var(--accent); color: var(--on-accent); }
  .acc-avatar { background: var(--accent); color: var(--on-accent); }
  .step-btn.done .step-num, #lab-nav .step-btn.done .step-num { color: var(--on-accent); }
  .lab-q-dot[aria-current="true"] { color: var(--on-accent); }
  .lab-dot[aria-current="step"] .n, .shop-steps li::before, .lab-tip > summary::before { color: var(--on-accent); }
  .wl-trust::before { color: var(--on-accent); }

  /* Header and section tabs */
  .hdr .tabs { border-radius: 14px; background: var(--surface-2); border-color: var(--line); }
  .hdr .tab { border-radius: 10px; }
  .hdr .tab[aria-selected="true"] { background: var(--surface); color: var(--accent-ink); box-shadow: var(--shadow-sm), 0 0 0 1px var(--line); }
  #save-status.save-status.busy { background: var(--accent-soft); color: var(--accent-ink); }

  /* Cards */
  .card, .lib-card, .wl-card, .lab-panel { border-radius: var(--radius-lg); border-color: var(--line); }
  .work-sum { border-radius: var(--radius); border-color: var(--line-strong); }
  .work-panel, .dlg { border-radius: var(--radius-lg); }
  .wl-card:hover { box-shadow: var(--shadow); }
  .wl-photo { border-radius: 20px; }
  .wl-lead p:first-child { border-left-color: var(--accent); }

  /* The answer card: a clear ring while you write */
  .main .card { transition: border-color .15s, box-shadow .15s; }
  .main .card:focus-within { border-color: var(--accent); box-shadow: 0 0 0 4px var(--accent-soft); }
  .main .card textarea:focus, .main .card input:focus { box-shadow: none; }

  /* Side list: vertical steps joined by a line */
  .sidebar h2 { color: var(--ink-2); }
  #lab-nav li { position: relative; }
  #lab-nav li:not(:last-child)::before { content: ""; position: absolute; left: 23px; top: 36px; bottom: -6px; width: 2px;
    border-radius: 2px; background: var(--line); pointer-events: none; }
  #lab-nav li:has(> .step-btn.done):not(:last-child)::before { background: var(--ok); }
  #lab-nav .step-btn { align-items: center; margin-bottom: 4px; border-radius: var(--radius); }
  #lab-nav .step-num { position: relative; z-index: 1; width: 28px; min-width: 28px; height: 28px; border-radius: 50%%;
    background: var(--surface); box-shadow: inset 0 0 0 2px var(--line); }
  #lab-nav .step-btn.done .step-num { background: var(--ok); box-shadow: none; }
  #lab-nav .step-btn[aria-current="step"] { background: var(--accent-soft); color: var(--accent-ink); }
  #lab-nav .step-btn[aria-current="step"] .step-num { background: var(--accent); color: var(--on-accent); box-shadow: 0 0 0 4px var(--accent-soft); }

  /* «Кеңес / Мысал / Дереккөз»: one segmented switch */
  .lab-panel-tabs { gap: 4px; margin: 10px 10px 0; padding: 4px; border: 0; border-radius: var(--radius); background: var(--surface-2); }
  .lab-panel-tabs button { min-height: 44px; border: 0; border-radius: 9px; color: var(--ink-2); }
  .lab-panel-tabs button:hover { color: var(--ink); }
  .lab-panel-tabs button[aria-selected="true"] { background: var(--surface); color: var(--accent-ink); border-bottom-color: transparent;
    box-shadow: var(--shadow-sm), 0 0 0 1px var(--line); }
  .lab-sample { border-left-color: var(--accent); background: var(--accent-soft); }
  .lab-terms button { color: var(--accent-ink); }

  /* Bottom dock: previous · progress · next */
  .footer { margin: 0 16px 12px; padding: 10px 14px; border: 1px solid var(--line); border-radius: var(--radius-lg);
    background: var(--surface); box-shadow: var(--shadow-dock); }
  .progress-fill, .lab-progress-bar span { background: var(--accent); }
  .lab-progress-bar, .progress-track { background: var(--surface-2); box-shadow: inset 0 0 0 1px var(--line); }
  @media (max-width: 900px) {
    .footer { margin: 0 8px max(8px, env(safe-area-inset-bottom, 0px)); padding: 8px 10px; }
  }
  @media print { .footer { box-shadow: none; } }
</style>
""" % {'light': LIGHT, 'dark': DARK}

rep('</style>\n</head>', '</style>' + CSS.rstrip('\n') + '\n</head>')
open(out, 'w', encoding='utf8').write(s)
print('refresh: ok')
