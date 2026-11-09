# 風險閘門補丁 v5.5.4（給 Hermes）

來源：`us-swing-v553-risk-defects-2026-11-07`（B1–B5 + 44 隻審計）。
基準：v5.5.3 包。**只補風險閘門，不引入 HK 分支、不改任何門檻數值。**
契約：`us-contract-1f.5` → **`1f.6`**（+4 欄），113 欄。

---

## 一句話

以前 `Risk_OK=PENDING` 可以繞過風險帶，所以一張 **2.40×ADR** 的票照出。
現在建倉前就用**計劃止損**計風險，`Tradeable=FAIL` 一律冇票。

---

## 改了六個檔

| 檔案 | 改動 |
|---|---|
| `02_CODE/gates.py` | 新增 `tradeability()` + `Tradeable` / `Tradeable_Why` / `Room_At_Plan_Stop_R` / `Room_At_1_2ADR_R`；caps 入 CFG |
| `02_CODE/us_swing_v55.py` | 契約 1f.6；`generate_trigger` 只收 `Tradeable=PASS`；Priority 加風險負分 |
| `02_CODE/l2_prep.py` | `Tradeable=FAIL` → 一律 WATCH（任何 class） |
| `02_CODE/check_verdict.py` | 新增 **V4c**：BUY/STALK 必須 `Tradeable=PASS` |
| `02_CODE/invariants.py` | 新增 **I30**：`Trigger_US.csv` 每張票都要 `Tradeable=PASS` |
| `02_CODE/render_report.py` | WATCH/AVOID 不再印 entry / stop / 股數（B5） |
| `01_RULES/*` | PLAYBOOK 加風險閘門與 Tradeable 列；WORKFLOW 加 V4c / I30；字典補四欄 |

---

## 怎麼套用

```bash
cd /opt/us-swing
cp -r <本包>/02_CODE/*.py .            # 覆蓋六個檔（其餘不變）
cp -r <本包>/02_CODE/tests .           # 回歸測試
cp <本包>/01_RULES/*.md .              # 文件
chmod +x run_daily.sh run_l2.sh
```

> 唔需要重跑歷史資料；舊 run 仍可讀，只係新 run 才有 `Tradeable`。

## 怎麼驗（三步）

```bash
# 1) 自檢（會跑 26 項回歸測試，含 GME / DNA / CRL 三個 cap 案例）
./verify_install.sh
#    期望：ALL CHECKS PASSED

# 2) 真實重跑
./run_daily.sh
grep -c "" runs/run_<日期>/Trigger_US.csv          # 每張票都要 Tradeable=PASS

# 3) 閘門
./run_l2.sh check runs/run_<日期>                   # 期望 0 FAIL
```

## 預期結果（用 2026-11-06 同一批 44 隻）

| | v5.5.3 | v5.5.4 |
|---|---|---|
| 掛單 | 19 | **0** |
| `Risk_ADR > 1.2` 的票 | 16 | 0 |
| GME | STALK（買單 25.64） | **WATCH**，理由 `risk=2.40xADR > 1.2 (plan stop); risk=9.9% > 8%; room@plan stop=1.05R < 1.5` |

34 隻清單同日仍有 1 張：**RVTY**（0.84×ADR、3.9%、2.74R）。

---

## caps 是參數，不是寫死

```
SWING_RISK_ADR_CAP=1.2     # 風險 ×ADR 上限
SWING_RISK_PCT_CAP=8.0     # 風險 % 上限
```

審計建議值 = 1.2 / 8%。用這組，那一天 0 張票是**正確答案**（44 隻真的沒有合格票），
不是程式壞了。要放寬用環境變數，不要改程式。

| ADR cap | % cap | 那天票數 |
|---|---|---|
| 1.2 | 8% | 0 |
| 1.2 | 無 | 1（DNA） |
| 1.5 | 8% | 1（CRL） |

---

## 有一個判讀要修正

審計寫「19 張票、17 張 Risk_OK≠PASS」。實際上 `Trigger_US.csv` 當時連 **WATCH** 都收進去，
真正可執行的是 **6 張**（ECVT / GME / ERII / PRGO / CRL / DNA）。其餘 13 張本來就不該在檔案裡
—— 這條（報告 D）已一併修：現在只有 `Tradeable=PASS` 才入表。

---

## 未包含（要另外決定）

1. **REVERSAL 止損重寫**（報告 A）：5 隻的 stop 在 3–5×ADR。現在被 cap 擋死，所以不急；
   但要讓 REVERSAL 重新可交易，就要改 stop 錨點（POC → 反轉日低／MA20）。**這是換定義，不是修 bug。**
2. **B1 trigger 改錨到 Supply**：目前用「不發票」處理；改成掛在真阻力是策略選擇。

---

## 回滾

`cp` 覆蓋前先備份六個檔（`_backup_<時間>/`），回滾就是複製回去。沒有資料格式變更，
所以新舊 run 可以並存。
