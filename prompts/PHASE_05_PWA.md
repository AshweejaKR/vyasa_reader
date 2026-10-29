# Claude Code prompt — Phase 05: Android-installable PWA

Make Vyasa Reader installable from Android Chrome as a PWA and behave like an app. Do not turn it into an APK or add a complex JavaScript build pipeline.

## Required workflow

1. Read `CLAUDE.md`, `README.md`, `PLAN.md`, `SOURCES_AND_RIGHTS.md`, `docs/PROGRESS.md`, this prompt, and only files relevant to this phase.
2. First respond with a short plan (1–3 steps) and file paths. **WAIT for `APPROVED` before editing.**
3. After approval, implement **this phase only**; keep code simple (functions, few files, ~150 lines/file), no factories, extra frameworks, tests, mocks, scraping, or unrelated work.
4. **Do not execute** shell/Python, builds, tests, installs, Git, deployment, or remote AWS actions. No fabricated verification. Document commands for user execution when needed.
5. Update `docs/PROGRESS.md` and prepend a concise entry in `docs/DEVELOPMENT_LOG.md` only after completing the phase. State `Verification: not run`. **STOP.**

## Work after approval

- Add a valid web app manifest (name, short name, icons, `start_url`, `scope`, `display=standalone`, theme/background colors) and proper meta/link tags.
- Provide simple 192x192 and 512x512 PNG icons **you create or otherwise have permission to use**. Do not use the source site's logo without permission.
- Add a minimal service worker: cache same-origin app shell/static assets. Handle updates deliberately and show a helpful offline fallback.
- Cache local content only when expressly permitted by rights decision; do not cache/proxy/redistribute third-party web pages or PDFs.
- Ensure service worker scope/paths work behind Nginx and HTTPS; document that `localhost` works for development but public plain HTTP EC2 IP does not provide a standard installable PWA experience.
- Document install steps for Chrome on Android and one remove/reinstall/troubleshooting path.

## Acceptance

Manual acceptance (not run by Claude): manifest and service worker work on localhost or HTTPS; app launches without browser chrome when installed; offline app shell is usable; no restricted source content is stored.
