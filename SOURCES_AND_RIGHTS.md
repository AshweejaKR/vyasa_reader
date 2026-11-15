# Sources, feasibility, and rights checkpoint

**Research checked:** 28 October 2026. Public pages can change. This is technical planning information, not legal advice.

## Verified public entry points

- Website: https://www.vyasaonline.com/
- Kannada Mahabharata stories: https://www.vyasaonline.com/stories-in-mahabharata-kannada/ (index listed **59 stories** in the checked page)
- Parvas/translations: https://www.vyasaonline.com/translations10/ (18 Maha Parvas plus Harivamsha listing)
- Chapter-wise translation index: https://www.vyasaonline.com/chapter-wise-translation-of-mahabharata/
- Example original story: https://www.vyasaonline.com/2018/10/27/%E0%B2%86%E0%B2%B0%E0%B3%81%E0%B2%A3%E0%B2%BF-%E0%B2%89%E0%B2%A6%E0%B3%8D%E0%B2%A7%E0%B2%BE%E0%B2%B2%E0%B2%95/mahabharata/
- Translator's GitHub repository: https://github.com/vyasaonline/mahAbhArata
- GitHub-hosted reader: https://vyasaonline.github.io/mahAbhArata/
- GitHub `content` branch (reference): https://github.com/vyasaonline/mahAbhArata/tree/content
- Relevant Adi Parva, Paushya Parva, Chapter 3 (reference): https://github.com/vyasaonline/mahAbhArata/blob/content/01_Adiparva/003_paushya-parva.md
- Owner contact: https://www.vyasaonline.com/contact/

The website says the Kannada translation of the 18 Maha Parvas was completed in 2022. The public repository describes the translator as **BM Ramesh**. The checked repository's root file list did not expose an obvious `LICENSE` file; this is **not proof** no license/permission exists elsewhere.

## Written permission update (2026-11-10)

Written permission: BM Ramesh replied on 2026-11-10 to the 2026-11-04 personal, non-commercial Vyasa Reader request, saying “Please go ahead and use the content on my website. No issues.” The request expressly described hosting selected Kannada translation text on personal AWS, readability-only reformatting, limited personal offline browser caching, and one-time rate-limited retrieval from website or GitHub. Reply also asks whether revised translations (Adi Parva in progress), additional recension portions, and Shastra Samgraha can be reflected when ready. User acknowledged on 2026-11-11. Keep the original correspondence privately; do not commit the PDF or email addresses to this public repository.

The owner's express reply permits the described personal reading app use of **website content**. Preserve attribution and original links. Do not assume permission covers third-party media, commercial redistribution, or all GitHub content. See `docs/CONTENT_ACCESS_DECISION.md` for boundaries and import controls.

## First selected-story sources (checked 2026-11-15)

- Primary text for `aruni-uddalaka`: the original VyasaOnline story linked above. It is a prose retelling placed in Adi Parva / Paushya Parva / Chapter 3.
- Secondary cross-check only: the GitHub `content` branch contains a much larger Markdown chapter with Sanskrit verse identifiers and Kannada translation; the online reader uses that body of material. They must not be assumed to have identical wording or revision dates.
- Do not import GitHub Markdown or verse identifiers into the short website story by default. The author's personal-app permission explicitly refers to website content. Preserve the original story URL and B.M. Ramesh attribution; do not commit the private translation text to the public project.
- The site-reader and GitHub links are navigation/reference resources, **not** blanket redistribution permission.

## What remains unverified

1. Separate rights for **third-party illustrations, pictures, PDFs**, commercial reuse, and any uses beyond the described personal app.
2. Whether the WordPress REST API is publicly enabled, what endpoints are intended for reuse, and whether cross-origin access is allowed. The endpoints were not validated during this planning pass.
3. Whether the source allows embedding in iframes or third-party proxying. Do not assume it does.
4. Whether any content-specific license applies in the linked GitHub repo or author correspondence.
5. Content pagination and stable IDs across all chapters. A few publicly visible source pages do not prove all content can be programmatically imported.

## Safe MVP recommendation

- Start with your own catalog containing source URLs/titles, and self-written demo reading content.
- Written permission for the described website-text use is now recorded. Import only selected website text after attribution/source tracking; do not assume third-party media rights.
- Record author, original URL, license text/permission date, any restrictions (public vs private hosting, offline caching, attribution), and allowed source format.
- On refusal or uncertainty, keep an external-link-only mode. It cannot deliver exact resume on third-party pages.
- A public repository and 'free download' are not blanket republication permissions.

## Permission request outline

Ask the translator/site owner whether a **personal, non-commercial, attribution-rich mobile PWA** may show the Kannada translations on your EC2 site. Specifically request permission for (a) hosting text, (b) converting text for a clean reader, (c) browser offline caching, and (d) automated retrieval/import if any. Offer direct links back to each original story and honor any conditions or denial.

## Notes for Phase 00 Claude Code

Treat this document as a starting bibliography. Recheck current pages without broad crawling. Document evidence and precise unknowns in `docs/CONTENT_ACCESS_DECISION.md`. Never infer a license from public access or GitHub visibility.
