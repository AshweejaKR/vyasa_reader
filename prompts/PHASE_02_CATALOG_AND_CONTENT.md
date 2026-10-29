# Claude Code prompt — Phase 02: catalog and allowed content

Extend Vyasa Reader to show content **inside** the reader only when that content is expressly permitted. The default original-source items remain link-only.

## Required workflow

1. Read `CLAUDE.md`, `README.md`, `PLAN.md`, `SOURCES_AND_RIGHTS.md`, `docs/PROGRESS.md`, this prompt, and only files relevant to this phase.
2. First respond with a short plan (1–3 steps) and file paths. **WAIT for `APPROVED` before editing.**
3. After approval, implement **this phase only**; keep code simple (functions, few files, ~150 lines/file), no factories, extra frameworks, tests, mocks, scraping, or unrelated work.
4. **Do not execute** shell/Python, builds, tests, installs, Git, deployment, or remote AWS actions. No fabricated verification. Document commands for user execution when needed.
5. Update `docs/PROGRESS.md` and prepend a concise entry in `docs/DEVELOPMENT_LOG.md` only after completing the phase. State `Verification: not run`. **STOP.**

## Work after approval

- Add a straightforward Stories list and Parvas/Chapters list, with stable collection-specific ordering. Seed only a few curated original URLs; **no bulk harvesting**.
- Implement a simple `/read/<item_id>` route with a clear split: `link_only` shows title/source and **Open Original** button; `approved` loads a local whitelisted UTF-8 content fixture.
- For in-app testing, create 1–2 clearly marked **self-written fictional demo** Kannada paragraphs. Do not paraphrase or extract VyasaOnline translations for fixture content.
- Use a minimal JSON content format with text blocks (`paragraph`, `heading`, optionally `verse`) and stable block IDs; escape render by default. Do not render arbitrary remote HTML/JS.
- Implement Previous/Next inside one collection, guarded against missing entries, and visible author/source attribution fields.
- If the Phase 00 rights document shows actual explicit permission, describe the conditions and an **optional user-supplied local-file import path**; otherwise do not build a remote fetcher.

## Acceptance

Manual acceptance (not run by Claude): both lists browse correctly; approved/demo reading works; link-only items redirect only on deliberate user action; source credit visible; there is no proxy/scraper.
