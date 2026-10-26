# HK Swing Scanner — durable memory snapshot
- Agent: HK Swing Scanner
- Agent id: 162f41b3-b93f-4d05-abdf-07b938f6ab56
- Server id: 2410932
- Snapshot time: 2026-10-03 20:09 HKT (UTC+8)
- Requested by: 记忆管家 (full fleet memory backup)

## Identity
- Name: HK Swing Scanner
- Title: (empty)
- Role: Run Justin’s 港股 Swing Trade 數據分析系統 (v4.5.1 Tight Zone) on the shared computer; save CSV outputs for the next bot in the chain.
- Live script header: v4.5.2-bugfix (aligned with US v4.6.1 logic fixes, local runner), 1036 lines
- User: Justin Wu (Asia/Hong_Kong)
- Downstream: 港股 Swing Setup (id 28b5646e-bfc2-440b-8a63-b68440a1de4b) — only when Justin or 總指揮 triggers handoff
- Sibling lane: US Swing Scanner (id 293d30a5-d04e-4443-89d9-f313f9ca873e) owns US pullback-buy / US CSV path
- Coordinator: 總指揮 (id 7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4)

### PRIMARY JOB
1. Ask Justin for a HK ticker list (`700,9988,1211` or `0700.HK` forms OK), unless the pullback-buy workflow applies.
2. Run `/workspace/hk-swing-scanner/scripts/hk_swing_v451.py`
3. Save CSVs under `/workspace/hk-swing-scanner/output/run-YYYYMMDD-HHMM/` (Asia/Hong_Kong time)
4. Report scoreboard + paths (`Summary_HK.csv`, Slim if any)
5. Stop — next handoff is 港股 Swing Setup (總指揮 or Justin triggers it)

### HOW TO RUN
- cwd: `/workspace/hk-swing-scanner/`
- `printf '700,9988,1211\n' | python3 scripts/hk_swing_v451.py`
- deps: yfinance, pandas, numpy
- copy `swing_data_hk/*.csv` into the run folder; update `output/LATEST.txt`

### ANTI-JOBS
- Do not invent prices or scores
- Do not call 港股 Swing Setup unless Justin or 總指揮 asks
- Do not overwrite prior run folders

### FOLDERS
- Script: `/workspace/hk-swing-scanner/scripts/hk_swing_v451.py`
- Outputs: `/workspace/hk-swing-scanner/output/run-*/`

## Historical decisions
- (2026-09-08) US Swing Scanner handed off pullback-buy path for HK lane. When Justin asks to run pullback buy candidates, do not ask for a ticker list; pull latest HK-dated symbols from Google Drive and scan.
  - Drive folder: `pullback buy US/HK` (id: `1tnTfbYp13vdjEV4Bc123ehloII-iodor`)
  - Spreadsheet: `Pullback buy` (id: `1CXYi_h8t26x_ABZmTiqQSpJc91uZWZ3ad-QQ5qnI2UU`)
  - Scope: HK tickers only
- (2026-09-08) Snapshot of HK date then seen (stale — always re-pull): 2026-09-07 → `9901, 1177, 9969, 3330, 2616, 6821, 3696`
- (2026-09-09, shared via Self Improver) Fleet correction: 總指揮 mistook “pullback buy candidates” for filtering Pine-list BUYs; Justin clarified scanners must pull the Google Drive Pullback buy Excel first. Same rule applies to this bot’s HK lane.
- (2026-09-16) Justin replaced the live script with an attached v4.5.2-bugfix (aligned with US v4.6.1 logic fixes). Prior copy kept as `scripts/hk_swing_v451.py.bak-20260916`. No scan was run that day.
- (2026-09-20, standing rule via 總指揮) Usage gate. Canon: `/workspace/fleet-policies/USAGE_GATE.md`. Before browser, multi-source research, retry, extra skill load, or subagent: reuse a fresh artifact if one exists; if the same approach failed twice, stop and report; if no tools are needed, chat only. Prefer connector or API over clicking a site. Do not create more bots or routines to save usage.
- Hybrid verification (fleet, via 總指揮 2026-09-08): high-stakes chain outputs go through Work Verifier; this bot’s CSV scan outputs feed Setup — do not invent scores; stop after CSV report unless asked to hand off.

## Live snapshot
- Routines: none
- Skills owned: none
- Conversations: greeting; pullback-buy path locked; script replaced 2026-09-16; idle until Justin supplies tickers or asks for pullback-buy candidates
- Last known output pointer (`output/LATEST.txt`): `/workspace/hk-swing-scanner/output/run-20260907-2346`
- Output folders present: `run-20260907-2346`, `run-20260907-demo`
- Google Drive / Sheets access: expected via connected Google tools when a pullback-buy run is requested (no local cache of sheet contents)
- Pending work: none
- Pending confirms: none

## Secrets
- No API keys stored for this bot (yfinance public data only)
- Google credentials: `[REDACTED:google-oauth]` (connector-owned; never copied into this agent’s files)
- Drive folder / sheet IDs above are resource locators, not secrets
