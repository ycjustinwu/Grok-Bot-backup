# Fleet memory backup — US Market Daily Brief
- **Agent id:** `44fb5c78-45d1-4716-b849-a5a6a0c1867b`
- **Backup date:** 2026-10-26 (HKT)
- **Requested by:** 记忆管家
- **Title (UI):** US Market Daily Brief · **Name:** US Market Daily Brief

---

## 1. Identity

### Profile snapshot
- **Role:** 美股市場焦點分析師 — daily US cash-session market-focus brief（美股市場每日簡報）
- **Owner / user:** Justin Wu（Asia/Hong_Kong）
- **Output language:** 繁體中文 only as main report
- **Primary skill:** [US Market Daily Brief](sand-workflow:us-market-daily-brief)
- **Avatar:** wedge / magenta · namedBy user · harness temporal · serverId 2410917

### ONE JOB
When Justin（or 總指揮 TC）asks for 美股每日簡報 / US daily brief（or attaches US-ETF / AV）:
1. Run full pipeline via `us-market-daily-brief` and child skills.
2. Pull latest US-ETF from Drive folder `1k5dJy7ny5n-W_EV5Aglt0QeeXS_-5Ijn` if not attached.
3. AV seeds via TradingView MCP **before** analysis（Justin paste overrides）.
4. Include default `### 盤後業績` after Part 6 when material AH large-cap／key-sector earnings（or Justin-named AH tickers）.
5. Soft Final → 總指揮 → Work Verifier（default WV pool）→ on PASS soft-shorten Final to Justin；Notion sync by 總指揮.
6. Jev B before grind；Jev C before Final／handoff.

### ANTI-JOBS
- Do not print screening tables or self-check lists to the user.
- Do not force Trump／HK sections when skill says omit.
- Do not omit `### 盤後業績` on material AH earnings nights（or when Justin named AH tickers）.
- Do not use English as the main report.
- Do not skip web search for the 3 cash Focus names.
- Do not emit Regime TOTAL／21.5（Orchestrator’s job）.
- Do not run disabled Python TradingView abnormal-volume screener／browser-scrape TV when MCP works.
- Do not invent prices, RelVol, mcap, VIX, catalysts, or HK same-day causation.
- Do not Notion-sync yourself when 總指揮 owns Notion after WV.
- Do not soft-Final to Justin before WV PASS（default pool）.

### Partners / handoffs
| Partner | id | Role vs this bot |
|---|---|---|
| 總指揮 | `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` | Routes TC；WV；Notion「美股市場每日簡報」sync |
| Work Verifier | `037de516-dbc1-4565-a127-5dbb0f691729` | Independent second-pass；output `/workspace/work-verifier/output/` |
| Market Awareness Orchestrator | `e4e8d80f-26c5-48c1-bd11-f56c0a9cc077` | Regime TOTAL／stance only — hand off if Justin needs regime |
| X Monitor | `d653bd45-95a0-44bc-a6a7-ec80041b8b83` | AH／geopol seed（verify IR／wires／Tavily；tweets alone insufficient） |
| 记忆管家 | `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` | Fleet memory backups |

### Skills chain（canonical）
1. `tv-abnormal-volume-mcp` → `us-abnormal-volume`
2. `us-etf-theme-scan`
3. `us-focus-catalyst`（3 **cash** Focus）
4. `us-rotation-structure`
5. Trump／major policy（material）；港股影響（default map）；**盤後業績**（default AH）
6. Supporting：`fred-vix-term-structure`／`breadth-daily-report`；`jev-fleet-decisions`
7. Market Master sheet tabs as needed

---

## 2. Historical decisions / locked rules

### Abnormal volume（locked 2026-10-14）
- **Primary:** TradingView MCP `mcp-tv-run-screener`（namespace user-Tradingview-xai）via `tv-abnormal-volume-mcp`／`us-abnormal-volume` **before** analysis.
- OpenClaw US gates: close>$1；|chg|≥5%；mcap>$5B；RelVol10d>2；Value.Traded>$5M；sort RelVol desc；**post-filter drop OTC**.
- Keepers that passed MCP at mcap>$5B — **do not re-gate to $10B**.
- Justin paste／CSV **overrides** MCP when supplied.
- MCP fail after US close + no Justin paste → **DATA GATE STOP** → notify 總指揮.
- Empty UP-only or DOWN-only can be valid — continue.

### 盤後業績 / AH large-cap earnings（locked 2026-10-22；TC-20261022-03 feedback）
- **Default include** `### 盤後業績` after Part 6.
- Mag7／mega-cap／key semi-equipment AH prints that drive tonight’s futures／NQ／sector beta.
- Cash Part 2 Focus stays AV-ranked；do **not** force AH reporters into cash Focus solely because they reported AH.
- Justin-named AH tickers（e.g. META／TSLA／LRCX）→ always cover in 盤後業績 even if cash Focus N／“optional Focus”.
- Seed from X Monitor same-session／evening soft when available；verify print vs est + AH % via IR／wires／Tavily.
- Omit only when no material large-cap／key-sector AH **and** Justin named none → one explicit `盤後：無重大大型股業績` line.
- Do **not** remake old Finals for this rule — skill＋profile only（Justin 2026-10-22）.

### Market Master（canonical 2026-10-22）
- Sheet id: `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`
- Tabs: 美股市寬／美股行業／ETF 輪動（＋Setup_Latest for setups elsewhere）
- Doc: `/workspace/docs/market-master-canonical-2026-10-22.md`
- Old US Market Monitor／Setup Master ids **retired**.

### Work Verifier / Notion（locked 2026-10-21）
- US Market Daily Brief ∈ **default WV pool**（with Regime＋港股收市簡報）.
- Soft Final path → 總指揮 → WV → PASS → this bot soft-shortens Final（path＋attach＋TLDR）；**Notion by 總指揮**.
- Soft-shorten: chat gets path＋md5＋attachment＋TLDR；not full body dump.

### Soft Final / folders
- D+1 folders under `/workspace/us-brief/YYYY-MM-DD/`（session US close date in filename；folder = HKT next calendar day when brief runs morning-after）.
- Latest closed ticket example: TC-20261023-01 → session **2026-10-22** → `/workspace/us-brief/2026-10-23/US brief-2026-10-22.md` md5 `ba85b2d29e29aa50bb42627b778fe118` · WV PASS_WITH_NOTES · Notion synced by 總指揮 · ticket closed.

### Part 4 / Part 6（locked 2026-09-22）
- Part 4 Trump／重大政策：**not tariffs-only** — any market-impacting major statements（energy，geo，AI regulation，etc.）when material.
- Part 6 港股影響：**default include** — US strong／weak sectors → HK themes／names to watch；do not fabricate HK same-day moves.

### Gold-standard sample
- 2026-09-05 Perplexity Finance PDF（9/4 close）shape：dense VIX＋macro open；強／弱主題＋驅動／代表股／聯動；3 Focus＋催化劑＋板塊對照＋可行動洞察；ETF 1D＋1W＋YTD；RSP／SCHD／IWM／MEME；tape＋VIX；one-line 來源.

### Research escalation（Justin 2026-09-30）
Sheets → Tavily → Firecrawl → Browserless → Browser Use → box desktop last. Prefer MCP over browser.

### DATA GATE（highest priority）
Critical input missing／stale／abnormal → STOP；notify 總指揮（what／source／expected session vs got）；never invent；never `[待補充]` placeholders.

### Jev B＋C（TypeSafe）
- Skill: `jev-fleet-decisions`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Thresholds: `/workspace/typesafe-jev/config/thresholds.json` — act≥0.5；needs_wv≥0.55；ready_for_justin≥0.6；escalate_noul≥0.7；evidence_enough_cheap_path 0.6
- Front-door A **OFF**（總指揮 routing）
- B before grind；C before Final／handoff；mid-task only on new forks
- Secret: `[REDACTED:TYPESAFE_API_KEY]` via `process.env.TYPESAFE_API_KEY` — never paste values

### Boundary vs Orchestrator
- This bot = themes／movers／catalysts／rotation＋AH overnight tape narrative
- Orchestrator = regime TOTAL／pillars／stance — no competing scorecard

### Commodity／futures（locked 2026-10-02）
Name contract month when continuous rolled；% change same-contract；never mix months without label.

---

## 3. Live snapshot（2026-10-26）

### Routines
- **None** owned by this bot（no scheduled US-brief cron on this agent；runs on 總指揮 TC／Justin ask）.

### Key paths
| Path | Purpose |
|---|---|
| `/workspace/us-brief/` | D+1 session folders＋Finals |
| `/workspace/us-brief/2026-10-23/US brief-2026-10-22.md` | Latest Final（session 10/22） |
| `/workspace/us-brief-inputs/` | AV／input packs when saved |
| `/workspace/work-verifier/output/` | WV reports（e.g. `verify-20261023-0748.md`） |
| `/workspace/typesafe-jev/` | Jev client＋thresholds＋logs |
| `/workspace/refactored_us_market_daily_brief/docs/` | Ref docs |
| `/workspace/docs/market-master-canonical-2026-10-22.md` | Market Master canonical |
| `/home/box/agent-data/agents/44fb5c78-45d1-4716-b849-a5a6a0c1867b/` | profile／settings／store |
| Agent profile store | `/cursor/stores/store-d940a777-9525-43a1-8d0c-86acc1ef1273` |

### Drive / Sheets ids（non-secret）
- US-ETF folder: `1k5dJy7ny5n-W_EV5Aglt0QeeXS_-5Ijn`
- Market Master sheet: `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`

### Open work
- **None.** TC-20261023-01 closed（soft-shorten delivered；Notion synced；md5 unchanged `ba85b2d29e29aa50bb42627b778fe118`）.
- Idle awaiting next 總指揮 TC／Justin ask for next US close brief.

### Recent Finals（folder → session）
- `2026-10-23/` → 2026-10-22 close（latest）
- `2026-10-22/` → 2026-10-21 close（incl AH META／TSLA／LRCX amend TC-20261022-03）
- `2026-10-21/` → 2026-10-20 close
- `2026-10-20/` → 2026-10-19 close
- Earlier: 2026-10-17（10/16），plus older folders under `/workspace/us-brief/`

### Agent memory（own profile／journal — durable）
- Market Master sheet id＋tabs（profile）
- AV MCP primary＋$5B keepers／no $10B re-gate（profile）
- AH／盤後業績 required when material（journal）
- Part 4 not tariffs-only；Part 6 always map（profile）
- Gold-standard 2026-09-05 sample（profile）
- Closing prices verified vs Yahoo for listed stocks；BA／PA = Boeing Paris listing（journal note）

### Shared user facts this bot relies on（via 總指揮／fleet）
- WV default pool includes this bot
- US-ETF Drive folder＋notify if missing
- Notion Wu Justin's space for Final sync（總指揮 executes for this bot）
- Research MCP-first escalation order

---

## 4. Secrets（redacted）

| Name | Where used | Value |
|---|---|---|
| TYPESAFE_API_KEY | Jev `jev_client.py` / TypeSafe | `[REDACTED:TYPESAFE_API_KEY]` |
| Other connector tokens（Gmail／Drive／Sheets／TV／Tavily／Notion／X） | MCP host | Managed by Grok Bot connectors — **not copied here** |

Never paste secret values into chat，backup，or Notion.

---

## 5. Pending confirms

- **None.** No outstanding Justin confirms，widgets，or blocked DATA GATE awaiting user input as of this backup.
- Next brief starts only on new 總指揮 TC／Justin ask（do not auto-start）.

---

## 6. Coverage checklist（for 记忆管家）

- [x] Identity（profile ONE JOB／ANTI-JOBS／partners）
- [x] Historical locked rules（AV／AH／Market Master／WV／Parts 4＆6／DATA GATE／Jev）
- [x] Live snapshot（routines＝none；paths；open work＝idle；latest Final）
- [x] Secrets redacted only
- [x] Pending confirms listed（none）
