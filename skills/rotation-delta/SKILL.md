---
name: rotation-delta
description: >-
  Use as Market Awareness step 4.6 — compute the book-ETF rotation delta
  (churn5/10/20 + leader persistence) and render ONE non-scoring line, escalating
  only when a regime rotation fires. Ships its own calculator (rotation_calc.py).
version: 1.1.0
owner: 小小超 (Hermes) → Grok bot (Market Awareness Orchestrator)
scope: non-scoring. Never feeds TOTAL / pillar A / B / band / hysteresis / FT / Change C / Exposure.
---

# Rotation Delta (制度輪動偵測) — Grok 自足版

## 為何存在

Regime score 答「環境幾好」，答唔到「邊個易做、邊個難做」。2026-10 的實例：

- 10-06 ~ 10-14：top-8 = `ARKG/ARKW/BUG/CIBR/DRAM/FOTO/IGV/MAGS/MEME/QQQ/SOXX`（AI 鏈）
- **10-20：top-8 一日全換**（churn5 = 16/16）
- 11-04：top-8 = `IHI/PHO/XHB/XRT/XLV/XLB/IYT/KRE`（醫療器械／水務／建屋／零售／大藥／物料／運輸／銀行）

整段時間 TOTAL 幾乎無反應，因為 TOTAL 量度廣度與宏觀，**唔量度領導權屬誰**。單日快照無法捕捉，因為輪動係「排名隨時間」的物件。所以要存 rank 歷史，再計 churn。

## 何時跑

每次 Market Awareness（v6.4.6）的 **silent compute 階段**，放在 Step 4（Layer Context）之後、Step 5（Index Drawdown Gate）之前。即使 Justin 只問 regime score 都要跑 —— 判定結果可能就係今日最重要那句。

## 一、計算（用附帶腳本，唔准手算）

腳本：`/workspace/market-awareness/rotation/rotation_calc.py`（canonical；skill 目錄有副本；只用標準庫）。

```bash
# A) 有 RS workbook PH_MT 的寬表匯出（首列日期、首行 ticker）
python3 /workspace/market-awareness/rotation/rotation_calc.py --matrix PH_MT.csv --out-state rotation_state.csv --out-history rotation_history.csv

# B) 有長期價存（date,ticker,close）
python3 /workspace/market-awareness/rotation/rotation_calc.py --long prices.csv --out-state rotation_state.csv --out-history rotation_history.csv

# C) 自我驗算（唔需要任何檔案，必須 PASS 才可用）
python3 /workspace/market-awareness/rotation/rotation_calc.py --selftest
```

**資料來源優先序**（任選一個能拿到 30 個以上 session 的）：

1. RS workbook `1D3BrzLH3DmxX8Gv3W9Yhvd9q_LNOGXyNyUzjnXzqmHk` → tab `PH_MT`（首行 ticker、首列日期、由舊到新）。整個 tab 匯出 CSV 即可。
2. Market Master `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` → `ETF_Prices`（ETF 為列、日期為欄的轉置形狀，腳本會自動判向）。111 個日期欄 → 可算出 91 個 session，足夠 churn20 + persist。
3. 若兩者都拿不到 → 走 §四 代理模式，並在報告標 `⚠️ 輪動數據代理`。

腳本自動處理：日期格式（ISO / 斜線 / 日月年）、千分位逗號、缺值、寬表 vs 轉置表、缺書、缺基準。

## 二、定義

```
ratio(t,d)   = close(t,d) / close(VOO,d)
mom20(t,d)   = 100 × ( ratio(t,d) / ratio(t, d−20 sessions) − 1 )
rank(t,d)    = 當日 29 本書按 mom20 的名次（1 = 最強）
in_top8      = rank ≤ 8
persist(t,d) = 過去 20 個 session 中 in_top8 的日數
churnN(d)    = | top8(d) △ top8(d−N sessions) |      對稱差，0–16（8 個位全換 = 16）
```

- 缺當日價的書：該書當日不參與排名（唔准補舊價），並在報告標 `DATA GAP`。
- `S`（Apps Script 的 book score）與 `mom20` 是兩條公式：`S` 揀個股（書內），`mom20` 判輪動（書與書）。**唔准混算、唔准互相換算。**

## 三、四檔判定（腳本已內建，唔准自行改門檻）

| 檔 | 條件（由上往下，先符合先報） | 報告行為 |
|---|---|---|
| ③ **制度輪動**（重大） | `churn5 ≥ 14` **或** `churn10 ≥ 14` | 頂欄 `🚨 制度輪動`；⚠️重要旗號第一條；三、操作立場前置三句 |
| ② **輪動中** | `churn5 ≥ 10` **或** `churn10 ≥ 10`（未達 14） | 頂欄 `🔄 輪動中`；附加觀察寫「舊／新並存，等確認」 |
| ④ **已定格** | `churn5 ≤ 8` **且** `churn10 ≤ 8` **且** `churn20 ≥ 14` | 附加觀察寫「輪動已完成（N 個 session 前），禁止再用舊 proxy」 |
| ① **延續** | 其餘 | 一行過，不升級、不佔版面 |

門檻校準來源：94 個 session（2026-06-24 → 2026-11-04，29 本書、2,723 筆）——
`churn5` 中位 6／p75 8／p90 10／max 16；`churn10` 8／10／12／16；`churn20` 12／14／16／16。
`churn5 = 16` 全樣本只出現過一次（2026-10-20），所以 14 = 「換清光」，10 = p90 = 「開始換」。

判定必須**寫出數字**，唔准只寫形容詞。

## 四、渲染（總共只多 1 行，最多 3 個升級位）

**(a) 頂欄（今日動作）** — 只在 ②③：

```
今日動作：觀望｜🚨 制度輪動（churn10 16/16）｜Exposure 0–10%
```

**(b) `### ⚠️ 重要旗號`** — ②③ 必寫，③ 排第一條：

```
🚨 制度輪動（churn5 16/16）：舊領導 SOXX/DRAM/FOTO/MEME 已被 IHI/PHO/XLV/XRT 取代。
```

**(c) `### 三、操作立場` 前置** — 只在 ③，固定三句：

```
🚨 制度輪動日 → (i) 舊領導 proxy（<清單>）一律當 Headwind，唔准以 Favor 名義開倉；
(ii) 新領導只做 pullback，唔追第一日；(iii) 觀察名單若仍掛在舊書，今日起降權至觀察下限。
```

**(d) `### 附加觀察｜輪動位移（非計分）`** — **每日必出，一行過**，緊貼 `附加觀察｜ETF RS 主題傾斜` 之後。直接貼腳本輸出的第 2、3 行：

```
輪動位移｜churn5 6 ／ churn10 6 ／ churn20 16｜判定：已定格（11 個 session 前完成）
現任：IHI PHO XHB XRT XLV XLB IYT KRE｜上批：FOTO MEME SOXX CIBR IGV MAGS BUG ARKG
```

- ① 就係上面兩行，唔加解釋。
- ② 加一句「舊／新並存，等確認」。
- ③ 加 (c) 三句。
- ④ 加「禁止再用舊 proxy」。

## 五、Fallback（拿唔到歷史／腳本跑唔到）

改用 5 日代理，**必須標示**：

```
churn5_proxy = | top8_by_(S 今日) △ top8_by_(S 5日前) |      # 📊 RS 總覽 D 欄 / F 欄
```

- 代理只有 5 日維度，**唔可以**判 ④（已定格需要 churn20）。
- 代理門檻放寬一級：`≥5` → ②；`≥7` → ③。**未經校準**，只在斷供時用，報告要寫明。
- 連續兩日代理 → ⚠️ 重要旗號加 `⚠️ 輪動指數斷供 n 日`（基礎設施問題，非市場問題）。
- 缺數就寫 `?`，唔准估。

## 六、驗收（腳本已通過，重跑必須一致）

| 截到該日重跑 | 必須輸出 |
|---|---|
| `2026-10-20` | `🚨 制度輪動`，churn 5/16、10/14 |
| `2026-10-21` | `🚨 制度輪動`，churn 5/12、10/16 |
| `2026-10-27` | `🔄 輪動中`，churn 5/4、10/12 |
| `2026-11-04` | `已定格`，churn 6/6/16，top8 = IHI PHO XHB XRT XLV XLB IYT KRE |
| `2026-10-06` | `延續`，churn 6/4/12 |

另外必須成立：TOTAL／band／hysteresis／FT／Exposure 在以上五次重跑中完全一致（diff = 0）。

## 七、紅線（違反即 defect）

1. **Non-scoring**：唔准入 TOTAL／pillar A／B／band／hysteresis／FT／Change C／Exposure。
2. 唔准用輪動去「解釋」當日漲跌（因果倒轉）。輪動係狀態，唔係新聞成因。
3. 缺數唔准估；`churn` 缺一項寫 `?` + `DATA GAP`。
4. 唔准把 `S` 與 `mom20` 混算。
5. ③ 當日**唔可以**放寬 Exposure；要更嚴（新領導只做 pullback）。
6. 唔准每日都出「制度輪動」——只有 ③ 門檻觸發才升級；其餘日子一行過，否則報告會被噪音淹沒，等於冇報。

## 八、輸出檔案契約

`rotation_state.csv`（腳本每日覆寫，1 行 + 表頭）：

```
session,books,churn5,churn10,churn20,rot_state,top8,old8,median_persist
2026-11-04,29,6,6,16,已定格,"IHI:19.8:14,PHO:15.7:14,XHB:14.8:5,XRT:14.6:15,XLV:13.9:14,XLB:11.5:12,IYT:9.2:4,KRE:9.1:3","FOTO:-32.5:29,MEME:-32.4:28,SOXX:-21.7:26,CIBR:-7.4:21,IGV:-4.4:18,MAGS:-3.3:16,BUG:-0.5:13,ARKG:0.4:12",4
```

- 示例的 `mom20` 為求可讀四捨五入至 1 位小數，腳本實際輸出 4 位（例如 `IHI:19.7976:14`）。
- `top8` 元素 = `TICKER:mom20:days_in_top8`（現任領導，越前越強）
- `old8` 元素 = `TICKER:mom20:今日rank`（20 個 session 前的領導，按今日 rank 由差至好排）→ 即「禁用 proxy 清單」
- `median_persist` = 當日 29 本書 persist 的中位數

`rotation_history.csv`（累積，供查核）：

```
date,book,mom20,rank,in_top8,days_in_top8
```

## 九、交接狀態

- 腳本版本 v1.1.0；`--selftest` PASS；五個驗收案例全中（見 §六）。
- 同一份腳本在 Hermes 側用 `data/rs/prices.db`（208 session）跑過，結果與本文件一致（94 session 歷史、2,723 筆）。
- 若日後改 `LOOKBACK`／門檻／`TOP_N`，必須重跑 §六 全部案例並更新本文件，否則唔算改完。
