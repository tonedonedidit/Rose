# Hardware build (active app)

**Purpose:** track hardware on hand and connect warehouse receiving with office purchasing, so the numbers match what was ordered and nothing gets ordered just to order.

**Locations in scope:**
- Rack D (level 1, front spots a and b)
- Supplies (Rack 0)
- Rack 1 (handles)
- Office racks 1 and 2 (misc supplies next to the office)

Bunks and cantilevers stay in the app (Boards tab) but aren't being worked on yet. **Cabinet pallets (Aisles A, B, C) are removed;** the full build is saved in `../full-app-build/`.

**Bottom bar:** Home · Hardware · Incoming · Boards · Office (More for floor users).

**The loop it closes:**
1. **Office imports or makes a PO.** Each part shows as "coming".
2. **The floor checks the delivery in** with what actually came. Anything short stays on backorder; damaged or wrong items are flagged for the office.
3. **Put away.** The app suggests the part's own spot and adds the stock to the hardware pallet there.
4. **Grab parts for jobs.** Usage is logged per job number.
5. **Office:**
   - **Today:** what arrived, slips, backorders.
   - **Reorder:** reorder point minus what's on hand minus what's already coming.
   - **Usage by job.**
   - **Value.**

**Tested (Oct 28):** 30/30 hardware checks plus the office/receiving suite, light and dark, zero errors.
