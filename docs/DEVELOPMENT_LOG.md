# Development Log

## 2026-10-29 — Phase 04: Resume and bookmarks
- Summary: Versioned `vyasa.v1.state` localStorage schema keyed by catalog id and block id (offset ratio, timestamp, per-item positions, bookmarks, auto-resume flag); malformed or old values are discarded or clamped. Debounced scroll save plus flush on visibilitychange, pagehide and link clicks. Restore after `document.fonts.ready`; font changes keep the nearest paragraph. Home auto-redirects only on a fresh session with no same-origin referrer, and only to an item still in the approved catalog; an Auto-resume toggle, Continue Reading button, bookmark list and storage-limits note were added. Link-only items show a no-tracking notice. Demo story extended with more self-written fictional text for testing.
- Added: `static/resume.js`
- Modified: `app.py`, `static/reader.js`, `static/style.css`, `templates/base.html`, `templates/home.html`, `templates/read.html`, `data/content/demo-story.json`, `README.md`, `PLAN.md`, `docs/PROGRESS.md`, `docs/DEVELOPMENT_LOG.md`
- Verification: not run

## 2026-10-29 — Phase 03: Reader UI
- Summary: Reader column (68ch, rem-based size, generous spacing), Kannada font stack with system fallbacks (no bundled fonts), A-/A+ and light/dark controls saved in versioned localStorage keys, Back to library link. Controls appear only for in-app (approved) content; link-only items show no text. Theme script loads in the head to avoid a flash.
- Added: `static/reader.js`
- Modified: `static/style.css`, `templates/read.html`, `templates/base.html`, `README.md`, `PLAN.md`, `docs/PROGRESS.md`, `docs/DEVELOPMENT_LOG.md`
- Verification: not run

## 2026-10-29 — Phase 02: Catalog and allowed content
- Summary: Added `/stories`, `/parvas`, and `/read/<item_id>`. `link_only` items show credit and an Open Original button (no auto-redirect); `approved` items load a JSON block file confined to `data/content/`, rendered escaped. Previous/Next within a collection. One fictional, self-written demo story added. No importer or fetcher, since no permission is recorded.
- Added: `data/content/demo-story.json`, `templates/list.html`, `templates/read.html`, `templates/_items.html`
- Modified: `app.py`, `data/catalog.json`, `templates/base.html`, `templates/home.html`, `static/style.css`, `README.md`, `PLAN.md`, `docs/PROGRESS.md`, `docs/DEVELOPMENT_LOG.md`
- Verification: not run

## 2026-10-29 — Phase 00: Source and rights (reconciliation)
- Summary: Added content decision (`link_only`; rights not verified) from summarized fetches of the stories index, Parvas index, one story page, contact page, and GitHub repo. No Parva/chapter page inspected. No text copied. Corrected PLAN status and PROGRESS order; Phase 01 was implemented before Phase 00, now reconciled; next is Phase 02.
- Added: `docs/CONTENT_ACCESS_DECISION.md`
- Modified: `PLAN.md`, `docs/PROGRESS.md`, `docs/DEVELOPMENT_LOG.md`
- Verification: not run

## 2026-10-29 — Phase 01: Flask foundation
- Summary: Minimal Flask app with `/`, `/health`, 404 page, and a tolerant JSON catalog loader. Link-only fixture with 3 metadata entries (VyasaOnline URLs); no story text copied. Mobile-first, accessible styling with Kannada font stack.
- Added: `app.py`, `requirements.txt`, `data/catalog.json`, `templates/base.html`, `templates/home.html`, `templates/404.html`, `static/style.css`, `docs/DEVELOPMENT_LOG.md`
- Modified: `README.md`, `docs/PROGRESS.md`
- Note: Phase 00 (rights) not yet done; all entries are `link_only`.
- Verification: not run
