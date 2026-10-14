# Stone & Rose Growth Log

## Baseline (needs Tone's numbers; everything below is blank until he gives them)
- Leads per month and where they come from:
- Consultations booked per month:
- Projects closed per month:
- Average job value and margin:
- Current capacity (projects at once):
- Service cities (confirm the default list on the new site):
- Do you build, or design only: DESIGN ONLY (confirmed 2026-10-14). Revenue is design fees.
- Licensed? ROC number:
- Real reviews available (count, where):
- Google Business Profile exists? Search Console connected?

## Decisions
- 2026-10-14: Built the new site in `desert-modernist/` as a separate copy. Old site untouched.
- 2026-10-14: Replaced email with tony@stoneandrosellc.com and phone with (480) 650-8957 everywhere.
- 2026-10-14: Deliverables: renders and walk-through video included, 360° video optional (site, schema, FAQ, forms, llms.txt all say so).
- 2026-10-14: Added `/contractors/` partner page with its own inquiry form. Terms left open (see `docs/partner-models-and-gaps.md`).
- 2026-10-14: Forms post to `/api/lead` (Resend) and fall back to Formspree if that endpoint is missing, so no lead is lost.
- 2026-10-14: Rewrote the hero H1 to name the service and place. Old headline kept only as the brand tagline.
- 2026-10-14: Dropped duplicate portfolio images and cropped phone screenshots (removed a street address).

- 2026-10-14: Tone confirmed design only (no construction). Removed "we build", "Built to Last", "Based & Built" and the OG image wording; added a "Do you build the project?" FAQ; added the partner pitch "we design and do not build, so we are not competing with you."

- 2026-10-14: Tone confirmed hosting is Netlify. Converted the Resend handler to a Netlify Function (`netlify/functions/lead.js`), added `desert-modernist/netlify.toml`, and documented a separate Netlify site (base directory `desert-modernist`) so the old site stays live.

- 2026-10-14: Tone confirmed 100+ completed renders. Replaced the "50+ Designs" stat with "100+ Completed Renders" (home stat, schema, llms.txt, contractor page).
- 2026-10-14: Pricing decision: homeowners get public "starting at" prices (needs Tone's numbers); contractors stay back end (rate sheet by email). Reasoning in `docs/pricing-decision.md`. Contractor page now says partner pricing is not published.

## Experiments
(none yet)

## Open questions for Tone (batched, with recommendation)
0. Pricing numbers needed to publish: starting price for 3D Render Only, for a full design (renders plus walk-through video), and for the 360° video add-on. Plus a partner rate sheet to email contractors (not published). See `docs/pricing-decision.md`.
1. Confirm the service cities. Recommendation: keep only cities you actually work in; add each one only when you have a local project to show.
2. Confirm the domain is stoneandrosellc.com.
3. Are you licensed, and what is the ROC number? Recommendation: show it in the footer and Google profile.
4. (Answered: design only.) Site now says so in About, Process, FAQ and the partner page.
5. Partner terms. Recommendation: a per-project design fee, tiered by project size, paid by the contractor or passed to their client in the quote. Since you do not build, there is no build to credit it against.
6. Send the numbers for the baseline above.
7. Create the second Netlify site from branch `claude/desert-modernist-site` (steps in `desert-modernist/README.md`), review it on the netlify.app address, then tell me when to move the domain. No merge to `main` needed to test.
