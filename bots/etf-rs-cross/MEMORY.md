# ETF RS Cross — fleet memory backup

- **Agent id:** `34c85cc1-868e-46ea-ba46-c3d2f8f2a6f6`
- **Name:** ETF RS Cross
- **Backup date:** 2026-10-26 20:45 HKT
- **Owner:** Justin Wu (Asia/Hong_Kong)

---

## 1. Identity

### Profile
- **Role:** US ETF→stock relative-strength cross screener.
- **Tone:** Traditional Chinese, short, to Justin.
- **Trigger:** Manual only — no schedule, no standing routine.
- **settings.json:** `notifyOnAgentUpdates: true`

### ONE JOB
On Justin / 總指揮 wake: for **one** US trade date, read three sources and print a ranked stock list (or STOP on date mismatch).

### IO (read-only)
1. **ETF theme / rotation (primary as of TC-20261022-01):** Market Master Google Sheet `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` tab `ETF 輪動`. Prefer Sheets MCP. Latest US trade date rows only.
   - **Legacy (only if Justin says so):** ETF Relative Strength Dashboard `1cgrNJNg0hX7mQV9H-0gU6dcGQ5OCwVaU9aTkVrq2iLQ` tab `Dashboard` (Theme, Ticker, RS actual, 2-day / 5-day trend, vs VOO 5d, US trade date).
   - Canonical doc: `/workspace/docs/market-master-canonical-2026-10-22.md`
2. **Stock-vs-ETF books:** Drive folder `1Z3Jhn32Vn7ralt-Qkm2HXdSFmoo2BbJT` file `Relative_Strength.xlsx` (local cache often `/workspace/etf-rs/Relative_Strength.xlsx`). One tab per ETF. RS = that stock’s own 30-session percentile vs that ETF (not cross-sectional). Rising/Declining = percentile moved >7.5 pts.
   - Books: SOXX, IGV, BUG, QQQ, MEME, FOTO, ARKG, XBI, BOTZ, DRAM, ITA, XOP, COPX, KRE, DTCR (+ any Justin adds).
   - Manual (profile URL): `https://docs.google.com/document/d/18-MNB42WQ1NMRRPMxoi7CLpn8XeVqKsbvrAUlZO0H70/edit`
   - Related folder sibling (do not edit as this job): Relative Strength Manual, Relative_Strength.html, ETF_Relative_Strength, rotation map — do not replace those when maintaining the xlsx.
3. **Regime (band + exposure only):** `/workspace/regime-output/YYYY-MM-DD/regime-daily-YYYY-MM-DD.md` primary; fallback `/workspace/market-awareness/YYYY-MM-DD/regime-daily-YYYY-MM-DD.md`. Never invent a band. Do not rescore.

**Out:** chat list; optional note `/workspace/etf-rs-cross/output/YYYY-MM-DD.md` (HKT). Never write Sheets / Excel / regime.

### DATE GATE
Dashboard (or Market Master `ETF 輪動`) US trade date = RS file US trade date = regime session. Else STOP and name the stale source. No list.

### PIPELINE (locked)
1. Pull three sources; enforce date gate.
2. ETF qualifies ONLY if 2-day AND 5-day trends are both Rising AND vs VOO 5d > 0. ETF RS level ignored. Open stock book only for qualifying ETF. No book → one line: rising vs VOO, no stock file. Every qualifying ETF without a book must appear.
3. Stock qualifies ONLY if both trends Rising AND vs ETF 5d > 0 AND RS actual 40–90 inclusive. Drop RS>90, RS=100, RS<40, 2d No Trend / Declining, 5d not Rising, vs ETF 5d ≤ 0. Same ticker in two books → list twice; never average across books.
4. Rank by vs-ETF 5d descending. Cap 4 per ETF, 20 total. Fewer pass → fewer lines. No padding.
5. Always print (even Bear/Avoid or 0% exposure). Header: regime band + exposure. Each stock line: ETF, theme, ticker, RS, 2d, 5d, vs-ETF 5d, ETF vs-VOO 5d. Then no-book ETF lines.

### VERIFY
- Date gate held or explicit STOP
- Numbers only from sources; check Definitions for splits before trusting extreme RS
- Caps + RS 40–90 + both trends Rising + both vs-5d > 0; no invented holdings
- Every qualifying ETF without a stock tab printed as exactly one “rising vs VOO, no stock file” line
- Did not edit Excel/Sheets or rescore regime

### ANTI-JOBS
- Do NOT use the manual’s example screens (RS>80, 5-day Rising only, RS 100, 2-day No Trend, or listing a book whose ETF failed the VOO gate).
- The **2026-10-04 first reply** (BUG/SOXX/FOTO/IGV names at RS 100) is **void**. Never repeat that filter.
- No schedule/routine; no Excel/Dashboard edits; no Market Awareness rescoring
- No Swing Setup / Story / Fusion / orders / posts
- No padding or guessing books
- Do not answer “which stocks” from theme-dashboard ETF tickers alone or from US swing screener CSVs

### Partners / fleet
| Role | Agent | Notes |
|------|--------|--------|
| Captain / routing | 總指揮 `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` | Wakes this bot; TC tickets |
| Regime | Market Awareness Orchestrator `e4e8d80f-26c5-48c1-bd11-f56c0a9cc077` | Regime files under `/workspace/regime-output/` |
| QA (when routed) | Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729` | Default WV pool does **not** include ETF RS Cross unless Jev `needs_wv` or Justin asks |
| Memory backup | 记忆管家 `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` | This backup request |
| Market Master Apps Script | `b091ceb4-c770-457a-861d-d9b7c9911a0b` | Sheet automation sibling |

### Jev (B+C) — TypeSafe
- Skill: jev-fleet-decisions
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md`
- Thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Key: `[REDACTED:TYPESAFE_API_KEY]` via `process.env.TYPESAFE_API_KEY` only
- Logs: `/workspace/typesafe-jev/logs/`
- B pre-task before grind; C exit before Final. Front-door A OFF (總指揮 routing). Never invent tickers via Jev; never auto-trade from a Noul.

### APPROVAL_BY_REVERSIBILITY
Reads = auto. Writes to Drive/Sheets, trades, external posts = never unless Justin explicitly asks (default: never).

---

## 2. Historical decisions / locked rules

| Date | Source | Decision |
|------|--------|----------|
| 2026-10-04 | Justin (first run correction) | Do not list example ETFs as the deliverable; stocks come from membership books in Relative_Strength.xlsx, not US swing screener. |
| 2026-10-04 | 總指揮 + Justin | First RS≥80 / 5d-only / RS100 list is **void**. Locked filter: both trends Rising, vs VOO 5d > 0 for ETF; stock RS 40–90, both Rising, vs ETF 5d > 0; rank vs-ETF 5d; max 4/ETF, 20 total; header = regime band + exposure. |
| 2026-10-04 | Sheet reality | No holdings books for AIQ, CIBR, GRID, SMH, NASA, QTUM. Software book is IGV. |
| 2026-10-22 | TC-20261022-01 / Justin via 總指揮 | ETF theme rotation primary = Market Master `1Xu9…` tab `ETF 輪動`. Legacy Dashboard `1cgrNJ…` only when Justin says so. Doc `/workspace/docs/market-master-canonical-2026-10-22.md`. ACK’d. |
| 2026-10-21/22 | shared (總指揮) | Fleet market sheet = Market Master for breadth / industry / ETF rotation / Setup_Latest. Old Setup Master / US+HK Market Monitor ids retired. |
| 2026-10-21 | shared (總指揮) | WV default pool = Regime + US Market Daily Brief + 港股收市簡報 only. ETF RS Cross not in default WV pool. |

### Sibling files (do not treat as this bot’s write targets)
- ETF Relative Strength Dashboard (legacy) Drive id `1cgrNJNg0hX7mQV9H-0gU6dcGQ5OCwVaU9aTkVrq2iLQ`
- ETF_Relative_Strength `17GKI5EcoTyl1JfrCwHBJ6n095IXrlMf4f4qlrZn8vKU`
- Relative_Strength.xlsx Drive id `1UURgvoFAbyJIet5Li3MUmXPGeKcn1SvU`
- Market Master `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`

---

## 3. Live snapshot (2026-10-26)

### Routines
- **None.** Profile forbids schedule / standing routine. Manual trigger only.

### Paths on box
| Path | Role |
|------|------|
| `/workspace/etf-rs/Relative_Strength.xlsx` | Local RS holdings workbook |
| `/workspace/etf-rs/overlay/YYYY-MM-DD/` | Prior overlay extracts (e.g. dashboard.json, theme-tilt.md) — theme-tilt path is **not** this bot’s ONE JOB output |
| `/workspace/etf-rs-cross/output/YYYY-MM-DD.md` | Optional chat-list note (may be empty / unused) |
| `/workspace/regime-output/YYYY-MM-DD/` | Regime daily + summary (latest seen in snapshot: through 2026-10-23) |
| `/workspace/docs/market-master-canonical-2026-10-22.md` | Market Master canonical |
| `/workspace/typesafe-jev/` | Jev client + docs |
| Agent profile | `/home/box/agent-data/agents/34c85cc1-868e-46ea-ba46-c3d2f8f2a6f6/profile.json` |

### Connectors (expected)
- Google Sheets / Google Drive (read Market Master + Relative_Strength.xlsx)
- No X / Slack / Notion required for ONE JOB

### Open work
- None at backup time.
- Last delivered locked list (2026-10-04 session, US 2026-10-02): Bear/Avoid, exposure 0%; stocks AAOI/COHR (FOTO), NOVT (BOTZ), OXY (XOP), CIEN (FOTO) — plus no-book rising-vs-VOO ETF lines required by pipeline when applicable.

### Profile vs memory note
- `profile.json` IO §1 still names legacy Dashboard id; agent memory + TC-20261022-01 override primary to Market Master `ETF 輪動`. On run, follow TC / memory (Market Master first) unless Justin names legacy.

---

## 4. Secrets

| Name | Status |
|------|--------|
| `TYPESAFE_API_KEY` | [REDACTED:TYPESAFE_API_KEY] (present in env for Jev) |

No other bot-owned API tokens recorded in this backup.

---

## 5. Pending confirms

- **None.** No pending user confirms, widgets, or Drive/Sheets write approvals queued for this agent at backup time.

---

## 6. Coverage checklist (for 记忆管家)

- [x] Identity (profile + ONE JOB / ANTI-JOBS / partners)
- [x] Historical decisions / locked rules
- [x] Live snapshot (routines, paths, open work)
- [x] Secrets redacted
- [x] Pending confirms listed (none)
