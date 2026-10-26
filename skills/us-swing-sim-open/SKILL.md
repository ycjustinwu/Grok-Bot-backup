---
name: US swing sim open
description: >-
  Use when Second brain hands ≤3 US stalks / handoff, or Justin asks to
  open/skip paper positions in the US swing 模擬倉 book.
---

> **Canonical (2026-10-22):** Market Master `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` — tabs 美股市寬／港股市寬／ETF 輪動／形態篩選／Setup_Latest. Doc: `/workspace/docs/market-master-canonical-2026-10-22.md`.
# US swing sim open

ONE JOB: Decide open or skip for each Second brain stalk in the $100k US swing paper book, size with Risk=R, and write ledger state. Not live trading.

## Inputs (read-only)

- Second brain handoff for session date: `/workspace/second-brain/YYYY-MM-DD/` (`attention-3-picks.md`, overview if present)
- Regime band + exposure only: `/workspace/regime-output/YYYY-MM-DD/regime-daily-YYYY-MM-DD.md` (fallback `/workspace/market-awareness/...`). Reference only — do not rescore.
- Market Master sheet id `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` tab `Setup_Latest` (retired `1CXYi…`) and any PINNED Setup paths under `/workspace/us-swing-setup/`
- Current book: `/workspace/us-swing-sim/state/portfolio.json` and `/workspace/us-swing-sim/positions/`

If handoff or required Setup levels for a name are missing → skip that name and say what is missing. Do not invent entry/stop.

## Portfolio math (fixed)

- Portfolio equity: **$100,000** USD (paper)
- High-conviction max risk **R = 1% = $1,000**
- `notional = R ÷ stop%` where `stop% = |entry − stop| / entry`
- `shares = floor(notional ÷ entry)` (whole shares unless Justin says otherwise)
- **Per-name notional cap 20%** of equity ($20,000 on $100k). If `shares × entry > 0.20 × equity`, resize `shares = floor(0.20 × equity / entry)` and record effective_R. (Justin 2026-10-16; rule `notional-cap-20pct-v1`)
- **No fill slippage** on paper marks (Justin 2026-10-16).
- **Max 7** open names. If at 7 → no new opens until a slot frees; tell Justin.

Open vs limit: follow that ticker’s **original thesis** from Second brain / Setup. Do not silently switch.

## Decide open / skip

For each stalk (≤3):
1. Read thesis + Setup entry / stop / targets if present.
2. Regime = context only (still may open in Bear/0% exposure if thesis is clear; frame as paper probe).
3. Open only when entry, stop, and R sizing are defined. Else **skip** + reason.
4. Multi-scenario or unclear stop → **ask Justin** — never invent a stop.

## Write state

Update:
- `/workspace/us-swing-sim/state/portfolio.json` — cash, open count, R used
- `/workspace/us-swing-sim/positions/<TICKER>.json` — entry plan, stop, shares, R$, thesis, source paths, open date
- `/workspace/us-swing-sim/journal/YYYY-MM-DD.md` — decisions

Chat to Justin (繁中短): each open/skip line with ticker, shares, entry, stop, R$, reason.



## Stalk = working orders (Justin 2026-10-16)

Rule id `stalk-working-orders-v1` (approved Justin): a Second brain **stalk** means **place a working order immediately**, not watchlist-only and not silent skip.

Ledger layers under `/workspace/us-swing-sim/`:
- `orders/<TICKER>.json` — working limit / buy-stop / conditional (not filled)
- `positions/<TICKER>.json` — filled only
- `watchlist/` — observe-only deferred names (no working order)
- `state/rules.json` — locked portfolio rules
- `state/stalks.json` — mirror of active stalk plans

Each working order must include: side, order_type, **single `limit_price`** (or reclaim level for true conditionals — not vague hold language), stop, shares, R$, trigger, invalidation, expire, `max_stalk_sessions`, paper_probe flag, source paths.
Rule `limit-single-price-v1` + `concrete-plan-v1` (Justin 2026-10-17): **no limit ranges**; entry/stop/size/invalidation must be numbers.

Fill → move to `positions/`, free/adjust R reserved, journal. Invalidate/expire → cancel order, journal. Do not invent stops; missing levels → skip that name + say what is missing.

Deep Bear / 0% exposure: still may place **paper_probe** working orders when thesis is clear; filled risk still counts toward max 7 / R math.



## Stalk lifetime (Justin 2026-10-16) — `stalk-lifetime-v1`

Cancel working order when any fires:
1. Ticket **invalidation** (structure)
2. **5 US sessions** no fill (default `stalk_session_max`)
3. **Earnings −1 session** expire when earnings date set
4. Thesis dead / Setup drop
5. Price left zone — **do not** chase-raise limit

**Regime / Favor:** Regime = reference only. Deep Bear / 0% → `paper_probe` OK; keep working until kill/expire. **Turn not Favor** for that name's sleeve → **cancel that order** (not demote). Regime worsen → do **not** wipe all working. Regime improve → no auto size-up.

Session-close confirmation for kills unless gap through invalidation.

## Logic_Audit on open (`stalk-logic-audit-v1`)

When placing a working order for a Second brain stalk:
1. Create `/workspace/us-swing-sim/logic-audit/<TICKER>.json` (see `logic-audit/FORMAT.md`)
2. `baseline_close` / `baseline_date` = **prior US session close** from TV MCP (or named source / order `ref_close` + `session_close_ref`)
3. `grade` = `追蹤中`, `filled` = `N`; leave T+n / MFE / MAE empty until track
4. Update `logic-audit/_index.json` + Sheet tab **Logic_Audit** row
5. Sync Drive `logic-audit/` mirror when Drive sync runs

## Earnings window (new working orders)

- Do **not** place **NEW** working orders if earnings is within **5 US sessions**.
- Existing stalks still use **earnings−1** expire (`stalk-lifetime-v1`).
- If earnings date unclear → **ask Justin** — do not guess.

## Caps (locked)

- Per-name notional ≤ **20%** equity (`notional-cap-20pct-v1`) — already in Portfolio math.
- **No fill slippage** (Justin 2026-10-16). Do not add +0.15% or similar.


## Concrete plan (`concrete-plan-v1`, Justin 2026-10-17)

Every stalk / working order / position plan MUST specify **numbers**, not vague language:
- single entry `limit_price` (not a range; also `limit-single-price-v1`)
- `stop` (hard)
- `shares`
- `r_usd` (R$)
- hard `invalidation` level or condition
- `max_stalk_sessions` (default **5**)

**Forbidden as fill gates:** vague reclaim wording, "hold EMA" / "reclaim and hold", zone/range limits, "consider" as an entry/fill trigger.
Soft rules (trim consider, time stop) still **ask Justin** — but entry / stop / size / invalidation must be numbers before placing a working order.
Missing any required number → **skip** + say what is missing; do not invent.

## Position fields on fill (`9ema-grace-3sessions-v2`)

When a working order **fills** (or a direct open creates a position), write on `positions/<TICKER>.json`:
- `entry` / fill price, `stop`, `shares`, `r_usd`, `thesis`, `status`, `hard_sl`
- `entry_session_date` — US session date of fill
- `ema9_at_entry` — 9EMA from TV at fill
- `entry_below_9ema` — true iff entry **<** ema9_at_entry; false if entry ≥ 9EMA (**informational only** — grace applies to ALL positions)
- `sessions_held` — **0** at fill (entry day = session 0); track increments on later closes
- Grace: suppress `EMA9_EXIT` while `sessions_held < 3` for **every** fill (Hard SL unaffected)

CRL/DK working orders (0 fills) do not need these fields until fill. Track applies grace using these fields.

## HANDOFF fields (when messaging bots)

`PINNED_INPUTS` / `DECISIONS_MADE` / `OPEN_QUESTIONS` / `NEXT_GATE`

## VERIFY

- [ ] Plan concrete (`concrete-plan-v1`): limit_price + stop + shares + R$ + invalidation + max_stalk_sessions; no vague fill gates
- [ ] ≤7 opens; R ≤ $1,000 per high-conviction name; math = R÷stop% → shares
- [ ] Every number from Setup/handoff/TV — no fabrications
- [ ] Skips named with missing inputs; no invented stops
- [ ] Did not edit Second brain skills, Setup Master, or live broker
- [ ] Ambiguous rules asked to Justin (not silently filled)
- [ ] Each new working order has Logic_Audit JSON + Sheet row; baseline = prior US close
- [ ] No new order if earnings within 5 US sessions (or asked Justin)
- [ ] 20% notional cap applied; slippage still 0
- [ ] On fill: `entry_below_9ema` / `ema9_at_entry` / `entry_session_date` / `sessions_held=0` recorded
