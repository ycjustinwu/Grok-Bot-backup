# 旅行計劃助手 — Durable Memory Snapshot
- Agent id: 83647ac1-ec27-4889-aa08-1e376d4b738c
- Snapshot written: 2026-10-03 (Asia/Hong_Kong)
- Requested by: 记忆管家 (full fleet memory backup)

## Identity
- Name: 旅行計劃助手
- Role: yc／Senior Travel Logistics Architect v2.5
- ONE JOB: 只做旅行／行程／交通／簽證旅行件／酒店與日行程表
- Client frame: 香港高淨值家庭（2大人 + 男孩約9歲與12歲）；輸出繁體中文；先問診後處方；邏輯與執行力優先
- Pipeline skills: Travel Consultative Intake → Travel HK Safety Net → Travel Logistics Links → Travel Itinerary Table → Travel Plan Architect
- Defaults: Google ecosystem；美食＋深度體驗；物流順暢；Maps query API；航班只用 Google Flights search 連結；嚴禁複雜日期死鏈
- Fence vs 全富決策副手: 本 bot 擁有行程／航班連結／每日動線／簽證旅行實務／行李與時差節奏；投資／教育／資金配置／非旅行家庭決策轉介 全富決策副手
- Anti-jobs: 不做投資建議或資產配置；不代寫學校／寄宿決策；未選定日期與節奏前不輸出完整行程
- Standing usage gate (Justin via 總指揮, 2026-09-20): before browser / multi-source research / retry / extra skill load / subagent, reuse a fresh artifact if one exists; same approach failed twice → stop and report; no tools needed → chat only. Prefer connector or API over clicking a site. Do not create more bots or routines to save usage. Canon: /workspace/fleet-policies/USAGE_GATE.md

## Historical decisions
- (2026-09-07) User opened first consult: Christmas-period family trip to Australia; asked for recommendations
- (2026-09-08) Presented Top-tier Australia Christmas menu for family with boys ~9 & 12:
  1. Sydney-led (primary recommendation)
  2. Gold Coast + Brisbane
  3. Melbourne + Great Ocean Road
  4. Sydney + Melbourne dual-city (10–12+ days)
  5. Cairns / Great Barrier Reef (wet-season caveat)
- (2026-09-08) Noted typical HK international-school winter break window ~mid-Dec to early Jan; recommended ~10–14 day trip length; did not generate full itinerary (intake rule: wait for menu selection)
- (2026-09-14) Prior disaster-recovery snapshot written to /workspace/2410940-memory-backup.md (63 lines) and acknowledged to 记忆管家
- Fence decision (profile): non-travel family/finance/education decisions → 全富決策副手; high-stakes market QA is outside this bot’s job

## Live snapshot
### Agent-local durable memory
- Profile: The user has two boys
- Profile: The user's family is based in Hong Kong and follows Hong Kong international school calendars
- Profile: Standing usage gate (see Identity)
- Log: Planning a Christmas-period family trip to Australia

### Relevant shared user facts (travel-adjacent)
- Elder son (~12) at Queen's College (皇仁書院)
- Younger son (~9) at Raimondi College Primary (高主教書院小學); British Council Primary Plus for English
- Justin has Gmail, Google Calendar, Google Drive connected (used by 全富決策副手 for scheduling/email-aware decisions — available context for trip calendar later, not owned by this bot)

### Conversation state (incomplete intake)
- Destination country locked: Australia
- Season locked: Christmas / school winter break period
- Menu selection: PENDING (widget offered 2026-09-08; no user pick yet)
- Exact dates: NOT locked
- Transport (self-drive / transit / private transfer): NOT asked / NOT locked
- Pacing (packed / balanced / slow): NOT asked / NOT locked
- Full itinerary: NOT generated (correctly blocked until selection)

## Secrets
- [REDACTED:any-api-tokens] — none stored by this agent
- [REDACTED:booking-accounts] — none stored
- [REDACTED:passport-visa-numbers] — none stored

## Coverage
- Identity / role / fence / usage gate: yes
- Agent profile + log memory files: yes
- Active Australia Christmas consult state: yes
- Pending intake locks: yes
- No credentials or booking secrets held

## Pending confirms (user)
1. Australia Christmas destination menu selection (Sydney / Gold Coast+BNE / Melbourne+GOR / dual-city / Cairns / mix)
2. Exact trip dates / length within Christmas window
3. Ground transport preference
4. Trip pacing preference
