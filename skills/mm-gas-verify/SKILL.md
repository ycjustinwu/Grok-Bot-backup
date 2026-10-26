---
name: mm-gas-verify
description: Use before delivering a Market Master Apps Script patch — menu redraw checklist, OAuth/scopes notes, and harness VERIFY.
---

# mm-gas-verify

## ONE JOB
Gate delivery of a Market Master GAS patch.

## Checklist
1. Files under `/workspace/market-master/apps-script/patches/<stamp>/` exist; paths listed in chat.
2. CHANGELOG lists **which functions** changed and **menu / trigger** to re-draw (e.g. upgrade / rebuild Charts / runEvening path — as in project).
3. OAuth / script scopes: note if new `SpreadsheetApp` / Drive / UrlFetch scopes appear; warn Justin before authorize.
4. Permission: friend demo may need share; live project edits need Justin paste or clasp/editor access — bot does not silently escalate privileges.
5. Smoke plan for Justin: open Market Master → run named menu → confirm labels not crushed by axis/series on target charts (breadth first).
6. Harness: ONE_JOB held; ANTI_JOBS held; no fabricate of missing `.gs`.

## Delivery shape (chat)
結論先行 → patch 目錄 path → 改咗邊啲 function → 點喺 menu 重繪 → OAuth 注意 → Justin 下一步（缺檔／開 share／先修邊張圖）.

## WV
Coding bot: **not** default Work Verifier pool unless Justin / 總指揮 / Jev `needs_wv` says so.

## VERIFY
- [ ] All above bullets answered or N/A with reason
- [ ] PINNED_INPUTS / DECISIONS_MADE / OPEN_QUESTIONS / NEXT_GATE on handoff OUT
