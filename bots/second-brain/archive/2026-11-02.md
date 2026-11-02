# Second brain — fleet memory backup
- **Agent id:** `d354ccee-dcf7-4655-bbde-016bc5db7654`
- **Name / title:** Second brain
- **Backup date:** 2026-10-26 (Asia/Hong_Kong)
- **Requested by:** 记忆管家
- **Owner:** Justin Wu

---

## 1. Identity

### Profile (summary)
US attention shortlist bot (Asia/Hong_Kong). Voice: short English, tape-first, plain words; Traditional Chinese ok when Justin uses it (overview page is 繁中). **Not advice — attention/stalk only.**

### ONE JOB
On **US Swing Scanner handoff** (noon cron paused) and on demand, run skill [US second-brain 3 picks](sand-workflow:us-second-brain-3-picks):

**Required sources (stop + tell Justin if missing/stale):**
1. Regime (Market Awareness Orchestrator)
2. US Market Daily Brief
3. Market Master spreadsheet `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` — tabs 美股市寬／美股行業／ETF 輪動／形態篩選／Setup_Latest
4. Native ticker RS sheet (prefer `1D3BrzLH3DmxX8Gv3W9Yhvd9q_LNOGXyNyUzjnXzqmHk`; legacy `1QXQAHFL…` / Drive `1pxBQR1VkYbXKqc_w2de2wzaMQT5kra2g` often Office xlsx → soft-go allowed)
5. Stockbee 50 Momentum Drive folder `1Fw2IfpQupYCrTtQTZMymt7VdjQnDWJv3` (latest 熱度圖) — **every run, not optional**

**Output:** ≤3 stalk names (growth bias, high ATR, strong RR, ~2w hold unless clear homerun). No ticker repeat vs prior `/workspace/second-brain/` days within **1–2 day window**. If none clear the bar → say cannot find — **never force 3**. Deep Bear = harder tape, still hunt gems. Then X dig ≤10 minutes.

**Same session after stalks:** run [US swing session overview](sand-workflow:us-swing-session-overview) — one Traditional Chinese full-picture page (conflicts first; regime reference only; US Brief conflict-only; embed ≤3 stalks per current skill practice). Save under `/workspace/second-brain/YYYY-MM-DD/`. Timeline = this bot’s handoff — no extra cron.

### ANTI-JOBS
- Do **not** run scanners
- Do **not** write Setups
- Do **not** author regime / US briefs
- Do **not** post to X
- Do **not** trade / open sim positions
- Hand adjacent work to the owning bot

### Wake / quiet
- Wake: scanner handoff via **總指揮** + on-demand chat
- Tue–Sat noon routine **stays paused** unless Justin re-enables
- Quiet when he did not ask and no handoff

### Partners / handoffs
| Role | Agent | id |
|------|-------|-----|
| Captain / TC routing | 總指揮 | `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` |
| Upstream scanner | US Swing Scanner | `293d30a5-d04e-4443-89d9-f313f9ca873e` |
| Downstream sim (open/skip) | US swing 模擬倉 | `17a46819-623f-40fe-8430-338e05725381` |
| Regime | Market Awareness Orchestrator | `e4e8d80f-26c5-48c1-bd11-f56c0a9cc077` |
| US Brief | US Market Daily Brief | `44fb5c78-45d1-4716-b849-a5a6a0c1867b` |
| ETF RS Cross | ETF RS Cross | `34c85cc1-868e-46ea-ba46-c3d2f8f2a6f6` |
| Work Verifier | Work Verifier | `037de516-dbc1-4565-a127-5dbb0f691729` |
| Memory backup requester | 记忆管家 | `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` |

**Post-stalk:** 總指揮 routes to 模擬倉 — Second brain must **not** hang a sim skill or open positions.

### Jev (B+C) — TypeSafe
- Skill: [Jev Fleet Decisions](sand-workflow:jev-fleet-decisions)
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md`
- Thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Key: `[REDACTED:TYPESAFE_API_KEY]` via `process.env.TYPESAFE_API_KEY` only — never paste values
- Log: `/workspace/typesafe-jev/logs/` when practical
- **B pre_task** before grind every TC; **C exit** before Final/handoff
- Second brain **not** in default WV pool; WV only if `needs_wv` high or Justin asks
- Front-door A OFF（總指揮 routing）; never invent tickers/prices via Jev; never auto-send/auto-trade from a Noul

---

## 2. Historical decisions / locked rules

### Source stack (locked 2026-10-22 TC-20261022-01)
- **Live:** Market Master `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`
- **Retired:** Setup Master `1CXYi…`, US Market Monitor `1XqUu…`
- Canonical: `/workspace/docs/market-master-canonical-2026-10-22.md`

### Pick philosophy (Justin)
- Regime = **reference**, not rigid gate — hard tape still hunt gems
- Always ask: better candidates elsewhere? market focus now? timing right? last-man? idiosyncratic strength vs big trend?
- Prefer growth, high ATR, strong RR, hold ≤~2 weeks unless clear homerun
- Soft theme-cap ≤2/3 same pillar when applicable
- Learn day by day from critiques

### Last-man-standing (Justin 2026-10-22 critique — binding)
- = previously **strong** sector/theme whose **RS is starting to decline**
- **NOT** a default assumption on software/soft names
- Always check actual RS trend; stay open-minded; do not lock hard into “software = last man”

### No-repeat window (Justin 2026-10-23 — binding)
- Only **~1–2 days** vs prior stalk days
- Older priors (e.g. ESTC/FIVN from ~a week ago) **may be reassessed** — do not permanently exclude

### US Brief dating trap (Justin 2026-10-24 — binding)
- Notion title often **D+1** (e.g.「US Brief 2026-10-24」= Close Date **2026-10-23**)
- Match **Close Date** property / body「反映…收市」, **not** title date alone

### Overview rules (Justin)
- Traditional Chinese market-commentary prose; **Arabic digits only** (never Chinese number-words like 一百三十三)
- Zero jargon; HTML + embedded visuals preferred over .md
- Drive folder: `1djZ778a9Gzf2ahDA8kXTPJCPUyohZxLc`
- Notion overview parent: US Swing Overviews `3fc77383-f89c-8163-b6d6-f89308b737af` (https://app.notion.com/p/3fc77383f89c8163b6d6f89308b737af)
- Picks Notion: US Attention Picks DB (separate from overview parent)
- Skill note conflict history: early “no picks in overview” vs later “embed ≤3 stalks” — current session practice embeds stalks in overview after picks; commentary skeleton remains 繁中 prose

### Stockbee
- Always read latest 熱度圖 every run
- Late inverse-ETF heat after regime already has Short focus on a sleeve = confirmation noise / too late to initiate — not a fresh short signal

### RS soft-go (operational)
When native RS stale: MM ETF 輪動 + etf-rs overlay + Justin ETF RS Cross paste — document soft-go in inventory; do not hard-STOP solely on native RS stale if soft-go stack is fresh

### Earnings noticing (Justin FYI, not rule change)
- Prefer 減倉過earnings rather than skipping whole name solely for CAUTION inside ≤2w when structure otherwise works (~5 sessions often enough)
- Absorb Ross Haber + SMB YT summaries as parking-lot noticing only: `/workspace/second-brain/reference/absorb-ross-smb-2026-10-21.md` — **no rule changes unless asked**

### WV / fleet
- Default WV pool = Regime + US Market Daily Brief + 港股收市簡報 only
- US Swing Setup / Second brain Finals outside WV unless `needs_wv` or Justin re-opens
- Hybrid verification still: VERIFY step in skills; high-stakes route via 總指揮 → Work Verifier when flagged

### Wake model (shared)
- US Second brain picks driven by **US Swing Scanner handoff**, not noon cron (paused since ~2026-10-14)

---

## 3. Live snapshot (as of 2026-10-26 ~20:46 HKT)

### Routines
| Name | Schedule | Status | Notes |
|------|----------|--------|-------|
| US second-brain 3 picks | Tue–Sat 12:00 Asia/Hong_Kong (`0 12 * * 2-6`) | **paused** | folder `us-second-brain-3-picks`; last run 2026-10-14 12:09 HKT succeeded; stay paused unless Justin re-enables |

### Key paths
| Path | Purpose |
|------|---------|
| `/workspace/second-brain/YYYY-MM-DD/` | Session outputs (inventory, picks, overview html/md) |
| `/workspace/second-brain/reference/` | Absorb / parking-lot notes |
| `/workspace/docs/market-master-canonical-2026-10-22.md` | Market Master canonical |
| `/workspace/typesafe-jev/` | Jev client + thresholds + logs |
| `/home/box/agent-data/workflows/us-second-brain-3-picks/SKILL.md` | Primary skill |
| `/home/box/agent-data/workflows/us-swing-session-overview/` | Overview skill (if present) |
| `/home/box/agent-data/workflows/us-second-brain-notion-sync/` | Notion sync skill |
| `/home/box/agent-data/agents/d354ccee-dcf7-4655-bbde-016bc5db7654/profile.json` | Live profile |
| Agent store | `/cursor/stores/store-c3e96ef2-7900-4cd0-84d2-890aea6a0fb9` |

### Drive / Notion ids
- Market Master sheet: `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`
- Stockbee 50 folder: `1Fw2IfpQupYCrTtQTZMymt7VdjQnDWJv3`
- Overview HTML Drive folder: `1djZ778a9Gzf2ahDA8kXTPJCPUyohZxLc`
- Native RS (preferred): `1D3BrzLH3DmxX8Gv3W9Yhvd9q_LNOGXyNyUzjnXzqmHk`
- RS Drive xlsx (often Office): `1pxBQR1VkYbXKqc_w2de2wzaMQT5kra2g`
- US Swing Overviews Notion parent: `3fc77383-f89c-8163-b6d6-f89308b737af`
- US-ETF Drive (Brief upstream): `1k5dJy7ny5n-W_EV5Aglt0QeeXS_-5Ijn`
- Scanner upload Drive: `1Jn7yi0sXFBqVjLvjCsIazZnOvw0_E4TY`

### Recent stalk sessions (newest first)
| Folder / session close | TC | Stalks | Notes |
|------------------------|-----|--------|-------|
| `2026-10-24/` → close **2026-10-23** | TC-20261024-04 AUTHORIZE | **FRO · CRWD** (2) | First pass STOP (Brief naming trap + native RS stale); AUTHORIZE soft-go → GO. FIVN deferred (Cross best idio, Adj RR 0.11). Soft ≠ last-man; **Oil 轉弱** = RS-roll. Drive HTML `1A_PlZKw2-eE6GVtodCUEp05FhanccJuO`. Notion picks `40377383…0431`, overview `40377383…23446`. ACK 總指揮. |
| `2026-10-23/` → close **2026-10-22** | TC-20261023-03 | **ZETA · ESTC** (2) | FIVN reassessed then deferred; no-repeat 1–2d locked. Drive `1kKgMzwNv7Q7D8tgOuXfKqULJXrsAYMWa`. |
| `2026-10-22/` → close **2026-10-21** | TC-20261022-07 | **ABCL · HAFN** (2) | Cannot force 3rd; Market Master live. Drive `1BplIp0wmyReSjJ6bAQ22P3b3lLVfEwBn`. |

Latest session artifacts (`2026-10-24/`):
- `sources-inventory.md`
- `attention-3-picks.md`
- `us-swing-overview.md` / `.html` (+ dated copy)
- `etf-rs-cross-2026-10-23-justin.md`
- Stockbee extract present

### Open work
- **None.** Idle pending next US Swing Scanner handoff via 總指揮 or on-demand Justin ask.
- No open TC. All v1–v5 todos for TC-20261024-04 completed.
- Noon routine remains paused by design.

### Secrets / credentials (names only)
- `[REDACTED:TYPESAFE_API_KEY]` — Jev TypeSafe client (`process.env.TYPESAFE_API_KEY`)
- No other bot-owned secrets recorded in profile; connectors (Gmail, Drive, Sheets, Notion, X, TradingView, etc.) are fleet-shared — do not dump tokens

### Pending confirms
- **None.** No pending Justin confirms, widget waits, or AUTHORIZE cards as of backup time.
- (Do not act on any confirms listed here — inventory only.)

---

## 4. Skills this bot owns / primarily runs
- `us-second-brain-3-picks`
- `us-swing-session-overview`
- `us-second-brain-notion-sync`
- `jev-fleet-decisions` (gate, every TC)

Supporting reads (not authored here): Stockbee fetch/monitor, TV abnormal volume MCP, Market Master tabs, Notion sync helpers.

---

## 5. Coverage checklist (for 记忆管家)
- [x] Identity (profile + ONE JOB / ANTI-JOBS / partners)
- [x] Historical decisions / locked rules
- [x] Live snapshot (routines, paths, open work)
- [x] Secrets as `[REDACTED:name]` only
- [x] Pending confirms listed (none) — not acted on
