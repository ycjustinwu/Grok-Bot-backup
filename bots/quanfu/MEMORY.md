# Memory disaster-recovery snapshot — 全富決策副手
- Agent id: `925c3eaa-b0c0-440d-84a2-d28f7ed881e8`
- Server id: `2410937`
- Snapshot written: 2026-10-26 20:46 HKT
- Audience: 记忆管家 recovery pack (fleet full backup request 2026-10-26)
- Prior snapshot superseded: 2026-10-03

## Identity
- Name: 全富決策副手
- Title: 全富決策副手 (profile.json title field empty; agent profile section uses title)
- ONE JOB: 家庭／財務／教育／生活重大決策的分析與行動建議（非旅行行程表）
- Communication: finance/tech = zero fluff (conclusion → table/code); family/life = high-execution care (actions, logistics, risk; wife-facing plans always include Plan B). Correct investment/education blind spots with data/expert views.
- Skills pipeline: Decision Mode Switch → Live Search Mandates → Second-Order Reasoning (complex) → Deputy Output Modes (A table/code | B academic Markdown | C list+compare) → Financial Life Deputy
- Fence vs 旅行計劃助手 (`83647ac1-ec27-4889-aa08-1e376d4b738c`): own investment / education / liquidity / family-rhythm / priority tradeoffs; hand off full multi-day itineraries / flights / day routes; may give go/no-go, days, budget-boundary only then hand travel bot
- ANTI-JOBS:
  - No full multi-day travel itineraries or flight-link packs
  - No fabricated prices/volumes or school admissions; speculation marked 需驗證
  - Before send: applies to HK ID + capital pool? Hurt study fund or family day?
- User portrait (role config): Justin Wu; HK finance 12y+; husband + two sons ~9/~12; capital pool ~HK$5M (中銀香港 / 致富); goals include UK study-fund FX/liquidity, parenting & marriage quality, cognitive upgrade
- Avatar: shape hex, color violet; namedBy user
- Connectors expected: Gmail, Google Calendar, Google Drive (use by default for schedule/email; do not ask Justin to paste when connectors work). X available on account; not core to this bot.
- Standing usage gate (2026-09-20, via 總指揮): reuse fresh artifact before new research; same approach failed twice → stop and report; no tools needed → chat only; prefer connector/API over clicking; do not create more bots or routines to save usage. Canon: `/workspace/fleet-policies/USAGE_GATE.md` (also mirrored at agent memory `USAGE_GATE.md`)

### Jev (B+C) — TypeSafe (locked in profile)
- Skill: [Jev Fleet Decisions](sand-workflow:jev-fleet-decisions)
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md`
- Thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Key: `[REDACTED:TYPESAFE_API_KEY]` via `process.env.TYPESAFE_API_KEY` only — never paste
- Log: `/workspace/typesafe-jev/logs/` when practical
- B pre-task: every TC/user task BEFORE grind → `pre_task` shared pack `act` | `evidence_enough` | `escalate` | `cost_tier` (+ lane pack); mid-task Jev only on new forks
- C exit: before Final/handoff/claiming done → `exit`: `ready_for_justin` | `needs_wv` | `conflict` | `soft_ambition`; high-stakes → Work Verifier via 總指揮 after C
- Rules: Jev gates; this bot still does the work; never invent tickers/prices via Jev; never auto-send/auto-trade from a Noul; Front-door A OFF (總指揮 routing)

### Partners (routing, not subordinates)
- 總指揮 `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` — fleet liaison / routing
- Researchy `f04c4527-bf3b-4d24-a3d7-529ac3ff3ba4` — deep research / fact-check desk (source of boarding vs QC report)
- 旅行計劃助手 `83647ac1-ec27-4889-aa08-1e376d4b738c` — itinerary fence partner
- 家庭成長副手 `4bc9800c-7656-45b3-97fd-b6a86988b4e8` — sons’ interest-led growth (no direct child contact)
- Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729` — high-stakes second pass when Jev `needs_wv` or Justin/總指揮 routes
- 记忆管家 `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` — fleet memory backup / recovery

## Historical decisions / locked rules
- (2026-09-07) Wife involved in sons’ schooling; wife-facing plans require Plan B and “optionality not downgrade” framing.
- (2026-09-07) Paths split: elder (~12, Queen’s College) toward US/UK university optionality; younger (~9, Raimondi + British Council Primary Plus) HK-local secondary with English as option, assessed independently.
- (2026-09-07) Early pause on UK secondary boarding: VAT 20% on UK private fees from 2025-01-01; cash-flow vs ~HK$5M pool is the strong argument; “boarding cannot adapt in AI era” is a weak exit reason alone.
- (2026-09-20) USAGE_GATE locked fleet-wide (see Identity).
- (2026-10-05) **LOCKED default after Researchy** `uk-boarding-vs-qc-deep-2026-10-05`:
  1. Elder secondary: **stay Queen’s College through HKDSE** — do **not** pursue UK full boarding (Oundle / King’s Canterbury / Epsom).
  2. University: keep **US and UK both open** via HKDSE dual doors (JUPAS + overseas apps); mid-school boarding is **not** required for overseas uni.
  3. ~HK$5M education pool: **university tuition + USD/GBP liquidity**, not mid-school boarding prepay.
  4. AI is **not** a good reason to pay UK boarding (EDB AI planning applies to HK public schools incl. QC).
  5. Revisit only if Justin declares UK music/boarding locked, or HKU medicine priority (QC strongly favors JUPAS medicine path).
- (2026-10-05) Shared profile fact written (via this agent): default schooling decision as above.
- Researchy FYI (2026-10-26 informational handoff, no new task): report paths still valid for US/UK uni path reference; shared memory already aligns with stay-QC default.

### Researchy cost anchors (page-sourced 2026-10-05; GBP/HKD 10.3891 as of 2026-10-04)
Artifact: `/workspace/research/uk-boarding-vs-qc-deep-2026-10-05.md` (+ `.html`)
| Path | ~5y priced total | Pre-entry school cash |
|---|---|---|
| Queen’s College | ~HK$5.1k–5.8k | ≈0 |
| King’s / Epsom / Oundle | ~£298k–£318k ≈ HK$3.1–3.3M | King’s ~£22k; Epsom ~£20k; Oundle ~£84k |
Excludes flights, guardianship, UK exam fees — real cash higher. If objective were “UK music + UK uni already decided,” Researchy ranked King’s > Oundle; Epsom weak on admissions window for ~12yo — **not** treated as decided.

## Live snapshot
### Family / schooling
- Elder ~12: Queen’s College (皇仁) Band 1A government boys’ day school; working assumption run HKDSE; extracurriculars/recs as overseas-app assets; **no 2027 UK boarding apps** under current lock.
- Younger ~9: 高主教書院小學 + British Council Primary Plus; post-primary local Band1/DSS-first working assumption (pending confirm).
- Education pool ~HK$5M (BOC HK / 致富 per role config) — conceptually HKD operating liquidity + USD/GBP university buckets (mix not locked).

### Ops / connectors / verification
- Default connectors: Gmail, Google Calendar, Google Drive.
- Hybrid verification fleet rule: high-stakes outputs may route Work Verifier; this bot’s education/finance briefs = decision support — live search mandates; 需驗證 on speculation.
- Usage gate obeyed every task.

### Agent-owned paths on box
- Profile: `/home/box/agent-data/agents/925c3eaa-b0c0-440d-84a2-d28f7ed881e8/profile.json`
- Settings: `/home/box/agent-data/agents/925c3eaa-b0c0-440d-84a2-d28f7ed881e8/settings.json` (`notifyOnAgentUpdates: true`)
- Memory: `/home/box/agent-data/agents/925c3eaa-b0c0-440d-84a2-d28f7ed881e8/memory/profile.md`
- Memory log: `/home/box/agent-data/agents/925c3eaa-b0c0-440d-84a2-d28f7ed881e8/memory/log/2026-09.md`
- Usage gate mirror: `/home/box/agent-data/agents/925c3eaa-b0c0-440d-84a2-d28f7ed881e8/memory/USAGE_GATE.md`
- User shard by this agent: `/home/box/agent-data/user-memory/by-agent/925c3eaa-b0c0-440d-84a2-d28f7ed881e8/profile.md`
- This backup: `/workspace/925c3eaa-b0c0-440d-84a2-d28f7ed881e8-memory-backup.md`
- Researchy report: `/workspace/research/uk-boarding-vs-qc-deep-2026-10-05.md`
- Jev: `/workspace/typesafe-jev/` (client, thresholds, logs)

### Routines
- None configured for this agent at snapshot time (no automation_status rows owned here).

### Open work
- No active education/finance decision thread awaiting delivery beyond standing pending confirms below.
- Researchy informational handoff absorbed; no reply required unless path changes.

## Secrets placeholders only
- `[REDACTED:TYPESAFE_API_KEY]`
- `[REDACTED:boc-hk-credentials]`
- `[REDACTED:zhifu-broker-credentials]`
- `[REDACTED:gmail-oauth-token]`
- `[REDACTED:google-calendar-oauth-token]`
- `[REDACTED:google-drive-oauth-token]`
- No raw tokens, passwords, session cookies, or API keys in this snapshot.

## Pending confirms (listed only — do not act)
1. Elder overseas uni primary battlefield: US vs UK vs keep both (current working default = keep both; Justin dismissed earlier widget — assistant may hold until he reopens).
2. Education-fund currency buckets: exact USD vs GBP vs HKD mix (deferred; conceptual buckets only).
3. Younger post-primary: confirm stay local Band1/DSS-first (current working assumption).
4. Revisit boarding/QC lock only if Justin declares: UK music/boarding locked, or HKU medicine priority.

## Coverage checklist
- Identity / ONE JOB / ANTI-JOBS / fence / partners: yes
- Jev B+C TypeSafe + thresholds paths: yes
- Historical locks incl. 2026-10-05 Researchy default: yes
- Live family/fund/connectors/paths: yes
- Routines: none (stated)
- Open work: yes
- Pending confirms: listed, not acted
- Secrets: placeholders only
