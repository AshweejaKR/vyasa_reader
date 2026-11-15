# Content Access Decision

**Decision: permission received for the described personal, non-commercial Vyasa Reader use (2026-11-10).** Existing catalog items remain `link_only` until their content is actually imported, attributed, and reviewed. Do not mark all items `approved` automatically.

## Permission evidence and scope

Written permission: BM Ramesh replied on 2026-11-10 to the 2026-11-04 personal, non-commercial Vyasa Reader request, saying “Please go ahead and use the content on my website. No issues.” The request expressly described hosting selected Kannada translation text on personal AWS, readability-only reformatting, limited personal offline browser caching, and one-time rate-limited retrieval from website or GitHub. Reply also asks whether revised translations (Adi Parva in progress), additional recension portions, and Shastra Samgraha can be reflected when ready. User acknowledged on 2026-11-11. Keep the original correspondence privately; do not commit the PDF or email addresses to this public repository.

- Evidence: email thread titled *RE: Vyasa Mahabharata — Request for Permission to Use VyasaOnline Kannada Mahabharata Content in a Personal Reading App*, reply dated 2026-11-10. Private copy held by project owner, **not stored in public Git**.
- Permitted within the described app: selected website Kannada Mahabharata text, personal AWS hosting, readability-preserving formatting, limited browser offline caching, and modest one-time retrieval. Use the website as the expressly approved source; confirm GitHub-repository reuse separately if needed because the reply explicitly names website content.
- Attribution promised: BM Ramesh / VyasaOnline and direct link to the original page for each imported item. Preserve text meaning and remove material if requested.
- Not established: a general open-source license, unrestricted commercial distribution, rights to third-party images/illustrations/PDFs, mass scraping, or republishing to other products. Keep those excluded pending separate evidence.
- Author requested future compatibility with revised translations, additions from other recensions, and the Shastra Samgraha series. This is a future-content request, **not** evidence that revisions are already published or a mandate for live scraping.

## Safe content workflow

1. Keep `link_only` as default; record each imported item’s original URL, title, translator attribution, source revision/date, import date, and local file path.
2. Import a small, explicitly selected website text item; review formatting and attribution before changing its catalog status to `approved`.
3. Keep stable item/block identifiers when refreshing translations so bookmarks and resume can fall back gracefully if paragraphs change.
4. Provide a manual, rate-limited update path for revised source text; never auto-overwrite reader content or scrape broadly. Track revisions and preserve rollback ability.
5. Offline caching is permitted for this personal app, but opt into bounded same-origin text caching only after implementing clear versioning, cache limits, and invalidation. Existing service worker still caches app shell only.
6. Keep original correspondence private. Record any new restrictions or withdrawal here and honor removal requests.

## Historical research

Earlier source checks (2026-10-29) found the stories and Parvas indexes, chapter index, and the public GitHub repository; no obvious repository license was found. Those checks predate the direct written permission and no longer block the narrowly described website-text use. See `SOURCES_AND_RIGHTS.md` for entry points and unresolved technical details.
