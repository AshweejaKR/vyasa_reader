# Vyasa Reader — Local run and verification (first Kannada story)

**Status:** Instructions prepared, **not executed**. This guide applies to the public source on branch `fix/first-story-review-gate` plus the **separate private approved Aruni overlay** delivered in ChatGPT on 2026-11-17. The overlay is **not** in the GitHub repository.

## 1. Clone the feature branch (Windows PowerShell)

From a terminal in the directory where you keep projects:

```powershell
git clone https://github.com/AshweejaKR/vyasa_reader.git
cd vyasa_reader
git switch --track origin/fix/first-story-review-gate
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install "Flask>=3,<4"
```

Use Python 3.10+ (the code uses `Path.is_relative_to`). On Windows, **Gunicorn is not required** to run the Flask development app; it is for Linux deployment. The only app dependency needed for this local check is Flask.

Already have a clone? Ensure the checkout is clean **before** adding private data, fetch branch updates, and switch to `fix/first-story-review-gate`; do not overwrite uncommitted work.

Linux/macOS alternative:

```sh
git clone https://github.com/AshweejaKR/vyasa_reader.git
cd vyasa_reader
git switch --track origin/fix/first-story-review-gate
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## 2. Baseline without private text

In the repository root, start the app:

```powershell
.\.venv\Scripts\python.exe app.py
```

Linux/macOS: `.venv/bin/python app.py`. Open these URLs on the same computer:

| URL | Expected |
| --- | --- |
| http://127.0.0.1:5000/ | Home, Stories, Parvas, Continue Reading |
| http://127.0.0.1:5000/health | `{"status":"ok"}` |
| http://127.0.0.1:5000/read/demo-story | Fictional demo and reading controls |
| http://127.0.0.1:5000/read/aruni-uddalaka | **Link-only** notice and Open Original; no story text |
| http://127.0.0.1:5000/read/unknown | Not-found page (HTTP 404) |

This baseline is **expected**: public GitHub deliberately contains neither the approved Kannada translation nor its private catalog switch.

## 3. Add the *private* approved story

1. Download the **Vyasa_Reader_Aruni_Approved_Private_Overlay.zip** provided separately in ChatGPT. Do not use the older `pending` draft ZIP. Extract it into a separate, private temporary folder first.
2. Confirm the extracted ZIP includes `INSTALL_PRIVATE.md`, `data/content/aruni-uddalaka.json`, and `data/catalog.json`. Read `INSTALL_PRIVATE.md`.
3. Copy its `data/content/aruni-uddalaka.json` into your checkout at `data/content/aruni-uddalaka.json`. This file is Git-ignored. It must contain six blocks (`p0001`–`p0006`) and `review_status: "approved"`.
4. **Only in your private local checkout**, edit the existing `data/catalog.json` entry with id `aruni-uddalaka`: set `"content_status": "approved"` and `"content_path": "aruni-uddalaka.json"`. Leave all other entries unchanged. Alternatively, use the ZIP's complete catalog snapshot **only if** your repository catalog still matches that snapshot.
5. Do **not** commit this private catalog edit or the translation file. The tracked `data/catalog.json` will appear modified in `git status`; this is intentional for private testing only.
6. Restart Flask if needed, and open http://127.0.0.1:5000/read/aruni-uddalaka .

Expected: six Kannada paragraphs, B.M. Ramesh / VyasaOnline credit, Original source link, A−/A+ controls, Dark/Light mode, Bookmark control. If only the external link appears, the catalog entry is still `link_only`. If "This text is not available right now" appears, check the JSON path and **both** approval flags.

**Do not run the importer over this approved JSON**: `scripts/import_selected_story.py` refuses to overwrite existing content. The approved ZIP is already the selected reviewed text.

## 4. Manual acceptance checks

| Check | Action | Expected |
| --- | --- | --- |
| Kannada layout | Open Aruni at ~360 px and desktop width; use A+ until the story scrolls | Six readable paragraphs; no horizontal scrolling |
| Content/source | Compare first and last paragraphs with VyasaOnline; click Original | Correct text and source URL; no comments, menu, or "The other stories" |
| Theme and font | Use A+/A− and Dark/Light, refresh | Settings persist in this browser |
| Bookmark | Scroll, click Bookmark this spot; return Home | Bookmark appears; selecting it returns near saved paragraph |
| Resume | Scroll on Aruni, navigate away, then open `http://127.0.0.1:5000/?launch=pwa` | Should auto-resume Aruni near saved spot (simulates app-icon launch) |
| Manual navigation | From Stories choose Demo or Aruni directly | Explicit choice is not overridden by resume |
| Auto-resume off | Uncheck Auto-resume on Home; revisit `/?launch=pwa` | Home stays visible; Continue Reading still available |
| Fallback: review | Temporarily set private JSON `review_status` to `pending`; refresh | Text unavailable; **never** shown. Restore to `approved` after test |
| Fallback: missing file | Temporarily move the private story JSON elsewhere; refresh | Text unavailable, not a server crash. Restore the file |
| Link-only | Open Stories Index or Parvas Index | Opens external source; no in-app position tracking |
| Service worker | Visit `/sw.js`, DevTools > Application > Service Workers | Registration can be inspected on localhost; **story pages are not offline-cached** |

**Limits:** PWA installation on an actual Android phone and the EC2 deployment require HTTPS and remain **separate, unverified** tests. Reading state uses browser `localStorage` only. A fresh browser profile or cleared site data loses it. A phone cannot visit your PC's `127.0.0.1` address. There is **no general runtime fetch or server cache for every Mahabharata chapter yet**.

## 5. Leave the feature branch clean

After testing, store the private overlay ZIP separately. If `data/catalog.json` was changed **only** for this private trial, restore the public catalog:

```powershell
git status --short
git restore data/catalog.json
git status --short
```

**Warning:** `git restore data/catalog.json` discards *all* local changes to that tracked file. Never use it if you have other catalog edits you want to keep. The ignored private story JSON may remain on disk; verify it is not added to Git. Do not use `git add -f` to force-add the private JSON, and do not commit a public catalog `approved` entry without a matching permitted content deployment.

## 6. Record outcomes

For each acceptance check, record **Pass/Fail**, browser/OS, any failure steps and screenshot locally. Do not mark Android/EC2 as verified until tested on those devices. The final merge of this feature branch remains the owner's decision.
