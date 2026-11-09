---
name: story-search
description: Turn a completed STORY HANDOFF v5 into a Traditional Chinese investment narrative with live search, and write two JSON files the renderer reads. Use when the run folder has story_handoffs.md with Story_Needed=True. Do not run on raw SwingAnalysis.csv. Never upgrade WATCH or AVOID to BUY.
metadata:
  type: workflow
  version: "3.2"
  upstream: l2_prep.py (STORY HANDOFF v5)
  downstream: verdicts_US.jsonl -> check_verdict.py -> render_report.py
  project: us-swing-v5.5.2
---

# Story Search (v3.2)

美股投資敘事分析師。把已完成的技術 handoff 轉成可驗證、有催化劑的故事。規則只來自本 skill
同 `references/`。

Search 覆蓋一切時效事實。內置 KB 只用來路由主線，唔好用嚟報今日的數字。

## v3.2 相對 v3.1 改了甚麼

| # | 改動 | 原因 |
|---|---|---|
| 1 | 執行者由 Grok 改為 **DeepSeek**；上游 `l2_prep.py`，下游 `verdicts_US.jsonl` | S4 搬進本管線 |
| 2 | **每日 pipeline 一律寫兩份 JSON**（`stories/<T>_story.json`、`_search_log.json`）；用戶臨時問「幫我搜 X 的故事」仍可直接在對話回覆 | V12／V13 要機檢來源；快報由 renderer 排版 |
| 3 | **改正** `Vol_Expansion << 1 = 縮量風險`：底部量縮是好事，只有突破日 `Volume_Confirm=LOW` 才算風險 | 混用會把好事讀成壞事 |
| 4 | 刪除所有 `TARGET` 相關規則；`PRIMARY TARGET` 不存在 | v5 沒有目標價 |
| 5 | 一句講晒 ≤50 字（硬檢 ≤60） | 對齊 V17 但保留原本寫作紀律 |
| 6 | 每份報告最後一行固定 `CONVICTION: CONFIRM \| CHALLENGE \| NEUTRAL` | V11 機檢 |
| 7 | 財報天數直接讀 handoff，不自己數 | L1 用 NYSE session 算 |
| 8 | 路由不再靠 AGENTS.md，只看 `Story_Needed` 旗標 | 本管線沒有 HK 分支 |

## Load order (mandatory)

1. 讀 `story_handoffs.md` 的 `STORY HANDOFF v5` 區塊。至少要 TICKER + VERDICT；否則拒做。
2. 知道市場與行業後讀 `references/kb-routes.md`；需要背景時看 `KB/`（四份研究包，
   見 `KB/README.md` 的編號對照）。KB 只作路由與定性描述，數字一律以搜尋為準。
3. **先搜後寫**。永遠不要先寫故事再補 URL。
4. 寫入前讀 `references/output-template.md`。
5. 送出前靜靜跑 `references/quality-checklist.md`，再跑 `check_verdict.py`。

## When this runs

觸發：`story_handoffs.md` 內有 `Story_Needed=True` 的檔（基準 BUY / STALK）。

不觸發：`*_SwingAnalysis.csv`、`Contract_US.csv` 本身、regime 分數、大市簡報、估值。

## Hard constraints (do not drift)

- **不改** VERDICT、ENTRY、STOP、SUPPLY ABOVE。故事只可以影響 `conviction`。
- **沒有目標價**。v5 沒有 target；上方只有阻力（`SUPPLY ABOVE`）。禁用「目標價 / T1–T3 / RR」。
  （T1–T15 作為 KB 趨勢代號可以使用。）
- **量能有兩種意思，不可混用**：`BASE VOLUME DRY-UP` 低 = 賣壓衰竭 = **好**；
  `BREAKOUT VOLUME: LOW` = 突破未確認 = **風險**；`PENDING` / `NOT_APPL` = 不評論。
- **CHALLENGE 要有可查證據**。硬事件（FDA / AdCom / 增發 / 併購 / 判決 / 下調指引）必須附
  日期與 URL；軟性風險要寫明「軟性風險」。
- 沒有 URL → 該數字不可進 `numbers`。
- 缺欄位寫 `MISSING`，不要猜。
- 用戶貼的新聞／截圖 = `[USER]`，權重低於 `[SEARCH]`。
- KB 數字與 30 日內搜尋衝突 → 以搜尋為準，報告頭部標「已用最新數據覆蓋 KB」。
- 30 日以上舊聞 → `stale: true`，報告標 ⚠️。
- X／Twitter 只作情緒，不可單獨承載基本面數字。
- **每日 pipeline 寫檔案是交付的一部分**（v3.1 的「不要寫檔」不適用於每日流程）。
  用戶臨時手動要求一篇故事時，可以只在對話回覆，但唔會產生 `stories/*.json`。

## 輸出模式（同一份 skill，兩種執行環境）

| 模式 | 誰 | 交付 |
|---|---|---|
| **A 檔案**（預設） | DeepSeek / Hermes 環境（有檔案系統） | 寫 `stories/<T>_story.json`、`<T>_search_log.json` |
| **B 對話** | Grok 等只有聊天、不能寫檔的環境 | 兩個 ```json 區塊 + 最後一行 `CONVICTION: ...`，由操作者貼進 run 資料夾 |

模式 B 的格式（**區塊標題必須是 `search_log` 與 `story`**，方便人手複製成兩個檔）：

````
```json search_log
{"ticker":"UNH","searched_at":"...","queries":[...]}
```

```json story
{"ticker":"UNH", ... }
```

CONVICTION: CONFIRM
````

模式 B 不做的事：不寫檔、不跑 `check_verdict.py`（由 Hermes 端跑）、不改 verdict。
其餘硬規則（無目標價、來源要 URL、量能兩種意思、≤5 次搜尋）完全相同。

## Language

- 正文繁體中文；ticker、欄位名、setup code 保持英文。
- 一句講晒必須粵語、≤50 字、與 VERDICT 一致。
- 情緒標籤：BUY → 🚀／✅；WATCH、STALK → ⚡；AVOID → ❌／⚠️。永不 BUY + ❌。

## Terms (do not misuse)

| Term | Meaning | Not this |
|------|---------|----------|
| RS Score | Stock% − Benchmark% | Not RSI, not a percentile |
| RS +30.1 | Beat the benchmark by 30.1% | Not weakness |
| RS benchmark | Only the one in the handoff（v5 是 SPY） | Do not assume HSI / SPX |
| 入場區 | Ideal buy range | Not the stop |
| 止損價 | Hard exit | Not the entry |

`RS` 或缺就寫 `MISSING`，不要自己算。

## Earnings window (mandatory)

```
讀 handoff 的 EARNINGS flag 與天數（不要自己數交易日）。

CLEAR    → 無上限
CAUTION  → 只搜財報前的催化劑；不可把「持有過財報」當催化劑
PASS     → v5 基準已降為 AVOID，不會出現在 Story_Needed
UNKNOWN  → 必須多搜一次財報日期，寫入 earnings_check；找不到寫「未能確認」
```

## Pipeline

### STEP 1 — 市場 + 路由

```
US → KB B。醫藥／生科 → 加 KB D。標 核心受惠 / 邊緣受惠 / 無關。
不在表內 → 用最接近的 Trend，並在 market_line 寫「框架外推」。
```

`market_line` 寫「T號 + KB 名稱」；`route_tag` 寫受惠程度。寫進報告頭部。

### STEP 2 — Live search

先確認公司再做故事。預設 3 條一般 + 最多 2 條行業補充（≤5）。
Earnings UNKNOWN 可加第 6 條專門搜日期。連續兩條空結果 → 停，寫「敘事待查」。

```
Q1  [TICKER / company] + 路由關鍵字 + catalyst | 訂單 | 補貼 | 2026
Q2  [TICKER] + earnings | 分析師 | upgrade | downgrade
Q3  BUY/STALK/WATCH → institutional flow | ETF
    AVOID           → risk | 監管 | dilution | 下修
```

每條事實保留 標題 + URL + 日期，優先用 90 日內。全部寫進 `search_log.json`。

### STEP 3 — 三重檢查

1. Why Now — 甚麼變了？之前為何不成？窗口多長？
2. Moat — 七種護城河之一（網絡／規模／轉換成本／反向定位／稀缺資源／品牌／流程）。
3. Numbers — 收入／backlog／readout／deal 金額，帶日期。

「市場很大 / 政策支持」而無可驗證細節 → 強度 ≤5。

### STEP 4 — 衝突處理

| 情況 | 做法 |
|---|---|
| 故事好 + 技術 WATCH/AVOID | 保留故事，標「技術未配合」，不改 VERDICT |
| 故事差 + 技術 BUY | 降低敘事分，風險段必寫，conviction → CHALLENGE |
| 只中第一層 | ≤5，「故事尚早，等落地」 |
| 無搜尋結果 | 「敘事待查」，不要發明 |

### STEP 5 — 寫檔

- `stories/<T>_search_log.json`：每條查詢 + 命中（title/url/date）。
- `stories/<T>_story.json`：欄位見 `references/output-template.md`。
- 最後一行：`CONVICTION: CONFIRM | CHALLENGE | NEUTRAL`。

CONVICTION 定義：CONFIRM = 有日期有數字有來源的催化劑支持；CHALLENGE = 有新聞或風險打對台；
NEUTRAL = 兩邊都無硬催化劑。**必須引用搜尋結果，不可空泛。**

## Anti-hallucination

1. 具體日期／數字／事件而無 URL → 不可進 `numbers`。
2. 只有標題的搜尋結果 → 只可作標題級主張，不可推論金額。
3. 無「分析師普遍認為」，除非指名一間 + 連結。
4. 不可把 KB 框架句當今日新聞。
5. 模型記憶 vs 搜尋 → 搜尋為準；兩者皆無 → 待查。
6. 永不叫用戶違反 L1 的止損。

## 同步到 Story_Search_DB（S9 之後，選用）

`story_search_sync.py --rows run_X` 會由 `stories/*.json` + `verdicts_US.jsonl` + `L2_Input.csv`
直接砌出 30 欄的 row（CSV），不需要人手抄數字。

- `conviction` 只寫 **BUY / STALK / WATCH / AVOID**（與 sheet 既有 27 行一致）。
- `narrative_conviction` 寫 **CONFIRM / CHALLENGE / NEUTRAL**；舊行留空，不回填。
- `kb_note` 只放 KB 註記，不再放敘事判斷。
- 兩個欄位都有白名單檢查；寫入其他值會被清空並印 WARN，不會污染 sheet。
- 輸出以**欄名**對齊（header 隨資料一齊出），sheet 欄序改了也不會錯位。

`full_report_url` 由 Hermes 上傳 Drive 後回填；上傳失敗留空，不阻擋。
