"""Prepare one permitted Kannada story; never publish or approve automatically."""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = (
    "https://www.vyasaonline.com/2018/10/27/"
    "%E0%B2%86%E0%B2%B0%E0%B3%81%E0%B2%A3%E0%B2%BF-"
    "%E0%B2%89%E0%B2%A6%E0%B3%8D%E0%B2%A7%E0%B2%BE%E0%B2%B2%E0%B2%95/mahabharata/"
)
CHAPTER_URL = (
    "https://github.com/vyasaonline/mahAbhArata/blob/content/"
    "01_Adiparva/003_paushya-parva.md"
)
TARGET = ROOT / "data" / "content" / "aruni-uddalaka.json"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}


class StoryBody(HTMLParser):
    """Extract paragraphs only from a WordPress post's content element."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.content_depth = None
        self.paragraph = None
        self.paragraphs = []
        self.stopped = False

    def handle_starttag(self, tag, attrs):
        if tag == "br" and self.paragraph is not None:
            self.paragraph.append("\n")
        if tag in VOID:
            return
        self.tags.append(tag)
        classes = (dict(attrs).get("class") or "").split()
        if (self.content_depth is None and tag in ("div", "section", "article")
                and ("entry-content" in classes or "post-content" in classes)):
            self.content_depth = len(self.tags)
        if (self.content_depth is not None and tag == "p"
                and self.paragraph is None and not self.stopped):
            self.paragraph = []

    def handle_data(self, data):
        if (self.paragraph is not None and not self.stopped
                and not any(t in self.tags for t in ("script", "style", "noscript"))):
            self.paragraph.append(data)

    def handle_endtag(self, tag):
        if tag == "p" and self.paragraph is not None:
            value = "".join(self.paragraph)
            value = re.sub(r"[ \t\r\f\v]+", " ", value)
            value = re.sub(r" *\n *", "\n", value).strip()
            if value.casefold().startswith("the other stories"):
                self.stopped = True
            elif value:
                self.paragraphs.append(value)
            self.paragraph = None
        if tag in self.tags:
            index = len(self.tags) - 1 - self.tags[::-1].index(tag)
            del self.tags[index:]
        if self.content_depth is not None and len(self.tags) < self.content_depth:
            self.content_depth = None


def fetch_paragraphs():
    request = Request(SOURCE_URL, headers={"User-Agent": "VyasaReader/1.0 (personal one-time import)"})
    with urlopen(request, timeout=20) as response:
        if urlsplit(response.geturl()).hostname not in ("www.vyasaonline.com", "vyasaonline.com"):
            raise SystemExit("Source redirected away from VyasaOnline; import stopped.")
        if response.headers.get_content_type() != "text/html":
            raise SystemExit("Expected a VyasaOnline HTML story page.")
        page = response.read(1_500_001)
    if len(page) > 1_500_000:
        raise SystemExit("Source page is too large; import stopped.")
    parser = StoryBody()
    parser.feed(page.decode("utf-8-sig"))
    parts = parser.paragraphs
    if not 4 <= len(parts) <= 12 or not any("ಆರುಣಿ" in p for p in parts):
        raise SystemExit("Story structure unexpected; use a reviewed private UTF-8 text file.")
    return parts


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/import_selected_story.py --fetch | private-story.txt")
    if TARGET.exists():
        raise SystemExit("Content file exists; refusing to overwrite a possible reviewed revision.")
    if sys.argv[1] == "--fetch":
        parts = fetch_paragraphs()
        method = "single_website_fetch"
    else:
        if sys.argv[1].startswith("-"):
            raise SystemExit("Unknown option. Use --fetch or a private UTF-8 .txt file.")
        raw = Path(sys.argv[1]).expanduser().read_text(encoding="utf-8-sig")
        if re.search(r"<\s*/?\s*(?:html|body|p|div|script)\b", raw, re.I):
            raise SystemExit("Text file contains HTML; use plain story text.")
        parts = [p.strip() for p in re.split(r"\n\s*\n", raw.replace("\r\n", "\n")) if p.strip()]
        method = "manual_text"
    text = "\n\n".join(parts)
    if not 2 <= len(parts) <= 100 or not 1 <= len(text) <= 100_000:
        raise SystemExit("Story text/paragraph count is outside the allowed range.")
    content = {
        "title": "ಆರುಣಿ ಉದ್ಧಾಲಕ", "author": "B.M. Ramesh",
        "source_name": "VyasaOnline", "source_url": SOURCE_URL,
        "chapter_reference_url": CHAPTER_URL,
        "permission_date": "2026-11-10", "source_revision": None,
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "source_method": method, "source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "review_status": "pending",
        "blocks": [{"id": f"p{i:04d}", "type": "paragraph", "text": p}
                   for i, p in enumerate(parts, 1)],
    }
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    with TARGET.open("x", encoding="utf-8") as output:
        json.dump(content, output, ensure_ascii=False, indent=2)
        output.write("\n")
    print(f"Prepared {len(parts)} blocks at {TARGET}; review_status=pending. Not published.")


if __name__ == "__main__":
    main()
