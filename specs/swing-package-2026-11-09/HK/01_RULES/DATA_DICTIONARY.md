# 資料字典 — `Contract_US.csv`（v6.0：109 欄）

一檔股票一行，最後一根 bar 的值。`03_RUN_2026-11-04/Contract_US.csv` 就是這份 schema 的實例。

**讀這份檔案前先知道三件事**

1. 三態閘門 `PASS / FAIL / UNKNOWN`；`Risk_OK` 多一個 `PENDING`（突破前的止損還沒存在）。
2. 任何 `*_Why` 都是「數字 + 門檻」，不是形容詞。
3. 沒有 `BUY`。`Candidate_Class` 是分類，不是建議。

---

## A. 身分與分類（1–6）

| 欄位 | 型別 | 意義 |
|---|---|---|
| `Ticker` / `Date` / `Close` | str / date / float | 標的、最後一根 bar 的日期、收盤 |
| `Candidate_Class` | enum | `A_SETUP`（Setup+Risk 都過）/ `C_WATCH`（**Setup PASS + Risk FAIL**）/ `B_LEADER_WAIT`（強勢股但沒 setup）/ `X_NONE` |
| `Screen_Flag` | enum | 上面四者的標籤版（`SETUP/WATCH/LEADER_WAIT/NONE`），給不讀 class 的舊流程用 |
| `Entry_Feasible` | enum | `AT_TRIGGER`（今日突破）/ `NEXT_DAY` / `LATE` / `NOT_YET`（等突破）/ `AT_MARKET`（回調，可現價）/ `MISSED` / `INVALIDATED` / `NO_SETUP` |

## B. 三個閘門（7–12）

| 欄位 | 意義 |
|---|---|
| `Leader_OK` / `Leader_Why` | 趨勢（Minervini 或 soft）＋ `RS_Score ≥10` ＋ 股價 ≥$5、日均額 ≥$20M |
| `Setup_OK` / `Setup_Why` | 有 base（5–40 日、寬度 ≤ 家族上限、狀態 READY/ARMED/TRIGGERED）或 有 pullback 且低動能 |
| `Risk_OK` / `Risk_Why` | 風險在家族 ADR 帶內 ＋ 到供給 ≥ 下限 R ＋ 盈利非 PASS ＋ 未延伸 |

`*_Why` 會列出**失敗的那幾條**（最多 3 條），全過時列關鍵數值。

## C. 分數（13–14）

| 欄位 | 意義 |
|---|---|
| `Priority_Score` | 0–65，**只有領導力**：`MN 20 + MA 10 + RS 10/20/30 + Q ≤5 − EXT 20`。是排序鍵，不是門檻，也不代表 setup 品質 |
| `Score_Breakdown` | `MN:+20|RS:+30|Q:+2` 這種形式；各項相加**必定**等於 `Priority_Score`（不變量 I1） |

## D. 領導力原料（15–30）

| 欄位 | 意義 |
|---|---|
| `RS_Score` | 63 日報酬減 SPY，百分點 |
| `RS_Status` | `OK` / `UNKNOWN`。抓不到 SPY 時是 UNKNOWN，**不會寫 0** |
| `RS_1M` / `RS_3M` | 20 / 60 日相對報酬 |
| `RS_Line_Up` / `RS_Line_NH` / `RSNHBP` | RS 線 20 日 +1%、63 日新高、新高但價格未新高 |
| `Weak_Day_RS_Pct` | 最近 20 個 SPY 下跌日中，該股跑贏的比例（forward-filled） |
| `RS_Role` | `leader` / `candidate` / 空（匯出標籤，不進分數） |
| `Minervini_Trend` / `Minervini_Stage2` | 0/1 |
| `Extension_MA20_Pct` | 距 MA20 的百分比（紅旗 #1 用） |
| `RSI_14` | Wilder RSI |
| `Vol_Expansion` | 今日量 ÷ 50 日均量 |
| `Vol_Avg_20` | 20 日均量（股數） |
| `ADR_Pct` | 14 日平均日幅 ÷ 收盤 ×100 |

## E. Base 與 Setup（31–45）

| 欄位 | 意義 |
|---|---|
| `Setup_Family` | `BREAKOUT` / `PULLBACK` / `NONE` — 這次判定用的是哪一條路 |
| `Setup_Code` | `A_BASE`（base 突破）或 `B` / `D` / `E` / `H`（回調家族） |
| `Pullback_Code` | 若當日存在回調候選，是哪一個（即使最後選了突破） |
| `Base_State` | 被選中的那個 base 的狀態：`FORMING/READY/ARMED/TRIGGERED/SPENT/FAILED/EXPIRED/NONE`；回調時為 `PULLBACK` |
| `BaseS_State` / `BaseW_State` | 兩個家族的狀態（同時匯出，方便比較） |
| `Setup_Len_Days` | base 長度（回調時為 0） |
| `Base_Width_ATR` / `Base_Width_Pct` | base 高度 ÷ ATR、÷ 價格 |
| `Base_Compressed_Pct` | 區段內真正壓縮的 bar 比例（寬鬆家族才有意義） |
| `Base_Cleanliness` | 區段內收在 MA20 上的比例 |
| `Base_Vol_Decay` | 區段均量 ÷ 區段前 20 日均量 |
| `Base_HigherLows_Pct` | 壓縮日之間低點遞升的比例 |
| `Base_Prior_Advance_Pct` | base 起點前 63 日的最低點到 base 高點的升幅 |
| `Base_Count_126` | 最近 126 根內有幾個 base（含失敗/過期；「頻繁換手」的代理，不是「第幾波」） |
| `Depth_ATR` | 回調深度（ATR 倍數），PULLBACK 品質分用 |
| `Vol_Ratio_Pullback` | 回調 3 根均量 ÷ 20 日均量，PULLBACK 品質分用 |
| `Confluence_Count` | 回調時位於價格下方的支撐位數目（MA20 / AVWAP_low / POC / SR flip），PULLBACK 品質分用 |
| `Drawdown_Pct` | 反轉前的跌幅（前 252 日高 → 60 日低），REVERSAL 品質分用 |
| `UpDown_Vol` | 低點以來上漲日量 ÷ 下跌日量，REVERSAL 品質分用 |
| `HigherLow_Pct` | 低點之後形成的更高低點高出幾 %，REVERSAL 品質分用 |
| `MA10` / `MA20` / `MA50` | 移動平均，支撐梯級用 |
| `SMA50_Slope` | MA50 相對 10 個交易日前的变化（%），趨勢列用 |
| `VAL_60D` | 60 日成交量價值區下緣，支撐梯級用 |

## F. 委託單（46、56–68）

| 欄位 | 意義 |
|---|---|
| `Stop_Type_Plan` | 這筆的止損屬於哪一類：`PB_STRUCT` / `MA_STRUCT` / `VP_STRUCT` / `SR_STRUCT` / `TRIGGER_LOW` / `BASE_LOW` |
| `Trigger_Date` / `Days_Since_Trigger` | 突破日、距今幾根 |
| `Trigger_Price` | 計畫觸發價 = base high ×1.001（未突破時）或實際進場參考 |
| `Trigger_Min_Vol` | 突破日的最低量門檻（1.5 × 20 日均量） |
| `Trigger_Vol_Ratio` | 突破日實際量 ÷ 20 日均量；`Volume_Confirm` 的來源，紅旗 #2 引用它 |
| `Entry_Ref` / `Entry_Src` | 進場參考價與來源（觸發收盤／計畫觸發／現價） |
| `Invalidate_Below` | 失效價：突破前是 base low，突破後是突破日低點 |
| `Risk_Pct_Plan` / `Risk_ADR_Plan` | 風險百分比、除以 ADR 的倍數 |
| `Room_To_Supply_R` | （最近供給 − 進場）÷ 風險。**全檔唯一的「報酬」數字** |
| `Supply_Level` / `Supply_Source` | 最近供給價，來源 `RES20_PRIOR` / `HIGH52W_PRIOR` / `NONE_ABOVE`（藍天） |
| `Shares_per_1000_Risk` | 每 1000 美元風險可買幾股（中性單位，不是建議倉位） |
| `Room_Basis` | `RISK` = 空間以實際風險為單位；`PROV_1ADR` = 突破前用 1×ADR 暫代（R 只是名稱）；`NONE` = 無空間可用 |

## G. 市場狀態（47–55）

| 欄位 | 意義 |
|---|---|
| `Regime_State` | `MOMENTUM` / `NEUTRAL` / `RISK_OFF` / `UNKNOWN` |
| `Regime_Label` | 使用者表上的原始文字（例如 `強勢`） |
| `Regime_Source` | `SHEET` / `INDEX_FALLBACK` |
| `Regime_Date` | 表上的日期（落後 >3 天會標 STALE 在 `Regime_Why`） |
| `Index_Regime_State` | 第二意見：^IXIC 10/20 EMA |
| `Breadth_50D` / `Ratio_10D` / `Momentum_Share` / `Sp500_Chg_Pct` | 表上的市寬、10 日比率、動力股佔比、S&P 漲跌 |

## H. 結構位（69–80，全部 per-bar）

| 欄位 | 意義 |
|---|---|
| `Resistance_20D_Prior` | 前 20 日最高（不含今日） |
| `High_52W` / `Dist_from_52W_High_Pct` | 252 日高、距 52 週高 % |
| `POC_60D` / `Dist_to_POC_Pct` | 60 日成交量控制點與距離 |
| `AVWAP_20D_Low` / `Dist_to_AVWAP_Low_Pct` | 以 20 日低點為錨的 VWAP |
| `AVWAP_HVD` | 以 126 日最大量日為錨的 VWAP |
| `VAH_60D` | 60 日價值區上緣 |
| `SR_Flip_Level` | S/R 翻轉位（舊高被突破後的價位） |
| `SR_Flip_Live` | 該翻轉位仍有效（未失效、未過期）—— setup H 的前提 |
| `SR_Flip_Age` | 距突破那根幾根 bar（15 根後失效） |
| `Bullish_FVG1_Upper/Lower` | 價格下方最近**未被回補**的多方缺口 |

## I. 盈利與版本（81–84）

| 欄位 | 意義 |
|---|---|
| `Earnings_Proximity_Flag` | `CLEAR` / `CAUTION`（8–14 日）/ `PASS`（≤7 日）/ `UNKNOWN` |
| `Volume_Confirm` | `PASS` / `LOW` / `PENDING` / `UNKNOWN` / `NOT_APPL`（非突破家族）。**不要用 `NA`**：pandas 會讀成缺失值 |
| `Room_To_Soft_R` | 到最近的**軟**供給（VAH/AVWAP/MA50/200）的空間；只作提醒，不攔截 |
| `Earnings_Date` / `Days_To_Earnings` | 下次盈利日，以及距離幾個 **NYSE 交易日（sessions）**——v6.1 起引擎、字典、handoff、快報四處統一為交易日；`≤7` / `8–14` 兩個門檻也是交易日 |
| `contract_version` | `us-contract-1f.4`；schema 改了就要改這個 |
| `Market` | `US` / `HK`（`SWING_MARKET`） |
| `Benchmark` | RS 的基準：US `SPY`、HK `2800.HK` |

---

## 不在這張表裡的東西（已刪除）

`Tight_Zone_*`、`Playbook_Flag`、`Setup_Type`、`Stop_Type`、`Adjusted_Stop`、`RR_*`、
`Target_*`、`Suggested_Stop`、`Risk_*`、`Reward_*`、`Mini_Breakout_*`、`Breakdown_*`、
`Slap_Back_*`。理由見 `04_HISTORY/OLD_SYSTEM_EVIDENCE.md`。
