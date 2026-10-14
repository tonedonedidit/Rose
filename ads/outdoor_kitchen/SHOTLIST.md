# Shot list: Ad A (outdoor kitchen)

30 fps output from 60 fps source, no speed ramps (every shot is a hero moment, real-time). Crop windows follow hero centers measured on 1920-px source frames. 9:16 = 608x1080 source window scaled to 1080x1920. 4:5 = 864x1080 window scaled to 1080x1350. Windows are top-anchored (y0 = 0) so the hero sits low and the text zone above it stays clean.

Grade (all shots): shadow lift (gamma 0.90), mild S-curve, +2.5% red / −3.5% blue. The footage is one golden-hour daylight state throughout, so the grade is identical on every shot and no cut jumps.

Source second numbers below are source timestamps (0–76 s). Ad time is in the first column.

| Ad time | Shot | Source in–out | Push-in | 9:16 crop (hero centre x, window x0 range) | 4:5 crop | Reason |
|---|---|---|---|---|---|---|
| 0.0–2.8 | H hook | 15.2–18.0 (first 0.9 s wipes from edge-filtered linework into the render) | none (1.00) | grill centre 770 → 690 → 695; x0 466 → 386 → 391 | grill + fridge, centre 860 → 790 → 800 | Opens on the stainless grill, the signature subject, with clean dark wall above it for text. A 608 px window cannot hold the whole island (≈1000 px wide at 17 s), so the grill is the hero: at 15.2–18.0 s it is 510–600 px wide and fits. Push-in is off because at 1.05 the grill hood slices at the right edge (checked in preview). Real time. Source 0–4 s is banned (dark passage). |
| 2.8–6.8 | B1 placement | 10.0–14.0 | 1.00 → 1.05 | island centre 665 → 820 → 915; x0 361 → 516 → 611 | centre 765 → 860 → 960 | Island under the ramada in its herringbone pad. The camera dollies forward and the island drifts right in frame, so the crop drifts right with it (leading the subject, same direction as the move). Cut into it from the hook is a static-to-move contrast. Chairs at right (1330+) intentionally left out: they are not the hero. |
| 6.8–9.4 | B2 flow | 63.4–66.0 | 9:16 1.00 → 1.03; 4:5 1.06 → 1.09 | centre 736 → 722; x0 432 → 418 | centre 760 → 745 | Pullback that puts pad, dining set, lawn edge and kitchen in one frame. Hero is the dining pad and the kitchen across the lawn, not the fire pit (which is beat 3's hero), so the bowl can sit at the frame edge. 4:5 starts at 1.06 so the bottom crop removes the soccer ball. 9:16 starts at 63.4 s so the ball (x≈1130) is outside the window. Stops at 66.0 s, where the ball becomes large. |
| 9.4–12.8 | B3 upsell | 45.2–48.6 | 1.00 → 1.06 | fire pit centre 990 → 1150; x0 686 → 846 | centre 1000 → 1150 | Fire pit with flame, bowl fully inside the window, chair and sofa edge as context. The camera drifts left-to-right; the crop follows. Soccer ball (x≈340) stays outside. |
| 12.8–15.3 | E end card | 48.6–51.1 | 1.00 → 1.03 | centre 1100 | centre 1100 | Last hero shot continues, dimmed to 56% under the end card (2.5 s, the maximum). Stops before 51.2 s: 51–55 s (gray wall) is banned. |

## Text positions (and why)

| Card | Ad time | 9:16 position | Reason (measured luma in the text box on the cropped, graded frame) |
|---|---|---|---|
| hook | 0.0–1.5 | label y 276 (46 px), headline y ~356 (118 px) | Dark ramada wall above the grill, luma 38. Light scrim only (0.22). No fade-in. Enlarged after review feedback that the hook read small. |
| three | 1.5–2.8 | same | Same wall, luma 27. |
| b1 | 2.8–6.8 | same | Roof underside and dark wall, luma 76, scrim 0.27. Keeps clear of the TV at right (text ends before x≈700). |
| b2 | 6.8–9.4 | same | Sky and mountains, luma 185, scrim 0.59, local to the text box. |
| b3 | 9.4–12.8 | label y 600 (9:16) / 470 (4:5), left | **Moved from the top** (sky and house wall, luma 240, needed a 0.60 scrim that read as a smudge) down onto the gray back wall: luma 141, scrim 0.46. Sits above the sofa and fire pit, not on them. |
| end | 12.8–15.3 | centered, y 560–1000 | Over the dimmed seating shot, local scrim 0.50, wordmark 86 px, URL 48 px. Inside the safe box (x 65–1015, y 270–1248). |

4:5 uses the same left-aligned text with label at y 190 and nothing in the bottom 15% (y > 1147).

## Card timing
Every card fades in and out in 0.22 s with a 10 px upward settle on the way in (no bounce). The hook card is full alpha at frame 0.
