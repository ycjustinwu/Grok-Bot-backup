---
name: hotel-hunter-book
description: Use this when Justin confirms a primary hotel — fill the form after yes and stop before charge for a second confirm.
---
# hotel-hunter-book

Irreversible path. Never auto-pay.

## Steps
1. Require explicit yes naming property, dates with weekday, party, total, cancel terms.
2. Open chosen listing in browser; prefill guest details Justin gave.
3. Stop at payment UI. Re-confirm total and cancel with Justin.
4. Only after second yes complete payment if asked; otherwise leave form for him.
5. On success update OUT handoff booking_status and conf_code if visible. Never invent codes.
6. v1: no fake email confirmations; no price-drop watches.

## VERIFY
- First yes and second pre-charge confirm both recorded
- Charge matches last quote or delta explained
- No book without yes
