---
name: Breadth Daily Report
description: >-
  Use this when Justin asks for breadth / market breadth / run breadth —
  capture, OCR+vision, FRED VIX/VXVCLS via /workspace/scripts, emit the 9-row
  Daily Breadth Report.
---
# Breadth Daily Report

Daily market-breadth report. Triggers: `breadth` / `market breadth` / `run breadth`.

## Pipeline

1. **Breadth Chart Capture** — 8 SharpCharts PNGs → RGB under `/workspace/breadth`
2. **Breadth OCR Verify** — `python3 /workspace/scripts/breadth_ocr.py` then **8/8 vision**
3. **FRED VIX Term Structure** — `python3 /workspace/scripts/fred_vix.py --quiet` (needs `FRED_API_KEY`)
4. 9-row table + overall line

## 9-row order

$VIX · **$VIX/VXVCLS (FRED)** · $SPXA50R · $SPXA200R · $SPXA20R · $NYSI · $NYMO · $NAMO · $NASI

Signal zones: SPXA <30/30–40/40–60/>60 · oscillators <-30 / -30–0 / 0–+30 / >+30 · summation <0 / 0–100 / 100–300 / >300 · VIX/VXVCLS <0.82 POOR · 0.82–1 CALM · >1 UNCERTAINTY

Scripts live at `/workspace/scripts/` (package copy: `refactored_breadth_monitor/scripts/`).
