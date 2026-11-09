# v6.1 — 第一批修正（2026-11-07）

> **檔案整理（v6.8 後）**：本文提到的 `tests/batch1.py` … `batch7.py` 已全部合併為
> **`app/code/tests/suite.py`**（50 個案例，單一入口）。以下記錄保留原檔名以便追溯。


來源：Claude 對 v6.0 的審閱（C1–C6）。**只修 bug，不改任何門檻或幾何。**

## 約束

| 約束 | 結果 |
|---|---|
| 不改門檻／幾何 | ✅ 只動 `l2_prep` / `check_verdict` / `invariants` / 文件 |
| 同一份樣本 Contract 109 欄逐格不變 | ✅ 見 §7 |
| 每項附回歸測試 | ✅ `tests/batch1.py`（12 項） |

---

## 1. I29 是死的（C5）

**問題**：`load()` 用預設 `pd.read_csv`，字面 `NA` 早已變成 NaN，I29 永遠看不到它。

**修法**：I29 自己用 `keep_default_na=False` 重讀原始 CSV，只檢查狀態欄。

**驗證**：往 `Volume_Confirm` 塞 `NA` → `FAIL I29 {'Volume_Confirm': ['NA']}`；乾淨樣本 PASS。

---

## 2. baseline 可被 L2 改掉（C4/V1）

**問題**：`check_verdict` 讀 `L2_Input.csv` 的 baseline，而 L2 與它在同一個資料夾。

**修法**：
- `l2_prep.compute_baseline()` 成為唯實作（S3 與 S6 共用）。
- `check_verdict` 用 `l2_status.json` 記錄的**旗標**重算 baseline → **V1b**。
- `l2_status.json` 記錄 Contract 與 L2_Input 的 **sha256** → **V1c**。

**為甚麼要記旗標**：`SWING_INDEX_20EMA_RULE` / `SWING_WEAK_BUY_RULE` 是環境變數，
兩邊不一致會產生誤報。現在以 S3 當日記錄的旗標為準。

---

## 3. V6 可被一句話繞過（C4）

**問題**：`[col for col in c.columns if col in reason]`——`Market`、`Date`、`Close` 都是欄位名，
"Market sentiment bad" 就能過。

**修法**：`l2_prep.downgrade_codes()` 預先為每檔算出可引用的規則碼
（`RSI_HOT`、`EXT_MA20`、`THIN_ROOM`、`SOFT_LEVEL`、`NOT_LEADER`、`LOW_VOLUME`、
`EARNINGS_CAUTION`、`EARNINGS_UNKNOWN`、`EARNINGS_SOON`、`WEAK_QUALITY`、`PROV_RISK`、`BASE_FAILED`），
每碼帶 `field` / `value` / `why`，寫入 `L2_Input.csv` 的 `Downgrade_Codes`。
V6 只接受這個清單裡的碼；自由文字一律 FAIL。

---

## 4. V9 不檢查散文裡的價格（C4/V2）

**問題**：`closer` 與 `invalidation` 的價格完全沒驗證，「收市跌穿 392.50」可以寫成任何數字。

**修法**：抽出兩個欄位裡所有帶小數的價格，必須落在該檔 Contract 的允許集合內
（`Entry_Ref`、`Invalidate_Below`、`Trigger_Price`、`Supply_Level`、`Supply_Soft_Level`、
`Close`、`MA10/20/50`、`POC_60D`、`VAL_60D`、`SR_Flip_Level`），容差 0.5%。

> 沒有採用「佔位符由 renderer 填」的方案：那要改 verdicts 的 schema，
> 屬於第二批（會動到輸出格式）。先用價格白名單，效果等價且不動 schema。

---

## 5. STALK 可以帶著已知風險開單（C6）

**問題**：`C_WATCH + NOT_YET → STALK` 不看 `Risk_OK`。C_WATCH 的定義就是 Setup PASS + Risk FAIL，
所以「延伸 18%」的待突破 base 也會拿到一張活的 buy-stop。

**修法**：
- `baseline_verdict`：只有 `Risk_OK == PENDING` 才 STALK，FAIL/UNKNOWN 一律 WATCH。
- **V4c**：`STALK` 且 `Risk_OK ∈ {FAIL, UNKNOWN}` → FAIL。
- 未知的 `Candidate_Class` 由「靜默 AVOID」改為 **raise**。
- 修正 `DATA_DICTIONARY` 對 C_WATCH 的定義（舊版寫「風險不可用」，與程式不符）。

**窮舉測試**：4 個 class × 8 個 feasibility × 4 個 risk = 128 組合，
斷言「沒有任何 BUY/STALK 帶 FAIL/UNKNOWN 風險」。

**與 A1 的交互（要記錄）**：A1 的回歸測試原本用 `Risk_OK='FAIL'` 造出 STALK，
再驗證盈利覆寫。C6 修好之後，那條路徑不再產生票，A1 的前提就不成立了。
已把 A1 測試改成在 `Risk_OK='PENDING'`（真正有票）下驗盈利覆寫，
並新增一條「Risk FAIL + 盈利 PASS → WATCH（無票）」。
**A1 的意圖保留，只是換了合法的前提。**

---

## 6. `Days_To_Earnings` 單位四處矛盾（C6）

引擎是 NYSE **交易日**（v5.3 F11），字典寫「日曆日」，handoff 與快報寫「交易日」。
統一為**交易日**，字典改正，並註明 `≤7` / `8–14` 兩個門檻也是交易日。

---

## 7. Contract 逐格不變（證明）

引擎未改一行。以 `SWING_ASOF=2026-11-04` 重跑 34 隻，與批前樣本逐格比對：

34 隻 × 108 欄，**只有 1 格不同**：ROL 的 `High_52W` 由 65.3972 → 65.3971（−0.0001，
Yahoo 資料抖動），下游 Supply / Room / Class 全部不變。詳見 `BATCH1_CONTRACT_DIFF.md`。

---

## 未做（第二批）

| 項目 | 為甚麼 |
|---|---|
| 52 週高懸崖（`0.25×ATR` 改「跳過」而非「忽略」） | 屬幾何 |
| 風險帶方向（風險帶內失敗率 53.5%、帶外 37.4%） | 屬門檻，要先做 episode 級存活分析 |
| 量能 1.5× 的門檻 | 同上（目前量比對失敗率 1.3σ，不顯著） |
| 港股零量／半日市 | 屬資料層 |
| 散文價格佔位符 | 屬 schema |
| 突變測試 | 下一輪（需先有 10–15 個突變腳本） |

---

## 8. 港股端到端（補測，同日）

原本只測到 L1+S3（12 隻港股 → Contract）。**沒有測 S4–S7**，所以港股從來未產出過一份快報。
補測兩隻有票的（6862.HK BUY、2269.HK STALK），用真實搜尋寫 story + verdicts，跑完整條鏈。

結果：**閘門 0 FAIL、兩份快報產生、index 正常**。

### 這一輪立刻暴露三個只會在港股出現的 bug

| # | 問題 | 位置 | 修法 |
|---|---|---|---|
| 1 | handoff 寫死 `MARKET: US` | `l2_prep.handoff_block` | 讀 Contract 的 `Market` 欄 |
| 2 | 快報表頭寫死 `市場：US` | `render_report.render` | 讀 `Market` 欄 |
| 3 | 價格一律印 `$`（港股應為 HK$） | `render_report.p()` | 按 `Market` 切換 `$` / `HK$` |

三個都不是幾何或門檻問題，是**市場標籤與幣別**。美股永遠測不出來。

### 檔案命名約定（給寫 story 的人）

`stories/<TICKER>_story.json`，ticker **保留原本的點**：`6862.HK_story.json`（不是 `6862_HK_...`）。
`check_verdict` 與 `render_report` 都用 `f'{ticker}_story.json'` 組路徑。

---

# v6.2 — Grok 審閱的第二批（2026-11-07）

來源：Grok 對 v6.1 的審閱。逐條核對後：**2 條真 bug、3 條測試空窗、2 條已覆蓋、1 條延後。**

## 已修

### G1 `baseline_verdict` 仍可在不可達路徑產生「Risk FAIL 的 STALK」（真 bug）

**Grok 的發現，而且我的 128 組窮舉測試漏了它**——因為我把 `Earnings_Proximity_Flag` 固定成 `CLEAR`，
沒有測盈利覆寫與風險檢查的先後次序。

順序問題：盈利覆寫把 `BUY → STALK`，而風險檢查只寫 `if v == 'BUY'`，於是 STALK 跳過了風險檢查。

**修法**：在盈利覆寫**之後**再加一道最終檢查：

```python
if v in ('BUY', 'STALK') and Risk_OK not in ('PASS', 'PENDING'):
    v = 'WATCH'
```

**驗證**：4 種 Risk × 4 種 Earnings = 16 組；斷言「FAIL/UNKNOWN 風險下永不產生票」。
另外單獨斷言 Grok 給的那個組合 → WATCH。

### G2 V9 價格白名單太鬆，而且漏整數（真 bug + 已知殘餘）

**兩個問題**：
1. 容差 0.5% 太鬆——港股的 `47.65`（`BuyStop_Max_Stop`）之所以過關，是因為它**撞中了 MA20 = 47.677**，
   不是因為它在白名單裡。這等於檢查靠運氣。
2. 只檢查帶小數的數字，「跌穿 400」完全不查。
3. `BuyStop_Max_Stop` 根本不在白名單裡。

**修法**：
- 容差收緊到 **0.02% 或 1 仙**（取較大者）。
- 加入 `BuyStop_Max_Stop`。
- 改用 token 抽取 + 後置過濾：小數或 ≥3 位整數都算價格候選；跟隨 `% 家 次 億 萬 元 年 月 日 倍 季 個 隻 檔 點 天`
  的、日期（`2026-01-12`）、`MA20` 這類識別碼一律排除。

**驗證**：`跌穿 400` → 被檢查；`MA20`、日期、`1322 家`、`223.37 億元` → 不誤殺。

### G3 base 幾何凍結：補回歸測試

用合成資料：偵測一次 → append 一根不可能屬於該 run 的 bar → 再偵測 → 斷言同一 episode 的 high/low 不變。

### G4 `PROV_THIN`：區分「暫代 R 造成的薄空間」

`Room_Basis = PROV_1ADR` 且 `Room_To_Supply_R < 1.5` 時，除了 `PROV_RISK` 再加一個 `PROV_THIN`。

### G6 I17 / I25 / I27 由死變活

三條不變量原本在真實樣本「沒有對象可檢查」而 PASS。現在用最小合成 Contract 測：

| 不變量 | 合成案例 | 結果 |
|---|---|---|
| I17 | STRICT base 45 日（上限 30） | **FAIL** ✅ |
| I25 | TRIGGERED 且收盤 < 突破日低 | **FAIL** ✅ |
| I27 | A_SETUP + `Volume_Confirm=LOW` + 無 REMARK | **FAIL** ✅ |

順手修了一個 crash：`Class_Note` 全空時 `.str.contains` 會拋 `AttributeError`（合成 Contract 撞到）。

### G7 `downgrade_rate`

`check_verdict` 寫入 `l2_status.json`：當日有票時的降級比率。**不做閘門**，但在 0% 時印 WARN
（「2 張票、0 張降級——檢查 L2 是否有增值」）。

## 未採納（附理由）

| Grok 建議 | 為甚麼不做 |
|---|---|
| **SOFT_NEAR 代碼** | `SOFT_LEVEL` 已經存在（`Room_To_Soft_R < 1` 時發出）。再加一個只會重複。 |
| **`data_revision_flag` 進 Evidence** | 要改引擎與 Contract → 違反「第一批 Contract 逐格不變」；屬第二批資料層。 |
| **散文價格一律帶一位小數** | 約束 L2 寫法而非驗證輸出；收緊容差後已達到同樣效果。 |
| **港股 `Shares_per_1000_Risk` 註解** | 已在 DATA_DICTIONARY 的 D15 註明；報告加註屬下一輪文件整理。 |

## 測試總覽

```
tests/batch1.py     12/12
tests/batch2.py      7/7
tests/regressions.py ALL PASS（A1–A12）
不變量  美股 23 PASS · 港股 23 PASS
閘門    美股 0 FAIL · 港股 0 FAIL
```

---

# v6.3 — 港股 patch（只影響港股 ticker）

US 流程已完成，唔再擴 scope。呢一輪只做**港股獨有**嘅三件事，骨架全部沿用。

## 1. 零成交 bar 唔再算「壓縮」

**問題**：壓縮條件係 `range ≤ ADR` 且 `vol < 0.85×Vol20`。零成交 bar 兩條都完美符合，
所以一段停牌／無人交易嘅日子會變成一個「完美 base」。Yahoo 多數唔出停牌日，
但對流動性差嘅港股會回傳 `Volume = 0` 的 bar。

**修法**（`base_layer.detect_bases`）：壓縮判定加 `Volume > 0`。

**驗證**：
- 合成 60 根零成交 bar → **0 個 episode**；同一批改回正常成交量 → 1 個 episode。
- 美股 34 隻 × 16,849 根裡其實有 **14 根零成交 bar**（不是零），所以不能假設「美國冇影響」。
  用 `SWING_ASOF=2026-11-04` 重跑對照：**Contract 只差 1 格**（ROL 的 `High_52W` 1e-4 資料抖動），
  即那 14 根都不在壓縮 run 內，守衛對美國輸出零改變。
- 港股 39 隻 × 19,110 根有 **233 根零成交 bar（1.2%）**——守衛在這裡才有實際作用。

## 2. 港股清單由 12 隻擴到 40 隻

`tickers_hk.txt` 換成 40 隻流動性較好的港股（騰訊、阿里、美團、小米、港交所、平安、
建行、友邦、中芯、藥明生物、海底撈、網易、京東、吉利、安踏、李寧、三桶油、中移動、
匯豐、新地、中銀香港、國壽、招行、比亞迪、理想、蔚來、小鵬、快手、京東健康、金沙、
銀河、創科、中電、長建、長實…）。

第一跑：**39/40 成功**，`0011.HK`（恒生銀行）Yahoo 已無資料（私有化），已從清單移除。

## 3. 港股 Runbook

新增 `HK_RUNBOOK.md`：跑的時間（**17:30 HKT 之後**，唔係 05:30）、基準為何用 2800.HK、
代號格式、每手／流動性／印花稅為何唔做、零成交與半日市嘅處理。

## 實跑結果（39 隻）

```
109 欄 · 23 條不變量全過
A_SETUP 2（6862 海底撈 BREAKOUT、0386 中石化 PULLBACK）
C_WATCH 9 · B_LEADER_WAIT 5 · X_NONE 23
baseline：BUY 2 / STALK 1 / WATCH 13 / AVOID 23
```

順便驗證咗 C6 規則在真實港股生效：2269（Risk=PENDING）→ STALK；
3968（Risk=FAIL 的 C_WATCH）→ WATCH。

## 仍然唔做（你嘅決定）

每手股數、流動性閘門、印花稅、半日市量能標準化。四項都寫入 runbook 嘅「唔做」表。

---

# v6.4 — 港股 patch（Claude 審閱後的批次 1）

## 逐條核對

| Claude | 我 | 處理 |
|---|---|---|
| #8 五位數代號 `00700` → `00700.HK` | **真 bug** | 先去前導零再補 4 位 |
| #6 財報 why 放錯分支 | **真 bug** | why 搬回財報分支；Risk 分支刪走財報字樣 |
| #5 V9 誤殺 `2800.HK`、漏 2 位數 | **真 bug** | 掃描前剔除代號；整數門檻 3 位 → 2 位 |
| #1 合成日線不留痕 | **真，最嚴重** | 新增 `Bar_Source`；SYNTH 不得觸發突破 |
| #10 幣別寫死 | **真** | `gates` 的 liq 文字與 RULEBOOK 改由 profile 產生 |
| #9 指數寫死 | **部分** | `Sp500_Chg_Pct` 係死欄（全 NaN）→ **直接刪除**，唔改名 |
| #2 override 作用域 | **真** | 模組層預設 `{}` |
| K10「港股冇季報」 | **我錯，佢對** | 1071 係 A+H、6160 美股雙重上市，兩者都按季報告。改寫成「Yahoo 覆蓋不足」 |

## 唔採納（附理由）

| Claude 建議 | 為甚麼唔做 |
|---|---|
| 財報 ESTIMATED（去年同期 + 1 年，±10 日） | 用戶指示：財報唔深挖。**有就用 TV，冇就 UNKNOWN + 報告寫「請自行核實」** |
| 來源衝突規則（差 >5 日 → UNKNOWN） | 同上。改成簡單規則：**有明確來源（TV/HKEX）就優先，但仍須 ≥ as-of** |
| `Written_At` 過期檢查 | 同上 |
| HOLD_OFF 新 verdict | 會震動 schema；改用 `Class_Note` 標示 |
| 半日市、Tick_Size、Lot_Size | 屬批次 2；用戶已定每手自行處理 |

## 實際改動

| 檔案 | 改動 |
|---|---|
| `markets.py` | `normalize_ticker` 去前導零；`currency_symbol()` |
| `gates.py` | `configure()` 設定 `cur`；Leader_Why 用 profile 幣別 |
| `us_swing_v55.py` | `Bar_Source` 欄；SYNTH 降級 A_SETUP→C_WATCH；刪 `Sp500_Chg_Pct`；override 優先於 Yahoo；RULEBOOK 由 profile 產生 |
| `l2_prep.py` | 財報 why 歸位；`earnings_overrides` 模組層 |
| `check_verdict.py` | V9 剔除代號、支援 2 位數價 |
| `render_report.py` | UNKNOWN 財報加「（未能確認，請自行核實）」 |

**Contract：1f.4 → 1f.5**，欄數仍然 109（+`Bar_Source`、−`Sp500_Chg_Pct`）。

## 美股影響（實測）

`SWING_ASOF=2026-11-04`，34 隻：

| 項目 | 結果 |
|---|---|
| 欄位 | −`Sp500_Chg_Pct`（全 NaN 死欄）、+`Bar_Source`（全 DAILY） |
| 判斷欄位（Class / 三閘 / 分數） | **逐格相同**（16/11/6/1） |
| 數值差異 | 只在 Regime 區塊（Google Sheet 由 11-05 更新到 11-06）+ ROL `High_52W` 1e-4 |

## 測試

```
tests/batch3.py  7/7（新增）
tests/batch1.py 12/12 · batch2.py 9/9 · regressions A1–A12 全過
港股 6 隻：23 條不變量全過
```

## 未做（批次 2）

`ADR/ATR/Vol20` 只用有成交 bar、半日市、`Tick_Size`/`Lot_Size`、RS 窗口對齊、合成 bar 的兩段跑。

---

# v6.5 — 港股批次 2（只對 HK 生效）

## 改動

| 項 | 內容 | 只對 HK |
|---|---|---|
| H | `Tradable` mask：ADR / ATR / Vol_Avg_20 / Vol_50 只用**有成交**的 bar | ✅ |
| I | `Base_Untraded_Bars`：base 區間內零成交 bar 的數量 | ✅ |
| J | 半日市：由 XHKG 日曆的 session 長度判定（< 中位數 70%），當日不計入壓縮與量能 | ✅ |
| K | HKEX tick 表；`Trigger_Price` 向上取整、`Invalidate_Below` 向下取整；`Tick_Size` / `Tick_Pct` | ✅ |
| O | 新 downgrade codes：`TICK_COARSE`、`BASE_UNTREADED`、`SYNTH_BAR` | ✅ |

Contract：港股 **112 欄**（+`Tick_Size`, `Tick_Pct`, `Base_Untraded_Bars`），美股仍 **109 欄**。

## 美股零影響（實測）

`SWING_ASOF=2026-11-04`，34 隻，批次 2 前後：

```
欄數 109 → 109（無增無減）
差異格數：1（ROL High_52W −1e-4 資料抖動）
Candidate_Class 16/11/6/1 → 16/11/6/1
```

**Hermes 的美股安裝維持 v6.4，不更新**（用戶指示：HK 的修正不要動美國）。

## 測試

```
tests/batch4.py  7/7（tick 表、取整、零量、Tradable mask、HK 代碼）
港股 6 隻：23 條不變量全過
港股 4 隻：閘門 0 FAIL、4 份快報
```

## 自己引入、自己記下的三個問題

| # | 問題 |
|---|---|
| K11 | `Risk_ADR_Plan` 用未取整的價，`Risk_Pct_Plan` 用取整後 → 兩者可能矛盾 |
| K12 | `Tradable` mask 令長期低成交股**永遠冇 base**（可能是對的，但未評估） |
| K2 | 半日市門檻「70% 中位數」是拍的，未用真實早收市日校驗 |

## 未做

RS 窗口對齊（會改全部數值，等批准）、`REGIME_INDEX` 寫死、每手股數、印花稅。

---

# v6.6 — RS guard（用戶批准的三行）

## 是甚麼

`RS_Score` 用「股票自己 63 根」減「基準自己 63 根」。股票缺 bar 時兩條腿窗口不同。
實測（0700 模擬）：缺 3 根差 +3.3 點、缺 5 根差 +7.7 點——足夠跨過 RS ≥ 10。

## 但今日 0/73 隻受影響

| | 窗口內缺 bar | RS 差 | 翻轉 |
|---|---|---|---|
| 港股 39 | 0 | 0.00 | 0 |
| 美股 34 | 0 | 0.00 | 0 |

所以**唔重算**（會改全部數值），改為拒絕信任：

- 最近 63 個基準交易日缺 ≥3 根 → `RS_Status=STALE`、`Leader_OK=UNKNOWN`
- 完整數據的股票：**零影響**（實測港股 6 隻、美股 34 隻全部 OK）

## 測試

`tests/batch5.py` 3/3：guard 觸發 → UNKNOWN；完整數據仍照常判斷；門檻是 3 不是 2。

## 用戶決定關閉的項目（已寫入 review pack 的 06_USER_DECISIONS.md）

每手股數、印花稅、港股 regime 第二意見、流動性閘門。呢四項唔會再出現在 backlog。

---

# v6.7 — 回應 Claude 對 v6.4–v6.6 diff 的審閱

## 三項「聲稱已修、實際無效」

| # | 問題 | 修法 |
|---|---|---|
| 1 | `earnings_overrides` 修在 `l2_prep`，用的人在引擎 | 移到引擎模組層；`l2_prep` 的重複行刪除 |
| 2 | `RULEBOOK_ROWS` 是 import 時求值的清單 | 改為 `build_rulebook_rows()`，寫檔時求值。實測港股印 `HK$1` + `no liquidity gate` |
| 3 | override 別名 `zfill(4)` 對 `01071` 無效 | 別名改經 `markets.normalize_ticker`（固定用 HK profile） |

## 新功能的邏輯錯誤

| # | 問題 | 修法 |
|---|---|---|
| 4 | `Base_Untraded_Bars` 用最後 N 根回推 | 改用所選家族的凍結 `Start`/`End`；無 base → **NA**（不是 0） |
| 5 | tick 取整在 gates 之後 | 取整移入 `gates.evaluate`、風險運算**之前**；`BuyStop_Max_Stop` 一併；浮點用 `round(p/t, 6)` |
| 6 | SYNTH 降級後 `Screen_Flag` 不同步 | 同步 `Screen_Flag=WATCH`、`Entry_Feasible=NOT_YET` |
| 7 | RS guard 覆寫 `Leader_OK`，洗掉 FAIL、破壞 I28 | 只 `checks.insert`，由 `_verdict` 決定（FAIL > UNKNOWN） |
| 8 | 半日市切斷 STRICT base | **用戶決定唔做半日市，整項移除**（含 `half_day_sessions()`） |
| 9 | V9 `CODE_TOKENS` 可被繞過 | 只剝零補四位與 `.HK`；裸 `388` 保留。單位加 `週/周/股/蚊/手/厘/仙` |
| 10 | 兩市場共用 `contract_version` | 改為 `hk-contract-1f.5` / `us-contract-1f.5`（**沒有**統一欄位集） |

## 其他

- override 只在其日期 **≤** Yahoo 日期時才取代（單向 `min`，只會更保守）
- `BASE_UNTREADED` → `BASE_UNTRADED`
- 未做：`Tick_Risk_Share`、RS 對齊判 STALE、Data_Quality 零量比例

## 驗證

```
batch6 8/8（新）· batch5 3/3 · batch4 7/7 · batch3 7/7 · batch1 12/12 · batch2 9/9
A1–A12 全過 · 港股 23 條不變量 0 FAIL
美股 34 隻：109 欄、差異 0 格、Class 16/11/6/1
```

## 測試自身也要改（記錄）

三個舊測試因為行為改變而失效，已更新到**新的正確行為**：
- `batch5`：stale 不再強制 UNKNOWN → 改為「保留 FAIL、且永不 PASS」
- `batch4`：`BASE_UNTREADED` → `BASE_UNTRADED`
- `batch3`：override 預設值的位置由 `l2_prep` 改到引擎

---

# v6.8 — 回應 Claude 對 v6.7 的審閱（三項）

## 1. tick 取整搬到風險判定之前

`Risk_OK`、`Risk_Why`、`Risk_ADR_Plan` 之前用未取整價，`Room` 與 `Shares` 用取整價——同一張票兩套數字。
現在取整在 `lo, hi` 與 `risk_pct` 計算**之前**，全部用同一組價。

**測試**：用輸出的 `Entry_Ref`、`Invalidate_Below` 重算風險%，必須等於 `Risk_Pct_Plan`。
實測 4 張港股票全部相等（1.7647 / 2.4948 / 17.3282 / 3.6900）。

**行為改變**（不是 bug）：6862 的 `Risk_ADR_Plan` 由 0.5935 → 0.6278。用可下單的價算，數字必然變。

## 2. base_layer 不再 round 觸發價

`Planned_Trigger` 改為原值 `high * 1.001`，取整只在 gates 做。
低價股（tick 0.001 / 0.005）不會先被 `round(…,2)` 破壞。

**測試**：`0.2345` + tick `0.005` → `0.235`。

## 3. SYNTH 降級收尾

- `Screen_Flag` 改由**最終** `Candidate_Class` 取值（之前用 `gate_out` 的舊值覆寫）
- `Trigger_US.csv` 跳過 `Bar_Source=SYNTH_60M` 的列

**測試**：SYNTH 行不進 Trigger 表；flag 與 class 一致。

## 4. 半日市：一行固定文字（用戶批准的最低限度）

報告表頭（只限港股）加一句，**零邏輯、不偵測**：
「註：平安夜、除夕、農曆年前夕為半日市，當日成交量偏低，量能判斷請自行留意。」

## 美股仍然零影響

```
欄數 109 → 109
差異格數：0（v6.7 → v6.8）
Candidate_Class 16/11/6/1 → 16/11/6/1
```

**過程記錄**：第一次跑出 27 格差異——`Planned_Trigger` 不再 round 之後，美股 `Entry_Ref`
由 2 位小數變成 4 位。已在 gates 為美股補回 `round(entry, 2)`（僅 `entry_from_planned` 分支）。
自己引入、自己修回。

## 測試

```
batch7 4/4（新）· batch6 8/8 · batch5 3/3 · batch4 7/7 · batch3 7/7
batch1 12/12 · batch2 9/9 · A1–A12 全過
港股 6 隻：23 條不變量 0 FAIL
```

## 未做

`TICK_COARSE` 的 0.3% 門檻（仍在，只作顯示）、統一兩市場 schema（用戶決定）、
RS 對齊判 STALE、Data_Quality 零量比例。
