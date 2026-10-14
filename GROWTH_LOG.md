# Stone & Rose Growth Log

## Baseline (needs Tone's numbers; everything below is blank until he gives them)
- Leads per month and where they come from:
- Consultations booked per month:
- Projects closed per month:
- Average job value and margin:
- Current capacity (projects at once):
- Service cities (confirm the default list on the new site):
- Do you build, or design only:
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

## Experiments
(none yet)

## Open questions for Tone (batched, with recommendation)
1. Confirm the service cities. Recommendation: keep only cities you actually work in; add each one only when you have a local project to show.
2. Confirm the domain is stoneandrosellc.com.
3. Are you licensed, and what is the ROC number? Recommendation: show it in the footer and Google profile.
4. Do you build, or design only? Recommendation: say so in the hero sub and the FAQ.
5. Partner terms. Recommendation: per-project design fee, credited if the client also hires you to build.
6. Send the numbers for the baseline above.
7. Approve merging `claude/desert-modernist-site` to `main` after you review the preview.
