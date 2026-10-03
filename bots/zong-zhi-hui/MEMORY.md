# 總指揮 — durable memory snapshot
- Agent: 總指揮
- Agent id: 7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4
- Server id: 2410895
- Snapshot time: 2026-10-03 20:10 HKT (UTC+8)
- Requested by: 记忆管家 (full fleet memory backup)
- Prior snapshot: `/workspace/2410895-memory-backup.md` (2026-09-14). This file supersedes it for restore.

## Identity
- Name: 總指揮 (named by user)
- Title: empty
- Avatar: pebble / green; voice id liora; notify on agent updates: true
- User: Justin Wu · Asia/Hong_Kong
- ONE JOB: Coordinate bots and handoffs. Do not do specialist analysis when a specialist exists.
- Justin talks here; crew reports outcomes and blockers here, not past this chat, unless he opened their chat.
- Handoffs carry `TC-YYYYMMDD-##`. High-stakes (Swing Setup, Story, Fusion, Regime, Daily Briefs) go through Work Verifier before Justin treats them as Final. Scanners skip verifier unless asked.
- Final form: full artifact in chat (one-click copy) plus the file. A short TLDR may lead but is not the Final.
- Speak outcomes, not internals. One decision card per decision. Escalate money, deletes, ambiguous go/no-go, conflicting bots, irreversible actions.
- Creation gate: new or rewritten bots/skills must pass harness-bot-standard. Prefer UpdateAgent over a duplicate bot. Prompt Architect / dr eggbot fix failures first.

### Roster (ids)
- Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729`
- X Brief `0ba0445d-a3df-4430-8a47-0eeb0cbbafcf`
- HK Swing Scanner `162f41b3-b93f-4d05-abdf-07b938f6ab56`
- Self Improver `1d369773-e1f5-4fdf-9a3a-2a38b1f54e16`
- 港股 Swing Setup `28b5646e-bfc2-440b-8a63-b68440a1de4b`
- US Swing Scanner `293d30a5-d04e-4443-89d9-f313f9ca873e`
- 投資敘事分析師 `3f297e81-4667-4dae-b517-b4f7ddee3537`
- US Market Daily Brief `44fb5c78-45d1-4716-b849-a5a6a0c1867b`
- 日常小助手 `553a3812-2d16-4787-879c-f8f05ba6182d`
- 美股 Swing Setup `747b3374-ada7-44d7-8cf4-73098b1c10af`
- 旅行計劃助手 `83647ac1-ec27-4889-aa08-1e376d4b738c`
- Video Transcriber `8483d4a7-8144-46c8-900b-a55b5f17630a`
- Sweeper / 清道夫 `8dbca7e8-e0d0-4447-821a-f9a3ad9d7e06`
- 全富決策副手 `925c3eaa-b0c0-440d-84a2-d28f7ed881e8`
- 港股收市簡報 `b9d6b823-8ae3-46a7-bc08-9beb4a35c631`
- 记忆管家 `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`
- Fusion Formatter `c45141fc-c050-49e2-9635-dca556a0cc1f`
- dr eggbot `cfe284bb-b01f-4f60-81af-4345d37a42f8`
- Prompt Architect `cfe4ca9b-b60f-49d3-bd0d-454c269f4388`
- Market Awareness Orchestrator `e4e8d80f-26c5-48c1-bd11-f56c0a9cc077`

Lanes: Market Awareness ‖ US Market Daily Brief ‖ 港股收市簡報 ‖ X Brief. Swing HK: HK Swing Scanner → 港股 Swing Setup → 投資敘事分析師 → Fusion Formatter. Swing US: US Swing Scanner → 美股 Swing Setup → 投資敘事分析師 → Fusion Formatter. Life: 旅行計劃助手 (trips only) ‖ 全富決策副手 (family/finance, no full itineraries). 日常小助手: Gmail + Calendar scan, read-only.

## Historical decisions
### Research and usage (locked)
- Usage gate (2026-09-20): reuse a fresh artifact; if the same approach failed twice, stop and report; prefer connector/API over clicking; do not create extra bots or routines to save usage. Canon `/workspace/fleet-policies/USAGE_GATE.md`.
- Research order (2026-09-30): Google Sheets MCP → Tavily → Firecrawl CLI (`[REDACTED:FIRECRAWL_API_KEY]`) → Browserless MCP → Browser Use MCP → box desktop last. Browser only when MCP exhausted, login needed, fail twice, or cannot access.
- Connectors Justin uses: Gmail, Google Calendar, Google Drive, Google Sheets, Tavily, X. Collapse plan 2026-09-30: keep plugin Gmail/Drive/Calendar/Sheets; thin xAI Drive and xAI Calendar duplicates were to be disconnected by Justin.
- Firecrawl is CLI/skills only (no MCP). Browserless MCP needsAuth until connected. Browser Use MCP was already connected.

### Briefs and AV lists
- HK and US abnormal-volume lists are Justin-manual only. TradingView paste is always valid: do not cross-check or overwrite price, RV, or name against Yahoo.
- From 2026-09-30: no 100億 H-share market-cap gate. Hide verification/method noise when checks are clean.
- HK briefs: Markdown only `HK brief-YYYY-MM-DD.md` under `/workspace/hk-brief-inputs/YYYY-MM-DD/`. No Kami/PDF unless he asks that day. Infographic preference is baoyu (dashboard / dense), not photo covers.
- Final always includes the full markdown in chat plus the file.

### Dates
- US CUP / Market Monitor stamp D+1 = US cash session D. HK Market Monitor is NOT D+1: session D uses the sheet label D.
- HK Market Monitor sheet: `1yIZLgTIqq38i_fK-q5oBWFogk0OCH1WuZ9a6AiAP8WI`.
- For US Market Monitor Up4/Down4, prefer Summary / D+1 numbers when they match Stockbee direction (locked 2026-09-18, TC-20260918-08).

### US scanner and Drive
- From 2026-09-24: scanner runs only Justin’s supplied list. No auto pullback-sheet dedupe. 總指揮 uploads Drive; scanner does not.
- Drive parent `US_Stock_Data` id `1Jn7yi0sXFBqVjLvjCsIazZnOvw0_E4TY`. Folder name = US bars/session date (e.g. "Oct 2"), not HKT run day. Search and reuse a same-name folder. Native CSVs only: Summary_US, Claude_Input_Slim, Data_Quality_Report, *_SwingAnalysis. Stop at Potential Setups. Do not auto-handoff to 美股 Swing Setup.
- Script: `/workspace/us-swing-scanner/scripts/us_swing_v451.py`. Outputs: `/workspace/us-swing-scanner/output/run-*/`.

### Setup Master (replaced Pullback buy Excel from 2026-09-26)
- Sheet id `1CXYi_h8t26x_ABZmTiqQSpJc91uZWZ3ad-QQ5qnI2UU`, tab US_MASTER. Lives in Drive folder "pullback buy US/HK" id `1tnTfbYp13vdjEV4Bc123ehloII-iodor`. Date = HK file date, so US data = prior US session.
- Trigger phrase "get setups from setup master": re-download, name the US session, run `/workspace/screener-sheet-review/pull_top5.py` for top 5 by Score from TC_shallow, TC_deep, CB (no BB/ARB; drop flag_breakdown/flag_arb; keep both tiers). Three tables plus a comma ticker line, then stop. Never auto-run the scanner. Justin picks the list.
- Older rule that both Drive Pullback Excel and Pine lists are Potential Setups is superseded for the auto-pull. Pine lists Justin pastes remain a separate optional path.

### Market Awareness
- Order: T2108 Excel → StockCharts breadth → regime with Stockbee + breadth + US-ETF. Stage `/workspace/market-inputs/YYYY-MM-DD/` and `/workspace/us-brief-inputs/YYYY-MM-DD/`.
- Regime v6.4.6: pillar A floor −4. Two consecutive raw days in the same band can force an effective upgrade and allow band jumps. Index DD Gate before V-REVERSAL only when T2108 < 20.
- ETF RS overlay is non-scoring. Sheet `1cgrNJNg0hX7mQV9H-0gU6dcGQ5OCwVaU9aTkVrq2iLQ`. Skills etf-rs-overlay-ingest and etf-rs-theme-tilt. Scanner gets ETF_RS_theme / sector_wind / sector_wind_note; scores unchanged. Unmapped names stay N/A (do not force a sector).
- Print the revised prior Stockbee row when Stockbee revises a past day.
- DATA GATE: missing/stale/abnormal sources → stop that phase, tell Justin expected vs actual date, never invent.

### Fusion and visuals
- After Justin picks a setup: Setup → Story → Fusion delivers report MD + ACHR-style infographic prompt (`/workspace/fusion/templates/INFOGRAPHIC_PROMPT_FORMAT_REF_ACHR.md`: 股票/行業/標題/主題故事/時間線/關鍵維度/操作劇本/一句講晒), then Work Verifier. Stop before baoyu image generation unless he explicitly asks.
- Kami for PDF/DOCX when a print doc is wanted. Sketchnote for cream educational notes. Visual-director for other assets.

### 日常小助手 (2026-10-03)
- Bot already existed. dr eggbot wrote the instruction; UpdateAgent applied (no new bot, no new routine).
- Job: scan Gmail + Google Calendar for mail that needs a reply and events/deadlines in the next 7 days. Traditional Chinese, short lists. Read-only. Draft only if Justin says 起草/draft. No send, no calendar edits.
- Optional notes `/workspace/daily-assistant/notes/YYYY-MM-DD.md`. Travel → 旅行計劃助手. Family/finance decisions → 全富決策副手. Market briefs stay with the specialist bots.

### Ops still held
- Weekly self-improve reflection paused 2026-09-14 (folder `fc876dfe-75a7-5341-91ad-6b47295e8a98`, cron `0 18 * * 5` HKT). Last run 2026-09-11 succeeded.
- Kick HK after-close brief paused, never run (folder `7fab2cfd-90de-5938-bfe8-5237cd89db62`, cron `5 18 * * 1-5` HKT). HK briefs are manual when Justin pastes movers.
- Self-improve items A–D from 2026-09-11 were held: apply nothing yet. Not reconfirmed since.
- Work Verifier refined 2026-09-11, same id. Pipeline Launch → Doctor → Drive → Evidence → Cleanup. Reports under `/workspace/work-verifier/output/`.
- Family note from the 2026-09-14 snapshot only (not reconfirmed this run): elder son ~12 at Queen’s College; younger ~9 at Raimondi College Primary + British Council Primary Plus. X handle recorded then as @Ycjustinwu.

## Live snapshot
As of this chat, 2026-10-03 evening HKT. Latest US cash session covered: **2026-10-02**. Next unused task id about **TC-20261003-06**. Nothing pending.

| Deliverable | Session | Result |
|---|---|---|
| 港股收市簡報 | 2026-10-02 | PASS_WITH_NOTES. `/workspace/hk-brief-inputs/2026-10-02/HK brief-2026-10-02.md`. HSI 23,972.29 −2.60%. UP 0 / DOWN 0005, 02888, 09698. Connect pause 10/1–10/7, next southbound 10/8. |
| US Market Daily Brief | 2026-10-02 cash (CUP stamp 10/03; 10/03 is Saturday) | PASS_WITH_NOTES. `/workspace/us-brief-inputs/2026-10-02/US brief-2026-10-02.md`. Epicenter NONE. Focus STX/WDC and HPE. CTVA paste name Celanese kept. |
| Market Awareness | 2026-10-02 | PASS_WITH_NOTES. `/workspace/market-awareness/2026-10-02/regime-daily-2026-10-02.md`. TOTAL +0.5/21.5. Effective Bear/Avoid CONFIRM day 2. T2108 20.53 (Reversal Watch off). Exposure 0%. VIX/VXV 0.882 labelled 1d stale. |
| US Swing Scanner | 2026-10-02 | GATE PASS 49/49. Box `/workspace/us-swing-scanner/output/run-20261003-1656/`. Drive folder "Oct 2" https://drive.google.com/drive/folders/1mY4RD2dnGyR74G_PdamBjkL8OG_mvCDo — 52/52 native CSVs. SPY close 769.64. SBLK wind UNMAPPED/N/A. BUY 18 / STALK 3 (FIVN 100 through U 55). Stopped at Potential Setups. |
| Prior US scan | 2026-10-01 | GATE PASS 47/47. Drive "Oct 1" folder id `12VoSCAgQx1R86xr0oyFx5CVinONniIA_`. |

Earlier Oct 1 session also has US brief + Market Awareness finals in this thread. SNPS focus was rewritten around the Ansys ~$35B deal (not a scanner row).

### Routines
Both paused. Do not re-enable on restore unless Justin says so.

## Secrets
Names only. No values, tokens, or file contents.
- `[REDACTED:FIRECRAWL_API_KEY]` — Firecrawl CLI
- `[REDACTED:~/.grok/auth.json]` — Grok Build OAuth session recorded 2026-09-14; do not copy into git
- `[REDACTED:XAI_API_KEY]` — not the preferred path; SuperGrok OAuth was used
- `[REDACTED:Google connector tokens]` — Gmail, Calendar, Drive, Sheets
- `[REDACTED:X connector]`
- `[REDACTED:box-browser-sessions]` — StockCharts / Stockbee / TradingView cookies, not copied

## Pending confirms
- Re-enable the two paused routines? Still no.
- Self-improve A–D from 2026-09-11: still held, not re-asked.
- Family schools and X handle above are from the 2026-09-14 snapshot, not reconfirmed 2026-10-03.
- Grok Build auth may need a fresh device login on a new machine.
- 日常小助手 instruction was applied in chat on 2026-10-03. An older memory line still said "confirmation pending"; treat the applied instruction as current.
