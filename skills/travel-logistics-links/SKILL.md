---
name: Travel Logistics Links
description: >-
  Use this when adding flights or ground logistics to a trip plan — reliable
  Google flight search links (never dated deep-links), Maps links, and live
  checks for hours/strikes.
---
# Travel Logistics Links

Build reliable logistics for flights and ground movement. **No dead deep-links.**

## Flight logic

If a leg is **>400 km** or requires crossing water, evaluate flying.

For each flight option state:
- Duration (e.g. `1h 50m`)
- Carrier note (reliable vs low-cost)
- **Search link only** — never invent dated booking URLs with complex params

**Forced flight URL format:**
`https://www.google.com/search?q=flights+from+[Origin]+to+[Dest]`

## Maps / ground

- Maps: `https://www.google.com/maps/search/?api=1&query=[Location Name]`
- Self-drive: MapCode / parking tip when relevant
- Transit: line + exit when relevant

## Search first

Live-check fares ballpark, hours, strikes, and closures via web before locking a day. Mark uncertainty if search fails.
