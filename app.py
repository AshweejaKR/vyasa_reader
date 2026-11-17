import json
import os
import re
import secrets
from pathlib import Path

from flask import Flask, Response, abort, redirect, render_template, request, send_from_directory, url_for

from on_demand import (INDEX, cached_titles, item as source_item, load_chapter,
                       navigation, neighbors, reader_item, register_direct, registry)
from source_html import SourceError

BASE_DIR = Path(__file__).resolve().parent
CATALOG_PATH = BASE_DIR / "data" / "catalog.json"
CONTENT_DIR = (BASE_DIR / "data" / "content").resolve()
REQUIRED = ("id", "title", "collection", "sort_order", "source_url", "content_status")
BLOCK_TYPES = ("heading", "paragraph", "verse")

SAFE_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")

app = Flask(__name__)


@app.before_request
def private_source_access():
    if request.path == "/health":
        return None
    username = os.environ.get("VYASA_PRIVATE_USER", "")
    password = os.environ.get("VYASA_PRIVATE_PASSWORD", "")
    if not username and not password:
        return None
    if not username or not password:
        return Response("Set both reader credentials or neither.", status=503)
    auth = request.authorization
    if not auth or not (secrets.compare_digest(auth.username or "", username)
                        and secrets.compare_digest(auth.password or "", password)):
        return Response("Authentication required.", status=401, headers={
            "WWW-Authenticate": 'Basic realm="Vyasa Reader"'})
    return None


@app.after_request
def prevent_private_html_caching(response):
    if response.mimetype == "text/html":
        response.headers["Cache-Control"] = "private, no-store"
        response.headers["Vary"] = "Authorization"
    return response


def load_catalog():
    """Return (items, error). Never raises; error is a short user-facing message."""
    try:
        data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [], "The catalog file is missing."
    except (OSError, ValueError):
        return [], "The catalog file could not be read."
    if not isinstance(data, list):
        return [], "The catalog format is invalid."
    items = []
    for entry in data:
        if (
            isinstance(entry, dict)
            and all(key in entry for key in REQUIRED)
            and isinstance(entry["id"], str) and SAFE_ID.fullmatch(entry["id"])
            and isinstance(entry["title"], str) and bool(entry["title"].strip())
            and entry["collection"] in ("stories", "parvas")
            and entry["content_status"] in ("link_only", "approved")
            and isinstance(entry["sort_order"], int) and not isinstance(entry["sort_order"], bool)
            and isinstance(entry["source_url"], str)
            and (not entry["source_url"] or entry["source_url"].startswith("https://"))
            and (entry["content_status"] != "link_only" or bool(entry["source_url"]))
        ):
            items.append(entry)
    seen = set()
    unique = []
    for entry in items:
        if entry["id"] not in seen:
            seen.add(entry["id"])
            unique.append(entry)
    items = unique
    items.sort(key=lambda e: (e["collection"], e["sort_order"]))
    skipped = len(data) - len(items)
    return items, (f"{skipped} catalog entries were skipped as invalid." if skipped else None)


def load_content(item):
    """Return the content dict for an approved item, or None if unavailable or invalid."""
    if item["content_status"] != "approved" or not item.get("content_path"):
        return None
    path = (CONTENT_DIR / str(item["content_path"])).resolve()
    if path.suffix != ".json" or not path.is_relative_to(CONTENT_DIR):
        return None
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    blocks = content.get("blocks") if isinstance(content, dict) else None
    if not isinstance(blocks, list) or not all(
        isinstance(b, dict) and b.get("type") in BLOCK_TYPES and isinstance(b.get("id"), str) and SAFE_ID.fullmatch(b["id"])
        and isinstance(b.get("text"), str)
        for b in blocks
    ):
        return None
    ids = [b["id"] for b in blocks]
    if len(ids) != len(set(ids)):
        return None
    # All imported website text requires explicit editorial approval.
    if item["source_url"] and content.get("review_status") != "approved":
        return None
    return content


@app.route("/")
def home():
    items, error = load_catalog()
    stories = [i for i in items if i["collection"] == "stories"]
    parvas = [i for i in items if i["collection"] == "parvas"]
    approved = {i["id"]: i["title"] for i in items if i["content_status"] == "approved"}
    approved.update(cached_titles())
    return render_template("home.html", stories=stories, parvas=parvas,
                           approved=approved, error=error)


@app.route("/stories")
def stories():
    return redirect(url_for("source_browse", section="stories"))


@app.route("/parvas")
def parvas():
    return redirect(url_for("source_browse", section="parvas"))


@app.route("/source/<section>")
@app.route("/source/<section>/<parent>")
def source_browse(section, parent=None):
    if section not in INDEX:
        abort(404)
    if parent is not None and parent not in registry():
        abort(404)
    error = None
    try:
        entries = navigation(section, parent)
    except SourceError as exc:
        entries, error = [], str(exc)
    if entries is None:
        abort(404)
    origin = registry()[parent]["url"] if parent else INDEX[section]
    return render_template("source_list.html", section=section, parent=parent,
                           entries=entries, origin=origin, error=error)


@app.route("/read/<item_id>")
def read(item_id):
    record = source_item(item_id)
    if record:
        try:
            content = load_chapter(record)
        except SourceError:
            content = None
        prev_item, next_item = neighbors(record)
        return render_template("read.html", item=reader_item(record),
                               content=content, prev_item=prev_item, next_item=next_item)
    items, _ = load_catalog()
    same = []
    for item in items:
        if item["id"] == item_id:
            current = item
            same = [i for i in items if i["collection"] == item["collection"]]
            break
    else:
        abort(404)
    if current["id"] in ("stories-index", "parvas-index"):
        return redirect(url_for("source_browse",
                                section="stories" if current["id"] == "stories-index"
                                else "parvas"))
    content = load_content(current)
    if not content and current.get("source_url"):
        dynamic_id = register_direct(current)
        if dynamic_id:
            return redirect(url_for("read", item_id=dynamic_id))
    pos = same.index(current)
    prev_item = same[pos - 1] if pos > 0 else None
    next_item = same[pos + 1] if pos + 1 < len(same) else None
    return render_template(
        "read.html", item=current, content=content, prev_item=prev_item, next_item=next_item
    )


@app.route("/sw.js")
def service_worker():
    response = send_from_directory(app.static_folder, "sw.js", mimetype="text/javascript")
    response.headers["Cache-Control"] = "no-cache"
    return response


@app.route("/offline")
def offline():
    return render_template("offline.html")


@app.route("/health")
def health():
    return {"status": "ok"}


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
