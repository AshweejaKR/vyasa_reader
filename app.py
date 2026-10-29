import json
from pathlib import Path

from flask import Flask, render_template

BASE_DIR = Path(__file__).resolve().parent
CATALOG_PATH = BASE_DIR / "data" / "catalog.json"
REQUIRED = ("id", "title", "collection", "sort_order", "source_url", "content_status")

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
            and str(entry["source_url"]).startswith("https://")
        ):
            items.append(entry)
    items.sort(key=lambda e: (str(e["collection"]), str(e["sort_order"]).zfill(6)))
    skipped = len(data) - len(items)
    return items, (f"{skipped} catalog entries were skipped as invalid." if skipped else None)


@app.route("/")
def home():
    items, error = load_catalog()
    stories = [i for i in items if i["collection"] == "stories"]
    parvas = [i for i in items if i["collection"] == "parvas"]
    return render_template("home.html", stories=stories, parvas=parvas, error=error)


@app.route("/health")
def health():
    return {"status": "ok"}


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
