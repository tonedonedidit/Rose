# Force Receiving: how each side uses it, what's missing, what would help

Written Oct 29 after Tony and Roman tried the app in the office. It covers the build at force-receiving.netlify.app.

## How the app gets used today

| Who | Does every day | Does sometimes | Rarely or never |
|---|---|---|---|
| **Warehouse** (fcwarehouse) | Check in deliveries, put away, take for a job, send boards to the saw | Pallets, count a spot, move stock, report a problem | Activity, Find by spot code |
| **Office** (fcadmin) | Dashboard, Issues, import the order Excel | Stock edits, exports, Find with the map | Today (the warehouse's screen) |

**The weak spot:** the app only knows what people type into it. Each step someone skips (a pull not logged, a pallet built without the app) moves the numbers further from the floor. Every improvement below is judged by one question: does it make logging faster than skipping it?

## Warehouse: what's missing or slow

1. **Pallets (built today).** Make a pallet, add items by boxes, edit, move, rename, print a QR label, and delete. Putting away to a spot that has a pallet loads the pallet.
   - *Still open:* are cabinet pallets (the old Force Inventory stickers) in scope again, or hardware only?
2. **Pulls aren't logged when people are busy.** "Take for job" takes 4 taps.
   - *Proposal:* scan the spot or pallet QR, and the app jumps straight to "Take how many?" with the last job # filled in. That's 2 taps.
3. **Labels.** Spots have no printed labels yet, so scanning only works for pallets.
   - *Proposal:* a "Print spot labels" sheet for Rack D, Supplies, Rack 1 and the office racks, 30 per page.
4. **Counting.** There's no route that walks a person spot by spot.
   - *Proposal:* "Count Rack D". It goes spot by spot, shows the expected number, and takes OK or a new number. About 15 minutes a month.
5. **Board stacks.** Saw pulls are logged by hand while the beam saw tracks the same cuts.
   - *Needs:* one sample of the saw's export. Then programmed cuts come from the saw, and people only log custom cuts and remakes.
6. **Glove use.** Tap targets are 52–60 px.
   - *Proposal:* a "big buttons" setting per device for tablets on the floor.
7. **No signal in a corner of the warehouse.** Right now a save fails and shows an error.
   - *Proposal:* queue the save and send it when the signal comes back.

## Office: what's missing or slow

1. **Excel import is guesswork until we see Stephen's real file.** Every column is kept now, but the app still guesses which column is the quantity, the PO and the date.
   - *Needs:* the real order file, so the import is exact on the first try.
2. **Live Excel sync.** Today Stephen drags the file in by hand.
   - *Proposal:* a small "Force Sync" program on the computer that holds the file. It sends changes on every save.
   - *Needs:* IT to allow installing a program, or the file moved to OneDrive or Google Sheets.
3. **Reorder screen.** Low stock shows on the Dashboard, but there's no "make a reorder list by vendor" button like the old build had.
   - *Proposal:* bring it back, with the export going to Excel.
4. **Issue follow-up.** Issues show their age, but nobody gets notified.
   - *Proposal:* a morning email to Stephen listing open issues older than 2 days and late deliveries.
5. **Boards cut per day** (built today). Counts sheets per saw, plus custom cuts and remakes, for the last 7 days.
   - *Proposal:* add "boards received" next to it, so in and out show side by side, and a per-color breakdown.
6. **3D map** (built today, office only, in Find). Matches light up green, "Map" on a result flies to it, and tapping a spot opens it.
   - *Still open:* the doors area's real position. It's drawn across from Rack D as a guess.
7. **One shared office login.** The log shows the name typed on the device, not a verified person.
   - *Fine for now.* Separate logins can come later if it matters.

## Quality of life, both sides

- **The screen no longer jumps while typing** (fixed today). Live updates used to throw away what you were typing in Find.
- **Toasts cover the bottom row** on a phone for 3 seconds. *Proposal:* shorten them and lift them above the tab bar.
- **Undo** for the last action (put away, take, count) for 10 seconds. That's cheaper than fixing it later.
- **Dark mode on the floor tablets** is easier on the eyes and the battery. It already works and follows the device setting.

## Questions to settle (bring to Stephen and Roman)

1. Can you send the real order Excel, and one beam saw export file?
2. How many saws report output? The app has "Beam saw" now; office can add more under More → Saws.
3. Cabinet pallets: back in scope, or hardware only?
4. How many door pallet spots are there, and where exactly (the map has 12 across from Rack D)?
5. Can a small program be installed on the computer that holds the Excel?
6. Who gets the morning issues email?
7. Should taking stock require a job #, or stay optional for supplies?

## Recommended next build, in order

1. Import tuned to the real Excel (needs the file).
2. Scan-to-take plus spot labels (fastest win for accurate counts).
3. Reorder list by vendor.
4. Saw export import (needs a sample).
5. Count Rack D walk.
6. Morning email.
7. Offline save queue.
