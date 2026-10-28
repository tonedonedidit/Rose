# Liquid Glass: how we design

These are the rules for every screen, page and graphic in the Force Gilbert app, and for anything built after it. Follow them and the work looks like one product from one hand. Break one only on purpose, and write down why.

---

## 1. The idea in one line
**Content sits on frosted glass that floats over a warm, softly lit room.** The glass is never the hero. It is a calm surface that lets the one thing you need, a number, a spot or a button, read instantly.

## 2. The three layers
Every screen has exactly three depths. Don't add a fourth.

| Layer | What lives there | How it's made |
|---|---|---|
| **Backdrop** | Nothing you tap | Base color plus 3–4 large, very blurred color blobs (peach, lavender, warm sand). Fixed; never scrolls. |
| **Glass** | Lists, tiles, cards, inputs | Translucent fill + backdrop blur + a lit top rim + a soft drop shadow |
| **Floating glass** | Tab bar, sheets, menus, toasts | The same glass, more opaque and blurrier, detached from the screen edges, with a bigger shadow |

Never put glass on glass on glass. Inside a sheet, cards use a flat translucent fill with **no** second blur. Stacked blur gets muddy and slow on iPhone.

## 3. Glass recipe (copy exactly)
```css
background: var(--cell);                       /* light: rgba(255,255,255,.58) · dark: rgba(255,245,235,.075) */
backdrop-filter: saturate(180%) blur(22px);
border: 1px solid var(--rim);                  /* light: rgba(255,255,255,.78) · dark: rgba(255,240,225,.16) */
box-shadow: inset 0 1px 0 rgba(255,255,255,.95),   /* the lit top edge: this is what makes it "liquid" */
            0 12px 32px -14px rgba(60,40,20,.22);  /* warm, low, soft. Never pure black. */
```
- **The top rim is mandatory.** Without the inset highlight it's just a gray box.
- **Shadows are warm** (brown-tinted) and pushed down with negative spread. Avoid hard, centered or gray shadows.
- Always keep a fallback: if `backdrop-filter` isn't supported, the fill goes ~92% opaque so text stays readable.

## 4. Color
- **One accent: orange.** Light `#C2410C` (text and icons, 4.9:1 on white) with `#F27A2E` as the top of gradients. Dark `#FF8A3D`.
- The accent marks **what you can do**: primary buttons, selected tab, links, spot codes. Status never uses it.
- **Status colors are small and fixed:** green counted, orange not counted, red wrong or late, purple recount. They appear as a dot or chip, never a full fill.
- **Text:** warm near-black `#16120F` / secondary `#6E6A66`. In dark mode, warm white `#FBF6F1` / `#B3A79C`. Never pure `#000` on glass.
- **3D part tints** (map only): hardware blue, boards sand, handles violet, screws slate, packaging amber, pallets teal, misc gray.
- **Dark mode** is a warm, dim room (`#140E0A` with amber glow). It is not a black screen.

## 5. Shape
| Element | Radius |
|---|---|
| Buttons, tabs, chips, search, steppers, segmented controls | **Capsule** (999px) |
| Tiles | 26px |
| Lists and cards | 22px |
| Sheets | 34px, inset 8px from screen edges |
| Map stage | 30px |
| Small spot cells | 14px |

Corners get rounder as things get bigger and float higher. Never mix a sharp corner into a glass screen.

## 6. Type
- **System font** (SF Pro on iPhone). One family, no decorative fonts.
- Scale: **Large title 34/700** (tight −2.5% tracking) · **Section header 13/600 caps, +6% tracking** · **Body 17** · **Secondary 15** · **Caption 13**.
- **Numbers use rounded, tabular figures** so quantities line up and feel friendly. The big quantity on a spot card is 44px.
- Labels are 1–3 words. A sentence is a hint, and a hint gets one muted line at most.

## 7. Space and layout
- 8 pt grid. 16 pt side margins. 22 pt between groups. 12 pt between tiles.
- **Thumb zone:** primary actions sit in the bottom third. The main button is full-width, 52 pt tall and pinned above the home bar.
- Tap targets are at least 44 pt. Tab items 54 pt.
- One screen, one job. Actions come first; lists and history sit behind a tap.

## 8. Controls
- **Primary button:** orange vertical gradient, white text, lit rim, orange glow underneath. **One per screen.**
- **Secondary button:** glass with orange text. **Destructive:** glass with red text, always last, always confirmed.
- **Segmented control:** glass capsule track; the selected segment is a raised white pill.
- **Stepper:** round glass − and +, with a large rounded number between them and the total spelled out underneath ("2 boxes = 40 pcs").
- **Icons:** 2 pt outline strokes, rounded caps, sitting in a white-glass circle in the accent color. No multicolor icon squares.
- **Tab bar:** a floating glass capsule. The active tab gets an orange-tinted lens pill behind its icon.

## 9. Motion
- Sheets rise in 280 ms on a soft spring (`cubic-bezier(.2,.9,.3,1)`). Menus pop at 160 ms from their anchor.
- The 3D camera glides on an eased curve with a slight lift. It never cuts.
- Respect **Reduce Motion**: no slides or flights, only instant changes.
- Motion explains where something came from. It is never decoration.

## 10. The 3D map in the same language
- Light, warm interior (`#E9E4DE`), concrete floor, tilt-up walls cut away on the camera side.
- **Solid = counted.** **Frosted glass with a tinted outline = not counted yet.** **Outline only = reserved, empty.** The legend sits under the map, always.
- Labels are small glass capsules. Bay labels are dark glass, so they read over racks.
- The map's floating controls are round glass buttons. The selected state is the orange gradient.

## 11. Before anything ships, check
- [ ] Three layers only; no glass-on-glass blur inside sheets
- [ ] Every glass surface has the lit top rim
- [ ] One primary (orange) button per screen
- [ ] Text contrast ≥ 4.5:1 on its glass, in **light and dark**
- [ ] 390 pt wide: no sideways scroll, nothing under the home bar or notch
- [ ] Works with Reduce Motion and without `backdrop-filter`
- [ ] Every list has an empty state; every action has a toast saying what changed and where
- [ ] Zero console errors
