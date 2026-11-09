---
name: US swing sim track
description: >-
  Use while US swing paper book has open positions: mark with TradingView MCP
  and apply or flag exit rules (incl. Supply_Level / Room exhaustion half-trim).
---
# US swing sim track

ONE JOB: Mark open paper positions and apply clear exit rules (or annotate + ask Justin when unclear). Not a live broker.

## Inputs

- Open positions under `/workspace/us-swing-sim/positions/`
- Portfolio state `/workspace/us-swing-sim/state/portfolio.json`
- Working orders `/workspace/us-swing-sim/orders/`
- Position fields for supply: `Supply_Level`, remaining `Room_To_Supply_R` when recorded at open / from Contract
- Prices / EMA: TradingView MCP (prefer over browser). Usage gate: reuse fresh marks; stop after two failed same approaches.

## Exit rules (execute when clear; else ask)

1. Hard SL — session close below stop → full exit. Gap through stop → exit. **Unaffected by 9EMA grace.**
2. +3 sessions from entry — **AUTO** trim 1/3 + move stop to BE (`trim-1-3-be-auto-v1`, Justin 2026-10-22). **Do not ask.** On the post-close pass that first sets `sessions_held >= 3`, queue `pending market_open_sell` for the **next** US cash open (`trim=floor(shares/3)`, remain, stop→entry). Fill @ that session Open (TV MCP; no slippage). Set `trim_1_3_done=true` (once). Skip if already done or pending `TRIM_1_3_BE` exists. Journal `TRIM_1_3` on fill.
3. Close below 9EMA → full exit — **with grace `9ema-grace-3sessions-v2` (Justin 2026-10-20):**
   - **ALL** positions: **suppress** `EMA9_EXIT` while `sessions_held < 3`. First eligible 9EMA exit check is when `sessions_held` reaches **3**.
   - Hard SL / gap SL still fire during grace. Time-stop / thesis unchanged. Trim at held=3 is AUTO (rule 2).
4. **Supply / room exhaustion (v5.5.2):** when price reaches `Supply_Level`, **or** remaining `Room_To_Supply_R ≤ 0.3` → **reduce half**. Journal `SUPPLY_HALF` (or equivalent). Soft-replace any “neither SL nor target hit” wording → **neither SL nor Supply_Level / room exhaustion**.
5. 5 sessions with neither SL nor Supply_Level / room exhaustion → consider time stop; ask Justin if not pre-decided.
6. Thesis / structure invalid → exit.
7. Multi-scenario conflict → ask Justin.

Do not invent new exit rules. Do not invent targets. If the written rule is ambiguous → ask Justin / 北極星 / 總指揮.

## Actions

For each open name:
1. Pull mark (and 9EMA when needed).
2. If this track pass is a **new** US session close after `entry_session_date`, set `sessions_held` = count of completed US closes with date > `entry_session_date`.
3. Apply exits: Hard SL / gap first; then Supply_Level / Room≤0.3 half; then 9EMA only if `sessions_held >= 3`; then **auto** queue/fill trim 1/3+BE when held first hits 3.
4. If a hard/auto rule fires → close/trim in ledger; journal the trigger with price + timestamp (HKT) + exit_reason code.
5. Update position files + portfolio cash/R freed.

## Out

- Updated position/portfolio JSON
- `/workspace/us-swing-sim/journal/YYYY-MM-DD.md` append
- Short Traditional Chinese chat: what fired, what is watching

## Working orders (pre-fill)

Also scan `/workspace/us-swing-sim/orders/` each track pass:
1. Mark with TV MCP (or named source).
2. If limit or conditional / buy-stop trigger **fills** per order_type → open position file, remove/cancel working order, journal fill + HKT time, update portfolio.
   - **`limit_buy`:** session Low ≤ `limit_price` → fill @ `limit_price` (no slippage).
   - **buy-stop (STALK):** honor `Trigger_Price` / `Trigger_Min_Vol` / void if fill-day low ≤ `BuyStop_Max_Stop`.
   - **`market_open_sell` (trim):** when marks session == `execute_session`, fill @ session Open; apply remain shares + BE stop; set `trim_1_3_done`.
   On buy fill, **required** on `positions/<T>.json` for `9ema-grace-3sessions-v2`:
   - `entry_session_date`, `ema9_at_entry`, `entry_below_9ema`, `sessions_held=0`
   - Carry `Supply_Level` / `Room_To_Supply_R` from open plan when available
3. If invalidation or expire hits → cancel order, journal, do not invent a new entry.
3b. **`limit-away-5pct-cancel-v1`:** Close ≥ limit×1.05 (buy) → AUTO cancel; sell ≤ limit×0.95 → AUTO cancel.
4. Soft ambiguity on whether fill occurred → ask Justin.

## Concrete plan check (`concrete-plan-v1`)

Working orders must carry concrete numbers. Do **not** treat vague reclaim / "hold EMA" / zone ranges / "consider" as fill gates. Missing numbers → cancel or ask Justin.

## Stalk lifetime on track pass (`stalk-lifetime-v1`)

Increment session count; cancel if sessions≥5, invalidation, earnings−1, thesis dead, left zone, or `limit-away-5pct-cancel-v1`. Sleeve **Turn not Favor** → cancel that order. Do not wipe all orders solely because regime band worsened.

## Daily order (fixed)

1. **Mark + exit** open positions (hard SL / gap / Supply half / 9EMA / **auto trim 1/3+BE** / thesis)
2. **Working orders** — fills / cancels / lifetime kills
3. **Logic_Audit** — T+n / MFE / MAE
4. **Expire** stalks ≥5 sessions without fill → `未到價過期`
5. Sync Sheet + Drive via `python3 /workspace/us-swing-sim/tools/sync_sheet.py` (single writer; contract `/workspace/us-swing-sim/SHEET_CONTRACT.md`)
6. **TradingView us shortlist sync** (`tv-us-shortlist-sync-v1`) — watchlist id `351605193`

## Exit reason codes

`HARD_SL` | `GAP_SL` | `TRIM_1_3` | `SUPPLY_HALF` | `EMA9_EXIT` | `TIME_STOP` | `THESIS_INVALID` | `OTHER`

Keep close-based SL (session close below stop / gap) — **not** Low≤stop. Keep **9EMA** full exit — **not** 20MA — subject to grace. Trim 1/3+BE at held=3 is AUTO. Time stop remains ask-Justin unless pre-decided.

## Logic_Audit update (`stalk-logic-audit-v1`)

Update T+1/T+3/T+5, MFE/MAE; grades 精準到價 / 假突破止蝕 / 未到價過期 / 結構作廢 / 追蹤中.

## Cadence

**Pre-open:** routine `us-swing-sim-pre-open-check` (~21:00 HKT Mon–Fri).
**Post-close:** routine `us-swing-sim-post-close-track` (~05:00 HKT Tue–Sat).

## W44 permanent gates (`RULES-20261101-W44`)

1. `better-price-v1` + `better-price-stop-reanchor-v1` — better fill → AUTO recompute stop + R$.
2. `limit-away-5pct-cancel-v1`
3. `sheet-readback-done-v1`
4. `post-trim-hold-v1` — trimmed ≥5 sessions: HOLD until BE/Hard SL or EMA9_EXIT; no time-stop ask.
5. `weekly-exec-eval-v1`

## VERIFY

- Concrete plan on working orders; no vague fill gates
- Marks from TV MCP — no invented prints
- Hard SL / Supply half / 9EMA / gap / auto-trim applied or explicitly deferred
- If `sessions_held < 3` → do **not** `EMA9_EXIT`; still apply Hard SL / gap / Supply half
- When `sessions_held` first hits 3 and `trim_1_3_done` false → queue/fill trim+BE without asking
- Time-stop still ask-Justin unless pre-decided; phrase uses Supply_Level / room exhaustion (not “target”)
- Banned tokens absent: Hermes-deleted underscore fields (risk-reward ratio*, target-N*, setup-type*, adjusted-stop*)
- Ledger matches chat; max 7 held; no live orders
- Daily order respected; Sheet = `sync_sheet.py` full rebuild only
- TV `us shortlist` matches positions + orders + watchlist
- Exit reason codes written; Logic_Audit updated
- W44 better-price stop reanchor + sheet readback done
