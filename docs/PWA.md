# PWA — Install and Troubleshooting (Phase 05; not run / not verified)

## What is cached

- App shell only: `/offline`, `static/style.css`, `static/reader.js`, `static/resume.js`, the manifest, and the icon (cache `vyasa-shell-v1` in `static/sw.js`).
- Story pages, catalog pages, and any `data/content` text are **never** cached by the service worker. Link-only entries and VyasaOnline pages or PDFs are never fetched, cached, or proxied. Cross-origin requests are ignored.
- Offline, a page navigation shows `/offline` ("You are offline"). Saved position and bookmarks stay in localStorage but cannot open stories without a connection.
- If a content-caching permission is later recorded in `docs/CONTENT_ACCESS_DECISION.md`, caching can be revisited in a separate phase.

## Requirements

- Chrome requires **HTTPS** for service workers and install. `http://localhost` and `http://127.0.0.1` also work for development.
- A public plain-HTTP EC2 IP does **not** give a standard installable PWA. Use an HTTPS hostname (Phase 06).
- The service worker is served at `/sw.js` (scope `/`) with `Cache-Control: no-cache`. Behind Nginx, proxy `/sw.js` and `/static/` to Gunicorn without adding long cache headers to `/sw.js`, and serve the app at the site root (not a sub-path), since `scope` and `start_url` are `/`.

## Install on Android Chrome

1. Open the HTTPS address in Chrome and wait for the page to load (reload once so the service worker takes control).
2. Menu (three dots) > **Install app** (or **Add to Home screen** > **Install**).
3. Open Vyasa Reader from the home screen icon; it should open without the address bar.

## Updates

When `sw.js` changes (bump `CACHE` in `static/sw.js` whenever shell files change), the new worker waits. The app shows "A new version is available" with a **Reload** button; the page reloads once the new worker is active.

## Remove, reinstall, troubleshoot

1. Remove: long-press the app icon > **Uninstall** (or Chrome menu > Settings > Apps).
2. Clear data: Chrome > Settings > Site settings > All sites > this site > **Clear & reset**. This also deletes saved position and bookmarks.
3. Reinstall by repeating the install steps.
4. No install option: confirm the address is HTTPS (or localhost) and that `/static/manifest.webmanifest` and `/sw.js` load. On desktop Chrome, check DevTools > Application > Manifest / Service Workers.
5. Stale files: DevTools > Application > Service Workers > Unregister, then reload.

## Icon note

The icon is a self-made SVG (`static/icons/icon.svg`, referenced with `sizes: any`). PNG icons at 192x192 and 512x512 could not be generated without running commands. Add them and list them in the manifest if a Chrome version or launcher requires PNG.
