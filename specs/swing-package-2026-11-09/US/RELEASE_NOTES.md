# v5.5.3 / v5.5.2 相對 v5.2 的變化（給 Hermes 看「為甚麼要升級」）

> **v5.5.3（2026-11-06）**：修復首日實跑發現的 12 個缺陷（A1–A12），詳見 `BUGFIX_2026-11-06.md`。
> 契約仍是 `1f.3` / 107 欄，**不需要重跑歷史資料**。升級只需覆蓋 `02_CODE/*.py` 與 `01_RULES/*.md`。

## 一句話

舊版把「判斷」藏在掃描器裡（zone、RR、target），而且數字有幾個會騙人。
新版把判斷全部拿掉，只交事實；判斷交給 L2，**而且 L2 可被機器檢查**。

## 掃描器（L1）

| 舊 | 新 | 為甚麼 |
|---|---|---|
| Tight Zone 判定 | 刪除 | 2451 個 active bar，0 次 `Close < zone low` —— 從來沒觸發過 |
| `RR_Ratio_*` | 刪除 | `RR_T3 = (Res20 + 3ATR − Close)/Risk`，而 `Res20 ≥ Close` ⇒ 永遠 ≥ 3×ATR/Risk。它量的是 1/風險，不是報酬 |
| 目標價 T1/T2/T3 | 刪除 | 沒有 RR 就沒有目標，留著只會誤導 |
| 突破只看收盤 | 加 `BO_FAILED` | 45.9% / 50.0% 的已觸發 base 最後跌破突破日低，舊版仍顯示 TRIGGERED |
| 供給從現價量 | 從**進場價**量 | 舊版偶爾出現「供給在進場價之下」 |
| 一家 base | 兩家（STRICT 5–30 / WIDE 10–40） | 覆蓋率 12.5% / 23.6% |
| S/R flip = 突破當日 | = 回測（15 日內） | 舊版 setup H 幾乎不出現 |
| `NA` 字串 | `NOT_APPL` | pandas 會把 `NA` 讀成缺失值 |
| 盈利按日曆日 | 按 NYSE session | 假期會算錯 |

## 兩段架構

| 層 | 誰 | 能不能改 verdict |
|---|---|---|
| L1 | 掃描器 | 不輸出 verdict |
| S4 | DeepSeek 搜尋 | 不改，只標 CONFIRM/CHALLENGE/NEUTRAL |
| L2 | DeepSeek 決策 | 只可降級 |
| S6 | `check_verdict.py` | 機器否決 |

## 新增的檔案

`stories/<T>_story.json`、`_search_log.json`、`reports/index.md`、
`reports/<T>_投資快報.md`、`reports/<T>_image_pack.md`。

`TradeBook_YYYYMMDD.md` 取消，功能併入 `reports/index.md`。

## 契約版本

`us-contract-1f.3`，**107 欄**。若你的程式有寫死欄位數或欄位名，請一併更新。
