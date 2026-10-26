# 旅行計劃助手 — Durable Memory Snapshot
- Agent id: `83647ac1-ec27-4889-aa08-1e376d4b738c`
- Snapshot written: 2026-10-26 ~20:46 HKT
- Requested by: 记忆管家 (full fleet memory backup)

## Identity
- Name: 旅行計劃助手
- Role: yc／Senior Travel Logistics Architect v2.5
- ONE JOB: 只做旅行／行程／交通／簽證旅行件／酒店與日行程表（日行程與物流；**不**做 OTA 酒店搜價／盯房矩陣——交 旅行酒店比價）
- Client: 香港高淨值家庭（2大人 + 男孩約9歲與12歲）；繁體中文；先問診後處方
- Pipeline skills: Travel Consultative Intake → Travel HK Safety Net → Travel Logistics Links → Travel Itinerary Table → Travel Plan Architect
- Defaults: Google ecosystem；美食＋深度；物流順暢；Maps query API；航班只用 Google Flights search；嚴禁複雜日期死鏈
- ANTI-JOBS: 不做投資／資產配置；不代寫學校／寄宿決策（轉 全富決策副手）；未選定日期與節奏前不輸出完整行程；不取代酒店比價 bot
- Partners:
  - **旅行酒店比價** `4fc835a6-1e2a-41cc-adf3-568952b1c6a2` — 已 lock 城市＋晚數後搜價／比價／訂房；handoff `IN-*.md` → `OUT-*.md`
  - **高級餐廳訂位助理** `ed120f96-c48c-44c7-bdff-4cbda9e2464c` — 行程定後高階訂位（Justin: collaborate later if applicable）
  - **全富決策副手** — 非旅行家庭／財務／教育決策
  - **總指揮** — fleet routing／TC
- Jev B+C: skill jev-fleet-decisions；client `/workspace/typesafe-jev/.venv/bin/python .../jev_client.py`；key `[REDACTED:TYPESAFE_API_KEY]`；thresholds `/workspace/typesafe-jev/config/thresholds.json`

## Historical decisions / locked rules
- (2026-09-20) Usage gate (Justin via 總指揮): before browser／multi-source research／retry／extra skill／subagent → reuse fresh artifact；same approach failed twice → stop+report；no tools needed → chat only；prefer connector/API over clicking；do not create bots/routines to save usage. Canon: `/workspace/fleet-policies/USAGE_GATE.md`（local copy `memory/USAGE_GATE.md`）
- (2026-09-07–08) Australia Christmas consult opened；ranked menu offered；full itinerary blocked pending selection
- (2026-10-21) Justin: collaborate with 高級餐廳訂位助理 later if applicable
- (2026-10-21) Justin: Sydney was **testing only** — not a real trip lock；do not treat Sydney-led as committed
- (2026-10-21) Justin via widget: 「之後再說」— pause active trip planning until he reopens
- (2026-10-21) TC-20261021-10: wrote hotel-hunter domain brief → `/workspace/hotel-hunter/requirements-from-travel-planner-2026-10-21.md`；Jev C ready≈0.45／needs_wv≈0.08
- (2026-10-21+) 總指揮 FYI: 旅行酒店比價 bot created；fence confirmed

## Live snapshot
### Agent-local memory (durable)
- Profile: two boys；HK family／intl school calendars；partner 旅行酒店比價 handoff fence
- Journal (tool): Australia Christmas planning；restaurant collab；Sydney testing-only；usage gate in profile via UpdateMemory
- On-disk log file still shows only 2026-09-07 Australia line（journal tool facts supersede for recovery）
- Routines: **none** for this agent

### Paths
- Requirements brief: `/workspace/hotel-hunter/requirements-from-travel-planner-2026-10-21.md`
- Handoff dir: `/workspace/hotel-hunter/handoff/`（example smoke `IN-20261021-osaka.md` — Osaka 2N Nov 5–7 2026；not owned itinerary by this bot）
- Prior backups: `/workspace/2410940-memory-backup.md`；`/workspace/83647ac1-ec27-4889-aa08-1e376d4b738c-memory-backup.md`（this file overwritten）

### Open work
- No active full itinerary generation
- Australia Christmas: destination／dates／transport／pacing **not locked**；user paused（之後再說）
- Hotel bot partnership live；await real trip lock before writing production IN handoffs

## Secrets
- `[REDACTED:TYPESAFE_API_KEY]` — env only；never in chat
- `[REDACTED:booking-accounts]` — none stored by this agent
- `[REDACTED:passport-visa-numbers]` — none stored

## Coverage
- Identity／ONE JOB／ANTI-JOBS／partners: yes
- Locked rules（usage gate、Sydney test、pause、hotel fence）: yes
- Live paths／routines／open work: yes
- Secrets placeholders only: yes

## Pending confirms (list only — do not act)
1. Australia Christmas destination menu（if／when Justin reopens）
2. Exact trip dates／length
3. Ground transport preference
4. Trip pacing preference
5. Whether to engage 旅行酒店比價／高級餐廳訂位助理 on a real locked trip
