---
name: Fusion Bridge
description: >-
  Use this when fusing 港股 Swing Setup technical output with Story Search 敘事報告
  into a ≤500-字 Fusion Report, 4-block infographic prompt, and optional baoyu
  one-pager — the bridge between those bots.
---
# Fusion Bridge

Orchestrate the bridge from **港股 Swing Setup** + **Story Search** → Key Action Fusion Report + Infographic prompt + optional one-pager image (Fusion Formatter v1.3).

## When to run

User pastes both reports, or points at Swing tech + Story 敘事 for the same ticker/date.

## Pipeline

1. **Fusion Ingest** — parse A+B; prefer GEMINI HANDOFF; tech over story; Adjusted_Stop only
2. **Fusion Report** — OUTPUT ① ≤500 字
3. **Fusion Infographic Prompt** — OUTPUT ② 4 blocks
4. **Fusion Swing Infographic** — (when user wants the image) baoyu-infographic dashboard from OUTPUT ②, layout like Henlius/HNGE/COTY examples
5. Quality checklist, then deliver

## Quality checklist

- [ ] OUTPUT ① ≤500 字
- [ ] 一句講晒 廣東話 ≤50 字
- [ ] OUTPUT ② ≤4 bullets/block
- [ ] VERDICT matches tech (not story)
- [ ] No facts outside inputs
- [ ] Stop = ADJUSTED STOP
- [ ] EARNINGS warnings when needed
- [ ] STALK uses volume-break framing
- [ ] If image generated: prices/VERDICT match Fusion; 16:9 dashboard

## Pipeline position

`CSV → 港股 Swing Setup → GEMINI HANDOFF → Story Search → 敘事報告 → Fusion Bridge → Fusion Report + Infographic Prompt → Fusion Swing Infographic (baoyu)`
