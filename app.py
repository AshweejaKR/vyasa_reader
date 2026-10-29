import json
from pathlib import Path

from flask import Flask, abort, render_template, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
CATALOG_PATH = BASE_DIR / "data" / "catalog.json"
CONTENT_DIR = (BASE_DIR / "data" / "content").resolve()
REQUIRED = ("id", "title", "collection", "sort_order", "source_url", "content_status")
BLOCK_TYPES = ("heading", "paragraph", "verse")

app = Flask(__name__)


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
            and (not entry["source_url"] or str(entry["source_url"]).startswith("https://"))
        ):
            items.append(entry)
    items.sort(key=lambda e: (str(e["collection"]), int(e["sort_order"]) if str(e["sort_order"]).isdigit() else 0))
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
        isinstance(b, dict) and b.get("type") in BLOCK_TYPES and b.get("id") and isinstance(b.get("text"), str)
        for b in blocks
    ):
        return None
    return content


def list_page(collection, heading):
    items, error = load_catalog()
    items = [i for i in items if i["collection"] == collection]
    return render_template("list.html", heading=heading, items=items, error=error)


@app.route("/")
def home():
    items, error = load_catalog()
    stories = [i for i in items if i["collection"] == "stories"]
    parvas = [i for i in items if i["collection"] == "parvas"]
    approved = {i["id"]: i["title"] for i in items if i["content_status"] == "approved"}
    return render_template("home.html", stories=stories, parvas=parvas, approved=approved, error=error)


@app.route("/stories")
def stories():
    return list_page("stories", "Stories")


@app.route("/parvas")
def parvas():
    return list_page("parvas", "Parvas")


@app.route("/read/<item_id>")
def read(item_id):
    items, _ = load_catalog()
    same = []
    for item in items:
        if item["id"] == item_id:
            current = item
            same = [i for i in items if i["collection"] == item["collection"]]
            break
    else:
        abort(404)
    pos = same.index(current)
    prev_item = same[pos - 1] if pos > 0 else None
    next_item = same[pos + 1] if pos + 1 < len(same) else None
    content = load_content(current)
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
