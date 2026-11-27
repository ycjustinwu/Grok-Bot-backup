---
name: US second-brain 3 picks
description: >-
  Use when Hermes Drive US session is ready (L2_Input + verdicts + index) or
  Justin/總指揮 asks on demand: shortlist ≤3 US stalks from Hermes facts into the
  §3.3 handoff block (Tradeable PASS + Room_To_Supply_R / Setup_Quality_Grade —
  never RR/targets).
---
# US second-brain 3 picks

ONE JOB: Build Justin’s daily US attention shortlist (≤3 stalks) from Hermes Drive session facts + context stack, emit **only** the Hermes §3.3 handoff block per stalk, then a short X dig. Discussion stays in the **Second brain** bot chat.

Not advice. Stalk / observe framing. Deep Bear = probe-only mindset until exposure >0% — still hunt gems.

Default trigger: **Hermes Drive session ready** (`Drive US_Stock_Data/<Mon D>/` has `L2_Input.csv` + `verdicts_US.jsonl` + `index.md`) or Justin/總指揮 on demand. **Not** US Swing Scanner handoff (Scanner US chain deprecated v5.5.2).


## Script-first (required)

Before any LLM ranking / §3.3 drafting from raw Hermes CSV/jsonl:

1. Ensure the session pack is local (Drive MCP download — see `/workspace/second-brain/scripts/download_notes.md`).
2. Run the single command (sibling `soft_final_draft.py` is imported automatically):

```bash
python3 /workspace/second-brain/scripts/hermes_soft_final.py \
  --pack-dir <local-hermes-pack> \
  --out-dir /workspace/second-brain/YYYY-MM-DD \
  --prior-dir <optional previous Soft out-dir> \
  --prior-pack-dir <optional previous Hermes pack> \
  --drive-folder <optional Drive folder URL or id> \
  --book TEM@72.21,UNTY@57.46
```

`--prior-dir` / `--prior-pack-dir` auto-discover when `--out-dir` is `/workspace/second-brain/YYYY-MM-DD`. `--run-date` defaults to today Asia/Hong_Kong; `--tc` defaults to `TC-YYYYMMDD-SB-novN`.

3. Read `attention-3-picks.draft.md` + `judgment_flags.json` first, then `ranked_candidates.json` + `handoff_blocks.md` + `handoff_blocks.script.md` + `script_verify.json` as needed. `soft_final_stub.md` is a deprecated one-line pointer — do not fill old PLACEHOLDERs.
4. **LLM must NOT re-rank from raw CSV/jsonl when script output exists.** Start from the draft + `judgment_flags.json`. May **confirm or undo a soft demote** of a script STALK (soft-demote is a draft suggestion only; `ranked_candidates.json` / `handoff_blocks.script.md` keep the pre-demote script stalks). Never upgrade WATCH/AVOID; never invent prices/targets — Contract copy in handoff wins. Do not recap regime / US Brief / Market Master / RS overview. Do not load those full reports unless a flag says a conflict must be checked. Never treat index BUY as buyable (`verdicts_US.jsonl` wins). If `story_in_pack` is set, no further S4 unless Justin asks. Never auto-wake 模擬倉.
5. If script exit `2` (missing/date mismatch) → stop and report. Exit `3` (no *script* survivors) → Soft Final **cannot find**; do not pad. Exit `0` with draft Soft stalks = 無 after soft-demote is also cannot-find — do not pad.

Docs: `/workspace/second-brain/scripts/README.md`.

## Required sources

### Primary (Hermes — must be present for the session Date)
1. **Drive `US_Stock_Data/<Mon D>/L2_Input.csv`** — baseline / quality / Speak_Up (Second brain primary setup source).
2. **Drive `US_Stock_Data/<Mon D>/verdicts_US.jsonl`** — if present, **authoritative** gated verdicts (wins over index §③ / baseline). Missing → may still draft handoff notes but **do not** hand names to 模擬倉 for open.
3. **Drive `US_Stock_Data/<Mon D>/index.md`** — daily book conclusions only. **Do not order from index §③** (Hermes A2). Never treat ✅ as buyable (Hermes A3).
4. **Drive `US_Stock_Data/<Mon D>/Contract_US.csv`** — price truth. Copy levels; never recompute. Read CSV with `keep_default_na=False`.

Folder Date must match Contract `Date`. Wrong folder → stop and report.

### Context (still required when available; missing → note, do not invent)
5. **Regime** — latest Market Awareness / regime-daily for the US close.
6. **US Market Daily Brief** — Final for that close.
7. **Market Master · 美股市寬／美股行業／ETF 輪動** — id `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` (breadth / rotation context only — **not** setup truth; Setup_Latest is not the entry source).
8. **ETF/ticker RS** sheet — native `1D3BrzLH3DmxX8Gv3W9Yhvd9q_LNOGXyNyUzjnXzqmHk`.
9. **Stockbee 50 Momentum** — Drive `1Fw2IfpQupYCrTtQTZMymt7VdjQnDWJv3` — required every run.

If primary Hermes files are missing/stale for the target close → **stop**. Tell Justin what is missing. Do not invent fills.

Research order: Google Drive/Sheets MCP → Tavily → Firecrawl → Browser Use → box desktop last. Prefer TradingView MCP for technicals on stalk candidates. Skip Browserless / Finance.

## Selection bar

- Open-minded: **no hard veto / always-watch list**.
- Rank by: **`Setup_Quality_Grade` → `Room_To_Supply_R` (prefer ≥ 2) → `RS_Score`**.
- Hard exclude:
  - **`Tradeable` when column present on Contract/verdicts:** require `Tradeable==PASS` for any stalk; `Tradeable FAIL` (or empty when col present) → treat as **WATCH** using `Tradeable_Why` verbatim — never put FAIL in ≤3 stalks; never upgrade
  - `Risk_OK != PASS`
  - `Earnings_Proximity_Flag ∈ {PASS, UNKNOWN}` — **A1: always skip PASS even if STALK baseline leaked**
  - `Entry_Feasible ∈ {INVALIDATED, MISSED}`
- `Risk_ADR_Plan` in family band: breakout **0.3–1.2**; pullback/reversal **0.8–2.5**.
- Prefer `Room_To_Supply_R ≥ 2`. May still stalk `Room ≥ 1.0` with explicit `thin_room` tag when Grade is strong and nothing clears ≥2 — never pad. Never stalk `Room < 1.0`.
- **Growth bias** when two names are otherwise equal.
- Hold horizon: **~2 weeks max** unless Justin marks a homerun.
- Multi-source agreement preferred (Hermes Speak_Up + regime + brief + RS + Stockbee). One lonely signal is not enough.
- Up to **3** attention names. Fewer is fine. If none clear the bar → say **cannot find** — do **not** force 3 / never lower the bar to fill 3.
- **Capital scarcity / can’t-miss:** default **0–2** stalks; empty OK.
- **No Soft Final void** without Justin/總指揮 **AUTHORIZE**; one Final per bar-date.
- **No-repeat** vs prior Second-brain days’ tickers under `/workspace/second-brain/` (~1–2 day window).
- Deep Bear / DEEP DEFENSIVE / 0% exposure = harder tape, **not** “no longs”. Frame as attention/stalk, not size-up buys.
- **Never upgrade WATCH / AVOID.** Never stalk `Tradeable FAIL` when col present. Never invent a target. Never recompute prices/stops — copy Contract.
- Contract may be **113 cols** (Tradeable era). Prefer `hermes_soft_final.py` script output which already hard-excludes Tradeable FAIL.

## Regime = reference, not rigid gate

- Always **read** regime (Focus Long / Focus Short / excess / ETF RS overlay) as context.
- Do **not** veto solely because Focus Long is empty.
- Soft concentration guard: when Focus Long is empty, prefer **≤2 of 3** in the same pillar / P# cluster.

## Stockbee + short timing

- Read the **latest** 熱度圖 every run.
- On thrust days, Fresh/Sustained heat + rising RS leaders support the momentum climate call.
- Late Stockbee inverse-ETF heat after regime Short focus already flagged a sleeve is usually **too late to initiate**.

## Mandatory reflection (every pick, every run)

Before locking the list, answer in the note (short, plain):

1. **Better candidates?** — Did the stack surface stronger names? Why not them?
2. **Market focus now?** — What is leading / flowing today?
3. **Timing?** — Thrust vs pullback climate? Last-man-standing risk?
4. **Why this ticker vs the big trend?** — Specific setup / earnings path / RS vs peers / Speak_Up.
5. **Evidence conflict?** — If high-RS sector ETFs dual-decline, treat as rollover risk.

## Output shape (every run)

Human Soft Final and the chat summary follow `/workspace/second-brain/templates/soft-final-output.md` (worked example: `/workspace/second-brain/2026-11-12/attention-3-picks.md`). Use Traditional Chinese **書面語**, not colloquial Cantonese.

Start from the script's `attention-3-picks.draft.md` (and upload helper `attention-3-picks-notion.md`). Polish 獨立判斷 if needed; do not rebuild the header / tables / PINNED from scratch unless a flag is wrong.

Assume Justin has already read that day's regime, US Brief, Market Master, and RS overview — do **not** recap those reports. Lead with the decision and stock-selection tables; add independent judgment and things he might miss. Process metadata (PINNED_INPUTS) stays at the bottom.

For each Soft stalk (0–3), also emit **exactly** this Hermes §3.3 block in `handoff_blocks.md` (no Adj risk-reward lines, no invented T1/T2/T3, no old ENTRY ZONE / PRIMARY TARGET fields):

```
<TICKER> · <Setup_Family>/<Setup_Code> · <verdict> · quality <Grade>
entry <Entry_Ref> (<Entry_Src>) · stop <Invalidate_Below> (<Stop_Type_Plan>) · risk <Risk_Pct_Plan>% = <Risk_ADR_Plan>xADR
room <Room_To_Supply_R>R → <Supply_Level> (<Supply_Source>) · soft <Supply_Soft_Level> (<Room_To_Soft_R>R)
RS <RS_Score> (<RS_Status>) · earnings <flag> <date>
speak-up: <Speak_Up 全文>
why: <一句，引用 Speak_Up 或 Quality detail>
```

Required fields: Setup_Family/Setup_Code, verdict, quality Grade, Entry_Ref/Entry_Src, Invalidate_Below/Stop_Type_Plan, Risk_Pct_Plan/Risk_ADR_Plan, Room_To_Supply_R → Supply_Level/Supply_Source, soft Supply_Soft_Level/Room_To_Soft_R, RS_Score/RS_Status, earnings flag+date, Speak_Up, why.

**Observe / 其他備註:** non-stalk names — remarks only. **Do not** auto-route to 美股 Swing Setup (US Setup deprecated) or 模擬倉. Do not message Setup bot.

Save: `/workspace/second-brain/YYYY-MM-DD/attention-3-picks.md`

After Final: run [US second-brain Notion sync](sand-workflow:us-second-brain-notion-sync) unless TC says skip Notion.

## Session overview

Do **not** write or sync a US swing session overview unless Justin specifically requests it.

## X dig

- Cap **≤10 minutes** wall clock.
- Prefer public X reads; filter cashtag spam.
- After dig: short update under the picks.

## Discussion mode

When Justin replies, stay on the shortlist: levels, invalidation, alternate names, X follow-ups. Do not expand into HK briefs, scanners, or motion HTML unless he asks.

## Red lines (Hermes §5 + A1–A3)

1. Never change prices/stops or invent targets — copy `Contract_US.csv`.
2. Never upgrade WATCH / AVOID.
3. No `verdicts_US.jsonl` → do not hand opens to 模擬倉 (handoff notes only).
4. Never lower the bar to fill 3 names.
5. Never parse old US handoff (ENTRY ZONE / ADJUSTED STOP / PRIMARY TARGET) as valid v5.
6. Never run S4 story search (outsourced via Hermes).
7. A1: `Earnings_Proximity_Flag=PASS` → always skip.
8. A2: `verdicts_US.jsonl` wins over index §③.
9. A3: never treat index ✅ as buyable.

## VERIFY

- [ ] Primary Hermes files present for session Date (or stop with missing list)
- [ ] Folder Date matches Contract `Date`
- [ ] Each stalk is Hermes §3.3 handoff block only — required fields present
- [ ] Banned tokens absent in outputs: Hermes-deleted underscore fields (risk-reward ratio*, target-N*, setup-type*, adjusted-stop*)
- [ ] Hard excludes applied (Risk_OK, earnings PASS/UNKNOWN, Entry_Feasible)
- [ ] A1–A3 honored; no WATCH/AVOID upgrades; no invented targets
- [ ] ≤3 stalks; never force 3; thin_room tagged when Room < 2
- [ ] Did not run Hermes scan/L2/S4; did not wake Scanner/Setup for US
- [ ] Soft Final follows the 書面語 output template; started from `attention-3-picks.draft.md` + `judgment_flags.json`; no regime/brief/MM/RS recap; those reports not fully loaded unless a flag required a conflict check; overview skipped unless Justin asked
- [ ] Soft demote of a script STALK was only confirmed or undone — WATCH/AVOID never upgraded; index BUY never treated as buyable
- [ ] PINNED_INPUTS lists exact local pack / context *paths* (no inlined report bodies)

## Anti-jobs

- Not a scanner (Hermes owns L1; US Swing Scanner deprecated for US chain).
- Not Setup writer (美股 Swing Setup US path deprecated) — observe remarks only.
- Not S4 story search (outsourced).
- Not regime author / US brief author.
- Do not recompute prices or invent targets.
- Do not post to X or trade.
