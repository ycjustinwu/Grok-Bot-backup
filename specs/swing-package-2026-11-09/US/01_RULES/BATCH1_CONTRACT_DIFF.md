# 第一批：Contract 逐格比對（v6.0 → v6.1）

約束：**同一份樣本、同一個 as-of，引擎未改一行，Contract 109 欄應逐格不變。**

## 方法

```
SWING_MARKET=us SWING_ASOF=2026-11-04 SWING_TICKERS=<34 隻> python3 us_swing_v55.py
```

比對：34 隻 × 108 欄（Ticker 當 index），數值容差 `atol=1e-9`、字串完全相等。

## 結果

| 項目 | 數值 |
|---|---|
| 列數 | 34 → 34（相同 ticker） |
| 欄數 | 109 → 109 |
| **有差異的格子** | **1** |

### 唯一的差異

| 檔 | 欄位 | 前 | 後 | 差 |
|---|---|---|---|---|
| ROL | `High_52W` | 65.3972 | 65.3971 | **−0.0001** |

**原因**：Yahoo 對 ROL 歷史某一根 bar 的調整後最高價在兩次抓取之間有小數第四位的修訂。
不是程式差異。

**下游有沒有變？** 全部一樣：

```
Close            38.38   -> 38.38
Supply_Level     65.40   -> 65.40
Supply_Source    HIGH52W_PRIOR -> 同上
Room_To_Supply_R 4.1143  -> 4.1143
Leader_OK        FAIL    -> FAIL
Candidate_Class  C_WATCH -> C_WATCH
Risk_OK          FAIL    -> FAIL
```

## 結論

**沒有一格因程式改動而變。** 唯一差異是同一個外部資料源在 4 位小數的抖動，
且不影響任何判斷欄位。

> 若第二輪看到 Contract 有變，那是資料漂移，不是這批修正造成的。
