---
name: US swing sim reconcile
description: >-
  Use weekly or when Justin asks for US swing paper book P and L, adherence, and outside-judge stats.
---
# US swing sim reconcile

ONE JOB: Produce an auditable paper reconcile — P and L, rule adherence, and two outside-judge metrics. Optional Work Verifier on high-stakes.

## Inputs

- `/workspace/us-swing-sim/state/portfolio.json`
- `/workspace/us-swing-sim/positions/` + closed trades journal
- Market Master `Setup_Latest` (`1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`) / PINNED Setup paths used at entry (must list under PINNED_INPUTS)
- Regime band/exposure at entry dates (reference only)

## Report (Traditional Chinese short; numbers English OK)

1. Book snapshot — equity vs 100000 USD start, open names (max 7), R in use
2. Closed trades — ticker, entry, exit, R multiple, trigger (SL / 9EMA / trim / time / thesis / other)
3. Rule adherence — any broken hard rule? list; soft consider outcomes
4. Outside judge A — paper P and L vs Market Master Setup_Latest path (planned entry/stop/targets vs what the book did)
5. Outside judge B — setup failure rate: count SL-hit exits vs target-hit (or favorable) exits; show both counts and rate. No padding.

Save: `/workspace/us-swing-sim/reconcile/YYYY-MM-DD.md`

Deliver via chat to Justin and/or 總指揮 as asked. 北極星 does not execute this book.


## Dashboard extras

When enough data exists (still no fabricate):
1. **Expectancy / trade** — mean R multiple of closed trades
2. **Max drawdown estimate** — peak-to-trough on equity curve from ledger
3. **SPY buy-and-hold** over the same window — marks from TV MCP (or named source); cite source

## Sample discipline

If **closed trades &lt; 30**: state clearly「樣本不足，唔下 setup／exit 結論」. Rankings / grade leaderboards are **observational only**. Same for Logic_Audit closed audits n&lt;30 (`stalk-logic-audit-v1`).

## Outside judge C (Logic_Audit grades)

Optional short section separate from P&L:
- Counts: 精準到價 / 假突破止蝕 / 未到價過期 / 結構作廢 / 追蹤中
- Do **not** mix with Outside judge A/B P&L conclusions
- If n&lt;30 → counts only, no quality verdict

## Earnings-through trades

If a position was **held through earnings**, tag it (`earnings_through=Y`). Exclude from **main** expectancy line, or show a **separate** expectancy line. Never silently blend with non-earnings trades.

## High-stakes

When Justin/總指揮 flags high-stakes (or large drawdown / rule-break batch) → hand to Work Verifier (id 037de516-dbc1-4565-a127-5dbb0f691729) before treating as final. Include PINNED_INPUTS, DECISIONS_MADE, OPEN_QUESTIONS, NEXT_GATE.

## VERIFY

- Both outside-judge sections have real counts/numbers from the ledger
- PINNED_INPUTS lists exact Setup/state files used
- No fabricated P and L; math ties to position files
- Did not rescore regime or edit Market Master / Setup_Latest
- Ambiguities listed under OPEN_QUESTIONS — not silently resolved
- If closed trades <30 → 樣本不足 stated; no setup/exit conclusions
- Outside judge C grade counts separate from P&L when Logic_Audit present
- Earnings-through trades tagged and split from main expectancy
- SPY B&H / DD / expectancy sourced — no fabrications

