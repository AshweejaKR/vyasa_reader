# Vyasa Reader

**Status:** Planning only — no live app yet.

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
