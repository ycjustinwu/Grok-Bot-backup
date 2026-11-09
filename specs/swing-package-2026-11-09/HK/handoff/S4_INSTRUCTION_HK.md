# S4 Story 任務書（港股・SuperGrok 版）— run_earn_over / as_of 2026-11-06

> 你只需要寫**敘事文字**。所有價格、比率、股數由程式從 `L2_Input.csv` 填入，**你不要改任何數字、不要發明目標價**。
> 輸出：每隻股票一個 `<TICKER>_story.json`（UTF-8、純 JSON、不加註解）。

## 一、你要寫的三隻

### 1. 0386.HK — 中國石油化工（Sinopec）
- 系統判定：**BUY**（A_SETUP / PULLBACK-B / 可即市入）
- 進場參考 4.805｜失效位（跌破即錯）4.695｜風險 2.29%（0.91×ADR）｜上行空間 1.18R（至 RES20 4.93）
- Leader PASS、量能 NOT_APPL、財報 CLEAR（不在 7 日內）
- 系統理由：回調 1.1ATR 至支撐 4.79，跌幅 0.91×ADR、量 1.00×
- 注意：軟阻力 AVWAP_20D_HIGH 4.82 只差 0.14R

### 2. 6862.HK — 海底撈國際（Haidilao International，餐飲）
- 系統判定：**BUY**（A_SETUP / BREAKOUT-A_BASE / 下一日開市）
- 進場參考 10.19｜失效位 10.02｜風險 1.67%（0.59×ADR）｜上行空間 1.76R（至 BEAR_FVG 10.49）
- Leader **FAIL**、量能 PASS（1.76× 均量）、財報 CLEAR
- 系統理由：12 日寬底突破，底部寬度 3.7×ATR

### 3. 2269.HK — 藥明生物（WuXi Biologics）
- 系統判定：**STALK**（C_WATCH / BREAKOUT-A_BASE / 未觸發，buy-stop 51.60）
- 風險 **17.25%（2.70×ADR）＝ 太闊**：止損放在突破日低位；若以 51.60 成交，當日低位必須守在 47.65（1.2×ADR）之上才算可用
- Leader **FAIL**、量能 PENDING、財報 CLEAR
- 注意：軟阻力 VAH_60D 53.85 只差 0.68R

## 二、輸出 schema（每隻一份 JSON）

```json
{
  "ticker": "0386.HK",
  "market_line": "一句市場定位（≤40 字，寫板塊／資金流，不寫技術指標）",
  "story_main": "主敘事（≤200 字，空格與標點不計）",
  "story_main_score": 0,
  "why_now": "為何是現在（≤60 字）",
  "moat": "護城河／競爭位置（1–2 句）",
  "numbers": "基本面數字（營收／利潤／指引；有出處）",
  "story_sub": "次線敘事（≤120 字）",
  "story_sub_score": 0,
  "risks": ["故事或基本面風險，最多 4 條；不可寫技術指標或系統價位"],
  "conviction": "CONFIRM | CHALLENGE | NEUTRAL",
  "conviction_why": "為何這個 conviction（1 句）",
  "story_tag": "短標籤",
  "hard_event": "下一個硬事件（業績／政策／數據）或 null",
  "earnings_check": "財報日期與距離，或 NOT_NEAR",
  "sources": ["來源名稱 + 日期"],
  "traps": "最容易被人講錯的一點"
}
```

## 三、硬規則（違反＝整份退件）

1. **不得出現**自行發明的目標價、`T1/T2/T3`、`RR`、RSI、MA、ADR、量比、系統止損價。
2. 引用賣方數字**必須寫出處**（例：「分析師平均目標 5.2 元（2026-10 券商報告）」），否則一律當發明。
3. `conviction` 只可用 `CONFIRM` / `CHALLENGE` / `NEUTRAL`。
4. `risks` ≤ 4 條，只寫**故事／基本面**風險；技術風險由程式負責。
5. 繁體中文（香港用語），不要簡體字；股票名首次出現寫全名。
6. **不要**改動系統給的 verdict、entry、stop、risk；你只描述「為何這隻值得／不值得看」。
7. 每隻的 `sources` 至少 2 個，其中至少 1 個係 2026 年 10 月之後。
8. 若你認為系統判定與事實矛盾（例如業績剛發盈警），照寫，但 `conviction` 用 `CHALLENGE` 並在 `conviction_why` 說明。

## 四、自檢（交回前逐條答）

1. 三隻是否各有一份獨立 JSON，檔名 `<TICKER>_story.json`？
2. 全文是否零個自製目標價／T1-T3／RR／技術指標？
3. `story_main` ≤200、`why_now` ≤60、`story_sub` ≤120 字？
4. `risks` 是否 ≤4 條且全部非技術性？
5. 是否繁體中文、無簡體字？
6. `conviction` 是否只用三個值之一？
7. 每隻 `sources` ≥2 且有一個 2026-10 之後？
8. 有無改動任何系統數字？（答案必須是「無」）

## 五、背景（讓你寫得準）

- 2026-11-06 港股：恒指 24,481.86（−1.27%）、成交 2,474 億（−30.6%）；**A 股創業板 −3.96%、PCB 板塊 −5.86%**，港股 AI 硬件鏈跌 7–16%，平台股相對抗跌
- 當日市場判定：**投資機會＝冇**（形態篩選 HK 只有 2 個 TC，動力股 14 隻散 11 行業）
- 所以這三隻要答的問題只有一個：**在一個「指數托住、個股冇人接」的日子，它們各自的敘事是否足以支撐一個有止損的倉位？**

---
*本任務書由 Hermes 生成（2026-11-07 01:0x HKT）。L1 事實與閘門已跑完；你只負責 S4。*
