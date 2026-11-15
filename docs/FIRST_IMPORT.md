# First selected content import — Aruni Uddalaka

Status: **one-story website fetch merged to main; original story source inspected 2026-11-15 (six narrative paragraphs), but importer not run and text not reviewed or deployed**. This does not publish the translation or turn on in-app reading.

## Verified references

- **Primary approved text:** https://www.vyasaonline.com/2018/10/27/%E0%B2%86%E0%B2%B0%E0%B3%81%E0%B2%A3%E0%B2%BF-%E0%B2%89%E0%B2%A6%E0%B3%8D%E0%B2%A7%E0%B2%BE%E0%B2%B2%E0%B2%95/mahabharata/
- **Online chapter reader (reference only):** https://vyasaonline.github.io/mahAbhArata/
- **GitHub source (reference only):** https://github.com/vyasaonline/mahAbhArata/tree/content
- **Relevant chapter:** https://github.com/vyasaonline/mahAbhArata/blob/content/01_Adiparva/003_paushya-parva.md
- Story placement: Adi Parva → Paushya Parva → Chapter 3. The chapter Markdown includes other stories/verses; it is **not** the same as the short website story. Do not combine or silently replace text from different versions.
- Credit: **B.M. Ramesh / VyasaOnline**. Permission dated 2026-11-10 covers the described personal, non-commercial use of **website** text. GitHub visibility or the online reader is not a separate redistribution license. No third-party images or PDFs.
- Source preflight (2026-11-15): six narrative paragraphs precede a distinct “The other stories” index and comment form. The index and comments are not story content. Page inspection alone is not verification that the local importer extracts every paragraph correctly.

## One-story workflow

1. On your machine, run `python scripts/import_selected_story.py --fetch` from the repository root. The script makes **one** HTTPS request to the fixed VyasaOnline story URL, extracts paragraph text from the post body (not navigation/comments/scripts), and writes `data/content/aruni-uddalaka.json` with `review_status: pending`. It does not browse the story index, download other chapters, or update the catalog.
2. If the source layout changes, or you prefer full control, copy only the Kannada story body to a private UTF-8 `.txt` file (separate source paragraphs with blank lines) and run `python scripts/import_selected_story.py private-story.txt` instead. Never import source HTML, comments, or images.
3. Review **every generated paragraph** against the primary website page. Check that the introduction and concluding sentence are present; no "The other stories" list, navigation, comment form, or missing Kannada text. Verify spelling, line breaks, order, and source credit. The original website story is prose: do not invent Sanskrit verse numbers or use GitHub chapter text to fill gaps.
4. Paragraph IDs are initially `p0001`, `p0002`, etc. They support resume/bookmarks, but may shift if a later source revision inserts text. Preserve existing IDs manually on revisions; this importer refuses to overwrite its output. A SHA-256 of the imported text, import date, fetch method, and unknown source revision are recorded.
5. After manual source comparison, set the private JSON `review_status` to `approved` **and only then** change `data/catalog.json` for `aruni-uddalaka` to `content_status: approved` and `content_path: "aruni-uddalaka.json"` on the intended private deployment. The Flask loader now requires `review_status: "approved"` for every item with a nonempty original `source_url`; an imported draft cannot be displayed by accidentally approving its catalog entry. Keep the public catalog `link_only` while the private text is unavailable there.
6. Manually verify Kannada display, credit and original link, bookmarks, auto-resume, missing-content fallback, and Android PWA behavior before treating the item as released. Record the outcome in `docs/PROGRESS.md` and `docs/DEVELOPMENT_LOG.md`.

## Privacy and compatibility

- `data/content/aruni-uddalaka.json` and `private-story.txt` are ignored by Git. **Never commit the imported translation to this public repository by default.**
- In-app reader uses local `data/content/` JSON files; an approved catalog entry without its private file will display "text not available". Keep both files together on the intended private server.
- No runtime fetch by Flask, no periodic polling, no bulk scraping, no automatic publish and no remote upload. Fetch failures require manual handling; no execution/Android/EC2 checks have been run.
