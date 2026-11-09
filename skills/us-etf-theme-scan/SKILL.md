---
name: US ETF Theme Scan
description: >-
  Use this when scanning a TradingView US-ETF CSV for daily market themes — Tier
  1 39 names always, Tier 2 SPDR/breadth as confirmation, Tier 3 macro alerts on
  trigger; report X/N quoted.
---
# US ETF Theme Scan

Find the day’s **strong / weak thematic ETFs** from Justin’s TradingView `US-ETF_[DATE].csv`. Silent work; hand a structured theme list to the brief.

## File

Read the **entire** CSV. Filter **Price Change % 1 day > +1% or < −1%**. Pull latest from Drive folder `1k5dJy7ny5n-W_EV5Aglt0QeeXS_-5Ijn` when not attached.

**Quoted coverage (locked 2026-10-31):** After the scan, report **X/N quoted** for the Tier-1 universe (and note unresolved tickers). Never silently shrink N when rows are missing — unresolved stay visible under DATA GAPS.

**Ticker rename (locked 2026-10-31):** Tema American Reshoring ETF **RSHO → WELD** (fund rename 2026-06-01; ticker change 2026-06-22). Prefer **WELD** in Tier-1 / thin-peer lists. If a CSV still lists RSHO or omits WELD, treat as stale ticker in the source file — do not invent %, and do not report “missing RSHO” as an active gap once WELD is present.

## Three-tier scan (do not skip Tier 1)

### Tier 1 — always scan all 39 (output every name with |1D| > 1%)

- AI/Tech: AIQ, BOTZ, IGV, QTUM, ARKK, IPO
- Semiconductors: SOXX, SMH
- Space/Defense: UFO, PPA, ROKT, SHLD, ITA, DRNZ
- Energy Transition: URA, NLR, LIT, COPX, REMX, ICLN, TAN
- Biotech: XBI, GNOM, IDNA, OZEM, HEAL
- Crypto/Fintech: WGMI, BITQ, BLOK, FINX, IBIT
- Cyclicals: KRE, XHB, ITB, PAVE, WELD, JETS
- Value/Sentiment: SCHD, MEME

If a ticker is missing from the CSV, note the gap; do not invent a %.

### Tier 2 — confirmation only

Use **only after** a matching Tier 1 theme is confirmed (not a free scan):

- 11 SPDRs: XLK, XLC, XLY, XLF, XLV, XLI, XLP, XLE, XLB, XLU, XLRE
- Breadth: VOO, QQQ, IWM, RSP

### Tier 3 — silent unless a trigger fires

| Trigger | Call these ETFs |
| VIX 1D > +20% **or** VIX > 25 | VIXY, VIXM, TAIL, TLT, HYG |
| UUP 1D \|Δ\| > 0.5% **or** FXY 1D \|Δ\| > 1% | UUP, FXY, SHY, TIP, RINF, IVOL, LQD, BKLN |
| GLD 1D \|Δ\| > 1.5% **or** USO 1D \|Δ\| > 2% | GLD, GDX, SLV, USO, CPER, MOO |
| ASHR or MCHI 1D \|Δ\| > 2% **or** major US–China policy news | ASHR, MCHI, EWY, DXJ, EWZ, CEW, EMB, EMLC |
| IBIT or WGMI 1D \|Δ\| > 5% | ETHA, DAPP, BLOK |
| Tier 1 theme confirmed but peers too thin | CIBR, BUG, DTCR, METV, GRID, XOP, AGNG, AIEQ, WELD, ROKT, BOAT, XRT, IBUY, MOAT, PSP, SIL, CPER |

VIX for Tier 3: user paste, or [FRED VIX Term Structure](sand-workflow:fred-vix-term-structure) / [Breadth Daily Report](sand-workflow:breadth-daily-report) — never invent.

## Gate

Need **at least 3–5** strong or weak ETFs before handing off. If the CSV cannot support that, say why and still list what passed. Only themes that actually moved (|1D|>1%) enter the parent Part 1 — quiet themes stay out (section contract).

When 1W/YTD columns exist, pass them through for parent theme rows; never invent.

## Output (internal)

For each theme cluster: name, tickers + 1D% (+1W/YTD if present), strong vs weak, which tier, which Tier 2/3 confirmers, **quoted X/N**. Cluster by the eight Tier 1 buckets.
