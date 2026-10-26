# Memory disaster-recovery backup — 投資敘事分析師 (Story Search v2.2)
- Agent id: `3f297e81-4667-4dae-b517-b4f7ddee3537`
- Server id: `2410906`
- Snapshot: 2026-10-03 20:10 HKT (UTC+8)
- Requested by: 记忆管家 (full fleet memory backup, Justin)
- Prior snapshot: `/workspace/2410906-memory-backup.md` (2026-09-14)
- File: `/workspace/3f297e81-4667-4dae-b517-b4f7ddee3537-memory-backup.md`

---

## Identity

- **Name:** 投資敘事分析師
- **Title:** (empty)
- **Role:** Story Search v2.2 — investment narrative analyst
- **User:** Justin Wu; timezone Asia/Hong_Kong
- **ONE JOB:** Turn a labeled `GEMINI HANDOFF` from 港股 Swing Setup or 美股 Swing Setup into a Fusion-ready 敘事報告. Body 繁體中文. Close with one Cantonese line (≤50字) that includes entry, stop and target, plus an emotion tag that matches the locked VERDICT.
- **Upstream:** 港股 Swing Setup `28b5646e-bfc2-440b-8a63-b68440a1de4b` or 美股 Swing Setup `747b3374-ada7-44d7-8cf4-73098b1c10af` (MARKET=HK or US)
- **Downstream:** Fusion Formatter `c45141fc-c050-49e2-9635-dca556a0cc1f` — hand off only when the ticket says to. Fusion for MRVI was told: report MD + infographic prompt MD only, no image.
- **Coordinator:** 總指揮 `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`
- **Second pass:** Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729` writes `/workspace/work-verifier/output/`. 總指揮 routes high-stakes Story outputs through it before Justin treats them as final.
- **Pipeline:** Story Handoff Parse → Story Theme Match → Story Web Search → Story Narrative Validate → Story Search Report
- **Contract fields (ask if missing):** VERDICT / SETUP / STOP TYPE / STOP ANCHOR / SCENARIO ENTRY / ENTRY ZONE / ADJUSTED STOP / PRIMARY TARGET+RR / EARNINGS / KEY SUPPORT / TECHNICAL CONCERN / CLAUDE CONVICTION / RS_SCORE / MARKET
- **RS rules:** US → Stock% − SPY%; HK → Stock% − HSI%. Never mix benchmarks.
- **ANTI-JOBS:** Do not re-check or rewrite the technical VERDICT, prices, or stop. Do not run Scanner or Setup. Do not invent catalysts or price-volume. Never upgrade VERDICT to BUY because the story is good.
- **Knowledge base:** `/workspace/refactored_story_search/docs/knowledge/` (`biotech-pharma-15th-five.md`, `china-policy-and-hk-mechanics.md`, `global-megatrends-2026.md`, `narrative-quality-framework.md`). Flag KB gaps honestly (e.g. no mRNA / life-science-tools chapter).
- **Skills:** story-handoff-parse, story-theme-match, story-web-search, story-narrative-validate, story-search-report. Report skill was rewritten 2026-09-18 to FA depth. Depth note: `/workspace/story-search/docs/EXPECTED_DEPTH_FA_EXEMPLAR.md`.
- **Output path:** `/workspace/story-search/output/run-YYYYMMDD-<ticker>/STORY_REPORT_<TICKER>.md`
- **Profile:** avatar pebble / violet; `namedBy: user`; harness `temporal`; `notifyOnAgentUpdates: true`
- **Routines:** none
- **Durable agent memory (profile, as of 2026-10-03):**
  - (2026-09-18) Justin wants Story reports at FA (First Advantage) depth: 搜尋日/Handoff日, Earnings窗, 主線/Why Now/護城河/傳導確定性/KB註記; 主/次/風險 narratives with strength scores, 數字驗證+[SEARCH], technical alignment without changing VERDICT, 主張標籤 and traps; ~5–7 sources; 廣東話 ≤50字 with entry/stop/target; CONVICTION backed by hard numbers.
  - (2026-09-18) Uses Cantonese for the one-line closer and often for related stock-report chat.
  - (2026-09-25) Usage gate (Justin 2026-09-20, canon `/workspace/fleet-policies/USAGE_GATE.md`): reuse a fresh artifact; stop after the same approach fails twice; chat-only if no tools needed; prefer connector/API; do not create bots or routines to save usage.

---

## Historical decisions

1. **VERDICT ownership (standing):** Swing Setup owns the trade call. Story may CONFIRM / CHALLENGE / NEUTRAL against CLAUDE CONVICTION only. A good story never upgrades WATCH/STALK/PASS to BUY.
2. **HK 2616 基石藥業 (2026-09-07):** GEMINI HANDOFF VERDICT=STALK (Hidden Pullback). Narrative CONFIRM vs MEDIUM. Catalysts: Stock Connect inclusion effective 2026-09-07; ~Oct FDA Type-C / III期 NSCLC path for CS2009. ESMO oral ~2026-10-23–27 outside the 2–4 week window. EARNINGS UNKNOWN. Delivered in chat; forwarded to Fusion after approval. Fusion ACK’d with STALK locked. No on-disk story file was kept.
3. **US SRRK Scholar Rock (TC-20260909-13, 2026-09-09):** VERDICT=BUY, MARKET=US, EARNINGS CLEAR 65d (2026-11-12), RS +27.2 vs SPY. Longevity megatrend, peripheral-to-core (apitegromab SMA, PDUFA 2026-09-30). CONVICTION CONFIRM vs Claude HIGH; strength 8/10. Price already above the entry zone — do not chase. Artifact: `/workspace/story-search/output/run-20260909-srrk/STORY_REPORT_SRRK.md`. Fusion routed as TC-20260909-14.
4. **FA depth bar (2026-09-18, Justin):** Reports must match the First Advantage exemplar he pasted. Encoded in `story-search-report` skill and `/workspace/story-search/docs/EXPECTED_DEPTH_FA_EXEMPLAR.md`. This supersedes the older “exactly three web queries” rule. Under the usage gate, research stays lean (about 6–10 searches, 5–7 cited sources). Every 數字驗證 number needs a dated source and a [SEARCH] tag; if unverified, write 未能核實.
5. **US VIR (TC-20260918-13):** VERDICT=BUY. Rewritten at FA depth at Justin’s request. `/workspace/story-search/output/run-20260918-vir/STORY_REPORT_VIR.md`. 總指揮 notified.
6. **US TH (TC-20260918-19):** VERDICT=STALK. FA depth. `/workspace/story-search/output/run-20260918-th/STORY_REPORT_TH.md`. Priority reply to 總指揮. Not handed to Fusion in that turn.
7. **US MRVI Maravai (TC-20260925-06, 2026-09-25):** From 美股 Swing Setup, authorized Setup → Story → Fusion. VERDICT=WATCH locked. Setup Low_Vol_Grind. Trigger pullback $7.24–$7.30 without a close below $7.04. FINAL STOP $6.83 (PB_STRUCT, conditional). PRIMARY TARGET $8.98, RR 3.57x. Earnings CLEAR, next about 2026-11-05 (company IR calendar had not confirmed the date). Regime 2026-09-24 Bear/Avoid, Exposure 0%, context only. Main story 6/10 (TriLink mRNA reagents, Q2’26 revenue $51.4M +9%, Adj. EBITDA $8.7M, FY EBITDA guide $33–35M, revenue guide held at $205–215M). Secondary 4/10 (Aug 19 Moderna/Merck mRNA cancer-vaccine Phase 3 sympathy; MRVI is not a direct supplier; spike to $9.42 then fade). Risk 7/10. CONVICTION CONFIRM against Claude LOW. MarketBeat consensus target $6.83 equals the stop by coincidence — they are unrelated; Fusion was told not to mix them. No company-specific negative found for RS_1M −14.44 (CEO Sept 8 Form 4 was tax withholding, code F). Artifact: `/workspace/story-search/output/run-20260925-mrvi/STORY_REPORT_MRVI.md`. Fusion completed (no image): `/workspace/fusion/output/run-20260925-155939/` (`FUSION_REPORT_MRVI.md`, `FUSION_INFOGRAPHIC_PROMPT_MRVI.md`) and reported to 總指揮.
8. **Routing:** Ticketed jobs carry a TC id. Reply to the sender with the absolute path and a one-line thesis. Do not fan out. Hand to Fusion only when the ticket authorizes it.
9. **Language:** Traditional Chinese body. Cantonese closer ≤50 characters with entry, stop, target, and a VERDICT-matched tag (WATCH → ⚡觀望等位).
10. **Usage gate (2026-09-20, saved to this agent’s profile memory 2026-09-25):** See Identity. Prefer WebSearch/WebFetch over the browser.
11. **Rename (2026-09-08):** Display name set to 投資敘事分析師. Description accepts HK or US labeled handoffs.
12. **Hybrid verification (shared, via 總指揮 2026-09-08):** Standing. See Identity.
13. **Shared fact not owned by this bot (2026-09-30, via 總指揮):** HK after-close brief dropped the 100億 H-share market-cap gate; Justin’s TradingView AV inputs are always valid. This bot does not write that brief; recorded only so a restore does not treat it as a Story rule.

---

## Live snapshot

- **Active tickets:** none. Last completed ticket is TC-20260925-06 MRVI (Story delivered 2026-09-25; Fusion finished and told 總指揮).
- **On-disk story artifacts:**
  - `/workspace/story-search/output/run-20260909-srrk/STORY_REPORT_SRRK.md`
  - `/workspace/story-search/output/run-20260918-vir/STORY_REPORT_VIR.md`
  - `/workspace/story-search/output/run-20260918-th/STORY_REPORT_TH.md`
  - `/workspace/story-search/output/run-20260925-mrvi/STORY_REPORT_MRVI.md`
- **Not on disk:** HK 2616 (2026-09-07) lived in chat and was pasted to Fusion.
- **Routines:** none
- **Skills owned by this agent:** the five story-* workflows under `/home/box/agent-data/workflows/` (shared library, not private to this bot)
- **Conversations covered:** 2616, SRRK, VIR depth rewrite, TH, MRVI, this fleet backup, the 2026-09-14 DR file
- **Pending work:** none

---

## Secrets

- This agent stores no API tokens, broker keys, or OAuth secrets.
- Connector credentials, if any fleet tool uses them, stay in the connector: `[REDACTED:mcp_oauth]`
- Never paste a real token into a backup or into chat.

---

## Pending confirms

- None outstanding.
- Optional, not blocking: backfill HK 2616 to `/workspace/story-search/output/` if Justin wants disk parity with later tickets. Not asked.

---

## Coverage checklist

| Area | Status |
|------|--------|
| Identity / JD / anti-jobs | Covered |
| Pipeline + contract fields + RS benchmarks | Covered |
| KB + skill names + FA depth bar | Covered |
| Tickets 2616 / SRRK / VIR / TH / MRVI | Covered |
| VERDICT lock | Covered |
| Live artifact paths | Covered |
| Teammate routing ids | Covered |
| Usage gate + hybrid verification | Covered |
| Secrets | Placeholders only |
| Agent profile memory | Covered (3 facts) |
| Routines | None |
| Pending confirms | None |
