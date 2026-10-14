# Pricing decision: what to show, and to whom

Decided 2026-10-14. No numbers are published until Tone gives them (a price is something customers hold the business to).

## Decision
| Audience | Decision | What the site does |
|---|---|---|
| Homeowners | **Show "starting at" prices** for each design package. Exact quote after the consultation. | Add a Pricing section and an FAQ answer once Tone sends three numbers (below). |
| Contractors | **Keep pricing on the back end.** Send a rate sheet by email after an inquiry. | Already live: the partner page says partner pricing is not published and promises a quote. |

## Why homeowners should see a starting price
- **It filters the right buyers.** Firms that charge for design report that a fee screens out price shoppers who are "probably not serious enough about the project" ([NALP](https://blog.landscapeprofessionals.org/design-build-opting-to-charge-design-fees/)). Because you design only, design fees are your revenue, so a clear price is a feature, not a risk.
- **Design is a product with fixed deliverables** (3D renders, walk-through video, optional 360° video). Fixed deliverables can carry a starting price. Yardzen, the best-known design-only model, publishes flat design fees; its own site cites packages from $495 to $1,495 ([Yardzen](https://www.yardzen.com/faq)).
- **It matches how people search.** "How much does backyard design cost in Arizona" is a common question. A page with no number loses that search to pages that have one.
- **It saves your time.** People who see a starting price and still call are better leads.
- **Judgment call, not data:** Yardzen is a remote, lower-touch service. A studio that includes a walk-through video and local Arizona knowledge can price at or above the top of that range. I found no published conversion data tying price display to close rate, so treat the benefit as likely, not proven. Test it: compare lead quality for 60 days.

Use "starting at", not a fixed price. Show what the price includes. Never show a price for work you have not defined.

## Why contractors should not see numbers
- **Terms vary by partner.** Volume, scope, and whether the contractor pays or passes the fee to their client all change the number.
- **Channel conflict.** A public partner price lets homeowners see the contractor's cost, which makes contractors less willing to resell your design.
- **A rate sheet is a reason to start a conversation.** It captures the contact and lets you tailor terms. The partner page already says so.
- Contractors do see the **structure** (what is included, that the 360° video is an add-on) so they can judge fit before asking.

## Three numbers needed from Tone to publish the homeowner pricing
1. Starting price for **3D Render Only**.
2. Starting price for a **full design** (3D renders plus walk-through video).
3. Starting price for the **360° video add-on**.
Plus, for the back end: a **partner rate sheet** to email contractors.

## Paste-ready homeowner pricing section (add after "What you get with every design")
Fill the three numbers, then I will add it, update the FAQ and schema, and re-run QA.

```html
<section class="pad rule-top" id="pricing">
  <div class="section-head">
    <p class="section-eyebrow">Pricing</p>
    <h2 class="section-heading">What a Stone & Rose design costs</h2>
    <p class="section-text">Prices start at the amounts below. We quote your exact price after the consultation.</p>
  </div>
  <div class="included-grid">
    <div class="deliverable"><h3>3D Render Only</h3><p><strong>Starting at $[NUMBER 1]</strong></p><p>Photorealistic 3D renders of your project.</p></div>
    <div class="deliverable"><h3>Full design</h3><p><strong>Starting at $[NUMBER 2]</strong></p><p>Photorealistic 3D renders and a walk-through video.</p></div>
    <div class="deliverable"><h3>360° video add-on</h3><p><strong>Add $[NUMBER 3]</strong></p><p>Optional. Not included in the standard design.</p></div>
  </div>
</section>
```
FAQ to add: "How much does a Stone & Rose design cost?" with the same starting prices and "We quote your exact price after the consultation."

## How to choose the numbers
- Start from the cost to you: hours per design, software, and render time. Price so a typical design is clearly profitable.
- Benchmark the low end against Yardzen ($495 to $1,495 per its own site). Your inclusions (walk-through video, local expertise) justify the middle or upper part.
- A common structure in design-build firms is a design fee near 10% of the construction budget ([Structure Studios](https://www.structurestudios.com/blog/whats-the-best-way-to-charge-for-a-landscape-design)). That is one firm's practice, not a rule.
- Revisit after 10 paid designs.
