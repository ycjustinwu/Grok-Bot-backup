---
name: US Swing Sector Wind
description: >-
  Use this after US Swing Scanner v4.5.1 CSVs when annotating Claude_Input_Slim
  / Summary_US / Potential Setups with ETF_RS_theme, sector_wind, and optional
  sector_wind_note from Justin’s ETF RS Dashboard — annotation only, no score math.
---
# US Swing Sector Wind (Scanner annotation)

Post-process after `/workspace/us-swing-scanner/scripts/us_swing_v451.py` writes run outputs. Depends on [ETF RS Overlay Ingest](sand-workflow:etf-rs-overlay-ingest).

## Surfaces (Justin-read)

Annotate **all** of:

1. `Claude_Input_Slim.csv` (BUY/STALK slim — primary Setup handoff)
2. `Summary_US.csv` (full scoreboard)
3. Any Potential Setups Excel/scoreboard table the bot posts to chat / Drive that mirrors Slim columns

Do **not** change `Priority_Score`, `Action_Refined`, or playbook score math.

## New columns (exact names)

| Column | Values |
|--------|--------|
| `ETF_RS_theme` | Sheet Theme string (e.g. `P7 Software/Cyber`) or `UNMAPPED` |
| `sector_wind` | `Favor` \| `Headwind` \| `Neutral` \| `N/A` |
| `sector_wind_note` | Optional short note, e.g. `SOXX RS100 Rising v5+10.4%` |

## CSV header order

### Claude_Input_Slim.csv (22 cols)

```text
Ticker,Close,Priority_Score,Action_Refined,Playbook_Flag,Setup_Type,RR_Zone_Best,RR_Ratio_Best,Adjusted_Stop,Stop_Type,Adj_Risk_Dollar,Adj_Risk_Pct,Adj_RR_Ratio,Earnings_Proximity_Flag,Earnings_Date,SR_Flip_Active,MA_Compression_Zone,Tight_Zone_Active,Tight_Zone_Days,ETF_RS_theme,sector_wind,sector_wind_note
```

### Summary_US.csv

Append the same three columns **at end** of existing 27-col header (after `AVWAP_HVD`):

```text
…,POC_Level,AVWAP_HVD,ETF_RS_theme,sector_wind,sector_wind_note
```

## Mapping ticker → theme

1. Best-effort: map stock sector/industry → primary **liquid theme ETF proxy** (see `docs/sector-proxy-map.md`), then take that ETF’s **Theme** from Universe/Dashboard.
2. If multiple proxies, prefer the most liquid (SMH/SOXX, IGV, XBI, etc.) listed as primary in the map.
3. If unmapped → `ETF_RS_theme=UNMAPPED`, `sector_wind=N/A`, note `unmapped`.

## sector_wind rules (locked)

Use **primary proxy** row(s) on Dashboard for the mapped theme (not crypto substitutes):

1. **Favor:** mapped theme ETF(s) have **RS actual ≥ 80** AND **5-day trend = Rising** AND **vs VOO 5d > 0**
2. **Headwind:** theme **avg RS < 30** OR theme **mostly 5d Declining** OR primary proxy **vs VOO 5d < 0** with **RS < 50**
3. **Neutral:** otherwise
4. **N/A:** unmapped or insufficient history (missing RS / trends on proxy)

### Crypto / meme exclusion

Do **not** treat pure crypto/meme ETFs (`IBIT`, `ETHA`, `WEED`, `MEME`, `BITQ`, and similar) as equity sector wind for ordinary stock setups. If a stock **only** maps to P4 crypto proxies → `sector_wind=Neutral` or `N/A` with note `crypto-proxy-excluded` — **never auto-Favor** from crypto RS.

## Priority sort (annotation only)

- Do **not** change BUY/STALK score math from `sector_wind`.
- If the bot already sorts by `Priority_Score`, on **ties** sort `Favor` above `Neutral` above `Headwind` above `N/A`.
- Document for downstream Setup: Headwind **may** later raise the bar — Scanner itself only annotates unless Justin already required that tie-break.

## Implementation note

Preferred: small post-pass script or bot step that joins Slim/Summary to overlay JSON — **avoid** baking RS into `calculate_priority_score`. Script patch to `SLIM_COLS` is optional later; skill-level annotation is enough for TC draft apply.

## DATA GATE

Missing/stale RS sheet → fill `ETF_RS_theme=UNMAPPED` (or leave blank only if entire annotate step skipped), `sector_wind=N/A`, note `RS overlay DATA GAP`; still ship Scanner scores. If 總指揮 marked overlay mandatory for the run → STOP and notify.

## VERIFY

- [ ] Three columns present on Slim + Summary with exact names
- [ ] Slim header order matches 22-col contract above
- [ ] No change to Priority_Score / Action_Refined formulas
- [ ] Favor/Headwind/Neutral/N/A rules followed; crypto proxies excluded from auto-Favor
- [ ] US trade date mentioned in chat scoreboard or note when overlay used
- [ ] Tie-break Favor > Headwind only on equal Priority_Score
