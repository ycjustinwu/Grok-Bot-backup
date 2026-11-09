# 修復 — 風險未成為掛單閘門（B1–B5，2026-11-07）

來源：Hermes 缺陷單 `us-swing-v553-risk-defects-2026-11-07` + 44 隻審計。
立場：**風險是門，不是分數**（Justin 2026-11-07）。

> 核對結果：5 條全部成立。但「19 張票」要修正一個讀法——`Trigger_US.csv` 當時連 WATCH
> 都收進去，真正可執行的是 **6 張**（ECVT / GME / ERII / PRGO / CRL / DNA），其餘 13 張本來
> 就不該在檔案裡。這條（D）本身也是 bug，已一併修。

---

## 改了甚麼

### 1. `Tradeable`：建倉前就判斷風險（B1 / B2 / B3 / B4）

L1 新增 `Tradeable`（PASS / FAIL）。判斷用**計劃止損**（突破前 = 平台低位），所以在觸發前
就有數字可判，`Risk_OK=PENDING` 不再是繞過風險 cap 的後門。

```
risk_adr > 1.2            → FAIL   （SWING_RISK_ADR_CAP）
risk_pct > 8.0%           → FAIL   （SWING_RISK_PCT_CAP）
room@plan stop < 家族門檻   → FAIL
room（1×ADR 或實際） < 門檻 → FAIL
非 pending 而 Risk_OK≠PASS → FAIL
```

三條規則各自獨立，訊息會串起來寫進 `Tradeable_Why`，例如 GME：

```
risk=2.40xADR > 1.2 (plan stop); risk=9.9% > 8%; room@plan stop=1.05R < 1.5
```

### 2. 掛單檔案只收可交易的（D）

`generate_trigger()` 以前只看 `Entry_Feasible`。現在多一條 `Tradeable=PASS`。
WATCH 的名字不會再出現在 `Trigger_US.csv`。

### 3. L2 與閘門同步（B2）

- `l2_prep.baseline_verdict`：`Tradeable != PASS` → 一律 WATCH（任何 class），
  原因寫進 `Baseline_Why`。
- `check_verdict` 新增 **V4c**：任何 BUY / STALK 必須 `Tradeable=PASS`。
- `invariants` 新增 **I30**：`Trigger_US.csv` 每一張票都要是 `Tradeable=PASS`。

### 4. 獎勵用可交易止損計（B4）

新增兩欄：`Room_At_Plan_Stop_R`（計劃止損）、`Room_At_1_2ADR_R`（1.2×ADR 止損）。
`Room_To_Supply_R` 保留作審計。GME：宣稱 2.52R，實際 **1.05R**。

### 5. Priority 加風險負分（審計 #4）

`Risk_ADR_Plan > 1.2` → −15、`> 1.0` → −5；`Room_At_Plan_Stop_R < 1R` → −10。
只減不加，所以「高分」不再等於「闊止損」。

### 6. WATCH / AVOID 不再印價位（B5）

`render_report` 對非行動 verdict 只寫「暫不掛單 / 要等 / 原因」，不印 entry、stop、
股數；`image_pack` 同步（入場寫「暫不掛單」、止損寫「未設」）。

---

## 44 隻重跑：前後對照

同一批股票、同一日（as_of 2026-11-06），用新引擎重跑：

| | 舊 (v5.5.3) | 新 |
|---|---|---|
| `Trigger_US.csv` | 19 | **0** |
| 其中 `Risk_ADR > 1.2` | 16 | 0 |
| 其中 `Room < 1R` | 14 | 0 |
| GME | STALK，買單 25.64 | **WATCH**，無票，寫明 `2.40×ADR > 1.2` |

19 張逐隻都被擋，且每一張都有具名理由（不是靜靜消失）：

```
CALY 5.32×   SARO 5.15×   NXT 4.18×   BIRK 3.98×   MIR 3.08×
LION 2.46×   ECVT 2.41×   GME  2.40×   ERII 2.19×   PRGO 1.60×
CTKB 1.49×   TMO 1.41×    BHB  1.41×   AZTA 1.35×   CRL 1.34×
WST 1.14×（room 0.20）    DNA 12.1%    ZYME 1.08×（room 0.22）  BTSG 1.08×（room 0.13）
```

34 隻清單同日仍有 1 張票：**RVTY**（0.84×ADR、3.9%、2.74R、Risk_OK PASS）。

---

## 這代表當日「沒有可交易 setup」——要選 caps

把 19 個候選按 caps 重算：

| ADR cap | % cap | room floor | 票數 |
|---|---|---|---|
| **1.2** | **8%** | 1.5（家族預設） | **0** |
| 1.2 | 無 | 1.5 | 1（DNA） |
| 1.5 | 8% | 1.5 | 1（CRL） |
| 1.5 | 無 | 1.5 | 2（CRL、DNA） |

**預設用 1.2 / 8%（審計建議），代價是那天一張票都沒有。**
這不是 bug，是那 44 隻在那一天真的沒有風險合格的票。要不要放寬，是策略決定，不是程式決定。

---

## 未做（需要你決定）

1. **REVERSAL 止損重寫**（審計 A）：5 隻 REVERSAL 的 stop 在 3–5×ADR。現在它們被 cap 擋掉，
   所以沒有迫切性；但若要讓 REVERSAL 重新可交易，就要把 stop 從「POC − 0.5ATR」改成
   更近的結構（反轉日低／MA20），否則這個家族在 ADR 高的名字上永遠出不了票。
   **我沒有擅自改**，因為那是換止損定義，不是修 bug。
2. **B1 的 trigger 改錨**（把 `Trigger_Price` 移到 `Supply_Level`）：現在用「不發票」處理，
   更保守；要改成「掛在真阻力」則是策略選擇。
