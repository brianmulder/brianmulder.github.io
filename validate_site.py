"""Offline checks for the committed static site; no generator execution."""

import ast
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
DOMAIN = "www.brianmulder.com"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.urls = []
        self.json_chunks = []
        self.in_json = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                raise ValueError(f"Duplicate HTML id: {attrs['id']}")
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.urls.append(attrs[key])
        if tag == "meta" and attrs.get("property") == "og:image":
            self.urls.append(attrs.get("content", ""))
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_json = True

    def handle_data(self, data):
        if self.in_json:
            self.json_chunks.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.in_json:
            json.loads("".join(self.json_chunks))
            self.json_chunks.clear()
            self.in_json = False


def validate():
    page = Page()
    page.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    page.close()
    if page.in_json:
        raise ValueError("Unclosed JSON-LD script")
    for url in page.urls:
        parsed = urlsplit(url)
        if parsed.netloc and parsed.netloc != DOMAIN:
            continue
        if parsed.scheme and parsed.scheme not in ("http", "https"):
            continue
        path = (ROOT / unquote(parsed.path).lstrip("/")).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError(f"Link escapes repository: {url}")
        if path.is_dir():
            path /= "index.html"
        if not path.is_file():
            raise ValueError(f"Missing local link target: {url}")
        if path == ROOT / "index.html" and parsed.fragment:
            if unquote(parsed.fragment) not in page.ids:
                raise ValueError(f"Missing HTML anchor: {url}")
    if (ROOT / "CNAME").read_text().strip() != DOMAIN:
        raise ValueError("Unexpected Pages domain")
    if (ROOT / "llm.txt").read_bytes() != (ROOT / "llms.txt").read_bytes():
        raise ValueError("llm.txt and llms.txt differ")
    for name in ("cv.txt", "llms.txt", "llm.txt"):
        text = (ROOT / name).read_text(encoding="ascii")
        if not text.strip():
            raise ValueError(f"Empty public text: {name}")
        if name == "cv.txt" and max(map(len, text.splitlines())) > 72:
            raise ValueError("CV exceeds 72 columns")
    for name in ("Brian-Mulder-CV.pdf", "Brian-Mulder-CV-Detailed.pdf"):
        if not (ROOT / name).read_bytes().startswith(b"%PDF-"):
            raise ValueError(f"Invalid PDF signature: {name}")
    if not (ROOT / "social-card.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Invalid social-card PNG signature")
    if not (ROOT / "portrait.jpg").read_bytes().startswith(b"\xff\xd8\xff"):
        raise ValueError("Invalid portrait JPEG signature")
    for name in ("build_text.py", "build_social_card.py", "validate_site.py"):
        ast.parse((ROOT / name).read_text(), filename=name)
    print("PASS: local links/anchors, JSON-LD, domain, public text, asset signatures, Python syntax")


if __name__ == "__main__":
    validate()
