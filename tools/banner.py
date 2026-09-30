"""Generate matching animated space banners (SVG) for the profile and each repo.

GitHub renders README SVGs as images: CSS keyframes and SMIL animate, but
webfonts and scripts don't load, so text uses a system font stack.
"""
import random
import sys
from xml.sax.saxutils import escape

W, H = 1200, 300
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"


def stars(rng, n, w, h):
    out = []
    for i in range(n):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        r = rng.choice([0.6, 0.8, 1.0, 1.0, 1.3, 1.7])
        dur = rng.uniform(2.5, 6.0)
        delay = rng.uniform(0, 6)
        cls = "tw" if rng.random() < 0.55 else ""
        color = rng.choice(["#ffffff", "#ffffff", "#cfd8ff", "#ffe9c4", "#b9f3ff"])
        style = f' style="animation-duration:{dur:.1f}s;animation-delay:-{delay:.1f}s"' if cls else ""
        out.append(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}"{style}/>')
    return "\n    ".join(out)


def banner(title, subtitle, kicker="", seed=7, planet_hue=("#7c5cff", "#2bd2ff"), height=H):
    rng = random.Random(seed)
    h = height
    p1, p2 = planet_hue
    kicker_svg = (
        f'<text x="64" y="{h/2 - 52:.0f}" class="kicker">{escape(kicker)}</text>' if kicker else ""
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-label="{escape(title)}">
  <title>{escape(title)}</title>
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#05060f"/>
      <stop offset="0.55" stop-color="#0d0b24"/>
      <stop offset="1" stop-color="#1b0f3a"/>
    </linearGradient>
    <radialGradient id="neb1" cx="0.78" cy="0.25" r="0.45">
      <stop offset="0" stop-color="{p1}" stop-opacity="0.35"/>
      <stop offset="1" stop-color="{p1}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="neb2" cx="0.15" cy="0.95" r="0.5">
      <stop offset="0" stop-color="{p2}" stop-opacity="0.18"/>
      <stop offset="1" stop-color="{p2}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="planet" cx="0.35" cy="0.3" r="0.8">
      <stop offset="0" stop-color="{p2}"/>
      <stop offset="0.55" stop-color="{p1}"/>
      <stop offset="1" stop-color="#140a33"/>
    </radialGradient>
    <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#c9bfff"/>
    </linearGradient>
    <linearGradient id="streak" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0.9"/>
    </linearGradient>
    <clipPath id="frame"><rect width="{W}" height="{h}" rx="18"/></clipPath>
  </defs>
  <style>
    .tw {{ animation: twinkle 4s ease-in-out infinite; }}
    @keyframes twinkle {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.15; }} }}
    .shoot {{ animation: shoot 9s linear infinite; opacity: 0; }}
    @keyframes shoot {{
      0% {{ transform: translate(0,0); opacity: 0; }}
      2% {{ opacity: 1; }}
      9% {{ transform: translate(-520px,260px); opacity: 0; }}
      100% {{ transform: translate(-520px,260px); opacity: 0; }}
    }}
    .title {{ font: 700 64px {FONT}; letter-spacing: -1px; }}
    .sub {{ font: 400 22px {FONT}; fill: #b8b3e6; }}
    .kicker {{ font: 600 14px {FONT}; fill: {p2}; letter-spacing: 4px; }}
  </style>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{h}" fill="url(#sky)"/>
    <rect width="{W}" height="{h}" fill="url(#neb1)"/>
    <rect width="{W}" height="{h}" fill="url(#neb2)"/>
    {stars(rng, 170, W, h)}
    <g class="shoot"><rect x="980" y="30" width="140" height="2" rx="1" fill="url(#streak)" transform="rotate(-26 1120 31)"/></g>

    <!-- planet + ring -->
    <g transform="translate(1010 {h*0.62:.0f})">
      <ellipse rx="150" ry="30" fill="none" stroke="{p2}" stroke-opacity="0.35" stroke-width="2" transform="rotate(-18)"/>
      <circle r="78" fill="url(#planet)"/>
      <path d="M -150 0 A 150 30 0 0 0 150 0" fill="none" stroke="{p2}" stroke-opacity="0.8" stroke-width="3" transform="rotate(-18)"/>
      <!-- orbiting moon -->
      <g transform="rotate(-18)">
        <circle r="6" fill="#e9e4ff">
          <animateMotion dur="16s" repeatCount="indefinite" path="M 150 0 A 150 30 0 1 1 -150 0 A 150 30 0 1 1 150 0"/>
        </circle>
      </g>
    </g>

    {kicker_svg}
    <text x="64" y="{h/2 + 8:.0f}" class="title" fill="url(#titleGrad)">{escape(title)}</text>
    <text x="66" y="{h/2 + 50:.0f}" class="sub">{escape(subtitle)}</text>
  </g>
</svg>
'''


def footer(seed=11):
    rng = random.Random(seed)
    h = 90
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-label="">
  <defs>
    <linearGradient id="fsky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#05060f" stop-opacity="0"/>
      <stop offset="1" stop-color="#1b0f3a"/>
    </linearGradient>
    <clipPath id="fr"><rect width="{W}" height="{h}" rx="18"/></clipPath>
  </defs>
  <style>
    .tw {{ animation: twinkle 4s ease-in-out infinite; }}
    @keyframes twinkle {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.15; }} }}
  </style>
  <g clip-path="url(#fr)">
    <rect width="{W}" height="{h}" fill="url(#fsky)"/>
    {stars(rng, 60, W, h)}
  </g>
</svg>
'''


if __name__ == "__main__":
    out = sys.argv[1]
    kind = sys.argv[2]
    if kind == "footer":
        svg = footer()
    else:
        title, subtitle = sys.argv[3], sys.argv[4]
        kicker = sys.argv[5] if len(sys.argv) > 5 else ""
        seed = int(sys.argv[6]) if len(sys.argv) > 6 else 7
        hues = tuple(sys.argv[7].split(",")) if len(sys.argv) > 7 else ("#7c5cff", "#2bd2ff")
        svg = banner(title, subtitle, kicker, seed, hues)
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
