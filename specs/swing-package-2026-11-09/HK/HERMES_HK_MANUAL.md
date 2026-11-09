# Hermes 港股安裝手冊

## 0. 一句話

**這是一個獨立安裝。你現有的美股安裝不會被改動一個 byte。**

| | 美股（你已有） | 港股（本包） |
|---|---|---|
| 目錄 | `/opt/us-swing`（或你現用） | `/opt/hk-swing` |
| 清單 | `tickers.txt` | `tickers_hk.txt` |
| 輸出 | `runs/run_<日期>/` | `runs/hk/run_<日期>/` |
| 指令 | `./run_daily.sh` | `./run_daily.sh`（已內建 `SWING_MARKET=hk`） |
| 時間 | 05:30 HKT | **17:30 HKT 之後** |

## 1. 安裝

```bash
cd hk_package
./INSTALL_HK.sh /opt/hk-swing
```

安裝器會拒絕裝進一個「有 `tickers.txt`、冇 `tickers_hk.txt`」的目錄——那看起來是美股安裝。

## 2. 每日流程（同美股一樣的形狀）

```bash
cd /opt/hk-swing
./run_daily.sh                       # S1–S2 → runs/hk/run_<日期>/
./run_l2.sh prep  runs/hk/run_<日期>
#   S4/S5 由 LLM 交回 stories/ 與 verdicts_US.jsonl
./run_l2.sh check runs/hk/run_<日期>   # exit 2 = 不發
./run_l2.sh render runs/hk/run_<日期>
```

## 3. 財報日：**用你的 TradingView，不要用 Yahoo**

Yahoo 對港股只有 74% 有日期（39 隻裡 10 隻 UNKNOWN）。你 Hermes 有 TV schedule，所以：

1. 掃描前，對 `tickers_hk.txt` 每隻叫 `get_symbol_data_batch`
2. 取 `earnings_release_next_date`（epoch → HKT → 日期）
3. 整份重寫 `earnings_overrides.csv`
4. 再跑 `./run_daily.sh`

**唔好用 `get_earnings_calendar`**（HKEX 回 0 條）；**唔好用 `days_to_earnings`**（港股一律 null）；
**時間 20:00 是佔位值**，只有日期可信。詳見 `TV_EARNINGS_SPEC.md`。

## 4. 三個唔好（防混亂）

1. **唔好**把本包的 `us_swing_v55.py` / `base_layer.py` 等複製到美股安裝——版本會分岔，
   之後兩邊要分別 patch。
2. **唔好**把 `tickers_hk.txt` 改名做 `tickers.txt` 放進港股安裝——`run_daily.sh` 已固定讀 `tickers_hk.txt`。
3. **唔好**兩個安裝共用 `runs/`。

## 5. 驗證

```bash
cd /opt/hk-swing && ./verify_hk.sh
```

預期：`ALL CHECKS PASSED`。

## 6. 出錯時

| 症狀 | 處理 |
|---|---|
| `no tickers in tickers_hk.txt` | 清單空白或全被 `#` 註釋 |
| Contract 只有幾隻 | 部分代號 Yahoo 無資料（例如已私有化的 `0011`）；看 `Data_Quality_Report.csv` |
| 全部 UNKNOWN 財報 | `earnings_overrides.csv` 未寫或日期已過（過期會被忽略） |
| 報告寫 `$` 而非 `HK$` | 跑錯安裝（應該用 HK 目錄） |
