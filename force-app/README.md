# Force Receiving (v7)

The single file `index.html` runs in three places:
- **claude.ai preview:** https://claude.ai/artifact/JanWGBN9F242LUGkKdAFtN. Data lives in the artifact's db.
- **Company site (Netlify):** not deployed yet. When `/api/ping` answers, the page switches to the server store: sign-in is checked on the server, and sync polls every 2.5 s.
- **Opened as a file:** saves on that device only (used by the tests).

Sign-ins: `fcadmin` (office) and `fcwarehouse` (warehouse). The preview checks a SHA-256 hash in the page, which is a gate, not security. The Netlify version checks passwords on the server from environment variables.

Test: `scratchpad/v7/day.js` replays the hypothetical day (boards, hardware with missing strap, cardboard delayed through a re-import, doors with a damaged door reordered and auto-archived, saw pulls). Result: 66/66 passing, light and dark, 390 px and 1366 px, zero console errors.
