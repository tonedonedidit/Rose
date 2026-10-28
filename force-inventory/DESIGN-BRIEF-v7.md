# Force Receiving & Inventory — v7 plan (for your review)

**Status: plan only. Nothing is built.** You review → answer the questions at the end → say "go" → I build → I replay your hypothetical day as a full test and report what passes and what doesn't.

## 1. What the app is for (one sentence)
**The office and the shop see the same deliveries, the same counts and the same problems, live, so what was ordered, what arrived and what's on the shelf always match, and nobody orders just to order.**

Everything that doesn't serve that sentence gets cut (see §6).

## 2. Your day, mapped to the app
| Time | What happens | What the app does |
|---|---|---|
| Before 6:00 | Stephen's Excel already lists every open order: 12 units of white 6 mm board, 10 pallets of hardware, 7 cardboard, 12 pallets of doors, each from a different vendor with its own date | The app **reads the Excel live**. No uploading. Each order line shows under its delivery date. |
| 6:10 | Tony opens the app | **Today** shows 4 deliveries expected: Boards (Vendor A), Hardware (Vendor B), Cardboard (Vendor C), Doors (Vendor D), with what's on each. |
| 7:00 | Boards arrive, all good. Tony signs the paper and checks it against the paper | One tap: **"All here, all good."** No line-by-line re-entry; the paper is still the paper. The delivery turns ✓ **Arrived** for the office instantly. |
| 7:05 | Put away | Boards appear in **Put away**. Each **stack** goes in with its count (40 + 40 + 20) into **bunk slots** that fit the board (white 3/4 → Bunk 1, 6 mm → Bunk 4…). The tally shows 100 of 100 ✓. |
| 8:00 | Stephen arrives | His **Office board** already shows: Boards ✓ arrived complete at 7:00, put away in BK4-1/BK4-2. He didn't have to walk over to know. |
| 9:00 | Hardware arrives; 1 box of strap missing vs the list | Tony taps **"Something's wrong"** → Missing → *Strap, 1 box* → note *"Not on truck; driver says backordered."* The delivery shows ⚠ **Arrived with 1 issue**, and the issue lands in Stephen's queue. Everything else gets put away into its spots. |
| 10:00 | Cardboard didn't come. Stephen types **Delayed** in the Excel status cell | The app picks up the change on its own within a couple of minutes: Cardboard moves from *Today* to *Delayed (new date)*. Nobody re-uploads anything. |
| 11:00 | Door pallets arrive (doors team) | Received by pallet count against the order: *12 of 12 pallets ✓*. Each pallet's sizes and quantities per job come from the order. |
| Later | At the door machine, one door is scratched | A shared **"Report a problem"** screen at the door station: **−1 · Vanity 45 sink base door · Job 24-1182 · Damaged · "scratched"**. It goes straight to Stephen's **Reorder queue**. |
| Office | Stephen reorders | He taps **Reordered**, enters the new PO#, and the issue moves to *Waiting on replacement*. When that PO line arrives, it **archives itself**. |

## 3. The few things the app holds
1. **Order lines (from Excel; the office owns these):** PO#, vendor, item #, description, type (Boards / Hardware / Packaging / Doors), qty + unit, expected date, status (*Ordered / Delayed / Cancelled*), job (doors), note. The app never edits them.
2. **Deliveries (the shop owns these):** lines grouped by vendor + PO + date. States:
   - *Expected → Arrived ✓ / Arrived with issues ⚠*. Also *Late* (date passed, automatic), *Delayed* (set in the Excel) and *Cancelled*.
   - What arrived = what was ordered **unless an issue says otherwise.** That's the trick that removes double entry.
3. **Issues (both sides):** Missing · Short · Damaged · Wrong item · Extra, with item, qty, job, note and an optional photo.
   - **Statuses:** Open → Reordered (new PO#) → Archived. They archive automatically when the replacement arrives, or by hand ("credit taken", "not needed").
   - **Raised anywhere:** at receiving, at the door machine, or on the floor.
4. **Stock (only where it's worth it):** hardware spots (Rack D L1 a/b, Rack 1, Supplies, office racks) and board bunk slots. On hand = put away − taken. Doors and cabinets are not stocked (see §7).

## 3b. Quantities: totals, stacks, pallets and boxes (from your answers)
**The problem you spotted:** the Excel says *100 boards* or *300 cardboard*, but the truck brings **stacks of 40 + 40 + 20** or **6 pallets**, and hardware comes on **mixed pallets** (about 50 boxes of about 10 item numbers each). If the app asks "put 100 here", it's asking for something that doesn't exist on the floor.

**The rule: the Excel total is the target, never an instruction.** The app checks what you put away against it, in the units you can actually see.

**1. Two steps, not one**

| Step | When | What you enter |
|---|---|---|
| **Arrived** (dock) | When the truck is unloaded | Nothing, if it's all there: **"All here"**, plus problems if any. Optional: number of pallets/stacks. |
| **Put away** (the real count) | Right away or the next day (you said sometimes a day later) | Each **stack, pallet or box group** as you place it. The app adds them up against the order. |

Until something is put away, it shows on the office board as **"On the dock: 3 of 10 hardware items not put away yet"**. Nothing gets lost between the two steps.

**2. Boards and cardboard: each stack or pallet is its own unit**
- Put away one stack at a time: *Stack 1: 40 → BK4-1*, *Stack 2: 40 → BK4-1*, *Stack 3: 20 → BK4-2*. A running tally shows **100 of 100 ✓**.
- A bunk slot holds several stacks (up to 5 high). Each stack keeps its own count, so a whole stack can be pulled later, or part of one sent to the saw.
- Cardboard works the same way: 6 pallets = 6 units, each with its own count, on Supplies' top level.
- If the paper says per-stack counts, type those. If it only gives a total, the app splits it evenly as a starting point, and you correct any stack that's different.

**3. Hardware: down-stack a mixed pallet by item**
- Open the delivery → **Put away**. You see only the item numbers on *that* order, as big buttons with the description and the ordered total.
- Tap the item → enter **boxes** → the app does the math (*10 boxes × 20 = 200*) → type the spot → done. Repeat as boxes come off the pallet.
- Each item shows **put away / ordered**, e.g. *Hinges 180 / 200*. Finish with any item short and the app asks: *"20 hinges short: report missing?"* One tap makes the issue for Stephen.
- **Per-box amount is set once per item** (you said it's always the same). The first time an item arrives without it, the app asks "How many per box?" and remembers.

**4. When the box number isn't the Excel number**
You said item numbers vary between the boxes and the Excel. So at put-away you **pick from the order's list** (description + number), rather than typing whatever's on the box. If a box's number differs, you can save it as a **second name** for that item, so search and future deliveries recognize it.

**5. The Excel stays simple**
One total per item per PO, the way it's written today. Where a line is in boxes or pallets instead of pieces, the item's setting says what the Excel counts in ("Excel counts: pieces / boxes / pallets"). It's set once per item, by the office.

**Answered (Oct 28)**
- **Board paperwork shows only the total, but each stack has its own slip** with its quantity and color. → At put-away you type each stack's number from its slip. The app checks the stacks add up to the paperwork total.
- **To the saw:** up to **28 sheets at a time**. The **beam saw computer already tracks what's cut.** Single sheets also get pulled for remakes at random times. → Two board actions:
  - **To saw:** sheets from a stack, max 28 per pull.
  - **Take sheet(s):** reason Remake, Job # optional.
  The stack's count drops either way.
- **Backorder on the slip = Backorder.** It shows to Stephen as *Backorder* (no reorder needed, still expected), separate from *Missing*.
- **Extra arrives:** keep it. It's flagged *Extra* on the office board, and Stephen decides what happens to it.
- **Per-box amounts:** a fixed number per item number, set once on the item and applied automatically every time that item arrives or is pulled.

**Still open on quantities**
- F. Can the **beam saw computer export** what it cut (a daily report or file)? If yes, the app can take board usage straight from the saw. Nobody would type cuts twice, and the counts would stay right.

## 4. Excel stays the office's tool: live, no uploads
This is the make-or-break piece. The app can follow the sheet live only if the sheet lives somewhere the app can read online:

| Where the Excel lives | Live? | How |
|---|---|---|
| **Google Sheets** | ✅ Yes | The app reads it through your Google Drive connection every ~2 minutes while it's open. One office screen keeps it fresh for everyone. Hourly backup check from a scheduled task. |
| **OneDrive / SharePoint (Excel online)** | ✅ Likely | The same approach through a Microsoft connection, if your Claude plan has the Microsoft 365 connector. To verify. |
| **A file saved on a desktop PC / emailed around** | ❌ No | Nothing online to read. It would need an upload each time, which is what you don't want. |

**What the sheet needs (I'll provide a template):**
- One **Orders** tab with fixed columns: PO# · Vendor · Item # · Description · Type · Qty · Unit · Expected date · Status · Job · Note.
- **One row per item per PO.** Status uses one of: Ordered, Delayed, Cancelled.
- The app shows a warning row for anything it can't read ("Row 14: no quantity"), instead of guessing.

The app does **not** write into the Excel at first. Shop results live in the app and show on the Office board. Later, if wanted, a "Received" column can be filled automatically.

## 5. Screens (organized by who's holding the device)
**Shop (tablet):**
1. **Today:** cards per delivery: *Expected today · Late · Delayed · Arrived*. Big type, vendor + what's on it.
2. **Delivery:** the line list, then two buttons:
   - **All here, all good**
   - **Something's wrong** (pick the line → what → qty → note → photo)
3. **Put away:** what's waiting, with the right spot suggested.
   - Boards: bunk slots only, enforcing your white / colored / 6 mm rules.
   - Hardware: its own spot.
   - Typed spot or big buttons.
4. **Report a problem:** one screen with 4 fields (item, qty, job, why). Also pinned as a station screen at the door machine.
5. **Find:** on hand and where, for hardware and boards (map as the "show me" assist).

**Office (computer, wide layout):**
1. **Board:** today's deliveries and their state, issues needing action (oldest first, aging in red after 2 days), and what's late.
2. **Reorder queue:** open issues + low hardware. Each has **Reordered (PO#)** → waiting → archived.
3. **Orders check:** per PO: ordered · arrived · outstanding · issues. This is the "numbers match" view.
4. **Low stock:** hardware only. It subtracts what's on order, so nothing gets ordered twice.

## 6. What Scott and Nathan would call useless, so it's cut or changed
| Feature today | Verdict | Change |
|---|---|---|
| Line-by-line quantity entry at check-in | **Duplicate of the paper** (your point) | Replaced by **"All here, all good"** + exceptions only. |
| "Slip given to office" / "Office has it" switches | Paper goes to the office regardless | **Removed.** |
| Daily report screen | Nobody will open it | Folded into the Office board. |
| Inventory value ($) | Needs costs nobody maintains | Hidden until costs exist. |
| Counting screws, nails, cardboard by the piece | Costs more time than it saves | Tracked as **OK / Low** with one tap, not counts. |
| Pick lists, saw lists, ship lists, return-to-vendor flows | Not how the shop works | **Removed.** Only "Take for job" for hardware and "Report a problem". |
| 3D map as a tab | Impressive, not daily | Stays only as "show me where" from Find. |
| Roles and logins per person | Friction | Two modes: **Shop** and **Office**. One shared login per tablet is fine. |
| Labels on every spot, day one | Big setup cost | Rack D and the bunks only, at first. |

## 7. What will mess us up (and the guardrail)
1. **The Excel changes shape:** a moved column, merged cells, or a new tab per vendor breaks the sync. → A fixed template, plus a validation banner that names the bad row. The app matches on PO# + Item #, never on row number.
2. **Item numbers missing or inconsistent:** vendors describe the same item differently. → The Item # column is required. Unmatched lines still show, but they're marked "new item".
3. **Units don't match:** ordered in cases, received as pieces. → Each line carries its own unit. The app never converts on its own.
4. **Who sets which status:** office and shop both change status and contradict each other. → The office owns *Ordered / Delayed / Cancelled* in Excel. The shop owns *Arrived / Issues* in the app. *Late* is automatic.
5. **Issues raised but never closed:** the reorder gets lost. → An owner (Stephen), aging alerts, and auto-archive when the replacement PO line arrives.
6. **Pulls not logged:** hardware counts drift and the numbers stop being trusted. → Hardware only, logged at Rack D. A 15-minute monthly count of Rack D. Everything else is OK/Low.
7. **The doors team doesn't use it:** they're a different team at a machine. → One pinned station screen with 4 fields. No login, no menus.
8. **Partial deliveries across days:** what arrives 6 of 10 now and the rest Thursday stays open for the rest. Only the missing 4 stay expected.
9. **Double entry creeps back:** if Stephen also keeps "received" columns in Excel, the work doubles. → Rule: Excel = what we ordered; app = what happened.
10. **Connectivity / logins:** every tablet must be signed in to Claude. → Shared accounts per tablet, decided before rollout.

## 8. Look: Force Cabinets brand
- **Taken from the logo:** charcoal **#303032** on white, and a heavy slab-serif "FORCE" wordmark.
- **The app uses:**
  - Charcoal primary buttons and headings, in a slab serif.
  - Clean white and light-gray surfaces. The Liquid Glass style is kept, but neutral.
  - Color **only for state**: green = arrived OK, amber = late / delayed, red = issue. Nothing decorative competes with those three.
- **Office board:** a wide desktop layout.
- **Shop screens:** extra-large tap targets for gloves.

## 9. Done when (the test I'll run after building)
I replay your exact day as an automated test:
1. **6:10:** 4 deliveries show on Today.
2. **Boards:** "All good" → put away only into bunk slots → the office sees ✓ complete.
3. **Hardware:** 1 strap missing reported with a note → the office sees ⚠ + an issue.
4. **Cardboard:** the Excel status changes to Delayed → the app shows Delayed with no upload.
5. **Doors:** 12/12 pallets → the station reports −1 vanity 45 sink base door, scratched → the queue → Reordered (PO#) → auto-archived when it arrives.
6. **Orders check:** ordered vs arrived vs outstanding matches for every PO.

All at tablet and desktop sizes, light and dark, zero errors.

## Questions for you
1. **Where does the order Excel live today?** On a desktop PC, in OneDrive/SharePoint, in Google Sheets, or emailed around? This decides whether live sync is possible.
2. **Can the office keep one master Orders tab** with the fixed columns above? Who types *Delayed*: Stephen only, or Roman too?
3. **Doors:**
   - Where are door pallets stored?
   - Does the app need to know which door pallet sits where, or only check counts at arrival and take problem reports from the machine?
4. **Brand:** is charcoal/white from the logo right, or is there a brand color or guide I should use?
5. **Office device:** do Stephen and Roman work on a desktop browser? Do they have Claude logins?
6. **Who closes issues?** Stephen only, or anyone in the office?
7. **Cardboard, strap, foam:** track as *OK/Low* only, or by count?
8. **Excel write-back:** should received quantities ever go back into the Excel? My recommendation: not at first.
