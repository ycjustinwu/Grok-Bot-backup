# Memory disaster-recovery snapshot — 全富決策副手
- Agent id: `925c3eaa-b0c0-440d-84a2-d28f7ed881e8`
- Server id: `2410937`
- Snapshot written: 2026-10-03 (HKT)
- Audience: 记忆管家 recovery pack

## Identity
- Name: 全富決策副手
- Title: (empty)
- ONE JOB: 家庭／財務／教育／生活重大決策的分析與行動建議（非旅行行程表）
- Communication: finance/tech = zero fluff (conclusion → table/code); family/life = high-execution care (actions, logistics, risk; wife-facing plans always include Plan B)
- Skills pipeline: Decision Mode Switch → Live Search Mandates → Second-Order Reasoning → Deputy Output Modes (A/B/C) → Financial Life Deputy
- Fence vs 旅行計劃助手: own investment/education/liquidity/family-rhythm decisions; hand off full itineraries/flights/day routes to 旅行計劃助手
- Anti-jobs: no full multi-day travel itineraries; no fabricated school admissions; mark speculation 需驗證; check HK ID + capital pool + study-fund / family-day impact before send
- User portrait (role config): Justin Wu; HK finance 12y+; husband + two sons ~9/~12; capital pool ~HK$5M (BOC HK / 致富); goals include UK study-fund FX/liquidity, parenting and marriage quality, cognitive upgrade
- Avatar: shape hex, color violet
- Connectors expected in use: Gmail, Google Calendar, Google Drive (X available on account; not core to this bot)
- Standing usage gate (2026-09-20, via 總指揮): reuse a fresh artifact before new research; same approach failed twice → stop and report; no tools needed → chat only; prefer connector/API over clicking a site; do not create more bots or routines to save usage. Canon: `/workspace/fleet-policies/USAGE_GATE.md`

## Historical decisions
- (2026-09-07) Paused default UK secondary boarding path: VAT 20% on UK private school fees from 2025-01-01; all-in boarding often ~£45k–£70k/year per child; cost/cash-flow case strong vs ~HK$5M pool.
- (2026-09-07) Corrected blind spot: “boarding schools cannot adapt in the AI era” is a weak exit reason; prefer cash-flow + optionality framing with wife.
- (2026-09-07) Default reframed: elder continues Queen’s College (皇仁); UK boarding only as later Sixth Form option if clear incremental benefit; younger assessed independently; education pool prioritizes university tuition + USD/GBP liquidity, not mid-school boarding burn.
- (2026-09-07) Paths split: elder (~12, Queen’s College) toward US/UK university; younger (~9, 高主教書院小學 + British Council Primary Plus) HK-local secondary with English as option.
- (2026-09-07) Wife involved in sons’ schooling decisions; wife-facing communications require Plan B and “optionality not downgrade” framing.
- Pending user choice (widget unanswered, still open as of 2026-10-03): elder overseas uni primary battlefield — US vs UK vs keep both; or first do fund currency allocation USD/GBP/HKD.

## Live snapshot
### Family / schooling
- Elder son ~12: Queen’s College (皇仁書院), Band 1A government boys’ day school; tuition ≈ free (admin/PTA level only).
- Younger son ~9: Raimondi College Primary (高主教書院小學); English strengthened via British Council Primary Plus.
- Education fund pool: ~HK$5M relevant to schooling/uni decisions (BOC HK / 致富 per role config).
- Working thesis: keep QC seat for elder; burn window for overseas spend delayed to uni (3–4 years UK / 4 years US) rather than 5–7 years boarding now.

### Cost anchors last researched (2026-09-07; re-verify before acting)
- GBP/HKD ≈ 10.61; USD/HKD ≈ 7.84 (mid-market; bank worse).
- UK boarding (secondary): ~£40k–£60k fees; intl all-in often £45k–£70k/year.
- UK UG intl: tuition ~£12k–£38k/year; all-in often £27k–£55k/year.
- US: public OOS tuition sticker avg ~US$31.9k; private nonprofit ~US$45k; COA often US$50k–90k+/year.

### Ops / connectors
- Use Gmail, Google Calendar, Google Drive by default for schedule/email-aware decisions; do not ask Justin to paste calendar/mail when connectors work.
- Hybrid verification fleet rule (via 總指揮): high-stakes bot outputs may route through Work Verifier (`037de516-dbc1-4565-a127-5dbb0f691729`); this bot’s education/finance briefs are decision support — apply live search mandates; mark 需驗證 on speculative bits.

### Agent-owned memory files (source of truth on box)
- `/home/box/agent-data/agents/925c3eaa-b0c0-440d-84a2-d28f7ed881e8/memory/profile.md`
- `/home/box/agent-data/agents/925c3eaa-b0c0-440d-84a2-d28f7ed881e8/memory/log/2026-09.md`
- User shard contributed by this agent: `/home/box/agent-data/user-memory/by-agent/925c3eaa-b0c0-440d-84a2-d28f7ed881e8/profile.md`

## Secrets placeholders only
- `[REDACTED:boc-hk-credentials]`
- `[REDACTED:zhifu-broker-credentials]`
- `[REDACTED:gmail-oauth-token]`
- `[REDACTED:google-calendar-oauth-token]`
- `[REDACTED:google-drive-oauth-token]`
- No raw tokens, passwords, session cookies, or API keys included in this snapshot.

## Coverage
- Identity / ONE JOB / fence / anti-jobs / usage gate: yes
- Family schooling decisions + fund reframing: yes
- Live connector expectations: yes
- Pending confirms: yes (US vs UK primary; fund FX split; younger local-first)
- Routines: none configured for this agent at snapshot time
- Secrets: placeholders only

## Pending confirms (for Justin)
1. Elder overseas uni primary market: US / UK / keep both open.
2. Education-fund currency buckets: target USD vs GBP vs HKD mix.
3. Whether younger’s post-primary track should stay local Band1/DSS-first (current working assumption).
