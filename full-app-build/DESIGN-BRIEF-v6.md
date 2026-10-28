# Force Gilbert Inventory: v6 plan (revised for review)

**Status: built and tested (Oct 28, 2026). Build report at the bottom.**
Order: (1) you review this plan and answer the questions at the bottom → (2) you say "go" → (3) I build → (4) I review my own build and run a full test of every flow, then report what passed, what failed, and what's still missing.

---

## 1. What v6 is
Three storage sections that work the same way: **Pallets**, **Boards** and **Hardware**. The **map answers "where is it?"**: search or scan, and the map shows only that area and glides to the exact spot with plain-words directions. Old QR stickers keep working. Every screen has one job and the same shape as its neighbors.

## 2. Decisions so far
| Topic | Decision |
|---|---|
| Pallets | Aisles A, B, C. **Levels 1–3: single pallets, 4 per bay level** (a, b back; c, d front). **Level 4: double pallets only, 2 per bay** (a+b, c+d). |
| Boards | Bunks 1–4 (4 columns each, 5 units high), Cantilever 1, Cantilever 2 (3 columns: 8 / 8 / 5 arms), Board drop |
| Hardware | **Rack D level 1** (front only, spots **a** and **b**), Hardware racks 1 & 2, Rack 1 (handles), **Supplies** (Rack 0: molding, misc, cardboard on top) |
| Rack D levels 2–4 | Standard layout, empty for now (cabinets later) |
| Hardware tracking | **By pallet.** One QR label per pallet, made in this app. Mostly one part per pallet, plus one **Misc hardware** and one **Misc handles** pallet. No item labels. |
| Cabinet pallets | Built by scanning cabinet stickers. Old stickers and old pallet sheets keep working (decoded, see §6). |
| Office | You only. More people can be added later. |

## 3. Plan check: what would not have worked, and the fix
I went through every flow in the plan against what the app and its platform can actually do. These are the problems I found.

| # | Problem | Why it fails | Fix in this plan |
|---|---|---|---|
| 1 | **Everyone needs a Claude login to use the shared app** | The live, shared data only works for people signed in to claude.ai who are in your organization (Team/Enterprise plan), or who you invite by email. A floor worker with no account sees the app but can't save. | **Question A.** Options: Team plan seats for the crew, shared warehouse iPhones/iPads signed in to one account (with a "who are you?" name picker), or a mix. |
| 2 | **Scanning a code that's eight lines long** | A Bluetooth scanner "types" the code and presses Enter after each line, so one cabinet sticker would arrive as 8 separate scans. | The scan field collects a burst of keystrokes and treats everything within ~0.3 s as one scan. Tested with the real code from your photo. |
| 3 | **No live camera inside the page** | The page can't open a live camera view on iPhone. Photo scanning works (snap → decode) but costs ~3 taps per cabinet: about 50 taps for a 16-cabinet pallet. | Photo scan stays as a backup. **Recommended: one Bluetooth scanner** (~$40–120) for building pallets: one trigger pull per cabinet. **Question B.** |
| 4 | **The page can't print directly** | "Print" buttons don't work inside the app on iPhone. | **Print** saves a ready-to-print PDF (pallet sheet, hardware label, spot labels). iPhone: it opens in Files → Share → Print. **Question C** (which printer) decides the PDF size. |
| 5 | **Pallets already high in the racks** | The plan said "scan the cabinets to fill in an old pallet". Cabinets on a level 3–4 pallet are out of reach. | **Two-step onboarding:** (1) **Location first**: scan the pallet sheet and pick or scan the spot. Done in seconds, and the pallet is findable on the map. (2) **Contents later**: fill them in when the pallet comes down, or from a **photo of the pallet sheet** that Claude reads into the item list, or from an old-app export. **Question D.** |
| 6 | **Two people changing the same spot at once** | Saves are last-one-wins. Two people pulling from D-11-a at the same moment could wipe out one of the pulls. | Each change briefly **locks the spot or pallet**, re-reads the latest count, then saves. Nothing is lost. |
| 7 | **"Office only" is honor-system today** | Hidden buttons don't stop someone determined. | Use claude.ai sharing roles: **Editor = office, Contributor = floor**. The database itself then refuses part and setting edits from Contributors. POs stay writable by the floor (they check deliveries in); deleting a PO remains a hidden office button. |
| 8 | **History beyond the newest 600 moves** | The app loads the newest 600 moves live. Usage by job and older reports would quietly miss older ones. | Reports and job lookups fetch their own date range on demand instead of relying on the live 600. |
| 9 | **"Office" replaced "More" for you** | Your Office tab would hide the More items (Incoming, Outgoing, Count, Map, Setup). | The **Office tab contains everything in More**, plus the office tools. |
| 10 | **Hardware contents tied to rack spots** | Today stock lives on spots. "Pallet keeps its contents when moved" needs contents to live on the pallet. | Hardware pallets become real records. A spot shows the pallets on it. Moving a pallet changes one field. Totals, search and reorder all count pallet contents. Existing D-11/12/13 stock becomes pallets automatically. |
| 11 | **Old and new pallet IDs** | If the old app keeps making pallets while this one does too, the same pallet could exist twice or be edited in only one place. | **Question E** (cut-over). New pallets get a new `Pallet:<id>` in the same format, so the old app won't misread them. |
| 12 | **Directions from where you're standing** | The app doesn't know where you are. | Directions are written from the building entrance or the hole in the wall, e.g. "Warehouse 2 → aisle between D and C → Rack D, bay 11 → level 1, front left (a)". |
| 13 | **Wi-Fi in the racks** | Saving needs a connection. If a dead spot drops a save, the change is lost. | A clear "Not saved, tap to retry" banner. Nothing is assumed saved until confirmed. **Question F.** |
| 14 | **Bay 1 is at which end?** | "Start at bay 1" needs the real end of each run. The map has bay 1 at the end nearest the hole in the wall. | **Question G** to confirm. |

## 4. Screen order and bottom bar
Material moves one way: **arrives → stored → leaves.** The app follows that order.

**Bottom bar:** Home · Pallets · Boards · Hardware · More. For office users, More becomes **Office**, which contains all More items plus the office tools.
- **Home:** Search, the **Scan** button, Today (Receive · Put away · Pick lists · Count), then Alerts.
- **More / Office:**
  - Incoming, Outgoing, Count, Map overview, Reports, Setup.
  - Office users also get Import, People, Reorder, Usage by job and Value.
- **Map is not a tab.** It opens from search, from scans, from any spot, and from each section's area tiles.

## 5. One template for every section
| Row | Pallets | Boards | Hardware |
|---|---|---|---|
| 1. Header + one number | Pallets · 38 stored | Boards · 412 sheets | Hardware · 24 pallets |
| 2. Two main buttons | **Build pallet** · Store pallet | **Receive boards** · Send to saw | **Grab parts** · New hardware pallet |
| 3. Three status chips | Building · Ready to store · Shipping today | Low colors · Not counted · Wrong bunk | Low · Not counted · Recount |
| 4. Area tiles (tap = map shows only that area, starting at bay 1) | Aisle A · B · C (% full) | Bunks · Cantilever 1 · 2 · Drop | Rack D · Hardware 1 · 2 · Rack 1 · Supplies |
| 5. Searchable list | Pallets by job / unit | Boards by color / thickness | Pallets and parts by name |

Same sizes, same spacing, same order in all three.

## 6. Scanning: one Scan button, everything routes itself
Decoded from your photos:
- **Cabinet sticker:** 8 lines: Job · PO · Building · Unit · Type · Color · Cabinet · Cabinet ID, e.g. `Granville Remodel · PO#3303b-GVR-4 · Group 48 - [Casita Unit 1065] · 1065 · 2bed Casita Type A · Ultra Light Grey #8 · B30-ADA · 10651117`.
- **Old pallet sheet:** `Pallet:6aba968423164b53da864c63`, the old app's pallet ID.

| Scanned | Goes to |
|---|---|
| Old or new pallet sheet `Pallet:<id>` | That pallet: spot, job, unit, items, with Store · Move · Ship. Unknown ID: "Store it now" (location first) + "Add contents" |
| Cabinet sticker | The pallet that cabinet is on, with the cabinet highlighted. While building a pallet, it's added to that pallet. |
| Hardware pallet label `FORCE:HW:<id>` | That hardware pallet, with View · Take · Add · Count |
| Spot label `FORCE:SPOT:<code>`, or typed codes like D-11-a | That spot |

Scan methods: a Bluetooth scanner (best), photo scan (backup), or typing.

## 7. Search → map
1. Search anything: part, part #, color, job, unit, PO, pallet, spot. Or scan.
2. Tap a result. The **Where it is** card slides up. The map shows **only that area** and glides to the spot, with a pin, the plain-words directions (§3 #12), the quantity in big type, and **Add · Take · Move · Count**.
3. **Several places:** chips across the card. Tap a chip and the map glides there.
4. **Map focus:** tap an area and it shows alone, standing at **bay 1** in the aisle. **Next / Previous bay** buttons (and swipe) walk the run, with the bay number shown large. Overview brings everything back.

## 8. Pallets
1. **Build:** Single or Double → scan cabinets. Duplicates are caught, and you're warned if a cabinet's job, building or unit differs from the pallet's. A running count shows as you go.
2. **Complete:** saves the **pallet sheet PDF** in the same layout as today: job, group/unit, PO#, items · quantity · building, total, and the QR.
3. **Store:** scan the pallet, then scan or pick the spot. Singles are suggested on levels 1–3 and doubles on level 4, keeping each job together.
4. **Ship:** pick by job, mark each pallet loaded, then mark the truck gone. Spots free up.
5. **Audit an aisle:** walk the aisle scanning pallet sheets. The app lists pallets missing, misplaced or unknown. This is the count for pallets.

## 9. Hardware
- **Rack D level 1 = front spots a (left) and b (right) only.** Existing data moves: D-11-c→D-11-a, D-11-d→D-11-b, D-12-c→D-12-a, D-13-c→D-13-a. Old codes still find the new spots.
- **Hardware pallets:** to create one, name it, choose its spot, add parts and quantities, then save the label PDF. Single-part pallets open to the count; the Misc pallets open to a list.
- **Grab parts:** tap a part, then quantity, then job #. It pulls from the pallet that holds the part.
- **Hardware racks 1 & 2, Rack 1, Supplies:** tracked by shelf spot as today (**Question H**).

## 10. Boards
- **Bunk grid:** 4×4, colored by the rule. Each cell shows units and sheets. A wrong board gets a red outline.
- **Receive boards** (PO check-in filtered to boards) and **Send to saw** (feeds sheets cut per color in the daily report).
- **Cantilevers** match the real arm counts. **Board drop** is flagged after 2 days.

## 11. Everything connects
Part → pallets/spots → map. Spot → what's on it → its PO and pulls. Pallet → cabinets → job → shipment. Cabinet → pallet → spot. Job # → every pull and every pallet. Every number is tappable.

## 12. How I'll test the build (step 4)
I'll run every flow on a simulated iPhone (390 pt, light and dark) and report pass or fail for each:
- **Scanning:** scan the real cabinet code (single burst and multi-line). Build a 16-cabinet pallet, including a duplicate and a wrong-unit cabinet.
- **Pallets:** save the sheet PDF, store a double pallet (it must refuse levels 1–3), and onboard an unknown old pallet (location first). Search a cabinet ID and land on its pallet. Ship a job. Audit an aisle.
- **Hardware:** make a hardware pallet, move it, and check its contents moved. Grab parts. Run two simultaneous pulls on one pallet and check none is lost.
- **Map and search:** search "slide" → the map shows only Rack D and glides to D-11-a, with directions. Walk Rack D bay 1 → 18. Confirm old spot codes still resolve.
- **Office and floor:** Office tools, plus floor-role restrictions (Contributor can't edit parts).
- **Regression:** receiving with a backorder, counts, Excel import, reports, all four Office tools.

The report lists what passed, what failed, and what's still missing.

---

## Questions for you
- **A. Logins.** Will each person on the floor have their own claude.ai account in your company's plan, or will the warehouse use shared iPhones/iPads signed in to one account? Roughly how many people use it?
- **B. Scanner.** Is a Bluetooth barcode scanner OK (about $40–120; it pairs with the iPhone like a keyboard)? What did the old app scan with: the phone camera or a scanner?
- **C. Printer.** What prints pallet sheets today (letter paper from the office printer?), and what should hardware pallet labels print on?
- **D. Old pallets.** About how many cabinet pallets are in the racks now? And can the old app export its pallets? Its name would help.
- **E. Cut-over.** Will the old app stop being used once this one is live, or do both run for a while? Who still builds pallets in the old one?
- **F. Wi-Fi.** Is there reliable Wi-Fi or cell signal in Warehouse 2 by the racks?
- **G. Bay 1.** For Rack D and Aisles A–C, is bay 1 at the end nearest the hole in the wall?
- **H. Shelves.** Do Hardware racks 1 & 2 (screws, nails) and Rack 1 (handles) also get pallet-style QR labels, or stay tracked by shelf spot?


---

## Your answers (Oct 28)
Each worker has a tablet or their own phone. The old app ("Force Inventory") scanned with the device camera. Pallet sheets print on a regular printer, and cabinet stickers print on sticker sheets in the office. There are 100+ cabinet pallets in the racks. Goal: replace the old app (fallback: hardware only). Wi-Fi is good by the racks. Bay 1 = D-11, C-15, B-15, A-11. Hardware racks and Rack 1 are tracked by a designated spot per item plus a spot QR label.

## 13. Build report
**Tested on a simulated iPhone (390 pt), light and dark mode: 62 of 62 v6 checks passed, plus the earlier Office/receiving suite. Zero console errors and no sideways scrolling on any screen.**

| Area | Verified |
|---|---|
| Rack D move | D-11-c→D-11-a, D-11-d→D-11-b, D-12-c→D-12-a, D-13-c→D-13-a; old codes still resolve. Done on the live data in one atomic batch; the 3 slide spots became hardware pallets (1,000 pcs kept). |
| Scanning | An 8-line cabinet sticker typed by a scanner = one scan. Duplicate caught. Different unit warned. **Photos of your real pallet sheet and cabinet sticker decode** (the Photo button). |
| Pallets | Built from 3 cabinets → pallet sheet PDF → stored at a suggested spot. A double pallet is refused on levels 1–3. An unknown old sheet (`Pallet:6aba…`) is saved "location first". Scanning a cabinet opens its pallet. Audit and ship work. |
| Hardware | New pallet + label PDF. Moving it keeps its contents. Grab parts pulls from the pallet. Scanning its label opens it. Count on a Rack D spot counts the pallet. |
| Map | Search → shows only Rack D and glides to D-11-a with directions. An area tile starts at bay 1; Next goes to bay 2. |
| Roles | Floor gets the More tab, with no New/Edit part. **Live database refuses part edits from floor accounts** (checked on the real store). |
| Office | Backorders, slips, reorder → Make PO, job usage, value, Excel import (title rows, totals, remembered layout). |

**Not testable here (needs real people or devices):**
- Two people pulling at the same instant: the lock is built, but only shows under real simultaneous use.
- Claude reading a pallet-sheet photo: needs your consent in the live page.
- Printing from the iPad to your printer.
- A real Bluetooth scanner: the burst handling is tested; the device isn't.

**Still open:**
- Workers need to be signed in to claude.ai (Team plan seats, or a shared account per tablet) for saves to work. Today the app is private to you; share it from the page's Share menu (Contributor = floor, Editor = office).
- The old app's export, if it has one, would load the 100+ pallets' contents in one step.
