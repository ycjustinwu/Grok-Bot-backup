# 主張清單（Claim → 怎麼驗）— v5.4

文件裡每個數字都應該能被重算。這張表把「主張」對到「檔案 + 指令」。
若對不上，就是文件說謊——請直接指出。執行位置：`02_CODE`。

---

## A. 現行系統（v5.5.2）

| # | 主張 | 數值 | 怎麼驗 |
|---|---|---|---|
| A1 | Contract 欄位數 | **109**（US 34 隻）／**109**（HK 12 隻） | `python3 -c "import pandas as pd; print(pd.read_csv('run_v55/Contract_US.csv').shape)"` |
| A2 | 不變量全過 | **23 PASS / 0 FAIL** | `python3 invariants.py run_v55` |
| A3 | Playbook 引用的欄位都存在 | 33 個欄位、0 缺失（另加 l2 欄位檢查） | `python3 check_fields.py PLAYBOOK_v5.4.md runs/run_v55/Contract_US.csv`（在 app/ 內） |
| A4 | 引擎不輸出 verdict | `Screen_Flag` 只有 4 值 | `Summary_US.csv` 的 `Screen_Flag` |
| A5 | 分數各項相加等於 `Priority_Score` | 全部 | 不變量 I1 |
| A6 | 沒有可執行的舊機制 | grep 只剩註解 | `grep -rn "Tight_Zone\|RR_Zone" *.py` |
| A7 | 沒有狀態值會被 pandas 讀成缺失 | 18 欄乾淨 | 不變量 I29 |
| A8 | 突破前風險是 PENDING | — | `gates.py` 的 `pending` 分支 |

## B. Base 統計（v5.4，34 隻 × 500 根 = 16,849 bar）

| # | 主張 | 數值 | 怎麼驗 |
|---|---|---|---|
| B1 | BaseS episodes | **232** | `python3 stats.py run_v55` |
| B2 | BaseS 長度 p10/p50/p90 | **5 / 6 / 9** | 同上 |
| B3 | BaseS 覆蓋率 | **12.5%** | 同上 |
| B4 | BaseS 觸發率 / 突破失敗率 | **57.3% / 45.9%** | 同上 |
| B5 | BaseW episodes | **245** | 同上 |
| B6 | BaseW 長度 p10/p50/p90 | **10 / 12 / 18** | 同上 |
| B7 | BaseW 覆蓋率 | **23.6%** | 同上 |
| B8 | BaseW 觸發率 / 突破失敗率 | **57.1% / 50.0%** | 同上 |

**與 v5.2 的差異**：v5.2 的 B1–B8 是 159 / 6 / 9.7% / 54.7% 與 161 / 13 / 21.5% / 49.7%，
量在 376 根上；v5.4 用 500 根（`MONTHS=12`），且 F2b 改了 run 的結束條件。**不可直接相比**；
可比的只有同一份資料上的三規則對照：

| rule | BaseS | BaseW |
|---|---|---|
| v5.2 | 12.5% · 231 · p50 6d | 25.4% · 235 · p50 14d |
| v5.3 (F2) | 12.5% · 231 · p50 6d | 10.3% · 112 · p50 11d |
| **v5.4 (F2b)** | 12.5% · 231 · p50 6d | 23.6% · 245 · p50 12d |

驗證：`python3 experiments/f2_measure.py run_v55`（離線，內含三個變體）。

## C. 舊系統（v4.6）的失效證據

| # | 主張 | 數值 | 怎麼驗 |
|---|---|---|---|
| C1 | 總 bar 數 | 12,784 | `04_HISTORY/old_system_evidence.csv` |
| C2 | active zone bar | 2,451（19.2%） | 同上 |
| C3 | freshness 從未失敗 | 0 | 同上 |
| C4 | Mini_Breakout 在 active bar 上 | 0 / 37 | 同上 |
| C5 | Breakdown 在 active bar 上 | 0 / 169 | 同上 |
| C6 | ATR_FALLBACK 的 RR 下限 | 3.53 | `groupby('stop_type').rr_best.min()` |
| C7 | 8 隻 BUY 全部 RR ≥3.31 | 8/8 | `04_HISTORY/08_1a_before_after.csv` |

資料在 `../review_package_v52/04_HISTORY/`（v4.6 的量測快照，未變）。

## D. 不確定性

| # | 主張 | 數值 | 怎麼驗 |
|---|---|---|---|
| D1 | earnings 分佈 | CLEAR 22 / PASS 8 / UNKNOWN 4 | `Contract_US.csv` |
| D2 | UNKNOWN 不會變 PASS | 程式保證 | `gates.py::_verdict`（FAIL > UNKNOWN > PENDING > PASS） |
| D3 | 重播的盈利是假設值 | 強制 CLEAR | `replay.py` 輸出提示 |

## E. 未經真實資料檢驗的檢查（Claude 指出）

`I17`（A_SETUP 家族上限）、`I25`（TRIGGERED 不得跌破突破日低）、`I27`（低量不得 A_SETUP）
在本次 run 是「沒有對象可檢查」而通過：今天 0 個 TRIGGERED、0 個 REMARK、A_SETUP 只有 1 個
且是 PULLBACK。它們只在合成資料上測過，**在有突破日出現之前不能算已驗證**。

## 對不上時

1. 資料漂移（Yahoo 會修訂歷史；`03_RUN/run_v54` 是 2026-11-04 的快照）。
2. 日期：`2026-11-04` 是美股收市日。
3. 你比對的是哪一版：v5.2 的數字在 `../review_package_v52/`，不能與 v5.4 直接比。

三者都對得上、數字還不同，那就是文件錯了。
