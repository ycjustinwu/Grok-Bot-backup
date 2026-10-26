# Memory backup — US swing 模擬倉
**Agent id:** `17a46819-623f-40fe-8430-338e05725381`  
**Backup HKT:** 2026-10-26 20:45 HKT  
**Requested by:** 记忆管家 (fleet memory backup)

---

## 1. Identity

| Field | Value |
|--|--|
| Name / title | US swing 模擬倉 |
| Owner | Justin Wu · Asia/Hong_Kong |
| Tone | 繁體中文、短、to Justin；tickers/numbers may stay English |

### ONE JOB
Run a **$100,000 USD paper book** to validate Second brain stalks + Setup levels and practice Portfolio Management (Risk=R). **Not** a live-broker bridge. Success = sustainable runs, falsifiable, learns rules with Justin.

### PIPELINE / SKILLS
1. Second brain ≤3 stalks → [US swing sim open](sand-workflow:us-swing-sim-open)
2. While open → [US swing sim track](sand-workflow:us-swing-sim-track)
3. Weekly / on ask → [US swing sim reconcile](sand-workflow:us-swing-sim-reconcile)

Skill folders: `/home/box/agent-data/workflows/us-swing-sim-open|track|reconcile`

### ANTI-JOBS
- Not a live trade bridge; no broker orders
- Do not hang skills on or rewrite Second brain
- Do not author Setups, regime, US briefs, or scanners
- Do not invent portfolio rules; 北極星 does **not** run this book
- No standing routine unless Justin asks (note: Justin later approved post-close + pre-open routines — see Live snapshot)

### Partners
| Role | Agent |
|--|--|
| Captain / TC routing | 總指揮 `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` |
| Stalks upstream | Second brain `d354ccee-dcf7-4655-bbde-016bc5db7654` |
| Setup (read-only levels) | 美股 Swing Setup `747b3374-ada7-44d7-8cf4-73098b1c10af` — do not call unless Justin via 總指揮 |
| Ambition briefs only | 北極星 `83c42e28-ece0-4d8e-93e3-a26fb83ec80e` — never executes this book |
| High-stakes QA | Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729` — only when flagged / Jev needs_wv |
| Memory fleet | 记忆管家 `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` |

### Jev (B+C)
- Skill: [Jev Fleet Decisions](sand-workflow:jev-fleet-decisions)
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Key: `[REDACTED:TYPESAFE_API_KEY]` via `process.env.TYPESAFE_API_KEY` only
- Front-door A = OFF (總指揮 routing)
- WV: 美股 Swing Setup / this paper book **off default WV pool** unless Justin/Jev flags

---

## 2. Historical decisions / locked rules

Source of truth: `/workspace/us-swing-sim/state/rules.json` (12 rules, last update 2026-10-22 07:15 HKT)

| rule_id | Approved | Summary |
|--|--|--|
| `stalk-working-orders-v1` | 2026-10-16 | Stalk = place working order immediately (not watchlist-only) |
| `stalk-lifetime-v1` | 2026-10-16 | Cancel: invalidation / 5 sessions / earnings−1 / thesis dead / left zone; Favor-fade → cancel; Deep Bear paper_probe OK |
| `watchlist-journal-format-v2` | 2026-10-16 | Watchlist = SB stalks; Journal = after real execute |
| `notional-cap-20pct-v1` | 2026-10-16 | Per-name notional ≤20% equity; no fill slippage |
| `stalk-logic-audit-v1` | 2026-10-16 | Logic_Audit row per stalk; independent of P&L; min sample 30 |
| `9ema-grace-below-entry-v1` | 2026-10-16 | Superseded by v2 for grace scope |
| `limit-single-price-v1` | 2026-10-17 | One `limit_price` only — no ranges |
| `concrete-plan-v1` | 2026-10-17 | Must have limit/stop/shares/R$/invalidation/max_stalk_sessions; no vague reclaim gates |
| `9ema-grace-3sessions-v2` | 2026-10-20 | ALL positions: suppress EMA9_EXIT while `sessions_held < 3`; Hard SL unchanged |
| `tv-us-shortlist-sync-v1` | 2026-10-20 | Post-close sync TV watchlist **us shortlist** id `351605193` = open ∪ working |
| `trim-1-3-be-auto-v1` | 2026-10-22 | When `sessions_held` first hits 3 → AUTO trim 1/3 + BE next US open @ Open; once via `trim_1_3_done` |
| `limit-away-5pct-cancel-v1` | 2026-10-22 | Post-close: buy Close≥limit×1.05 → AUTO cancel (Logic_Audit 未到價過期) |

### Other locked prefs (memory / Justin)
- Equity paper **$100k**; R max **$1,000**/name; max **7** names
- Sheet single-writer: ledger SoT → `tools/sync_sheet.py` + `SHEET_CONTRACT.md`; never hand-patch cells
- Sheet id: `1mtSZo10jrCC_o4x0HnjjyrCEj_3FbBCcN8pgvZkU7v4` (Book/Watchlist/Orders/Positions/Journal/Logic_Audit/Dashboard)
- Market Master Setup_Latest: `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`
- Pre-open preferred **21:00 HKT** Mon–Fri (flexible ≤15 early, late=0)
- No-repeat window for Second brain stalks ≈ **1–2 days** (Justin 2026-10-23)
- CRL time-stop ask 2026-10-24: **HOLD** / already trimmed / no MOO exit (TC-20261024-02)

### Recent TCs (selected)
| TC | Outcome |
|--|--|
| TC-20261022-08 | HAFN OPEN; ABCL SKIP |
| TC-20261023-03 | ZETA+ESTC OPEN working; FIVN SKIP |
| TC-20261024-02 | CRL HOLD no time-stop |
| TC-20261024-04 | FRO OPEN working; CRWD+FIVN SKIP; ZETA leave; ESTC blocked |

### Track executes (selected)
- 2026-10-22: AUGO GAP_SL; CRL/DK trim+BE; DK HARD_SL; HAFN fill; FRSH MOO trim queued
- 2026-10-23: FRSH trim 485@15.29 (+$776); ESTC away-5% cancel; ZETA stalk 1/5

---

## 3. Live snapshot (as of backup)

### Routines (enabled)
| Name | Folder | Schedule (Asia/Hong_Kong) | Timing |
|--|--|--|--|
| US swing sim post-close track | `us-swing-sim-post-close-track` | `0 5 * * 2-6` (~05:00 Tue–Sat) | flexible early15 late30 |
| US swing sim pre-open check | `us-swing-sim-pre-open-check` | `0 21 * * 1-5` (~21:00 Mon–Fri) | flexible early15 late0 |

### Book (`/workspace/us-swing-sim/`)
| | |
|--|--|
| marks_session | **2026-10-23** |
| NAV / cash | **$103,589.10** / **$57,736.46** |
| OPEN | **CRL · FRSH · HAFN** |
| Working | **ZETA** L32.42 (elapsed 1/5) · **FRO** L52.93 (elapsed 0/5) |
| Cancelled | ESTC (limit-away-5pct 10/23) |
| Closed | AUGO, DK |
| R used / reserved | $321.92 / $1,435.28 |
| Pending MOO | none |
| Observe | ABCL, CRWD |

### Key paths
- Ledger root: `/workspace/us-swing-sim/`
- Contract: `/workspace/us-swing-sim/SHEET_CONTRACT.md`
- Sync: `/workspace/us-swing-sim/tools/sync_sheet.py`
- Equity curve SoT: `/workspace/us-swing-sim/state/equity_curve.json`
- SB in: `/workspace/second-brain/YYYY-MM-DD/`
- Regime ref: `/workspace/regime-output/YYYY-MM-DD/` (fallback market-awareness)
- Setup pinned: `/workspace/us-swing-setup/`
- Usage gate: `/workspace/fleet-policies/USAGE_GATE.md`

### Sheet / TV / Drive
- Paper Sheet: https://docs.google.com/spreadsheets/d/1mtSZo10jrCC_o4x0HnjjyrCEj_3FbBCcN8pgvZkU7v4/edit
- TV us shortlist id: `351605193`
- Drive mirror id (from state/drive.json when present): see `state/drive.json` — do not paste OAuth tokens

### Open work / next gates
- Next post-close track (~05:00 HKT Tue–Sat): marks for CRL/FRSH/HAFN + ZETA/FRO fill/cancel rules
- Next pre-open (~21:00 HKT weekdays): GO/HOLD/WATCH_GAP on opens + working
- FRO Oil轉弱 Favor-fade watch → cancel working if sleeve fades (stalk-lifetime-v1)
- No pending Justin confirms on paper book as of this backup

---

## 4. Secrets (redacted)

| Name | Storage | Value |
|--|--|--|
| TYPESAFE_API_KEY | `process.env.TYPESAFE_API_KEY` | `[REDACTED:TYPESAFE_API_KEY]` |
| Google Sheets / Drive / TradingView MCP | connector auth (Grok Bot MCP) | `[REDACTED:mcp-oauth]` — never paste |

No other bot-owned API secrets in ledger files.

---

## 5. Pending confirms (list only — do not act)

1. *(none)* — CRL time-stop already answered HOLD (2026-10-24).  
2. No open soft-ask widgets pending from this bot at backup time.  
3. Note: last marks_session still **2026-10-23** (weekend gap 10/25–10/26 HKT); next track should refresh after next US cash session.

---

## 6. Coverage checklist

- [x] Identity / ONE JOB / ANTI-JOBS / partners  
- [x] Locked rules (12) + key Justin prefs  
- [x] Routines (2)  
- [x] Live book snapshot + paths  
- [x] Secrets redacted  
- [x] Pending confirms listed without acting  
