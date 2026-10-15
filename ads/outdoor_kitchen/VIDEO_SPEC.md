# VIDEO_SPEC: Outdoor kitchen / ramada / fire builders (Ad A)

Files: `SR_outdoor_kitchen_9x16.mp4` (1080x1920, 15.3 s), `SR_outdoor_kitchen_4x5.mp4` (1080x1350, 15.3 s), `SR_outdoor_kitchen_6s_9x16.mp4` (6.0 s retargeting bumper). Source is video A, referenced by ID only.

## Concept and why
**"Three things a spec sheet can't show."** Three-beat list: placement, flow, the upsell. Each beat is a different zone of the same yard, proven by its own shot. Chosen because the footage has a signature grill moment (stops a thumb at frame 0), a clean island-in-pad shot, a wide pullback that shows zones connecting, and a fire pit with a real flame. It has no night and no bare lot, so lights-on and before/after were never options. Segment assignment is provisional until B, D and E are audited.

## Audience and pain
Owners and sales reps at outdoor kitchen, ramada/pergola and fire-feature companies in the East Valley. Pain: high-ticket structures sold off a spec sheet; homeowners can't judge scale and placement; upsells (fire pit, heater, lighting) get skipped. Secondary viewer: the homeowner, who just sees a yard they want.

## On-screen lines, exactly as rendered (9:16 and 4:5 carry the same text)

| Time | Label (Plex Mono, tracked) | Headline (Cormorant Garamond, rose italic accent in *asterisks*) |
|---|---|---|
| 0.0–1.5 | OUTDOOR KITCHEN BUILDERS | Selling islands / off a *spec sheet?* (full alpha at frame 0; background wipes from a flat line drawing into the render over 0.0–0.9 s) |
| 1.5–2.8 | THREE THINGS | A spec sheet / *can't* show. |
| 2.8–6.8 | 01 / PLACEMENT | Where it *sits.* |
| 6.8–9.4 | 02 / FLOW | How the yard / *connects.* |
| 9.4–12.8 | 03 / THE UPSELL | The fire pit / they *skip.* |
| 12.8–15.3 | STONE & ROSE (wordmark) | Send us your next / outdoor *plan.* + stoneandrosellc.com + rose rule, over the last hero shot dimmed to 56% |

Bumper (6.0 s): 0.0–2.2 hook card (same as above), 2.2–4.0 "SHOW IT FIRST" / "Where it *sits.*", 4.0–6.0 end card.

Fade in/out 0.22 s per card (hook has no fade-in). Label size is 0.40x headline size (hook label 46 px on a 118 px headline). Text sits in negative space; per-card placement and luma in `SHOTLIST.md`.

## Runner-up hooks (primary-text candidates)
Outdoor kitchen builders: send the plan. / Your spec sheet isn't closing the island. / A spec sheet can't show scale. / Homeowner can't place the island? / Ramada builders: show the yard first. (full ranked list of 14 in `PLAN.md`)

## CTA
**Send us your next outdoor plan.** (31 characters.) Same wording on the end card, instant-form headline, button and primary text.

## Audio (synthesized; no licensed music)
Warm A-minor pad bed, around −24 dB. Ticks on every card-in. A rising whoosh into the biggest boom at 2.8 s (the island reveal, inside the 5 s payoff window). Smaller whoosh and boom at the 6.8 and 9.4 s cuts. A filtered-noise crackle bed under the fire pit shot (9.4–12.8 s). A bell chime on the end card at 12.8 s. Master: two-pass loudnorm with a pre-compressor. **Measured: −14.2 LUFS integrated, −1.2 dBFS peak** (9:16 and 4:5), −14.0 LUFS / −2.3 dBFS (bumper). Source audio is near-silent and unused.

## Placements QA'd
- Reels 9:16: safe box x 65–1015, y 270–1248, nothing at x>853 below y 1152. Checked on `QA_contact.jpg` (cyan and magenta overlays). Text and wordmark are inside the box on every card.
- Feed 4:5: bottom 15% (y > 1147) clear. Checked in preview.
- Phone read at 360 px wide: `QA_phone360.jpg`. Labels, headlines and the CTA are legible.
- Decode: `ffmpeg -v error -i X -f null -` returned zero errors on all three files.
- Sizes: 19.7 MB (9:16), 18.8 MB (4:5), 8.0 MB (bumper). All under 30 MB. Encode: x264 `-preset medium -crf 19 -maxrate 10M -bufsize 20M`, 30 fps, yuv420p, faststart.
- Length 15.3 s (inside 15–20 s). Payoff (grill hero, island reveal, boom) by 2.8 s. End card 2.5 s.
- Banned source seconds not used: 0–4, 39–42, 51–55, 66–75, and 26–27 s. The ball is outside every crop.

## Known risks
1. **Frame 0 is a line drawing.** The hook opens on an edge-filtered drawing of the first frame and resolves into the render by 0.9 s. It makes "spec sheet" literal, but the first frame is less lush than the render. Covers use t = 1.2 s. It is a filtered render, not a real spec sheet, so no claim is made about what the studio's sheets contain.
2. **Soft in 9:16.** A 608x1080 window scaled to 1080x1920 is a 1.78x upscale from a 1080p render. Stills of the grill look good but fine texture (stone, pavers) is soft on large phones.
3. **B2 scrim.** The flow headline sits on sky and mountains (luma ≈ 185), so its local scrim is the strongest in the ad (0.59). It reads as a soft glow, not a panel. (B3's text was moved onto the gray wall to avoid the same issue.)
4. **Fire pit cut at the edge in B2.** In the 9:16 flow shot the bowl is partly outside the window because a 608 px window can't hold pit and kitchen. Hero there is the dining pad and kitchen.
5. **Competitor-paste.** "Selling islands off a spec sheet?" is audience-specific but a rival render shop with its own footage could run it. Frame 0 and the end card are the parts they can't paste.
6. **Claim check.** The ad claims only what it shows. "The upsell" card shows a fire pit and does not claim any sales result.
7. **Statue vignette** at the right edge of the pullback (63.4–66 s) is small and cropped out of the 9:16; it's visible in the 4:5. Client-identifying? No names or addresses, but it's a personal item. Review before posting.
8. **Time of day.** No night shot exists in this footage, so this ad cannot claim or imply the evening-use story.
9. **Provisional.** Assignment and structure may change after B, D and E are audited.

## Legal audit (AZ ROC)
Every line checked: no "we build", "our crews", "design-build", "we install", "we manage", "licensed contractor" or "landscape architect". The CTA asks the contractor to send a plan. The crew that builds is the viewer's crew. **Pass.**

## Truth audit
No prices, stats, review counts, testimonials, "#1", years, or turnaround numbers. No invented people. **Pass.** (No turnaround placeholder needed in this ad.)

## VO
See `VO_SCRIPT.md` (38 words, timed to the cut; Tone records it).


## Fresh-eyes review (independent agent, saw only QA_contact.jpg and QA_phone360.jpg)

| Round | Stop power | Who it's for | Believability | CTA | Changes made after |
|---|---|---|---|---|---|
| 1 (first cut) | 4 | 6 | 6 | 4 | Hook headline enlarged to 118 px and label to 46 px; hook background now wipes from a line drawing into the render so "spec sheet" is literal; B3 text moved from sky to the gray wall (scrim 0.60 → 0.46); end card brighter (56% dim, scrim 0.50), wordmark 86 px, URL 48 px, held the full 2.5 s. |
| 2 (current cut) | 5 | 7 | 6 | 4 | Nothing yet. **Still under the 8 bar on all four.** |

Reviewer suggestions rejected because they break house rules: solid pill behind the label (banned: no solid panels), invented offers and speed claims, adding cities the footage doesn't show. The reviewer saw 0.3x contact sheets, so "tiny text" complaints are partly a resolution artifact; the 360 px phone read is the better test of label legibility.

Still open, in priority order:
1. **CTA/service clarity (4):** add a "WE DESIGN. YOU BUILD." tracked line above the CTA on the end card. It is on-brief for the ROC rule and tells the viewer what they get back. Not done yet.
2. **Stop power (5):** the hook text is still small relative to a feed-stopping headline, and a 608 px window forces the grill to sit small at 15–18 s. Options: open on the 22.2–24 s sun-glare grill with the hook over a clean lower area, accepting a tighter crop.
3. **"Spec sheet" proof:** the linework wipe is a filtered render, not a spec sheet. A real spec-sheet inset needs a real spec sheet from Tone.
4. **Beat 2 (flow):** the pullback shows zones, not a path. Needs a travelling shot (a 60 fps glide from kitchen to fire pit does not exist in this footage).
