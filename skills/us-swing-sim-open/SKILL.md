---
name: US swing sim open
description: >-
  Use when Second brain hands ≤3 US stalks / Hermes §3.3 handoff, or Justin asks
  to open/skip paper positions in the US swing 模擬倉 book from verdicts_US.jsonl +
  Trigger/Contract (四問 + STALK buy-stop; no Setup Master).
---
# US swing sim open

ONE JOB: Decide open or skip for each Second brain stalk in the $100k US swing paper book using Hermes gated verdicts + Trigger params, size with Risk=R, and write ledger state. Not live trading.

## Inputs (read-only)

### Required Hermes Drive (session Date)
- `Drive US_Stock_Data/<Mon D>/verdicts_US.jsonl` — **unique entry gate**. Missing → today **`NO_TRADE`**, journal only (do not fall back to baseline / L2_Input alone).
- `Drive US_Stock_Data/<Mon D>/Trigger_US.csv` — buy-stop params for STALK (`Trigger_Price`, `Trigger_Min_Vol`, `BuyStop_Max_Stop`).
- `Drive US_Stock_Data/<Mon D>/Contract_US.csv` — price truth. Copy entry/stop; never recompute from ATR. `keep_default_na=False`.
- `Drive US_Stock_Data/<Mon D>/index.md` — conclusions only; **do not order from §③** (A2). Never treat ✅ as buyable (A3).
- If `L2_Check_Report.md` has FAIL → today **`NO_TRADE`**, notify Justin.
- **Tradeable gate (when col present):** open only if `Tradeable==PASS` **or** ticker is in `Trigger_US.csv` (PASS-only set). `Tradeable FAIL` → skip / no open. Never invent targets to clear the gate. Contract may be **113 cols**.

Folder Date must match Contract `Date`.

### Second brain + book
- `/workspace/second-brain/YYYY-MM-DD/` — ≤3 stalks as Hermes §3.3 handoff blocks
- Regime band + exposure only: `/workspace/regime-output/YYYY-MM-DD/` (fallback `/workspace/market-awareness/...`). Reference only — do not rescore.
- Current book: `/workspace/us-swing-sim/state/portfolio.json` and `/workspace/us-swing-sim/positions/`

**Do not** PIN `/workspace/us-swing-setup/` or Market Master Setup_Latest as entry truth (US Setup deprecated). Historical Setup artifacts are archaeology only.

If handoff or required Contract/Trigger levels for a name are missing → skip that name and say what is missing. Do not invent entry/stop.

## Portfolio math (fixed — keep verbatim)

- Portfolio equity: **$100,000** USD (paper)
- High-conviction max risk **R = 1% = $1,000**
- `stop% = |entry − stop| / entry`  (numbers copied from Contract / handoff)
- `R$ = min(0.01 × 100000, 0.20 × 100000 × stop%)`
- `shares = floor(R$ / (entry − stop))` (whole shares unless Justin says otherwise)
- **Per-name notional cap 20%** of equity ($20,000 on $100k). If `shares × entry > 0.20 × equity`, resize `shares = floor(0.20 × equity / entry)` and record effective_R. (Justin 2026-10-16; `notional-cap-20pct-v1`)
- **No fill slippage** on paper marks.
- **Max 7** open names. If at 7 → no new opens until a slot frees; tell Justin.

Acceptance math anchor (Hermes §3.4 UNTY 2026-11-05): entry 58.10, stop 56.654 → stop% 2.49%, R$ 497.76, shares 344.

Open vs limit: follow that ticker’s **original thesis** from Second brain handoff / Contract. Do not silently switch.

## 開倉前四問 (every name)

Before open / working order:

1. verdict ∈ {BUY, STALK} — never open WATCH/AVOID; never upgrade them.
1b. When Tradeable col present: `Tradeable==PASS` or in Trigger_US; else skip.
2. `Risk_OK=PASS` and `Earnings_Proximity_Flag` not in {PASS, UNKNOWN} — **A1: PASS → always skip**.
3. `Room_To_Supply_R ≥ 1.0` — if 1.0–1.5 → **half size** + tag `thin_room`.
4. if `Supply_Soft_Level` within <0.5R of entry → tag `soft_overhead`.

Fail any hard gate → **skip** + reason.

## STALK (`Entry_Feasible=NOT_YET`)

- **No market open.**
- Place buy-stop at `Trigger_Price`, size with volume ≥ `Trigger_Min_Vol`.
- Void if fill-day low ≤ `BuyStop_Max_Stop`.
- Missing `Trigger_US.csv` row/params → skip (`no trigger params`).

## Decide open / skip

For each stalk (≤3):
1. Confirm verdict in `verdicts_US.jsonl` (wins over baseline / index).
2. Copy entry/stop from Contract / Trigger / Second brain handoff block — never recompute from ATR; never invent targets.
3. Pass 開倉前四問.
4. Regime = context only (still may open in Bear/0% if thesis clear; frame as paper probe).
5. Open / working order only when entry, stop, and R sizing are defined. Else **skip** + reason.
6. Multi-scenario or unclear stop → **ask Justin** — never invent a stop.

## Write state

Update:
- `/workspace/us-swing-sim/state/portfolio.json`
- `/workspace/us-swing-sim/positions/<TICKER>.json` (filled) or `orders/<TICKER>.json` (working)
- `/workspace/us-swing-sim/journal/YYYY-MM-DD.md`

Chat to Justin (繁中短): each open/skip line with ticker, shares, entry, stop, R$, reason. Header: `OPEN x/7 · cash · R reserved · working notional`.

## Stalk = working orders (Justin 2026-10-16)

Rule `stalk-working-orders-v1`: a Second brain **stalk** means **place a working order immediately** when gates pass — not watchlist-only silent skip.

Ledger layers under `/workspace/us-swing-sim/`:
- `orders/<TICKER>.json` — working limit / buy-stop / conditional
- `positions/<TICKER>.json` — filled only
- `watchlist/` — observe-only
- `state/rules.json` · `state/stalks.json`

Each working order must include: side, order_type, **single `limit_price`** (or Trigger_Price for buy-stop), stop, shares, R$, trigger, invalidation, expire, `max_stalk_sessions`, paper_probe flag, source paths.
Rules `limit-single-price-v1` + `concrete-plan-v1`: **no limit ranges**; entry/stop/size/invalidation must be numbers.

## Stalk lifetime (`stalk-lifetime-v1`)

Cancel when: ticket invalidation · **5 US sessions** no fill · **Earnings −1 session** · thesis dead · price left zone (do not chase-raise).

Regime = reference. Deep Bear / 0% → `paper_probe` OK. **Turn not Favor** for that sleeve → cancel that order. Regime worsen → do not wipe all working.

## Logic_Audit on open (`stalk-logic-audit-v1`)

Create `/workspace/us-swing-sim/logic-audit/<TICKER>.json`; baseline = prior US session close; sync Sheet **Logic_Audit**.

## Earnings window (new working orders)

- Do **not** place **NEW** working orders if earnings within **5 US sessions** (or flag PASS/UNKNOWN already skipped by 四問).
- Existing stalks still use **earnings−1** expire.
- If earnings date unclear → **ask Justin**.

## Concrete plan (`concrete-plan-v1`)

Every plan MUST specify numbers: single entry/limit, stop, shares, r_usd, hard invalidation, max_stalk_sessions (default **5**).
Forbidden as fill gates: vague reclaim wording, "hold EMA", zone/range limits, "consider" as fill trigger.
Missing any required number → **skip**; do not invent.

## Position fields on fill (`9ema-grace-3sessions-v2`)

On fill write: `entry`, `stop`, `shares`, `r_usd`, `thesis`, `hard_sl`, `entry_session_date`, `ema9_at_entry`, `entry_below_9ema`, `sessions_held=0`. Grace suppresses `EMA9_EXIT` while `sessions_held < 3` for every fill (Hard SL unaffected).

## W44 permanent gates (`RULES-20261101-W44`)

1. `away-at-place-observe-v1` — Close ≥5% past L → OBSERVE only.
2. `cash-slot-pregate-v1` — Σ working notional ≤ cash AND open+working ≤ 7.
3. `soft-final-crowding-header-v1` — header OPEN x/7 · cash · R reserved · working notional.
4. `soft-final-void-authorize-v1` — void only with AUTHORIZE.
5. `no-reopen-3sess-v1` — cooldown / size-down exception.
6. `sheet-readback-done-v1` — Sheet readback if Positions/Dashboard changed.
7. `weekly-exec-eval-v1` — Sunday eval reminder.

## HANDOFF fields

`PINNED_INPUTS` / `DECISIONS_MADE` / `OPEN_QUESTIONS` / `NEXT_GATE` — PINNED must name exact Drive files for the session Date (`verdicts_US.jsonl`, `Contract_US.csv`, `Trigger_US.csv`, …).

## VERIFY

- [ ] `verdicts_US.jsonl` present else `NO_TRADE` only; L2 check FAIL → `NO_TRADE`
- [ ] 開倉前四問 applied; Tradeable PASS or Trigger membership when col present; A1 PASS skip; no WATCH/AVOID upgrades
- [ ] Plan concrete: limit/Trigger + stop + shares + R$ + invalidation + max_stalk_sessions
- [ ] Portfolio math unchanged ($100k / R=1% / 20% cap / whole shares / no slippage)
- [ ] Entry/stop copied from Contract/Trigger/handoff — no ATR invent; no invented targets
- [ ] STALK = buy-stop rules; missing Trigger → `no trigger params`
- [ ] Banned tokens absent: Hermes-deleted underscore fields (risk-reward ratio*, target-N*, setup-type*, adjusted-stop*)
- [ ] Did not edit Hermes Contract/verdicts; no Setup Master; no live broker
- [ ] W44 gates checked; Logic_Audit on new working orders
- [ ] PINNED_INPUTS lists exact Drive paths
