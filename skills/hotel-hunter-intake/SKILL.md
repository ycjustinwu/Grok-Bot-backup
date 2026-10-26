---
name: hotel-hunter-intake
description: >-
  Use this when starting a hotel-hunter stay search to lock family hard fields
  before any OTA hunt.
---
# hotel-hunter-intake

Lock stay inputs before compare. Refuse full shortlist if city or dates unlocked. **Do not open OTA compare until targets exist.**

## Steps
1. Read chat and/or `/workspace/hotel-hunter/handoff/IN-*.md`.
2. Require before any OTA hunt:
   - city + **area** (or preference axis: 方便 / 新落成 / 豪華)
   - check-in/out with weekday
   - rooms/type
   - **budget target** (per night or stay total, currency)
   - hard filters, airbnb_ok
3. **Target seeding (mandatory before compare):**
   - Ask Justin for hotels he has stayed at (any city) to infer preference, **or**
   - Research KOL / travel-blog / family-Japan shortlists for that city+area (Tavily/web; cite sources)
   - Produce a named **target list** (3–8 properties) with why each fits; write into intake draft
   - Only then hand off to hotel-hunter-compare for those names (+ 1 widen step if sold out)
4. State defaults aloud if used: 2 adults + children 9 and 12; prefer free cancel; no hostel.
5. If itinerary not locked or multi-city replan needed, escalate to travel planner and stop.
6. Write `/workspace/hotel-hunter/draft/intake-{YYYYMMDD-HHMM}-HKT.md` with PINNED_INPUTS including preference, budget, and **TARGETS[]**.

## VERIFY
- Required fields present (budget + area/preference + targets) or ask recorded
- No blind OTA browse without targets
- Party and dates match IN file when provided
- No OTA prices invented at this step
