# Sector → primary ETF proxy (Scanner best-effort)

Static reference for [US Swing Sector Wind](sand-workflow:us-swing-sector-wind). Map stock GICS/industry (yfinance or known list) → **one primary liquid proxy**, then read that ticker’s Theme / RS from Dashboard.

| Stock sector / industry cue | Primary proxy | Typical Theme |
|----------------------------|---------------|---------------|
| Semiconductors / chip equip | SMH (alt SOXX) | P2 Hardware/Infra |
| Software / SaaS / cloud | IGV (alt CLOU, WCLD) | P7 Software/Cyber |
| Cybersecurity | BUG / CIBR | P7 Software/Cyber |
| Biotech / genomics | XBI (alt IBB) | P3 Biotech |
| Pharma / health providers | XLV | P5 Defensive (or P3 if pure biotech) |
| Internet / mega-cap tech | QQQ / XLK | P1 or P6 per name — prefer XLK/QQQ row Theme |
| AI / robotics / autonomy | BOTZ / IRBO / relevant P6 | P6 Frontier Tech |
| Defense / aerospace | ITA / PPA | L2 Defense |
| Energy / E&P / oil services | XLE / XOP | L2 Oil |
| Gold / miners | GLD / GDX | L2 Gold |
| Uranium / nuclear | URNM / NLR | L2 Nuclear |
| Lithium / battery materials | LIT | L2 Lithium |
| China / EM ADR heavy | MCHI / KWEB / EEM | L2 China/EM |
| Utilities / staples | XLU / XLP | P5 Defensive |
| Brokers / speculative retail | — | often P4 — use Neutral unless equity proxy clear |
| Crypto miners / pure crypto | IBIT/ETHA/BITQ | **exclude** → Neutral/N/A |

If unsure → `UNMAPPED` / `N/A`. Never invent a Theme label not on the sheet.
