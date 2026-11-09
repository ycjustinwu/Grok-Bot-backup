---
name: tvscreener
description: Use when Justin wants TradingView screener pulls via the unofficial tvscreener Python lib (stock/ETF/crypto/forex/options filters → Pandas), or a custom TV universe seed before Package Ops / Hermes. Not a substitute for Hermes or /opt/swing Contract/Tradeable/L2.
---

# tvscreener (TradingView Screener API)

Unofficial library: https://github.com/deepentropy/tvscreener · docs https://deepentropy.github.io/tvscreener/

## Runtime on this box

- Venv: `/workspace/tvscreener-venv`
- Python: `/workspace/tvscreener-venv/bin/python`
- MCP binary (optional connector): `/workspace/tvscreener-venv/bin/tvscreener-mcp`
- Package: `tvscreener==0.8.2` (+ `[mcp]`)

Always call through that venv — system pip is PEP 668 locked.

## When to use

- Seed a ticker universe / custom screen (gainers, RS, volume, ETF filters)
- Pull TV screener fields into a CSV for Justin or Package Ops intake
- Quick quotes / calendars / news helpers when TV MCP is awkward for bulk tabular

## When NOT to use

- US/HK swing Soft Final path (Hermes L1→S4→L2 or `/opt/swing` Package Ops)
- Inventing Contract / Tradeable / Trigger / Story JSON
- Replacing TradingView MCP AV-seed for daily briefs

## Smoke / basic pull

```bash
/workspace/tvscreener-venv/bin/python - <<'PY'
import tvscreener as tvs
ss = tvs.StockScreener()
df = ss.get()  # default ~150 rows
print(df.head())
# Optional: write CSV for handoff
# df.to_csv('/workspace/tvscreener-out/latest.csv', index=False)
PY
```

Prefer writing outputs under `/workspace/tvscreener-out/` with a dated filename, then tell Justin the path (and offer Drive upload only if he asks).

## Handoff to swing

If Justin wants a package scan from a tvscreener list: export ticker column → give **full list** to Swing Package Ops (`9c97ff04…`) on-demand; do not invent scan math here.

## MCP (optional)

If Justin enabled the tvscreener MCP connector, prefer its tools for interactive screens. Else use the venv Python script path (script-first).

## VERIFY
- [ ] Used `/workspace/tvscreener-venv/bin/python`
- [ ] Did not invent Contract/Tradeable/Trigger/Story JSON
- [ ] CSV under `/workspace/tvscreener-out/` when writing
