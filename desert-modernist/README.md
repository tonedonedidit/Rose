# Stone & Rose site (Desert Modernist)

Static site. Open `index.html` or serve the folder. Pages: `/` and `/contractors/`.

## Before launch (checklist)
- [ ] Confirm the service-area cities (home page, FAQ, JSON-LD `areaServed`, `llms.txt`).
- [ ] Confirm the domain `stoneandrosellc.com` (canonical tags, `og:url`, `sitemap.xml`, `robots.txt`, JSON-LD). Search and replace if different.
- [ ] Create the new Netlify site (below) and test on its `*.netlify.app` address.
- [ ] Set up Resend (below). Until then the forms use the Formspree fallback.
- [ ] Add the ROC license number, years in business and real reviews when verified.
- [ ] Submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools.
- [ ] Create or update the Google Business Profile with the same name, phone, email, services and service area.
- [ ] Place a real test inquiry on both forms and confirm both emails arrive (owner alert and auto-reply).

## Netlify: a second site, so the old one stays up
The old site keeps running exactly as it is. The new one is a separate Netlify site built from the same repo:
1. Netlify, Add new site, Import an existing project, GitHub, repo `tonedonedidit/Rose`.
2. Branch to deploy: `claude/desert-modernist-site` (use `main` after it is merged).
3. Base directory: `desert-modernist`. Leave build command empty. Publish directory: `.` (already set in `netlify.toml`).
4. Deploy. Test everything on the new `*.netlify.app` address.
5. At launch only: Netlify, Domain management, move `stoneandrosellc.com` to the new site (or add it there and remove it from the old one). Netlify issues the HTTPS certificate. Keep the old site until the new one is confirmed.

`netlify.toml` (inside `desert-modernist/`) routes `/api/lead` to the function and adds basic security headers. Netlify only reads it for the new site, so the old site is unaffected.

## Resend setup (email delivery for the forms)
1. Create a Resend account and add the domain `stoneandrosellc.com`. Add the DNS records Resend shows (SPF, DKIM). Wait for "Verified".
2. Create an API key (sending access).
3. In Netlify, Site configuration, Environment variables, add (mark the key as secret and make it available to Functions):
   - `RESEND_API_KEY` = the key
   - `LEAD_FROM_EMAIL` = `Stone & Rose <leads@stoneandrosellc.com>` (any address on the verified domain)
   - `LEAD_TO_EMAIL` = `tony@stoneandrosellc.com` (default if unset)
4. Trigger a new deploy so the function picks up the variables. The forms post to `/api/lead`. If the function is not configured or returns a server error, the page posts to Formspree instead, so no lead is lost.
5. Never put the API key in any file in this repo.

`netlify/functions/lead.js` validates input, drops bot submissions (hidden `website` field), escapes everything in the email, sends the lead to the owner with the lead's address as reply-to, then sends the lead an automatic reply. Test it with `node netlify/functions/lead.test.js` (uses a mock, sends nothing).

The old Formspree form still delivers to whichever inbox owns it. Change that notification address in the Formspree dashboard to tony@stoneandrosellc.com.

## Files
`netlify.toml` Netlify settings. `netlify/functions/lead.js` the Resend handler. `css/site.css`, `js/site.js` shared by both pages. `assets/` renders and logo. `icons/` favicons. `og.png` share image. `robots.txt`, `sitemap.xml`, `llms.txt` for crawlers and AI assistants.
