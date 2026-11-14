"""Publish every tracked repository file as an inspectable, safely rendered page."""
from __future__ import annotations
import html
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
from urllib.parse import unquote, urlsplit, urlunsplit
import bleach
import markdown

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
EXTENSIONS = ["tables", "fenced_code", "toc", "sane_lists"]
TAGS = ["a","abbr","b","blockquote","br","code","dd","del","div","dl","dt","em",
        "h1","h2","h3","h4","h5","h6","hr","i","li","ol","p","pre","s","span",
        "strong","table","tbody","td","th","thead","tr","ul"]
STYLE = """
body{font:16px/1.55 system-ui,sans-serif;margin:0;background:#0b0f17;color:#e9eef7}
a{color:#9dd0ff} header{padding:1rem 2rem;background:#121a28}
main{max-width:1050px;margin:2rem auto;padding:0 1rem}
article{background:#151d2b;border-radius:10px;padding:1.5rem}
pre{background:#09111e;padding:1rem;overflow-x:auto;white-space:pre-wrap;overflow-wrap:anywhere}
table{display:block;overflow-x:auto;border-collapse:collapse}
td,th{border:1px solid #3c4a61;padding:.6rem} nav{margin:1rem 0;display:flex;gap:1rem;flex-wrap:wrap}
small{color:#aebdd4} blockquote{border-left:3px solid #9dd0ff;padding-left:1rem;margin-left:0}
"""

def sources():
    tracked = subprocess.run(["git","-C",str(ROOT),"ls-files","-z"],check=True,capture_output=True).stdout
    result = []
    for name in tracked.decode().split("\0"):
        if not name or name.startswith(("site/",".git/")):
            continue
        path = Path(name)
        full = ROOT / path
        if full.is_symlink() or not full.is_file() or not full.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError(f"Unsafe or missing tracked file: {name}")
        result.append(path)
    return sorted(result, key=lambda p: p.as_posix())

def page(path):
    return Path("pages") / (path.as_posix() + ".html")

def relative(from_page, target):
    return Path(os.path.relpath(target, start=from_page.parent)).as_posix()

def directories(names):
    return {str(parent) for name in names for parent in PurePosixPath(name).parents if str(parent)!="."}

def links(body, origin, current, names):
    def replace(m):
        url = html.unescape(m.group(1))
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc or url.startswith("//") or not parsed.path or parsed.path.startswith("/"):
            return m.group(0)
        candidate = os.path.normpath(os.path.join(origin.parent.as_posix(),unquote(parsed.path))).replace("\\","/")
        if candidate in names:
            target = page(Path(candidate))
        elif candidate.rstrip("/") in directories(names):
            target = Path("pages") / candidate.rstrip("/") / "index.html"
        else:
            return m.group(0)  # The link checker rejects unresolved local URLs.
        result = urlunsplit(("","",relative(current,target),parsed.query,parsed.fragment))
        return 'href="' + html.escape(result,quote=True) + '"'
    return re.sub(r'href="([^"]*)"',replace,body)

def shell(title, body, output, origin=None):
    home = html.escape(relative(output,Path("index.html")),quote=True)
    navigation = f'<a href="{home}">Repository catalogue</a>'
    if origin is not None:
        raw = html.escape(relative(output,Path("raw")/origin),quote=True)
        navigation += f' <a href="{raw}">Original source</a>'
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(title)} | ERC-8004 CSP</title><style>{STYLE}</style>'
            f'</head><body><header>ERC-8004 Consumer Security Profile</header><main>'
            f'<nav aria-label="Navigation">{navigation}</nav><article>{body}</article>'
            f'<p><small>Derived display. Repository files remain authoritative.</small></p>'
            f'</main></body></html>')

def main():
    tracked = sources()
    names = {p.as_posix() for p in tracked}
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)
    groups = {}
    for source in tracked:
        groups.setdefault(source.parent.as_posix(),[]).append(source)
        current = page(source)
        destination = SITE / current
        destination.parent.mkdir(parents=True,exist_ok=True)
        raw = SITE/"raw"/source
        raw.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/source,raw)
        if source.suffix.lower()==".md":
            marked = markdown.markdown((ROOT/source).read_text(encoding="utf-8"),extensions=EXTENSIONS)
            clean = bleach.clean(marked,tags=TAGS,
                     attributes={"a":["href","title"],"code":["class"],"td":["align"],"th":["align"]},
                     protocols=["http","https","mailto"],strip=True)
            body = links(clean,source,current,names)
        else:
            try:
                body = "<pre><code>"+html.escape((ROOT/source).read_text(encoding="utf-8"))+"</code></pre>"
            except UnicodeDecodeError:
                body = "<p>Binary file. Use the original source link.</p>"
        destination.write_text(shell(source.as_posix(),body,current,source),encoding="utf-8")
    dirs = directories(names)
    for directory in sorted(dirs):
        output = Path("pages")/directory/"index.html"
        output_full = SITE/output
        output_full.parent.mkdir(parents=True,exist_ok=True)
        child_dirs = sorted(d for d in dirs if str(PurePosixPath(d).parent)==directory)
        targets = [(d+"/",Path("pages")/d/"index.html") for d in child_dirs]
        targets += [(p.name,page(p)) for p in groups.get(directory,[])]
        body = "<h1>"+html.escape(directory)+"/</h1><ul>"+"".join(
            f'<li><a href="{html.escape(relative(output,target),quote=True)}">{html.escape(label)}</a></li>'
            for label,target in targets)+"</ul>"
        output_full.write_text(shell(directory,body,output),encoding="utf-8")
    sections = []
    for group,items in sorted(groups.items()):
        heading = "Top-level files" if group=="." else group+"/"
        section = "<h2>"+html.escape(heading)+"</h2><ul>"+"".join(
            f'<li><a href="{html.escape(page(p).as_posix(),quote=True)}">{html.escape(p.name)}</a></li>'
            for p in items)+"</ul>"
        sections.append(section)
    intro = ("<h1>Repository content catalogue</h1><p>All tracked specifications, "
             "documentation, governance records, Rego policies, schemas, tests, workflows "
             "and examples are available below. Each page links to its original source. "
             "The generated site/ directory is excluded.</p>")
    (SITE/"index.html").write_text(shell("Repository catalogue",intro+"".join(sections),Path("index.html")),encoding="utf-8")
    (SITE/".nojekyll").write_text("",encoding="utf-8")
    print(f"Published {len(tracked)} files and {len(dirs)} directory indexes.")

if __name__=="__main__":
    main()
