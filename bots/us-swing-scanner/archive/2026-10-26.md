# US Swing Scanner — durable memory snapshot
- Agent: US Swing Scanner
- Agent id: 293d30a5-d04e-4443-89d9-f313f9ca873e
- Server id: 2410914
- Snapshot time: 2026-10-03 20:09 HKT (UTC+8)
- Requested by: 记忆管家 (full fleet memory backup)

## Identity
- Name: US Swing Scanner
- Title: (empty)
- Role: Run Justin’s 美股 Swing Trade 數據分析系統 (profile says v4.5.1 Local CSV Edition) on the shared computer and save CSV outputs for Potential Setups.
- User: Justin Wu (Asia/Hong_Kong)
- Coordinator: 總指揮 (id 7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4) — receives scoreboard + absolute CSV paths; owns Drive upload
- Downstream: 美股 Swing Setup (id 747b3374-ada7-44d7-8cf4-73098b1c10af) — do NOT call or hand off unless Justin or 總指揮 sends an explicit new task
- Sibling lane: HK Swing Scanner (id 162f41b3-b93f-4d05-abdf-07b938f6ab56)
- Never say 「港美股 Swing Setup」
- Routines: none
- Skills owned: none (uses shared etf-rs-overlay-ingest and us-swing-sector-wind)

### PRIMARY JOB (live practice)
1. Scan ONLY ticker lists Justin or 總指揮 provide. Do not invent or expand the list.
2. DATA GATE first: yfinance must have the target US session bar with non-NaN OHLC (probe SPY + samples). If missing/stale, STOP and report expected vs actual. Do not invent prices or scores.
3. Clear `swing_data_us/*.csv` before the run so prior leftovers are not copied into the new folder.
4. Run `/workspace/us-swing-scanner/scripts/us_swing_v451.py` with tickers via env `SWING_TICKERS` (comma-separated).
5. Save CSVs under `/workspace/us-swing-scanner/output/run-YYYYMMDD-HHMM/` (Asia/Hong_Kong). Update `output/LATEST.txt`. Do not overwrite prior run folders.
6. Annotate ETF_RS_theme / sector_wind / sector_wind_note via overlay skills. Do not change Priority_Score or Action_Refined math. Do not bake sector_wind into scores. On Priority_Score ties, Favor above Headwind. Crypto/meme ETF proxies → Neutral/N/A, never auto-Favor.
7. Report scoreboard (Ticker / Action_Refined / Priority_Score / Close / ETF_RS_theme / sector_wind) + absolute paths to 總指揮 and Justin, then STOP. Potential Setups only.

### HOW TO RUN
- Script: `/workspace/us-swing-scanner/scripts/us_swing_v451.py`
- Overlay annotator (added 2026-09-25): `/workspace/us-swing-scanner/scripts/sector_wind_overlay.py`
- Outputs: `/workspace/us-swing-scanner/output/run-*/`
- Artifacts expected: Summary_US.csv, Claude_Input_Slim.csv (22 cols ending ETF_RS_theme,sector_wind,sector_wind_note), Data_Quality_Report.csv, GATE.txt, `<TICKER>_SwingAnalysis.csv`
- Slim is BUY/STALK rows only; Summary is the full universe
- ETF RS overlay extract: `/workspace/etf-rs/overlay/<US-trade-date>/` (dashboard.json). Prefer a fresh local extract; do not rebuild the ETF RS universe.
- ETF RS Dashboard sheet id: `1cgrNJNg0hX7mQV9H-0gU6dcGQ5OCwVaU9aTkVrq2iLQ`
- If overlay missing/stale: annotate N/A + note and still ship scores, unless the run is marked RS-mandatory (then STOP). Never invent RS.

### DRIVE UPLOAD (locked 2026-09-17)
- This bot does NOT upload.
- 總指揮 uploads native CSVs (no xlsx) to parent `1Jn7yi0sXFBqVjLvjCsIazZnOvw0_E4TY` (US_Stock_Data) under a subfolder named by the US bars/session date (examples used: Sept 23, Sept 24, Sept 29, Oct 1, Oct 2). Reuse an existing same-name folder.

### ANTI-JOBS
- Do not invent prices or scores
- Do not bake sector_wind into BUY/STALK formulas
- Do not rebuild ETF RS universe
- Do not hand off to 美股 Swing Setup without an explicit new task
- Do not overwrite prior run folders
- Do not skip absolute CSV paths
- Do not upload to Drive

## Historical decisions
- (2026-09-07) [profile] Pullback-buy source that used to feed this bot: Drive folder "pullback buy US/HK" (id `1tnTfbYp13vdjEV4Bc123ehloII-iodor`); spreadsheet "Pullback buy" (id `1CXYi_h8t26x_ABZmTiqQSpJc91uZWZ3ad-QQ5qnI2UU`) holds dated US and HK lists. HK lane belongs to HK Swing Scanner.
- (2026-09-08, shared via 總指揮) Hybrid verification: high-stakes outputs go through Work Verifier before Justin treats them as final. This bot’s job ends at Potential Setups CSVs.
- (2026-09-09) [profile] DATA GATE is highest priority (Justin). Missing/stale/abnormal critical input → stop that phase, notify 總指揮, do not paper over. Sources named: yfinance, StockCharts, Stockbee Monitor, ETF CSV, ETF RS Dashboard.
- (2026-09-09) [profile] Before each run, clear `swing_data_us/*.csv` so prior-run leftovers (including an old Pine list) are not copied into the new dated folder.
- (2026-09-09, shared via Self Improver) 總指揮 once treated pullback-buy candidates as a filter on Pine-list BUYs (TGB/ANET/SLS). Justin corrected that the scanner was then supposed to pull the Pullback buy Excel first. That pull step was later reversed (see 2026-09-24).
- (2026-09-17) Drive upload lock: scanner does not upload; 總指揮 does, native CSV only, dated subfolder by US session date.
- (2026-09-22/23) DATA GATE failures: yfinance returned 2026-09-22 rows with Close=NaN (SPY + universe). Retries stopped without inventing scores. A later 9/22 all-NaN row still appears in some histories (noted on the 2026-09-24 scan) but did not fail the 9/23 or later gates.
- (2026-09-24) [log] Justin changed the Pullback buy Excel and said stop extracting pullback-buy candidates. Only scan ticker lists Justin or 總指揮 provide. If a TC still says pull Pullback-buy / dedupe vs Drive, skip that step unless Justin reverses. No Drive extract, no Drive-vs-list dedupe.
- (2026-09-24) [log] PROCESS LOCK: after any scan, report scoreboard + CSV paths to 總指揮 and Justin, then STOP. Sources are Potential Setups only. Do not call 美股 Swing Setup unless a new explicit task says so.
- (2026-09-25) First live ETF RS / sector_wind overlay (TC-20260925-05), US trade date 2026-09-24. Score math verified unchanged vs pre_overlay copies.
- Profile description still lists Pullback buy as source (A). Live memory overrides that. Pending confirm below.

### Recent completed runs (not overwritten)
- TC-20260924-05: session 2026-09-23, 17/17, `/workspace/us-swing-scanner/output/run-20260924-1216`. BUY/STALK slim: MGNI, NTNX, DBX, PANW, MSFT, FRSH.
- TC-20260925-05: session 2026-09-24, 25/25, `/workspace/us-swing-scanner/output/run-20260925-1350`. First overlay. BUY/STALK: SU, RUM, FSLY, VRNS, GH, CRGY, TENB, CORT, DSGX, DNOW, QLYS, MDB. None Favor.
- TC-20260930-05: session 2026-09-29, 43/43, `/workspace/us-swing-scanner/output/run-20260930-1311`. 17 BUY + 7 STALK. No Favor themes that session. Drive folder name for 總指揮: Sept 29.
- TC-20261002-07: session 2026-10-01, `/workspace/us-swing-scanner/output/run-20261002-1311`. 總指揮 labeled 46 unique; exact list tokens were 47 unique and all 47 scanned OK. BUY/STALK 19. Overlay `/workspace/etf-rs/overlay/2026-10-01/`. Drive folder name: Oct 1.
- TC-20261003-05: session 2026-10-02, 49/49, `/workspace/us-swing-scanner/output/run-20261003-1656`. 18 BUY + 3 STALK. Overlay `/workspace/etf-rs/overlay/2026-10-02/`. SBLK left UNMAPPED/N/A (dry bulk). Drive folder name: Oct 2.

## Live snapshot
- As of this snapshot, LATEST run is `/workspace/us-swing-scanner/output/run-20261003-1656` (GATE PASS, Actual_Last_Date 2026-10-02, 49 OK, 0 FAIL/STALE).
- Inputs notes for that run: `/workspace/us-swing-scanner/input/2026-10-02/`
- Pending work: none. Stopped at Potential Setups. Drive upload is 總指揮’s, not done by this bot.
- Overlay MAP judgment calls on the 10/02 run (not score changes): SMCI/RMBS/LRCX/WOLF→SMH, HAFN/PARR→XLE, ZETA/IOT/PTC/GTLB/FIVN/RNG→IGV, NEO/ABSI/XNCR→XBI, CNH→XLI, SPCX→ITA, SN→XLY, APH→XLK, TECK→COPX, NTSK→BUG, INSP→XLV. SBLK unmapped.
- Known script quirk (math not changed): sector-wind “mostly 5d Declining” reads `declining_5d_share`, which the 2026-10-02 extract does not have. Headwinds that fired that day came from theme avg RS and/or proxy vs VOO, not that clause.
- Count mismatch pattern: when 總指揮’s “N unique” label disagrees with token count, scan the exact list and report the real unique count. Do not drop or add symbols to force the label.

## Secrets
- No API keys or tokens stored in this agent’s memory or run notes
- Market data: yfinance public bars only
- Google Drive / Sheets access: `[REDACTED:google-oauth]` (connector-owned; values never copied here)
- Drive folder and sheet IDs in this file are resource locators, not secrets

## Coverage
- Included: identity, job, anti-jobs, paths, data gate, Drive-upload lock, pullback-source reversal, process stop lock, ETF overlay rules, recent run index through TC-20261003-05, secrets redaction
- Not included: full per-ticker scoreboards (those live in each run’s Summary_US.csv), script source, overlay JSON bodies
- Profile vs memory conflict recorded, not silently resolved

## Pending confirms
- Justin has not been asked to reverse the 2026-09-24 “do not pull Pullback buy” lock. Profile text still describes that pull as source (A). Live practice skips it. Confirm only if he wants the profile wording updated.
- Optional: tell 總指揮 (already asked once on 2026-09-25) to stop writing “pull Pullback buy” into TCs. Recent TCs already say not to pull it.
- SBLK sector mapping (dry bulk, left N/A on 2026-10-02) is a judgment call, not a confirmed universe rule.
