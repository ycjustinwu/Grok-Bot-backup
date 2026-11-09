# v6.10 — 風險閘門（2026-11-08，移植自 US v5.5.4）

**原因**：2269.HK 藥明生物以 STALK 出票，plan risk 17.3% = 2.72×ADR，而 HK 當時只有
`Risk_OK`（判斷「有無結構止損」），冇任何止損距離檢查；pending breakout 更在 risk band 檢查之前
就返回 `PENDING`，所以整條風險帶都被跳過。冇 trading plan 的票對操作者無用 —— 這就是移植的理由。

## 改了 6 個檔

| 檔 | 改動 |
|---|---|
| `gates.py` | 新增 `tradeability()`；CFG `risk` 加 `cap_adr`(1.2) / `cap_pct`(8.0，env 可覆寫)；`evaluate()` 輸出 `Tradeable` / `Tradeable_Why` / `Room_At_Plan_Stop_R` / `Room_At_1_2ADR_R` |
| `us_swing_v55.py` | 合約加 4 欄；`generate_trigger()` 只收 `Tradeable=PASS`（首次移植漏了這步，I30 抓出 11 張不可交易票） |
| `l2_prep.py` | `tradeable_gate()`：`Tradeable=FAIL` → 任何 class 一律 WATCH |
| `check_verdict.py` | 新增 **V4d**：BUY/STALK 必須 `Tradeable=PASS` |
| `invariants.py` | 新增 **I30**：`Trigger_US.csv` 每張票都要 `Tradeable=PASS` |
| `render_report.py` | WATCH/AVOID 不印入場/止損/股數，改印「暫不掛單／要等／原因」 |

## cap 是參數，不是寫死

```
SWING_RISK_ADR_CAP=1.2     # 風險 ×ADR 上限
SWING_RISK_PCT_CAP=8.0     # 風險 % 上限（會浮動到 1.2×ADR，高 ADR 名字不被硬 8% 誤殺）
```

Justin 2026-11-08：「high adr one always high momentum stocks indeed」——所以 `cap_pct` 取
`max(8%, 1.2 × ADR%)`；低 ADR 名字若出現 12% 止損仍然 FAIL，分辨力保留。

## 驗證

- `HOME=/opt/data python3 tests/suite.py` → **51/51**（新增 1 個 v6.10 案例）
- `bash verify_hk.sh` → **ALL CHECKS PASSED**（24 條 invariant）
- 2026-11-06 同一批 39 隻實跑（`runs/hk/run_20261108_gate3`）：

| | 前 | 後 |
|---|---|---|
| BUY / STALK / WATCH / AVOID | 2 / 1 / 13 / 23 | **2 / 0 / 14 / 23** |
| Trigger 票數 | 3（含 2269） | **2**（6862 0.63×ADR、0386 0.99×ADR） |
| 2269.HK | STALK | **WATCH** — `risk=2.72xADR > 1.2`；`risk=17.3% > 8%`；`room@plan stop=0.63R < 1.5` |

S4/S5 未跑（`check_verdict` 因而 exit 2，屬設計），本 patch 只改腳本，不改資料。
