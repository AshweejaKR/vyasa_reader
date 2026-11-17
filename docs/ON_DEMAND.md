# On-demand Kannada chapters — private mode

**Status:** Source written on branch `fix/first-story-review-gate`; **runtime, Android and EC2 behavior not tested**. This feature is opt-in and **off by default**. Use it only for the translator-authorized personal, non-commercial reading app.

## What happens

1. Open **Browse Kannada stories** or **Browse Maha Parvas and chapters** in the app.
2. Flask downloads **only the selected VyasaOnline HTML index**. It stores a small index of titles/URLs privately under `data/runtime/`, not any chapter text.
3. Select one story or chapter. Flask fetches **only that page**, extracts WordPress post paragraphs as plain text, checks source host/size/Kannada structure, and saves `data/runtime/chapters/v-*.json`. Subsequent opens reuse the local server copy, even if the source website is down.
4. The reader shows an **unreviewed auto-fetched** notice, VyasaOnline/B.M. Ramesh credit, Original link, and normal text controls/bookmarks/resume. Automatic previews do **not** set the public catalog to `approved`, and they are **not a substitute** for manually approved content.
5. Click the existing **ಆರುಣಿ ಉದ್ಧಾಲಕ** catalog entry while private mode is on: it can also load automatically without installing the separate approved ZIP. If a private approved version is already installed and its catalog entry is `approved`, the reviewed local version remains preferred.

Only website-hosted HTML source pages are accepted. The site's PDF and image downloads, GitHub Markdown, third-party pages, scripts, comments, and broad bulk imports are excluded. Some chapter layouts may fail or lose specialized verse formatting: the source link remains available. **Not all chapters are guaranteed compatible.**

## Windows local setup

Use Python 3.10+ and switch to the named feature branch. Inside project root, with the existing virtual environment:

```powershell
.\.venv\Scripts\python.exe -m pip install "Flask>=3,<4"
$env:VYASA_ON_DEMAND = "1"
$env:VYASA_PRIVATE_USER = "reader"
$env:VYASA_PRIVATE_PASSWORD = "CHOOSE_A_LONG_UNIQUE_PASSWORD"
.\.venv\Scripts\python.exe app.py
```

Browser: http://127.0.0.1:5000/. When asked for credentials, supply the username/password above. Replace the sample password before using. Localhost HTTP is acceptable for development; **never use this mode over public HTTP** because HTTP Basic credentials would be exposed. Only enable on a personal server protected by HTTPS and access controls.

Linux/EC2: set the same three environment variables in the **private systemd service environment**, protect its config file, run one Gunicorn worker for this small personal service, and serve behind HTTPS Nginx. No AWS configuration is changed by this branch. **Do not put passwords in public Git, GitHub Actions logs, or source files.** If private credentials are missing while `VYASA_ON_DEMAND=1`, the app fails closed with HTTP 503.

To disable, unset `VYASA_ON_DEMAND` or set it to `0` and restart. Existing public demo and link-only behavior returns. Do not enable this feature on a public anonymous instance.

## Fix for "Index structure unexpected; no chapters saved" (2026-11-17)

The first parser extracted index links only when an `entry-content`/`post-content` container was detected and the anchor was inside `ol > li`. This could return zero links on real WordPress pages. It now reads ordered lists independently of that container (plus list links within the main article), excluding headers/nav/footers/asides. The original Kannada Stories index was separately checked and contains **59 linked stories**; the Translations index links to **18 Maha Parvas plus Harivamsha**, and Adi Parva contains many chapter links. Only page links you click are fetched; no bulk import was added.

To retry: update your local checkout from the **same feature branch**, restart Flask, sign in to private mode, and choose **Browse all Kannada stories** or **Browse Maha Parvas and chapters**. Previous failed zero-link responses were not saved as chapter indexes, so normally nothing must be deleted. If it still fails, identify the exact page (**Stories**, **Maha Parvas**, or a selected Parva) and compare its **Open original index** link to the website; the source layout may have changed. Do not delete cached approved translations or the entire `data/runtime/` folder just to troubleshoot.

## Manual checks (not run)

| Test | Steps | Expected |
| --- | --- | --- |
| Default protection | Start without `VYASA_ON_DEMAND`; open `/read/aruni-uddalaka` | Stays link-only without approved overlay |
| Auth required | Enable mode, open Home in a fresh browser | HTTP Basic login prompt; no content before login |
| Source index | Home > Browse Kannada stories | Titles from Stories index; no story text downloaded yet |
| One story | Choose `ಉಪಮನ್ಯು` | One HTML story fetched; preview notice, original URL, Kannada text |
| Cache | Reload the same story | Same locally saved text; no second website request |
| Existing story | Open `/read/aruni-uddalaka` without private approved ZIP | Redirects to on-demand copy, not link-only |
| Maha Parva | Browse Maha Parvas > Adi Parva > a chapter | One chapter page fetched and displayed if compatible |
| Reader | Bookmark, change font/theme, return to `/?launch=pwa` | Reading position saved in this browser |
| Missing/unusual page | Select a page with unsupported layout or offline first request | Safe unavailable notice plus Original link; no arbitrary HTML rendered |
| Credit/rights | Inspect reader and `data/runtime/` | VyasaOnline/B.M. Ramesh attribution; content never goes to public Git |
| Limit | More than 20 uncached source requests per hour | New fetches blocked, cached pages remain readable |

Manual cache reset: **back up before removing** individual `data/runtime/index-*.json`, `registry.json`, or `chapters/v-*.json`. Deleting cache may break old resume anchors if source text changes. Do not delete the reviewed private `data/content/aruni-uddalaka.json` by mistake. No automatic refresh, unbounded prefetch, or bulk crawl.

## Security, storage, limitations

- Outbound requests are HTTPS, fixed to `vyasaonline.com` / `www.vyasaonline.com`; redirects to other hosts, non-HTML, and large pages fail closed. Only one selected page is fetched per click. Browser receives escaped plain text, **never** remote HTML/scripts.
- Server cache and index metadata are in `data/runtime/` (Git-ignored). No Git commits or cloud uploads of translated chapters. SHA-256 and UTC import time are recorded for each cached chapter.
- Limit: **20 uncached requests per hour per application worker**, with a shared history file. For the personal EC2 deployment use one worker; this lightweight quota is not a multi-worker distributed rate limiter.
- There is no login account system: HTTP Basic protects the entire app while private on-demand mode is enabled. Turn on HTTPS before remote use. Avoid sharing credentials. Do not operate an open public fetch proxy.
- Browser `localStorage` holds reading progress/bookmarks. Cached texts live on the Flask/EC2 server, **not** in phone localStorage. The service worker still caches **app shell only**: offline chapter reading is not available.
- Source might change; existing server cache is not overwritten silently (bookmark IDs stay intact). To refresh, review source revisions and reset a selected cached file deliberately. Personal-app permission does not imply a blanket right to publish GitHub translation files or third-party media.
