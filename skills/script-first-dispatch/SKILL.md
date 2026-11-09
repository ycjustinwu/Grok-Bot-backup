---
name: script-first-dispatch
description: Use before any browser, Computer Use, scrape, page-read, or fetch — and when designing bot steps: Connector then Script then Browser Script then Computer Use; write a reusable script when the job is structured or will repeat.
---

# Script-first dispatch

Fleet hard rule (Justin 2026-11-02). Source: https://x.com/heydengai/status/2117046781594980637
Full doc: `/workspace/docs/script-first-dispatch-2026-11-02.md`

## Benchmark (same page fetch)
- Computer Use ~213K tokens
- Browser + Script ~51K (~76% less)
- Pure script: 0 model tokens at execute

## Ladder (cheapest first)
1. Connector / MCP (Sheets, Drive, TradingView, Notion, Tavily, Firecrawl, OpenMarket, X, etc.)
2. Script (curl / CLI / Python / Node; write and save under `/workspace` when repeating)
3. Browser Script (Playwright / Browserless / Firecrawl interact / Browser-use as API — not visual click loops)
4. Computer Use last only: login UI, captcha after script fail, GUI with no API/DOM, or user explicitly asks

## Before browser or desktop
1. Name the outcome.
2. Try connector.
3. If public or structured: write or reuse a script; persist path in Soft Final.
4. Then Browser Script; then Computer Use.
5. Soft Final states which rung ran and why any higher rung failed.

## Principles
- Model decides; code executes.
- Prefer MCP over box browser for market briefs.
- Escalate one rung with a one-line reason; no silent jump to Computer Use.

## Anti-jobs
- No acting human on a page for fetch/scrape/read.
- No Computer Use for convenience.
- Scripts still read live sources; never invent numbers.
