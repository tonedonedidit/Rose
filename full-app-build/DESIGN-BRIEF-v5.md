# Force Gilbert Inventory: v5 brief (office first)

## The goal
The app should be one that the office trusts enough to stop keeping side spreadsheets. The floor should find it faster than asking someone, and a boss should be able to follow it without a walkthrough. Every number on screen comes from a person counting, receiving or pulling, and the app shows which numbers are verified and which are still guesses.

## Decisions already made (from your answers)
| Topic | Decision |
|---|---|
| Placeholder pallets in 3D | **Only placeholders** go see-through. Counted stock stays solid and realistic. |
| Ghost style | **Frosted glass plus a crisp outline**, tinted by part type |
| Who v5 is for | **Office first** (Scott, Nathan, buyers) |
| PO spreadsheets | **Hand-made Excel**: columns move around, and a file can have extra rows and notes |
| Short delivery | **The PO stays open for the rest** as a backorder |
| Office tools wanted | Arrived & paperwork, reorder list, usage by job, inventory value (**all four**) |
| Permissions | **Office-only** for deleting POs, editing parts, importing and confirming paperwork |
| Process | Brief first; **you approve it, then I build** |

---

## 1. 3D map: verified vs placeholder

**The rule:**

| State | What it means | How it looks |
|---|---|---|
| **Verified** | Counted with a real number | Solid, realistic contents: boxes, wrapped pallets, board units |
| **Placeholder** | Part is known but the quantity is not counted (e.g., D-11-d, D-12-c) | Frosted glass block with a crisp edge outline, tinted by part type, about 25% opacity |
| **Reserved** | Spot is set aside for a part but empty (e.g., D-13-c before the hinges arrive) | Outline only, with a faint floor footprint. No block. |
| **Empty** | Nothing set | Nothing drawn |

**Tints by part type** (one calm palette, readable in both light and dark):

| Part type | Tint |
|---|---|
| Hardware | Blue |
| Boards | Warm sand |
| Handles | Violet |
| Screws & nails | Slate |
| Packaging | Amber |
| Cabinet pallets | Teal |
| Molding & misc | Gray |

**Other map changes:**
- A small legend in the map's corner: **Solid = counted · Glass = not counted yet · Outline = reserved**.
- When a placeholder is counted, it fades from glass to solid on the spot. That gives a visible "verified" moment for a demo.
- Tapping a placeholder opens its card with **Count it** as the main button.
- The overview gets a **"Verified 12% of spots"** pill, so the boss sees progress at a glance.

## 2. Office hub (new tab; replaces Count in the bar for office users)

The Office tab has four tiles, with the numbers first.

**1. Today**
- Deliveries that arrived, what's still due, and what's late.
- **Slips not handed in** and **slips not confirmed**, with who received each one and when.
- One tap marks a slip received.

**2. Reorder**
- Parts at or below their reorder point, **grouped by vendor**.
- Each line shows have, coming and order qty (filled to "fill to").
- Buttons: **Copy for email** and **Make PO** (creates a draft PO the office edits).

**3. Usage by job**
- Search or pick a job #.
- Shows every pull, cut and handle for that job: part, quantity, from where, who, when, and cost.
- Totals per job, plus a top-jobs list for the week.
- Copy or export to Excel.

**4. Inventory value**
- Total dollars on hand, split by part type (bar list).
- **"N parts have no cost"** links straight to fixing them.
- Uses counted stock only. Placeholders are listed separately as **unverified**.

## 3. Incoming built for hand-made Excel

**Importing**
- **Open the .xlsx file directly** (from iPhone Files, email or a computer) using SheetJS. Pasting rows still works as a backup.
- **Smart header finding:**
  - Skips title rows, blank rows, totals and notes.
  - Finds the header row even if it isn't row 1.
  - Matches columns by meaning: PO, vendor, date, part #, description, qty, unit, cost.
- **Remembers the column layout** per file shape or vendor, so the second import is one tap.
- **Review screen before anything saves**, with every line marked:
  - **✓ matched** to an existing part
  - **New** part, created flagged for review
  - **Fix**: missing qty or an unreadable date
- **Duplicate POs** are not skipped silently. The office gets **Update lines** or **Skip** for each one.

**Short deliveries and backorders**
- Check-in records what came. If it was short, the PO becomes **Partial**: the missing qty stays open on the PO and shows under a **Backorder** filter.
- The next check-in only asks about what's still missing.
- The office can **Close short** (office-only), with a reason.

**Paperwork**
- A switch for **Slip given to office**, then **Office confirmed** (office-only), each stamped with name and time.

## 4. Permissions

**Office role:**
- Delete POs.
- Create, edit or delete parts.
- Import.
- Confirm paperwork.
- Close a PO short.
- Set costs.
- Change reorder points.
- Edit spot designations.

**Floor (everyone):**
- Receive, put away, count, move, take/pull, and pick lists.

**How the office role is assigned:**
- The page owner is office automatically.
- Office users can add or remove other people under Setup → People. Anyone who has used the app shows there.
- Office-only buttons are **hidden** for floor users (not shown greyed out), so their screens stay simple.
- This-device mode has an Office switch behind a 4-digit PIN.
- Honest limit: this is enforced by the app, not a bank-grade lock. Every change is still logged with who made it.

## 5. Professional layout rules (all screens)

- **Typography:** one scale only. Large title 34, section header 13 caps, body 17, secondary 15, numbers in rounded tabular figures.
- **Spacing:** 8 pt grid; 16 pt side margins; 22 pt between groups.
- **Numbers:** quantities right-aligned with units. Packs always read "47 boxes · 940 pcs".
- **Status:** a dot plus 1–2 words, the same everywhere (Counted / Not counted / Reserved / Wrong spot / Recount / Late / Partial).
- **Every list has an empty state:** one line, plus the button that fills it.
- **Every action confirms with a toast** that says what changed and where ("Added 2 boxes to D-13-c").
- **Destructive actions** are always last on a screen, in red, and ask for confirmation.
- **No jargon:** say "part", not SKU, and "spot", not location.

## 6. Done when
1. Placeholders render as tinted frosted glass with outlines, counted stock is solid, and the legend explains both.
2. A hand-made PO file with a title row and a totals row imports correctly from the .xlsx file in under 5 taps.
3. A 30-of-50 delivery leaves 20 on backorder, and the next check-in asks only for those 20.
4. A floor user never sees delete, import, edit-part or confirm-paperwork.
5. The Office hub shows today's slips, reorder by vendor, usage for a job #, and total value.
6. 390 pt wide with no sideways scroll, light and dark, zero console errors, and the existing data stays compatible.

## Not in v5 (later)
- Live Google Sheets sync (needs the Google Drive connector).
- Camera QR scanning inside the page; a Bluetooth scanner or the iPhone keyboard scanner works today.
- Real part numbers, Rack D levels 2–4 use, and Rack 0/1 and office rack bay counts. These stay placeholders until you send them.
