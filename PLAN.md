# PLAN.md — Vyasa Reader

**Status:** Phases 00–06 written; runtime and deployment unverified. Permission recorded 2026-11-10. Direct, one-story website-fetch update merged to `main` in PR #4 (2026-11-15). First-story review enforcement is on `fix/first-story-review-gate` pending review/merge; actual website-text import and manual approval still pending.

## Goal

Build an independent, Android-first Kannada Mahabharata reader that also works on PC. Host on an existing AWS EC2 instance. On reopening the installed app, resume the last **in-app** story near the saved paragraph. This is **not** an official VyasaOnline app.

## MVP

- Browse a small, curated catalog: Kannada stories and Parva/chapter links.
- Read **permitted** content in a clean, responsive layout; large Kannada text, font controls, dark/light mode, Previous/Next.
- Save the last in-app item and paragraph position automatically in browser `localStorage`; enable auto-resume by default, provide Continue Reading and bookmarks.
- Install as an Android PWA over HTTPS; use a home-screen icon and basic offline app shell.
- Work on mobile and desktop. Progress is **device/browser-specific**, not synchronized.

**Out of scope:** Database, login, cloud sync, React, bulk scraping, AI features, analytics, unrelated commercial redistribution, and third-party media without separate rights.

## Content-rights gate

- Use `SOURCES_AND_RIGHTS.md` for known URLs and unknown permissions.
- Public accessibility or a public GitHub repository **does not** prove reuse rights.
- Website-text permission is recorded in `docs/CONTENT_ACCESS_DECISION.md` (2026-11-10). Keep existing entries `link_only` until each is individually imported, attributed, and reviewed.
- Import selected website text under the documented personal, non-commercial permission. Preserve BM Ramesh / VyasaOnline attribution and original URLs. Exclude third-party illustrations/PDFs and broad GitHub reuse pending separate confirmation.
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

## Post-permission work (one scoped task at a time)

1. **Permission and metadata:** Record the private evidence reference and per-item attribution/source URL. No permission PDF or email addresses in public Git.
2. **Selected website-text import:** Prepare a single, manual or one-time website-HTTPS retrieval path; preserve paragraph structure, escape source HTML, keep stable IDs, and review each item before switching `link_only` to `approved`. The short VyasaOnline story is the primary permitted source; the author's GitHub `content` branch and hosted reader are chapter references, not interchangeable text or broad reuse licenses.
3. **Reader validation:** Manually check Kannada rendering, Previous/Next, bookmarks, auto-resume, and fallbacks after text revisions. Existing implementation remains unverified.
4. **Revisions:** Support manual refresh and source version metadata for revised Adi Parva, additional recension material, and Shastra Samgraha when published. Avoid unattended scraping; keep a rollback path.
5. **Offline content:** Extend app-shell-only caching to selected approved same-origin text only after bounded storage, invalidation, versioning, and removal handling are designed and approved.
6. **PWA/deployment:** Supply PNG icons and manually verify HTTPS installation, Android reopen, offline behavior, and EC2 security. No deployment implied by document updates.

These are proposed maintenance/integration tasks, **not completed phases**. Keep the existing simple Flask + JSON architecture. Work on only one explicitly requested task at a time.

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
