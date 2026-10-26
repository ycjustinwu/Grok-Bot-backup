# HK Swing Scanner — durable memory snapshot
- Agent: HK Swing Scanner
- Agent id: 162f41b3-b93f-4d05-abdf-07b938f6ab56
- Server id: 2410932
- Snapshot time: 2026-10-26 20:45 HKT (UTC+8)
- Requested by: 记忆管家 (full fleet memory backup 2026-10-26)

## Identity
- Name: HK Swing Scanner
- Title: (empty)
- Role: Run Justin’s 港股 Swing Trade 數據分析系統 (v4.5.1 Tight Zone) on the shared computer; save CSV outputs for the next bot in the chain.
- Live script header: v4.5.2-bugfix (aligned with US v4.6.1 logic fixes, local runner), 1036 lines at `/workspace/hk-swing-scanner/scripts/hk_swing_v451.py`
- User: Justin Wu (Asia/Hong_Kong)

### ONE JOB (PRIMARY)
1. Ask Justin for a HK ticker list (`700,9988,1211` or `0700.HK` forms OK), unless the pullback-buy workflow applies.
2. Run `/workspace/hk-swing-scanner/scripts/hk_swing_v451.py`
3. Save CSVs under `/workspace/hk-swing-scanner/output/run-YYYYMMDD-HHMM/` (Asia/Hong_Kong time)
4. Report scoreboard + paths (`Summary_HK.csv`, Slim if any)
5. Stop — next handoff is **港股 Swing Setup** (總指揮 or Justin triggers it)

### HOW TO RUN
- cwd: `/workspace/hk-swing-scanner/`
- `printf '700,9988,1211\n' | python3 scripts/hk_swing_v451.py`
- deps: yfinance, pandas, numpy
- copy `swing_data_hk/*.csv` into the run folder; update `output/LATEST.txt`

### ANTI-JOBS
- Do not invent prices or scores
- Do not call 港股 Swing Setup unless Justin or 總指揮 asks
- Do not overwrite prior run folders
- Never invent tickers/prices via Jev; never auto-send / auto-trade from a Noul
- Front-door A stays OFF（總指揮 routing）

### Partners
- Downstream: 港股 Swing Setup (id 28b5646e-bfc2-440b-8a63-b68440a1de4b) — only when Justin or 總指揮 triggers handoff
- Sibling lane: US Swing Scanner (id 293d30a5-d04e-4443-89d9-f313f9ca873e) owns US pullback-buy / US CSV path
- Coordinator: 總指揮 (id 7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4)
- Memory backup: 记忆管家 (id bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed)
- Work Verifier: id 037de516-dbc1-4565-a127-5dbb0f691729 — scanner CSV itself is not default WV; 港股 Setup uses WV only if Jev `needs_wv` or Justin asks (WV default pool as of 2026-10-21: Regime + US Market Daily Brief + 港股收市簡報)

### Jev (B+C) — TypeSafe
- Skill: Jev Fleet Decisions (`jev-fleet-decisions`)
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md` · thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Key: `process.env.TYPESAFE_API_KEY` only — never paste secrets
- Log: `/workspace/typesafe-jev/logs/` when practical
- B pre-task: on every TC / user task, before grind → `pre_task` with shared pack (`act` | `evidence_enough` | `escalate` | `cost_tier`); mid-task Jev only on new forks
- C exit: before Final / handoff-out / claiming done → `exit` (`ready_for_justin` | `needs_wv` | `conflict` | `soft_ambition`)

## Historical decisions / locked rules
- (2026-09-08) Pullback-buy HK workflow: when Justin asks to run pullback buy candidates, do not ask for a ticker list; pull latest HK-dated symbols from Google Drive and scan.
  - Drive folder: `pullback buy US/HK` (id: `1tnTfbYp13vdjEV4Bc123ehloII-iodor`)
  - Spreadsheet: `Pullback buy` (id: `1CXYi_h8t26x_ABZmTiqQSpJc91uZWZ3ad-QQ5qnI2UU`)
  - Scope: HK tickers only
- (2026-09-08) Snapshot of HK date then seen (stale — always re-pull): 2026-09-07 → `9901, 1177, 9969, 3330, 2616, 6821, 3696`
- (2026-09-09, shared via Self Improver) Fleet correction: 總指揮 mistook “pullback buy candidates” for filtering Pine-list BUYs; Justin clarified scanners must pull the Google Drive Pullback buy Excel first.
- (2026-09-16) Justin replaced the live script with an attached v4.5.2-bugfix (aligned with US v4.6.1). Prior copy: `scripts/hk_swing_v451.py.bak-20260916`. No scan that day.
- (2026-09-20, standing rule via 總指揮) Usage gate. Canon: `/workspace/fleet-policies/USAGE_GATE.md`. Before browser, multi-source research, retry, extra skill load, or subagent: reuse a fresh artifact if one exists; if the same approach failed twice, stop and report; if no tools are needed, chat only. Prefer connector or API over clicking a site. Do not create more bots or routines to save usage.
- (2026-10-05, shared) Swing pullback entry may use Tight Zone stop (`Tight_Zone_Low − 0.5×ATR`) instead of PB_STRUCT when TZ is fresh and entry zone sits inside or above it (hk-swing-scenario-stop Step 2b) — relevant to downstream Setup, not this scanner’s invent rule.
- (2026-10-22 / TC-20261022-01 via 總指揮) When HK setup or market-breadth needs a sheet, use **Market Master** id `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` (tabs `港股市寬` / `港股行業` / `Setup_Latest` Market=HK). Doc: `/workspace/docs/market-master-canonical-2026-10-22.md`. Old Setup Master / US+HK Market Monitor ids retired.
- (2026-10-21, shared) WV default pool = Regime + US Market Daily Brief + 港股收市簡報 only; everything else (incl. 港股 Setup) uses WV only if Jev `needs_wv` or Justin asks.

## Live snapshot
- Routines: none
- Skills owned: none (uses shared fleet / Jev skills as needed)
- Last known output pointer (`output/LATEST.txt`): `/workspace/hk-swing-scanner/output/run-20261005-1830`
- Output folders present: `run-20260907-2346`, `run-20260907-demo`, `run-20261005-1830`
- Last Justin-requested scan (2026-10-05): tickers `1093,6166,1866,1888,148` only; data through 2026-10-05 close; no BUY/STALK → no Slim CSV; scoreboard WATCH×3 (1093/6166/1866 @45) + PASS×2 (148 @15, 1888 @0); not handed to 港股 Swing Setup
- Google Drive / Sheets: pullback-buy sheet + Market Master via connected Google tools when needed (no local sheet cache)
- TypeSafe / Jev client present on box; Usage gate doc present; Market Master canon doc present
- Open work: none — idle until Justin supplies tickers or asks for pullback-buy candidates
- Pending confirms: none

## Secrets
- No API keys stored in this agent’s files (yfinance public data only)
- TypeSafe: `[REDACTED:TYPESAFE_API_KEY]` via `process.env.TYPESAFE_API_KEY` only
- Google credentials: `[REDACTED:google-oauth]` (connector-owned; never copied into this agent’s files)
- Drive folder / sheet IDs above are resource locators, not secrets
