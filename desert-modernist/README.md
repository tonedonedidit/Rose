# Stone & Rose site (Desert Modernist)

Static site. Open `index.html` or serve the folder. Pages: `/` and `/contractors/`.

## Before launch (checklist)
- [ ] Confirm the service-area cities (home page, FAQ, JSON-LD `areaServed`, `llms.txt`).
- [ ] Confirm the domain `stoneandrosellc.com` (canonical tags, `og:url`, `sitemap.xml`, `robots.txt`, JSON-LD). Search and replace if different.
- [ ] Deploy the folder as the site root so `/api/lead` resolves (Vercel project root = this folder).
- [ ] Set up Resend (below). Until then the forms use the Formspree fallback.
- [ ] Add the ROC license number, years in business and real reviews when verified.
- [ ] Submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools.
- [ ] Create or update the Google Business Profile with the same name, phone, email, services and service area.
- [ ] Place a real test inquiry on both forms and confirm both emails arrive (owner alert and auto-reply).

## Resend setup (email delivery for the forms)
1. Create a Resend account and add the domain `stoneandrosellc.com`. Add the DNS records Resend shows (SPF, DKIM). Wait for "Verified".
2. Create an API key (sending access).
3. In the host's environment variables (Vercel: Project, Settings, Environment Variables) set:
   - `RESEND_API_KEY` = the key
   - `LEAD_FROM_EMAIL` = `Stone & Rose <leads@stoneandrosellc.com>` (any address on the verified domain)
   - `LEAD_TO_EMAIL` = `tony@stoneandrosellc.com` (default if unset)
4. Deploy. The forms post to `/api/lead`. If the function is missing or returns a server error, the page posts to Formspree instead.
5. Never put the API key in any file in this repo.

`api/lead.js` validates input, drops bot submissions (hidden `website` field), escapes everything in the email, sends the lead to the owner with the lead's address as reply-to, then sends the lead an automatic reply. Test it with `node api/lead.test.js` (uses a mock, sends nothing).

The old Formspree form still delivers to whichever inbox owns it. Change that notification address in the Formspree dashboard to tony@stoneandrosellc.com.

## Files
`css/site.css`, `js/site.js` shared by both pages. `assets/` renders and logo. `icons/` favicons. `og.png` share image. `robots.txt`, `sitemap.xml`, `llms.txt` for crawlers and AI assistants.
