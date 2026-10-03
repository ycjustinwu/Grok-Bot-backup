# Memory disaster-recovery backup — 港股收市簡報
- Agent name: 港股收市簡報
- Agent id: b9d6b823-8ae3-46a7-bc08-9beb4a35c631
- ServerId: 2410898
- Snapshot time: 2026-09-14 (HKT)
- Backup path: `/workspace/2410898-memory-backup.md`

## Identity
- Role: Hong Kong / Greater China equities research analyst producing daily **港股收市後簡報** for experienced trader Justin Wu.
- Language: **全部輸出必須繁體中文**.
- Session close 16:00 HKT; target delivery ~16:30 HKT (routine historically 18:00 HKT weekdays).
- Title chip: (empty in profile.json); avatarShape pebble; avatarColor orange; namedBy user; harness box.
- Primary skills: `hk-after-close-brief`, `hk-unusual-movers`, `hk-catalyst-research`, `hk-sector-rotation`, `hk-market-alerts` (+ Market Monitor CUP section).
- Orchestration order: Unusual Movers → Catalyst／三大頭條 → Sector Rotation → 個股顯著異動 → Market Alerts／北水 → Market Monitor → assemble Markdown (skip empty sections).
- Unusual-movers gates: 市值≥100億、|Δ|≥5%、成交≥20日均量2倍; mega-caps noise filter unless |Δ|>3%.
- Anti-jobs: no fluff emotion paragraphs; don’t list all 11 sectors if quiet; never invent catalysts/prices; **no default PDF**.

## Historical decisions
- (2026-09-07) Discovery sources locked: HKEJ Stock360 Industry + Spot; verify on HKEX / AAStocks / Yahoo Finance HK.
- (2026-09-07) Justin may supply TradingView abnormal rise/drop (CSV/screenshot/paste) as discovery seed only — still verify.
- (2026-09-07) Export iteration: docx → pptx → Kami PDF; built `/workspace/tools/kami_md2pdf.py` (Kami parchment / ink-blue / 倉耳今楷) for fast MD→PDF.
- (2026-09-08) Filename pattern: `HK brief-YYYY-MM-DD.md` (and `.pdf` when requested) under `/workspace/hk-brief-inputs/YYYY-MM-DD/`.
- (2026-09-08) Stock Connect 北水: **HKEX Mutual Market Historical Daily (zh-HK) only**; include major/active southbound (+ material northbound). Do not trust unverified third-party net figures as authority.
- (2026-09-08) Added **五、Market Monitor（CUP）** from Google Sheet fileId `1yIZLgTIqq38i_fK-q5oBWFogk0OCH1WuZ9a6AiAP8WI` — mirror Market Awareness Orchestrator US CUP playbook (Summary/History/Sector/Industry only; Up4/Down4, SMA20/50, MLI n/%/升%, Top3 Sector + Top5 Industry; side-channel not a second score; flag MLI升%<~40% when indices strong; HK filters Price≥1 HKD Vol≥300k). Do not redo 2026-09-08 brief solely for this addition.
- (2026-09-08) After switching 北水 to HKEX for that day, **do not re-run** 2026-09-08 brief.
- (2026-09-09) **Delivery lock (token save)**: Markdown only by default — path `/workspace/hk-brief-inputs/YYYY-MM-DD/HK brief-YYYY-MM-DD.md`; **do not** run Kami/WeasyPrint/PDF unless Justin explicitly asks that day; chat deliver 繁中 body and/or MD path. JD + skill + cron prompt aligned (TC-20260909-18).
- (2026-09-09) Routine cron prompt updated for MD-only; remains **paused** (`enabled: false`), schedule `0 18 * * 1-5`.
- (2026-09-09) Re-ran brief with Justin extra movers seed (`justin-extra-movers.md`); Work Verifier routed via 總指揮.
- (2026-09-10) Ran session brief with Justin TV movers CSV + Market Monitor (today’s Summary existed); southbound net derived from HKEX buy−sell splits when page lacks net column.
- (2026-09-14) Sweeper asked to append stay-quiet-on-empty clause to paused routine; applied via update_state (keep schedule + paused).

## Live snapshot
### Profile (durable)
- Primary discovery: HKEJ Stock360 Industry `https://stock360.hkej.com/marketWatch/Industry` + Spot `https://stock360.hkej.com/marketWatch/Spot`.
- Optional TV abnormal discovery from Justin; always verify.
- Filenames: `HK brief-YYYY-MM-DD` under `/workspace/hk-brief-inputs/YYYY-MM-DD/`.
- 北水: HKEX Historical Daily zh-HK only.
- Market Monitor sheet: `https://docs.google.com/spreadsheets/d/1yIZLgTIqq38i_fK-q5oBWFogk0OCH1WuZ9a6AiAP8WI/edit` (fileId `1yIZLgTIqq38i_fK-q5oBWFogk0OCH1WuZ9a6AiAP8WI`); CUP playbook as above.

### Log highlights (2026-09)
- kami_md2pdf.py tooling exists; PDF was preferred early then locked off by default.
- 2026-09-08: TV CSVs staged at day’s folder for 18:00 run.
- 2026-09-09: Spot OCR/screenshot at `stock360-spot.png`; Industry/stock subpage blank; Monitor missing 09-09 row that day; `hkex-connect.md` saved (NB buy/sell splits often unavailable on page).
- Recent deliverables dirs: `/workspace/hk-brief-inputs/2026-09-07|08|09|10/` with MD (+ legacy PDF on some days).

### Routine — 港股收市後簡報
- Folder: `automation-1788788112710`
- Schedule: `0 18 * * 1-5` (weekdays 18:00 HKT)
- Status: **paused** (`enabled: false`)
- Last known successful run (automation_status): 2026-09-09 ~18:25 HKT
- Prompt intent (as of this snapshot): run after-close skill; HKEJ + TV CSVs + HKEX 北水 + Market Monitor sheet; MD only path; no PDF unless asked; deliver 繁中 to Justin; no invented numbers; **If markets are closed (HK holiday) or there is no usable session data for a brief, stay quiet — do not send filler like "(no change.)" or an empty brief.**

### Connectors / tools (no secrets)
- Google Drive MCP (`user-Google-drive`) used for Market Monitor sheet read — OAuth via Cursor account; no bot-stored token.
- Yahoo Finance public chart API used for price/volume verify when HKEX API absent.
- Box browser / computerUse for Stock360 + HKEX pages.

### Teammate routing (operational)
- 總指揮 (7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4): task tickets TC-*; Work Verifier handoff.
- Work Verifier (037de516-dbc1-4565-a127-5dbb0f691729): second-pass on high-stakes briefs.
- Sweeper / 清道夫 (8dbca7e8-e0d0-4447-821a-f9a3ad9d7e06): quiet-on-empty / token hygiene.
- 记忆管家 (bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed): this backup.

## Secrets placeholders only
- Google Drive / Google account OAuth: `[REDACTED:google-oauth]`
- Any Yahoo/HKEX session cookies if present in box browser: `[REDACTED:box-browser-cookies]`
- No API keys intentionally stored in this agent’s memory files.
- Market Monitor sheet is Drive-linked (fileId public in memory); access depends on Justin’s connected Google account: `[REDACTED:google-drive-access]`

## Coverage notes
- Included: identity/JD, profile facts, Sept log, routine schedule/status/prompt, delivery locks, key paths, teammate ids, secret placeholders.
- Not included: full chat transcripts, raw Yahoo dumps, PDF binaries, real tokens.
- Pending confirms: none for this backup write; routine quiet-clause update applied same session (still paused — resume only if Justin/總指揮 asks).
