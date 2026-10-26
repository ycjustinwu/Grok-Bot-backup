---
name: Regime Daily Report
description: >-
  Use this to render the Regime v6.4.6 繁體中文 daily — 今日動作+linkage+Trial carve-out
  top bar, Dashboard, sections 一–三, flags, Market Master Monitor + ETF RS,
  modifiers, summary, Section 8 (Q11); only after silent compute.
---
# Regime Daily Report (v6.4.6)

**v6.4.6** final **rendered** output (label: `v6.4.6 hysteresis multi-band confirm`) — 全部繁體中文. Anti-repetition. No raw data tables except Dashboard. Match sample tone.  
Spine: `docs/v6.4.3/regime-scoring-v6.4.3.txt`. Add-ons: `docs/v6.4.5/fast-track-and-change-c.md` + `docs/CHANGELOG-v6.4.6.md` (5B multi-band).
**動作層（2026-10-22）：** `docs/今日動作-trial-carve-out-2026-10-22.md` — 頂欄今日動作／linkage／Trial carve-out；**唔改** TOTAL／hysteresis。

## Execution reminder
Silent compute (Sections 1→2→3→4→5→7→0 + Section 6 Steps 1–5 + **FT / Change C / FT STATE** + **Trial carve-out eval**) must be **fully done** before this skill renders. Concise / no-raw-table rules apply **only** to rendered text.

## Completion contract (before render)
- Version guard: no Pillar C; no 5D table; totals /12 + /9.5 = /21.5; TOTAL in [−10.5, 21.5]
- A2 clipped [−1,4]; A3 clipped [−1,2]; A1-ii parity-first; A1-i/iii zero-denom handled
- McClellan for A2/A3/Pairs/Deployment via PRIORITY ORDER; **0A④** = NYMO≥0 AND NAMO≥0 simple AND
- A3 zero-cross bonus checked on **$NYSI** only
- B2-i exactly 7 names (no MAGS); B3 shows found/45; found=0 → B3=0 + DATA GAP
- Late Stage uses B3 **%** vs 50%; RSI overheat evaluated; Layer1 pull includes **1D% + RelVol + RSI14**
- **LEADING SECTOR** computed; P5 #1 → N/A for FT/CC
- **Fast-Track** ①②③ evaluated; if fired → print ⚡ line + Day1 Exposure ≤30%; write FT STATE
- **Change C** evaluated only if T2108<20% V-REVERSAL branch
- **Index Drawdown Gate (2026-10-01):** if T2108<20, compute SPX dd vs 252-session high (Stockbee S&P) **before** V-REVERSAL. FAIL (<5%) → no V-REVERSAL + `⚠️ 參與度收縮但指數未跌`; NEUTRAL (5–8%) + V-REVERSAL → 今日部署 首注輕試 + 封頂 10%; PASS (≥8%) → normal. Does not change TOTAL
- Layer2 includes VIXY 1D% if Carry Unwind evaluated
- TOTAL = A(clipped)+B1+B2+B3 only; hysteresis **multi-band confirm** (pending=raw band) + **Intermediate Land** on pending FAIL when raw>effective (Justin 2026-10-23) + ratchet (new-floor lower; floor wins); Step3 uses EFFECTIVE **unless FT**
- Short-side 5C done; Layer1 ranked 7 groups; Layer0 done; missing-ticker applied
- Section 0 ①② from **VOO EMA** CSV; 今日部署 = one qualitative sentence
- **Pillar A floor = −4** (A1 −2 + A2 −1 + A3 −1). A −3 is NOT the floor; write e.g. `A −3 (floor −4)`
- **Prior-day Stockbee revision** (flagged by ingest): print `前值 X (存檔) → 修訂 Y，Δ Z (vs 修訂前值)` in Dashboard 評分 line + 重要旗號 + 市場脈絡總結; hysteresis still uses archived prior; never reissue prior day
- Literal line `MARKET=US` directly under the 📊 title
- **今日動作＋linkage＋Trial（2026-10-22）：** silent eval done; top bar fields ready; 准試倉 only if Trial 三條件全齊（缺一不可）; Exposure 旁註 ∈ {字面 0%, 試倉例外開, 試倉例外唔開}; 主題許可 = Focus ∩ MM |z| ∩ ETF Favor

## Output order
1. `📊 [DATE] 市場制度日報`, then literal line `MARKET=US`
2. **### 今日動作**（必寫；最頂動作層）
   - 三選一：**准 swing 試倉**／**觀望**／**收手**
   - 主題許可（准盯）／禁止（或降權）— 原料：Focus Long／Short ∩ Market Master IndustryGroup |z|>1.96 ∩ ETF 輪動 Favor／Avoid
   - Exposure／effective 對齊一句 + 旁註：`字面 0%`／`試倉例外開`／`試倉例外唔開`
   - 規則：`docs/今日動作-trial-carve-out-2026-10-22.md`（由 [Regime Modifiers And Stance](sand-workflow:regime-modifiers-and-stance) 算出）
3. **### 中間 linkage**（必寫；唔入 TOTAL）
   - effective／pending／exposure vs Checklist／Deployment — 唔同向必須一句點解（曝險錨 = effective／hysteresis）
   - MM 動力股佔比（vs 昨；缺則 vs P50）+ 行業 |z| 偏強／偏弱 → 撐或反「准唔准动手」
4. **0C Dashboard box** (①–⑤ YES/NO with 0A④ ≥0 AND-gate, Market Trend, Focus Themes Long/Short, 評分 X/21.5 前值, 制度=EFFECTIVE (or FT-upgraded), 立場, Exposure Ceiling after ratchet/**FT 30%** + Trial 旁註若適用)
5. ### 一、市場廣度 (2–3句: T2108 zone, McClellan state, NYSI/NASI)
6. ### 二、宏觀與主題 (USD/bonds/credit + strongest themes + ACTIVE Layer2 one-liners + cooling if any)
7. ### 三、操作立場 — Stance Label + 2–3句 + 今日部署 + Short焦點 + 升級條件 + 降級警告  
   If FT: include `⚡ FAST-TRACK OVERRIDE 觸發 — 首日封頂 30%`. If Change C: `🔓 V-REVERSAL 腿放寬（Change C 生效）`. FT Day2 flags as applicable.
   If Index Drawdown Gate FAIL: include `⚠️ 參與度收縮但指數未跌（距高位僅 −X.X%）— 非底部訊號`. If Gate NEUTRAL + V-REVERSAL: 今日部署 must be 首注輕試 + 封頂 10%.
8. ### ⚠️ 重要旗號 (1–3 or 今日無重大警示; include DATA GAP / EXTREME RATIO / NYMO-NAMO divergence / FT 續鎖 / 無法確認 FT 狀態; Trial 開／唔開可一句)
9. ### 附加觀察｜US Market Monitor（Market Master／股票層） — **always required**. Must include 動力股佔比、SPY/QQQ ATR、IndustryGroup |z|>1.96. Skeleton in `docs/cup-market-monitor.md`. Non-scoring.
10. ### 附加觀察｜ETF RS 主題傾斜（非計分） — Favor / Avoid / **趨勢觀察** per [ETF RS Theme Tilt](sand-workflow:etf-rs-theme-tilt). Non-scoring.
11. ### 🔔 Modifier Notes (triggered only; omit if none)
12. ### 市場脈絡總結 (100–150字, concrete numbers)
13. Section 8: FOMC + 財報季 + 季節性 + 自我質疑 **Q1–Q8 + Q11 + Q12** (✅/⚠️ only); ≤220字  
   **Q11:** FT fired while breadth still weak → ⚠️  
   **Q12:** 頂欄今日動作自洽？准試倉必須有 Trial 三條件數字／狀態；缺條件卻准試倉 → ⚠️；張力日（Uptrend vs Deep Bear）必須喺 linkage 處理 → 否則 ⚠️

Internal scoring work may show calcs in chat when Justin asks for audit; the **daily deliverable** follows this lean shape. Boundary: do **not** produce US Market Daily Brief theme package.
