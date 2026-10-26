# 總指揮 memory backup — 2026-10-26

- Bot id: `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`
- Name / title: 總指揮
- Backup requested by: 记忆管家
- Written: 2026-10-26 ~20:46 HKT (Asia/Hong_Kong)
- Owner: Justin Wu

---

## 1. Identity

### Profile (from profile.json)
- **ONE JOB:** Coordinate bots and handoffs. Do not do specialist analysis yourself when a specialist exists.
- Role: Justin’s single Grok Bot liaison (Firstmate-style captain contact). Justin talks to 總指揮; crew reports outcomes/blockers to 總指揮, not past him to Justin (unless he opened their chat).
- Server harness: temporal; avatar green pebble; namedBy user.

### CAPTAIN LIAISON (locked ops)
- Default handoff for >quick tool call / multi-minute grind.
- Every tasked handoff: `TC-YYYYMMDD-##`; crew replies against that id (incl. empty).
- Async: hand off → tell Justin what’s under way → relay results.
- One decision = one message + one choice card.
- Speak outcomes/consequences, not internals.
- Secrets: never paste in chat; Justin gives credentials via secure card to the target bot.

### ROSTER MAP (partners)
- **Market:** Market Awareness Orchestrator ‖ US Market Daily Brief ‖ 港股收市簡報 ‖ X Brief
- **Swing HK:** HK Swing Scanner → 港股 Swing Setup → 投資敘事分析師 → Fusion Formatter
- **Swing US:** US Swing Scanner → 美股 Swing Setup → 投資敘事分析師 → Fusion Formatter
- **Life:** 旅行計劃助手 ‖ 旅行酒店比價 ‖ 高級餐廳訂位助理 ‖ 全富決策副手
- **Meta:** Prompt Architect ‖ Self Improver ‖ dr eggbot ‖ Work Verifier
- **Also routed often:** Second brain; US swing 模擬倉; X Monitor; ETF RS Cross; Market Master Apps Script; 北極星; Sweeper; 记忆管家; Researchy; HTML Motion Studio; YouTube Analyzer Deep; 文章分析; 日常小助手; Career Coaching; 家庭成長副手; Feature RE Spec; Video Transcriber; Explainer Video bot

### DISPATCH (summary)
1. Prefer specialist; exact `/workspace/...` paths + TC id; remind Jev B pre_task (`jev-fleet-decisions`).
2. **WV gate v1.1 (2026-10-21):** default pool = Regime/Market Awareness + US Market Daily Brief + 港股收市簡報 only. Others: WV only if Jev C `needs_wv` ≥ threshold OR Justin asks OR hard conflict. **美股 Swing Setup** off WV unless re-opened. Scanners / empty Second brain skip. Policy: `/workspace/typesafe-jev/wv-gate-jev-v1.md`.
3. After PASS / PASS_WITH_NOTES → short verdict; FAIL → escalate with verify path; WV skipped → soft Final.
4. Google connectors first for calendar/email/Drive.
5. Escalate to Justin: money, deletes, ambiguous go/no-go, conflicting bots, irreversible actions.

### Jev (light-C only)
- Front-door A OFF (總指揮 owns routing).
- Skip B on pure route/TC fan-out.
- Run C when this bot claims a Final / stand-in, or WV-gate on non-pool when `needs_wv` missing/unclear.
- Key: `[REDACTED:TYPESAFE_API_KEY]` via `process.env.TYPESAFE_API_KEY` — never paste.
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md`, `wv-gate-jev-v1.md`, client `/workspace/typesafe-jev/jev_client.py`, thresholds `/workspace/typesafe-jev/config/thresholds.json`.

### pstack (meta Option A)
- `/workspace/typesafe-jev/pstack-principles-hang-v1.md`
- Use guard-context + never-block (reversible) + outcome; lean TC/handoffs.
- Do NOT hang poteto/architect/arena/tdd/create-verification-skill or invent Firstmate CLI.

### CREATION GATE
- New/rewritten bots/skills must pass `harness-bot-standard`. Else refuse or send Prompt Architect / dr eggbot.

### ROUTINE DELIVERY RISK (fleet) — Justin 2026-10-23
- Enabled + scheduled ≠ delivered.
- Modes: (A) never-run; (B) wake then “Activity task failed” before tools.
- Diagnose: automation_status + transcript for Activity task failed.
- Do not assume asleep / clock / X quota first.
- Time-critical: post-deadline follow-through or one-shot recovery; do not recreate already-enabled routine.

### ANTI-JOBS
- No swing math / regime scoring / specialist research by 總指揮.
- No inventing tickers, prices, VERDICTs.
- No auto-WV non-pool work.
- Never use 「港美股 Swing Setup」.
- No bots that fail harness gate.
- No multi-minute grind kept in this chat when a crewmate owns it.
- Do not become Firstmate CLI; coding fleets prefer Cursor cloud agents via coding crewmate if Justin asks.

### IO
- Shared computer is the bus.
- Verify reports: `/workspace/work-verifier/output/`.

---

## 2. Historical decisions / locked rules

### WV / QA
- **2026-10-21:** WV default pool = Regime + US Market Daily Brief + 港股收市簡報 only; 美股 Swing Setup outside unless re-opened. Policy v1.1.
- Hybrid verification live: Work Verifier id `037de516-dbc1-4565-a127-5dbb0f691729` writes to `/workspace/work-verifier/output/`.

### Market Master
- **Canonical sheet (2026-10-22):** id `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` — tabs 美股市寬／美股行業／港股市寬／港股行業／ETF 輪動／形態篩選／Setup_Latest. Old Setup Master / US+HK Market Monitor retired. Doc `/workspace/docs/market-master-canonical-2026-10-22.md`.
- Setup shortlist: Setup_Latest / 形態篩選; Primary in TC_shallow/TC_deep/CB; top-by-Score = Justin-pick only — **never auto-run US Swing Scanner**.
- **Market Master Apps Script** bot `b091ceb4-c770-457a-861d-d9b7c9911a0b`; inbox `/workspace/market-master/apps-script/`; skills mm-gas-intake / mm-gas-merge-charts / mm-gas-verify. First ticket = US/HK breadth axis distortion (merge friend viewWindow into existing stack).

### Regime
- Scoring v6.4.6; Intermediate Land lock (2026-10-23): pending FAIL + raw higher than prior effective → effective lands on raw, pending clears; TOTAL unchanged; Day-1 ladder still forbidden.
- Daily requires top-bar 今日動作 (准試倉／觀望／收手) + linkage + Trial carve-out (skills regime-daily-report / regime-modifiers-and-stance / market-awareness-orchestrator); WV feature regime-today-action. Does not change TOTAL/hysteresis.

### US / HK briefs & AV
- Research prefer MCP: Google Sheets → Tavily → Firecrawl → Browserless → Browser Use → box desktop last.
- US-ETF Drive folder `1k5dJy7ny5n-W_EV5Aglt0QeeXS_-5Ijn` — notify if missing.
- AV UP/DOWN: TradingView MCP (`tv-abnormal-volume-mcp`); Justin paste overrides.
- HK: no 100億 H-share mcap gate; trust TV AV without Yahoo cross-check; auto-hide clean verification detail.
- US Brief: required `### 盤後業績` after Part 6 for large-cap/Mag7/key semi AH; seed X Monitor then IR/wires; skill+bot only (no remake old Finals).

### Swing / Second brain / 模擬倉
- US Second brain: driven by US Swing Scanner handoff (not noon cron); ≤3 stalks; noon routine stays **paused**.
- After stalks: also `us-swing-session-overview`; route 模擬倉 open/skip.
- 模擬倉 id `17a46819-623f-40fe-8430-338e05725381`: paper $100k, R=1%/$1k, max 7 positions; state `/workspace/us-swing-sim/`.
- US Swing Scanner Drive: folder `1Jn7yi0sXFBqVjLvjCsIazZnOvw0_E4TY` dated subfolders.
- Preference: growth, high ATR, strong R:R; hold ≤~2 weeks unless clear homerun; Deep Bear = harder tape not zero opportunity.
- US RS sharpen vs Ross id `88d71c92-…` = SKIP for Jev hang (empty/broken profile).

### Notion
- Workspace: Wu Justin's space.
- Auto-sync Final MD (and Motion HTML/MP4) for market-brief / family-growth / career-coaching / HTML Motion Studio / YouTube Analyzer / 文章分析 without re-asking.
- HK 港股收市簡報庫 `collection://803e4190-3dc3-4863-a15a-fbd0d9875ee4` — 總指揮 syncs after WV PASS when same-date row exists.
- Notion body via `$file:/absolute/path.md` as entire content arg (never embed `$file:` inside markdown text).
- Lookup skill: notion-db-lookup; catalog `/workspace/notion-briefs-import/library-catalog.json`.

### Other locks
- LinkedIn (Composio): read-only unless Justin explicitly instructs edit/post.
- Justin role: equity structured product specialist at BNP Paribas (promoted as of Oct 2026).
- Schooling default (2026-10-05): elder ~12 stays Queen’s College through HKDSE; overseas uni later; education pool prioritizes uni FX liquidity.
- Jev B+C hung on fleet (A off) since 2026-10-16; smoke OK jev-1.13.0.
- **2026-10-26:** Declined Melvin-style Fleet Activity Dashboard — do not refresh/push; routine `fleet-activity-dashboard-refresh` **deleted**. Page may remain in Library unused. Canvas id `79abd185-a09f-474f-bcf3-e933820ebf3b` / store `8322307b-0a6a-4cfd-81ff-9e28f2f4c4f5`.

---

## 3. Live snapshot (2026-10-26 evening HKT)

### Routines (總指揮 automation_status)
| Routine | Status | Schedule | Notes |
|---|---|---|---|
| Weekly self-improve reflection | paused | Fri 18:00 HKT | last 2026-09-11 succeeded |
| Kick HK after-close brief | paused | Weekdays 18:05 | never run |
| X @bot tags from Justin | paused | Hourly weekdays 09:02–20:02 | last 2026-10-14 |
| Notion Finals catch-up sync | **enabled** | Weekdays 18:12 | last 2026-10-26 **failed** (usage) |
| US second-brain 3 picks | paused | Tue–Sat 12:00 | never run; intentional — scanner-driven |

Deleted this day: `fleet-activity-dashboard-refresh` (Justin declined).

### Recent closed TCs (selected)
- **TC-20261026-01** 港股收市簡報 2026-10-26: Final `/workspace/hk-brief/2026-10-26/HK brief-2026-10-26.md` (md5 `1f14181a3e78193dba86cde8219915a4`); WV `verify-20261026-1940.md` PASS_WITH_NOTES; Notion https://app.notion.com/p/40577383f89c811ea822c8168715c20e — CLOSED.
- Soft Final highlight: 恒指 23,211.81 (+0.51%); 科指 −0.36%; 成交 ~1,758億; VHSI 20.61; AV 3 UP/7 DOWN; 北水 −20.75億; Master Up4 23 / Dn4 31.
- Prior closed (carry): TC-20261024-03 Regime 10/23; TC-20261024-04 screener→SB→模擬倉 (FRO OPEN / CRWD+FIVN SKIP); X Monitor Sat recover; CRL HOLD.

### Paths / artifacts live
- HK brief: `/workspace/hk-brief/2026-10-26/`
- WV out: `/workspace/work-verifier/output/verify-20261026-1940.md`
- X Monitor on-demand softshort (US Brief seed): `/workspace/x-monitor/ondemand-2026-10-26-softshort.md` (+ body/candidates/pages) — Weekday+Evening routines failed earlier on usage; on-demand delivered to Justin in X Monitor chat; routines left enabled.
- Market Master Apps Script inbox: `/workspace/market-master/apps-script/`
- Fleet activity pointer under `/workspace/fleet-activity/`: **gone** (aligned with decline).

### Open work / idle state
- **Idle** on Justin’s latest explicit asks (HK brief done; dashboard declined).
- Optional / waiting Justin (not acted): Market Master Apps Script breadth `.gs` / shares handoff still pending his scripts.
- Soft offer (not confirmed): audit fleet routines vs GrokBotRadar usage Article # (re-read tax) — Justin has not approved.

### Usage note (2026-10-26)
- Hits: Notion Finals catch-up failed (usage); X Monitor Weekday+Evening failed (usage) then on-demand softshort recovered.
- Manual HK Notion sync after WV still succeeded.

### Secrets (names only)
- `[REDACTED:TYPESAFE_API_KEY]` — Jev / TypeSafe
- No other bot-owned secrets listed in this backup; connector OAuth stays in connectors, never exported as values.

---

## 4. Pending confirms (listed only — do not act)

1. **Market Master Apps Script** — Justin still to provide/approve breadth chart `.gs` / share scripts for first ticket (axis distortion / viewWindow merge).
2. **GrokBotRadar usage playbook** — 總指揮 offered a ten-step fleet routine/handoff audit; awaiting Justin go/no-go.
3. **Notion Finals catch-up routine** — enabled but last run failed on usage; whether to keep enabled / recover / change cadence is Justin’s call (not changed here).
4. **Fleet Activity Dashboard Page** — declined refresh; Page may still sit in Library for Justin to delete himself (no auto-delete).

---

## 5. Coverage checklist

- [x] Identity / ONE JOB / ANTI-JOBS / roster partners
- [x] Locked rules (WV, Market Master, Regime Intermediate Land, briefs/AV, Second brain, Notion, LinkedIn, Jev)
- [x] Live routines snapshot
- [x] Recent TC + paths
- [x] Open / pending confirms listed without action
- [x] Secrets redacted by name only
