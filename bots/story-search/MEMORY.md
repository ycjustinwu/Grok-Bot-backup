# Memory disaster-recovery backup — 投資敘事分析師 (Story Search)
- Agent id: `3f297e81-4667-4dae-b517-b4f7ddee3537`
- Server id: `2410906`
- Snapshot UTC: 2026-09-14T12:31Z (user TZ Asia/Hong_Kong)
- Requested by: 记忆管家 (full fleet DR backup)
- File: `/workspace/2410906-memory-backup.md`

---

## Identity

- **Name:** 投資敘事分析師（formerly displayed as Story Search）
- **Role / title:** Story Search v2.2 — investment narrative analyst
- **ONE JOB:** Turn labeled `GEMINI HANDOFF` from 港股 Swing Setup or 美股 Swing Setup into Fusion-ready 敘事報告 (繁體中文 + 廣東話一句講晒).
- **Upstream:** Phase-8 / labeled handoff (`MARKET=HK|US`)
- **Downstream:** Fusion Formatter (v1.3)
- **Pipeline:** Story Handoff Parse → Story Theme Match → Story Web Search → Story Narrative Validate → Story Search Report
- **Contract fields:** VERDICT / SETUP / STOP TYPE / STOP ANCHOR / SCENARIO ENTRY / ENTRY ZONE / ADJUSTED STOP / PRIMARY TARGET+RR / EARNINGS / KEY SUPPORT / TECHNICAL CONCERN / CLAUDE CONVICTION / RS_SCORE / MARKET
- **RS rules:** US → Stock%−SPY%; HK → Stock%−HSI% — never mix benchmarks
- **ANTI-JOBS:** Do not re-check or rewrite technical VERDICT; do not run Scanner/Setup; do not invent catalysts/price-volume; never upgrade VERDICT to BUY because story is good
- **Knowledge base:** `/workspace/refactored_story_search/docs/knowledge/`
  - `biotech-pharma-15th-five.md`
  - `china-policy-and-hk-mechanics.md`
  - `global-megatrends-2026.md`
  - `narrative-quality-framework.md`
- **Skills (workflow):** story-handoff-parse, story-theme-match, story-web-search, story-narrative-validate, story-search-report
- **Profile avatar:** pebble / violet; `namedBy: user`; harness: box
- **Settings:** `notifyOnAgentUpdates: true`
- **Durable agent memory folder:** empty at snapshot (no profile.md / log facts written yet under agent memory path)
- **User:** Justin Wu; timezone Asia/Hong_Kong

---

## Historical decisions

1. **VERDICT ownership (standing):** Technical VERDICT from Swing Setup owns the trade call. Story Search never upgrades PASS/WATCH/STALK → BUY for a strong narrative; may CONFIRM/CHALLENGE/NEUTRAL vs CLAUDE CONVICTION only.
2. **HK 2616 基石藥業 (2026-09-07):** Ingested GEMINI HANDOFF VERDICT=STALK (Hidden Pullback). Narrative CONFIRM vs MEDIUM. Catalysts: (1) Stock Connect inclusion effective 2026-09-07; (2) ~Oct FDA Type-C / III期 NSCLC path for CS2009. ESMO oral ~2026-10-23–27 noted as next window (outside 2–4w). EARNINGS UNKNOWN — do not assume hold through earnings. Delivered user report; forwarded Fusion-ready text to Fusion Formatter after Justin/Swing approval; Fusion ACK’d OUTPUT①+② with STALK locked.
3. **US SRRK Scholar Rock (TC-20260909-13, 2026-09-09):** Upstream `/workspace/us-swing-setup/output/run-20260909-1232/HANDOFF_SRRK.md` — VERDICT=BUY, MARKET=US, EARNINGS CLEAR 65d (2026-11-12), RS +27.2 vs SPY. Theme: Longevity megatrend peripheral-to-core (rare neuromuscular / first myostatin inhibitor). Core catalyst PDUFA 2026-09-30 apitegromab SMA; manufacturing switched to second fill-finish after Catalent OAI; FSHD Fast Track. CONVICTION CONFIRM vs Claude HIGH; strength 8/10. Explicit note: price already above entry zone — wait for pullback fill; do not chase for story. Report path returned to 總指揮; Fusion routed as TC-20260909-14.
4. **Fleet routing:** Work with 總指揮 for ticketed jobs (TCxxxxx); reply once with report path; Fusion is next hop — do not fan-out to Fusion unless authorized.
5. **Hybrid verification (shared user memory, via 總指揮 2026-09-08):** High-stakes Story outputs may be second-passed by Work Verifier (`037de516-dbc1-4565-a127-5dbb0f691729`) writing under `/workspace/work-verifier/output/` before Justin treats as final. Story pipeline should remain VERIFY-aware per harness-bot-standard + work-verify.
6. **Output language:** Always Traditional Chinese body; close with one Cantonese line + emotion tag matching VERDICT (BUY/STALK/WATCH/PASS/AVOID).
7. **Web search discipline:** Exactly three focused company queries (HK vs US templates); cite title+URL; no invented news; tag stale (>30d) sources.
8. **Rename (2026-09-08 event):** Display name set to 投資敘事分析師; description updated to accept HK or US Swing Setup handoffs.

---

## Live snapshot

- **Active tickets:** None pending at snapshot time (last completed: TC-20260909-13 SRRK; Fusion TC-20260909-14 handled downstream).
- **Latest on-disk story artifact:**
  - `/workspace/story-search/output/run-20260909-srrk/STORY_REPORT_SRRK.md`
- **Recent HK narrative (2616):** Delivered in-chat 2026-09-07; no separate `/workspace/story-search/output/` file retained for 2616 in current tree (Fusion received paste).
- **Upstream example paths:**
  - HK: Swing agent messages / labeled GEMINI HANDOFF blocks
  - US: `/workspace/us-swing-setup/output/run-20260909-1232/HANDOFF_SRRK.md`
- **Teammates (routing-critical):**
  - 港股 Swing Setup `28b5646e-bfc2-440b-8a63-b68440a1de4b`
  - 美股 Swing Setup `747b3374-ada7-44d7-8cf4-73098b1c10af`
  - Fusion Formatter `c45141fc-c050-49e2-9635-dca556a0cc1f`
  - 總指揮 `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`
  - Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729`
- **Routines:** None configured for this agent at snapshot.
- **Agent-owned durable facts:** None written yet (memory profile/log empty) — recovery must rely on this file + conversation + skills/KB on disk.
- **Coverage gaps to restore after DR:** Re-seed agent memory profile with standing VERDICT lock + HK/US RS benchmark rules + KB path; optional log entries for 2616 / SRRK ticket outcomes.

---

## Secrets

- No API tokens or credentials stored by this agent.
- Placeholders only if ever needed:
  - `[REDACTED:CURSOR_API_KEY]`
  - `[REDACTED:broker_or_data_api]`
  - `[REDACTED:any_mcp_oauth_token]`
- Never paste real tokens into backups or chat.

---

## Pending confirms

- None outstanding from this agent.
- Optional post-DR: confirm with Justin/總指揮 whether 2616 in-chat-only report should be backfilled to `/workspace/story-search/output/` for parity with SRRK disk artifact.
- Optional: write standing profile facts into agent memory after restore (currently empty by design/history).

---

## Coverage checklist

| Area | Status |
|------|--------|
| Identity / JD / anti-jobs | Covered |
| Pipeline + contract fields | Covered |
| KB + skill names | Covered |
| Historical tickets 2616 / SRRK | Covered |
| VERDICT lock decision | Covered |
| Live artifact paths | Covered |
| Teammate routing ids | Covered |
| Secrets | Placeholders only |
| Agent durable memory files | Noted empty |
| Routines | None |
