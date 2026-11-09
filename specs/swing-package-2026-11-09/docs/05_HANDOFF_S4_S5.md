# 05 — S4 story handoff and S5 verdict contract

## What the story model receives

One row per name from `L2_Input.csv`: ticker, baseline verdict, entry reference, plan stop,
risk %/ADR, room, leader/setup/risk gates, earnings proximity, `Tradeable_Why`.

**It must not invent prices.** Entry, stop, size and the risk numbers come from the program.

## What it returns — `<TICKER>_story.json`

```json
{
  "ticker": "0386.HK",
  "market_line": "一句市場定位（≤40 字，寫板塊／資金流，不寫技術指標）",
  "story_main": "主敘事（≤200 字）",
  "story_main_score": 0,
  "why_now": "為何是現在（≤60 字）",
  "moat": "護城河／競爭位置（1–2 句）",
  "numbers": "基本面數字（營收／利潤／指引；有出處）",
  "story_sub": "次線敘事（≤120 字）",
  "story_sub_score": 0,
  "risks": ["故事或基本面風險，最多 4 條；不可寫技術指標或系統價位"],
  "conviction": "CONFIRM | CHALLENGE | NEUTRAL",
  "conviction_why": "為何這個 conviction（1 句）",
  "story_tag": "短標籤",
  "hard_event": "下一個硬事件或 null",
  "earnings_check": "財報日期與距離，或 NOT_NEAR",
  "sources": ["來源名稱 + 日期"],
  "traps": "最容易被人講錯的一點"
}
```

## Hard rules (a violation rejects the whole file)

1. No invented targets, no `T1/T2/T3`, no `RR`, no RSI/MA/ADR/volume-ratio numbers, no stop prices.
2. Any sell-side figure must name its source and date, else it counts as invented.
3. `conviction` ∈ `CONFIRM` / `CHALLENGE` / `NEUTRAL` only.
4. `risks` ≤ 4, story/fundamental only — technical risk belongs to the program.
5. Traditional Chinese for HK, English for US; no simplified characters in either.
6. Never change the verdict, entry, stop or risk handed in.
7. At least **2 sources**, at least one dated after the data date; `CONFIRM` requires two distinct domains.
8. If the story contradicts the system call, still write it — set `conviction=CHALLENGE` and say why.

## `<TICKER>_search_log.json`

```json
{"ticker": "0386.HK", "queries": ["..."], "urls": ["https://..."], "retrieved": "2026-11-09"}
```

`check_verdict` compares story numbers against this log (V12/V13) — a number with no matching source
fails the gate. Reconstructed logs must say so inside `queries`, e.g.
`"由報告來源重建 — 未附原始 query"`.

## `verdicts_<market>.jsonl`

One JSON object per line:

```json
{"ticker": "0386.HK", "verdict": "BUY", "entry": 4.805, "stop": 4.695, "conviction": "CONFIRM", "story_tag": "Turnaround"}
```

`verdict` must equal the baseline unless the story justifies a documented change; prices must match
`Contract_US.csv` exactly (V1/V2).

## Run order

```bash
python3 story_search_sync.py runs/<market>/run_<date>   # merge stories + logs into the run
bash run_l2.sh check runs/<market>/run_<date>           # exit 0 required
bash run_l2.sh render runs/<market>/run_<date>          # index.md + 快報 + image packs
```
