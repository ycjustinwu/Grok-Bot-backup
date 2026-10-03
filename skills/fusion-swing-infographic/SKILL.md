---
name: Fusion Swing Infographic
description: >-
  Use this when generating the one-page swing-trade finance infographic after
  Fusion Formatter — map OUTPUT ② into the Henlius/HNGE/COTY-style 4-block
  dashboard and generate via baoyu-infographic.
---
# Fusion Swing Infographic

Generate the **one-page swing-trade infographic** that sits after Fusion Formatter. Upstream: Fusion OUTPUT ① (快報) + OUTPUT ② (4-block prompt). Downstream: image via **baoyu-infographic** (preferred for data-rich finance).

## When to use

User has a fused Swing + Story brief and wants the visual one-pager like the Henlius / Hinge Health / Coty examples.

## Layout contract (match examples)

Landscape **16:9** one-pager:

1. **Header** — `TICKER MARKET` · name · short theme title · sector chips · earnings badge if present
2. **主題故事** — 3–4 icon+metric bullets from story (verbatim numbers)
3. **關鍵維度** — RS · Minervini/trend · Vol_Expansion · Stop_Type (+ Ext/RSI/52W dist if in input)
4. **操作劇本** — VERDICT | setup · Entry (green) · Stop=`ADJUSTED STOP` (red) · Ladder T1–T3 · RR · Priority · optional mini path chart
5. **一句講晒** — copy from Fusion Report (Cantonese) · small disclaimer/sources

Full visual notes: `/workspace/refactored_fusion_formatter/docs/swing-infographic-layout.md`  
Examples: `/workspace/refactored_fusion_formatter/docs/infographic-examples/`

## Pipeline

1. Require Fusion OUTPUT ② (and ① if available). If only raw Swing+Story, run **Fusion Bridge** first.
2. Map blocks → `structured-content.md` style sections; **no new facts**.
3. Call **baoyu-infographic**:
   - Layout: `dashboard` (default) or `dense-modules` if very packed
   - Style: craft-handmade or technical-schematic / corporate-memphis if user prefers cleaner boards
   - Aspect: `16:9` · Language: zh-TW for HK names; match source otherwise
4. Confirm layout×style×aspect unless user already said `GENERATE` / `直接生成` / `--no-confirm`.
5. Generate image; attach result. Keep all prices/VERDICT identical to Fusion (tech wins).

## Verdict framing in the visual

- **STALK** — “Setup coiled; wait volume at entry/TZ high” — not a chase badge
- **WATCH** — wait breakout or pullback zone
- **BUY** — only if Fusion VERDICT is BUY
- Never paint a bullish hero that contradicts WATCH/AVOID

## Anti-jobs

- Do not use sketchnote cream-paper for these finance boards (wrong density)
- Do not invent stops/targets
- Do not drop the stop or ladder
- Do not upgrade VERDICT for a prettier story panel
