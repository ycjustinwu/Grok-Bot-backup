---
name: Regime Daily Report
description: >-
  Use this to render the Regime v6.4.6 繁體中文 daily — Dashboard, sections 一–三,
  flags, US Market Monitor ADDITIONAL Observation, modifiers, summary, and
  Section 8 self-challenge (incl. Q11 Fast-Track); only after silent compute.
---
# Regime Daily Report (v6.4.6)

**v6.4.6** final **rendered** output (label: `v6.4.6 hysteresis multi-band confirm`) — 全部繁體中文. Anti-repetition. No raw data tables except Dashboard. Match sample tone.  
Spine: `docs/v6.4.3/regime-scoring-v6.4.3.txt`. Add-ons: `docs/v6.4.5/fast-track-and-change-c.md` + `docs/CHANGELOG-v6.4.6.md` (5B multi-band).

## Execution reminder
Silent compute (Sections 1→2→3→4→5→7→0 + Section 6 Steps 1–5 + **FT / Change C / FT STATE**) must be **fully done** before this skill renders Section 6 + Section 8. Concise / no-raw-table rules apply **only** to rendered text.

## Completion contract (before Section 6/8)
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
- TOTAL = A(clipped)+B1+B2+B3 only; hysteresis **multi-band confirm** (pending=raw band) + ratchet (new-floor lower; floor wins); Step3 uses EFFECTIVE **unless FT**
- Short-side 5C done; Layer1 ranked 7 groups; Layer0 done; missing-ticker applied
- Section 0 ①② from **VOO EMA** CSV; 今日部署 = one qualitative sentence
- **Pillar A floor = −4** (A1 −2 + A2 −1 + A3 −1). A −3 is NOT the floor; write e.g. `A −3 (floor −4)`
- **Prior-day Stockbee revision** (flagged by ingest): print `前值 X (存檔) → 修訂 Y，Δ Z (vs 修訂前值)` in Dashboard 評分 line + 重要旗號 + 市場脈絡總結; hysteresis still uses archived prior; never reissue prior day
- Literal line `MARKET=US` directly under the 📊 title

## Output order
1. `📊 [DATE] 市場制度日報`, then literal line `MARKET=US`, then **0C Dashboard box** (①–⑤ YES/NO with 0A④ ≥0 AND-gate, Market Trend, Focus Themes Long/Short, 評分 X/21.5 前值, 制度=EFFECTIVE (or FT-upgraded), 立場, Exposure Ceiling after ratchet/**FT 30%**)
2. ### 一、市場廣度 (2–3句: T2108 zone, McClellan state, NYSI/NASI)
3. ### 二、宏觀與主題 (USD/bonds/credit + strongest themes + ACTIVE Layer2 one-liners + cooling if any)
4. ### 三、操作立場 — Stance Label + 2–3句 + 今日部署 + Short焦點 + 升級條件 + 降級警告  
   If FT: include `⚡ FAST-TRACK OVERRIDE 觸發 — 首日封頂 30%`. If Change C: `🔓 V-REVERSAL 腿放寬（Change C 生效）`. FT Day2 flags as applicable.
   If Index Drawdown Gate FAIL: include `⚠️ 參與度收縮但指數未跌（距高位僅 −X.X%）— 非底部訊號`. If Gate NEUTRAL + V-REVERSAL: 今日部署 must be 首注輕試 + 封頂 10%.
5. ### ⚠️ 重要旗號 (1–3 or 今日無重大警示; include DATA GAP / EXTREME RATIO / NYMO-NAMO divergence / FT 續鎖 / 無法確認 FT 狀態)
6. ### 附加觀察｜US Market Monitor（CUP／股票層） — **always required** (ingest self-pulled Drive JSON). Skeleton in `docs/cup-market-monitor.md`. Non-scoring. If Drive DATA GAP only: one line under 重要旗號 instead — never invent.
7. ### 附加觀察｜ETF RS 主題傾斜（非計分） — after CUP; Favor / Avoid / **趨勢觀察（sheet 2-day+5-day）** per [ETF RS Theme Tilt](sand-workflow:etf-rs-theme-tilt). Non-scoring.
8. ### 🔔 Modifier Notes (triggered only; omit if none)
9. ### 市場脈絡總結 (100–150字, concrete numbers)
10. Section 8: FOMC + 財報季 + 季節性 + 自我質疑 **Q1–Q8 + Q11** (✅/⚠️ only); ≤200字  
   **Q11:** FT fired while breadth still weak → ⚠️

Internal scoring work may show calcs in chat when Justin asks for audit; the **daily deliverable** follows this lean shape. Boundary: do **not** produce US Market Daily Brief theme package.
