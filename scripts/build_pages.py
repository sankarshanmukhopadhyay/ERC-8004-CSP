from __future__ import annotations

import html
from pathlib import Path
import shutil
import markdown

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

DOCS = [
    ("README.md", "Home"),
    ("spec/erc-8004-csp.md", "Specification"),
    ("conformance/checklist.md", "Conformance Checklist"),
    ("conformance/test-cases.md", "Conformance Test Cases"),
    ("docs/architecture.md", "Architecture"),
    ("docs/threat-model.md", "Threat Model"),
]

STYLE = """
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; background: #0b0f17; color: #e9eef7; }
a { color: #8cc7ff; }
.container { max-width: 1000px; margin: 0 auto; padding: 2rem; }
nav { display: flex; flex-wrap: wrap; gap: 1rem; margin-bottom: 2rem; }
nav a { text-decoration: none; padding: 0.55rem 0.8rem; border-radius: 999px; background: #121a28; }
article { background: #121826; border-radius: 16px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.25); }
code, pre { background: #0d1320; border-radius: 8px; }
pre { padding: 1rem; overflow-x: auto; }
table { border-collapse: collapse; width: 100%; display: block; overflow-x: auto; }
th, td { border: 1px solid #2a3346; padding: 0.6rem; text-align: left; }
blockquote { border-left: 4px solid #8cc7ff; margin-left: 0; padding-left: 1rem; color: #c8d5ea; }
.footer { margin-top: 1.5rem; color: #b7c5db; font-size: 0.95rem; }
"""

MD_EXTENSIONS = ["tables", "fenced_code", "toc", "sane_lists"]


def render_page(title: str, body_html: str) -> str:
    nav_links = " ".join(
        f'<a href="{Path(path).with_suffix(".html").name}">{html.escape(label)}</a>' for path, label in DOCS
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>{STYLE}</style>
</head>
<body>
  <div class="container">
    <nav>{nav_links}</nav>
    <article>{body_html}</article>
    <div class="footer">Built from repository Markdown by <code>scripts/build_pages.py</code>.</div>
  </div>
</body>
</html>"""


def main() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True, exist_ok=True)

    for rel_path, title in DOCS:
        src = ROOT / rel_path
        text = src.read_text(encoding="utf-8")
        body_html = markdown.markdown(text, extensions=MD_EXTENSIONS)
        out_name = Path(rel_path).with_suffix(".html").name
        (SITE / out_name).write_text(render_page(title, body_html), encoding="utf-8")

    # Convenience landing file for static hosting.
    home = SITE / "README.html"
    shutil.copyfile(home, SITE / "index.html")


if __name__ == "__main__":
    main()
