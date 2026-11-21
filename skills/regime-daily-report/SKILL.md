---
name: Regime Daily Report
description: >-
  Use this to render the Regime v6.4.6 Traditional Chinese daily in four-layer
  compact form (今日結論, 准盯／避開, 市場狀態＋計分＋觀察, 附錄; themes must name ETFs) — only after
  silent compute.
---
# Regime Daily Report (v6.4.6)

**v6.4.6** final **rendered** output (label: `v6.4.6 hysteresis multi-band confirm`) — 全部繁體中文。
**Presentation lock (Justin 2026-11-12):** four-layer compact. Canon: `/workspace/docs/regime-daily-compact-format-2026-11-12.md`. Skeleton: `/workspace/market-awareness/templates/regime-daily-compact-template.md`.
Approved example: `/workspace/market-awareness/2026-11-11/regime-daily-2026-11-11.md`.
- GFM Markdown tables, **max 4 columns** (Notion / mobile readable).
- **No ASCII boxes** (the old 0C Dashboard box is retired).
- **Four layers only in the reading body:** 今日結論 → 准盯／避開 → 市場狀態＋計分＋行業同主題觀察 → 附錄.
- **One fact once:** 動作、倉位上限、而家跟嘅制度、今日分數區間只在「今日結論」寫完整；不要再寫獨立「決策卡」「中間 linkage」「重要旗號」「市場脈絡總結」牆。
- Reading layer uses plain Chinese (見 canon 用詞表). Internal codes (effective／raw／pending 1/2／A1-ii／FT ①②③) may appear in 附錄 only.
- **Every named theme must include 2–4 representative ETFs** in the reading layer (not only one pillar). Fuller lists go under 附錄「主題對應 ETF」.
- **No** walls of scoring prose: one-sentence conclusion + one score table (scores appear once).
- **No** raw ticker dumps. Decision, score, and observation tables are required.
- Never put a half-width `|` inside a cell (use `／` or fullwidth `｜`, e.g. `｜z｜`).
- Scoring math, hysteresis, FT, Exposure, and stance rules are **unchanged** — this skill only changes how they are shown.

Spine: `docs/v6.4.3/regime-scoring-v6.4.3.txt`. Add-ons: `docs/v6.4.5/fast-track-and-change-c.md` + `docs/CHANGELOG-v6.4.6.md` (5B multi-band).
**動作層（2026-10-22）：** `docs/今日動作-trial-carve-out-2026-10-22.md` — 今日動作／Trial carve-out；**唔改** TOTAL／hysteresis。張力解釋寫入「今日結論」，唔另開 linkage 節。
**Rotation Delta（2026-11-05）：** non-scoring — `docs/rotation-module-v1.1.md` + [rotation-delta](sand-workflow:rotation-delta).
**Monitor 讀法（2026-10-29）：** `docs/cup-market-monitor.md` — 行業趨勢主軸 = **ΔLIFT＋Pace**；|z| 只做顯著性過濾。

## Execution reminder
Silent compute (Sections 1→2→3→4→5→7→0 + Section 6 Steps 1–5 + **FT / Change C / FT STATE** + **Trial carve-out eval**) must be **fully done** before this skill renders. Concise / no-raw-ticker-dump rules apply **only** to rendered text; scoring and decision tables are required in the deliverable.

## Completion contract (before render)
- Version guard: no Pillar C; no Section 5D trade-unit table; totals /12 + /9.5 = /21.5; TOTAL in [−10.5, 21.5]
- A2 clipped [−1,4]; A3 clipped [−1,2]; A1-ii parity-first; A1-i/iii zero-denom handled
- McClellan for A2/A3/Pairs/Deployment via PRIORITY ORDER; **0A④** = NYMO≥0 AND NAMO≥0 simple AND
- A3 zero-cross bonus checked on **$NYSI** only
- B2-i exactly 7 names (no MAGS); B3 shows found/45; found=0 → B3=0 + DATA GAP
- Late Stage uses B3 **%** vs 50%; RSI overheat evaluated; Layer1 pull includes **1D% + RelVol + RSI14**
- **LEADING SECTOR** computed; P5 #1 → N/A for FT/CC
- **Fast-Track** ①②③ evaluated; if fired → 今日結論寫白話封頂（首日倉位上限 ≤30%）+ write FT STATE；三腿明細入附錄
- **Change C** evaluated only if T2108<20% V-REVERSAL branch
- **Index Drawdown Gate (2026-10-01):** if T2108<20, compute SPX dd vs 252-session high (Stockbee S&P) **before** V-REVERSAL. FAIL (<5%) → no V-REVERSAL + 今日結論加非底部訊號白話; NEUTRAL (5–8%) + V-REVERSAL → 今日部署 首注輕試 + 封頂 10%; PASS (≥8%) → normal. Does not change TOTAL. 明細入附錄
- Layer2 includes VIXY 1D% if Carry Unwind evaluated
- TOTAL = A(clipped)+B1+B2+B3 only; hysteresis **multi-band confirm** (pending=raw band) + **Intermediate Land** on pending FAIL when raw>effective (Justin 2026-10-23) + ratchet (new-floor lower; floor wins); Step3 uses EFFECTIVE **unless FT**
- Short-side 5C done; Layer1 ranked 7 groups; Layer0 done; missing-ticker applied
- Section 0 ①② from **VOO EMA** CSV; 今日部署後果寫在「今日結論」最後（若明日／跌回／深熊）
- **Pillar A floor = −4** (A1 −2 + A2 −1 + A3 −1). A −3 is NOT the floor; write e.g. `A −3 (floor −4)` in the 計分表或附錄
- **Prior-day Stockbee revision** (flagged by ingest): 正文一句；存檔 vs xlsx PREV 對照表放附錄；hysteresis still uses archived prior; never reissue prior day
- Literal line `MARKET=US` directly under the 📊 title
- **今日動作＋Trial（2026-10-22）：** silent eval done; 今日結論 fields ready; 准試倉 only if Trial 三條件全齊（缺一不可）; 倉位上限旁須能讀出 ∈ {字面 0%, 試倉例外開, 試倉例外唔開}（試倉明細可入附錄）; 主題許可 = Focus ∩ MM **ΔLIFT 轉強／Pace 轉向**（|z| 僅顯著性加權）∩ ETF Favor，且每主題帶代表 ETF

## Output order
1. `📊 [DATE] 市場制度日報`, then literal line `MARKET=US`
2. **### 今日結論**（必寫；最頂閱讀層）
   - 一行動作＋倉位上限＋TOTAL／區間，然後 **決策表**（最多 4 欄：項目｜今日）：動作、倉位上限、而家跟嘅制度、今日分數區間。五秒可讀完。
   - 動作三選一：**准 swing 試倉**／**觀望**／**收手**。若 Rotation Delta = ②／③：動作旁加輪動中／制度輪動標記（non-scoring；**唔**改 Exposure 數字）。
   - 2–4 句解釋（只寫一次）：短線 vs 累積、快速升級有無開、試倉例外有無開、點解唔跟 raw 或市況標籤加倉。
   - 若明日仍係同一分數區間／跌回／跌入深熊嘅後果。
   - 規則：`docs/今日動作-trial-carve-out-2026-10-22.md`（由 [Regime Modifiers And Stance](sand-workflow:regime-modifiers-and-stance) 算出）
3. **### 准盯／避開**
   - 准盯表、避開／降權表（主題｜說明）。每行必須有 2–4 隻代表 ETF。
   - 原料：Focus Long／Short ∩ Market Master **ΔLIFT／Pace 趨勢**（|z|>1.96 只做顯著過濾）∩ ETF 輪動 Favor／Avoid
   - Trial 若未在今日結論講清，可一句補；唔開獨立 Trial 大段
4. **### 市場狀態** — 廣度／波動／動力股／輪動現任等，每項一次（T2108、4% 脈衝、5D／10D、短線情緒、累積寬度、SPXA、S&P、VIX、VIX／VXV、動力股佔比、MLI、ATR、輪動判定＋現任）
5. **### 計分** — 一句「廣度＋宏觀＝TOTAL」＋**一張**分項表（廣度三項、宏觀三項、合計）。前值修訂正文一句；對照表入附錄。
6. **### 行業同主題觀察（非計分）**
   - 行業：ΔLIFT／Pace 轉強／轉弱分表（趨勢主軸）；分叉必寫；|z| 只做過濾。對應 ETF 若同方向唔一致，要分開睇。
   - 主題傾斜：一主題一行，方向｜主題｜要點＋代表 ETF。來源 [ETF RS Theme Tilt](sand-workflow:etf-rs-theme-tilt) 同 [Rotation Delta](sand-workflow:rotation-delta)。
   - 唔用舊嘅獨立「附加觀察｜Monitor／ETF RS／輪動」一級標題；內容必須齊，詳細名單入附錄。
7. **### 附錄**
   - 核對清單（①–⑤ YES/NO，0A④ ≥0 AND-gate，Market Trend，Deployment Trend，異動）
   - 閘門同領先板塊（FT／Change C／Index DD／LS／Trial 明細、主題層第 2／第 3／最弱＋ETF）
   - 昨日欄位修訂表（若有）
   - 宏觀分項同層級明細
   - 調節項（triggered only；唔改总分）
   - 輪動同行業補充（churn5/10/20、現任／上批、雙升／雙降 ticker＋主題）。③ 制度輪動時附錄寫：舊領導 proxy 一律 Headwind；新領導只做 pullback；觀察名單掛舊書者降權（**唔**放寬 Exposure）
   - **主題對應 ETF** 表（正文已點名嘅主題；代表 2–6 隻）
   - 資料來源同缺口（DATA GAP／ITA 拆細／FRED 等）
   - 自我質疑 **Q1–Q8 + Q11 + Q12**（項／判定／註或短句）
     - **Q11:** FT fired while breadth still weak → ⚠️
     - **Q12:** 頂欄今日動作自洽？准試倉必須有 Trial 三條件數字／狀態；缺條件卻准試倉 → ⚠️；張力日必須喺「今日結論」處理（只寫一次）→ 否則 ⚠️

Internal scoring work may show calcs in chat when Justin asks for audit; the **daily deliverable** follows this four-layer shape. Boundary: do **not** produce US Market Daily Brief theme package.
