"""Single-page VyasaOnline HTML parsing; no generic crawling or remote HTML rendering."""
import re
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

HOSTS = {"vyasaonline.com", "www.vyasaonline.com"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}


class SourceError(Exception):
    """The requested page cannot safely be used as a Kannada HTML source."""


def source_url(url, base="https://www.vyasaonline.com/"):
    """Allow only HTTPS website pages, never file/download/API URLs."""
    try:
        parts = urlsplit(urljoin(base, url))
        if (parts.scheme != "https" or parts.hostname not in HOSTS
                or parts.username or parts.password or parts.port not in (None, 443)
                or any(parts.path.lower().endswith(s) for s in
                       (".pdf", ".zip", ".jpg", ".png", ".doc", ".docx")) 
                or parts.path.startswith(("/wp-content/", "/wp-json/", "/feed"))):
            return None
    except ValueError:
        return None
    return urlunsplit(("https", parts.netloc.lower(), parts.path or "/", "", ""))


class OnlySourceRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if source_url(newurl) is None:
            raise SourceError("Redirected outside the allowed website.")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_html(url):
    if source_url(url) != url:
        raise SourceError("Invalid source address.")
    request = Request(url, headers={"User-Agent": "VyasaReader/1.0 (personal on-demand reading)"})
    try:
        with build_opener(OnlySourceRedirects()).open(request, timeout=15) as response:
            if (source_url(response.geturl()) is None
                    or response.headers.get_content_type() != "text/html"):
                raise SourceError("Not a supported HTML page.")
            raw = response.read(2_500_001)
        if len(raw) > 2_500_000:
            raise SourceError("Page larger than permitted import size.")
        return raw.decode("utf-8-sig")
    except (HTTPError, URLError, OSError, TimeoutError, UnicodeError) as exc:
        raise SourceError("Website unavailable or response invalid.") from exc


class SourcePage(HTMLParser):
    """Capture post text and index links while excluding site navigation."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.body_depth = None
        self.paragraph = None
        self.anchor = None
        self.paragraphs = []
        self.links = []
        self.stopped = False

    def handle_starttag(self, tag, attrs):
        if tag == "br" and self.paragraph is not None:
            self.paragraph.append("\n")
        if tag in VOID:
            return
        self.tags.append(tag)
        classes = (dict(attrs).get("class") or "").split()
        if (self.body_depth is None and tag in ("div", "section", "article")
                and ("entry-content" in classes or "post-content" in classes)):
            self.body_depth = len(self.tags)
        outside_nav = not any(t in self.tags for t in ("nav", "header", "footer", "aside"))
        in_list = "li" in self.tags and ("ol" in self.tags or "ul" in self.tags)
        in_article = "main" in self.tags or "article" in self.tags or self.body_depth is not None
        if tag == "a" and outside_nav and (("ol" in self.tags and "li" in self.tags)
                                            or (in_article and in_list)):
            self.anchor = ((dict(attrs).get("href") or ""), [])
        if self.body_depth is None or self.stopped:
            return
        if tag == "p" and self.paragraph is None:
            self.paragraph = []

    def handle_data(self, data):
        if any(t in self.tags for t in ("script", "style", "noscript")):
            return
        if self.anchor is not None:
            self.anchor[1].append(data)
        if self.body_depth is None or self.stopped:
            return
        if data.strip().casefold().startswith("the other stories"):
            self.stopped = True
            self.paragraph = None
            return
        if self.paragraph is not None:
            self.paragraph.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.anchor is not None:
            href, words = self.anchor
            label = re.sub(r"\s+", " ", "".join(words)).strip()
            if href and 1 <= len(label) <= 120:
                self.links.append((href, label))
            self.anchor = None
        if tag == "p" and self.paragraph is not None:
            value = "".join(self.paragraph)
            value = re.sub(r"[ \t\r\f\v]+", " ", value)
            value = re.sub(r" *\n *", "\n", value).strip()
            if value:
                self.paragraphs.append(value)
            self.paragraph = None
        if tag in self.tags:
            index = len(self.tags) - 1 - self.tags[::-1].index(tag)
            del self.tags[index:]
        if self.body_depth is not None and len(self.tags) < self.body_depth:
            self.body_depth = None


def parse_page(html):
    parser = SourcePage()
    parser.feed(html)
    if parser.body_depth is None and not parser.paragraphs and not parser.links:
        raise SourceError("Expected WordPress content was not found.")
    return parser
