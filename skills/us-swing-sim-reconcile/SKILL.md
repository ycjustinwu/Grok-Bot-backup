---
name: US swing sim reconcile
description: >-
  Use weekly or when Justin asks for US swing paper book P and L, adherence, and
  outside-judge stats vs verdict distribution (verdicts_US.jsonl ground truth).
---
# US swing sim reconcile

ONE JOB: Produce an auditable paper reconcile — P and L, rule adherence, and outside-judge metrics vs Hermes verdict distribution. Optional Work Verifier on high-stakes.

## Tradeable / post-gate note

After Tradeable hard-gate, expect more **WATCH** names (FAIL demotions with `Tradeable_Why`). Reconcile must tolerate **113-col** Contract; do not invent targets; ground truth remains `verdicts_US.jsonl`. Post-gate WATCH inflation is expected — do not treat it as book error alone.

## Inputs

- `/workspace/us-swing-sim/state/portfolio.json`
- `/workspace/us-swing-sim/positions/` + closed trades journal
- **Ground truth:** Drive `US_Stock_Data/<Mon D>/verdicts_US.jsonl` for the sessions under review (PINNED)
- Supporting: `Contract_US.csv`, `Trigger_US.csv`, `index.md` (conclusions only)
- Regime band/exposure at entry dates (reference only)

Do **not** PIN Market Master Setup_Latest or `/workspace/us-swing-setup/` as path truth for new reconciles.

## Report (Traditional Chinese short; numbers English OK)

1. Book snapshot — equity vs 100000 USD start, open names (max 7), R in use
2. Closed trades — ticker, entry, exit, R multiple, trigger (SL / 9EMA / SUPPLY_HALF / trim / time / thesis / other)
3. Rule adherence — any broken hard rule? list; soft consider outcomes
4. **Outside judge A — P&L vs verdict distribution** — BUY / STALK / WATCH / AVOID each at **5d** and **10d**; ground truth = `verdicts_US.jsonl`. No padding.
5. **Outside judge B — exit character** — count SL-hit exits vs Supply_Level touch / room-exhaustion (favorable) exits; show both counts and rate. No invented target-column language.

Save: `/workspace/us-swing-sim/reconcile/YYYY-MM-DD.md`

Deliver via chat to Justin and/or 總指揮 as asked. 北極星 does not execute this book.

## Dashboard extras

When enough data exists (still no fabricate):
1. **Expectancy / trade** — mean R multiple of closed trades
2. **Max drawdown estimate** — peak-to-trough on equity curve from ledger
3. **SPY buy-and-hold** over the same window — marks from TV MCP; cite source

## Sample discipline

If **closed trades < 30**: state clearly「樣本不足，唔下 setup／exit 結論」. Rankings / grade leaderboards are **observational only**. Same for Logic_Audit closed audits n<30.

## Outside judge C (Logic_Audit grades)

Optional short section separate from P&L:
- Counts: 精準到價 / 假突破止蝕 / 未到價過期 / 結構作廢 / 追蹤中
- Do **not** mix with Outside judge A/B P&L conclusions
- If n<30 → counts only, no quality verdict

## Earnings-through trades

If a position was **held through earnings**, tag it (`earnings_through=Y`). Exclude from **main** expectancy line, or show a **separate** expectancy line. Never silently blend.

## High-stakes

When Justin/總指揮 flags high-stakes (or large drawdown / rule-break batch) → hand to Work Verifier (`037de516-dbc1-4565-a127-5dbb0f691729`) before treating as final. Include PINNED_INPUTS, DECISIONS_MADE, OPEN_QUESTIONS, NEXT_GATE.

## VERIFY

- Outside judge A uses verdict distribution from `verdicts_US.jsonl` (5d/10d per class)
- Outside judge B uses Supply_Level / room exhaustion vs SL — no invented target-column / invented targets
- PINNED_INPUTS lists exact Drive verdicts/Contract/state files used
- Banned tokens absent: Hermes-deleted underscore fields (risk-reward ratio*, target-N*, setup-type*, adjusted-stop*)
- No fabricated P and L; math ties to position files
- Did not rescore regime or edit Hermes Contract/verdicts
- Ambiguities under OPEN_QUESTIONS — not silently resolved
- If closed trades <30 → 樣本不足 stated
- Outside judge C grade counts separate from P&L when Logic_Audit present
- Earnings-through trades tagged and split from main expectancy
- SPY B&H / DD / expectancy sourced — no fabrications
