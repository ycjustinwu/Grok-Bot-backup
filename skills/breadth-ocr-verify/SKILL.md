---
name: Breadth OCR Verify
description: >-
  Use this after breadth chart capture — run /workspace/scripts/breadth_ocr.py
  then mandatory 8/8 vision cross-check; watch McClellan minus-sign and 5/8
  errors.
---
# Breadth OCR Verify

Extract LAST/close from breadth chart PNGs with `scripts/breadth_ocr.py`, then **vision cross-check all 8**. Never trust OCR alone.

## Script (canonical)

`/workspace/scripts/breadth_ocr.py` (copy also in `refactored_breadth_monitor/scripts/`)

```bash
# latest batch under /workspace/breadth
python3 /workspace/scripts/breadth_ocr.py
python3 /workspace/scripts/breadth_ocr.py --json
python3 /workspace/scripts/breadth_ocr.py -v
python3 /workspace/scripts/breadth_ocr.py /workspace/breadth/VIX_MMDD_rgb.png
```

Default `--workspace` is `/workspace`. Exit `0` all good · `2` vision fallback needed · `1` tesseract failed.

## Strategy (in script)

PSM 3 → 6 → 11 → 12. Prefer `(Daily)` then `Last`. Skip `decimal_fallback` if daily/last found (avoids Open). Convert palette PNG to RGB before enhance.

Vision fallback flags: value `None` · `|value| < 10` · ends `.03`/`.07`. McClellan minus-drop is **not** auto-detected — that is why 8/8 vision is mandatory.

Need `tesseract` + Pillow. RGB convert if mode P.

## After script — still vision 8/8

VIX, SPXA50R, SPXA200R, SPXA20R, NYSI, NYMO, NAMO, NASI. Extremes >80%/<20%. Quote-Last vs (Daily). McClellan sign. Cross vs FRED if contradictory.

Traps: 5↔8 · 1↔7 · missed decimal · dropped minus · Open vs Last.

Hand verified values to **Breadth Daily Report**.
