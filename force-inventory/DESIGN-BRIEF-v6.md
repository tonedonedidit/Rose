# Force Gilbert Inventory: v6 brief (sections, search-to-map, pallet building)

## The goal
Split the app into **three storage sections that each work the same way**: Pallets, Boards and Hardware. The **map becomes the answer to "where is it?"** instead of a place you browse: search for anything, and the map glides there and tells you, in plain words, where to walk. Every screen has a reason to exist and the same shape as its neighbors.

## What you told me
| Topic | Decision |
|---|---|
| Pallets section | Aisles A, B, C. **Levels 1–3: single pallets. Level 4: double pallets only** (a+b, c+d), which already matches the spot codes, e.g. A-44-c+d. |
| Boards section | Bunks 1–4, Cantilever 1 & 2, Board drop |
| Hardware section | Rack D level 1, Hardware racks 1 & 2, **Rack 1 (excess handles)**. Hardware is tracked **by pallet**: one QR label per pallet, made in this app; no item labels. |
| Rack 0 | **Labeled "Supplies"** everywhere (map, search, spot codes stay R0-…). Holds molding, misc and cardboard on top. Shown as the Supplies area inside the Hardware section. |
| Pallet identity | Every cabinet has a QR sticker printed by the office (type, job, phase, building, floor, unit, color). A pallet is built by **scanning each cabinet into it**. The finished pallet gets a **printed sheet** with its own QR code, listing every item, quantity, building, unit and job name. |
| Bottom bar | My call, by the formula below |
| Office data | Stephen and Roman have the sheets. Questions for them are in a separate form. |

## The formula: how screens are ordered
Material moves in one direction: **arrives → is stored → leaves.** The app follows that order everywhere, left to right and top to bottom:

1. **Search first**: the fastest answer to most questions.
2. **Where things live**: the three sections, in the order a delivery is unloaded: Pallets, then Boards, then Hardware.
3. **What's moving**: Incoming, then Outgoing.
4. **Oversight**: Office, Count, Setup.

**Bottom bar:** Home · Pallets · Boards · Hardware · More (More becomes **Office** for office users).
- **Home** = search bar + "Today" (Receive, Put away, Pick lists, Count) + alerts.
- **More / Office** = Incoming, Outgoing, Count, Map overview, Reports, Import, Setup.
- **The map is no longer a tab.** It opens from search, from any spot, and from each section's header (section map).

## One template for every section (balanced and level)
Every section screen has the same five rows, in this order:

| Row | Pallets | Boards | Hardware |
|---|---|---|---|
| **1. Header** (name + one key number) | Pallets · 38 stored | Boards · 412 sheets | Hardware · 61 parts |
| **2. Two primary buttons** | **Build pallet** · Store pallet | **Receive boards** · Send to saw | **Grab parts** · Put away |
| **3. Status strip** (3 chips, tappable) | Building 2 · Ready to store 3 · Shipping today 4 | Low colors 2 · Not counted 9 · Wrong bunk 1 | Low 5 · Not counted 12 · Recount 1 |
| **4. Areas** (mini map tiles, tap = map glides there) | Aisle A · B · C, with % full | Bunks 1–4 · Cantilever 1 · 2 · Drop | Rack D · Hardware 1 · 2 · Rack 1 · Supplies |
| **5. List** (search within section) | Pallets by job | Boards by color / thickness | Parts by name |

Same spacing, same component sizes, same order. Learn one section and you know all three.

## Search → map (the main use of the map)
1. Search (Home or 🔍): part name, part #, color, job #, pallet #, spot code, or a **scanned QR**.
2. Tap a result. A **"Where it is"** card slides up, and the map glides to the spot in the background:
   - **Pin and beam** on the exact spot, with the rest of the warehouse dimmed slightly.
   - **Plain-words directions**, e.g. "Warehouse 1 → through the opening → Rack 1 (right of Cantilever 1) → shelf 3, bay 1."
   - **Quantity in big type**, plus the four verbs: Add · Take · Move · Count.
3. **More than one location:** chips across the card ("D-11-c · 47 boxes" · "Receiving · 30 pcs"). Tap a chip and the map glides there; all locations get small pins.
4. **A pallet search** shows the pallet's spot plus its contents: job, building, unit and item count.


## Map focus: one area at a time
- **Tapping a rack or area (e.g. Rack D) isolates it.** Every other aisle, rack and bunk disappears, leaving the floor, walls and that one area, so nothing blocks the view.
- **It starts at the beginning**, Bay 1 (or Column 1 / Bunk 1), standing in the aisle, not zoomed to the middle. "Next bay" and "Previous bay" buttons (and a swipe) walk down the run in order. The bay number shows large.
- **Overview** brings everything back. Search results isolate the area the item is in the same way, then glide to its exact spot.

## Pallets: build → store → ship
1. **Build pallet:** choose Single or Double, then **scan each cabinet sticker**.
   - Ways to scan (a page can't open a live camera on iPhone):
     - A **photo scan button** that opens the camera, decodes the QR from the picture, and adds it.
     - A Bluetooth or phone scanner that types into the field.
     - Typing the code.
   - Each scan adds a line (type, job, phase, building, floor, unit, color, read from the sticker as far as its data allows). A duplicate scan is caught.
   - A running count and a mismatch warning ("This cabinet is Building 3; the pallet is Building 2").
2. **Complete** prints the **pallet sheet** with the pallet QR, items, quantities, building, unit and job name. It's sized for 4×6 thermal labels and letter paper.
3. **Store pallet:** scan the pallet QR (or pick it). The app suggests a spot: singles on levels 1–3 and doubles on level 4, keeping one job together where possible. You confirm and it's done.
4. **Ship:** pick pallets by job (or truck). Mark each loaded, then mark the truck gone. The spots free up.
5. **Search any cabinet QR** and you land on its pallet and spot.


## Old QR codes: decoded and reused (no reprinting)
Decoded from your photos:

| Label | QR holds | Meaning |
|---|---|---|
| **Pallet sheet** | `Pallet:6aba968423164b53da864c63` | The old app's pallet record ID (24-character database ID; created Sep 28, 2026). It holds no contents itself. |
| **Cabinet sticker** | 8 lines of text: `Granville Remodel` · `PO#3303b-GVR-4` · `Group 48 - [Casita Unit 1065]` · `1065` · `2bed Casita Type A` · `Ultra Light Grey #8` · `B30-ADA` · `10651117` | Job · Order · Building · Unit · Type · Color · Cabinet · Cabinet ID (unit 1065 + label ID 1117) |

What the app does with them:
- **A cabinet sticker describes itself.** A scan fills in job, PO, building, unit, type, color and cabinet with no lookup and no office export. The cabinet's key is PO + cabinet ID, so the same ID on different jobs never collides.
- **A pallet sticker is a key.** The old ID becomes the pallet's permanent ID in the new app. Nothing is reprinted.
- **Bringing an existing pallet into the app takes about one minute per pallet:**
  1. Scan the pallet sheet.
  2. The app says it doesn't know this pallet yet and asks you to scan its cabinets.
  3. Scan the cabinet stickers you can reach.
  4. The app fills the pallet (job, building, unit, PO, item list and count) and compares it to the printed total ("14 of 16 scanned").
  5. Store it in its spot.
  
  No retyping, no reset. An export from the old app, if one exists, would just skip this step.
- **New pallets** keep the same `Pallet:<id>` format, so old and new stickers work the same way, and the printed sheet keeps the same layout (job, group/unit, PO#, item · quantity · building, total).


## Hardware pallets: one QR per pallet, made in this app
- **Hardware has no item labels.** Each hardware pallet gets **one QR label, created and named in this app**, e.g. "Blum hinges & plates" or "Slides 16 in., white".
- **Making one:** in Hardware → **New hardware pallet**:
  1. Name it.
  2. Choose its spot (e.g. D-11-c).
  3. Add what's on it (part + quantity, with box math).
  4. Print the label: a large name, the spot, the QR, and the date.
- **A pallet keeps its contents when it moves.** The contents belong to the pallet, not the rack spot: move the pallet to another spot and everything on it moves too.
- **One Scan QR button, everywhere** (Home, the search bar, each section). Whatever is scanned goes to the right place:

| Scanned | Goes to |
|---|---|
| `Pallet:<id>` (old cabinet pallet sheet) | Pallets → that pallet: spot, job, unit, items, with Store / Move / Ship |
| Cabinet sticker (8 text lines) | Pallets → the pallet that cabinet is on, with the cabinet highlighted (or "Add to pallet" while building one) |
| **New hardware pallet label** | Hardware → that pallet: contents with **View · Take · Add · Count**, its spot, and a map pin |
| Spot label (e.g. D-11-c) | That spot's card |

- New labels use a clear prefix so they never clash with the old ones, e.g. `FORCE:HW:<id>` for hardware pallets and `FORCE:SPOT:D-11-c` for spots. Plain old spot codes still work.

## Boards
- **Bunk view:** a 4×4 grid colored by the rule (white, colored, 6 mm). Each cell shows units and sheets. A wrong-bunk board is outlined red.
- **Receive boards** and **Send to saw** (sheets cut today by color feed the daily report).
- **Cantilevers:** columns × arms, matching the real 8/8/5 layout. **Board drop** is flagged if anything sits there more than 2 days.

## Hardware
- **Grab parts** stays the fastest path: tap a part, set quantity, enter the job, and you're done.
- **Rack D level 1 boxes** show box count and pieces. **Rack 1** groups handles by style and finish. **Supplies (Rack 0)** shows molding and misc, with cardboard on top.
- Reorder points live here (office-only to edit).

## Connected: every object links to its neighbors
- **Part → spots → map**, and **spot → part → its PO and its pulls**.
- **Pallet → its cabinets → job → shipments**, and **cabinet QR → pallet → spot**.
- **PO → items → where each was put away**, and **job # → everything pulled and every pallet**.
- Every number is tappable and goes to the thing it counts.

## Done when
1. Search "hinge" (or scan a cabinet QR) and in **one tap** the map glides to the spot with plain-words directions.
2. A pallet can be built by scanning cabinet stickers, printed, stored on the right level, and found again by scanning any cabinet on it.
3. The three sections use the identical five-row template.
4. Everything still works at 390 pt, in light and dark mode, with zero errors, and the existing data stays compatible.

## Open questions (in the office form for Stephen and Roman, plus these for you)
1. ~~Rack 0~~ Decided: labeled **Supplies**.
2. ~~Old QR codes~~ Decoded (see above). Optional: the old app's name, and whether it can export pallets. That would only speed up bringing existing pallets in.
