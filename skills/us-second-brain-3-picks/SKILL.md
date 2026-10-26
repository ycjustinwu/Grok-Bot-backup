---
name: US second-brain 3 picks
description: >-
  Use when running Justin’s US second-brain attention stack (scanner handoff,
  reverse/deep-PB dig, or on demand): aggregate regime + US brief + Monitor + RS
  + Setup + Stockbee 50 into ≤3 stalk names, then a ≤10 min X dig; after the
  shortlist, run US swing session overview for the same session.
---

> **Canonical (2026-10-22):** Market Master `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` — tabs 美股市寬／港股市寬／ETF 輪動／形態篩選／Setup_Latest. Doc: `/workspace/docs/market-master-canonical-2026-10-22.md`.
# US second-brain 3 picks

ONE JOB: Build Justin’s daily US attention shortlist (≤3 names) from the required doc stack, then a short X dig to stress-test. Discussion with Justin happens in the **Second brain** bot chat.

Not advice. Stalk / observe framing. Deep Bear = probe-only mindset until exposure >0% — still hunt gems.

Default trigger: **US Swing Scanner handoff** (noon cron paused). On no-scanner / bad-tape days, may run reverse/deep-PB dig when Justin/總指揮 asks.

## Required sources (all must be present + fresh for the session date)

1. **Regime** — latest Market Awareness / regime-daily for the US close being traded (usually prior session).
2. **US Market Daily Brief** — Final for that close.
3. **Market Master · 美股市寬／美股行業** — id `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` (ex-US Market Monitor)
4. **ETF/ticker RS** sheet — id `1QXQAHFL8bp-N4QN0D9Iwu2hVzN1n6AXY` (native RS; keep)
5. **Market Master · ETF 輪動** — same id `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` (prefer over legacy RS full pic `1cgrNJ…` unless Justin says otherwise)
6. **Market Master · Setup_Latest／形態篩選** — same id (ex-Setup Master)
7. **Stockbee 50 Momentum** — Drive folder `1Fw2IfpQupYCrTtQTZMymt7VdjQnDWJv3` — **required every run** (latest 熱度圖 / analysis doc). Momentum interlinks for longs and short timing. Do **not** sync that folder to Notion.

When scanner handoff exists, screener BUY/STALK is the **primary pool**; marked off-screener still OK.

If any of the seven core sources is missing or stale for the target close → **stop**. Tell Justin what is missing. Do not invent fills.

Research order: Google Sheets MCP → Tavily → Firecrawl → Browser Use → box desktop last. Prefer TradingView MCP for technicals on stalk candidates (OHLCV, technicals rating, symbol data). Skip Browserless / Finance.

## Selection bar

- Open-minded: **no hard veto / always-watch list**.
- Swing bar: **high ATR + strong risk-reward**. Skip weak RR even if the story is cute.
- **Growth bias** when two names are otherwise equal.
- Hold horizon: **~2 weeks max** unless Justin explicitly marks a homerun.
- Multi-source agreement preferred (regime theme + brief + Monitor + RS + Setup + Stockbee). One lonely signal is not enough.
- Up to **3** attention names. Fewer is fine. If none clear the bar → say **cannot find** — do **not** force 3.
- **No-repeat** vs prior Second-brain days’ tickers (check prior run notes under `/workspace/second-brain/`).
- Deep Bear / DEEP DEFENSIVE / 0% exposure = harder tape + higher failure rate, **not** “no longs”. Still hunt ECO/TNK-style gems when the stack supports them. Frame as attention/stalk, not size-up buys.

## Regime = reference, not rigid gate

- Always **read** regime (Focus Long / Focus Short / excess / ETF RS overlay) and use it as context.
- Do **not** veto a name solely because Focus Long is empty or the name’s pillar isn’t a Focus Long theme — hard tape still has gems.
- Do **not** upgrade stalk → size on story alone when regime gives no long-theme cover; keep exposure framing honest.
- Soft concentration guard: when Focus Long is empty, prefer **≤2 of 3** in the same pillar / same P# cluster. A third same-theme name needs an explicit *theme-echo / lower priority* label or a clear idiosyncratic reason.

## Stockbee + short timing

- Read the **latest** 熱度圖 every run (Fresh / Sustained / underlying heat via levered ETFs / Fading).
- Use it to **interlink** momentum with the six other sources — not as a standalone long or short list.
- **Shorts:** if regime Focus Short / Short focus already flagged a sleeve for a while (e.g. P6 Frontier), late Stockbee inverse-ETF heat on those names is usually **too late to initiate** — treat as confirmation noise / crowded after-move, not a fresh short signal. Prefer early regime Short focus + breakdown structure over chasing heat after the fact.
- Levered-ETF heat is noisy; map to underlyings and cross-check TV + regime before naming a short stalk.

## Mandatory reflection (every pick, every run)

Before locking the list, answer in the note (short, plain):

1. **Better candidates?** — Did the stack surface stronger names outside this cluster? Why not them?
2. **Market focus now?** — What is actually leading / flowing today (sectors, factors, leaders), not what was strong last week?
3. **Timing?** — Is this the right window, or are these leaders **last men standing** (relative strength while the tape rolls)? For shorts: is Stockbee heat early or late vs regime Short focus?
4. **Why this ticker vs the big trend?** — What is *specific* (setup, earnings path, RS vs peers, volume character, catalyst) that lets it hold up if the broad trend is hostile?
5. **Evidence conflict?** — If high-RS sector ETFs are dual-decline / “leaders may roll,” treat that RS as **rollover risk**, not a green light to pile a third name into the same cluster.

Learn from critiques day by day; fold sharp points into the next run’s reflection, not into rigid new vetoes.

## Output shape (every run)

Lead with tape one-liner (regime label + exposure cue + what’s working / dying).

Brief **Stockbee read** (1–3 lines: heat leaders, any short-heat late vs regime).

Then for each pick (1–3):
- Ticker — name
- Why (plain: which sources agree)
- **Why vs big trend** (one line from reflection #4)
- Levels / invalidation in short form when known
- Earnings date if near
- Stalk note (don’t chase / wait pullback / observe proxy)

Include a short **Reflection** block covering better candidates / market focus / timing / last-man-standing.

Deferred section optional (e.g. Setup #1 skipped for weak RR).

End with **What I can dig on X** (≤7 concrete dig lines). Then run digs.

Save a dated note: `/workspace/second-brain/YYYY-MM-DD/attention-3-picks.md` (include tickers for no-repeat).

After Final: run [US second-brain Notion sync](sand-workflow:us-second-brain-notion-sync) — picks → **US Attention Picks** DB; overview → parent **US Swing Overviews** (`3fc77383-f89c-8163-b6d6-f89308b737af`). Skip Notion when the active TC says Second brain must not Notion.

## After shortlist → session overview

Same session (after stalks file is saved, before or after X dig is fine; prefer after stalks are locked):

Run skill [US swing session overview](sand-workflow:us-swing-session-overview) for the **same YYYY-MM-DD**. That page is the full-picture one-pager (conflicts first; regime reference only; Brief conflict-only). Do not skip unless Justin says so.

## X dig

- Cap **≤10 minutes** wall clock, then deliver what you have.
- Prefer public X reads; filter cashtag spam.
- Goal: confirm / kill the tape story and each name (flows, earnings tone, theme leadership persistence, last-man-standing risk).
- After dig: short update under the picks — what strengthened, what weakened. Not a raw feed.

## Discussion mode

When Justin replies in this chat, stay on the shortlist: levels, invalidation, alternate names, X follow-ups. Do not expand into HK briefs, scanner runs, or motion HTML unless he asks.

## Anti-jobs

- Not a scanner (that’s US Swing Scanner).
- Not Setup writer (美股 Swing Setup).
- Not regime author (Market Awareness).
- Not US brief author (US Market Daily Brief).
- Do not post to X or trade.
