# Stone & Rose Landscaping: project context

## The business
- Arizona landscape design studio, Phoenix metro (480 area code). Owner: Tone.
- Designs backyards, pools, outdoor kitchens, front yards, lighting and planting in photorealistic 3D.
- Deliverables: 3D renders, HOA submittal packages, spec sheets, measured build plans.
- Two audiences:
  1. Homeowners: design, then build with a partner contractor or their own.
  2. Contractors who can't produce renders/submittals/plans: recurring partnership, referrals both ways, client stays the contractor's.
- Contact: (480) 973-5166 · Stoneandrose@gmail.com · instagram.com/stoneandrose
- Tagline: "Your Outdoor Life, Elevated."
- Goal: real customers finding the business (SEO, local search, AI search, outreach).

## The site
- Static HTML: `index.html` (homeowners), `contractors.html` (contractor partners), shared `styles.css` and `site.js`. No build step.
- Images in `images/` as WebP (full + `-800` mobile versions). Portfolio images are 3D renders and are labeled as such.
- Forms post to Formspree `https://formspree.io/f/mlgpprov` with a hidden `audience` field (Homeowner / Contractor).
- Domain placeholder `www.YOURDOMAIN.com` until the real domain is set: run `./set-domain.sh domain.com`.
- SEO files: `robots.txt`, `sitemap.xml` (update `lastmod` on changes), `llms.txt`, JSON-LD in each page head.

## Rules
- Never send emails, DMs, posts or publish anything without Tone's explicit yes.
- Never invent proof: no fake reviews, numbers, licenses, cities or projects. Unknown facts are flagged for Tone, not guessed.
- Never publish client addresses or identifiable details (phone status bars, street names in screenshots).
- Client copy: no em dashes, no AI filler words (see human-copy skill). Plain, specific, local.
- Test with a headless browser at phone and desktop widths before calling site work done.

## Open questions for Tone
- Real domain name?
- Exact cities served (for Google Business Profile and site)?
- Is "50+ designs completed" accurate? Any built projects with real photos?
- Does Stone & Rose build, or design only and hand off to contractors? Any AZ ROC license?
- Contractor terms: priority scheduling for partners, ongoing rates, turnaround time, revisions included?
- Postal address for outreach emails (required by CAN-SPAM).
