# Claude Code prompt — Phase 03: simple comfortable Kannada reader

Improve in-app reading comfort on Android. Keep it lightweight with vanilla CSS/JavaScript, no design system or UI component framework.

## Required workflow

1. Read `CLAUDE.md`, `README.md`, `PLAN.md`, `SOURCES_AND_RIGHTS.md`, `docs/PROGRESS.md`, this prompt, and only files relevant to this phase.
2. First respond with a short plan (1–3 steps) and file paths. **WAIT for `APPROVED` before editing.**
3. After approval, implement **this phase only**; keep code simple (functions, few files, ~150 lines/file), no factories, extra frameworks, tests, mocks, scraping, or unrelated work.
4. **Do not execute** shell/Python, builds, tests, installs, Git, deployment, or remote AWS actions. No fabricated verification. Document commands for user execution when needed.
5. Update `docs/PROGRESS.md` and prepend a concise entry in `docs/DEVELOPMENT_LOG.md` only after completing the phase. State `Verification: not run`. **STOP.**

## Work after approval

- Create a focused reader view: narrow readable text column (roughly 65–75ch/appropriate mobile width), 16–20 px baseline on mobile, generous line spacing and paragraph gaps. Honor browser text zoom.
- Use a Unicode Kannada-capable font stack with sensible device fallbacks; **no unlicensed bundled fonts**.
- Provide visible A−/A+ font controls and light/dark toggle; persist preferences in versioned localStorage keys.
- Preserve Kannada punctuation/verse line breaks. Keep title, source credit, Previous/Next and a simple back-to-library control.
- Make all controls accessible by keyboard and touch (good labels/contrast); avoid auto-play, animations or unnecessary menus.
- Document manual checks at approximately 360 px and 412 px viewport widths and desktop; do not claim to have run them. Do not add book-like page-turn animations.

## Acceptance

Manual acceptance (not run by Claude): reader is legible on Android; text size and theme survive refresh; no horizontal overflow; external link-only content is not falsely shown as in-app text.
