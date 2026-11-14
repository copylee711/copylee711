"""Build the static, animated SVG assets for the profile README.

Each asset is written in a dark and a light variant (assets/<name>-dark.svg,
assets/<name>-light.svg); the README picks one via <picture> + prefers-color-scheme.

Usage: python .github/scripts/build_assets.py
"""
import html
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "assets"

MONO = "'JetBrains Mono','Cascadia Code','SF Mono',Consolas,monospace"
SANS_LIGHT = "'Helvetica Neue','Segoe UI Light','Segoe UI',Arial,sans-serif"

THEMES = {
    "dark": dict(
        bg="#0a0a0b", ink="#ffffff", glow=".09", dots=".07", vignette="#000000", vig_op=".75",
        title="#c9ccd2", title_hi="#ffffff", eyebrow="#6e737b", sub="#8a9099", meta="#4f545b", pulse="#9aa3ad",
        hair=".45", frame=".08", orbit1=".035", orbit2=".045", orbit_dot=".5",
        sec_num="#5c6370", sec_title="#e4e6ea", sec_cap="#6e737b",
    ),
    "light": dict(
        bg="#fbfbfc", ink="#0b0c0e", glow=".05", dots=".08", vignette="#e9ebef", vig_op=".9",
        title="#2b2f36", title_hi="#9aa1ab", eyebrow="#8c959f", sub="#57606a", meta="#8c959f", pulse="#57606a",
        hair=".35", frame=".09", orbit1=".05", orbit2=".07", orbit_dot=".45",
        sec_num="#8c959f", sec_title="#1f2328", sec_cap="#8c959f",
    ),
}

# 终端配色：暗色 One Dark，亮色 One Light
TERM = {
    "dark": dict(bg="#1e2127", bar="#282c34", border="#ffffff", border_op=".1", sep_op=".35",
                 fg="#abb2bf", cmd="#61afef", arg="#e5c07b", str="#98c379", key="#c678dd", var="#e06c75",
                 num="#d19a66", dim="#5c6370", cy="#56b6c2", ok="#98c379", cursor="#528bff"),
    "light": dict(bg="#fafafa", bar="#eaeaeb", border="#000000", border_op=".1", sep_op=".08",
                  fg="#383a42", cmd="#4078f2", arg="#c18401", str="#50a14f", key="#a626a4", var="#e45649",
                  num="#986801", dim="#a0a1a7", cy="#0184bc", ok="#50a14f", cursor="#526fff"),
}


# ---------------------------------------------------------------- header
def header(t: dict) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 340" width="1200" height="340" role="img" aria-label="copylee711">
  <defs>
    <radialGradient id="light" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="{t['ink']}" stop-opacity="{t['glow']}"/>
      <stop offset="1" stop-color="{t['ink']}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="{t['ink']}" fill-opacity="{t['dots']}"/>
    </pattern>
    <radialGradient id="vignette" cx="50%" cy="50%" r="70%">
      <stop offset=".55" stop-color="{t['vignette']}" stop-opacity="0"/>
      <stop offset="1" stop-color="{t['vignette']}" stop-opacity="{t['vig_op']}"/>
    </radialGradient>
    <linearGradient id="sweep" gradientUnits="userSpaceOnUse" x1="-600" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="{t['title']}"/>
      <stop offset=".44" stop-color="{t['title']}"/>
      <stop offset=".5" stop-color="{t['title_hi']}"/>
      <stop offset=".56" stop-color="{t['title']}"/>
      <stop offset="1" stop-color="{t['title']}"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="0 0;1800 0;1800 0" keyTimes="0;.6;1" dur="7s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="hair" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['ink']}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{t['ink']}" stop-opacity="{t['hair']}"/>
      <stop offset="1" stop-color="{t['ink']}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="card"><rect width="1200" height="340" rx="16"/></clipPath>
  </defs>
  <style>
    .glow {{ animation: drift 16s ease-in-out infinite; }}
    @keyframes drift {{ 0%,100% {{ transform: translate(-180px, 0); }} 50% {{ transform: translate(180px, 10px); }} }}
    .title {{ font: 300 84px {SANS_LIGHT}; letter-spacing: 14px; opacity: 0; animation: fadeUp 1.6s cubic-bezier(.16,1,.3,1) .2s forwards; }}
    .eyebrow {{ font: 500 13px {MONO}; letter-spacing: 6px; fill: {t['eyebrow']}; opacity: 0; animation: fade 1.4s ease .1s forwards; }}
    .sub {{ font: 400 15px {MONO}; letter-spacing: 5px; fill: {t['sub']}; opacity: 0; animation: fadeUp 1.6s cubic-bezier(.16,1,.3,1) .7s forwards; }}
    .meta {{ font: 400 12px {MONO}; letter-spacing: 3px; fill: {t['meta']}; opacity: 0; animation: fade 1.4s ease 1.2s forwards; }}
    @keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes fade {{ to {{ opacity: 1; }} }}
    .rule {{ stroke-dasharray: 360; stroke-dashoffset: 360; animation: draw 1.8s cubic-bezier(.65,0,.35,1) .6s forwards; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    .pulse {{ animation: pulse 2.4s ease-in-out infinite; }}
    @keyframes pulse {{ 0%,100% {{ opacity: .35; }} 50% {{ opacity: 1; }} }}
    .orbit {{ transform-box: view-box; transform-origin: 600px 170px; animation: spin 60s linear infinite; }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @media (prefers-reduced-motion: reduce) {{
      * {{ animation: none !important; }}
      .title, .eyebrow, .sub, .meta {{ opacity: 1; }}
      .rule {{ stroke-dashoffset: 0; }}
    }}
  </style>
  <g clip-path="url(#card)">
    <rect width="1200" height="340" fill="{t['bg']}"/>
    <rect width="1200" height="340" fill="url(#dots)"/>
    <ellipse class="glow" cx="600" cy="150" rx="420" ry="220" fill="url(#light)"/>
    <g class="orbit" fill="none" stroke="{t['ink']}">
      <circle cx="600" cy="170" r="520" stroke-opacity="{t['orbit1']}"/>
      <circle cx="600" cy="170" r="380" stroke-opacity="{t['orbit2']}" stroke-dasharray="2 8"/>
      <circle cx="980" cy="170" r="2" fill="{t['ink']}" fill-opacity="{t['orbit_dot']}" stroke="none"/>
    </g>
    <rect width="1200" height="340" fill="url(#vignette)"/>
    <text x="600" y="102" text-anchor="middle" class="eyebrow">— DEVELOPER · BUILDER —</text>
    <text x="607" y="190" text-anchor="middle" class="title" fill="url(#sweep)">copylee711</text>
    <line class="rule" x1="420" y1="222" x2="780" y2="222" stroke="url(#hair)" stroke-width="1"/>
    <text x="600" y="258" text-anchor="middle" class="sub">CODE  ·  CRAFT  ·  CURIOSITY</text>
    <g class="meta">
      <circle class="pulse" cx="40" cy="306" r="3" fill="{t['pulse']}"/>
      <text x="54" y="310">AVAILABLE FOR COLLABORATION</text>
      <text x="1160" y="310" text-anchor="end">EST. 2026</text>
    </g>
    <rect x=".5" y=".5" width="1199" height="339" rx="16" fill="none" stroke="{t['ink']}" stroke-opacity="{t['frame']}"/>
  </g>
</svg>
"""


# ---------------------------------------------------------------- section titles
SECTIONS = [
    ("about", "01", "ABOUT", "WHO I AM"),
    ("stack", "02", "STACK", "TOOLS I BUILD WITH"),
    ("activity", "03", "ACTIVITY", "WHAT I'VE BEEN UP TO"),
]


def section(t: dict, num: str, title: str, caption: str) -> str:
    W, H = 860, 64
    title_w = len(title) * 22  # 字距较大时的估算宽度
    line_x1 = 74 + title_w + 18
    cap_w = len(caption) * 9.2
    line_x2 = W - cap_w - 18
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{title.title()}">
  <style>
    .n {{ font: 500 12px {MONO}; letter-spacing: 2px; fill: {t['sec_num']}; }}
    .t {{ font: 300 24px {SANS_LIGHT}; letter-spacing: 8px; fill: {t['sec_title']}; }}
    .c {{ font: 500 11px {MONO}; letter-spacing: 3px; fill: {t['sec_cap']}; }}
    .in {{ opacity: 0; animation: in 1.2s cubic-bezier(.16,1,.3,1) forwards; }}
    @keyframes in {{ from {{ opacity: 0; transform: translateX(-10px); }} to {{ opacity: 1; transform: none; }} }}
    .ln {{ stroke-dasharray: {W}; stroke-dashoffset: {W}; animation: draw 1.6s cubic-bezier(.65,0,.35,1) .3s forwards; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    .dot {{ animation: pulse 2.4s ease-in-out infinite; }}
    @keyframes pulse {{ 0%,100% {{ opacity: .3; }} 50% {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} .in {{ opacity: 1; }} .ln {{ stroke-dashoffset: 0; }} }}
  </style>
  <g class="in">
    <text x="0" y="40" class="n">{num}</text>
    <circle class="dot" cx="{40 + 8}" cy="35.5" r="2.5" fill="{t['sec_num']}"/>
    <text x="74" y="43" class="t">{html.escape(title)}</text>
  </g>
  <line class="ln" x1="{line_x1:.0f}" y1="36" x2="{line_x2:.0f}" y2="36" stroke="{t['ink']}" stroke-opacity="{t['hair']}" stroke-width="1"/>
  <text x="{W}" y="40" text-anchor="end" class="c in" style="animation-delay:.5s">{html.escape(caption)}</text>
</svg>
"""


# ---------------------------------------------------------------- terminal
def terminal(c: dict) -> str:
    lines = [
        ("cmd", [("whoami", "cmd")]),
        ("out", [("copylee711", "var"), (" — building tools for AI agents, desktop & Android", "fg")]),
        ("cmd", [("cat ", "cmd"), ("./interests.json", "arg")]),
        ("out", [("{ ", "fg"), ('"focus"', "var"), (": [", "fg"), ('"ai-agents"', "str"), (", ", "fg"), ('"mcp"', "str"),
                 (", ", "fg"), ('"local-first"', "str"), (", ", "fg"), ('"android"', "str"), ("] }", "fg")]),
        ("cmd", [("ls ", "cmd"), ("-F ", "key"), ("~/projects", "arg")]),
        ("out", [("dsh-computer-use/", "cmd"), ("   ", "fg"), ("dsh-office/", "cmd"), ("   ", "fg"),
                 ("dsh-remote-control/", "cmd"), ("   ", "fg"), ("dsh-proxy/", "cmd")]),
        ("out", [("Super-Knowledge-Base/", "cmd"), ("   ", "fg"), ("twinfile/", "cmd"), ("   ", "fg"),
                 ("syncboard/", "cmd"), ("   ", "fg"), ("homepage/", "cmd")]),
        ("cmd", [("git ", "cmd"), ("log ", "fg"), ("--oneline ", "key"), ("-1", "num")]),
        ("out", [("a1b2c3d ", "arg"), ("(", "arg"), ("HEAD -> ", "cy"), ("main", "str"), (") ", "arg"),
                 ("feat(computer-use): let agents drive the desktop", "fg")]),
        ("cmd", [("echo ", "cmd"), ("$MOTTO", "var")]),
        ("out", [("Simple things, done well.", "str")]),
    ]
    W, X0, Y0, LH, CW = 860, 32, 96, 38, 10.2
    PW = 4.6 * CW

    def spans(segs):
        return "".join(f'<tspan fill="{c[k]}">{html.escape(s)}</tspan>' for s, k in segs)

    def prompt(y):
        return (f'<text x="{X0}" y="{y}" class="t" fill="{c["ok"]}">➜</text>'
                f'<text x="{X0 + 2.4 * CW:.1f}" y="{y}" class="t" fill="{c["cy"]}" font-weight="700">~</text>')

    t, parts = 0.6, []
    for i, (kind, segs) in enumerate(lines):
        y = Y0 + i * LH
        txt = "".join(s for s, _ in segs)
        if kind == "cmd":
            dur = max(0.4, len(txt) * 0.055)
            vals = ";".join(str(round(k * CW + 2)) for k in range(len(txt) + 1))
            parts.append(
                f'  <g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>\n'
                f'    {prompt(y)}\n'
                f'    <clipPath id="c{i}"><rect x="{X0 + PW:.1f}" y="{y - 22}" height="30" width="0"><animate attributeName="width" '
                f'values="{vals}" calcMode="discrete" begin="{t + 0.3:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>\n'
                f'    <text x="{X0 + PW:.1f}" y="{y}" class="t" fill="{c["fg"]}" clip-path="url(#c{i})">{spans(segs)}</text>\n  </g>')
            t += 0.3 + dur + 0.25
        else:
            parts.append(f'  <text x="{X0}" y="{y}" class="t" fill="{c["fg"]}" opacity="0">{spans(segs)}'
                         f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="0.3s" fill="freeze"/></text>')
            t += 0.55
    yc = Y0 + len(lines) * LH
    H = yc + 36
    body = "\n".join(parts)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="about copylee711">
  <style>
    .t {{ font-family: {MONO}; font-size: 17px; white-space: pre; }}
    .cur {{ animation: blink 1s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
  </style>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{c['bg']}" stroke="{c['border']}" stroke-opacity="{c['border_op']}"/>
  <path d="M.5 12.5a12 12 0 0 1 12-12h{W - 25}a12 12 0 0 1 12 12v32H.5z" fill="{c['bar']}"/>
  <line x1=".5" y1="44.5" x2="{W - .5}" y2="44.5" stroke="#000" stroke-opacity="{c['sep_op']}"/>
  <circle cx="24" cy="22" r="6.5" fill="#ff5f57"/><circle cx="46" cy="22" r="6.5" fill="#febc2e"/><circle cx="68" cy="22" r="6.5" fill="#28c840"/>
  <text x="{W / 2}" y="27" text-anchor="middle" style="font:13px {MONO};fill:{c['dim']}">copylee711@github: ~ — zsh</text>
{body}
  <g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>
    {prompt(yc)}
    <rect class="cur" x="{X0 + PW:.1f}" y="{yc - 16}" width="10" height="20" fill="{c['cursor']}"/>
  </g>
</svg>
"""


# ---------------------------------------------------------------- divider
def divider(t: dict) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 12" width="1200" height="12" preserveAspectRatio="none">
  <defs>
    <linearGradient id="base" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['sub']}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{t['sub']}" stop-opacity=".35"/>
      <stop offset="1" stop-color="{t['sub']}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="glint" gradientUnits="userSpaceOnUse" x1="-240" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="{t['title']}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{t['title']}" stop-opacity=".9"/>
      <stop offset="1" stop-color="{t['title']}" stop-opacity="0"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="0 0;1440 0;1440 0" keyTimes="0;.7;1" dur="6s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>
  <rect x="0" y="5.5" width="1200" height="1" fill="url(#base)"/>
  <rect x="0" y="5.5" width="1200" height="1" fill="url(#glint)"/>
</svg>
"""


def main():
    OUT.mkdir(exist_ok=True)
    for mode, t in THEMES.items():
        files = {
            f"header-{mode}.svg": header(t),
            f"terminal-{mode}.svg": terminal(TERM[mode]),
            f"divider-{mode}.svg": divider(t),
        }
        for key, num, title, cap in SECTIONS:
            files[f"title-{key}-{mode}.svg"] = section(t, num, title, cap)
        for name, svg in files.items():
            (OUT / name).write_text(svg, encoding="utf-8")
            print("wrote", name)


if __name__ == "__main__":
    main()
