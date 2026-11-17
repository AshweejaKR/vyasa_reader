# Phase Progress — Vyasa Reader

Current phase: **All planned phases (00–06) written**
Current status: **Permission recorded; direct website-fetch support merged to main (PR #4); imported-text review guard and docs on `fix/first-story-review-gate` (not merged). Six-paragraph `aruni-uddalaka` content reviewed against rendered source and approved in a PRIVATE overlay (2026-11-17); private app installation, runtime, Android and EC2 verification pending**

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
- [ ] Install approved private JSON plus private catalog overlay into a checkout and confirm `/read/aruni-uddalaka` displays correctly.
- [ ] Manual reader/resume/bookmark checks and handling of revised paragraph anchors.
- [ ] Manual revision refresh for Adi Parva, additional recensions, and Shastra Samgraha when available.
- [ ] Separately decide bounded offline text caching; existing PWA caches shell only.
- [ ] HTTPS/Android/EC2 verification (including PNG icons and app-icon resume); none run.

Permission evidence: private email reply dated 2026-11-10; do not commit correspondence or personal addresses.
