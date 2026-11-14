"""Pages coverage and link integrity checks for all tracked repository sources."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit
import unittest
from scripts.build_pages import ROOT,SITE,page,sources

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag=="a":
            self.links.extend(v for k,v in attrs if k=="href" and v)

class PagesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (SITE/"index.html").is_file():
            raise AssertionError("Run python scripts/build_pages.py first")

    def test_all_tracked_files_published(self):
        for path in sources():
            with self.subTest(path=str(path)):
                self.assertTrue((SITE/page(path)).is_file())
                self.assertEqual((SITE/"raw"/path).read_bytes(),(ROOT/path).read_bytes())

    def test_catalogue_lists_every_source(self):
        catalogue=(SITE/"index.html").read_text(encoding="utf-8")
        for path in sources():
            with self.subTest(path=str(path)):
                self.assertIn(page(path).as_posix(),catalogue)

    def test_all_local_page_links_resolve(self):
        for output in SITE.rglob("*.html"):
            parser=LinkParser()
            parser.feed(output.read_text(encoding="utf-8"))
            for link in parser.links:
                parsed=urlsplit(link)
                if not parsed.path or parsed.scheme or parsed.netloc or link.startswith("//"):
                    continue
                with self.subTest(page=str(output.relative_to(SITE)),link=link):
                    dest=(output.parent/unquote(parsed.path)).resolve()
                    self.assertTrue(dest.is_relative_to(SITE.resolve()),"Link outside site")
                    self.assertTrue(dest.is_file(),f"Broken local link: {link}")

    def test_source_visibility(self):
        home=(SITE/"index.html").read_text()
        for item in ("validation.rego","rego-conformance.yml","PROJECT-STATUS.yaml",
                     "input.schema.json","upstream-alignment-2026-11.md"):
            self.assertIn(item,home)
        self.assertNotIn("site/index.html",home)
        self.assertTrue((SITE/".nojekyll").is_file())

if __name__=="__main__":
    unittest.main()
