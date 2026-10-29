# Content Access Decision

**Decision: `link_only`.** No translation text is hosted, copied, or cached by Vyasa Reader until an explicit license or written permission is documented here. This is technical planning, not legal advice.

**Rights status: NOT verified.** Public access and a public GitHub repository are not republication permission.

## Evidence basis

Pages were fetched individually on 2026-10-29 through a page-to-text tool that summarizes the page. Raw HTML, page footers, and linked sub-pages were not inspected directly. No crawler, download, or shell command was used. Absence of a notice in a summary is weaker than absence on the page itself.

## Verified (observed 2026-10-29, via summarized fetch)

| Source | Observation |
|---|---|
| Stories index `https://www.vyasaonline.com/stories-in-mahabharata-kannada/` | Numbered list of 59 Kannada story links; one free PDF (Stories Vol. 1, dated 21 Jun 2020); no copyright, license, or terms notice seen; no translator named. |
| Parvas index `https://www.vyasaonline.com/translations10/` | 18 Maha Parvas, each with a page link and PDF link; Harivamsha listed as item 19, no PDF, said to be still in translation; no copyright, license, or terms notice seen. Page credits J.A.B. van Buitenen's 1973 English translation as a source and the BORI Critical Edition as the Sanskrit base. |
| Example story page (Aruni Uddalaka, URL in `SOURCES_AND_RIGHTS.md`) | Title, breadcrumb, story text, one illustration, inline links to encyclopedia entries, ~58 related story links, previous/next navigation, share icons, comment form; no copyright or license notice seen; no translator credit visible in the content; footer credits only the theme and WordPress. |
| Contact page `https://www.vyasaonline.com/contact/` | Contact form only (name, email, subject, message); no email address listed; no terms of use seen. |
| GitHub `https://github.com/vyasaonline/mahAbhArata` | Root files shown: `.github`, `content` (submodule), `data`, `themes`, `.gitignore`, `.gitmodules`, `config.toml`. No LICENSE file or license statement shown. The "View all files" listing was not expanded, so one could exist beyond what was shown. About text: translation of the Sukthankar critical edition into Kannada by BM Ramesh. |

## Documented in `SOURCES_AND_RIGHTS.md`, not rechecked

- The Kannada translation of the 18 Maha Parvas was completed in 2022.
- Chapter-wise index: `https://www.vyasaonline.com/chapter-wise-translation-of-mahabharata/`.
- GitHub-hosted reader: `https://vyasaonline.github.io/mahAbhArata/`.
- A representative Parva or chapter page was **not** inspected; only the Parvas index was.

## Unknown (blocks any `approved` content)

1. Permission to copy, transform, host, cache, or redistribute the Kannada text, illustrations, or PDFs.
2. Any license in the GitHub repo, the `content` submodule, or the site beyond what was seen.
3. Whether the WordPress REST API is enabled or intended for reuse; not checked.
4. Whether iframe embedding or third-party proxying is allowed; do not assume it is.
5. Whether stable IDs and pagination exist across all chapters.
6. Required attribution wording, and whether non-commercial and offline-caching uses are allowed.

## Entry points and handling

| Type | Source | Handling now |
|---|---|---|
| Independent story pages (59) | Stories index and individual story URLs | `link_only`: title and original URL in the catalog, opened on VyasaOnline. |
| Parva and chapter pages (18 + Harivamsha) | Parvas index and per-Parva pages | `link_only`, same as above. Chapter-level structure still to be inspected. |
| PDFs | Linked from the indexes | Link only. Do not rehost. |
| In-app reader text | Self-written demo text only | Allowed. Not translation content. |

Catalog statuses: `link_only` (default) and `approved`. `approved` requires a license or written permission recorded below, with date and conditions.

## Attribution pattern

Every entry shows the title, "Source: VyasaOnline" with a link to the original URL, and the translator named only as documented (BM Ramesh per the GitHub About text). Do not imply an official VyasaOnline app or endorsement.

## Technical limitations

- External pages cannot be resumed to an exact scroll position; do not promise it.
- Link-only entries give navigation and "last opened" tracking at most, not paragraph restore.
- Source pages may change; no import should rely on their HTML structure.

## Open questions for the owner

See the request below. Record the reply, date, and conditions in this file before changing any entry to `approved`.

## Permission request (draft)

> Namaste. I am building a small, personal, non-commercial Kannada reader app (a mobile-friendly website that can be installed on a phone). It currently only links to your stories and Parvas on vyasaonline.com. I would like your permission to (a) show selected Kannada translations inside the app on my server, (b) reformat the text for comfortable reading, (c) allow browser offline caching, and (d) retrieve the text from your site or repository in a small, one-time, rate-limited way. Each item would carry your name, the original link, and any attribution wording you specify, and I would remove anything on request. Could you tell me whether this is allowed, which items or licence terms apply, and the attribution you prefer? Until I hear from you, the app will only link to your site.

## Permission record

None received. Date: n/a. Conditions: n/a.
