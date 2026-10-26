---
name: Story Search Report
description: >-
  Use this when producing the full Story Search narrative report from a HK or US
  Swing Setup GEMINI HANDOFF — FA-depth Why Now/moat/numbers/tech-alignment,
  Cantonese closer, Fusion-ready; never override the technical VERDICT.
---
# Story Search Report

Turn a **港股 or 美股 Swing Setup** `GEMINI HANDOFF` into a Fusion-ready **敘事報告**. 繁體中文 + 廣東話一句講晒. Do not redo chart analysis. Do not invent news. Do not change Swing’s VERDICT.

## Upstream / downstream

- **Upstream:** 港股／美股 Swing Setup labeled GEMINI HANDOFF (`MARKET=HK|US`)
- **Downstream:** Fusion Formatter (paste 敘事報告 as-is)
- **Pinned inputs:** read exactly the files listed in the HANDOFF / TC `PINNED_INPUTS` (e.g. that day's Summary_US/Summary_HK, scanner CSV, regime file), never "latest". If you need a file that is not pinned, note its absolute path under `OPEN_QUESTIONS`.
- **Settled rulings:** treat HANDOFF `DECISIONS_MADE` as closed; do not re-open them in the narrative.

## Pipeline

1. **Story Handoff Parse** — contract fields, earnings gate, HK/US, term lock
2. **Story Theme Match** — policy pillar or megatrend (`/workspace/refactored_story_search/docs/knowledge/`)
3. **Story Web Search** — ≥3 company searches; cite enough sources for every number (often 5–7)
4. **Story Narrative Validate** — Why Now / moat / numbers; CONFIRM/CHALLENGE vs CLAUDE CONVICTION
5. Emit Fusion output + checklist

## Depth bar (FA exemplar — required)

Justin’s expected depth matches the **First Advantage (FA)** style report. Thin summaries are not enough. Local note: `/workspace/story-search/docs/EXPECTED_DEPTH_FA_EXEMPLAR.md`

**Header must include:** ticker + name · 搜尋日期 · Handoff 日期 · MARKET · 市場主線 · 政策傳導層級（HK 第X層／US 核心｜邊緣）· Earnings 窗（CLEAR/CAUTION/PASS/UNKNOWN + days + next date if known）

**🗺️ 敘事定位 (short):** 主線一句 · Why Now 一句 · 護城河一句 · 傳導確定性 · KB 覆蓋註記（有／無；無則註明全靠 90 日內 search）

**Each of 1️⃣ 主／2️⃣ 次／3️⃣ 風險 must have:**
- 強度 or 風險 **x/10**
- **Why Now** (what changed; window; why not earlier)
- **護城河** (type + copyability in 12 months) — at least on 主敘事
- **數字驗證** with concrete figures, dates, and `[SEARCH]` tags — no bare claims
- **與技術訊號** — align or conflict with ENTRY／Vol／T1／TECHNICAL CONCERN; **never** change VERDICT or prices
- **主張標籤** (short claim + `[SEARCH]`)
- Risk block: pair to Claude TECHNICAL CONCERN; mark **陷阱** (narrative fallacy, big-TAM, etc.)

**💬 一句講晒:** 廣東話 ≤50 字；含順風車／Why Now 元素 + entry／stop／target（或等區）+ 一大風險；情緒標籤匹配 VERDICT

**搜尋來源:** title + URL，通常 **5–7** 條（業績、催化、分析師、風險／減持各至少一）

**CONVICTION ASSESSMENT:** CONFIRM｜CHALLENGE｜NEUTRAL + 硬數字對位 Claude 級別；明確「確認業務方向 ≠ 確認放量突破」類界限

## Cantonese closer (match VERDICT)

- **BUY** (or STALK with clear buy-soon plan): 搭順風車 + Why Now + RS if given + entry/stop/target + one risk
- **STALK / WATCH**: story exists; wait for entry zone or volume break — not chase
- **PASS / AVOID**: story may sound nice but tech + narrative risk; watchlist trigger only

Emotion: 🚀火箭升空｜✅穩陣上車｜⚡觀望等位｜⚠️刀口舔血｜❌敬而遠之

## Output (Fusion)

```
═══════════════════════════════════════════
📖 敘事報告：[TICKER] [NAME]
搜尋日期：[YYYY-MM-DD]
Handoff 日期：[YYYY-MM-DD]
市場：HK|US
市場主線：[…]
政策傳導層級：[第X層（HK）/ 核心｜邊緣（US）]
Earnings 窗：[CLEAR|CAUTION|PASS|UNKNOWN — N days；下一次約 …]
═══════════════════════════════════════════
🗺️ 敘事定位
主線／Why Now／護城河／傳導確定性／KB 覆蓋註記
───────────────────────────────────────────
1️⃣ 主敘事：…（強度：x/10）
Why Now／數字驗證 [SEARCH]／與技術訊號／主張標籤
2️⃣ 次敘事：…（強度：x/10）
…
3️⃣ 風險敘事：…（風險：x/10）
對位 TECHNICAL CONCERN／陷阱標記 [SEARCH]
───────────────────────────────────────────
💬 一句講晒（≤50字）
情緒標籤：…
搜尋來源：（5–7 title+URL）
CONVICTION ASSESSMENT: CONFIRM|CHALLENGE|NEUTRAL + 數字依據
───────────────────────────────────────────
PINNED_INPUTS:  [carry Swing HANDOFF list verbatim (absolute paths) | none — upstream missing]
DECISIONS_MADE: [carry Swing HANDOFF verbatim + any new Justin/coordinator ruling for this job | none]
OPEN_QUESTIONS: [Story's unresolved items + any unpinned file path used + any upstream field noted missing | none]
NEXT_GATE:      [e.g. "Fusion → merge; Work Verifier → PASS/PASS_WITH_NOTES before Final"]
═══════════════════════════════════════════
```

## Quality checklist

RS sign · entry≠stop · Cantonese matches VERDICT · triple validation · HK layer or US core/peripheral · per-block strength scores · numbers dated+[SEARCH] · tech alignment without VERDICT change · traps marked · no fiction · ≥5 sources · Fusion-ready · handoff tail present (PINNED_INPUTS / DECISIONS_MADE / OPEN_QUESTIONS / NEXT_GATE) · only pinned files read (else path under OPEN_QUESTIONS)
