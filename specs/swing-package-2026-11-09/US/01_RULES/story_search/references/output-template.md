# Output template — Fusion Prompt v1.1（v5.5.2 註記見末段）

Do not rename fields. Downstream Fusion reads these names.

## Handoff input (do not invent extra tech fields)

Accept extra Claude lines (SETUP TYPE, STOP TYPE, SCENARIO ENTRY, STOP ANCHOR) as context. Only
VERDICT / ENTRY / STOP / TARGET / EARNINGS / TECHNICAL CONCERN / CLAUDE CONVICTION are binding.
Extra lines may be cited in 風險敘事. Do not rebuild a chart.

If the block is incomplete (no TICKER or no VERDICT or market cannot be inferred) → refuse.

> **v5.5.2 override.** The engine emits `STORY HANDOFF v5`, not `GEMINI HANDOFF`. Binding fields
> are `VERDICT / ENTRY / STOP / SUPPLY ABOVE / EARNINGS / TECHNICAL CONCERN / QUALITY`.
> **`TARGET` does not exist** — the block says `TARGET: NONE (v5 has no target)`.

## Cantonese closer (≤50 characters, must match VERDICT)

### BUY

```
「[股票] 搭上 [主敘事] 呢班順風車，
[Why Now 一句]，
RS +[數] 係市場強勢股。
$[入場] 上車，$[止損] 守住，目標睇 $[T]。
最要留意 [最大風險]，倉位控制好。」
```

If RS is MISSING, drop the RS clause. Do not invent RS.

> **v5.5.2 override.** The BUY template above contains 「目標睇 $[T]」 — **delete that clause**.
> v5 has no target; quote `SUPPLY ABOVE` as resistance instead, without a target price.

### WATCH / STALK

```
「[股票] 故事係有——[主敘事一句]，
但技術上 [問題]，依家唔係最佳時機。
等回調到 $[入場] 或放量突破 $[位] 先部署，
急住追係 [風險比喻]，等等更值博。」
```

### AVOID / PASS

```
「[股票] 雖然 [主敘事] 聽落吸引，
但 [技術問題] 加上 [敘事風險]，
故事同數字都未支撐現價。
放 Watchlist，等 [具體觸發] 先考慮。」
```

If EARNINGS ≤7 days, the closer must flag binary risk (example 「出數前純賭仔」).

## Report block (paste-ready)

```
═══════════════════════════════════════════
📖 敘事報告：[TICKER] [名稱]
搜尋日期：[YYYY-MM-DD]
Handoff 日期：[YYYY-MM-DD]
市場：[HK / US / …]
市場主線：[主線 / Trend 名]
政策傳導層級：[第X層（HK）/ 核心|邊緣|無關（US）]
Earnings 窗：[CLEAR/CAUTION/PASS — X days；規則提示一句]

═══════════════════════════════════════════
🗺️ 敘事定位
主線：[名稱]
Why Now：[一句]
護城河：[類型 + 強弱]
傳導確定性：[高 / 中 / 低]
KB 覆蓋註記：[有無以 search 覆蓋舊 KB 數字；無則寫 無]

───────────────────────────────────────────
1️⃣ 主敘事：[標題]（強度：X/10）
[≤300 字]
數字驗證：[訂單/補貼/readout/deal/業績 — 帶日期]
與技術訊號：[呼應 / 衝突 / 中性]
主張標籤：關鍵句後標 [SEARCH] 或 [KB]

2️⃣ 次敘事：[標題]（強度：X/10）
[≤150 字]

3️⃣ 風險敘事：[標題]（風險：X/10）
[≤200 字]
[必須涵蓋：Claude TECHNICAL CONCERN + 最大基本面/流動性風險 + 縮量/earnings 若存在]

───────────────────────────────────────────
💬 一句講晒（廣東話，≤50 字）
「[金句]」

情緒標籤：[🚀火箭升空｜✅穩陣上車｜⚡觀望等位｜⚠️刀口舔血｜❌敬而遠之]

搜尋來源：
- [標題 + URL + 日期]
- [標題 + URL + 日期]
- [標題 + URL + 日期]

CONVICTION ASSESSMENT: [CONFIRM / CHALLENGE / NEUTRAL]
[一句：為何確認/挑戰；必須引用 search 結果，不得空泛]
```

## Emotion vs VERDICT

| VERDICT | Allowed tags |
|---------|----------------|
| BUY | 🚀火箭升空 or ✅穩陣上車 |
| WATCH / STALK | ⚡觀望等位 |
| AVOID / PASS | ❌敬而遠之 or ⚠️刀口舔血 |

---

## v5.5.2 交付物（機器用）

在這個管線裡，**報告由 `render_report.py` 產生**，S4 只交兩份 JSON：

1. `stories/<T>_search_log.json` — `{ticker, searched_at, queries:[{q, hits:[{title,url,date}]}]}`
2. `stories/<T>_story.json` — `{ticker, company, story_date, market_line, route_tag, story_main,
   story_main_score, why_now, moat, numbers:[{text,url,date}], story_sub, story_sub_score,
   risks:[], conviction, conviction_why, story_tag, hard_event, earnings_check, sources:[],
   traps:[]}`

上面的 Fusion 文字區塊由 renderer 從這兩份 JSON 排版而成，所以**不要手寫快報**；
`closer` / `emotion` / `invalidation` / `industry` / `title` / `finance_line` / `driver_line`
放在 `verdicts_US.jsonl`（S5）。
