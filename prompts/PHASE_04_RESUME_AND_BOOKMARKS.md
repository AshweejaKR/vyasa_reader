# Claude Code prompt — Phase 04: automatic save and resume

Implement the project's key feature: **resume the previous in-app story and nearest saved paragraph when the PWA is reopened**. This must work with long Kannada texts on Android Chrome.

## Required workflow

1. Read `CLAUDE.md`, `README.md`, `PLAN.md`, `SOURCES_AND_RIGHTS.md`, `docs/PROGRESS.md`, this prompt, and only files relevant to this phase.
2. First respond with a short plan (1–3 steps) and file paths. **WAIT for `APPROVED` before editing.**
3. After approval, implement **this phase only**; keep code simple (functions, few files, ~150 lines/file), no factories, extra frameworks, tests, mocks, scraping, or unrelated work.
4. **Do not execute** shell/Python, builds, tests, installs, Git, deployment, or remote AWS actions. No fabricated verification. Document commands for user execution when needed.
5. Update `docs/PROGRESS.md` and prepend a concise entry in `docs/DEVELOPMENT_LOG.md` only after completing the phase. State `Verification: not run`. **STOP.**

## Work after approval

- Use a versioned `localStorage` schema. Save last `item_id`, `paragraph_id`/block anchor, relative offset or scroll ratio, timestamp and optional per-item locations. Use stable catalog IDs; never use title as key.
- Save with a small debounce while scrolling and flush on `visibilitychange`/`pagehide` and navigation. Avoid high-frequency writes.
- On a **fresh app-icon launch**, auto-open the last in-app item by default. Add an Auto-resume ON/OFF setting; when OFF show a prominent **Continue Reading** button instead. Do not redirect on deliberate Home clicks or explicit item navigation; avoid redirect loops.
- Restore position after layout/font rendering, prefer stable paragraph anchors over raw pixels, clamp bad/old values and gracefully handle deleted items.
- **Explicit navigation wins:** if user deliberately opens item B, never bounce to saved item A. Font-size changes should retain the nearest paragraph.
- Add simple **bookmark this spot** and a bookmark list or action. Keep local storage only. Explain limitations if storage cleared, incognito used or a different phone/browser is opened.
- Never claim the app can track scroll position inside VyasaOnline external pages. Show an honest notice on `link_only` items.

## Acceptance

Manual acceptance (not run by Claude): read long demo -> scroll mid-way -> close browser/PWA -> reopen from icon -> automatically correct item and nearby paragraph by default. Refresh, theme/font change, Previous/Next, empty/malformed localStorage and explicit navigation all behave safely.
