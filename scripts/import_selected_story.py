"""Manual one-story import. Does not fetch pages or approve content."""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEM = "aruni-uddalaka"
SOURCE_URL = ("https://www.vyasaonline.com/2018/10/27/"
              "%E0%B2%86%E0%B2%B0%E0%B3%81%E0%B2%A3%E0%B2%BF-"
              "%E0%B2%89%E0%B2%A6%E0%B3%8D%E0%B2%A7%E0%B2%BE%E0%B2%B2%E0%B2%95/mahabharata/")
TARGET = ROOT / "data" / "content" / (ITEM + ".json")


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/import_selected_story.py PATH_TO_STORY.txt")
    source = Path(sys.argv[1]).expanduser()
    raw = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n").strip()
    if not raw or len(raw) > 100_000:
        raise SystemExit("Story text must contain 1–100,000 characters.")
    if re.search(r"<\s*/?\s*(?:html|body|p|div|script)\b", raw, re.I):
        raise SystemExit("Copy plain story text only, not website HTML.")
    parts = [p.strip() for p in re.split(r"\n\s*\n", raw) if p.strip()]
    if len(parts) < 2 or len(parts) > 100:
        raise SystemExit("Expected 2–100 story paragraphs separated by blank lines.")
    blocks = [{"id": f"p{i:04d}", "type": "paragraph", "text": p}
              for i, p in enumerate(parts, 1)]
    content = {
        "title": "ಆರುಣಿ ಉದ್ಧಾಲಕ",
        "author": "B.M. Ramesh",
        "source_name": "VyasaOnline",
        "source_url": SOURCE_URL,
        "permission_date": "2026-11-10",
        "source_revision": None,
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "source_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "review_status": "pending",
        "blocks": blocks,
    }
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    try:
        with TARGET.open("x", encoding="utf-8") as out:
            json.dump(content, out, ensure_ascii=False, indent=2)
            out.write("\n")
    except FileExistsError:
        raise SystemExit("Target exists. Refusing to overwrite; revisions need manual review.")
    print(f"Prepared {len(blocks)} blocks at {TARGET}. NOT approved/published.")


if __name__ == "__main__":
    main()
