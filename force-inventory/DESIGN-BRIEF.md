# Force Gilbert Inventory: redesign brief

## The job
Make the app something you'd hand a boss, a new installer, or an office buyer without a walkthrough, on an **iPhone, on the go**. It should feel like a native iOS app, not a desktop web page. Every screen should answer one question: **what do you want to do?** Facts appear only after someone taps to see them.

## Who uses it
| Person | Where | Wants |
|---|---|---|
| Installer | At Rack D, phone in one hand | Grab parts for a job in under 15 seconds |
| Floor lead | Dock, racks, bunks | Check in deliveries, put them away, count spots |
| Office (Scott, Nathan) | Desk or phone | Load POs, see what arrived, get the paperwork, reorder |
| Boss | Anywhere | Trust the numbers at a glance |

## iOS feel
- Use the system font (SF on iPhone), large titles, and inset grouped lists with chevrons. Follow light or dark mode automatically.
- A bottom tab bar with 5 tabs: Home · Map · Incoming · Outgoing · Count. The ☰ button opens a dropdown menu for everything else.
- **Bottom sheets** with a grabber handle for every quick action. The sheet slides up over the screen, and you swipe down or tap outside to close it.
- Native pickers: dropdowns open the iOS wheel. Choosing a spot is two wheels (Area, then Spot), with no typing needed.
- **Steppers** for quantities: big − and + buttons around a number. A segmented control switches between **Boxes** and **Pieces**, and the total shows under it.
- Tap targets of 44 pt or more, primary buttons of 50 pt, and the thumb zone at the bottom.

## Principles
1. **Buttons first, facts second.** A screen opens with its actions. Lists and history sit behind a tap.
2. **One job per sheet.** Add, Take, Move and Count each get one sheet: item, quantity, one big Done button.
3. **Same four verbs everywhere.** Whether you start from a spot, an item or the map, you get **Add · Take · Move · Count**.
4. **Fewer words.** Labels are 1 to 3 words. No paragraphs; hints are one muted line at most.
5. **Calm visuals.** One green tint for actions. Status uses small colored dots and chips. Spacing follows an 8 pt grid.

## 3D map: soft and real
- **Soft to drive:**
  - Smooth damped orbit, gentle rotate and zoom speeds, and the camera can't leave the building.
  - Zone chips across the top fly you anywhere in one tap. Double-tapping the floor glides you there.
  - A Home button returns to the aerial view.
  - Tapping a spot glides to a straight-on view and opens its sheet.
- **Real:**
  - Polished concrete floor with control joints, yellow floor tape along aisles, and full-height tilt-up concrete walls with roll-up dock doors.
  - The office has windows, and the dividing wall has its opening.
  - Walls are cut away on the camera side, so you can see in like a dollhouse while it still feels like standing inside.
  - Soft contact shadows, bright interior lighting, and plastic pallets with real slats.

## Scanning
Cabinet pallets already have QR codes, and hardware doesn't yet. Search accepts anything a scanner types, whether a cabinet QR or a spot code. The spot labels (QR) are ready as the start of a hardware QR system when the shop wants it.

## Screens
- **Home:** A search bar, then a 2-column grid of action tiles: Receive, Put away, Grab parts, Pick lists, Count, Map. Then an Alerts row with a number.
- **Spot sheet:** Spot code, a big quantity ("50 boxes", with "1,000 pcs" under it), the item name, and four buttons: Add · Take · Move · Count. Details sit behind a Details row.
- **Item sheet:** Name, total on hand, on order, and where it is (tap a row to go there). Plus the same four verbs and an Edit button.
- **Incoming:** New PO and Import buttons, an Expected / Put away / Done control, and a list. The PO screen shows step dots, items, two paperwork switches, and one big next-step button.
- **Outgoing:** Grab parts and New pick list buttons, an Open / Done control, and a list.
- **Count:** An Area picker, a progress ring, and a Start counting button. That opens the count sheet and moves to the next spot automatically.

## Done when
- From Home, D-11-c is 2 taps away (search → result) and shows 50 boxes / 1,000 pcs with Add · Take · Move · Count.
- An installer can grab parts in 4 taps plus typing the job number.
- Nothing needs typing a spot code; everything has a picker.
- It works at 390 pt with no sideways scroll, in light and dark mode, with zero console errors.
