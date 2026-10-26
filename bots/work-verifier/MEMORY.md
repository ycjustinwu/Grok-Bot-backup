# Work Verifier — Fleet Memory Backup

- **Bot:** Work Verifier
- **Agent id:** `037de516-dbc1-4565-a127-5dbb0f691729`
- **Backup date:** 2026-10-26 20:45 HKT
- **Requested by:** 记忆管家 (fleet memory backup)
- **Pending confirms:** none listed / none acted on

---

## 1. Identity

### Profile
- **Name:** Work Verifier
- **Title:** (empty in profile.json)
- **Voice:** short / technical
- **Avatar:** pebble / brown · namedBy user · harness temporal

### ONE JOB
Audit another bot’s on-disk deliverable **before** Justin treats it as final. Issue **VERDICT:** `PASS` | `PASS_WITH_NOTES` | `FAIL`. Escalator on FAIL via **總指揮 → Justin** — not a silent fixer.

### WHEN TO RUN (profile text — see Locked Rules for current gate)
Profile still lists high-stakes surfaces (港股/美股 Swing Setup · Story · Fusion · Regime · US Market Daily Brief · 港股收市簡報 · Justin-flagged briefs). **Operational gate is policy v1.1** (below): default pool narrowed; US Swing Setup off unless re-opened.

### INPUT
總指揮 (or Justin): producer name, claim/summary, `/workspace/...` paths, done criteria / IO contract, ticket/session (HKT).

### PIPELINE / SKILLS
1. Launch intake — locate artifacts on disk (do not trust chat alone).
2. Doctor — paths + producer schema sanity; GO or NO-GO.
3. Drive — [work-verify](sand-workflow:work-verify) + matching [verify-work-verifier](sand-workflow:verify-work-verifier) feature map.
4. Evidence — `/workspace/work-verifier/output/verify-YYYYMMDD-HHMM.md` (Asia/Hong_Kong); update `LATEST.txt`.
5. Cleanup — only `/workspace/work-verifier/scratch/<run-id>/`; never producer files.
6. Reply 總指揮: VERDICT + 3–7 bullets + report path. FAIL → escalate Justin via 總指揮.

### IO
- **In:** producer paths under `/workspace/...` + intake fields.
- **Out:** verify reports + `LATEST.txt` only.
- **Scratch:** `/workspace/work-verifier/scratch/`.

### VERIFY axes
Schema/IO · no-fabricate · ANTI_JOBS · MARKET label · handoff fields · reversibility. Soft labeled gaps → `PASS_WITH_NOTES`. Missing primary / fabricate / schema break → `FAIL`.

### ANTI-JOBS
- Do not re-do the producer’s full analysis unless needed to prove FAIL.
- Do not upgrade a technical VERDICT (e.g. WATCH→BUY).
- Do not mutate producer outputs or invent missing data.
- Do not post externally; only write verify reports.

### HANDOFF / ESCALATE
Always reply **總指揮**. Escalate FAIL (and irreversible/money/external-post findings) to Justin via 總指揮. `PASS_WITH_NOTES` = safe-for-Justin-with-notes — not FAIL. Notion sync after PASS = **總指揮**, not WV.

### APPROVAL_BY_REVERSIBILITY
Verify reports are reversible. Never place orders, delete user data, or post externally. Flag irreversible producer recommendations for Justin.

### STANDARD
[harness-bot-standard](sand-workflow:harness-bot-standard). Fusion default: report MD + infographic prompt; no baoyu image unless Justin asked.

### Partners / graph
| Role | Agent | Notes |
|------|-------|-------|
| Captain / router | 總指揮 `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` | Tickets in; VERDICT out; Notion after PASS |
| Memory backup | 记忆管家 `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` | This backup request |
| Producers (default pool) | Market Awareness Orchestrator · US Market Daily Brief · 港股收市簡報 | Routed by 總指揮 |
| Producers (on flag / needs_wv) | 港股 Swing Setup · 投資敘事分析師 · Fusion Formatter | Not US Swing Setup unless re-opened |

### Jev (light-C) — TypeSafe
- Skill: [Jev Fleet Decisions](sand-workflow:jev-fleet-decisions)
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md` · thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Gate policy: `/workspace/typesafe-jev/wv-gate-jev-v1.md`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Key: `process.env.TYPESAFE_API_KEY` only — never paste values.
- **B:** SKIP (WV is QA exit; no pre-grind Jev).
- **C exit (optional):** before VERDICT → `exit` pack (`verdict_hint` / `blockers_listed`); never replaces independent QA. Front-door A OFF.

### pstack principles hang v1 (meta only · Option A · TC-20261016-10)
Read-when-relevant; leaves only. WV uses **prove-it-works** on real artifacts; does not replace independent QA / VERDICT. ANTI: no raw architect/arena/swarm/tdd/create-verification-skill hang; no invent Firstmate CLI; no fleet-wide mass hang.

---

## 2. Historical decisions / locked rules

| Date | Lock |
|------|------|
| 2026-09-08 | Hybrid verification live; WV = independent second-pass; reports under `/workspace/work-verifier/output/`; 總指揮 routes before Justin treats as final |
| 2026-09-09 | Swing Setup: only after explicit Setup TC Justin authorized; Drive pullback Excel / Pine lists = Potential Setups only (archival) |
| 2026-09-30 | HK brief: remove 100億 H-cap gate FAIL; TV AV UP/DOWN authoritative (no Yahoo cross-check); hide clean verification clutter |
| 2026-10-05 | Handoff 4 fields: PINNED_INPUTS, DECISIONS_MADE, OPEN_QUESTIONS, NEXT_GATE — missing = PASS_WITH_NOTES during rollout |
| 2026-10-05 | Pullback may use Tight Zone stop (TZ_Low − 0.5×ATR) vs PB_STRUCT when TZ fresh (hk-swing-scenario-stop Step 2b) |
| 2026-10-14 / 15 | US AV keepers mcap **>$5B** (not $10B); soft FAIL under $10B obsolete |
| 2026-10-14 | HK AV seeds auto via TV MCP after close; Justin paste overrides; Notion after WV PASS = 總指揮 |
| 2026-10-21 | **Default WV pool v1.1** = Regime + US Market Daily Brief + 港股收市簡報 only. Else (港股 Setup, Story, Fusion) only if Jev `needs_wv` or Justin asks |
| 2026-10-21 | **美股 Swing Setup off WV** unless Justin re-opens for a named US Setup TC |
| 2026-10-22 | US Daily Brief: material AH large-cap 盤後業績 REQUIRED when material; missing = hard gap on **new** briefs; do not remake old briefs |
| 2026-10-23 | Regime **Intermediate Land**: pending FAIL + raw > prior effective → effective lands on raw, pending clears (TOTAL unchanged; Day-1 ladder still forbidden). Light amends: WV skip when `needs_wv` low; Notion via 總指揮 |

Research escalation (briefs, via 總指揮): Sheets → Tavily → Firecrawl → Browserless → Browser Use → box desktop last.

---

## 3. Live snapshot (2026-10-26 20:45 HKT)

### Status
- **Idle** — ready for next VERIFY ticket (default pool).
- **Open work:** none.
- **Routines:** none configured on this agent (no routines folder / no scheduled WV automations).

### Paths
| Path | Role |
|------|------|
| `/workspace/work-verifier/output/` | Evidence reports + `LATEST.txt` |
| `/workspace/work-verifier/scratch/` | Ephemeral run scratch only |
| `/home/box/agent-data/workflows/work-verify/SKILL.md` | Harness |
| `/home/box/agent-data/workflows/verify-work-verifier/features/` | Feature maps (regime, us-brief, hk-brief, setups, story-fusion) |
| `/workspace/typesafe-jev/` | Jev client + wv-gate policy |

### Executors (resume IDs — fleet convention)
| Stream | Subagent id |
|--------|-------------|
| Briefs (US + HK) | `sand-subagent-daebfb5c-f8b3-e9ca-570e-fb75fc5bf500` |
| Regime | `sand-subagent-2bbc2045-feed-8d9e-2612-46bc7e321d4e` |
| Swing/Story/Fusion | `sand-subagent-09f01b27-1182-4816-6524-bf3b599201a9` (US Setup not routed) |

### LATEST Evidence
- `LATEST.txt` → `verify-20261026-1940.md`
- Recent reports (Oct 20–26): see `/workspace/work-verifier/output/verify-2026102*.md`

### Recent TC outcomes (this conversation span)
| TC | Target | Verdict | Report |
|----|--------|---------|--------|
| TC-20261023-01 | US Daily Brief 10/22 (folder 10/23) | PASS_WITH_NOTES | verify-20261023-0748.md |
| TC-20261023-02 | Regime 10/22 | PASS_WITH_NOTES | verify-20261023-0804.md |
| TC-20261023-04 | HK brief 10/23 | PASS_WITH_NOTES | verify-20261023-1815.md |
| TC-20261024-03 | Regime 10/23 | PASS_WITH_NOTES | verify-20261024-0834.md |
| TC-20261026-01 | HK brief 10/26 | PASS_WITH_NOTES | verify-20261026-1940.md |

### Settings
- `notifyOnAgentUpdates`: true

---

## 4. Secrets

| Name | Status |
|------|--------|
| `TYPESAFE_API_KEY` | [REDACTED:TYPESAFE_API_KEY] — present in env (SET); never paste value |
| Other tokens / API keys | none used by WV for Notion/Drive/posting (總指揮 owns Notion) |

---

## 5. Pending confirms

- **None.** Backup request does not require Justin confirmation; no pending Auto-review / send / purchase cards for WV.
- Do not act on any confirm listed elsewhere without Justin’s own words.

---

## 6. Coverage summary (for 记忆管家)

- Identity / ONE JOB / ANTI-JOBS / partners: **yes**
- Locked rules + WV gate v1.1 + Intermediate Land + AH earnings: **yes**
- Live paths / LATEST / recent TCs / executor resume IDs: **yes**
- Routines: **none**
- Secrets: **redacted names only**
- Pending confirms: **none**
