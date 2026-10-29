# CLAUDE.md — Vyasa Reader

## Goal
Build a small, readable Kannada Mahabharata PWA with automatic reading resume.
Use Flask + plain HTML/CSS/JS. No database or extra framework in the MVP.
Never import/rehost third-party translations without documented permission.

## Start Here — Minimum Context
1. Read `README.md`, `PLAN.md`, and `SOURCES_AND_RIGHTS.md` when present.
2. Read `docs/PROGRESS.md` for phase state.
3. Read ONLY the requested `prompts/PHASE_XX_*.md`.
4. Read other Markdown, reference, and source files only as the phase requires.
5. If `docs/PROGRESS.md` is missing or conflicts with the requested phase, ask ONE short question; do not guess phase status.

## Strict Phase Mode
- Follow `PROGRESS.md` in order. Implement exactly ONE explicitly requested phase.
- Do not skip, combine, anticipate, or implement later phases.
- Preserve existing architecture, interfaces, public APIs, and file layout.
- Reuse existing code. No unrelated edits or refactors.
- If the phase prompt requires `APPROVED`, give a brief plan and WAIT before edits.
- If the phase is clear and no approval is required, proceed without questions.
- Stop immediately after the requested phase. Wait for the next instruction.

## Coding Rules
- Simplicity > architecture. Working code > perfect design.
- No over-engineering, factory patterns, extra layers, or needless abstractions.
- Prefer small functions over classes. Add a class only when clearly necessary.
- One responsibility per module; do not split tiny logic across many files.
- Aim for approximately 150 lines or fewer per source file; do not sacrifice clarity to force the limit.
- Simple algorithms, minimal dependencies, no premature optimization.
- Avoid duplicated logic, placeholders, TODO/FIXME, and commented-out code.
- Add only essential error handling; never invent external API behavior.
- Modify existing files first. Add new files only when necessary.
- No tests, test files, mocks, demos, or benchmarks unless explicitly requested.
- No speculative features, bulk crawling, unauthorized content copying, or unrelated tooling.

## Execution and Safety
- Source edits only: do NOT run shell/Python commands, builds, tests, installs, or git commands.
- Do NOT deploy, push, change AWS, or access remote systems unless explicitly authorized.
- Do not simulate execution or fabricate logs, results, API responses, or success claims.
- State unverified behavior as **not run / not verified**.
- Ask one concise question only for a material blocker; otherwise use existing facts.

## Updates After Implementation
- Mark only the completed phase in `docs/PROGRESS.md`.
- Prepend a brief entry to `docs/DEVELOPMENT_LOG.md`: date, phase, summary, files added/modified, docs updated.
- Preserve previous log entries. Update other docs only when affected.
- Do not touch `CHANGELOG.md` unless requested.
- If stopping at an approval gate or blocker, do NOT mark the phase complete.

## Response Format
- Short, direct; no filler, repetition, long explanation, or emojis.
- Put code in project files, not lengthy chat output.
- Before approval (only when required): `Plan: <1–3 steps>; Files: <paths>; Awaiting APPROVED.`
- After implementation, report only:
  - `Modified: <files or none>`
  - `Added: <files or none>`
  - `Progress/log: updated or blocked`
  - `Verification: not run` (unless explicitly verified by an allowed method)
- Then STOP. No next-phase proposal.

## Final Check (Internal Only)
Requested phase only? Existing design intact? Minimal code/files? No tests or commands?
Progress and log accurate? No unsupported success claims? Short response?
