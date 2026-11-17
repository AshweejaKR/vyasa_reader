# PWA — Install and Troubleshooting (Phase 05; not run / not verified)

## What is cached

- App shell only: `/offline`, `static/style.css`, `static/reader.js`, `static/resume.js`, the manifest, and the SVG/192px/512px PNG icons (cache `vyasa-shell-v3` in `static/sw.js`).
- Story pages, catalog pages, and any `data/content` text are **never** cached by the service worker. The optional, separately enabled Flask on-demand feature may fetch one permitted VyasaOnline HTML page into its **private server** cache, but the service worker never caches remote or translated pages, PDFs, or external links. Cross-origin service worker requests are ignored.
- Offline, a page navigation shows `/offline` ("You are offline"). Saved position and bookmarks stay in localStorage but cannot open stories without a connection.
- Written permission for limited offline caching in the described personal app was received 2026-11-10. **No text cache is implemented yet.** Consider bounded, versioned same-origin caching of reviewed approved items in a separate task; support cache invalidation/removal and do not cache third-party images or PDFs.

## Requirements

- Chrome requires **HTTPS** for service workers and install. `http://localhost` and `http://127.0.0.1` also work for development.
- A public plain-HTTP EC2 IP does **not** give a standard installable PWA. Use an HTTPS hostname (Phase 06).
- The service worker is served at `/sw.js` (scope `/`) with `Cache-Control: no-cache`. Behind Nginx, proxy `/sw.js` and `/static/` to Gunicorn without adding long cache headers to `/sw.js`, and serve the app at the site root (not a sub-path), since `scope` and `start_url` are `/`.

## Install on Android Chrome

1. Open the HTTPS address in Chrome and wait for the page to load (reload once so the service worker takes control).
2. Menu (three dots) > **Install app** (or **Add to Home screen** > **Install**).
3. Open Vyasa Reader from the home screen icon; it should open without the address bar. The manifest start URL `/?launch=pwa` signals an app-icon launch for auto-resume and the app clears the marker before normal navigation. Android behavior remains unverified.

## Updates

When `sw.js` changes (bump `CACHE` in `static/sw.js` whenever shell files change), the new worker waits. The app shows "A new version is available" with a **Reload** button; the page reloads once the new worker is active.

## Remove, reinstall, troubleshoot

1. Remove: long-press the app icon > **Uninstall** (or Chrome menu > Settings > Apps).
2. Clear data: Chrome > Settings > Site settings > All sites > this site > **Clear & reset**. This also deletes saved position and bookmarks.
3. Reinstall by repeating the install steps.
4. No install option: confirm the address is HTTPS (or localhost) and that `/static/manifest.webmanifest` and `/sw.js` load. On desktop Chrome, check DevTools > Application > Manifest / Service Workers.
5. Stale files: DevTools > Application > Service Workers > Unregister, then reload.

## Icon note

The project includes an original SVG book icon plus matching 192x192 and 512x512 PNG icons (`static/icons/`). The manifest lists all three; PNG and Android launcher rendering are not yet device-verified.
