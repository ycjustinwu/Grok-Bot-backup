# US Swing Scanner — Durable Memory Snapshot
- Agent: US Swing Scanner
- Agent id: 293d30a5-d04e-4443-89d9-f313f9ca873e
- Snapshot time: 2026-09-14 20:32 HKT (12:32 UTC)
- Requested by: 记忆管家 (full fleet disaster-recovery backup)

## Identity
- Name: US Swing Scanner
- Role: Run Justin's 美股 Swing Trade 數據分析系統 (v4.5.1 Local CSV Edition) on the shared computer; save CSV outputs for Potential Setups.
- User: Justin Wu (Asia/Hong_Kong)
- Script: `/workspace/us-swing-scanner/scripts/us_swing_v451.py`
- Working dir: `/workspace/us-swing-scanner/`
- Outputs: `/workspace/us-swing-scanner/output/run-YYYYMMDD-HHMM/` (Asia/Hong_Kong)
- Downstream: report to 總指揮 then STOP; do not call 美股 Swing Setup unless explicit TC
- Never say 「港美股 Swing Setup」 — US setup bot is 美股 Swing Setup
- Data gate (highest priority, Justin 2026-09-09): if critical input missing/stale/abnormal — STOP, do not invent, notify 總指揮 with failure source and expected vs got

## Historical decisions
- 2026-09-07: Drive folder `pullback buy US/HK` (id `1tnTfbYp13vdjEV4Bc123ehloII-iodor`) + spreadsheet `Pullback buy` (id `1CXYi_h8t26x_ABZmTiqQSpJc91uZWZ3ad-QQ5qnI2UU`) is the canonical pullback-candidate source; US-dated symbols for this bot, HK-dated for HK Swing Scanner.
- 2026-09-07: When Justin says run pullback buy, pull latest US date from that sheet and scan — no ticker ask.
- 2026-09-09: 總指揮 initially routed TradingView Pine list (SLS/FIGR/…) as TC-20260909-05; Justin corrected that "pullback buy candidates" means Drive Excel first (lesson via Self Improver).
- 2026-09-09 TC-20260909-07: re-ran from Drive sheet date 2026-09-09 (14 US names); prior Pine run folder `run-20260909-1033` left untouched.
- 2026-09-09: Before each run, clear `swing_data_us/*.csv` so prior-run leftovers do not mix into new run folder (process note from 總指揮 after leftovers copied into `run-20260909-1053`).
- 2026-09-09 PROCESS LOCK (總指揮): after any scan (Drive Excel OR Pine list), report scoreboard + CSV paths to 總指揮 (and Justin), then STOP. Both sources = Potential Setups only. Do not call/expect 美股 Swing Setup unless new explicit TC.
- Hybrid verification (fleet): Work Verifier does second-pass on high-stakes outputs; scanner itself is Potential Setups CSV producer, not a high-stakes analysis deliverable unless routed.

## Live snapshot
- LATEST.txt → `/workspace/us-swing-scanner/output/run-20260909-1053`
- Known run folders: `run-20260907-2359`, `run-20260909-1033` (Pine TC-05), `run-20260909-1053` (Drive TC-07), plus `consolidated-potential-setups-20260909.md`
- Last Drive US sheet date used: 2026-09-09
- Last Drive US tickers (14): DSGN, ELVN, TEM, CRSR, ZBIO, IOT, SRRK, VRNS, HNGE, EWTX, CMPS, ZURA, CLYM, PHVS
- Last Drive scoreboard (script only): SRRK BUY 90; DSGN/HNGE/ELVN BUY 88; ZURA BUY 83; EWTX BUY 80; PHVS/CLYM/CRSR BUY 75; CMPS BUY 70; TEM WATCH 60; IOT WATCH 55; VRNS WATCH 50; ZBIO WATCH 45
- Last Pine list (TC-05, superseded for "pullback buy" intent): SLS, FIGR, ALM, TGB, HBM, DAR, ANET, PAGS, OSCR, ROIV, SMR → run-20260909-1033
- Deps: yfinance, pandas, numpy (public data only; no API keys)
- Google Drive connector: connected (user-Google-drive)
- Secrets: none required for scanner; yfinance public only
- Pending confirms: none
- Open process debt: ensure clear of `swing_data_us` before every future copy (locked in memory)

## Secrets placeholders only
- Google Drive OAuth / MCP tokens: `[REDACTED:google-drive-mcp]`
- Any box env API keys: `[REDACTED:box-env]` (scanner does not use private market APIs)
