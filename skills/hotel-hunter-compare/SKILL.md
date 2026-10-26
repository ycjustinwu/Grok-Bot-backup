---
name: hotel-hunter-compare
description: >-
  Use this after hotel-hunter-intake to browser-compare OTAs and write shortlist
  MD plus OUT handoff.
---
# hotel-hunter-compare

Browser hunt only. No OTA MCP. **Compare named targets from intake**, not open-ended search dumps. Score price, quality, itinerary fit, availability, convenience.

## Channel rules
- **Japan:** **樂天 Travel first**. Then Hotels.com, Booking.com, official for top 2–3. **Agoda banned for Japan.** If 樂天 blocked, mark N/A reason; never substitute Agoda.
- **Non-Japan Asia:** Hotels.com, Agoda, Booking.com; official for top 2–3.
- Long-stay or airbnb_ok: accommodation-booking + site-playbooks-airbnb. Non-long-stay: do not hard-scan Airbnb.

## Steps
1. Load intake. Same dates, party, room band, budget band. **Work TARGETS[] first** (deep-link each property across channels).
2. Only if targets are sold out / out of budget: widen one step (adjacent area or one alternate from same KOL list), then stop and report.
3. Quote tax-inclusive totals (HKD≈ + original currency) plus cancel deadline.
4. Write `/workspace/hotel-hunter/output/{city}-{YYYYMMDD}-HKT.md` and `handoff/OUT-*.md`.
5. Chat table plus one primary and one backup with real deep links. Widget before book.

## VERIFY
- Japan: 樂天 present or N/A reason; Agoda absent by policy
- Rows map to intake targets (or documented widen)
- Stay totals not nightly-only; cancel deadline present
- No fabricated inventory or URLs; no aimless first-page scrapes as the deliverable
- Handoff four fleet fields filled
