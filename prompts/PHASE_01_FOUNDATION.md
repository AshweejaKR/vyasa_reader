# Claude Code prompt — Phase 01: minimal Flask foundation

Build the simplest runnable project for **Vyasa Reader**. The app must be mobile-first and support Kannada UTF-8, but **do not ingest third-party content yet**.

## Required workflow

1. Read `CLAUDE.md`, `README.md`, `PLAN.md`, `SOURCES_AND_RIGHTS.md`, `docs/PROGRESS.md`, this prompt, and only files relevant to this phase.
2. First respond with a short plan (1–3 steps) and file paths. **WAIT for `APPROVED` before editing.**
3. After approval, implement **this phase only**; keep code simple (functions, few files, ~150 lines/file), no factories, extra frameworks, tests, mocks, scraping, or unrelated work.
4. **Do not execute** shell/Python, builds, tests, installs, Git, deployment, or remote AWS actions. No fabricated verification. Document commands for user execution when needed.
5. Update `docs/PROGRESS.md` and prepend a concise entry in `docs/DEVELOPMENT_LOG.md` only after completing the phase. State `Verification: not run`. **STOP.**

## Work after approval

- Make a minimal Flask application with `/` home, `/health` (simple status), and a catalog data loader. Keep one clear app entry point and dependency file.
- Create a small `data/catalog.json` fixture with 2–3 **metadata-only** link-only example stories using exact known VyasaOnline URLs. Include stable ID, Kannada title, collection, sort order, source URL, content status, and optional local content path.
- Add simple accessible page styling; display site identity, Stories and Parvas navigation placeholders, and empty Continue Reading state.
- Add safe handling for missing/bad catalog and an informative 404. Avoid arbitrary file paths from browser input.
- Document intended start commands in README and one manual smoke-check procedure. Do not run them or claim success.

## Acceptance

Manual acceptance (not run by Claude): app starts locally, Kannada titles render, links open, health route works. No copied story bodies, scraping, or database.
