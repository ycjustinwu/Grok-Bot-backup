# 美股 Swing Setup — Fleet Memory Backup

- **Agent id:** `747b3374-ada7-44d7-8cf4-73098b1c10af`
- **Backup date:** 2026-10-26 20:46 HKT
- **Requested by:** 记忆管家
- **Secrets policy:** names only as `[REDACTED:name]` — no token values

---

## 1. Identity

| Field | Value |
|-------|--------|
| Name / Title | 美股 Swing Setup |
| Role | 美股 Swing Trade Setup 分析師（**v4.8-US**） |
| Market | US only (CSV from US Swing Scanner / `US_swing_v4.6` / `v4.6.1_Colab`) |
| Shared skills | Same Swing skill pack as 港股 Swing Setup; **market rules differ** |

### ONE JOB

Analyze uploaded / path-specified **US** Python CSV → Setup VERDICT, Trade Entry, **MARKET=US** GEMINI HANDOFF (for 投資敘事分析師).

**When to run:** Only when Justin or 總指揮 sends an **explicit task** with ticker + CSV path. Drive Pullback-buy Excel and TradingView Pine screener lists are **Potential Setups only** — scanner stops there; **do not** auto-take Setup after a scan.

### ANTI-JOBS

- Do not invent prices / volumes / VERDICT
- Do not compute Regime TOTAL
- Do not upgrade Story
- Do not process HK CSV
- Do not ship as Final without authorization
- Do not auto-call Story unless Justin asks
- Do not re-add RS quality points into Priority (Scanner owns ≤+5)
- Do not compute stops from RS flags

### Partners / routing

| Partner | Role |
|---------|------|
| **總指揮** (`7aa7a8a6-…`) | Task routing, Final authorize, Drive upload ownership |
| **US Swing Scanner** (`293d30a5-…`) | Upstream CSV / Summary / Slim / GATE; Potential Setups only |
| **投資敘事分析師** (`3f297e81-…`) | Downstream GEMINI HANDOFF → Story (only if Justin asks) |
| **Fusion Formatter** | Tech + Story fuse (not auto) |
| **Work Verifier** (`037de516-…`) | **Off by default** for this bot (see standing) |
| **Second brain** | Scanner handoff stalks — not Setup auto-run |
| Group | `US RS sharpen vs Ross` (`88d71c92-…`) with US Swing Scanner |

### IO

- **In:** `/workspace/us-swing-scanner/output/run-*/`
- **Out:** `/workspace/us-swing-setup/output/run-*/`
- **ETF overlay (read):** `/workspace/etf-rs/overlay/`
- **Jev:** `/workspace/typesafe-jev/` · client `.venv/bin/python …/jev_client.py`

### Core skills (live)

- [Swing Trade Analysis](sand-workflow:hk-swing-trade-analysis) — orchestration + Phase 7/8 + **output template / one-click HANDOFF copy** (2026-10-21)
- [Swing CSV Validate](sand-workflow:hk-swing-csv-validate)
- [Swing Setup Playbook](sand-workflow:hk-swing-setup-playbook)
- [Swing Scenario Stop](sand-workflow:hk-swing-scenario-stop)
- [US Swing RS Enhance](sand-workflow:us-swing-rs-enhance) — interpret only downstream
- [US Swing Sector Wind](sand-workflow:us-swing-sector-wind) — SECTOR WIND line (separate from RS CONTEXT)
- [Jev Fleet Decisions](sand-workflow:jev-fleet-decisions)

Prefer **live skills** if grok.com Project copy conflicts.

---

## 2. Historical decisions / locked rules

### Process gate (2026-09-09) — LOCKED

After US Swing Scanner → **stop**. Pullback-buy Excel / Pine screener = Potential Setups only. No Setup / Trade Entry / HANDOFF without **explicit new TC** from Justin or 總指揮.

### v4.8 core (aligned 2026-09-09 / journal 2026-09-16)

Tight Zone v2.1 · Freshness Gate · hidden pullback HL≥8 (playbook; profile text may say HL≥5 — **prefer live playbook**) · Earnings **UNKNOWN** forbids BUY · structure stop Risk% band vs ADR · pullback forbids ATR_FALLBACK as BUY basis · Ladder labels via `Target_*_Source` · TZ pullback exception Step 2b (Justin 2026-10-05): may use TZ stop when Freshness + entry inside/above zone.

### Haber RS enhance (2026-10-15) — LOCKED into v4.8-US

- Scanner: Priority = base + quality **≤+5** (`Up∧NH` +3; Weak≥60 +2; VolEdge only Power_Play/VCP_Breakout +2). **RSNHBP never in Priority**.
- Setup: **must NOT** re-add quality points. `RS_Role` = label only (`leader` / `candidate` / blank).
- HANDOFF: separate **RS CONTEXT** and **SECTOR WIND** lines.
- Stops: **never** from RS.
- Smoke: HTFL no false leader (`RS_Line_Up` preferred over raw Slope≈0).
- RSNHBP (RS NH before price): soft **STALK/WATCH** bias + highlight; **never alone → BUY**. Scanner special-mentions on scoreboard when True (group 2026-10-21).

### Work Verifier standing (2026-10-21) — LOCKED

Justin / 總指揮 TC-20261021-08: **美股 Swing Setup does not need WV** by default. Finals outside WV gate unless Justin re-opens. Fleet WV default pool = Regime + US Market Daily Brief + 港股收市簡報 only (other bots: Jev `needs_wv` or Justin ask).

**Note:** `profile.json` ANTI_JOBS text still says “Self-VERIFY 後等 總指揮交 Work Verifier” — **standing memory overrides**; treat as stale profile wording until profile rewrite.

### Output template (2026-10-21) — LOCKED

- `{T}_GEMINI_HANDOFF.md` = Phase 8 body only (banner→banner).
- Chat / `{T}_Final.md`: wrap HANDOFF in one ` ```text ` fence for Justin one-click Copy→Gemini.
- Repo note: `/workspace/us-swing-setup/OUTPUT_TEMPLATE.md`
- Sync pack (manual paste to grok Project): `/workspace/us-swing-setup/grok-project-sync/US_swing_Setup_Grok_Project_Instructions_20261016.md`

### Jev (B+C)

- Front-door A **OFF** (總指揮 routing).
- Every TC: `pre_task` before grind; `exit` before Final.
- Never invent tickers/prices via Jev; never auto-trade from Noul.

### Other fleet facts (context, not owned)

- Market Master sheet id `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` (Setup_Latest etc.)
- Scanner Drive parent `1Jn7yi0sXFBqVjLvjCsIazZnOvw0_E4TY` — **總指揮 uploads**, Setup does not.

---

## 3. Live snapshot (2026-10-26)

### Routines

- **None** owned by this agent (no scheduled automations in current automation status).

### Open work / todos

- **Idle.** No in-progress Setup TC.
- Last completed: **ATRC Final STALK** (2026-10-21), authorized outside WV.

### Latest deliverable

| Item | Path / value |
|------|----------------|
| Run | `/workspace/us-swing-setup/output/run-20261021-ATRC/` |
| VERDICT | STALK (OVERRIDE WATCH→STALK) |
| Entry | $56.55–$57.34 · max fill $56.95 |
| Stop | $55.05 PB_STRUCT (AVWAP_20D_Low) |
| L1 | $61.70 RR 2.50x |
| Files | `ATRC_Final.md`, `ATRC_GEMINI_HANDOFF.md`, `ATRC_Trade_Entry.csv`, validate/setup/scenario/verdict/SELF_VERIFY, `MANIFEST.txt` |
| Pinned scanner | `/workspace/us-swing-scanner/output/run-20261021-1148/` (GATE TC-20261021-07) |

### Recent group note (RS)

- Run `20261021-1148`: only **ZETA** had `RSNHBP=True` (candidate). Setup awaits explicit TC to analyze.

### Settings

- `notifyOnAgentUpdates`: true
- Avatar: pebble / blue

### Secrets (presence only)

| Name | Status |
|------|--------|
| `[REDACTED:TYPESAFE_API_KEY]` | SET in env (Jev) — value not written |

No other bot-owned API keys recorded in this backup.

---

## 4. Pending confirms

| Item | Status |
|------|--------|
| Profile ANTI_JOBS WV wording vs standing “WV off” | **Pending confirm** — list only; do **not** auto-UpdateProfile |
| Optional: browser-paste sync pack to grok.com Project “US swing Setup” | Not chosen (pack A only, 2026-10-16) — still optional |
| Optional: NBIS+SMCI Drive re-run Setup | Unconfirmed from earlier session — not active |

**No pending user confirm acted on in this backup.**

---

## 5. Coverage checklist

- [x] Identity / ONE JOB / ANTI-JOBS / partners
- [x] Process gate + v4.8 + RS enhance + WV standing + HANDOFF copy template
- [x] Paths IO + skills + Jev
- [x] Live: routines (none), open work (idle), last ATRC Final
- [x] Secrets redacted by name
- [x] Pending confirms listed, not executed

