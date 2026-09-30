"""Space-themed SVG panels so the whole profile README reads as one dark scene.

GitHub can't restyle README markdown, so every section is drawn as an image.
Text is wrapped here in Python, because SVG <text> doesn't wrap and
foreignObject isn't reliable everywhere.
"""
import os
import random
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(__file__))
from banner import stars  # noqa: E402

FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
VIOLET, CYAN, LILAC, MUTED, TEXT = "#7c5cff", "#2bd2ff", "#c9bfff", "#aaa4d8", "#ece9ff"

# Rough per-character advance widths for Segoe UI, in ems.
def text_w(s, size, bold=False):
    w = 0.0
    for ch in s:
        if ch in "il.,:;'|!·":
            w += 0.26
        elif ch in "fjrt()[] ":
            w += 0.33
        elif ch in "mwMW":
            w += 0.82
        elif ch.isupper() or ch.isdigit() or ch in "$%&":
            w += 0.60
        else:
            w += 0.52
    return w * size * (1.06 if bold else 1.0)


def wrap(s, max_px, size, bold=False):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        # 15% headroom: Macs render SF Pro and Linux often Arial, both wider than Segoe UI.
        if text_w(trial, size, bold) * 1.15 <= max_px:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def frame(w, h, seed, body, glow=VIOLET, glow2=CYAN, n_stars=None):
    rng = random.Random(seed)
    n = n_stars if n_stars is not None else int(w * h / 4200)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#070818"/>
      <stop offset="0.6" stop-color="#0d0b24"/>
      <stop offset="1" stop-color="#170d33"/>
    </linearGradient>
    <radialGradient id="g1" cx="0.9" cy="0.1" r="0.6">
      <stop offset="0" stop-color="{glow}" stop-opacity="0.22"/>
      <stop offset="1" stop-color="{glow}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="g2" cx="0.05" cy="1" r="0.6">
      <stop offset="0" stop-color="{glow2}" stop-opacity="0.12"/>
      <stop offset="1" stop-color="{glow2}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="clip"><rect width="{w}" height="{h}" rx="18"/></clipPath>
  </defs>
  <style>
    .tw {{ animation: twinkle 4s ease-in-out infinite; }}
    @keyframes twinkle {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.15; }} }}
    text {{ font-family: {FONT}; }}
  </style>
  <g clip-path="url(#clip)">
    <rect width="{w}" height="{h}" fill="url(#sky)"/>
    <rect width="{w}" height="{h}" fill="url(#g1)"/>
    <rect width="{w}" height="{h}" fill="url(#g2)"/>
    {stars(rng, n, w, h)}
    <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="18" fill="none" stroke="{LILAC}" stroke-opacity="0.16"/>
{body}
  </g>
</svg>
'''


def heading(x, y, label, color=CYAN):
    return (f'    <circle cx="{x+6}" cy="{y-8}" r="6" fill="{color}"><animate attributeName="opacity" '
            f'values="1;0.35;1" dur="3s" repeatCount="indefinite"/></circle>\n'
            f'    <text x="{x+22}" y="{y}" font-size="26" font-weight="700" fill="{TEXT}">{escape(label)}</text>\n')


def lines_svg(x, y, lines, size, fill, lh=1.45, weight=400):
    out = []
    for i, ln in enumerate(lines):
        out.append(f'    <text x="{x}" y="{y + i*size*lh:.0f}" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(ln)}</text>')
    return "\n".join(out) + "\n"


def pills(x, y, items, max_w, size=15, color=LILAC, gap=10, h=32):
    out, cx, cy = [], x, y
    for it in items:
        pw = text_w(it, size) + 28
        if cx + pw > x + max_w:
            cx = x
            cy += h + gap
        out.append(f'    <rect x="{cx:.0f}" y="{cy}" width="{pw:.0f}" height="{h}" rx="{h/2}" fill="#140f36" fill-opacity="0.8" stroke="{color}" stroke-opacity="0.35"/>')
        out.append(f'    <text x="{cx + pw/2:.0f}" y="{cy + h/2 + size*0.35:.0f}" font-size="{size}" fill="{TEXT}" text-anchor="middle">{escape(it)}</text>')
        cx += pw + gap
    return "\n".join(out) + "\n", cy + h


# ---------------------------------------------------------------- panels

def mission():
    W, H = 1200, 440
    body = heading(48, 64, "Mission log")
    body += lines_svg(70, 98, ["Evaluate. Build. Sell."], 19, MUTED)
    cards = [
        ("4 LLMs", "EVALUATE", "Benchmarked production LLMs on earnings calls at Microsoft for accuracy, bias, and failure modes. Informed the Azure AI roadmap and became an arXiv paper.", CYAN),
        ("300+", "BUILD", "Users on an LLM cover letter generator I built. Also a churn model at 95% accuracy on 20,000 users that took 1st place.", VIOLET),
        ("$500K+", "SELL", "In personal in-person sales at Live Nation, about $10K per show day. Founded Execute Coaching: 20+ clients, and I built its Django site.", "#ff5ca8"),
    ]
    cw, gap, x0, y0, ch = 352, 24, 48, 130, 272
    for i, (big, kick, desc, col) in enumerate(cards):
        x = x0 + i * (cw + gap)
        body += f'    <rect x="{x}" y="{y0}" width="{cw}" height="{ch}" rx="14" fill="#120d30" fill-opacity="0.72" stroke="{col}" stroke-opacity="0.35"/>\n'
        body += f'    <rect x="{x}" y="{y0}" width="4" height="{ch}" rx="2" fill="{col}"/>\n'
        body += f'    <text x="{x+28}" y="{y0+40}" font-size="13" font-weight="700" letter-spacing="3" fill="{col}">{kick}</text>\n'
        body += f'    <text x="{x+26}" y="{y0+90}" font-size="44" font-weight="700" fill="{TEXT}">{escape(big)}</text>\n'
        body += lines_svg(x + 28, y0 + 128, wrap(desc, cw - 50, 17.5), 17.5, MUTED, lh=1.4)
    return frame(W, H, 101, body)


PROJECTS = [
    ("options", "📈", "Options Scanner", "Ranks credit spreads, condors, and cash-secured puts, then checks its own scores against real outcomes. The backtester only surfaces strategies that hold up out of sample (p = 0.004 across 188 symbols).",
     ["Python", "DuckDB", "FastAPI", "React"], "#22d39b", "FLAGSHIP"),
    ("audit", "🔍", "Website Audit Tool", "Crawls a business's website and turns it into a prioritized PDF audit of speed, SEO, and conversion gaps. Ranks a whole prospect list by need. I use it to open sales calls.",
     ["Python", "PageSpeed API", "Places API"], "#ffb86b", "GTM"),
    ("cover", "✉️", "Cover Letter Generator", "Searches live job postings, embeds your resume, and writes a cover letter for the job you pick. 300+ users.",
     ["LangChain", "Pinecone", "OpenAI", "Streamlit"], "#ff5ca8", "GEN AI"),
    ("earnings", "🎙️", "Earnings Call Analyzer", "Sentiment by business line across Microsoft earnings calls, set against the stock's move, with a chatbot over the transcripts. Built alongside our arXiv paper.",
     ["OpenAI", "Plotly", "Streamlit"], "#50e6ff", "RESEARCH"),
    ("scholarship", "🎓", "Scholarship Finder", "Scrapes scholarships and uses an LLM to match them to a student's major, GPA, and financial need.",
     ["Web scraping", "OpenAI", "Streamlit"], "#ffd166", "NLP"),
    ("fitness", "🏋️", "AI Fitness Coach", "Builds a week of meals and training around your stats and goal, and projects your weight over time.",
     ["OpenAI", "Plotly", "Streamlit"], "#7c5cff", "GEN AI"),
]


def project_card(key, emoji, title, desc, tags, col, kicker, seed):
    W, H = 590, 330
    body = f'    <circle cx="60" cy="62" r="30" fill="{col}" fill-opacity="0.16" stroke="{col}" stroke-opacity="0.6"/>\n'
    body += f'    <text x="60" y="72" font-size="28" text-anchor="middle">{emoji}</text>\n'
    body += f'    <text x="106" y="52" font-size="12" font-weight="700" letter-spacing="3" fill="{col}">{kicker}</text>\n'
    body += f'    <text x="106" y="80" font-size="27" font-weight="700" fill="{TEXT}">{escape(title)}</text>\n'
    body += lines_svg(32, 128, wrap(desc, W - 60, 19), 19, MUTED, lh=1.38)
    p, _ = pills(32, 272, tags, W - 190, size=15, color=col, h=32)
    body += p
    body += f'    <text x="{W-32}" y="{294}" font-size="16" font-weight="600" fill="{col}" text-anchor="end">View repo →</text>\n'
    return frame(W, H, seed, body, glow=col, n_stars=34)


def launches_header():
    W, H = 1200, 110
    body = heading(48, 58, "Featured launches")
    body += lines_svg(70, 90, ["Things I've built and shipped. Click a card to open the repo."], 19, MUTED)
    return frame(W, H, 202, body, n_stars=40)


def toolkit():
    W = 1200
    items = ["Python", "SQL", "PyTorch", "TensorFlow", "scikit-learn", "Hugging Face", "LangChain", "OpenAI API",
             "Streamlit", "Django", "FastAPI", "Snowflake", "Airflow", "PySpark", "BigQuery", "Databricks",
             "Tableau", "AWS", "Git"]
    p, bottom = pills(48, 104, items, W - 96, size=19, h=44, gap=12)
    H = bottom + 40
    body = heading(48, 64, "Toolkit") + p
    return frame(W, H, 303, body)


def contact():
    W, H = 1200, 270
    body = heading(48, 64, "Open a channel", color="#ff5ca8")
    body += lines_svg(70, 104, wrap("Hiring for GTM engineering, forward-deployed engineering, or technical sales? Or want to talk LLM evals, options, or lifting? LinkedIn is the fastest way to reach me.", 800, 20), 20, MUTED)
    body += f'    <rect x="70" y="186" width="290" height="52" rx="26" fill="{VIOLET}"/>\n'
    body += f'    <text x="215" y="218" font-size="19" font-weight="600" fill="#fff" text-anchor="middle">Message me on LinkedIn ↗</text>\n'
    body += f'    <text x="384" y="218" font-size="19" fill="{LILAC}">or dominickkubica@gmail.com</text>\n'
    # small planet
    body += f'''    <g transform="translate(1040 140)">
      <ellipse rx="92" ry="18" fill="none" stroke="{CYAN}" stroke-opacity="0.3" stroke-width="2" transform="rotate(-16)"/>
      <circle r="48" fill="#ff5ca8" fill-opacity="0.85"/>
      <circle r="48" fill="url(#g1)"/>
      <path d="M -92 0 A 92 18 0 0 0 92 0" fill="none" stroke="{CYAN}" stroke-opacity="0.8" stroke-width="3" transform="rotate(-16)"/>
    </g>
'''
    return frame(W, H, 404, body, glow="#ff5ca8")


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    files = {"mission.svg": mission(), "launches.svg": launches_header(), "toolkit.svg": toolkit(), "contact.svg": contact()}
    for i, p in enumerate(PROJECTS):
        files[f"card-{p[0]}.svg"] = project_card(*p, seed=500 + i)
    for name, svg in files.items():
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(svg)
    print(" ".join(files))
