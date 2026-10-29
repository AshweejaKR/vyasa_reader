# PLAN.md — Vyasa Reader

**Status:** Planning; app not implemented.  **Phases:** 00–06.  **Priority:** Simple, comfortable reading.

## Goal

Build an independent, Android-first Kannada Mahabharata reader that also works on PC. Host on an existing AWS EC2 instance. On reopening the installed app, resume the last **in-app** story near the saved paragraph. This is **not** an official VyasaOnline app.

## MVP

- Browse a small, curated catalog: Kannada stories and Parva/chapter links.
- Read **permitted** content in a clean, responsive layout; large Kannada text, font controls, dark/light mode, Previous/Next.
- Save the last in-app item and paragraph position automatically in browser `localStorage`; enable auto-resume by default, provide Continue Reading and bookmarks.
- Install as an Android PWA over HTTPS; use a home-screen icon and basic offline app shell.
- Work on mobile and desktop. Progress is **device/browser-specific**, not synchronized.

**Out of scope:** Database, login, cloud sync, React, APIs for third-party scraping, bulk import, AI features, analytics, and unauthorized copies of translations.

## Content-rights gate

- Use `SOURCES_AND_RIGHTS.md` for known URLs and unknown permissions.
- Public accessibility or a public GitHub repository **does not** prove reuse rights.
- Until rights are established, store titles and original URLs as `link_only`. Use only independently written sample text for the in-app reader.
- Add actual translations only when a license or written permission covers hosting and any intended caching/transformation. Keep source attribution and URLs.
- External pages may open in a browser; **the app cannot reliably resume exact scroll position on VyasaOnline**. Do not promise it.

## Minimal stack

- Server: Python 3 + Flask; Gunicorn for production.
- Client: server-rendered HTML, plain CSS/JavaScript; no frontend framework or build step.
- Data: curated JSON catalog and permitted plain-text/JSON paragraphs; no database.
- State: versioned `localStorage` for settings, bookmarks, and reading progress.
- Deployment: existing Amazon Linux EC2, Nginx, HTTPS, systemd.

## Phase plan

| Phase | Scope | End deliverable |
|---|---|---|
| **00** | Review source structure, reuse rights, and alternatives; no app code | `docs/CONTENT_ACCESS_DECISION.md`; default `link_only` unless permission is proven |
| **01** | Minimal Flask app, homepage, small catalog, basic error handling | Server source and minimal template/assets; no content copying |
| **02** | Stories/Parvas catalog, approved-vs-link-only rendering, Previous/Next | Ordered navigation and safe content boundary |
| **03** | Mobile/PC reader UI, readable Kannada, font size, dark mode | Responsive reading interface; settings saved locally |
| **04** | Save/restore item + paragraph position; bookmarks | Auto-resume on app-icon launch; explicit navigation always wins |
| **05** | Manifest, icons, service worker, install flow | HTTPS-installable PWA and offline shell only |
| **06** | EC2 deployment instructions/configuration | Deployment runbook for Gunicorn + Nginx + systemd + HTTPS |

**Phase prompts:** `prompts/PHASE_00_SOURCE_AND_RIGHTS.md` through `prompts/PHASE_06_EC2_DEPLOY.md` in this project. Implement only one explicitly requested phase. No later-phase work.

## Strict implementation workflow

1. Use `CLAUDE.md` as the coding and execution policy. Read `README.md`, `PLAN.md`, `SOURCES_AND_RIGHTS.md`, `docs/PROGRESS.md`, and **only** the selected phase prompt/relevant files. Do not read unrelated docs.
2. Check `docs/PROGRESS.md`. Start with Phase 00. Never infer completion from file names alone.
3. Each existing phase prompt requires a brief proposed change list and user reply **`APPROVED`** before edits. No edits at this approval gate.
4. After approval, edit only current-phase files. Prefer functions, existing modules, few dependencies, and roughly 150 lines per source file (soft limit). No factories, unnecessary layers, tests, mocks, or demos.
5. Never execute shell/Python, builds, tests, installs, Git, or deployment commands under the current `CLAUDE.md`. Make source/documentation changes only. Never claim runtime checks passed.
6. Update `docs/PROGRESS.md` and prepend a brief entry in `docs/DEVELOPMENT_LOG.md` after completed phase work. Record verification as **not run** unless separately verified. Stop.

**Conflict rule:** `CLAUDE.md` restrictions take priority if a phase prompt conflicts with command-execution or other restrictions. Preserve the phase's actual feature scope and approval gate.

## Reader state and behavior

- Save `last_item_id`, stable paragraph anchor, relative offset, and update time under a versioned local key.
- Save on meaningful navigation, throttled/debounced scroll, and page hide. Restore after text/fonts settle; fall back safely if text or anchor changed.
- Auto-resume only on a fresh app launch, not when the user deliberately selects a different story.
- Use safe text rendering; never inject arbitrary third-party HTML or run remote scripts.

## Manual acceptance (not automated by Claude)

- [ ] Kannada text readable on Android and desktop; font/theme controls work.
- [ ] Close/reopen installed app: last **in-app** story and nearby paragraph return.
- [ ] Explicitly selected chapter does not get overridden by saved progress.
- [ ] Link-only items open the original source; no false scroll-resume claim.
- [ ] Storage cleared/private mode gracefully loses saved position.
- [ ] Installed HTTPS PWA launches standalone; offline shell handles missing content.
- [ ] EC2 uses HTTPS, keeps Gunicorn private, and restarts after reboot.

## File policy

Create files only as each phase needs them. No big skeleton up front. Keep `README.md` for usage, `PLAN.md` for scope, `docs/PROGRESS.md` for phase state, and `docs/DEVELOPMENT_LOG.md` for completed work. No `CHANGELOG.md` updates unless requested.
