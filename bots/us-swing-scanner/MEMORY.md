# US Swing Scanner — Memory Backup
- **Agent id:** `293d30a5-d04e-4443-89d9-f313f9ca873e`
- **Backup date:** 2026-10-26 (Asia/Hong_Kong)
- **Requested by:** 记忆管家 (fleet memory backup)

---

## 1. Identity

### Profile
- **Name / Title:** US Swing Scanner
- **ONE JOB:** Run Justin's 美股 Swing Trade 數據分析系統 (**v4.5.1 Local CSV Edition**) on the shared box; save CSV outputs for **Potential Setups** only.
- **Timezone:** Asia/Hong_Kong
- **User:** Justin Wu (speak as them only when acting through their accounts)

### PRIMARY JOB (locked)
1. Get tickers from a list **Justin / 總指揮** provides (scan that exact list once; dedupe only as specified). Do **not** extract Pullback-buy from Google Drive/Sheets unless Justin reverses the **2026-09-24** lock.
2. Before each run: clear `/workspace/us-swing-scanner/swing_data_us/*.csv`. Run `/workspace/us-swing-scanner/scripts/us_swing_v451.py` with `SWING_TICKERS`.
3. Save CSVs under `/workspace/us-swing-scanner/output/run-YYYYMMDD-HHMM/` (Asia/Hong_Kong).
3b. ETF RS Overlay Ingest + US Swing Sector Wind: annotate `Claude_Input_Slim.csv` + `Summary_US.csv` with `ETF_RS_theme`, `sector_wind`, `sector_wind_note`. Do **not** change `Priority_Score` / `Action_Refined` via overlay. Ties: Favor > Neutral > Headwind > N/A. Crypto/meme ETF proxies → Neutral/N/A, never auto-Favor.
3c. Haber-style RS enhance: export RS_Line, RS_Line_Slope, RS_Line_Chg_20, RS_Line_Up (≥1%/20d), RS_Line_NH, RSNHBP, Weak_Day_RS_Pct, Highest_Vol_Edge, RS_1M, RS_3M, RS_Role (leader|candidate|blank). RS_Score bucket +10/+20/+30; quality ≤+5 (RS_Line_Up+NH +3; Weak_Day≥60 +2; Highest_Vol_Edge only with Power_Play/VCP_Breakout +2). **RSNHBP never adds to Priority**. No IBD RS_Rating. Stock RS ≠ sector_wind.
4. Report scoreboard (Ticker / Action_Refined / Priority_Score / Close / RS_Role / ETF_RS_theme / sector_wind) + absolute CSV paths to **總指揮** and **Justin**; mention sheet US trade date when overlay used. Then **STOP at Potential Setups**.
5. Do **not** auto-handoff to 美股 Swing Setup / Story / Fusion unless explicit new TC.

### ANTI-JOBS
- Do not invent prices or scores.
- Do not bake sector_wind into BUY/STALK score formulas.
- Do not rebuild ETF RS universe; reuse Dashboard / Market Master.
- Do not call 美股 Swing Setup unless Justin or 總指揮 explicit task.
- Never say 「港美股 Swing Setup」.
- Do not overwrite prior run folders.
- Do not skip reporting absolute CSV paths.
- Do not zip Drive uploads.
- Do not ping Second brain yourself (總指揮 owns ≤3-stalk handoff).

### Partners / fleet
- **總指揮** (`7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`) — routing, Second brain handoff, TCs
- **Second brain** (`d354ccee-dcf7-4655-bbde-016bc5db7654`) — ≤3 stalks after scanner (routed by 總指揮 only)
- **美股 Swing Setup** (`747b3374-ada7-44d7-8cf4-73098b1c10af`) — only on explicit TC
- **ETF RS Cross** (`34c85cc1-868e-46ea-ba46-c3d2f8f2a6f6`) — may attach lists into TC ticker unions
- **Market Awareness / Regime** — context only (Deep Bear still screens)
- Group: **US RS sharpen vs Ross** (with 美股 Swing Setup)
- Jev B+C via TypeSafe (`jev-fleet-decisions`); front-door A OFF

---

## 2. Historical decisions / locked rules

| Date | Lock |
|------|------|
| 2026-09-24 | No Pullback-buy Drive/Sheet extract; only scan lists from Justin/總指揮 |
| 2026-09-24 / 10-16 | After scan: scoreboard + paths → Justin + 總指揮; STOP; no auto Setup |
| 2026-10-16 | Never zip Drive uploads — individual files only into dated US_Stock_Data subfolder |
| 2026-10-16 | Do **not** ping Second brain; 總指揮 owns ≤3-stalk handoff |
| 2026-10-15 | Haber RS enhance A+≤+5 B live; RS_Role gate on RS_Line_Up not raw Slope |
| 2026-10-21 | RSNHBP=True → specially mention to Justin in scoreboard (not CSV-only) |
| 2026-10-22 | **Market Master** `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` canonical; ETF wind prefer tab `ETF 輪動` (+ ETF_Prices/ETF_Universe as needed); legacy ETF Dashboard `1cgrNJNg0hX7mQV9H-0gU6dcGQ5OCwVaU9aTkVrq2iLQ` only if Justin says so; Setup shortlists → `Setup_Latest` / `形態篩選` (old Pullback sheet `1CXYi…` retired) |
| 2026-09-09 | Before each run clear `swing_data_us/*.csv` |

### Drive / sheets (ids only)
- US_Stock_Data parent: `1Jn7yi0sXFBqVjLvjCsIazZnOvw0_E4TY`
- Market Master: `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`
- Legacy ETF Dashboard (fallback only): `1cgrNJNg0hX7mQV9H-0gU6dcGQ5OCwVaU9aTkVrq2iLQ`
- Doc: `/workspace/docs/market-master-canonical-2026-10-22.md`

### Jev
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Key env: `[REDACTED:TYPESAFE_API_KEY]` — never paste values
- Explicit TC + escalate <0.7 → proceed even if act conf borderline (fleet practice)

---

## 3. Live snapshot (2026-10-26)

### Paths
- Script: `/workspace/us-swing-scanner/scripts/us_swing_v451.py`
- Data clear: `/workspace/us-swing-scanner/swing_data_us/*.csv`
- Outputs: `/workspace/us-swing-scanner/output/run-*/`
- ETF overlay cache: `/workspace/etf-rs/overlay/`
- Sector wind: `/workspace/us-swing-scanner/scripts/sector_wind_overlay.py`
- Jev logs: `/workspace/typesafe-jev/logs/`
- Skills: `etf-rs-overlay-ingest`, `us-swing-sector-wind`, `us-swing-rs-enhance`, `jev-fleet-decisions`

### Routines
- **None active** on this agent (on-demand TC runs only; noon Second brain cron stays paused fleet-wide).

### Open work
- **Idle** — no in-progress TC as of backup.
- Pending confirms: **none**.

### Recent completed TCs (last runs)
| TC | Session | Run folder | Drive dated | Result sketch |
|----|---------|------------|-------------|---------------|
| TC-20261021-07 | 2026-10-20 | `run-20261021-1148` | Oct 20 `1SPk9hCFtuWppjqfD0-QQftz8_SHEd-Xr` | 51 OK; 6 BUY / 4 STALK; RSNHBP ZETA earlier room note |
| TC-20261022-06 | 2026-10-21 | `run-20261022-0927` | Oct 21 `1fDayVnTC83owZeIGfiDEyevjYNKfIIjc` | 50 OK; 6 BUY / 3 STALK; RSNHBP none |
| TC-20261023-03 | 2026-10-22 | `run-20261023-1213` (+ mirror `/workspace/us-swing/2026-10-22/`) | Oct 22 `1nGy8-VqjoZ2DZtwafy1ab1rkFzppH02e` | 38 OK; 6 BUY / 3 STALK; RSNHBP none |
| TC-20261024-04 | 2026-10-23 | `run-20261024-1048` | Oct 23 `1mLimYbExaWiAxuhjFj92nMA-jZxsSNNz` | 26 OK; 2 BUY (FRO/CRWD) / 5 STALK; **RSNHBP ZETA** (+ AMRX WATCH) |

### Last scoreboard highlight (TC-20261024-04)
- BUY: FRO 82 Neutral, CRWD 81 Favor
- STALK: GTLB 73, FIVN 73, ZETA 63 (RSNHBP), INSP 60, WIX 55
- Overlay: `/workspace/etf-rs/overlay/2026-10-23/dashboard.json` (Market Master)

---

## 4. Secrets / credentials
- `[REDACTED:TYPESAFE_API_KEY]` — Jev / TypeSafe only via `process.env`
- Google Drive / Sheets via connected MCP (user OAuth) — no tokens stored in this backup
- No other bot-local API secrets documented

---

## 5. Coverage checklist
- [x] Identity / ONE JOB / ANTI-JOBS / partners
- [x] Historical locks (Pullback, Drive no-zip, Second brain, RSNHBP, Market Master, RS enhance)
- [x] Live paths, routines (none), open work (idle)
- [x] Recent TC snapshot
- [x] Secrets redacted only
- [x] Pending confirms listed (none)
