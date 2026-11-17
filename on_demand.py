"""Opt-in private, click-only source indexes and chapter cache (never public Git)."""
import hashlib
import json
import os
import threading
import time
from tempfile import NamedTemporaryFile
from datetime import datetime, timezone
from pathlib import Path

from source_html import SourceError, fetch_html, parse_page, source_url

ROOT = Path(__file__).resolve().parent / "data" / "runtime"
INDEX = {
    "stories": "https://www.vyasaonline.com/stories-in-mahabharata-kannada/",
    "parvas": "https://www.vyasaonline.com/translations10/",
}
LOCK = threading.Lock()


def enabled():
    return os.environ.get("VYASA_ON_DEMAND") == "1"


def _id(url):
    return "v-" + hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]


def _read(path, fallback):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return fallback


def _write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, suffix=".tmp",
                            delete=False) as output:
        json.dump(value, output, ensure_ascii=False, indent=2)
        output.write("\n")
        temp_name = output.name
    os.replace(temp_name, path)


def _page(url):
    """Cap all uncached outbound page requests to 20 per hour per app worker."""
    with LOCK:
        history = ROOT / "fetch_times.json"
        now = time.time()
        recent = [t for t in _read(history, []) if isinstance(t, (int, float)) and now - 3600 < t <= now]
        if len(recent) >= 20:
            raise SourceError("Hourly fetch limit reached; use cached pages or retry later.")
        _write(history, recent + [now])
    return parse_page(fetch_html(url))


def registry():
    entries = _read(ROOT / "registry.json", {})
    return entries if isinstance(entries, dict) else {}


def navigation(section, parent=None):
    if section not in INDEX:
        return None
    records = registry()
    if parent is not None:
        record = records.get(parent)
        if (section != "parvas" or not isinstance(record, dict)
                or record.get("kind") != "parva"):
            return None
        url = record["url"]
    else:
        url = INDEX[section]
    index_path = ROOT / ("index-" + _id(url) + ".json")
    cached = _read(index_path, None)
    if isinstance(cached, list):
        return cached
    page = _page(url)
    found = []
    seen = set()
    kind = "parva" if section == "parvas" and parent is None else "chapter"
    parva_path = ROOT / ("index-" + _id(INDEX["parvas"]) + ".json")
    other_parvas = {entry["url"] for entry in _read(parva_path, [])
                    if isinstance(entry, dict) and isinstance(entry.get("url"), str)}
    for href, title in page.links:
        address = source_url(href, url)
        if not address or address == url or address in seen:
            continue
        if kind == "parva" and not (
                "parva" in title.casefold() or "harivamsha" in title.casefold()):
            continue
        if parent is not None and address in other_parvas:
            continue
        seen.add(address)
        item_id = _id(address)
        found.append({"id": item_id, "title": title, "url": address, "kind": kind})
        records[item_id] = {
            "id": item_id, "title": title, "url": address,
            "kind": kind, "collection": section, "parent": parent or section,
        }
    if not 1 <= len(found) <= 500:
        raise SourceError("No supported chapter links found on this page. "
                          "Use Open original index for PDF-only or unsupported pages.")
    _write(ROOT / "registry.json", records)
    _write(index_path, found)
    return found


def item(item_id):
    if not isinstance(item_id, str) or not item_id.startswith("v-") or len(item_id) != 22:
        return None
    record = registry().get(item_id)
    return record if isinstance(record, dict) and record.get("kind") == "chapter" else None


def register_direct(entry):
    """Allow an already-curated website story without changing public catalog."""
    address = source_url(entry["source_url"])
    if not address:
        return None
    item_id = _id(address)
    records = registry()
    if item_id not in records:
        records[item_id] = {
            "id": item_id, "title": entry["title"], "url": address,
            "kind": "chapter", "collection": entry["collection"],
            "parent": entry["collection"],
        }
        _write(ROOT / "registry.json", records)
    return item_id


def reader_item(record):
    return {
        "id": record["id"], "title": record["title"],
        "collection": record["collection"], "source_url": record["url"],
        "source_name": "VyasaOnline", "author": "B.M. Ramesh",
        "content_status": "preview",
    }


def load_chapter(record):
    path = ROOT / "chapters" / (record["id"] + ".json")
    existing = _read(path, None)
    if existing is not None:
        return existing if isinstance(existing, dict) and existing.get("auto_preview") is True else None
    page = _page(record["url"])
    parts = page.paragraphs
    plain = "\n\n".join(parts)
    if (not 1 <= len(parts) <= 1200 or not 150 <= len(plain) <= 450_000
            or sum("\u0c80" <= ch <= "\u0cff" for ch in plain) < 10):
        raise SourceError("Source body could not be safely identified.")
    content = {
        "title": record["title"], "author": "B.M. Ramesh",
        "source_name": "VyasaOnline", "source_url": record["url"],
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "source_sha256": hashlib.sha256(plain.encode("utf-8")).hexdigest(),
        "review_status": "auto_unreviewed", "auto_preview": True,
        "blocks": [{"id": f"p{i:04d}", "type": "paragraph", "text": paragraph}
                   for i, paragraph in enumerate(parts, 1)],
    }
    _write(path, content)
    return content


def cached_titles():
    titles = {}
    for record in registry().values():
        if (isinstance(record, dict) and record.get("kind") == "chapter"
                and (ROOT / "chapters" / (record["id"] + ".json")).is_file()):
            titles[record["id"]] = record["title"]
    return titles


def neighbors(record):
    siblings = [x for x in registry().values()
                if isinstance(x, dict) and x.get("kind") == "chapter"
                and x.get("parent") == record["parent"]]
    ids = [x["id"] for x in siblings]
    if record["id"] not in ids:
        return None, None
    position = ids.index(record["id"])
    return (reader_item(siblings[position - 1]) if position else None,
            reader_item(siblings[position + 1]) if position + 1 < len(siblings) else None)
