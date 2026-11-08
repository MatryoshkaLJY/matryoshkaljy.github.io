"""Check the static site's local links, anchors, files, and inline JavaScript."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = ["index.html", "404.html", ".nojekyll", "robots.txt", "sitemap.xml"]
errors = []


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.links = []
        self.scripts = []
        self.current_script = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                errors.append(f"{self.path}: duplicate id {attrs['id']}")
            self.ids.add(attrs["id"])
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.links.append(attrs[attr])
        if tag == "img" and "alt" not in attrs:
            errors.append(f"{self.path}: image missing alt text")
        if tag == "script" and "src" not in attrs:
            self.current_script = []

    def handle_data(self, text):
        if self.current_script is not None:
            self.current_script.append(text)

    def handle_endtag(self, tag):
        if tag == "script" and self.current_script is not None:
            self.scripts.append("".join(self.current_script))
            self.current_script = None


pages = {}
for path in [ROOT / "index.html", ROOT / "404.html", *sorted((ROOT / "notes").glob("*.html"))]:
    page = Page(path.relative_to(ROOT))
    if not path.is_file():
        errors.append(f"Missing page: {path}")
        continue
    source = path.read_text(encoding="utf-8")
    for private_ref in ("file://", "/home/matryoshka/", "http://localhost", "http://127.0.0.1"):
        if private_ref in source:
            errors.append(f"{page.path}: local-only reference {private_ref}")
    page.feed(source)
    pages[path.resolve()] = page
    for index, script in enumerate(page.scripts, 1):
        result = subprocess.run(["node", "--check"], input=script, text=True, capture_output=True)
        if result.returncode:
            errors.append(f"{page.path}: inline script {index}: {result.stderr}")

for path, page in pages.items():
    for link in page.links:
        parts = urlsplit(link)
        if parts.scheme or parts.netloc:
            if parts.scheme not in ("https", "mailto", "data"):
                errors.append(f"{page.path}: unexpected URL scheme {link}")
            continue
        target = ((ROOT / unquote(parts.path).lstrip("/")) if parts.path.startswith("/")
                  else path.parent / unquote(parts.path)).resolve() if parts.path else path
        if target.is_dir():
            target = target / "index.html"
        if not target.is_relative_to(ROOT):
            errors.append(f"{page.path}: link escapes site root: {link}")
        elif not target.is_file():
            errors.append(f"{page.path}: missing local target: {link}")
        elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
            errors.append(f"{page.path}: missing anchor: {link}")

for filename in PUBLIC_FILES:
    if not (ROOT / filename).is_file():
        errors.append(f"Missing public file: {filename}")
if not (ROOT / "notes/say-halo-training-guide.html").is_file():
    errors.append("Missing training guide")
try:
    ET.parse(ROOT / "sitemap.xml")
    ET.parse(ROOT / "assets/favicon.svg")
except (ET.ParseError, FileNotFoundError) as error:
    errors.append(str(error))

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print(f"OK: {len(pages)} HTML pages, {sum(len(p.links) for p in pages.values())} links/resources, inline JavaScript, sitemap and favicon.")
