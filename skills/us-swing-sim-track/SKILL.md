---
name: US swing sim track
description: >-
  Use while US swing paper book has open positions: mark with TradingView MCP
  and apply or flag exit rules.
---
# US swing sim track

ONE JOB: Mark open paper positions and apply clear exit rules (or annotate + ask Justin when unclear). Not a live broker.

## Inputs

- Open positions under `/workspace/us-swing-sim/positions/`
- Portfolio state `/workspace/us-swing-sim/state/portfolio.json`
- Working orders `/workspace/us-swing-sim/orders/`
- Prices / EMA: TradingView MCP (prefer over browser). Usage gate: reuse fresh marks; stop after two failed same approaches.

## Exit rules (execute when clear; else ask)

1. Hard SL — session close below stop → full exit. Gap through stop → exit. **Unaffected by 9EMA grace.**
2. +3 sessions from entry — **AUTO** trim 1/3 + move stop to BE (`trim-1-3-be-auto-v1`, Justin 2026-10-22). **Do not ask.** On the post-close pass that first sets `sessions_held >= 3`, queue `pending market_open_sell` for the **next** US cash open (`trim=floor(shares/3)`, remain, stop→entry). Fill @ that session Open (TV MCP; no slippage). Set `trim_1_3_done=true` (once). Skip if already done or pending `TRIM_1_3_BE` exists. Journal `TRIM_1_3` on fill.
3. Close below 9EMA → full exit — **with grace `9ema-grace-3sessions-v2` (Justin 2026-10-20; supersedes below-entry-v1):**
   - **ALL** positions: **suppress** `EMA9_EXIT` while `sessions_held < 3`. First eligible 9EMA exit check is when `sessions_held` reaches **3** (close of the 3rd US session after entry).
   - Applies whether entry was above or below 9EMA at fill (`entry_below_9ema` is informational only — not a grace gate).
   - Session count: `entry_session_date` = US session of fill = **session 0**; `sessions_held` = completed US session closes with date **>** `entry_session_date` (increment on each post-close track pass).
   - Hard SL / gap SL still fire during grace. Time-stop / thesis unchanged. Trim at held=3 is AUTO (rule 2).
4. 5 sessions with neither SL nor target hit → consider time stop; ask Justin if not pre-decided.
5. Thesis / structure invalid → exit.
6. Multi-scenario conflict → ask Justin.

Do not invent new exit rules. If the written rule is ambiguous → ask Justin / 北極星 / 總指揮.

## Actions

For each open name:
1. Pull mark (and 9EMA when needed).
2. If this track pass is a **new** US session close after `entry_session_date`, set `sessions_held` = count of completed US closes with date > `entry_session_date` (do not count entry day).
3. Apply exits: Hard SL / gap first; then 9EMA only if `sessions_held >= 3` (`9ema-grace-3sessions-v2`); then **auto** queue/fill trim 1/3+BE per `trim-1-3-be-auto-v1` when held first hits 3 (and fill any pending `market_open_sell` whose `execute_session` matches this marks session).
4. If a hard/auto rule fires → close/trim in ledger; journal the trigger with price + timestamp (HKT) + exit_reason code.
5. Update position files + portfolio cash/R freed.

## Out

- Updated position/portfolio JSON
- `/workspace/us-swing-sim/journal/YYYY-MM-DD.md` append
- Short Traditional Chinese chat: what fired, what is watching

## Working orders (pre-fill)

Also scan `/workspace/us-swing-sim/orders/` each track pass:
1. Mark with TV MCP (or named source).
2. If limit or conditional trigger **fills** per order_type → open position file, remove/cancel working order, journal fill price + HKT time, update portfolio cash/R.
   - **`limit_buy` (`limit-single-price-v1` + `concrete-plan-v1`):** session Low ≤ `limit_price` → fill @ `limit_price` (no slippage). No vague reclaim/hold-EMA/zone fill gates.
   - **`market_open_sell` (trim):** when marks session == `execute_session`, fill @ session Open; apply remain shares + BE stop; set `trim_1_3_done`.
   On buy fill, **required** on `positions/<T>.json` for `9ema-grace-3sessions-v2`:
   - `entry_session_date` — US session calendar date of fill
   - `ema9_at_entry` — 9EMA at fill (TV MCP)
   - `entry_below_9ema` — `true` if fill/entry price **<** `ema9_at_entry`, else `false` (informational only; not a grace gate)
   - `sessions_held` — start at **0** (entry day = session 0); increment only on later session closes
   - Grace: EMA9_EXIT suppressed for **all** positions while `sessions_held < 3`
3. If invalidation or expire hits → cancel order, journal, do not invent a new entry.
3b. **`limit-away-5pct-cancel-v1` (Justin 2026-10-22):** using session **Close** only — buy limit: if `Close >= limit_price × 1.05` → AUTO cancel (no ask); sell limit: if `Close <= limit_price × 0.95` → AUTO cancel. Journal CANCEL; free R reserved; Logic_Audit `未到價過期`; drop from TV us shortlist. Do not chase-raise the limit.
4. Soft ambiguity on whether fill occurred → ask Justin.

## Concrete plan check (`concrete-plan-v1`, Justin 2026-10-17)

Working orders scanned on track must already carry concrete numbers: single `limit_price`, `stop`, `shares`, `r_usd`, hard `invalidation`, `max_stalk_sessions` (default 5).
Do **not** treat vague reclaim / "hold EMA" / zone ranges / "consider" as fill gates.
If an order is missing required numbers → do not invent; cancel or ask Justin. Time-stop still asks Justin; trim 1/3+BE at held=3 is AUTO.

## Stalk lifetime on track pass (`stalk-lifetime-v1`)

For each working order: increment session count on US session close marks; cancel if sessions≥5, invalidation, earnings−1 expire, thesis dead, left zone, or `limit-away-5pct-cancel-v1` (Close ≥5% past limit). If that name's sleeve **Turn not Favor** → cancel that order. Do not wipe all orders solely because regime band worsened.

## Daily order (fixed)

On each post-close track pass, in this order only:
1. **Mark + exit** open positions (hard SL / gap / 9EMA / **auto trim 1/3+BE** / thesis)
2. **Working orders** — fills (incl. pending `market_open_sell`) / cancels / lifetime kills
3. **Logic_Audit** — update T+n / MFE / MAE for all active stalks in `logic-audit/`
4. **Expire** stalks ≥5 sessions without fill → set grade `未到價過期` (and cancel working order if still open)
5. Sync Sheet (incl. **Logic_Audit** + **Dashboard**) + Drive mirror
   - **Single writer (mandatory):** move any closed positions to `closed/` first, then run `python3 /workspace/us-swing-sim/tools/sync_sheet.py`. Apply `.sheet_payloads/apply_plan.json` via Google Sheets MCP (`batch_clear_values` / `clear_range` + `write_range` parseInput=true using `$file:..._write.json` payloads). **No ad-hoc cell patches.** Contract: `/workspace/us-swing-sim/SHEET_CONTRACT.md`.
   - Equity curve UPSERT lives in `state/equity_curve.json` (script maintains it). Charts 1051207710 / 607204741 updated by apply_plan. Journal leave alone.
6. **TradingView us shortlist sync** (`tv-us-shortlist-sync-v1`) — see section below

## TradingView us shortlist sync (`tv-us-shortlist-sync-v1`, Justin 2026-10-20)

**Mandatory final step** after Sheet + Drive sync on every post-close track pass.
1. Build desired set = union of tickers in `positions/` + `orders/` (working) + `watchlist/` (skip FORMAT/_TEMPLATE/_index).
2. Map to `EXCHANGE:TICKER` via known map (NYSE:CRL, NYSE:DK, NASDAQ:FRSH, NASDAQ:LIFE, NASDAQ:AUGO) or `mcp-tv-search-symbols` (stock) for unknowns.
3. `mcp-watchlist-get-watchlist` id **`351605193`** (`us shortlist`).
4. **Add** missing symbols (`mcp-watchlist-add-to-watchlist`); **remove** any TV symbol not in desired set (`mcp-watchlist-remove-from-watchlist`).
5. Journal OPS: TV us shortlist sync — added […] / removed […] (or no-op).

## Exit reason codes (journal on close)

When closing or trimming a position, write one of:
`HARD_SL` | `GAP_SL` | `TRIM_1_3` | `EMA9_EXIT` | `TIME_STOP` | `THESIS_INVALID` | `OTHER`

Put the code in the position close record and Journal line. Keep close-based SL (session close below stop / gap through) — **not** Low≤stop. Keep **9EMA** full exit — **not** 20MA — subject to `9ema-grace-3sessions-v2` (all positions; first 3 sessions). Trim 1/3+BE at held=3 is AUTO (`trim-1-3-be-auto-v1`). Time stop remains ask-Justin unless pre-decided.

## Logic_Audit update (`stalk-logic-audit-v1`)

For each active file under `/workspace/us-swing-sim/logic-audit/` (status grade `追蹤中` or still in window):
1. Pull TV marks (close; track high/low for MFE/MAE when available)
2. Compute return_pct vs `baseline_close` for T+1 / T+3 / T+5 when those sessions have elapsed since `baseline_date`
3. Update `mfe_pct` / `mae_pct` over ≤5 US sessions
4. On fill → `filled=Y` (grade may stay `追蹤中` until path clear, or set `精準到價` when trigger+favorable)
5. On cancel for structure/thesis/Favor-fade → grade `結構作廢`
6. On stop-out after trigger → grade `假突破止蝕`
7. On ≥5 sessions / expire no fill → grade `未到價過期`
8. Write JSON + Sheet **Logic_Audit** + `_index.json`; sync Drive

## Cadence
**Pre-open (Justin 2026-10-22):** before each US cash open, pull TV premarket marks and decide GO/HOLD/WATCH_GAP/CANCEL on pending MOO (trim+BE), open Hard-SL gap risk, and working limits. Write `state/pre_open_latest.json` + journal. Do **not** invent open fills — fills still at Open print. Routine: `us-swing-sim-pre-open-check` (~21:00 HKT Mon–Fri).

Justin standing ask: after each US cash close, run this skill (routine `us-swing-sim-post-close-track`, ~05:00 HKT Tue–Sat). Sync Drive + Google Sheet after ledger updates, then sync TradingView **us shortlist** (`tv-us-shortlist-sync-v1`).

## VERIFY

- Concrete plan on working orders (`concrete-plan-v1`): no vague reclaim/hold-EMA/zone/consider fill gates
- Marks from TV MCP (or named source) — no invented prints
- Hard SL / 9EMA / gap / auto-trim rules applied or explicitly deferred with reason
- If `sessions_held < 3` → do **not** `EMA9_EXIT` on close below 9EMA (grace v2, all positions); still apply Hard SL / gap
- When `sessions_held` first hits 3 and `trim_1_3_done` false → queue/fill trim+BE without asking (`trim-1-3-be-auto-v1`)
- Time-stop still ask-Justin unless pre-decided
- Ledger matches chat; max 7 still held
- No live orders; no Second brain skill edits
- Daily order respected: exits → fills → Logic_Audit → expire → Sheet/Drive (incl. **Dashboard**) → TV us shortlist sync
- Dashboard marks_session == Book/portfolio marks_session after sync
- Sheet sync = `sync_sheet.py` full rebuild only (not one-off write_range patches); OPEN has no ghost closed tickers (AUGO/DK etc.)
- Book NAV / open tickers match `state/portfolio.json` + `positions/` exactly
- TV `us shortlist` (351605193) matches union of open positions + working orders + watchlist stalks (extras removed)
- Exit reason codes written on closes; Logic_Audit T+n/MFE/MAE updated
- No Low≤stop SL; no 20MA exit; no slippage on fills
- New fills carry `entry_below_9ema` / `ema9_at_entry` / `entry_session_date` / `sessions_held`
- Working limits: Close ≥5% past limit → cancelled (`limit-away-5pct-cancel-v1`); no ask
