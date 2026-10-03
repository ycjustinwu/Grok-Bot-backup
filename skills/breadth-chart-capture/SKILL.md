---
name: Breadth Chart Capture
description: >-
  Use this when capturing StockCharts market breadth charts (VIX,
  SPXA50/200/20R, NYSI/NYMO/NAMO/NASI) — SharpCharts direct PNG download first,
  RGB convert, Playwright only as fallback.
---
# Breadth Chart Capture

Fetch StockCharts breadth charts as PNGs. Trigger: `breadth` / `market breadth` / `run breadth`.

## Default method — SharpCharts direct image

Playwright sc3/ui often crashes in constrained containers. Prefer:

```bash
mkdir -p /workspace/breadth && cd /workspace/breadth
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0 Safari/537.36"
STAMP=$(date +%m%d)
for pair in "VIX:%24VIX" "SPXA50R:%24SPXA50R" "SPXA200R:%24SPXA200R" "SPXA20R:%24SPXA20R" "NYSI:%24NYSI" "NYMO:%24NYMO" "NAMO:%24NAMO" "NASI:%24NASI"; do
  name="${pair%%:*}"; sym="${pair##*:}"
  curl -sL -A "$UA" -o "${name}_${STAMP}.png" "https://stockcharts.com/c-sc/sc?s=${sym}&p=D&b=5&g=0&i=0" --max-time 30
done
```

## Verify

- `file` shows PNG
- Convert palette → RGB before OCR (P mode breaks tesseract enhance):
  `python3 -c "from PIL import Image; Image.open('X.png').convert('RGB').save('X_rgb.png')"`

## Fallback

1. SharpCharts direct (default)
2. Playwright `https://stockcharts.com/sc3/ui/?s=%24SYMBOL` screencap only if healthy
3. Manual browser screenshot

Then hand RGB PNGs to **Breadth OCR Verify**.
