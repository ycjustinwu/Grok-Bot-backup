# Second brain — fleet memory backup
- **Agent id:** `d354ccee-dcf7-4655-bbde-016bc5db7654`
- **Name / title:** Second brain
- **Backup date:** 2026-11-02 (Asia/Hong_Kong)
- **Requested by:** Justin (chat)
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
4. **Native Relative_Strength** Google Sheet `1D3BrzLH3DmxX8Gv3W9Yhvd9q_LNOGXyNyUzjnXzqmHk` (**Relative_Strength**, native as of **2026-11-02** — no longer Office soft-go). Tabs: `📊 RS 總覽` / `Screen` / `Scores` / `Turning` / `ETF_Candidates` / `Run_Status` / per-ETF books / `Map`. Scores: Sector **S** vs VOO, Stock **K** vs ETF, Joint **J = S×K/100**; **Top** only when sleeve **S≥70** and stock **K≥50**. Prefer Improvers (rising-RS thrust) + 5d Δ for last-man checks. Soft-go (legacy `1QXQAHFL…` / Drive `1pxBQR1VkYbXKqc_w2de2wzaMQT5kra2g`) only if Sheets API fails — document soft-go in inventory.
5. Stockbee 50 Momentum Drive folder `1Fw2IfpQupYCrTtQTZMymt7VdjQnDWJv3` (latest 熱度圖) — **every run, not optional**

**Output:** ≤3 stalk names (growth bias, high ATR, strong RR, ~2w hold unless clear homerun). Default prefer **0–2 can’t-miss**; never force 3. No ticker repeat vs prior `/workspace/second-brain/` days within **1–2 day window**. If none clear the bar → say cannot find. Deep Bear = harder tape, still hunt gems. Then X dig ≤10 minutes.

**Same session:** run [US swing session overview](sand-workflow:us-swing-session-overview) — one Traditional Chinese **PRE-PICK** full-picture page (conflicts first; regime reference only; US Brief conflict-only; **no ticker / stalk embed**). Save under `/workspace/second-brain/YYYY-MM-DD/`. Timeline = this bot’s handoff — no extra cron.

### ANTI-JOBS
- Do **not** run scanners
- Do **not** write Setups (leave Setup-candidate remarks only)
- Do **not** author regime / US briefs
- Do **not** post to X
- Do **not** trade / open sim positions
- Hand adjacent work to the owning bot

### Wake / quiet
- Wake: scanner handoff via **總指揮** + on-demand chat
- Tue–Sat noon routine **`us-second-brain-3-picks` stays paused** unless Justin re-enables
- Weekend routine **`weekend-stalk-cleanup-eval`** Sun ~10:00 HKT flexible — **enabled**
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
- Second brain **not** in default WV pool; self-VERIFY in skill; WV only if `needs_wv` high or Justin asks
- Front-door A OFF（總指揮 routing）; never invent tickers/prices via Jev; never auto-send/auto-trade from a Noul

---

## 2. Locked rules / Justin corrections (all still in force)

### Source stack (locked 2026-10-22 TC-20261022-01; RS native refresh 2026-11-02)
- **Live:** Market Master `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`
- **Retired:** Setup Master `1CXYi…`, US Market Monitor `1XqUu…`
- Canonical: `/workspace/docs/market-master-canonical-2026-10-22.md`
- **RS (2026-11-02):** Justin parked native Relative_Strength `1D3BrzLH3DmxX8Gv3W9Yhvd9q_LNOGXyNyUzjnXzqmHk` as going-forward source #4 — no more default Office soft-go

### Pick philosophy (Justin)
- Regime = **reference**, not rigid gate — hard tape still hunt gems
- Always ask: better candidates elsewhere? market focus now? timing right? last-man? idiosyncratic strength vs big trend?
- Prefer growth, high ATR, strong RR, hold ≤~2 weeks unless clear homerun
- Soft theme-cap ≤2/3 same pillar when applicable
- Learn day by day from critiques

### Last-man-standing (Justin 2026-10-22 — binding)
- = previously **strong** sleeve whose **RS starts declining**
- **NOT** a default assumption on software/soft names
- Always check actual RS trend (native sheet 5d Δ / Turning); stay open-minded; do not lock hard into “software = last man”

### No-repeat window (Justin 2026-10-23 — binding)
- Only **~1–2 days** vs prior stalk days
- Older priors may be reassessed — do not permanently exclude

### US Brief dating trap (Justin 2026-10-24 — binding)
- Notion title often **D+1** (e.g.「US Brief 2026-10-24」= Close Date **2026-10-23**)
- Match **Close Date** property / body「反映…收市」, **not** title date alone

### Momentum thrust / chase (Justin CRWD critique — binding)
- Weight **rising RS** harder; don’t fear chase when thrust is real
- Imperfect RR → **smaller-bet**, not auto-skip
- Still require structure honesty (No_Clear_Setup / Extended callouts)

### RDWR lesson (Justin 2026-10-29 / W44 — binding)
- **Extended + soft Adj RR must NOT fill ≤3** just because only rising-RS STALK remains
- Prefer **fewer stalks** (0–2) over pad-to-3

### Thrust / easy-money vs hard-penny (Market Awareness judgment)
- Cupsir cue / climate = judgment call via Market Awareness
- **Do NOT boilerplate climate every Final** — only when it changes the call (e.g. mid-week trial → late-week can’t-miss)

### MM 形態篩選 ∩ screener handoff
- TC Deep / CB ∩ screener = **soft boost or remark**
- Silent if none

### Capital scarcity / can’t-miss (W44 patch 2026-11-01 — binding)
- Raise bar to **can’t-miss / really good only**
- Prefer **0–2 A+**; skip merely-OK
- Empty Final OK under Bear / crowded book (keep 10/31 behavior)

### Crowding gate (2026-11-01 — binding)
- If 模擬倉 book **≥5/7 open** or cash thin: only stalk names that clear RR **and** aren’t already **≥5% away** from a sane entry
- Else Setup remarks / observe only

### One chase window per name (W44 — binding)
- Do **not** re-stalk a CRWD-class leader three days running without a **fresh pullback** print + size-down

### Soft Final fillable-or-don’t-stalk (W44 #2/#6 — binding)
- If preferred digest **L already ≥5% away from close** → do **not** stalk (remarks/observe)
- Each stalk needs one-liner **L / SL / away check**
- **Demote** if away fails or **L≈SL** (CRWD open-on-stop lesson)

### Soft Final entry QA block (binding)
- Soft Final must carry entry QA (L/SL/away) before handoff
- No Soft Final **void** without Justin/總指揮 **AUTHORIZE**; one Final per bar-date (10/28 void/re-OPEN churn lesson)

### Weekend cleanup + eval (routine `weekend-stalk-cleanup-eval`)
- Sun ~10:00 Asia/Hong_Kong flexible — **enabled**
- Include: planned-vs-actual, 反方向, plan flaws, numbered improvement plan
- Pull 模擬倉 open/skip/fills from box SoT / journals

### Setup remarks only
- Usually **skip** full 美股 Swing Setup on every run
- Leave Setup-candidate remarks instead; 總指揮 / Setup bot owns writing

### Post-stalk routing
- 總指揮 routes 模擬倉 — Second brain does **not** open/sim

### WV / fleet
- Fleet skip Work Verifier default (pool = Regime + US Brief + 港股收市簡報)
- Second brain **self-VERIFY**; WV only if `needs_wv` high or Justin asks

### Overview PRE-PICK only (locked)
- Overview = Traditional Chinese pre-pick market commentary — **no ticker / stalk embed**
- Arabic digits only; HTML + embedded visuals preferred
- Drive folder: `1djZ778a9Gzf2ahDA8kXTPJCPUyohZxLc`
- Notion overview parent: US Swing Overviews `3fc77383-f89c-8163-b6d6-f89308b737af`
- Picks → US Attention Picks DB (separate)

### Stockbee
- Always read latest 熱度圖 every run
- Late inverse-ETF heat after regime already has Short focus = confirmation noise / too late — not a fresh short signal

### Earnings noticing (Justin FYI, not rule change)
- Prefer 減倉過earnings rather than skipping whole name solely for CAUTION inside ≤2w when structure otherwise works
- Absorb Ross Haber + SMB YT summaries as parking-lot only: `/workspace/second-brain/reference/absorb-ross-smb-2026-10-21.md` — **no rule changes unless asked**

### Wake model (shared)
- US Second brain picks driven by **US Swing Scanner handoff**, not noon cron (paused since ~2026-10-14)

---

## 3. Recent Soft Finals (session folders under `/workspace/second-brain/`)

| Folder / close | TC | Stalks | md5 `attention-3-picks.md` | Notes |
|----------------|-----|--------|----------------------------|-------|
| `2026-10-26/` | TC-20261027-05 | **CRWD · ZETA · NEOG** (3) | `d1134ce7b05ebd34c017fccb3effd11f` | Probe OK; Soft≠last-man |
| `2026-10-28/` | TC-20261028-05 | **ABSI · PANW · SNOW** (3) | `09bc857741ee5f1847463cc62f3057d9` | **04b VOIDED** (AUTHORIZE path); 05 re-run kept |
| `2026-10-29/` | TC-20261029-03b | **RDWR · CRWD · TWST** (3) | `bb740725e3d8722b28870ae427c78a22` | RDWR Extended = Justin miss; CRWD re-stalk |
| `2026-10-30/` | TC-20261030-07b | **RNG · WMG · PSX** (3) | `cae6d9b9edf5663eada293c4edbc03c2` | RR-first RNG; Oil轉弱 honesty on PSX |
| `2026-10-31/` | TC-20261031-03b | **cannot-find (0)** | `f1dd75dab719d67459cd9d789370bfbb` | Bear/Avoid — empty correct |

Artifacts per session typically: `sources-inventory.md`, `attention-3-picks.md`, `us-swing-overview.md` / `.html`, Stockbee extract, `_jev_c.json`.

---

## 4. W44 weekend eval snapshot

- Paths: `/workspace/second-brain/weekly/2026-W44-cleanup-eval.md`, `/workspace/second-brain/2026-11-01/weekend-stalk-cleanup-eval.md` (+ amended / inventory)
- Ran: 2026-11-01 ~10:10–10:15 Asia/Hong_Kong · routine `weekend-stalk-cleanup-eval`
- **Fills from SB stalks:** NEOG @12.08 · SNOW @335.36 · CRWD @254.335 · RNG @81.65 (still OPEN)
- **Book then:** OPEN **6/7** — CRL／HAFN／NEOG／SNOW／CRWD／RNG · cash ~$18k · NAV ~$103k · r_used ~$2.1k
- Observe/away/cash-cap filtered: RDWR · TWST · ZETA · PANW · WMG · PSX · ABSI…
- **Forward patches into skill (2026-11-01):** ≤2 can’t-miss · crowding gate · fillable-or-don’t-stalk (L/SL/away) · one chase window · no Soft void without AUTHORIZE

---

## 5. RS sheet status (2026-11-02)

Justin locked native **Relative_Strength** `1D3BrzLH3DmxX8Gv3W9Yhvd9q_LNOGXyNyUzjnXzqmHk` going-forward (no more Office soft-go default).

Latest read (chat refresh):
- **trade_date / bar:** 2026-10-30
- **Run_Status:** DONE · **1822** tickers
- **Top sleeves:** PHO / XLV / XRT / XLB / BUG
- **Weak:** SOXX / QQQ / AIPO
- **Rolling hard 5d:** CIBR · CLOU · IGV
- Skill source #4 updated in `us-second-brain-3-picks` (Joint J / S / K / Top+Improvers)

---

## 6. Routines

| Name | Schedule | Status | Notes |
|------|----------|--------|-------|
| `us-second-brain-3-picks` | Tue–Sat 12:00 Asia/Hong_Kong | **paused** | Driven by scanner handoff instead; last noon run ~2026-10-14 |
| `weekend-stalk-cleanup-eval` | Sun 10:00 Asia/Hong_Kong (flexible) | **enabled** | Last run 2026-11-01 |

---

## 7. Coverage / pending / live snapshot

### Key paths
| Path | Purpose |
|------|---------|
| `/workspace/second-brain/YYYY-MM-DD/` | Session outputs |
| `/workspace/second-brain/weekly/` | Weekend cleanup+eval |
| `/workspace/second-brain/reference/` | Absorb / parking-lot notes |
| `/workspace/docs/market-master-canonical-2026-10-22.md` | Market Master canonical |
| `/workspace/typesafe-jev/` | Jev client + thresholds + logs |
| `/home/box/agent-data/workflows/us-second-brain-3-picks/SKILL.md` | Primary skill |
| `/home/box/agent-data/workflows/us-swing-session-overview/` | Overview skill (PRE-PICK) |
| `/home/box/agent-data/workflows/us-second-brain-notion-sync/` | Notion sync skill |
| `/home/box/agent-data/agents/d354ccee-dcf7-4655-bbde-016bc5db7654/profile.json` | Live profile |
| Agent store | `/cursor/stores/store-c3e96ef2-7900-4cd0-84d2-890aea6a0fb9` |

### Drive / Notion ids
- Market Master: `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`
- Stockbee 50 folder: `1Fw2IfpQupYCrTtQTZMymt7VdjQnDWJv3`
- Overview HTML Drive: `1djZ778a9Gzf2ahDA8kXTPJCPUyohZxLc`
- **Native Relative_Strength:** `1D3BrzLH3DmxX8Gv3W9Yhvd9q_LNOGXyNyUzjnXzqmHk`
- Legacy RS / Drive soft-go: `1QXQAHFL…` / `1pxBQR1VkYbXKqc_w2de2wzaMQT5kra2g` (fallback only)
- US Swing Overviews Notion: `3fc77383-f89c-8163-b6d6-f89308b737af`
- US Attention Picks: separate Notion DB
- US-ETF Drive (Brief upstream): `1k5dJy7ny5n-W_EV5Aglt0QeeXS_-5Ijn`
- Scanner upload Drive: `1Jn7yi0sXFBqVjLvjCsIazZnOvw0_E4TY`

### Open work
- **None.** Idle pending next US Swing Scanner handoff via 總指揮 or on-demand Justin ask.
- No open stalk TC as of this backup.
- Self-VERIFY only (WV skip unless `needs_wv`).

### Secrets / credentials (names only)
- `[REDACTED:TYPESAFE_API_KEY]` — Jev TypeSafe client (`process.env.TYPESAFE_API_KEY`)
- No other bot-owned secrets recorded; connectors are fleet-shared — do not dump tokens

### Pending confirms
- **None.** No pending Justin confirms, widget waits, or AUTHORIZE cards as of backup time.
- (Do not act on any confirms listed here — inventory only.)

---

## 8. Skills this bot owns / primarily runs
- `us-second-brain-3-picks` (refreshed in repo 2026-11-02 — native RS + W44 gates)
- `us-swing-session-overview` (PRE-PICK; no stalk embed)
- `us-second-brain-notion-sync`
- `jev-fleet-decisions` (gate, every TC)

Supporting reads (not authored here): Stockbee fetch/monitor, TV abnormal volume MCP, Market Master tabs, Notion sync helpers.

---

## 9. Coverage checklist (for 记忆管家 / Justin backup)
- [x] Identity (profile + ONE JOB / ANTI-JOBS / partners / Jev B+C)
- [x] Locked rules / Justin corrections (incl. W44 gates + native RS)
- [x] Recent Soft Finals + md5s
- [x] W44 weekend eval snapshot
- [x] RS sheet status 2026-11-02
- [x] Routines (paused noon + enabled weekend)
- [x] Secrets as `[REDACTED:name]` only
- [x] Pending confirms listed (none) — not acted on
