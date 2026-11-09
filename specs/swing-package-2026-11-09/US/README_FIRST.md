# 這是甚麼

**美股 swing 掃描器 v5.5.4**。它不是選股機器，是一條「掃描 → 敘事 → 決策 → 驗證 → 排版 → 發送」的流水線。

```
L1 掃描器        交事實：三個閘門 + 委託單。永遠不講 BUY/SELL。
S4 故事搜尋      交敘事：有 URL、有日期。（由 DeepSeek 執行，不是 Hermes）
L2 決策          只能降級，不能升級；價格照抄。
S6 閘門          check_verdict.py 一個開關。FAIL = 一律不發。
S7 排版          render_report.py 把數字填進快報，L2 只寫文字。
```

## 你（Hermes）要做的四件事

1. **每天 05:30（HKT）**跑 `./run_daily.sh`
2. **等 DeepSeek 交回** `verdicts_US.jsonl`（L2 產物）
3. 跑 `./run_l2.sh check` → 只有 exit 0 才繼續 → `./run_l2.sh render`
4. **發** `reports/index.md` + index 中 ✅ 的每檔快報；把快報上傳到 Drive；**不要**自己生成圖卡

## 三條不可違反的規則

| 規則 | 為甚麼 |
|---|---|
| `check_verdict.py` 非 0 **一律不發** | 寧願當天沒有東西看，也不要發一個沒驗證過的價格 |
| 不可以改任何價格／verdict | 價格來自 L1，L2 只可以降級。改了就無法追查 |
| 不可以在掃描失敗時硬發舊資料 | `l2_status.json` 不是 OK 就只發 NO_TRADE |

## 先讀哪份

- **安裝／升級**：`HERMES_MANUAL.md` 第 2、3 節
- **每天怎麼跑**：第 4、5 節
- **發送規格**：第 7 節
- **出錯怎麼辦**：第 9 節

## 這個包裡有

```
01_RULES/    規則書（playbook、workflow、資料字典、story-search、KB）
02_CODE/     引擎與所有腳本
03_SAMPLE/   一份完整樣本 run（可直接跑驗證，不用上網）
verify_install.sh   安裝後跑這個
patch_from_v52.sh   從舊版升級用
```
