"""Generate an animated GitHub stats card (SVG) for the profile README.

Usage: GITHUB_TOKEN=... python profile_stats.py <username> <output.svg>
Only uses the standard library so it runs on a bare Actions runner.
"""
import html
import json
import os
import sys
import urllib.request

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    pullRequests { totalCount }
    contributionsCollection {
      totalCommitContributions
      contributionCalendar { totalContributions }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""

EXCLUDED_LANGS = {"HTML", "CSS", "SCSS", "Less", "Batchfile", "PowerShell", "Shell", "Dockerfile", "Makefile"}
TOP_N = 6


def fetch(login: str, token: str) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]


def summarize(u: dict):
    repos = u["repositories"]["nodes"]
    langs: dict[str, list] = {}
    for repo in repos:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            if name in EXCLUDED_LANGS:
                continue
            entry = langs.setdefault(name, [0, e["node"]["color"] or "#8a9099"])
            entry[0] += e["size"]
    ranked = sorted(langs.items(), key=lambda kv: kv[1][0], reverse=True)
    total = sum(v[0] for _, v in ranked) or 1
    top = [(n, v[0] / total, v[1]) for n, v in ranked[:TOP_N]]
    rest = 1 - sum(p for _, p, _ in top)
    if rest > 0.005:
        top.append(("Other", rest, "#4a4d54"))

    metrics = [
        ("Stars Earned", sum(r["stargazerCount"] for r in repos)),
        ("Commits · 1y", u["contributionsCollection"]["totalCommitContributions"]),
        ("Pull Requests", u["pullRequests"]["totalCount"]),
        ("Contribs · 1y", u["contributionsCollection"]["contributionCalendar"]["totalContributions"]),
        ("Public Repos", u["repositories"]["totalCount"]),
        ("Followers", u["followers"]["totalCount"]),
    ]
    return metrics, top


def render(metrics, langs) -> str:
    W, H = 860, 230
    out = []
    # 左侧：3 列 x 2 行指标
    col_w, x0, y0 = 132, 36, 96
    for i, (label, value) in enumerate(metrics):
        x = x0 + (i % 3) * col_w
        y = y0 + (i // 3) * 74
        d = 0.15 + i * 0.08
        out.append(
            f'<g class="up" style="animation-delay:{d:.2f}s">'
            f'<text x="{x}" y="{y}" class="num">{value:,}</text>'
            f'<text x="{x}" y="{y + 22}" class="lbl">{html.escape(label.upper())}</text></g>'
        )

    # 右侧：语言堆叠条 + 图例
    bx, bw, by = 470, 354, 82
    out.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="8" rx="4" fill="#ffffff" fill-opacity=".06"/>')
    out.append(f'<clipPath id="bar"><rect x="{bx}" y="{by}" width="{bw}" height="8" rx="4"/></clipPath><g clip-path="url(#bar)">')
    cx = bx
    for i, (name, pct, color) in enumerate(langs):
        w = bw * pct
        out.append(
            f'<rect class="grow" style="animation-delay:{0.4 + i * 0.12:.2f}s" x="{cx:.2f}" y="{by}" '
            f'width="{w + 0.5:.2f}" height="8" fill="{color}"/>'
        )
        cx += w
    out.append("</g>")
    for i, (name, pct, color) in enumerate(langs):
        x = bx + (i % 2) * 180
        y = by + 38 + (i // 2) * 26
        out.append(
            f'<g class="up" style="animation-delay:{0.6 + i * 0.08:.2f}s">'
            f'<circle cx="{x + 5}" cy="{y - 4}" r="4.5" fill="{color}"/>'
            f'<text x="{x + 18}" y="{y}" class="lang">{html.escape(name)}</text>'
            f'<text x="{x + 160}" y="{y}" class="pct" text-anchor="end">{pct * 100:.1f}%</text></g>'
        )

    body = "\n  ".join(out)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="GitHub stats">
  <style>
    .h {{ font: 500 12px 'SF Mono','Cascadia Code',Consolas,monospace; letter-spacing: 4px; fill: #6e737b; }}
    .num {{ font: 300 34px 'Helvetica Neue','Segoe UI Light','Segoe UI',Arial,sans-serif; fill: #e4e6ea; }}
    .lbl {{ font: 500 10px 'SF Mono','Cascadia Code',Consolas,monospace; letter-spacing: 1.5px; fill: #6e737b; }}
    .lang {{ font: 400 13px 'Segoe UI','Helvetica Neue',Arial,sans-serif; fill: #c9ccd2; }}
    .pct {{ font: 400 12px 'SF Mono','Cascadia Code',Consolas,monospace; fill: #6e737b; }}
    .up {{ opacity: 0; animation: up .9s cubic-bezier(.16,1,.3,1) forwards; }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
    .grow {{ transform-box: fill-box; transform-origin: left; transform: scaleX(0); animation: grow 1.1s cubic-bezier(.65,0,.35,1) forwards; }}
    @keyframes grow {{ to {{ transform: scaleX(1); }} }}
    @media (prefers-reduced-motion: reduce) {{ .up, .grow {{ animation: none; opacity: 1; transform: none; }} }}
  </style>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="#0a0a0b" stroke="#ffffff" stroke-opacity=".08"/>
  <text x="36" y="44" class="h">GITHUB · STATS</text>
  <text x="470" y="44" class="h">LANGUAGES</text>
  <line x1="436" y1="36" x2="436" y2="{H - 36}" stroke="#ffffff" stroke-opacity=".07"/>
  {body}
</svg>
"""


def main():
    login, out_path = sys.argv[1], sys.argv[2]
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required")
    metrics, langs = summarize(fetch(login, token))
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(render(metrics, langs))
    print(f"wrote {out_path}: {metrics} {[(n, round(p, 3)) for n, p, _ in langs]}")


if __name__ == "__main__":
    main()
