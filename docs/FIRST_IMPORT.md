# First selected content import — Aruni Uddalaka

Status: **import workflow prepared, not run; story text not yet imported or reviewed**.

## Source and permission

- Source: https://www.vyasaonline.com/2018/10/27/%E0%B2%86%E0%B2%B0%E0%B3%81%E0%B2%A3%E0%B2%BF-%E0%B2%89%E0%B2%A6%E0%B3%8D%E0%B2%A7%E0%B2%BE%E0%B2%B2%E0%B2%95/mahabharata/
- Credit: B.M. Ramesh / VyasaOnline. Personal, non-commercial permission recorded on 2026-11-10. Keep permission email private.
- No third-party illustrations, PDFs, or GitHub-repository text are included.

## Manual import

1. Open the original website source. Copy **only the Kannada story body** (not navigation, comments, images, or HTML) into a private UTF-8 `.txt` file. Separate source paragraphs with one blank line; keep original punctuation and Kannada.
2. From the project root, run `python scripts/import_selected_story.py /path/to/your/private-story.txt` yourself. This writes `data/content/aruni-uddalaka.json` **once**, without network calls or catalog approval.
3. Compare every resulting paragraph with the original website. Check spelling, order, source attribution, footnotes, and whether paragraphs or verses need to be split. Do not silently rewrite original wording.
4. When and only when review passes, change the generated JSON `review_status` to `approved`, and update the `aruni-uddalaka` record in `data/catalog.json` from `link_only` to `approved` with `content_path: "aruni-uddalaka.json"`.
5. Manually verify in-app rendering, bookmark, resume, source credit, and an explicit link to the original. Record this in `docs/PROGRESS.md` and `docs/DEVELOPMENT_LOG.md`. Runtime/Android verification is **not done**.

## Safety and revisions

- Do not commit website translation text to a public GitHub repository by default. Add `data/content/aruni-uddalaka.json` and private source `.txt` to `.gitignore`; deploy the approved JSON to private hosting separately if permitted. The necessary `.gitignore` entries are included in this branch.
- Generated block IDs are stable **only while paragraph order is unchanged** (`p0001`, `p0002`, ...). For later revisions, preserve IDs manually instead of regenerating this file; the importer refuses overwriting existing content. Record an actual source revision date only if independently verified.
- This importer processes one named, selected story. It never scrapes or fetches a website, and never changes `content_status` automatically.
