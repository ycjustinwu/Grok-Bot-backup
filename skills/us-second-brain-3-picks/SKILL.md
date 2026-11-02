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
4. **ETF/ticker RS** sheet — native Google Sheet `1D3BrzLH3DmxX8Gv3W9Yhvd9q_LNOGXyNyUzjnXzqmHk` (**Relative_Strength**, Justin 2026-11-02 native). Primary tabs: `📊 RS 總覽` · `Screen` · `Scores` · `Turning` · `ETF_Candidates` · `Run_Status` · per-ETF books · `Map`. Use Joint **J** / Sector **S** / Stock **K** / Top+Improvers; soft-go only if Sheets API fails.
5. **Market Master · ETF 輪動** — same id `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` (prefer over legacy RS full pic `1cgrNJ…` unless Justin says otherwise)
6. **Market Master · Setup_Latest／形態篩選** — same id (ex-Setup Master)
7. **Stockbee 50 Momentum** — Drive folder `1Fw2IfpQupYCrTtQTZMymt7VdjQnDWJv3` — **required every run** (latest 熱度圖 / analysis doc). Momentum interlinks for longs and short timing. Do **not** sync that folder to Notion.

When scanner handoff exists, screener BUY/STALK is the **primary pool**; marked off-screener still OK.

**形態篩選 overlap (Justin 2026-10-30):** Cross Market Master tab **形態篩選** for **TC Deep** and **CB** rows vs the scanner handoff ticker set. Overlap = plus (prefer / soft score boost when otherwise close). If overlap exists but the name is not stalked, still leave a short **remark** so Justin sees it. Silent when no overlap.

If any of the seven core sources is missing or stale for the target close → **stop**. Tell Justin what is missing. Do not invent fills.

Research order: Google Sheets MCP → Tavily → Firecrawl → Browser Use → box desktop last. Prefer TradingView MCP for technicals on stalk candidates (OHLCV, technicals rating, symbol data). Skip Browserless / Finance.

## Selection bar

- Open-minded: **no hard veto / always-watch list**.
- Swing bar: **high ATR + strong risk-reward**. Prefer strong RR; imperfect RR can still stalk with an explicit **smaller-bet / size-down** flag (chase OK on thrust windows — do not auto-kill solely on soft Adj RR).
- **Do not** force an **Extended** / soft-RR name into the ≤3 just because it is the only rising-RS STALK (RDWR lesson 2026-10-29). Prefer fewer stalks; park Extended soft-RR in Setup remarks / digest-watch.
- **Tape mode — identify thrust vs pullback climate (every run):**
  - If momentum is **gaining** or the tape shows a **market thrust** / easy-money stretch (breadth thrust, clustered leaders ripping, Stockbee Fresh heat + rising RS leaders): default **pullback-buy is less effective**. Prefer earlier attention on true momentum names (rising RS + structure still alive) with honest size — **not FOMO size**, but more aggressive than wait-for-digest. Name what is working even when it conflicts with the classic pullback framework. Easy-money tape can exist for a while.
  - If tape is choppy / Cautious / leaders Extended without fresh thrust: keep digests/pullback framing.
  - Keep climate judgment **silent in the framework**; mention thrust/hard-penny in the note **only when it materially changes** the stalk call (not every run).
  - Climate = **judgment aided by Market Awareness / regime**, not a fixed tag. Easy-money vs hard-penny is hard to label early.
  - **Cupsir cue (live feedback):** if recent identified setups keep failing / stop-outs come easy → lean **hard-penny** (tighter bar, fewer stalks, digests OK). If setups hold and work → lean **easier momentum** (earlier attention OK). Vice versa. Note this in reflection when sim/book feedback is available.
- **Growth bias** when two names are otherwise equal.
- Hold horizon: **~2 weeks max** unless Justin explicitly marks a homerun.
- Multi-source agreement preferred (regime theme + brief + Monitor + RS + Setup + Stockbee). One lonely signal is not enough.
- Up to **3** attention names. Fewer is fine. If none clear the bar → say **cannot find** — do **not** force 3.
- **Capital scarcity / can’t-miss (W44 patch):** default **0–2** stalks; empty OK. Raise bar to can’t-miss / really good only — never pad-to-3 with merely-OK. Skip soft fills so cash isn’t locked when a true A+ appears.
- **No Soft Final void** without Justin/總指揮 **AUTHORIZE**; one Final per bar-date (W44 Soft void churn lesson).
- **Crowding gate (2026-11-01):** if sim book ≥5/7 open or cash thin, only stalk if Adj RR clears **and** price isn’t already ≥5% away from a sane entry — else Setup remarks / observe.
- **Fillable-or-don’t-stalk (W44 #2/#6):** if preferred digest/limit is already ≥5% away from close, remarks/observe only — **do not** count as a stalk. Soft Final each pick must show one line **L / SL / away check**; **demote** if away fails or L≈SL (CRWD open-on-stop lesson).
- **One chase window:** do not re-stalk the same CRWD-class leader across ~3 sessions without a fresh pullback + size-down.
- **No-repeat** vs prior Second-brain days’ tickers (check prior run notes under `/workspace/second-brain/`). Window is ~1–2 days; older priors may be reassessed.
- Deep Bear / DEEP DEFENSIVE / 0% exposure = harder tape + higher failure rate, **not** “no longs”. Still hunt ECO/TNK-style gems when the stack supports them. Frame as attention/stalk, not size-up buys.

## Regime = reference, not rigid gate

- Always **read** regime (Focus Long / Focus Short / excess / ETF RS overlay) and use it as context.
- Do **not** veto a name solely because Focus Long is empty or the name’s pillar isn’t a Focus Long theme — hard tape still has gems.
- Do **not** upgrade stalk → size on story alone when regime gives no long-theme cover; keep exposure framing honest.
- Soft concentration guard: when Focus Long is empty, prefer **≤2 of 3** in the same pillar / same P# cluster. A third same-theme name needs an explicit *theme-echo / lower priority* label or a clear idiosyncratic reason.

## Stockbee + short timing

- Read the **latest** 熱度圖 every run (Fresh / Sustained / underlying heat via levered ETFs / Fading).
- Use it to **interlink** momentum with the six other sources — not as a standalone long or short list.
- On thrust days, Fresh/Sustained heat + rising RS leaders are primary evidence for the momentum climate call above.
- **Shorts:** if regime Focus Short / Short focus already flagged a sleeve for a while (e.g. P6 Frontier), late Stockbee inverse-ETF heat on those names is usually **too late to initiate** — treat as confirmation noise / crowded after-move, not a fresh short signal. Prefer early regime Short focus + breakdown structure over chasing heat after the fact.
- Levered-ETF heat is noisy; map to underlyings and cross-check TV + regime before naming a short stalk.

## Mandatory reflection (every pick, every run)

Before locking the list, answer in the note (short, plain):

1. **Better candidates?** — Did the stack surface stronger names outside this cluster? Why not them?
2. **Market focus now?** — What is actually leading / flowing today (sectors, factors, leaders), not what was strong last week?
3. **Timing?** — Thrust vs pullback climate? Is this the right window, or are these leaders **last men standing** (relative strength while the tape rolls)? For shorts: is Stockbee heat early or late vs regime Short focus?
4. **Why this ticker vs the big trend?** — What is *specific* (setup, earnings path, RS vs peers, volume character, catalyst) that lets it hold up if the broad trend is hostile?
5. **Evidence conflict?** — If high-RS sector ETFs are dual-decline / “leaders may roll,” treat that RS as **rollover risk**, not a green light to pile a third name into the same cluster.

Learn from critiques day by day; fold sharp points into the next run’s reflection, not into rigid new vetoes.

## Output shape (every run)

Lead with tape one-liner (regime label + exposure cue + what’s working / dying). Add thrust/hard-penny **only if applicable**.

Brief **Stockbee read** (1–3 lines: heat leaders, any short-heat late vs regime).

Then for each pick (1–3):
- Ticker — name
- Why (plain: which sources agree)
- **Why vs big trend** (one line from reflection #4)
- Levels / invalidation in short form when known
- Earnings date if near
- Stalk note — apply thrust vs pullback framing in the pick itself when it matters; if Adj RR imperfect, say **smaller-bet**. Don’t boilerplate climate labels every run.

Include a short **Reflection** block covering better candidates / market focus / timing / last-man-standing.

Deferred section optional (e.g. Setup #1 skipped for weak RR).

**Soft Final entry QA (every stalk):** one line each — preferred **L** · **SL** · **away vs close** (%). Fail away or L≈SL → demote to Setup remarks before locking the list.

**Setup candidates (remarks — every run):** After Deferred, add a short block **Other Potential → 美股 Swing Setup?** listing 2–5 non-stalk (or imperfect-RR) names Justin may want to send to Setup for a deeper structure pass. One line each: ticker · why Setup might help (rising RS / Setup_Latest score / structure / earnings path) · why not stalked here (RR / caution / soft-cap / theme / Extended). Do **not** auto-run Setup or message Setup bot — remarks only so he can decide.

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

When Justin replies in this chat, stay on the shortlist: levels, invalidation, alternate names, X follow-ups. Do not expand into HK briefs, scanners, or motion HTML unless he asks.

## Anti-jobs

- Not a scanner (that’s US Swing Scanner).
- Not Setup writer (美股 Swing Setup) — remarks for Setup candidates only; never auto-run Setup.
- Not regime author (Market Awareness).
- Not US brief author (US Market Daily Brief).
- Do not post to X or trade.
