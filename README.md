# Vyasa Reader

**Status:** Phases 00-03 written (link-only catalog plus a fictional in-app demo story); not yet run.

Small, independent Kannada Mahabharata reader for **Android and PC**, intended to run on an AWS EC2 instance. Goal: comfortable reading and resume from where you stopped.

## Experience

- Open the installed app icon; resume the last permitted **in-app** story near its saved paragraph.
- Browse Stories or Parvas/Chapters. Use Previous/Next, bookmarks, larger text, and dark/light mode.
- Open source-only entries on [VyasaOnline](https://www.vyasaonline.com/) when translation hosting permission is not established.
- Same-browser/device progress only; clearing site data or using private browsing can remove it. **Exact resume does not work reliably inside external VyasaOnline pages.**

## Design choices

- **Python Flask + HTML/CSS/JavaScript**; no React, database, accounts, or complex architecture.
- JSON catalog; permitted content stored locally only when its reuse rights are documented.
- Browser `localStorage` for saved position, bookmarks, and display settings.
- HTTPS Progressive Web App (PWA); Nginx + Gunicorn + systemd on Amazon Linux EC2.
- No automated bulk scraping or unauthorized copying of translations.

## Run locally (not run / not verified)

```
python -m venv .venv
.venv\Scripts\activate          # Windows; on Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Smoke check, with the app running on http://127.0.0.1:5000:

1. `/` shows "Vyasa Reader", Stories and Parvas navigation, an empty Continue Reading state, and Kannada titles.
2. `/stories` and `/parvas` list their entries in order.
3. The demo story opens at `/read/demo-story` with its demo notice, credit, and Next link. It is fictional text written for testing.
4. A link-only title opens `/read/<id>` with an **Open Original** button; the original opens only when you click it.
5. `/health` returns `{"status":"ok"}`.
6. `/anything-else` and `/read/unknown` show the "Page not found" page with a 404 status.

## Reader manual checks (Phase 03; not run / not verified)

Open `/read/demo-story` at about 360 px, 412 px, and desktop width (browser dev tools device mode, plus a real Android phone if available):

1. Text is legible; the column is narrow with generous line and paragraph spacing; no horizontal scrolling.
2. A- and A+ change text size and disable at the limits; Dark/Light mode switches the theme.
3. Refresh the page: size and theme are kept (`vyasa.v1.fontStep`, `vyasa.v1.theme` in localStorage).
4. Tab through Back to library, A-, A+, theme toggle, and Previous/Next; focus is visible.
5. The verse keeps its line break. A link-only item (`/read/aruni-uddalaka`) shows no story text and no reader controls.

## Content rules (Phase 02)

- `content_status` is `link_only` or `approved`. `approved` items load a JSON file from `data/content/` (blocks of `heading`, `paragraph`, `verse`, each with a stable `id`).
- Only the fictional demo is `approved`. No explicit permission to host VyasaOnline translations is recorded in `docs/CONTENT_ACCESS_DECISION.md`, so there is no importer or fetcher.

## Project documents

| File | Purpose |
|---|---|
| `CLAUDE.md` | Mandatory Claude Code behavior, restrictions, and short response format |
| `PLAN.md` | MVP scope, phase boundaries, data behavior, manual acceptance |
| `docs/PROGRESS.md` | **Required by `CLAUDE.md`** to know which phase is pending or complete |
| `SOURCES_AND_RIGHTS.md` | Original website links and permission questions |
| `prompts/PHASE_XX_*.md` | Existing phase-specific Claude Code instructions |
| `docs/DEVELOPMENT_LOG.md` | Create/update when phase work is completed; newest entry first |

Avoid extra index/reference files unless project complexity actually requires them.

## Claude Code: start and continue

1. Put `CLAUDE.md`, `README.md`, `PLAN.md`, `SOURCES_AND_RIGHTS.md`, `docs/PROGRESS.md`, and the `prompts/` folder in the project.
2. Request **Phase 00** using `prompts/PHASE_00_SOURCE_AND_RIGHTS.md`.
3. Claude reads minimum relevant context, gives a brief plan, then **waits for `APPROVED`** (required by the phase prompts).
4. After approval, Claude edits **only that phase**, updates progress and development log, reports affected files and `Verification: not run`, then stops.
5. Review changes yourself. Request the next phase explicitly when ready. Never generate the whole app in one request.

**Important:** Current `CLAUDE.md` forbids executing commands, tests, builds, installs, Git, and deployment. Claude may prepare deployment instructions in Phase 06 but must **not** deploy. You run manual checks and commands separately.

## Phases at a glance

- **00:** Rights/technical feasibility decision.
- **01:** Minimal Flask foundation.
- **02:** Catalog and permitted-content boundary.
- **03:** Kannada reading UI, font/theme settings.
- **04:** Auto-resume and bookmarks.
- **05:** Android-installable PWA.
- **06:** EC2 deployment documentation and safe configuration.

See `PLAN.md` for specific deliverables and acceptance criteria.

## Deployment notes (after Phase 06)

- For Android installation, provide a trusted **HTTPS hostname**. A bare HTTP EC2 public IP is generally insufficient for PWA installation.
- Keep Gunicorn on loopback, expose only Nginx's public web ports, and restrict SSH access.
- Do not expose Flask debug mode, private credentials, or unauthorized translated content.
- Deployment commands and setup steps belong in Phase 06 runbook, **not** in the development instructions Claude executes.

## What is not promised

VyasaOnline content is not automatically licensed for republication. With `link_only` content, you get navigation to the original website, **not** a full in-app reader with scroll restoration. The full reading/resume experience needs content you are allowed to serve. See `SOURCES_AND_RIGHTS.md`.
