---
name: HK IPO research
description: >-
  Use when the user asks for current Hong Kong IPOs, a 今期招股 list, or a full or
  single-stage research note on one HK listing, for 打新.
---
# HK IPO research

Public-web only. No local scripts, no login, no broker API.

Not investment advice. Say that at the end of every note. Write the note in 繁體中文.

Runner is Researchy.

## When to run

- 今期招股, or a request to list coming IPOs: build the calendar, then a full report for each name on it.
- One stock code or company name: full report for that name only.
- If the user names one stage, run only that stage. The company brief still goes in, unless Justin says skip the brief.

## Calendar

Start at [HKEJ Stock360 IPO](https://stock360.hkej.com/IPO).

Cross-check each name against:

- TradeSmart IPO Tracker: https://lowrisktradesmart.org/en/tools/ipo-tracker
- AAStocks IPO: http://www.aastocks.com/tc/stocks/market/ipo/
- HKEXnews: https://www.hkexnews.hk

A name on HKEJ goes on the list. A name missing on HKEJ but present on TradeSmart, AAStocks, or HKEXnews still gets a row: HKEJ 沒有、見於 X. Do not omit it.

If the same field differs, list every figure and say which source is the newest. 不要取平均. Do not pick one figure and call it official.

## Company brief (required)

Before the four stages, write:

- 簡介: what the company is, in a few sentences, from the prospectus.
- 業務: what it sells, to whom, and where the money comes from. Cite the prospectus page.
- 可比公司: always give your own estimate of listed peers in Hong Kong and the US. Prospectuses usually hide peers as Company A, B, C and do not name tickers. Do not stop there. Name the tickers, say why each is comparable (same product, same customer, or same business model), and label the list 自行估計，非招股書. Say when no close peer exists. Do not force a match.

## Full report (four stages)

1. Prospectus. HKEXnews prospectus, with page citations. This is the primary source for offer terms, use of proceeds, and risks. Search `site:hkexnews.hk {company} 招股章程`.
2. Sponsor record. Search etnet `site:etnet.com.hk {sponsor} 保薦人` and jisilu `site:jisilu.cn {sponsor} 保荐`. Cite the page you actually opened. If the search returns nothing, say so.
3. Aggregate margin, grey market, and A+H, from https://lowrisktradesmart.org/en/tools/ipo-tracker then http://www.aastocks.com/tc/stocks/market/ipo/ then https://www.hkexnews.hk. If a page is down or has no number, write that the source has nothing. Do not fill the gap from a news article.
4. Per-broker margin and news ratings. Allowed to be incomplete. For each missing broker or rating write 此來源沒有. A missing stage 4 still counts as a finished report. Do not invent a broker table.

## 打新 read (suggestion, not an order)

倍數分檔是建議，不是指令. Use the oversubscription multiple from the cross-check, and show the band. Where a band names two labels, report both and do not pick one. State which source's multiple you used.

- Above 1,000×: 甲尾
- 200–1,000×: 甲尾 and 乙頭
- 50–200×: 甲尾 and 乙頭, depending on cash
- 10–50×: one board lot
- Below 10×: skip, or one board lot only as a probe

## File

On the shared computer, save one markdown file per IPO at `/workspace/hk-ipo/{code}-{date}.md`. `{code}` is the 5-digit HK code. `{date}` is the research date in HKT as YYYYMMDD (example `09688-20261005.md`). In Grok, where that folder does not exist, put the same markdown in the reply.

In Grok Bot chat, give the file path and a short summary. Do not paste the whole note unless the user asks to copy it.

## Self-check

Before you finish, confirm each line. This is not a second reviewer.

- The note is 繁體中文, and the disclaimer is present.
- Every disagreement is listed and not averaged.
- Every missing stage-4 source says 此來源沒有.
- HK and US comps are your own estimate, labeled 自行估計，非招股書, or the note says none and why.
- Grok Bot delivered the file path, or Grok delivered the full markdown.
