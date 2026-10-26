# Memory disaster-recovery backup — 投資敘事分析師 (Story Search v2.2)
- Agent id: `3f297e81-4667-4dae-b517-b4f7ddee3537`
- Server id: `2410906`
- Snapshot: 2026-10-26 20:46 HKT (UTC+8)
- Requested by: 记忆管家 (full fleet memory backup, Justin)
- Prior snapshots:
  - `/workspace/3f297e81-4667-4dae-b517-b4f7ddee3537-memory-backup.md` (2026-10-03; overwritten by this file)
  - `/workspace/2410906-memory-backup.md` (2026-09-14 / refreshed ~2026-10-23 on box)
- File: `/workspace/3f297e81-4667-4dae-b517-b4f7ddee3537-memory-backup.md`

---

## Identity

- **Name:** 投資敘事分析師
- **Title:** (empty)
- **Role:** Story Search v2.2 — investment narrative analyst
- **User:** Justin Wu; timezone Asia/Hong_Kong
- **ONE JOB:** Turn a labeled `GEMINI HANDOFF` from 港股 Swing Setup or 美股 Swing Setup into a Fusion-ready 敘事報告. Body 繁體中文. Close with one Cantonese line (≤50字) that includes entry, stop and target, plus an emotion tag that matches the locked VERDICT.
- **Upstream:** 港股 Swing Setup `28b5646e-bfc2-440b-8a63-b68440a1de4b` or 美股 Swing Setup `747b3374-ada7-44d7-8cf4-73098b1c10af` (MARKET=HK or US)
- **Downstream:** Fusion Formatter `c45141fc-c050-49e2-9635-dca556a0cc1f` — hand off only when the ticket says to / 總指揮 RELEASE. Default Fusion deliverable: report MD + infographic prompt MD only, no image.
- **Coordinator:** 總指揮 `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`
- **Second pass:** Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729` → `/workspace/work-verifier/output/`. **WV routing (Justin 2026-10-21, shared):** default WV pool = Regime + US Market Daily Brief + 港股收市簡報 only. Story/Fusion use WV **only if** Jev `needs_wv` or Justin/總指揮 explicitly routes. 美股 Swing Setup stays off WV unless re-opened. Older hybrid-verification shared fact (2026-09-08) still names Story among high-stakes; **prefer the 2026-10-21 default-pool rule** unless a ticket flags WV.
- **Pipeline:** Story Handoff Parse → Story Theme Match → Story Web Search → Story Narrative Validate → Story Search Report
- **Contract fields (ask if missing):** VERDICT / SETUP / STOP TYPE / STOP ANCHOR / SCENARIO ENTRY / ENTRY ZONE / ADJUSTED STOP / PRIMARY TARGET+RR / EARNINGS / KEY SUPPORT / TECHNICAL CONCERN / CLAUDE CONVICTION / RS_SCORE / MARKET
- **RS rules:** US → Stock% − SPY%; HK → Stock% − HSI%. Never mix benchmarks. Narrative follows MARKET tag.
- **ANTI-JOBS:** Do not re-check or rewrite the technical VERDICT, prices, or stop. Do not run Scanner or Setup. Do not invent catalysts or price-volume. Never upgrade VERDICT to BUY because the story is good.
- **Knowledge base:** `/workspace/refactored_story_search/docs/knowledge/` (`biotech-pharma-15th-five.md`, `china-policy-and-hk-mechanics.md`, `global-megatrends-2026.md`, `narrative-quality-framework.md`). Flag KB gaps honestly.
- **Skills:** story-handoff-parse, story-theme-match, story-web-search, story-narrative-validate, story-search-report. FA depth note: `/workspace/story-search/docs/EXPECTED_DEPTH_FA_EXEMPLAR.md`. Fleet gate skill: [Jev Fleet Decisions](sand-workflow:jev-fleet-decisions).
- **Jev (B+C) — TypeSafe (in profile description):** Client `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`; thresholds `/workspace/typesafe-jev/config/thresholds.json`; docs `/workspace/typesafe-jev/fleet-decision-layer-v1.md`; key `[REDACTED:TYPESAFE_API_KEY]` via env only; logs `/workspace/typesafe-jev/logs/` when practical. **B** every TC/user task before grind → `pre_task` (`act` | `evidence_enough` | `escalate` | `cost_tier`). Mid-task Jev only on new forks. **C** before Final/handoff-out → `exit` (`ready_for_justin` | `needs_wv` | `conflict` | `soft_ambition`). Front-door A OFF (總指揮 routing). Never invent tickers/prices via Jev; never auto-send/auto-trade from a Noul.
- **Output path:** `/workspace/story-search/output/run-YYYYMMDD-<ticker>/STORY_REPORT_<TICKER>.md`
- **Profile:** avatar pebble / violet; `namedBy: user`; harness `temporal`; `notifyOnAgentUpdates: true` (settings.json)
- **Routines:** none (per automation_status)
- **Durable agent memory (profile):**
  - (2026-09-18) FA (First Advantage) depth bar — see Historical #4
  - (2026-09-18) Cantonese one-line closer; often Cantonese for related stock-report chat
  - (2026-09-25) Usage gate (Justin 2026-09-20, `/workspace/fleet-policies/USAGE_GATE.md`): reuse fresh artifacts; stop after same approach fails twice; chat-only if no tools; prefer connector/API; never create bots/routines to save usage

---

## Historical decisions / locked rules

1. **VERDICT ownership (standing):** Swing Setup owns the trade call. Story may CONFIRM / CHALLENGE / NEUTRAL against CLAUDE CONVICTION only. A good story never upgrades WATCH/STALK/PASS to BUY.
2. **HK 2616 基石藥業 (2026-09-07):** VERDICT=STALK. Delivered in chat; Fusion after approval. No on-disk story file.
3. **US SRRK (TC-20260909-13):** BUY. `/workspace/story-search/output/run-20260909-srrk/STORY_REPORT_SRRK.md`. Fusion as TC-20260909-14.
4. **FA depth bar (2026-09-18, Justin):** Encoded in `story-search-report` + EXPECTED_DEPTH_FA_EXEMPLAR. ~5–7 sources; every 數字驗證 needs dated source + [SEARCH] or 未能核實. Supersedes older “exactly three web queries” rule; stays lean under usage gate.
5. **US VIR (TC-20260918-13):** BUY, FA rewrite. `/workspace/story-search/output/run-20260918-vir/STORY_REPORT_VIR.md`.
6. **US TH (TC-20260918-19):** STALK. `/workspace/story-search/output/run-20260918-th/STORY_REPORT_TH.md`. Not Fusion’d that turn.
7. **US MRVI (TC-20260925-06):** WATCH locked. Story `/workspace/story-search/output/run-20260925-mrvi/STORY_REPORT_MRVI.md`. Fusion (no image) `/workspace/fusion/output/run-20260925-155939/`. MarketBeat consensus $6.83 coincidentally equals stop — unrelated; do not mix.
8. **US NBIS + SMCI (TC-20261005-02, 2026-10-05):** Upstream Setup TC-20261005-01 handoffs under `/workspace/us-swing-setup/output/run-20261005-1329/`. MARKET=US.
   - **NBIS** STALK — Story `/workspace/story-search/output/run-20261005-nbis/STORY_REPORT_NBIS.md`. Entry $226.58–$229.22; FINAL STOP **$218.35 TZ** (Justin kept TZ vs WV-suggested PB_STRUCT $216.61 / RR 2.38x); T1 $254.74; RR **2.81x**. Scores 主7/次5/風險8. CONVICTION CONFIRM vs Claude MEDIUM-LOW. Closer includes 防攤薄. MSFT ~$17.4B kept **未能核實** for company-manuscript face value (F-S2). Oct 4 Summary_US cites NBIS P7 Favor (path below); analysis suggests P2 reclass — Favor label verified, sector wind not used by Fusion.
   - **SMCI** WATCH — Story `/workspace/story-search/output/run-20261005-smci/STORY_REPORT_SMCI.md`. Trigger $40.17–$41.01; stop $38.99; target $44.59; RR 2.50x. Scores 主6/次4/風險7. CONVICTION CONFIRM vs LOW. ICFR: **carry-over material weakness from FY25 10-K** (IT/permissions; Item 9A); other three remediated — **not** a “new” weakness (F-S1 soft fix).
   - **WV:** `PASS_WITH_NOTES` `/workspace/work-verifier/output/verify-20261005-1342.md`. Soft fixes applied in place; Fusion told to carry F-S1 wording.
   - **Fusion (MD only):** NBIS `/workspace/fusion/output/run-20261005-134531/`; SMCI `/workspace/fusion/output/run-20261005-134533/`. Fusion ACK’d F-S1 (no「新」) and NBIS closer 防攤薄; noted Setup MD vs Summary P7 Favor mismatch — Story already documented.
   - **Stop sequencing note:** Mid-run HOLD Fusion until Justin decided TZ; then RELEASE to Fusion. HANDOFF files left unchanged; Story note records TZ pullback exception.
9. **TZ-on-pullback exception (Justin 2026-10-05, shared_journal):** A swing pullback entry may use Tight Zone stop (Tight_Zone_Low − 0.5×ATR) instead of PB_STRUCT when TZ is fresh and entry zone sits inside/above it — written into `hk-swing-scenario-stop` Step 2b. Story must **not** invent or change stops; follow locked Handoff/Justin decision.
10. **Routing:** Ticketed jobs carry a TC id. Reply to sender with absolute path + one-line thesis. Do not fan out. Hand to Fusion only when ticket/總指揮 authorizes. Reply priority:true when coordinator waiting; FYI/status priority:false.
11. **Language:** Traditional Chinese body. Cantonese closer ≤50字 with entry/stop/target + VERDICT-matched tag (STALK/WATCH → ⚡觀望等位).
12. **Usage gate (2026-09-20 / profile 2026-09-25):** See Identity.
13. **Rename (2026-09-08):** Display name 投資敘事分析師.
14. **WV default pool (Justin 2026-10-21):** See Identity. Story still runs VERIFY in-skill; external WV is ticket-/Jev-gated.
15. **Shared facts not owned by this bot (record only):** HK after-close brief dropped 100億 H-cap gate (2026-09-30); Market Master sheet id `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` for breadth/setups; Notion Final sync applies to other bots’ briefs — this Story bot does not auto-Notion unless ticketed.

---

## Live snapshot

- **Active tickets / open Story work:** none. Last completed Story+Fusion ticket: **TC-20261005-02** (NBIS+SMCI). Soft fixes done; Fusion complete; WV PASS_WITH_NOTES addressed. No open TodoWrite items beyond this backup.
- **On-disk story artifacts:**
  - `/workspace/story-search/output/run-20260909-srrk/STORY_REPORT_SRRK.md`
  - `/workspace/story-search/output/run-20260918-vir/STORY_REPORT_VIR.md`
  - `/workspace/story-search/output/run-20260918-th/STORY_REPORT_TH.md`
  - `/workspace/story-search/output/run-20260925-mrvi/STORY_REPORT_MRVI.md`
  - `/workspace/story-search/output/run-20261005-nbis/STORY_REPORT_NBIS.md`
  - `/workspace/story-search/output/run-20261005-smci/STORY_REPORT_SMCI.md`
- **Related Fusion / WV (TC-20261005-02):**
  - Fusion NBIS: `/workspace/fusion/output/run-20261005-134531/` (`FUSION_REPORT_NBIS.md`, `FUSION_INFOGRAPHIC_PROMPT_NBIS.md`, `SELF_VERIFY_NBIS.md`)
  - Fusion SMCI: `/workspace/fusion/output/run-20261005-134533/`
  - WV: `/workspace/work-verifier/output/verify-20261005-1342.md`
  - Scanner cite for NBIS P7: `/workspace/us-swing-scanner/output/run-20261004-1629/Summary_US.csv`
  - Setup handoffs: `/workspace/us-swing-setup/output/run-20261005-1329/HANDOFF_NBIS.md`, `HANDOFF_SMCI.md`
- **Not on disk:** HK 2616 (chat-only)
- **Routines:** none
- **Skills:** five story-* workflows under shared `/home/box/agent-data/workflows/` (+ jev-fleet-decisions)
- **Persistent store mount:** `/cursor/stores/store-6f077d08-869d-4de4-af51-4a6e8df376ec` (this bot’s own store)
- **Jev this backup turn:** `pre_task` → act=`cheap_path` (conf 0.6), evidence_enough noul≈0.85, escalate low, cost_tier≈0 (local write)

---

## Secrets

- This agent stores no broker keys or OAuth secrets in files.
- TypeSafe / Jev: `[REDACTED:TYPESAFE_API_KEY]` (env `process.env.TYPESAFE_API_KEY` only — never paste values)
- Connector credentials: `[REDACTED:mcp_oauth]`
- Never paste a real token into a backup or into chat.

---

## Pending confirms

- **None outstanding** for this agent (no Justin decision waiting; no unapplied WV notes on open tickets).
- Optional, not blocking: backfill HK 2616 to `/workspace/story-search/output/` if Justin wants disk parity. Not asked — **do not act**.
- Informational (Fusion FYI, already reflected in Story): NBIS P7 Favor vs Setup MD wording mismatch — no further Story action required unless Justin asks.

---

## Coverage checklist

| Area | Status |
|------|--------|
| Identity / JD / anti-jobs | Covered |
| Pipeline + contract fields + RS benchmarks | Covered |
| KB + skill names + FA depth bar | Covered |
| Jev B+C + thresholds path + front-door OFF | Covered |
| Tickets 2616 / SRRK / VIR / TH / MRVI / NBIS+SMCI | Covered |
| VERDICT lock + TZ pullback exception (follow, don’t invent) | Covered |
| WV default-pool rule (2026-10-21) vs ticketed WV | Covered |
| Live artifact + Fusion + WV paths | Covered |
| Teammate routing ids | Covered |
| Usage gate | Covered |
| Secrets | Placeholders only |
| Agent profile memory (3 facts) | Covered |
| Routines | None |
| Pending confirms | Listed; none blocking |
