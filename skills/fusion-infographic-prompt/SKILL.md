---
name: Fusion Infographic Prompt
description: >-
  Use this after Fusion Report to emit OUTPUT ② (HK or US) — Justin's locked
  flat-field infographic prompt (股票/行業/標題/主題故事/關鍵維度/操作劇本/一句講晒), every number
  traced to the inputs.
---
# Fusion Infographic Prompt (locked format, 2026-09-25)

OUTPUT ② for every Fusion run, HK and US. This format is the default and replaces the older 4-block style. Reference example (structure only; the numbers are ACHR's, never reuse them): `/workspace/fusion/templates/INFOGRAPHIC_PROMPT_FORMAT_REF_ACHR.md`.

## Hard rules
- Plain field lines only. **No** BLOCK headers, numbered sections, style/layout/aspect directives, footer boilerplate or disclaimers.
- VERDICT copied from the technical HANDOFF and never upgraded by the story. Stop is the FINAL/ADJUSTED STOP from the HANDOFF (mark it 條件式 when the HANDOFF does).
- Every number must come from one of these: the Fusion Report MD, the Setup MD/HANDOFF, or the scanner CSV last row. Check them in that order; if a field is in none of them, write `—` and never estimate. RS stars: use them only when an input gives a rating, otherwise `—`.
- Prices keep a `$`; HK uses HK$ and 1M/3M relative to HSI, US uses SPY.
- Save as `FUSION_INFOGRAPHIC_PROMPT_<T>.md` in the run folder (`_v2`, `_v3` for redos).

## Template
```
股票：[代號] [HK/US]
行業：[行業／主題]
標題：[公司] -- [短句]
主題故事：
催化：[事件＋日期]
基本面：[硬數字]
驅動力：[主線／限制]
時間線：財報約 [n] 天後（[日期]，[CLEAR/WARNING]）
關鍵維度：
RS Score：[RS_Score] [⭐ or —]（1M [RS_1M]／3M [RS_3M]，[一句解讀]）
趨勢：Minervini [Trend_Basic]／Stage2 [Stage2_Strict]；[MA 斜率／價 vs MA 位置]
成交量：[Vol_Expansion]x [⬆️/➡️/⬇️] [狀態]
Risk%：[x]%＠$[entry] ｜ Ext [Extension_MA20_Pct]%／RSI [RSI_14]／距52W [Dist_from_52W_High_Pct]%
操作劇本：
建議：[VERDICT] | [Setup type]（[等乜、唔追乜]）
入場：$[zone]（[觸發條件]）
止損：$[FINAL STOP]（[Stop type]）| Ladder1 $[T1] Ladder2 $[T2] Ladder3 $[T3]
RR：L1 [x]x＠$[entry]（[補充]） | Priority [n]/100
一句講晒：
「[copy from Fusion Report, Cantonese, ≤50字]」
```

Risk% for WATCH/STALK uses the scenario entry against the FINAL STOP as the Setup MD states it. For BUY it uses the published entry.

## VERIFY (required before delivery)
1. Pull every number from the prompt and match each one to a line in the Fusion Report, the Setup/HANDOFF or the CSV. Any number without a source gets removed or replaced with `—`.
2. VERDICT, stop, entry, ladder and RR must equal the HANDOFF values.
3. Confirm the structure: no BLOCK or style lines, the fields are in template order, and 一句講晒 sits in 「」.
4. Record the result in the run's SELF_VERIFY file.

Then STOP. Don't generate an image unless Justin or 總指揮 explicitly asks for GENERATE/出圖.
