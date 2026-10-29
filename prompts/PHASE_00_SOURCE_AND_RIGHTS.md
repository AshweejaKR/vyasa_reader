# Claude Code prompt — Phase 00: source feasibility and rights

You are working on **Vyasa Reader**, a small Kannada Mahabharata PWA. This phase is **research and a decision document only**, not application code.

## Required workflow

1. Read `CLAUDE.md`, `README.md`, `PLAN.md`, `SOURCES_AND_RIGHTS.md`, `docs/PROGRESS.md`, this prompt, and only files relevant to this phase.
2. First respond with a short plan (1–3 steps) and file paths. **WAIT for `APPROVED` before editing.**
3. After approval, implement **this phase only**; keep code simple (functions, few files, ~150 lines/file), no factories, extra frameworks, tests, mocks, scraping, or unrelated work.
4. **Do not execute** shell/Python, builds, tests, installs, Git, deployment, or remote AWS actions. No fabricated verification. Document commands for user execution when needed.
5. Update `docs/PROGRESS.md` and prepend a concise entry in `docs/DEVELOPMENT_LOG.md` only after completing the phase. State `Verification: not run`. **STOP.**

## Work after approval

- Review the known VyasaOnline pages and GitHub source linked in `SOURCES_AND_RIGHTS.md` using available browser or provided evidence, **not shell commands**, and only reasonable individual requests. Do not run a crawler, downloader, mirror, or automated bulk import.
- Check published terms or explicit license if any and document **what is proven versus unknown**. Public download, publicly visible HTML, or public GitHub is not republication permission.
- Record content structure differences: independent Kannada story pages vs Parva/chapter pages; check one representative page of each if accessible.
- Assess practical options: `link_only` now; `approved` local text import if actual permission/license becomes available. Do not assume cross-origin access or iframe control.
- Create `docs/CONTENT_ACCESS_DECISION.md` with source URLs, source IDs, rights status, technical constraints, attribution pattern, open questions and the **request-to-owner wording**.
- Set the default decision to `link_only` until affirmative permission is documented. This allows app development using original demo text but does not claim full translation reading inside app.

## Acceptance

The document states the rights gate clearly and distinguishes externally linked items from hostable content. No original translation copied to repository. No application code, deployment, or remote actions.
