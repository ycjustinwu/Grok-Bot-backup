# 財報日：由 TradingView 寫入 override（給 Hermes）

## 為甚麼要這樣做

Yahoo 對港股財報日覆蓋差：39 隻港股裡 **10 隻 UNKNOWN（26%）**，美股只有 3%。
`UNKNOWN` 一律不可 BUY，所以港股會偏保守。你用 TV 補日期最準，因為同你看圖一致。

## 用邊個 tool（實測）

| | 結果 |
|---|---|
| `get_earnings_calendar` | ❌ **HKEX 回 0 條**（窗口 2026-11-06 → 2027-05-05，700/9988/1548/388 全 0） |
| `get_symbol_data` / `get_symbol_data_batch` + `earnings_release_date` / `earnings_release_next_date` | ✅ 5/5 有值 |

兩個欄位都是 **Unix epoch**，要自己轉 HKT。

## 三個限制（照你嘅實測）

1. **`days_to_earnings` 對港股一律 null** — 唔可以照抄美股邏輯，自己用日期相減。
2. **時間永遠 20:00**（收市後佔位值）— **只有日期可信**，時間不要用。
3. **事件過後唔會即時更新**（388 在 11-06 出數，仍然寫「下次 = 今日」）—
   要用「日期已過 **且** `earnings_release_date` 有變」兩者一齊判斷，唔好單靠一個。

## 寫入格式

`/opt/hk-swing/earnings_overrides.csv`

```csv
Ticker,Date,Source
1071,2027-03-25,TradingView
0700,2026-11-18,TradingView
```

- `Date` 用 **HKT 日期** `YYYY-MM-DD`（由 epoch 轉 HKT 再取日期）
- `Ticker` 接受 `1071` / `1071.HK` / `01071` / `01071.HK`
- 掃描器**只在 Yahoo 回唔到日期時才用**，不會覆蓋已有日期
- 跑嗰陣會印 `📅 1071.HK 財報日由 override 提供：2027-03-25（TradingView）`

## 建議流程（Hermes）

```
1. 每日掃描前，對 tickers_hk.txt 的每一隻叫 get_symbol_data_batch
2. 取 earnings_release_next_date → 轉 HKT → 取日期
3. 若該日期 <= 今天（事件已過）→ 改用 earnings_release_date 的最新值；仍過期就唔寫
4. 覆寫 earnings_overrides.csv（整份重寫，唔要 append，避免舊日期殘留）
5. 然後才跑 ./run_daily.sh
```

> 第 3 步對應你講嘅「日期已過唔會即時更新」。
> 掃描器有一道保險：**override 日期早於 as-of 日就會被忽略**，該檔維持 `UNKNOWN`（不會變成 CLEAR）。
> 所以寫錯過期日期不會造假，但會令該檔白白停留在 UNKNOWN——所以要按第 3 步更新。
