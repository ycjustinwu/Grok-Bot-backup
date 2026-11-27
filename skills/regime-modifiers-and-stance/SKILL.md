---
name: Regime Modifiers And Stance
description: >-
  Use this for Regime v6.4.6 modifiers (−6..+7), TOTAL /21.5, hysteresis
  multi-band + FT/CC, short 5C, stance Steps 1–5, 2026-10-22 Trial carve-out /
  今日動作, and CUPSIR Gates 1 & 4 stop-swing overlay (action-layer only; no TOTAL
  or regime_effective change).
---
# Regime Modifiers And Stance (v6.4.6)

**v6.4.6 = v6.4.3 scoring + v6.4.5 FT/CC/LS + hysteresis multi-band confirm (Justin lock 2026-09-23).**  
Label: `v6.4.6 hysteresis multi-band confirm`. Scoring spine still v6.4.3/v6.4.5 FT; **only 5B upgrade semantics** change.  
Modifiers (−6..+7) do **not** change TOTAL. Never both sides of the same pair. McClellan refs use PRIORITY ORDER (not 0A④).
Add-on canon: `/workspace/refactored_market_awareness/docs/v6.4.5/fast-track-and-change-c.md`.
Hysteresis canon: `docs/regime-bands.md` + `docs/CHANGELOG-v6.4.6.md` + `docs/hysteresis-intermediate-land-2026-10-23.md`.
**動作層 canon（2026-10-22）：** `docs/今日動作-trial-carve-out-2026-10-22.md` — Trial／今日動作／linkage；**唔改** TOTAL／5B。
**CUPSIR Gates 1 & 4（LOCKED Justin 2026-11-24）：** `/workspace/docs/cupsir-gates-1-and-4-2026-11-24.md` — 主動交易止蝕閘門，只疊加喺今日動作；**唔改** TOTAL／`regime_effective`／5B／FT／Index DD／Exposure 數字。

## Pairs 1–7 (data-driven) — UNCHANGED
1. McClellan divergence: index NH + McClellan LH → −1; index NL + McClellan HL → +1
2. Extreme reversal: >+100 then double-top down → −1; <−100 then double-bottom up → +1
3. Zero-line: failed near zero **2+** attempts → −1; crossed above zero and held **2+** days → +1 (**ops lock**)
4. Vol regime: VIX>20 & spike>+15% OR VIX>30 → −1; VIX drop>15% from elevated + breadth improves → +1
5. Breadth speed (xlsx): 5D from >2.0 to <0.8 in 3d → −1; reverse → +1
6. Q25 surge (xlsx **jump** = today−prev count): Down25 jump >+200 → −1; Up25 jump >+200 → +1
7. VIX term calm (**bonus only**): Condition A spike reversal — ratio was >1.0 in past 5d AND today <0.95 AND McClellan improving = state ∈ **{PR, NR, CU}**; Condition B calm recovery — today ∈[0.82,1.00] AND 3-day descending AND 3d-ago >0.92. Caution flag (not score): today ratio <0.82 and flat/down.

FOMC: ≤7 calendar days → **PRE-FOMC** (not OFF-CYCLE).

## 5A Score + Regime — UNCHANGED
TOTAL = A (clipped) + B1 + B2 + B3 only → **/21.5**, range **[−10.5, 21.5]**. Bands: `docs/regime-bands.md`.
If T2108 <20%, **Reversal Watch replaces** score-band regime for stance (Section 6 Step 5) — not merely an add-on flag. Extreme Oversold threshold **not widened**.

## LEADING SECTOR (LS) — NEW v6.4.5
= Layer 1 **#1 by 1W excess**. If #1 = **P5 Defensive** → **N/A** (FT + Change C auto-fail). P7 OK + low-confidence flag.
**Volume confirm** (present names only): `avg(1D%) > 0` AND `avg(RelVol) ≥ 2.0` AND found > 0; found=0 → N/A + DATA GAP. Group average — **not** any-one-name.

## FAST-TRACK OVERRIDE (FT) — NEW v6.4.5 (any T2108)
All three required:
1. 4% Ratio ≥ 3.0
2. VIX single-day drop > 10% `(VIX_today/VIX_prev − 1)`
3. LS volume confirm AND LS ≠ N/A

→ Skip 5B 2-day same-band; **upgrade effective today** to score’s band.  
→ Day-1 Exposure **hard cap 30%**.  
→ Print: `⚡ FAST-TRACK OVERRIDE 觸發 — 首日封頂 30%`

## Change C — NEW v6.4.5 (only T2108 < 20% V-REVERSAL)
Relaxes **② only** if BOTH: B2-i offensive spread ≥ +2% AND LS volume confirm.  
Relaxed ② = McClellan selling pressure stabilizing (today’s decline narrower or flat — no formal cross).  
① 4% Ratio > 3.0 and ③ VIX down today → **NEVER** relaxed.  
→ Print: `🔓 V-REVERSAL 腿放寬（Change C 生效）`  
FT + Change C same day: exposure still **30%**; label from Step 5 if on Reversal branch.

## 5B Hysteresis + Exposure ratchet — v6.4.6 LOCKED (Justin 2026-09-23) + Intermediate Land (2026-10-23)
- Cite 前值 **only** from `thread-memory/latest-state.json` / archive (never peer draft).
- **Upgrade pending target = today’s raw band** (the score band), **not** only the next adjacent band.
- After **2 consecutive calendar sessions** with the **same raw band**, and that band is **strictly above** prior effective → on day 2 set `regime_effective = that raw band`.
- **Multi-band jump allowed** (e.g. Deep Bear → Cautious in one confirm when raw was Cautious both days). Intermediate bands (Bear/Avoid) are **skipped**. Do **NOT** invent a one-band ladder.
- Day 1 of a new higher raw band: pending `1/2`, keep old effective.
- If day 2 raw **leaves** that pending target band → pending **fails**, then **Intermediate Land (Justin 2026-10-23)**:
  - `E` = prior effective, `R` = today’s raw, `T` = failed pending target.
  - `R < E` → immediate downgrade to `R`.
  - `R == E` → hold `E`; clear pending.
  - `R > E` → **land now** `regime_effective = R`, clear pending; print `⬆️ pending T FAIL → Intermediate Land → effective R`. Do **not** leave effective at old `E` while restarting `pending R 1/2`.
  - Not a day-1 one-band ladder; only on pending FAIL when raw remains above effective. Canon: `docs/hysteresis-intermediate-land-2026-10-23.md` + `docs/regime-bands.md`.
- Downgrade: still **immediate**, multi-band OK. FT / Change C unchanged.
- V-REVERSAL / Step5 override: immediate (Change C may relax ②).
- **Ratchet (exposure ceiling only):** upper +20pp/day max; once new regime confirmed, **lower = new regime’s own floor**. Down moves: no ratchet. If multi-band confirm makes floor > ratchet upper, **floor wins** (land at new floor).
- DEGRADED (no thread McClellan/VIX history): adopt today's band + 「未經確認」.
- **Supersedes** any prior “one-band-at-a-time / adjacent-only upgrade” ops gloss.

### FT STATE memory (MEM) — write every run
Persist `fast_track` on latest-state.json. Day-2:
| Yesterday | Today | Exposure |
|---|---|---|
| FT Day1 | Score same band or higher | Unlock normal 5A/5B ceiling (ratchet still) |
| FT Day1 | Score fell back | Stay 30% + `⚠️ Fast-Track 續鎖` |
| Unknown / no memory | — | Stay 30% + `⚠️ 無法確認 Fast-Track 狀態` (never assume unlocked) |
| FT re-triggers ①②③ | — | New Day1, 30% again |

## 5C Short-side — UNCHANGED
Weakest Layer1 by 1W excess vs VOO. Need **all three**: excess <−2%, group 1W avg <0, effective regime Neutral-or-below **OR** MEGA-CAP DIVERGENCE. Else 「Short: 暫無候選」. Sustainability: 1M also lag → 趨勢性弱勢; 1M still lead → rotation / half-size. If P7: split **BUG vs IGV** 1M tags when they diverge.

## Stance (silent Steps 1–5 → label)
1. Deployment Trend (Up/Down/Side) — McClellan tests: Uptrend state ∈ {PR, CU}; Downtrend = NF. **≠ Section 0 checklist**.
2. Mega-cap Divergence (2 of 4).
3. Market Condition Label from **EFFECTIVE** (post-hysteresis) regime band — **unless FT** upgraded today.
4. Offensive Override (NARROW BULL / CONCENTRATED ATTACK paths).
5. If T2108<20 → **Reversal Zone** (Step 5): run **INDEX DRAWDOWN GATE first**, then V-REVERSAL / DEAD CAT / UNCERTAIN (Change C may relax ② only).

### Step 5 — INDEX DRAWDOWN GATE（V-REVERSAL 前置檢查）— LOCKED Justin 2026-10-01
來源：動力股佔比筆記 —「指數未跌而動力股收縮」係下跌開頭，唔係底部。

**When:** only if T2108 < 20 (Reversal Watch / Step 5). **Does NOT** change TOTAL, Pillar A/B, bands, or hysteresis.

**Compute** (ingest hands `spx_drawdown` or stance computes from Stockbee):
- SPX drawdown = `(252-session high close − today close) ÷ 252-session high close`
- Series = Stockbee xlsx **S&P** column (session-dated rows). Prefer full 252 trading sessions.
- If xlsx has <252 sessions → use longest available window in the file (+ thread SPX history if present); label `⚠️ 窗口不足（N日）`. Never invent highs.

**Gate outcomes (apply BEFORE V-REVERSAL conditions):**
| Drawdown | Gate | Effect |
|---|---|---|
| ≥ 8% | **PASS** | Evaluate V-REVERSAL / DEAD CAT / UNCERTAIN as before (①②③ + Change C unchanged) |
| < 5% | **FAIL** | **Forbid V-REVERSAL**. Max outcome = UNCERTAIN, **or** DEAD CAT if DEAD CAT’s own three conditions fire (ratio <1.5 + McClellan neg + VIX >25). Print: `⚠️ 參與度收縮但指數未跌（距高位僅 −X.X%）— 非底部訊號` |
| 5% ≤ dd < 8% | **NEUTRAL** | V-REVERSAL may still evaluate; **if** it fires → 今日部署 forced `首注輕試 + 封頂 10%` (Exposure hard cap **10%**). Do **not** use normal V-REVERSAL 分批建倉 sizing. If V-REVERSAL does not fire → UNCERTAIN / DEAD CAT as usual |

①③ and Change C rules **unchanged**. Gate only decides whether a bottom label is allowed / how hard V-REVERSAL may deploy — not the score.

**今日部署** = one qualitative sentence from stance table — **no** unit/%/R/margin/short-count table. Under GATE NEUTRAL + V-REVERSAL: must say 首注輕試 + 封頂 10%.

## 今日動作＋Trial carve-out（動作層；LOCKED Justin 2026-10-22）
**After** Steps 1–5 + FT/CC + Index DD Gate. **Never** changes TOTAL, raw/effective band, pending day-count, or numeric Exposure ceiling from 5B/FT/Gate.
Canon: `docs/今日動作-trial-carve-out-2026-10-22.md`.

### Trial 三條件（須同時成立才可「准 swing 試倉」於 Deep Bear／字面 0%）
1. **pending 升級中** — pending exists AND pending target band **strictly above** effective.
2. **動力股佔比↑** — **primary:** today 動力股佔比% > yesterday (same Market Master History). **fallback:** no yesterday → today > in-table P50/median (disclose which). Flat or down → FAIL.
3. **風險胃納略改善** — **primary:** today B2 > prior B2 from `latest-state.json`. **fallback if B2 flat:** B2-i (進攻−防守 1W 差) today − prior **> 0**. Else FAIL.

| Outcome | 今日動作 | Exposure 旁註 |
|---|---|---|
| Trial 三條件全齊 | **准 swing 試倉**（細碼） | `試倉例外開`（字面 ceiling 仍按 5B，通常 Deep Bear=`字面 0%` + 例外開） |
| 缺一或多；Checklist／Deployment 偏多 | **觀望** | `試倉例外唔開` + Deep Bear 時 `字面 0%` |
| 缺一且風險惡化／降級 | **收手** | `試倉例外唔開` + `字面 0%` |
| effective 已允許新倉（非 Deep Bear 0%） | 跟正常 stance／ratchet（可准試倉／加倉語氣） | 跟 5B／FT 數字；唔滥用 Trial |

### Linkage fields（交 daily-report 渲染）
- One sentence: effective／pending／exposure vs Checklist／Deployment（曝險錨 = effective）
- One sentence: MM 動力股 + |z| 撐／反

### 主題許可 fields
- 准盯 = Focus Long ∩ MM |z|>1.96 同向偏強 ∩ ETF Favor
- 禁止／降權 = Focus Short ∪ MM |z| 偏弱 ∪ ETF Avoid
- Missing source → DATA GAP / shrink list; never invent tickers

Write `trial_carve_out` (+ bools for each condition + action + exposure_note) into `latest-state.json` / `regime-summary.json` for WV.

## CUPSIR Gates 1 & 4（主動交易止蝕閘門；LOCKED Justin 2026-11-24）
**After** Trial carve-out / 今日動作 is computed. **Never** changes TOTAL, raw / `regime_effective`, pending day-count, FT, Change C, Index Drawdown Gate, or numeric Exposure ceiling.
Canon: `/workspace/docs/cupsir-gates-1-and-4-2026-11-24.md`. Ingest hands `cupsir_gates` (Handover Note first; else CSV compute).

### Gate 1（市寬）
`(52W High − 52W Low) ÷ Universe < -2.00%` → `gate1_closed = true`.
- 禁止開新順勢／回調 swing 長倉。
- 若原動作係 **准 swing 試倉** → 降級為 `觀望｜🚨 Gate 1 落閘（停開順勢 swing）`。
- 已係觀望／收手而閘已落 → 同樣附加落閘標籤，唔再改基礎動詞。
- 未觸發但距離 −2.00% 線少於 0.50pp（`-2.00% ≤ 指標 < -1.50%`）→ `⚠️ 貼近落閘線`。恰等於 −2.00% 唔算落閘（觸發係嚴格 `<`）。
- 指標 `≥ -1.50%` → 無 Gate 1 標籤。
- 缺 52W 欄或宇宙數 → `gate1_closed = null`，附錄 DATA GAP；**唔**當已落閘，亦**唔**觸發主 DATA GATE。

### Gate 4（大小盤分歧）
`SPY/VOO > 200MA` **且** `IWM < 200MA` → `gate4_closed = true`。
- 禁止開新均值回歸長倉；動作欄附加 `｜⚠️ Gate 4 落閘（停開均值回歸）`。
- 大盤同 IWM **都在 200MA 之下**（或都在之上）→ 分歧不成立，未觸發。
- 大盤代理：Handover 優先；否則 CSV 嘅 200 日均線欄（通常 EMA 200）。SPY 同 VOO 結論衝突時預設 VOO，並披露。
- 缺可用 200MA 列 → `gate4_closed = null`，附錄 DATA GAP；唔發明。

### 動作疊加順序
先 Gate 1（可降級 准 swing 試倉 → 觀望），再附加 Gate 4 標籤。兩閘同日例子：`觀望｜🚨 Gate 1 落閘（停開順勢 swing）｜⚠️ Gate 4 落閘（停開均值回歸）`。
數字 Exposure 同 `試倉例外開`／`唔開` 旁註維持 Trial／5B 原值。

Write `cupsir_gates` into `latest-state.json` / `regime-summary.json`（keys 見 canon；缺值 `null`）。
