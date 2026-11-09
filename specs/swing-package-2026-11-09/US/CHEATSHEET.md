# 一頁 cheat sheet（貼在 cron 旁邊）

```
每天（HKT 05:30，週二至週六）
────────────────────────────────────────────
cd /opt/us-swing && ./run_daily.sh                 # exit 2 → 停（輸出到 runs/）
./run_l2.sh prep runs/run_$(date +%Y%m%d)               # 自動抓前一日
#   ← DeepSeek 交回 stories/ 與 verdicts_US.jsonl
./run_l2.sh check runs/run_$(date +%Y%m%d)              # exit 2 → 只發 L2_Check_Report，停
./run_l2.sh render runs/run_$(date +%Y%m%d)             # index + 快報 + image_pack
#   上傳 <T>_投資快報.md → Drive US_Swing/<交易日>/
#   發 index.md + index 中 ✅ 的檔
```

## 判斷表

| 看到 | 做 |
|---|---|
| `run_daily.sh` exit 0 | 繼續 |
| `run_daily.sh` exit 2 | 停；讀 `Invariant_Report.md` |
| `l2_status.json` ≠ OK | 只發一行 NO_TRADE |
| `check` exit 0 | 可以發 |
| `check` exit 2 | 只發 `L2_Check_Report.md`；不發交易簿 |
| 沒有 `verdicts_US.jsonl` | 同上（L2 未跑完） |

## 三個路徑

```
事實      runs/run_<日期>/Contract_US.csv
每日頁面  runs/run_<日期>/reports/index.md
每檔快報  runs/run_<日期>/reports/<T>_投資快報.md
```

## 三條紅線

1. 不改價格、不改 verdict
2. `check` FAIL 一律不發
3. 不用過期資料
