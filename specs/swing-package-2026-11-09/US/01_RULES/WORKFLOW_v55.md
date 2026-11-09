# US Swing 每日工作流 v5.5 — L1 → Story → L2 交易簿

> **v5.5.3（2026-11-06）**：修復 Hermes 缺陷單 A1–A12，詳見 `BUGFIX_2026-11-06.md`。契約不變（1f.3 / 107 欄）。

一份文件說清楚：每天由掃描到交易簿，每一步讀什麼、寫什麼、誰負責、規則在哪。
**本文件與 `l2_prep.py` / `check_verdict.py` 衝突時，以程式為準，並回報修正文件。**

---

## 0. 一句話分工

> **L1 判斷「是不是好 setup」，Story 搜尋「為甚麼會郁」，L2 寫「怎樣做、做哪幾隻、有甚麼要小心」。**
> 只有 L1 能決定 setup 與價格；Story 與 L2 只可以**降級**，永遠不可以升級。

| 步驟 | 誰 | 讀 | 寫 | 可否改 verdict / 價格 |
|---|---|---|---|---|
| S1 掃描 | `us_swing_v55.py`（`SWING_MARKET=us\|hk`） | Yahoo 數據、tickers.txt / tickers_hk.txt | `Contract_US.csv`、`Evidence_US.csv`、`Trigger_US.csv` | — |
| S2 自檢 | `invariants.py` | run 資料夾 | `invariants.txt` | — |
| S3 橋接 | `l2_prep.py` | Contract + 昨日 `L2_Input.csv` | `L2_Input.csv`、`story_handoffs.md`、`l2_status.json` | **計算**基準 verdict |
| S4 故事 | **DeepSeek（上網）** | `story_handoffs.md` + `story_search/`（規則目錄下）+ `KB/` | `stories/<T>_story.json`、`<T>_search_log.json` | 不可（只標 CONFIRM/CHALLENGE/NEUTRAL） |
| S5 決策 | DeepSeek（L2） | `L2_Input.csv` + `stories/*` + `positions.csv`（如有） | `verdicts_US.jsonl` | 只可降級；價格照抄 |
| S6 閘門 | `check_verdict.py` | 以上全部 | `L2_Check_Report.md`（V1–V17） | — |
| S7 排版 | `render_report.py` | `L2_Input.csv` + `verdicts_US.jsonl` + `stories/*` | `reports/index.md`、`<T>_投資快報.md`、`<T>_image_pack.md` | 只排版，不判斷 |
| S7b 上傳 | Hermes | `<T>_投資快報.md` | Google Drive `US_Swing/YYYY-MM-DD/`，回填 `full_report_url` | 只上傳，不改內容 |
| S8 圖卡 | **用戶人手（ChatGPT）** | `<T>_image_pack.md`（完整 prompt） | `reports/<T>_card.png` → 同一個 Drive 資料夾 | 不可改數字 |
| S9 發送 | Hermes bot | index + ✅ 快報（+ 已有圖卡） | Telegram / 檔案 | S6 有 FAIL 就**不發** |

---

## 1. 每日時序（HKT）

```
05:30  S1-S2  ./run_daily.sh                     (美股收市後；exit 2 = 不准往下)
05:35  S3     ./run_l2.sh prep run_YYYYMMDD       (自動抓前一日)
05:45  S4     DeepSeek: story_handoffs.md → stories/*.json（每檔 ≤5 次搜尋）
06:15  S5     DeepSeek: L2_Input.csv + stories/* → verdicts_US.jsonl
06:20  S6     ./run_l2.sh check run_YYYYMMDD      (exit 2 = 不發)
06:25  S7     ./run_l2.sh render run_YYYYMMDD     (index + 快報 + image_pack)
06:30  S7b    Hermes: 上傳快報到 Drive，回填 full_report_url（失敗留空，不阻擋）
之後         用戶：image_pack 貼到 ChatGPT → 核對價格 → 存 PNG → 上傳同一個 Drive 資料夾
06:35  S9     Hermes 發 index + ✅ 快報（有圖卡才附）
```

**停止條件**（任何一個成立 → L2 只輸出一行 NO_TRADE，不寫分析）：
- `l2_status.json` 的 `status = RUN_FAILED`（invariant FAIL 或引擎失敗）
- `status = DATA_STALE`（Contract 日期 ≠ 最近交易日；設 `SWING_EXPECTED_DATE` 時才檢）

---

## 2. 檔案契約

| 檔案 | 產生者 | 主要欄位 / 內容 |
|---|---|---|
| `Contract_US.csv` | L1 | **113 欄**（`us-contract-1f.6`），定義見 `DATA_DICTIONARY.md` |
| `L2_Input.csv` | l2_prep | Contract + `Baseline_Verdict`、`Baseline_Why`、`Setup_Quality`、`Setup_Quality_Grade`、`Setup_Quality_Detail`、`Speak_Up`、`Change_vs_Prev`、`Story_Needed` |
| `story_handoffs.md` | l2_prep | 每檔一個 `STORY HANDOFF v5` 區塊（§5.1） |
| `reports/index.md` | render_report | 每日交易簿（① 概況 ② 變化 ③ STALK ④ 觀察 ⑤ 持倉 ⑥ 報告連結） |
| `reports/<T>_投資快報.md` / `<T>_image_pack.md` | render_report | 每檔快報 / 給 GPT Image 2 的原文 |
| `stories/<T>_story.json` | S4 | 敘事（market_line / why_now / moat / numbers / risks / conviction / sources） |
| `stories/<T>_search_log.json` | S4 | 審計：每條查詢與命中 URL／日期 |
| `reports/<T>_card.png` | S8（Hermes→GPT Image 2） | 圖卡，數字只可來自 image_pack |
| `l2_status.json` | l2_prep | `status`、`reason`、`as_of`、各 verdict 數量 |
| `verdicts_US.jsonl` | L2 | 每檔一行 JSON（§6.2） |
| `TradeBook_YYYYMMDD.md` | L2 | 給你看的交易簿（§6.3） |
| `positions.csv` | 你（選用） | `ticker,entry_date,entry_price,stop,shares` |
| `L2_Check_Report.md` | check_verdict | V1–V17 結果 |

**讀 CSV 一律用 `keep_default_na=False`**（否則 `NOT_APPL`、`NONE` 以外的狀態字串仍有機會被讀成 NaN）。

---

## 3. 基準 verdict 與品質分（L1 側，`l2_prep.py` 計算）

### 3.1 Baseline_Verdict（規則，不交給 LLM）

| Candidate_Class | Entry_Feasible | 基準 | 條件 / 備註 |
|---|---|---|---|
| 任何 | INVALIDATED / MISSED | **AVOID** | |
| A_SETUP | AT_TRIGGER / NEXT_DAY | **BUY** | `Volume_Confirm=LOW`（REMARK 模式）→ STALK |
| A_SETUP | LATE | BUY 或 WATCH | BUY 需 `Risk_ADR_Plan≤1.0` 且 `Room_To_Supply_R≥2` |
| A_SETUP | AT_MARKET（PULLBACK） | **BUY** | |
| A_SETUP | AT_MARKET（REVERSAL） | BUY 或 STALK | BUY 需 `Leader_OK≠FAIL` 且 `Room≥2R` |
| C_WATCH | NOT_YET | **STALK** | 掛 buy-stop |
| C_WATCH | 其他 | WATCH | |
| B_LEADER_WAIT | — | WATCH | |
| X_NONE | — | AVOID | |

覆蓋（按序）：BUY 而財報 `PASS` → AVOID；`UNKNOWN` → STALK；`Risk_OK≠PASS` → WATCH。
（選用）`SWING_INDEX_20EMA_RULE=1`：`Index_Below_20EMA=True` 時 BREAKOUT 的 BUY → STALK。**預設關閉**（regime 只作表頭，2026-11-05 決定）。

### 3.2 Setup_Quality（0–5，只作顯示與排序，**永不改 class 或基準**）

| 家族 | 每項 +1 |
|---|---|
| BREAKOUT | `Base_Vol_Decay<0.7` · `Base_HigherLows_Pct≥0.6` · `Base_Cleanliness≥0.8` · `Base_Prior_Advance_Pct≥25` · `Base_Count_126≤2` |
| PULLBACK | 回調量 ≤0.8× · 深度 1–3 ATR · 支撐重疊 ≥2 · RS 線新高 · `Room≥2R` |
| REVERSAL | 跌幅 ≥35% · 升/跌量 ≥1.5 · 更高低點 ≥3% · 高於低點起算 AVWAP · `Room≥2R` |

分級：4–5 = **A+**，3 = **A**，≤2 = **B**；缺 3 項以上 = **NA**。
某欄不在 Contract → 顯示 `?項目`，不扣分也不加分。六個品質欄位自 `1f.2` 起已輸出，正常情況下不應再有 `NA`；
若出現 `NA`，代表該家族真的缺輸入，不是預期狀態。

### 3.3 Change_vs_Prev

`NEW` / `TRIGGERED` / `INVALIDATED` / `UPGRADED` / `DOWNGRADED` / `UNCHANGED`，對比昨日 `L2_Input.csv`。第一天全部視為 NEW 或 UNCHANGED。

### 3.4 Speak_Up（紅旗，計算好給 L2，L2 必須寫出來）

**單一來源：`l2_prep.py::speak_up()`。** playbook 不再自帶門檻（見 §7 的說明），只引用這支函式。

目前會觸發的條件：RSI>75 · 高於 MA20 超過 10%（15% 是 Risk 閘門，10–15% 是「要出聲」的區間）·
突破量 LOW · **空間 <1.5R** · 軟阻力 <1R · `Leader_OK=FAIL` · 財報 CAUTION（縮短持有）·
財報 UNKNOWN（story-search 必須找日期）。

---

## 4. Story 銜接規則（S4）

1. **只搜 `Story_Needed=True`**（基準 BUY / STALK）。WATCH 名單你要時手動觸發。
2. 每檔最多 5 次搜尋；財報 PASS 不會出現（基準已是 AVOID）。
3. Story Search 只輸出 `CONVICTION`，**不改 verdict**。降級由 L2 按 §6.1 規則做。
4. 財報 `UNKNOWN`：story-search 必須搜尋財報日期，附公司 IR 或交易所公告網址；寫入敘事報告的 `Earnings 窗`。**同日不會因此升級**，L1 次日確認日期後才會變回 BUY。
5. 故事搜尋的規則見 `story_search/SKILL.md`（規則目錄下）（**v3.2，由 Grok v3.1 原始檔改寫**；
   `references/` 為原始 kb-routes / output-template / quality-checklist，已加 v3.2／v5.5.2 註記）。

---

## 5. Story handoff 格式

### 5.1 `STORY HANDOFF v5`（由 `l2_prep.py` 生成，人不要改）

```
STORY HANDOFF v5
TICKER: AAA
MARKET: US
HANDOFF DATE: 2026-11-05
VERDICT: BUY
SETUP: BREAKOUT/A_BASE WIDE · state TRIGGERED · AT_TRIGGER
ENTRY: 100.50 (trigger close)
STOP: 97.20 (TRIGGER_LOW)
SUPPLY ABOVE: NONE_ABOVE (blue sky)
TARGET: NONE (v5 has no target; never invent one)
EARNINGS: CLEAR · 2026-12-10 · 24 sessions
RS (vs SPY): 22.1
BASE VOLUME DRY-UP: 0.60 (low = good)
BREAKOUT VOLUME: PASS (2.10x 20d avg)
QUALITY: A+ (5/5) +volume dried up | +higher lows | ...
TECHNICAL CONCERN: RSI 77
```

STALK（未突破）的 STOP 會寫成：`breakout-day low (set at fill); skip if that low < <BuyStop_Max_Stop>; base low <x>`。

### 5.2 舊 handoff 欄位對照（給 story-search）

| 舊（v4.4 GEMINI HANDOFF） | v5 |
|---|---|
| VERDICT | VERDICT（= Baseline_Verdict） |
| ENTRY ZONE | ENTRY（單一價格，不是區間） |
| ADJUSTED STOP | STOP |
| PRIMARY TARGET | **刪除** → 改讀 SUPPLY ABOVE |
| CLAUDE CONVICTION | QUALITY |
| Vol_Expansion | 拆成 BASE VOLUME DRY-UP（低=好）與 BREAKOUT VOLUME（LOW=風險） |
| EARNINGS ≤14 / ≤7 | EARNINGS 的 flag（CLEAR / CAUTION / PASS / UNKNOWN），**不要自己數天** |

---

## 6. L2 交易簿（S5）

### 6.1 L2 可以做與不可以做

**只有 L2 做得到的三件事**：
1. **取捨**：多檔 BUY 時，按 Grade → Room → RS 排序，最多 **3** 個 BUY（`SWING_MAX_BUYS`），其餘降為 STALK 並寫明「名額」。
2. **整合故事與矛盾證據**：把 Speak_Up、敘事 CONVICTION、產業重疊寫成判斷。
3. **持倉管理**（有 `positions.csv` 時）：止損更新、財報倒數、失效警號。

**降級規則（只有這幾種）**

| 原因代碼 | 允許 | 要求 |
|---|---|---|
| 欄位原因 | 任何降級 | `downgrade_reason` 必須寫出 Contract 欄位名與數值，例：`RSI_14=78 on trigger day` |
| `STORY_RISK` | **只限 BUY → STALK** | `conviction=CHALLENGE`，原因含**日期（YYYY-MM-DD）+ 網址**，且為硬事件（FDA / AdCom、增發、併購、訴訟判決、指引下修） |
| `SLOT` | BUY → STALK | 超出每日 BUY 名額 |
| 產業集中 | 不降級 | 同產業 ≥2 個 BUY 只寫提示並排先後 |

**禁止**：任何升級；改 entry / stop / trigger；發明 target；計算倉位或帳戶風險 %（倉位 = 你的每筆風險 × `Shares_per_1000_Risk` ÷ 1000，自行計算）。

**NO_TRADE**（整份只有一行）：`NO_SETUP`（無 BUY/STALK）· `ALL_DOWNGRADED` · `RUN_FAILED` · `DATA_STALE`。

### 6.2 `verdicts_US.jsonl`（機器檢查用，每檔一行）

必須包含所有基準 BUY / STALK；WATCH 可選。

```json
{"ticker":"AAA","verdict":"BUY","baseline":"BUY","entry":100.50,"stop":97.20,
 "grade":"A+","rank":1,"conviction":"CONFIRM","downgrade_reason":"",
 "cited_fields":["Volume_Confirm","Trigger_Vol_Ratio","RSI_14"],
 "story_tag":"Catalyst","narrative":"一句話"}
```

- STALK（未突破）的 `entry` = `Trigger_Price`；其他 = `Entry_Ref`。`stop` = `Invalidate_Below`。
- `conviction` 只能是 `CONFIRM` / `CHALLENGE` / `NEUTRAL`（V11 會拒收其他值）；沒有跑 story 的寫 `NEUTRAL`。
- 文字欄位（§10.1）寫在同一行；`risks` **只准寫故事與基本面**，技術風險由 renderer 從 `Speak_Up` 印出（V9）。
- `cited_fields` 只能用 `L2_Input.csv` 的欄位名。

### 6.3 交易簿 → 已併入 `reports/index.md`（v5.5.1）

原本的 `TradeBook_YYYYMMDD.md` 不再產生：它與 §10 的每日首頁重複。現在 **`reports/index.md`
就是每日交易簿**，由 `render_report.py` 從 `L2_Input.csv` 排版（① 概況 ② 今日變化 ③ STALK 掛單
④ 觀察 ⑤ 持倉 ⑥ 個股報告連結），價格全部由程式填。以下小節僅保留作格式參考。

```
═══ US SWING 交易簿 · <as_of> ═══
市場表頭：Regime <Label/State>（只作參考）· 指數 <Index_Regime_State> · 市寬 <% >50D>

① 今日變化
   TRIGGERED: … · NEW: … · INVALIDATED: … · UPGRADED / DOWNGRADED: …

② 行動計劃
   BUY（最多 3）── 每檔：
     TICKER · Setup 一句（如「WIDE base 14 日突破，突破量 2.1×」）· Grade A+
     入場 <entry>（<Entry_Src>）· 止損 <stop>（<Stop_Type_Plan>）· 風險 <Risk_Pct_Plan>% = <Risk_ADR_Plan>×ADR
     上方 <Supply_Level/藍天>（<Room>R）· 財報 <flag/date>
     故事：<主敘事一句> · CONVICTION <…> · 一句講晒「…」
     要小心：<Speak_Up 每一條>
     管理：突破日低失守即走；收市跌穿 MA10 減半；+2R 後止損移至成本
     ☐ 人工看圖（形態鬆散 / 跳空缺口 L1 看不到）
   STALK（明日掛單）── 表格：TICKER · buy-stop <Trigger_Price> · 最少成交量 <Trigger_Min_Vol> · 成交日低需 > <BuyStop_Max_Stop> · Grade · 故事一句

③ 觀察名單（WATCH / C_WATCH / B_LEADER_WAIT）── 每檔只寫「缺甚麼」（取自 Risk_Why / Setup_Why）

④ 持倉（有 positions.csv 才寫）
   TICKER · 成本 · 現價 · R 倍數 · 止損建議 · 財報倒數 · 警號（跌穿 MA10/MA20、突破失敗）

⑤ 故事附錄 ── 每檔敘事報告精簡版 + 來源（標題 · 網址 · 日期）

⑥ 週報（逢星期五）── forward_log 摘要（如有開啟）+ 本週教訓

不構成投資建議
```

**格式規則**：交易簿每個價格必須等於 `verdicts_US.jsonl` 的同一個數字；交易簿由 JSON 的內容展開，不另行計算。

---

## 7. L2 不變量（`check_verdict.py`）

| ID | 規則 |
|---|---|
| V1 | `verdict` ≤ `Baseline_Verdict`（不准升級） |
| V2 | `entry` / `stop` 與 Contract 相差 ≤0.01 |
| V3 | `cited_fields` 非空，且全部存在於 `L2_Input.csv` |
| V4 | BUY 必須 `Risk_OK=PASS`、財報不是 PASS/UNKNOWN、`Entry_Feasible` 不是 NOT_YET/INVALIDATED/MISSED |
| V4c | 任何 BUY/STALK 必須 `Tradeable=PASS`（風險 ×ADR、風險 %、空間三項 cap，用計劃止損計） |
| V5 | 每檔一行；BUY ≤ 3；NO_TRADE 獨立一行且原因代碼合法 |
| V6 | 欄位原因的降級必須寫出 Contract 欄位名 |
| V7 | `STORY_RISK` 只可 BUY→STALK，需 CHALLENGE + 日期 + 網址 |
| V8 | 基準 BUY / STALK 全部出現在輸出（不准默默漏掉） |

| V1b | baseline 由 `check_verdict` 用 `l2_prep.compute_baseline()` 重算，與 `L2_Input.csv` 不符即 FAIL |
| V1c | `l2_status.json` 記錄的 `Contract_US.csv` / `L2_Input.csv` sha256 必須與實際檔相符 |
| V4c | `STALK` 只准在 `Risk_OK ∈ {PENDING, PASS}` 時出現 |
| V6 | 降級必須引用 `l2_prep` 預算的規則碼（`Downgrade_Codes`），自由文字不接受 |
| V9 | 文字欄位：長度、情緒標籤、禁用詞（目標價/T1/T2/T3/RR）、`risks` 不得含技術欄位；**`closer` / `invalidation` 出現的價格必須存在於該檔的 Contract** |
| V10 | `l2_status.json` 不是 OK 時，唯一合法輸出是單行 `NO_TRADE` 且原因相符 |
| V11 | `conviction` 只能是 CONFIRM / CHALLENGE / NEUTRAL；且與 `story.json` 一致（V11b） |
| V12 | `sources[].url` 必須出現在同檔 `search_log.json` 的 hits |
| V13 | `numbers[]` 每項有 `url` + `date`，且 URL 在 search log 內 |
| V14 | BUY/STALK 且 CONFIRM/CHALLENGE → `sources` ≥2，`conviction_why` 引用其中一條（域名或 URL） |
| V15 | 文字不得含簡體字 |
| V16 | Earnings UNKNOWN → `earnings_check` 有日期+URL 或「未能確認」 |
| I30 | `Trigger_US.csv` 每一張票都必須 `Tradeable=PASS`（2026-11-07 風險閘門） |
| V17 | `story_main`≤200、`why_now`≤60、`story_sub`≤120、`invalidation`≤100、**`closer`≤50**（空格與標點不計，ticker／數字每字元計 1）、`risks`≤4 |

任何 FAIL → Hermes **不發交易簿**，改發 `L2_Check_Report.md`，你決定是否重跑 L2。
`render_report.py` 不再驗證、也不再 exit 2；它只負責排版，閘門只有 `check_verdict.py` 一個。

---

## 8. 開放決定（目前預設）

| 項目 | 預設 | 改法 |
|---|---|---|
| 指數跌穿 20EMA 時突破 BUY→STALK | **關** | `SWING_INDEX_20EMA_RULE=1`（需 L1 先輸出 `Index_Below_20EMA`） |
| 每日 BUY 上限 | 3 | `SWING_MAX_BUYS` |
| 持倉管理 | 無 `positions.csv` 時略過 ④ | 建立檔案即啟用 |
| forward_log | 關 | `SWING_FORWARD_LOG=1` |
| 弱 BUY 降級 | 關 | `SWING_WEAK_BUY_RULE=1`（B/NA 質素 + 空間<1.5R + 非領導 → 基準 BUY 改 STALK） |
| 交付方式 | Markdown 檔 | Hermes 發 `index.md` + index 中 ✅ 的每檔快報（圖卡有人手做才附） |
| 快報存檔 | 本機 | Hermes 上傳到 Google Drive `US_Swing/YYYY-MM-DD/`，權限「受限制（只限本人）」，回填 `full_report_url`；失敗留空、不阻擋 |
| 圖卡生成 | 人手 | 把 `<T>_image_pack.md` 貼到 ChatGPT → 核對價格 → 存 PNG → 上傳同一個 Drive 資料夾（可之後補傳） |

---

## 9. 版本與變更

- v5.5（本文件）：新增 `l2_prep.py`、`check_verdict.py`、STORY HANDOFF v5、交易簿格式、V1–V8。取代 `US_SWING_SETUP_PROMPT_v53.md` §1–§2 的 verdict 對照（改由程式計算）；其 §3–§6 欄位說明與 v5.4 Speak-up 表仍然有效。
- v5.5.2：S4 改由 DeepSeek 執行、`stories/*` 兩份 JSON、V12–V17、S8 改人手（ChatGPT）、S7b Drive 上傳、`closer`≤50、`SWING_WEAK_BUY_RULE`、
  contract `1f.3`（補 `MA10/MA20/MA50/SMA50_Slope/VAL_60D` 給支撐梯級）。
- 待 v5.6：L1 輸出 `Index_Below_20EMA`、`Sector`；財報第二資料源。（六個品質欄位已於 `1f.2` 完成。）

---

## 10. 最後一哩：投資快報 + GPT Image 包（S7，`render_report.py`）

**原則：L2 只寫文字，數字全部由程式從 `L2_Input.csv` 填入。** 所以快報與圖像包的價格不可能和 Contract 不一致。

### 10.1 文字放在哪兩份檔（v5.5.2 起分開）

| 檔案 | 欄位 | 誰寫 |
|---|---|---|
| `stories/<T>_story.json` | `market_line`、`story_main(+score)`、`why_now`、`moat`、`numbers`、`story_sub(+score)`、`risks`、`conviction(+_why)`、`story_tag`、`hard_event`、`earnings_check`、`sources`、`traps` | S4（DeepSeek 搜尋） |
| `verdicts_US.jsonl` | `ticker`、`verdict`、`baseline`、`entry`、`stop`、`grade`、`rank`、`conviction`、`downgrade_reason`、`cited_fields`、`closer`、`emotion`、`invalidation`、`industry`、`title`、`finance_line`、`driver_line` | S5（DeepSeek 決策） |

`conviction` 在兩份檔必須一致（V11b）。`risks` 只寫故事／基本面；技術風險由 renderer 從
`Speak_Up` 印出（V9 會擋在 risks 重述技術欄位或 Contract 價格）。

**文字內禁用**：自己發明的目標價、`T1/T2/T3`、`RR`（T1–T15 作為 KB 趨勢代號可以用）。
**可以引用**賣方數字，但要寫出處：`分析師／共識／券商／賣方` 開頭的目標價屬證據（A5）；
沒有出處的「目標價 70」一律 FAIL。驗證在 `check_verdict.py`（V9、V12–V17），不在 renderer。

### 10.2 由程式填入的部分

現價、質素/星級、RS、Setup（中文名 + base 家族/長度/寬度）、三閘、風險 %/×ADR、上方阻力/藍天、量能（突破量 + 底部量縮）、Ext/RSI、財報、今日變化、進場（STALK 自動寫 buy-stop、最低成交量、`BuyStop_Max_Stop`）、止損、每 $1,000 風險股數、管理規則、免責聲明。

### 10.3 舊快報欄位 → v5

| 舊 | v5 |
|---|---|
| Priority / Score | 質素 A+/A/B（0–5） |
| Setup / Playbook（Low_Vol_Grind、Zone、Freshness Gate） | Setup_Family/Code + Base_State |
| RR 主計劃 L1/L2/L3、最佳 RR | 刪除 → 風險 ×ADR + 上方阻力 R 倍數 |
| 目標 T1/T2/T3 | 刪除 → 上方阻力 / 藍天 |
| Vol_Expansion | 突破量（LOW = 風險）+ 底部量縮（低 = 好） |
| ATR_FALLBACK / TZ stop | Stop_Type_Plan（TRIGGER_LOW / PB_STRUCT / MA_STRUCT / SR_STRUCT / VP_STRUCT） |

### 10.4 Hermes 執行次序

```
./run_l2.sh check  run_X   → exit 0 才繼續（唯一的閘門；V9 已驗文字欄位）
./run_l2.sh render run_X   → reports/<T>_投資快報.md + <T>_image_pack.md + index.md
Hermes：發 index.md（每日交易簿）＋ index.md 中 ✅ 的每檔快報
        image_pack 原文**不改**交 GPT Image 2
        ❌ 的檔不發，只在 index 顯示原因
```

`render_report.py` 只排版、不判斷、也不會 exit 2；任何「不要發」的決定都來自 `check_verdict.py`。
`run_l2.sh prep` 會自動抓最近一個有 `L2_Input.csv` 的早於本次的 `run_*` 作為前一日，
找不到就全部標 `BASELINE` 並印出警告——不需要 Hermes 記住資料夾。
