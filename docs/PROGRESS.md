# Phase Progress — Vyasa Reader

Current phase: **All planned phases (00–06) written**
Current status: **Permission recorded; default in-app Kannada story/Parva/chapter reading implemented as source on `fix/first-story-review-gate` (not merged), with explicit Original links, optional password, private caching and fetch limits. Reviewed `aruni-uddalaka` overlay exists privately. Flask runtime, Android, and EC2 remain not run / unverified.**

Note: Phase 01 was implemented before Phase 00; the sequence is now reconciled. Phase 00 originally used `link_only`; 2026-11-10 author permission now allows the described personal-app website-text use. Existing catalog items remain `link_only` until individually imported.

| Phase | Status |
|---|---|
| 00 — Source and rights | Complete (decision updated with 2026-11-10 written permission; integration not started) |
| 01 — Flask foundation | Complete (written; verification not run) |
| 02 — Catalog and content | Complete (written; verification not run) |
| 03 — Reader UI | Complete (written; verification not run) |
| 04 — Resume and bookmarks | Complete (written; verification not run) |
| 05 — PWA | Complete (written; 192/512 PNG and SVG icons present; Android verification not run) |
| 06 — EC2 deployment docs | Complete (runbook and config written; not deployed; verification not run) |

Rules: Change only the requested phase after approval. Mark complete only after its deliverables are written. Record runtime verification separately; never assume commands or tests were run. Update `docs/DEVELOPMENT_LOG.md` after each completed implementation task.

## Post-permission work (pending; not a completed phase)

- [x] Prepared one-story manual importer and per-item attribution for `aruni-uddalaka`; merged to main (2026-11-15).
- [x] One-time direct website-fetch importer and source references merged to main (PR #4; importer not run; 2026-11-15).
- [x] Inspected primary source page: six narrative paragraphs plus unrelated index/comments. Added server-side imported-text review gate on branch `fix/first-story-review-gate` (not run; 2026-11-15).
- [x] Strengthened one-story importer on the **same branch**: stop at “The other stories”; require exactly six paragraphs and known opening/closing text. Static review only; no private JSON generated and no runtime checks run (2026-11-15).

- [x] Prepared private six-paragraph `aruni-uddalaka.json` from retrieved VyasaOnline text with source URL, attribution, import time, and SHA-256 (2026-11-15); repo importer not executed.
- [x] Compared six of six paragraphs with manually captured plain text of the rendered original webpage; all matched after removing link formatting/normalizing spaces. Approved content JSON and private catalog overlay prepared separately on 2026-11-17; **not committed to Git**.
- [x] Reviewed and approved first story **in private overlay only**; public catalog intentionally stays `link_only`.
- [x] Published Windows-first local setup and verification instructions in `docs/LOCAL_VERIFICATION.md` (documentation only, 2026-11-17).
- [x] Implemented opt-in private HTML-index/story/chapter loading and ignored server cache with HTTP Basic access control, per-worker fetch quota, source validation, unreviewed preview notice, and reader resume support on the same branch (2026-11-17). **Static source only; runtime not run/verified**. See `docs/ON_DEMAND.md`.
- [x] Source fix for reported empty-index error: broadened list link extraction outside specific WordPress post containers, preserved the verified 59-story index, and avoided redundant Parva footer links in chapter lists (2026-11-17). Source inspection/static review only; user runtime still unverified.
- [x] Updated default reading flow: Stories/Parvas open in-app indexes, selected HTML chapters display in reader, original links are explicit, password is optional, no `VYASA_ON_DEMAND` flag (2026-11-17; source only, not run).
- [ ] Install approved private JSON plus private catalog overlay into a checkout and confirm `/read/aruni-uddalaka` displays correctly.
- [ ] Manual reader/resume/bookmark checks and handling of revised paragraph anchors.
- [ ] Manual revision refresh for Adi Parva, additional recensions, and Shastra Samgraha when available.
- [ ] Separately decide bounded offline text caching; existing PWA caches shell only.
- [ ] HTTPS/Android/EC2 verification (including PNG icons and app-icon resume); none run.

Permission evidence: private email reply dated 2026-11-10; do not commit correspondence or personal addresses.
