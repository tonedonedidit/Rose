# Stone & Rose Growth Plan

Goal: real customers finding us. That means homeowners searching Google, Maps and AI assistants, plus a steady stream of jobs from partner contractors.

Starting point (checked 2026-10-15): a web search for "Stone & Rose Landscaping" Arizona returns nothing about the business. To Google and to ChatGPT, the business does not exist yet. Everything below fixes that, in order of impact.

---

## Week 1: get on the map (highest impact)

### 1. Domain and hosting
- Buy a domain. Short and matching the name is best (e.g. stoneandroseaz.com or stoneandroselandscaping.com; check availability).
- Host the site free on **Cloudflare Pages**, **Netlify** or **GitHub Pages**. Upload this repo; `index.html` is the homepage.
- Run `./set-domain.sh yourdomain.com` to fill in the domain everywhere (canonical tags, sitemap, schema, llms.txt).
- Set up a domain email (e.g. hello@yourdomain.com) through Google Workspace. It looks more established than Gmail to contractors and HOAs.

### 2. Google Business Profile (the single biggest lever)
Most local searches ("landscape design near me", "backyard design Gilbert") are answered from the Map pack and from Business Profiles, and AI answers lean on them too.
- Create it at business.google.com as a **service-area business** (hide the home address).
- Primary category: **Landscape designer**. Secondary: Landscape architect (only if licensed as one; otherwise skip), Landscaper, Garden designer.
- Service area: list the real cities you serve (for example Mesa, Gilbert, Chandler, Scottsdale, Queen Creek, Phoenix). Only cities you will actually take work in.
- Services: add every service from the website by name, including "HOA submittal packages" and "3D landscape renderings".
- Description (750 chars max), in plain language:
  > Stone & Rose is a landscape design studio in the Phoenix metro area. We design backyards, pools, outdoor kitchens and front yards in photorealistic 3D, so you see the finished yard before anything is built. Every design includes a materials and plant list, measured plans, and an HOA submittal package if your community needs one. We also produce renders, spec sheets and build plans for Arizona landscape and pool contractors. Call or text (480) 973-5166.
- Photos: upload 15+ renders (label them "3D design") and, as soon as any project is built, real photos of the finished yard. Add new photos every week or two.
- Posts: one a week. A render with a two-line caption about what was designed and where.
- Q&A: post and answer the FAQ questions from the website yourself.

### 3. Reviews
- Text every past client the review link from the Business Profile. Ask in person first, send the link the same day.
- Reply to every review within a couple of days.
- Never buy, fake or filter reviews. Google removes them and can suspend the profile.
- Target: 10 real reviews in the first 60 days. This is the number that moves Map rankings.

### 4. Search Console and Bing
- Add the site to **Google Search Console** and submit `sitemap.xml`.
- Add it to **Bing Webmaster Tools** (import from Search Console). Bing feeds ChatGPT search and Copilot.

---

## Weeks 2-4: be everywhere customers and AI look

### Directory listings
Name, phone and website must be **identical** everywhere: `Stone & Rose Landscaping`, `(480) 973-5166`.

| Site | Why |
|---|---|
| Houzz | Where people hiring designers look. Upload the renders as projects. |
| Yelp | Feeds Apple Maps and Siri. |
| Apple Business Connect | iPhone Maps listing. |
| Bing Places | Bing and Copilot. Can import from Google. |
| Nextdoor business page | Neighbors recommending neighbors, very strong for local services. |
| Facebook business page | Reviews, local groups, Marketplace services. |
| BBB | Trust signal for higher-ticket jobs. |
| Angi / HomeAdvisor / Thumbtack | Optional, paid leads. Try one and track cost per job. |

### Instagram (@stoneandrose)
You already make the best content in the business: 3D walkthroughs.
- Post walkthrough videos as Reels. Day-to-night transitions and "design vs. built" comparisons do well.
- Caption with the city and what was designed: "Gilbert backyard: pool, ramada and outdoor kitchen, designed in 3D."
- Before posting a walkthrough, **crop out phone status bars and street addresses**. The old site had screenshots showing "555 S Cholla St"; never publish a client's address.
- Link in bio: the website.

---

## Ongoing: the contractor partner engine

See `contractor-outreach.md`. This is the recurring revenue line: contractors who sell and build but can't produce renders, HOA submittals or measured plans.

Partner deal in one line: they send us design work, we send them homeowners who need a builder.

---

## Monthly: check if AI and Google can find you

Ask these questions in Google, ChatGPT and Perplexity once a month and note whether Stone & Rose shows up, who shows up instead, and which websites the answer cites:

1. best landscape designer in [your city] AZ
2. 3D backyard design Phoenix
3. who does HOA landscape submittals in [city]
4. backyard design with 3D renderings near Gilbert AZ
5. landscape design for pool builders Arizona
6. Stone & Rose Landscaping reviews
7. outdoor kitchen design Scottsdale
8. desert landscape design front yard Mesa

The sites the answers cite are where to get listed next.

---

## Website next steps (once the basics above are live)

- **Real photos.** Every built project: a photo of the finished yard next to its render. This is the strongest proof possible.
- **One page per core service** (Backyard Design, Pools, Outdoor Kitchens, HOA Submittals) with a real project on each. Only when there's a real project to show; thin pages hurt.
- **City pages** only for cities with real local projects to show.
- **Review excerpts** on the homepage once real reviews exist (first name + city).
- **Analytics:** add Cloudflare Web Analytics or Google Analytics to see which pages bring inquiries.
