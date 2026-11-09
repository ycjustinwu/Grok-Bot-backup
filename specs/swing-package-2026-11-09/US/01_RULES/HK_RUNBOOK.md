# 港股版 runbook（只講港股不同的地方）

US 的骨架完全照用，呢份只列**港股要特別處理**嘅幾點。

## 跑法

```bash
cd app
SWING_MARKET=hk ./code/run_daily.sh        # 讀 tickers_hk.txt → runs/hk/run_<日期>/
```

之後同美股一樣：

```bash
./code/run_l2.sh prep   runs/hk/run_20261106
#   S4/S5：對有票的檔做搜尋，寫 stories/<T>_story.json + verdicts_US.jsonl
./code/run_l2.sh check  runs/hk/run_20261106
./code/run_l2.sh render runs/hk/run_20261106
```

## 幾點同美股不同

| 項目 | 港股 | 為甚麼 |
|---|---|---|
| **跑的時間** | **17:30 HKT 之後**，不要 05:30 | Yahoo 的港股日線傍晚才齊；01:45 時只到 T-2（實測過） |
| **基準** | `2800.HK`（含息 ETF），不是 `^HSI` | 個股用調整價（含息），恒指是價格指數（除息）。混用等於給派息股免費優勢。16 隻股實測：RS 全部 −0.7 點、跨越門檻 0 隻 |
| **Regime** | Google Sheet 的「港股」區塊 | 市況 / %>50D / 10日比率，同一張表 |
| **代號** | `700` / `0700` / `0700.HK` 都收 | 引擎自動補零成 4 位 |
| **幣別** | 報告顯示 `HK$` | 由 `Market` 欄決定 |
| **每手股數** | **不處理** | `Shares_per_1000_Risk` 只是一個中性單位，落單前要自己按每手調整 |
| **流動性** | **不設閘門** | 你在 TradingView 先過濾；掃描器只在 Evidence 記錄成交額 |
| **印花稅** | 不計 | 系統不做 P&L |

## 已經處理的港股陷阱

| 陷阱 | 處理（v6.3） |
|---|---|
| **零成交 bar 被當成「完美壓縮」** | 壓縮判定要求 `Volume > 0`；零成交的 bar 不再計入 base |
| 停牌 | Yahoo 多數直接唔出嗰根，所以不會成 bar；零成交的情況由上面那條擋住 |
| 半日市（平安夜、除夕、農曆年前夕） | **未處理**。成交量大約一半、波幅亦窄，會被判成壓縮日。一年 3–4 次，影響有限，但要知道 |
| 除息令歷史重算 | 調整價會按新股息重算整條歷史，所以「凍結幾何」在除息日會小幅變動（比例不變，價位重算）。**這是預期行為**，不是 bug |

## 名單

`tickers_hk.txt`，一行一個。示範 40 隻流動性較好的；你自己加減。
下載失敗的檔會在 `Data_Quality_Report.csv` 見到，不會中斷整批。

## 港股 playbook 補充（兩句）

- `Leader_OK` 的 RS 是對 **2800.HK**，不是恒指本身。若你想用恒指，改 `markets.py` 一行。
- 港股沒有季度財報，`Earnings_Proximity_Flag = UNKNOWN` 會比美股多；
  `UNKNOWN` 一律不可 BUY（只能 STALK/WATCH），所以港股 A_SETUP 會偏少。這是刻意的保守。

## 只做故事、不做票（手動觸發）

`l2_prep` 只會對基準 BUY / STALK 設 `Story_Needed=True`。如果想對 **B_LEADER_WAIT / WATCH**
做故事搜尋（例如想知隻股值唔值得等），人手觸發即可：

1. 照跑 `./code/run_l2.sh prep runs/hk/<run>`
2. 對指定的檔做搜尋，寫 `stories/<T>_story.json` 與 `<T>_search_log.json`
3. 寫 `verdicts_US.jsonl`，verdict 用 **WATCH**（等於基準，不算升級）
4. `./code/run_l2.sh check` → `render`

V8 只要求基準 BUY/STALK 唔可以漏，所以只有 WATCH 的 run 一樣驗得過。

## 財報日：Yahoo 覆蓋不足，用 override 補

實測（39 隻港股 vs 34 隻美股）：

| | UNKNOWN 比例 |
|---|---|
| 港股 | **10 / 39 = 26%** |
| 美股 | 1 / 34 = 3% |

`UNKNOWN` 一律不可 BUY（只能 STALK/WATCH），所以港股會偏保守。補救方法：喺 `app/code/`
放一個 `earnings_overrides.csv`，你由 TradingView 抄個日期入去：

```csv
Ticker,Date,Source
1071,2027-03-25,TradingView
```

- 支援 `1071` / `1071.HK` / `01071` / `01071.HK` 四種寫法
- **只在 API 回唔到日期時才用**，不會覆蓋 Yahoo 已有的日期
- 執行時會印 `📅 1071.HK 財報日由 override 提供：2027-03-25（TradingView）`
- 只影響你列出的檔；其他檔完全照舊
