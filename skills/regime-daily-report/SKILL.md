---
name: Regime Daily Report
description: >-
  Use this to render the Regime v6.4.6 Traditional Chinese daily in five-section
  compact form (今日結論 with always-visible CUPSIR Gates 1 & 4, 准盯／避開, 市場狀態與計分,
  行業與主題精要, 極簡附錄 without embedding latest-state; themes must name ETFs) — only
  after silent compute.
---
# Regime Daily Report (v6.4.6)

**v6.4.6** final **rendered** output (label: `v6.4.6 hysteresis multi-band confirm`) — 全部繁體中文。
**Presentation lock (Justin 2026-11-24):** five-section compact. Canon: `/workspace/docs/regime-daily-compact-format-2026-11-24.md`. Skeleton: `/workspace/market-awareness/templates/regime-daily-compact-template.md` (dated copy also at `regime-daily-compact-template-2026-11-24.md`). This supersedes the 2026-11-12 four-layer compact canon for **presentation only**.
Approved specimen (format only; the official 11-23 Soft Final file and its Notion page stay in the prior four-layer form until Justin asks to change them): `/workspace/market-awareness/2026-11-23/regime-daily-2026-11-23-compact-review.md`.
- GFM Markdown tables, **max 4 columns** (Notion / mobile readable).
- **No ASCII boxes** (the old 0C Dashboard box is retired).
- **Five sections only in the reading body:** 今日結論 → 准盯／避開 → 市場狀態與計分 → 行業與主題精要 → 極簡附錄.
- **One fact once (Zero-Repetition):** 試倉三條件、快速升級失敗原因、昨日 Stockbee 修訂，只准在「今日結論」或「極簡附錄」寫一次；禁止在正文、附錄、自我質疑內重複。動作、倉位上限、而家跟嘅制度、今日分數區間只在「今日結論」寫完整。
- Reading layer uses plain Chinese (見 canon 用詞表). Internal codes (effective／raw／pending 1/2／A1-ii／FT ①②③) may appear in 極簡附錄 or in the session-folder `latest-state.json` on disk only — **never** embed that JSON in the Soft Final markdown.
- **Every named theme must include representative ETFs in section 2** (merged into the 准盯／避開 tables). **Do not** add a standalone 「主題對應 ETF」 appendix table.
- **No** walls of scoring prose: one sentence「廣度＋宏觀＝總分」+ one 6-row score table (scores appear once). Macro line-items go in the 「關鍵依據」column, not a repeated appendix prose block.
- **No** raw ticker dumps. The tables and 3 bullets specified below are required.
- Never put a half-width `|` inside a cell (use `／` or fullwidth `｜`, e.g. `｜z｜`).
- Five-section body (HTML comments not counted; **no** `latest-state` JSON embed) is capped at **1,200 CJK 漢字**. Terse; do not restate numbers already in tables. Session `latest-state.json` stays on disk as the hysteresis source; self-VERIFY checks that the disk file exists and matches the report’s stated scores／action／gates, and **must not** require an embed.
- Scoring math, hysteresis, FT, Exposure, Trial, CUPSIR Gates 1 & 4 (action overlay only), and stance rules are **unchanged** — this skill only changes how they are shown.

Spine: `docs/v6.4.3/regime-scoring-v6.4.3.txt`. Add-ons: `docs/v6.4.5/fast-track-and-change-c.md` + `docs/CHANGELOG-v6.4.6.md` (5B multi-band).
**動作層（2026-10-22）：** `docs/今日動作-trial-carve-out-2026-10-22.md` — 今日動作／Trial carve-out；**唔改** TOTAL／hysteresis。張力解釋寫入「今日結論」，唔另開 linkage 節。
**CUPSIR Gates 1 & 4（2026-11-24）：** `/workspace/docs/cupsir-gates-1-and-4-2026-11-24.md` — 止蝕閘只改動作欄標註／降級；**唔改** TOTAL／`regime_effective`。缺 52W／200MA 只在極簡附錄標 DATA GAP。
**Rotation Delta（2026-11-05）：** non-scoring — `docs/rotation-module-v1.1.md` + [rotation-delta](sand-workflow:rotation-delta).
**Monitor 讀法（2026-10-29）：** `docs/cup-market-monitor.md` — 行業趨勢主軸 = **ΔLIFT＋Pace**；|z| 只做顯著性過濾。

## Execution reminder
Silent compute (Sections 1→2→3→4→5→7→0 + Section 6 Steps 1–5 + **FT / Change C / FT STATE** + **Trial carve-out eval** + **CUPSIR Gates 1 & 4 overlay**) must be **fully done** before this skill renders. Concise / no-raw-ticker-dump / 字數上限 rules apply **only** to rendered text; scoring and decision tables are required in the deliverable.

## Completion contract (before render)
- Version guard: no Pillar C; no Section 5D trade-unit table; totals /12 + /9.5 = /21.5; TOTAL in [−10.5, 21.5]
- A2 clipped [−1,4]; A3 clipped [−1,2]; A1-ii parity-first; A1-i/iii zero-denom handled
- McClellan for A2/A3/Pairs/Deployment via PRIORITY ORDER; **0A④** = NYMO≥0 AND NAMO≥0 simple AND
- A3 zero-cross bonus checked on **$NYSI** only
- B2-i exactly 7 names (no MAGS); B3 shows found/45; found=0 → B3=0 + DATA GAP
- Late Stage uses B3 **%** vs 50%; RSI overheat evaluated; Layer1 pull includes **1D% + RelVol + RSI14**
- **LEADING SECTOR** computed; P5 #1 → N/A for FT/CC
- **Fast-Track** ①②③ evaluated; if fired → 今日結論寫白話封頂（首日倉位上限 ≤30%）+ write FT STATE；未開原因若要寫，只寫一次（今日結論或極簡附錄）
- **Change C** evaluated only if T2108<20% V-REVERSAL branch
- **Index Drawdown Gate (2026-10-01):** if T2108<20, compute SPX dd vs 252-session high (Stockbee S&P) **before** V-REVERSAL. FAIL (<5%) → no V-REVERSAL + 今日結論加非底部訊號白話; NEUTRAL (5–8%) + V-REVERSAL → 今日部署 首注輕試 + 封頂 10%; PASS (≥8%) → normal. Does not change TOTAL. 不適用或明細可壓成極簡附錄一句
- Layer2 includes VIXY 1D% if Carry Unwind evaluated
- TOTAL = A(clipped)+B1+B2+B3 only; hysteresis **multi-band confirm** (pending=raw band) + **Intermediate Land** on pending FAIL when raw>effective (Justin 2026-10-23) + ratchet (new-floor lower; floor wins); Step3 uses EFFECTIVE **unless FT**
- Short-side 5C done; Layer1 ranked 7 groups; Layer0 done; missing-ticker applied
- Section 0 ①② from **VOO EMA** CSV; 今日部署後果寫在「今日結論」第 3 點子彈（若明日／跌回／深熊）
- **Pillar A floor = −4** (A1 −2 + A2 −1 + A3 −1). A −3 is NOT the floor; write e.g. `A −3 (floor −4)` in the 計分表或極簡附錄
- **Prior-day Stockbee revision** (flagged by ingest): 極簡附錄一句；若重算總分差額為 0，不開對照表。hysteresis still uses archived prior; never reissue prior day
- Literal line `MARKET=US` directly under the 📊 title
- **今日動作＋Trial（2026-10-22）：** silent eval done; 今日結論 fields ready; 准試倉 only if Trial 三條件全齊（缺一不可）; 倉位上限旁須能讀出 ∈ {字面 0%, 試倉例外開, 試倉例外唔開}；試倉三條件若寫出，只准一次（今日結論或極簡附錄，不可兩處）; 主題許可 = Focus ∩ MM **ΔLIFT 轉強／Pace 轉向**（|z| 僅顯著性加權）∩ ETF Favor，且每主題帶代表 ETF（寫在第 2 節）
- **CUPSIR Gates 1 & 4（2026-11-24；可見性 t129u）：** overlay already applied by modifiers. 今日結論狀態表**必須有第 5 行「CUPSIR 閘門」**，即使兩閘都 PASS 都要寫清楚（例如 `Gate 1 PASS（−0.84%，未貼近）｜Gate 4 PASS（兩邊都在 200 日均下）`）。舊「恰好 4 行」鎖已被呢條可見性規則取代。動作欄必須用疊加後字串（Gate 1 可把准試倉降為 `觀望｜🚨 Gate 1 落閘（停開順勢 swing）`；近線標 `⚠️ 貼近落閘線`；Gate 4 附加 `｜⚠️ Gate 4 落閘（停開均值回歸）`）；落閘時動作欄標籤同第 5 行並存。閘門已在今日結論可見後，極簡附錄唔再寫長段 CUPSIR 依據；缺 52W／200MA 先在附錄標 DATA GAP。**Never** show a TOTAL or effective change from these gates.

## Output order
1. `📊 [DATE] 市場制度日報`, then literal line `MARKET=US`
2. **### 今日結論**
   - **5 行狀態表**（最多 4 欄，建議項目｜今日）：動作、倉位上限、而家跟嘅制度、今日分數區間、CUPSIR 閘門。第 5 行即使兩閘都 PASS 都要寫。表前唔加長導語，唔另開決策卡。
   - 動作三選一：**准 swing 試倉**／**觀望**／**收手**。若 Rotation Delta = ②／③：動作旁加輪動中／制度輪動標記（non-scoring；**唔**改 Exposure 數字）。CUPSIR Gate 1 落閘時唔准再寫「准 swing 試倉」，要用 `觀望｜🚨 Gate 1 落閘（停開順勢 swing）`；Gate 4 落閘時喺動作欄附加 `｜⚠️ Gate 4 落閘（停開均值回歸）`。未觸發但 Gate 1 距線 <0.50pp，標 `⚠️ 貼近落閘線`。落閘標籤同第 5 行並存。
   - **恰好 3 點子彈：**（1）反彈／未升級原因（2）動作依據（3）明日觸發點（若明日仍係同一分數區間／跌回／跌入深熊嘅後果）。閘門數字已在第 5 行，子彈唔再重複。
   - 規則：`docs/今日動作-trial-carve-out-2026-10-22.md`（由 [Regime Modifiers And Stance](sand-workflow:regime-modifiers-and-stance) 算出）
3. **### 准盯／避開**
   - 標題必須恰好係「准盯／避開」（盯 = U+76EF，斜線用全形 ／ = U+FF0F；唔可用形近字）。
   - 准盯表、避開／降權表。代表 ETF **直接合併寫入此表**；刪除附錄「主題對應 ETF」獨立大表。
   - 原料：Focus Long／Short ∩ Market Master **ΔLIFT／Pace 趨勢**（|z|>1.96 只做顯著過濾）∩ ETF 輪動 Favor／Avoid
4. **### 市場狀態與計分**
   - 精簡市場狀態表（建議 2 欄：項目｜今日），每項一次：T2108、4% 脈衝、5D／10D、短線情緒、累積寬度、SPXA、S&P、VIX、VIX／VXV、動力股佔比、MLI、ATR、輪動判定＋現任。
   - 一句「廣度＋宏觀＝總分」＋**一張 6 行**計分表（柱｜分項｜分數｜關鍵依據）：廣度三項、宏觀三項。宏觀分項明細寫入「關鍵依據」，刪除附錄重複宏觀文字段。
5. **### 行業與主題精要**
   - 恰好 3 點子彈：轉強行業、轉弱行業、ETF RS 雙升／雙降。行業以 ΔLIFT／Pace 為趨勢主軸；分叉必寫；|z| 只做過濾。對應 ETF 若同方向唔一致，要分開睇。來源 [ETF RS Theme Tilt](sand-workflow:etf-rs-theme-tilt) 同 [Rotation Delta](sand-workflow:rotation-delta)。
6. **### 極簡附錄**
   - 只列狀態與異常（清單／部署、閘門是否適用或觸發、調節項若有、DATA GAP／ITA／FRED 等），唔重複第 1–4 節已寫嘅數字。
   - **Exception-only 核對：** 若 Q1–Q12（項次同舊約：Q1–Q8 + Q11 + Q12）全部通過，只輸出 1 行「內部核對：Q1–Q12 全部通過（無異常）」；只有 FAIL 或規則衝突才展開。
     - **Q11:** FT fired while breadth still weak → 展開 ⚠️
     - **Q12:** 頂欄今日動作自洽？准試倉必須有 Trial 三條件（只可出現一次）；缺條件卻准試倉 → 展開 ⚠️；張力日必須喺「今日結論」處理（只寫一次）；`gate1_closed = true` 卻仍寫准試倉 → 展開 ⚠️
   - 昨日 Stockbee 修訂若重算總分差額為 0：1 句，不開對照表。ITA 等數據異常只在此節提一次。
   - **禁止**把該場次 `latest-state.json` 嵌入 Soft Final markdown（唔開 `#### latest-state`、唔用 fenced JSON、唔用 HTML 註解傾倒）。磁碟檔仍係 hysteresis 來源，繼續寫／更新；唔好為咗核對而把 JSON 貼回正文。

Internal scoring work may show calcs in chat when Justin asks for audit; the **daily deliverable** follows this five-section shape. Boundary: do **not** produce US Market Daily Brief theme package.
