# Default in-app Kannada chapter reading

**Status:** Implemented as source on `fix/first-story-review-gate`; not run or device-verified. This workflow is for the expressly permitted **personal, non-commercial** reading app. It is not a license to redistribute translations to a public audience.

## Reader flow — no mode switch

1. Open the app home page at `http://127.0.0.1:5000/`.
2. Choose **Stories** or **Parvas**. These go directly to the VyasaOnline-based in-app story list or the Maha Parva list. Selecting a Parva opens its chapter list.
3. Select one story or chapter. Flask retrieves **that one allowed VyasaOnline HTML page** (unless already cached), extracts text, and displays it in the reader without navigating to VyasaOnline.
4. A successfully fetched chapter is stored privately in `data/runtime/chapters/v-*.json` on the Flask/EC2 server. Later visits use that saved copy. No manual `data/catalog.json` edits are needed.
5. Use **View original on VyasaOnline** in the reader **only when you intentionally want to visit the source**. The source-list page also has an explicit original-index link. Fetch failures, PDF-only sources and unsupported layouts show an in-app notice, never an automatic offsite redirect.
6. Reader controls, bookmarks and auto-resume work for displayed chapters. Browser `localStorage` stores reading progress; the server, not the phone, stores text. Service worker still caches **app shell only**: chapter reading while fully offline is not implemented.

Each fetched chapter is marked `auto_unreviewed` and visibly identified as an unreviewed preview. The catalog is never silently marked `approved`; a separately reviewed private JSON still takes priority. Source layouts can change, so not every chapter is guaranteed to parse correctly.

## Run locally — Windows PowerShell

From a clean checkout of the feature branch, using Python 3.10+:

```powershell
git switch fix/first-story-review-gate
git pull --ff-only origin fix/first-story-review-gate
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install "Flask>=3,<4"
.\.venv\Scripts\python.exe app.py
```

No `VYASA_ON_DEMAND` flag, password or private content ZIP is required for default local browsing. Open `http://127.0.0.1:5000/`. The Flask development server binds to `127.0.0.1`: it is for local testing, not production.

### Optional private HTTP Basic password

By default, the app does **not** prompt for a password. To protect your own HTTPS server, set **both** environment variables before starting:

```powershell
$env:VYASA_PRIVATE_USER = "reader"
$env:VYASA_PRIVATE_PASSWORD = "SET_YOUR_OWN_LONG_SECRET"
.\.venv\Scripts\python.exe app.py
```

If both are unset, no login prompt. If only one is configured, access fails closed (503). When enabled, use HTTPS before remote access; Basic credentials are not encrypted on plain HTTP. Do not put passwords into Git. To remove the local password prompt, unset the variables in the same terminal session and restart the app. Do not expose an anonymous translated-text service publicly: the known author permission was for the described **personal**, non-commercial app; obtain broader permission and implement appropriate access/abuse controls before public publishing.

## Verification checklist — not executed

| Test | Action | Expected |
| --- | --- | --- |
| Home | Open `/` without any VYASA env variables | Home works; no password prompt |
| Stories | Click Stories or Browse Kannada stories | Story list appears within Vyasa Reader |
| Parvas | Click Parvas then Adi Parva | In-app list of chapters, no website redirect |
| Story | Click Aruni Uddalaka or Upamanyu | Kannada text in app if source HTML is compatible |
| Original | Click View original on VyasaOnline | Original website opens only by this action |
| Cache | Reopen the same story | Text loaded from `data/runtime/`, no new request |
| Controls | Adjust font/theme, bookmark paragraph, reopen | Browser preferences/bookmark/resume work |
| Unreviewed | Open auto-fetched story | Source attribution and unreviewed notice visible |
| Unsupported | Open a PDF-only or malformed page | Safe in-app unavailable message and original link |
| Fetch quota | Exceed 20 first-time source fetches/hour | Further first-time fetches blocked; cached pages still open |
| Optional password | Set both private credential variables | Browser Basic login prompt and HTTPS needed remotely |

If a source index fails, inspect the original-index link, update local feature branch, and retry. Earlier failed zero-link indexes were not cached. Do not delete the entire `data/runtime/` folder or reviewed `data/content/` files casually: bookmarked paragraph anchors can change if chapters are re-fetched.

## Limits and safeguards

- HTTPS allowlist: `vyasaonline.com` and `www.vyasaonline.com`; redirects and URL extensions for PDFs/archives/images blocked. Plain text is escaped in Jinja; no remote HTML/script execution.
- Only one selected index or chapter page is fetched at a time. No background bulk crawler, automatic per-chapter refresh, or all-chapter pre-download.
- Fetch quota is 20 **uncached** outbound requests/hour per single-worker app, persisted in `data/runtime/fetch_times.json`. Multiple production workers need stronger shared rate limiting and access controls. Initial index requests also count.
- Cached translations and index metadata are Git-ignored under `data/runtime/`; do not force-commit them or the separately approved private Aruni overlay.
- A story whose source HTML cannot be parsed is *not* promised to work; original website remains available on explicit request.
- This branch changes reader defaults and navigation only. Flask runtime, actual chapter extraction, Android PWA, and EC2 security have **not been tested**.
