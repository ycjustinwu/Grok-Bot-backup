# HERMES 安裝與操作手冊 — 美股 swing v5.5.4

> 給 Hermes（每日執行的 bot / daemon）讀。目標：裝一次、每天跑、出錯時知道停在哪一步。
> 讀完你應該能回答三個問題：**今天要跑甚麼指令、發甚麼檔、甚麼情況下一律不發。**

---

## 1. 系統在幹甚麼（先看這張圖，30 秒）

```
S1  掃描     us_swing_v55.py    → Contract / Evidence / Trigger（事實）
S2  自檢     invariants.py      → 23 條；exit 2 = 資料不可信
S3  橋接     l2_prep.py         → L2_Input.csv + story_handoffs.md（基準 verdict 由程式算）
S4  故事     DeepSeek（上網）    → stories/<T>_story.json + _search_log.json
S5  決策     DeepSeek（L2）      → verdicts_US.jsonl（只能降級）
S6  閘門     check_verdict.py   → V1–V17；exit 2 = 一律不發
S7  排版     render_report.py   → reports/index.md + 每檔快報 + image_pack
S7b 上傳     Hermes             → Google Drive，回填 full_report_url
S8  圖卡     用戶人手（ChatGPT） → <T>_card.png（可之後補）
S9  發送     Hermes             → index + ✅ 快報
```

**你負責 S1–S3、S6–S7、S7b、S9。S4/S5 是 DeepSeek，S8 是人。**

---

## 2. 安裝（新機器）

### 2.1 前置

| 項目 | 要求 |
|---|---|
| Python | 3.11 或以上（實測 3.12.3） |
| 套件 | `pip install -r requirements.txt` |
| 網路 | 需要（Yahoo Finance、你的 Google Sheet） |
| 時區 | **系統時區要設 Asia/Hong_Kong**（`run_daily.sh` 用本機日期命名資料夾） |
| 磁碟 | 每次 run 約 15–20 MB（逐檔歷史 CSV 佔大部分） |

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2.2 放哪裡

把 `01_RULES/`、`02_CODE/`、`03_SAMPLE/` 之外的**內容**放進一個工作目錄，例如：

```
/opt/us-swing/
  us_swing_v55.py  base_layer.py  gates.py  pullback.py  levels.py  regime.py
  invariants.py  replay.py  stats.py  check_fields.py
  l2_prep.py  check_verdict.py  render_report.py  forward_log.py  story_search_sync.py
  run_daily.sh  run_l2.sh  tickers.txt
  PLAYBOOK_v5.4.md  WORKFLOW_v55.md  DATA_DICTIONARY.md  CLAIMS_LEDGER.md
  story_search/...        （由 01_RULES/story_search 搬過來，放在規則旁邊）
  experiments/...
  runs/                   （每天自動建立：runs/run_YYYYMMDD/）
```

> `02_CODE/` 裡的檔案是**平的**（全部同一層），因為模組之間用 `import gates` 這種方式互相引用。
> 不要把它們放進子資料夾。
>
> 每次 run 的輸出固定落在 `runs/`，所以工作目錄本身不會被 `run_*` 塞滿。

### 2.3 股票清單

`tickers.txt`：一行一個美股代號，`#` 開頭是註解，空白會被忽略。

```
# 34 隻示範清單
UNH
INTA
...
```

`run_daily.sh` 會把它組成逗號分隔傳給引擎；也可以臨時用 `SWING_TICKERS=UNH,INTA ./run_daily.sh` 覆蓋。

### 2.4 權限

```bash
chmod +x run_daily.sh run_l2.sh
```

### 2.5 驗證安裝

```bash
./verify_install.sh
```

看到 `ALL CHECKS PASSED` 才算裝好。它會：編譯所有程式、對 `03_SAMPLE` 跑不變量、
跑欄位檢查、跑 L2 閘門、跑一次排版（在暫存目錄，不會弄髒樣本）。

---

## 3. 從舊版升級（patch）

你可能是 v5.2 或 v5.4。**做法一樣：備份 → 覆蓋程式 → 保留資料 → 驗證。**

### 3.1 一鍵

```bash
cd /path/to/hermes_package
./patch_from_v52.sh /opt/us-swing          # 換成你的實際目錄
```

它會：

1. 把舊檔備份到 `/opt/us-swing/_backup_<時間戳>/`
2. 覆蓋所有 `.py`、`run_daily.sh`、`run_l2.sh`
3. **不覆蓋** `tickers.txt`（你的清單）
4. **不碰**任何 `run_*` 資料夾（歷史紀錄）
5. 印出「改了哪些檔」與下一步

### 3.2 手動（想自己控）

要覆蓋的檔：

```
us_swing_v55.py  base_layer.py  gates.py  pullback.py  levels.py  regime.py
invariants.py  replay.py  stats.py  check_fields.py
l2_prep.py  check_verdict.py  render_report.py  forward_log.py  story_search_sync.py
run_daily.sh  run_l2.sh
PLAYBOOK_v5.4.md  WORKFLOW_v55.md  DATA_DICTIONARY.md  CLAIMS_LEDGER.md
01_RULES/story_search/**
experiments/**
```

**保留不動**：`tickers.txt`、`run_*`、`forward_log.csv`（如果有）、`positions.csv`。

### 3.3 升級後必須改的三個地方

| # | 位置 | 改成 |
|---|---|---|
| 1 | 你的 cron / scheduler | 指令改為 `./run_daily.sh`（它會自動找 `us_swing_v55.py`，找不到才退回 v54） |
| 2 | 你的 bot 發送邏輯 | 只發 `reports/index.md` + index 中 ✅ 的檔；**不再有 TradeBook** |
| 3 | 你的 Drive 上傳 | 新增 S7b：上傳快報到 `US_Swing/YYYY-MM-DD/` |

### 3.4 升級後驗證

```bash
cd /opt/us-swing && ./run_daily.sh          # 真跑一次
python3 check_fields.py PLAYBOOK_v5.4.md runs/run_<日期>/Contract_US.csv
```

第一行要 exit 0；第二行要 `all referenced fields exist`。

> **舊版 v5.2 的 `_SwingAnalysis.csv` 仍然可以讀**（replay 用），但不要用舊的欄位名寫新邏輯。

---

## 4. 每天怎麼跑

### 4.1 時序（HKT）

```
05:30  run_daily.sh                 → runs/run_<HKT日期>/
05:35  run_l2.sh prep               → L2_Input + story_handoffs
05:45  （DeepSeek 做 S4/S5，交回 stories/ 與 verdicts_US.jsonl）
06:20  run_l2.sh check              → exit 2 就停
06:25  run_l2.sh render             → reports/
06:30  上傳快報到 Drive、填 full_report_url
06:35  發送
```

> 資料夾用 **HKT 日期**（例如 11-06 05:30 跑的是 11-04 美股收市資料）。
> 真正的交易日看 `Contract_US.csv` 的 `Date`。

### 4.2 指令

```bash
cd /opt/us-swing

# 1) 掃描 + 自檢（exit 2 就不要往下）；輸出在 runs/run_<日期>/
./run_daily.sh

# 2) 橋接（自動抓最近一個有 L2_Input.csv 的 run 當「昨日」）
./run_l2.sh prep runs/run_20261106

# 3) 等 DeepSeek 放好 stories/*.json 與 verdicts_US.jsonl
#    然後：
./run_l2.sh check runs/run_20261106      # exit 0 才繼續
./run_l2.sh render runs/run_20261106

# 4) 發送
#    reports/index.md + index 中 ✅ 的 <T>_投資快報.md
```

一次做完（不含 S4/S5）：

```bash
./run_l2.sh all runs/run_20261106
```

### 4.3 退出碼 — 這是唯一的判斷依據

| 指令 | 0 | 1 | 2 |
|---|---|---|---|
| `run_daily.sh` | 正常，輸出 `runs/run_<日期>/` | 引擎失敗（多半是網路／Yahoo） | 不變量 FAIL → **資料不可信** |
| `run_l2.sh check` | 可以發 | — | **一律不發**，改發 `L2_Check_Report.md` |
| `run_l2.sh render` | 正常 | — | （已改為不因內容失敗；只有在程式錯誤時非 0） |

### 4.4 失敗了怎麼辦

| 症狀 | 處理 |
|---|---|
| `run_daily.sh` exit 1 | 看 log 尾巴。多數是 Yahoo 限流 → 隔 10 分鐘重跑一次，仍失敗就今天不發 |
| `run_daily.sh` exit 2 | 讀 `runs/run_<日期>/Invariant_Report.md` 的 FAIL 行。**不要手動改資料**，這是資料或程式問題 |
| `check` exit 2 | 讀 `L2_Check_Report.md`。若是 L2 寫錯（例如引用了不存在的 URL），請 DeepSeek 重做，不要自己改 verdict |
| `l2_status.json` = `DATA_STALE` | Contract 日期不是最近交易日（設了 `SWING_EXPECTED_DATE` 才會檢）。確認是否假期 |
| 沒有 `verdicts_US.jsonl` | `check` 會直接 exit 2 並說「layer 2 has not run yet」 |

---

## 4b. 風險閘門（v5.5.4 起）

`Trigger_US.csv` 只會出現 `Tradeable=PASS` 的票。這是建倉前就用**計劃止損**算的：
風險 ×ADR ≤ 1.2、風險 % ≤ 8、空間 ≥ 家族門檻。任一不過 → 不出票，該檔只留在 WATCH。

- 你**不需要**自己判斷風險；看到票就代表它已過閘。
- `Tradeable_Why` 寫明被擋原因（含數字），要解釋就照抄。
- 想放寬用環境變數（`SWING_RISK_ADR_CAP` / `SWING_RISK_PCT_CAP`），不要改程式。
- `I30` 會檢查「每一張票都是 Tradeable=PASS」，失敗即代表有人繞過閘門。

## 5. L2 階段（你不執行，但要會驗）

DeepSeek 交回兩樣東西：

| 檔案 | 內容 |
|---|---|
| `stories/<T>_story.json` | 敘事（主線、Why Now、護城河、數字、風險、信念、來源） |
| `stories/<T>_search_log.json` | 每一條搜尋與命中 URL |
| `verdicts_US.jsonl` | 每檔一行：verdict、entry、stop、conviction、closer… |

**你要做的只有一件事：跑 `check_verdict.py`，然後照 exit code 決定發不發。**

它驗 17 條，最重要的五條：

| ID | 意思 |
|---|---|
| V1 | 不可以升級（WATCH 不能變 BUY） |
| V2 | entry / stop 必須等於 Contract（誤差 ≤0.01） |
| V4 | BUY 必須 `Risk_OK=PASS`、財報不是 PASS/UNKNOWN |
| V12/V13 | 每個來源／數字都要出現在搜尋紀錄裡（防編造） |
| V10 | 掃描失敗時只准輸出一行 NO_TRADE |

---

## 6. 檔案契約（誰產生、給誰）

| 檔案 | 產生者 | 你會不會用到 |
|---|---|---|
| `Contract_US.csv` | S1 | 上游（L2 讀） |
| `Trigger_US.csv` | S1 | 明日委託單（人看） |
| `handoff_US.md` | S1 | 人看 |
| `Invariant_Report.md` | S2 | 出錯時讀 |
| `L2_Input.csv` | S3 | 上游 |
| `story_handoffs.md` | S3 | 給 S4 |
| `l2_status.json` | S3 | **你要讀**：不是 OK 就不要發 |
| `verdicts_US.jsonl` | S5 | 你餵給 check / render |
| `L2_Check_Report.md` | S6 | 失敗時發這個 |
| `reports/index.md` | S7 | **你要發** |
| `reports/<T>_投資快報.md` | S7 | **你要發** |
| `reports/<T>_image_pack.md` | S7 | 給人貼 ChatGPT |
| `stories/Story_Search_DB_rows.csv` | 同步腳本 | 給人貼 sheet |

---

## 7. 發送規格

### 7.1 發甚麼

1. **`reports/index.md` 全文**（每日交易簿：概況／變化／掛單／觀察／持倉／報告連結）
2. index 中標 **✅** 的每一檔 `<T>_投資快報.md`
3. 有 `<T>_card.png` 就附；沒有就跳過（不要寫「圖卡失敗」）

### 7.2 不發甚麼

| 情況 | 做法 |
|---|---|
| `check` exit 2 | 只發 `L2_Check_Report.md`，並講「今日不發交易簿」 |
| `l2_status.json` ≠ OK | 只發一行 NO_TRADE + 原因 |
| 當日沒有 BUY/STALK | 照發 index（會寫「今日沒有可發送的報告」） |

### 7.3 Drive 上傳（S7b）

```
資料夾：US_Swing/YYYY-MM-DD/          （日期用交易日，例如 2026-11-04）
檔案：  <T>_投資快報.md
權限：  受限制（只限本人）— 不要用「知道連結的任何人」
回填：  full_report_url
```

- 上傳失敗 → `full_report_url` 留空，**照樣繼續**，不要因此不發。
- 圖卡之後補傳到**同一個資料夾**即可。

### 7.4 不可以做的事

- ❌ 改任何價格、verdict、conviction
- ❌ 在 `check` FAIL 時「只發一部分」
- ❌ 用昨天的 `reports/` 補今天
- ❌ 自己呼叫圖像 API 生成圖卡（S8 是人手）
- ❌ 把 `full_report_url` 寫成「知道連結的任何人」權限

---

## 7b. 第二個市場（港股）

同一支引擎，只換 profile。`markets.py` 收藏市場常數（基準、指數、日曆、時區、門檻）。

```bash
SWING_MARKET=hk ./run_daily.sh        # 讀 tickers_hk.txt → runs/hk/run_<日期>/
```

| | 美股 | 港股 |
|---|---|---|
| RS 基準 | `SPY` | `2800.HK`（含息 ETF；不用 ^HSI 的原因見 HK_PORT_PLAN §7b） |
| 日曆 | NYSE | XHKG |
| Regime | Sheet 的「美股」區塊 | Sheet 的「港股」區塊 |
| 流動性閘門 | 內建（$20M/日） | **關閉**（用戶在 TradingView 先過濾） |
| 每手股數 | 1 | 不處理（用戶自行調整） |

市場會寫進 Contract 的 `Market` 與 `Benchmark` 兩欄，快報的「RS（對 …）」會自動跟著變。
輸出檔名仍是 `Contract_US.csv` 等（歷史命名），**靠資料夾分辨市場**。

## 8. 環境變數

| 變數 | 預設 | 用途 |
|---|---|---|
| `SWING_TICKERS` | 讀 `tickers.txt` | 臨時覆蓋清單（逗號分隔） |
| `SWING_ASOF` | 空 | 重播某日（`YYYY-MM-DD`）；設了就**不會**跑 forward_log |
| `SWING_OUTPUT_FOLDER` | `run_<日期>` | 自訂輸出資料夾 |
| `SWING_EXPECTED_DATE` | 空 | 設了就檢查 Contract 日期；不符 → `DATA_STALE` |
| `SWING_FORWARD_LOG` | `0` | `1` 才累積前瞻紀錄（預設關，無回測） |
| `SWING_MAX_BUYS` | `3` | L2 每日 BUY 上限（V5） |
| `SWING_WEAK_BUY_RULE` | `0` | `1` 時，B/NA 質素 + 空間<1.5R + 非領導 → 基準 BUY 降為 STALK |
| `SWING_INDEX_20EMA_RULE` | `0` | 保留；目前 L1 未輸出該欄，設了也無效 |
| `SWING_MARKET` | `us` | `us` 或 `hk`；決定基準、日曆、regime 區塊、股票清單 |

---

## 9. 疑難排解

| 訊息 | 原因 | 對策 |
|---|---|---|
| `no engine (us_swing_v55.py / us_swing_v54.py)` | 檔案沒複製齊 | 重跑 `patch_from_v52.sh` |
| `us_swing_v55.py missing` | 同上 | 同上 |
| `pandas.errors... NA` / 欄位全空 | 舊版用 `NA` 字串 | 必須用 v5.5.4（已改 `NOT_APPL`） |
| `check_fields.py` 說 MISSING | playbook 與 Contract 不同步 | 回報，不要自己改 playbook |
| `Invariant I18 ... missing` | Contract 欄位不對 | 確認跑的是 `us_swing_v55.py` |
| 掃描很慢 / 卡住 | Yahoo 限流 | 降低 ticker 數、隔 10 分鐘 |
| `KeyError: 'Ticker'` | 餵錯檔（不是 Contract） | 確認路徑 |

**通則：任何一個 exit 2，今天就不發。** 少發一天，比發錯一個價格好。

---

## 10. 紅線（違反任何一條，整個系統的信任就沒了）

1. 不可以自己算價格、自己改 stop。
2. 不可以把 WATCH / AVOID 升成 BUY。
3. 不可以在閘門 FAIL 時發送。
4. 不可以用過期資料（`l2_status` 不是 OK）。
5. 不可以把「掃描器無訊號」講成「今天沒有機會」——如實講沒有 setup。

---

## 11. 安裝驗收清單

跑完 `./verify_install.sh` 之後，逐項打勾：

- [ ] `python3 --version` ≥ 3.11
- [ ] `pip install -r requirements.txt` 無錯
- [ ] `chmod +x run_daily.sh run_l2.sh`
- [ ] `tickers.txt` 有你的清單
- [ ] `./verify_install.sh` → `ALL CHECKS PASSED`
- [ ] cron 已設（見下）
- [ ] Drive 上傳有權限、資料夾路徑正確
- [ ] bot 發送邏輯已改（只發 index + ✅）

### cron 範例

```cron
# 週二至週六 05:30 HKT（美股週一至週五收市後）
30 5 * * 2-6 cd /opt/us-swing && ./run_daily.sh >> log_cron.txt 2>&1
```

> 05:30 HKT = 前一日美股 16:00 ET 收市後約 1.5 小時。週六跑的是週五的資料。

---

## 12. 一星期試跑協議（用戶要求）

頭七天**不做任何實際交易**，每天核對三樣：

1. 快報的價格 = Contract 的價格（抽查兩檔）
2. `L2_Check_Report.md` 全 PASS
3. 圖卡（人手生成）的入場／止損／阻力 = 快報

七天後回顧：哪一天的 `check` 失敗過、為甚麼。那是這套系統最值錢的紀錄。
