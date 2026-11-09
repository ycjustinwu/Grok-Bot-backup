# 港股版 — 獨立安裝包

**呢個包只裝港股。你現有嘅美股安裝（`us-swing/` 或類似）完全唔會被碰。**

```
/opt/hk-swing/     ← 呢個包裝喺呢度
/opt/us-swing/     ← 你原本嘅，唔會改
```

## 一句話

同一支引擎、同一套閘門、同一份 playbook，只換市場常數：
基準由 `SPY` 變 **`2800.HK`**、日曆由 NYSE 變 **XHKG**、regime 讀 Google Sheet 的港股區塊。

## 你要做三件事

```bash
# 1. 裝（會自己驗證，唔會碰 US）
./INSTALL_HK.sh /opt/hk-swing

# 2. 填清單
vi /opt/hk-swing/tickers_hk.txt

# 3. 跑
cd /opt/hk-swing && ./run_daily.sh
```

## 同美股唔同嘅三點（其餘一樣）

| | 美股 | 港股 |
|---|---|---|
| 跑的時間 | 05:30 HKT | **17:30 HKT 之後**（Yahoo 港股日線傍晚才齊） |
| 基準 | SPY | **2800.HK**（含息 ETF，不是 ^HSI） |
| 財報日 | Yahoo 夠用（3% UNKNOWN） | Yahoo **26% UNKNOWN** → 由你 Hermes 的 TradingView 寫入 `earnings_overrides.csv` |

## 唔好做

- 唔好把呢個包嘅 `us_swing_v55.py` 複製去 US 安裝（版本會分岔）
- 唔好把 `tickers_hk.txt` 改名做 `tickers.txt`（US 會讀錯）
- 唔好兩個安裝共用同一個 `runs/`

詳見 `HERMES_HK_MANUAL.md`。
