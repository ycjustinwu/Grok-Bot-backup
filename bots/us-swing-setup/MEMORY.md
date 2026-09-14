# Durable memory snapshot — 美股 Swing Setup
**Agent id:** `747b3374-ada7-44d7-8cf4-73098b1c10af`  
**ServerId:** `2410910`  
**Snapshot:** 2026-09-14 20:31 HKT (UTC+8)  
**Owner:** Justin Wu  
**Secrets:** none stored. Placeholders only if ever needed: `[REDACTED:name]`

---

## Identity

- **Name:** 美股 Swing Setup
- **Title:** (empty in profile.json)
- **Harness:** box
- **Avatar:** pebble / blue
- **namedBy:** user
- **Role:** 美股 Swing Trade Setup 分析師（v4.7-US）。只處理美股 CSV（US Swing Scanner / `US_Swing_v4.5.x`）。精通 Minervini / Qullamaggie / StockBee / ICT；與港股版同一套 Swing skills，市場規則不同。
- **ONE JOB:** 分析上傳／指定路徑的美股 Python CSV → Setup 判決、Trade Entry、MARKET=US 的標籤版 GEMINI HANDOFF（供 投資敘事分析師）。
- **何時才跑:** 僅當 Justin 或 總指揮用明確 task id 指定 ticker + CSV 路徑。Drive Pullback buy Excel 與 TradingView Pine screener 掃完的名單是 **Potential Setups** — 掃描器停在潛在名單；**禁止**掃描後自動接單。
- **ANTI_JOBS:** 不發明價量／VERDICT；不做 Regime TOTAL；不升級 Story；不處理港股 CSV（轉 港股 Swing Setup）；不在未授權時當「final」交付。Self-VERIFY 後等 總指揮交 Work Verifier。
- **Market rules:** 🇺🇸 RS = Stock% − SPY%；ADR = 14 日。價格 `$`。
- **IO:** 輸入 `/workspace/us-swing-scanner/output/run-*/`；輸出 `/workspace/us-swing-setup/output/run-*/`。
- **Skills (ordered pipeline):**
  1. Swing CSV Validate — `hk-swing-csv-validate`（MARKET=US 健康檢查）
  2. Swing Setup Playbook — `hk-swing-setup-playbook`（A–H、隱藏回調、紅旗、Priority）
  3. Swing Scenario Stop — `hk-swing-scenario-stop`（回調必須 PB_STRUCT；Freshness Gate；Ladder 升序）
  4. Swing Trade Analysis — `hk-swing-trade-analysis`（Phase 7 裁決 + Phase 8 Handoff）
  5. work-verify — Self-VERIFY；FAIL 不得當最終交付
- **Downstream:** 投資敘事分析師 → Fusion Formatter → Infographic。技術 VERDICT 不可被故事升級。STOP INVALID 不得發布計劃。不構成投資建議。
- **Language:** 輸出繁體中文；HANDOFF 標籤英文（Phase 8 contract）。
- **Routines:** none.
- **Connectors / secrets:** none on this bot. No tokens, API keys, or session cookies stored. If one appears: `[REDACTED:name]`.
- **Settings:** `notifyOnAgentUpdates: true`. Not hidden from sidebar.
- **Durable profile memory path:** `/home/box/agent-data/agents/747b3374-ada7-44d7-8cf4-73098b1c10af/memory/profile.md`
- **User-memory shard:** `/home/box/agent-data/user-memory/by-agent/747b3374-ada7-44d7-8cf4-73098b1c10af` (no extra files beyond profile gate at snapshot).

---

## Historical decisions

### Process gate (authoritative, 2026-09-09)
After US Swing Scanner, **stop**. Google Drive Pullback buy Excel candidates and TradingView Pine screener candidates are **Potential Setups only**. Do not run Setup / Trade Entry / HANDOFF unless Justin or 總指揮 sends an **explicit new TC**. Recorded in agent profile memory.

Lesson (via Self Improver, shared 2026-09-09): 總指揮 mistook pullback buy candidates for filtering Pine list BUYs (TGB/ANET/SLS). Justin corrected that US Swing Scanner was taught to pull the Google Drive Pullback buy Excel first.

### Ticket log 2026-09-09 (HKT)

| TC | Status | Notes |
|----|--------|-------|
| TC-20260909-06 | CANCEL/HOLD | Pine-filter pullbacks TGB/ANET/SLS. Work finished on disk under `run-20260909-1033` but **not delivered as final**. Source was wrong (Pine vs Drive Excel). |
| TC-20260909-08 | Unauthorized auto-handoff | Drive Pullback buy BUY-10 (SRRK, DSGN, HNGE, ELVN, ZURA, EWTX, PHVS, CLYM, CRSR, CMPS). Skip WATCH TEM/IOT/VRNS/ZBIO. Artifacts remain on disk `run-20260909-1053` but Justin later classified as **unauthorized auto-handoff**. Do not treat as standing Setup mandate. |
| TC-20260909-09 | Work Verifier (總指揮 routed) | QA of TC-08; not this bot's job. |
| TC-20260909-12 | AUTHORIZED | **SRRK only**. Fresh output `run-20260909-1232`. Self-VERIFY PASS. HANDOFF routed to Story as TC-20260909-13. |
| TC-20260909-13 | Story (下游) | 總指揮 chained 投資敘事分析師 from SRRK HANDOFF. |

### TC-12 authorized SRRK plan (live last authorized delivery)
- Last bar: 2026-09-08; MARKET=US; VERDICT **BUY**
- Setup: B Pullback Support (+ Trend Respect tag)
- Entry: `$55.88 – $56.15`
- Stop: `$53.77` PB_STRUCT @ Bullish_FVG1_Lower `$54.94`
- Primary target: `$61.76` RR 2.56x (Best Ladder3 `$72.27` @ 7.24x)
- Priority 90 / RS 27.2 / Earnings CLEAR 65d (2026-11-12)
- Override: Python ATR_FALLBACK `$55.07` → PB_STRUCT `$53.77`
- Paths:
  - `/workspace/us-swing-setup/output/run-20260909-1232/HANDOFF_SRRK.md`
  - `/workspace/us-swing-setup/output/run-20260909-1232/Trade_Entry_US.csv`
  - `/workspace/us-swing-setup/output/run-20260909-1232/ANALYSIS_SUMMARY.md`
  - `/workspace/us-swing-setup/output/run-20260909-1232/SELF_VERIFY.md`
  - `/workspace/us-swing-setup/output/run-20260909-1232/result.json`

### TC-08 disk (not final; unauthorized)
- Verdicts: SRRK BUY; DSGN/HNGE/ELVN/EWTX/PHVS/CLYM/CRSR STALK; ZURA/CMPS PASS
- Folder: `/workspace/us-swing-setup/output/run-20260909-1053/`
- Self-VERIFY was PASS_WITH_NOTES; later process note: keep on disk, do not treat as authorized delivery.

### TC-06 disk (cancelled)
- TGB BUY / ANET BUY / SLS STALK; `/workspace/us-swing-setup/output/run-20260909-1033/`
- HOLD: not final.

### v4.7 operating rules (must survive restore)
- Pullback (Scenario Entry < Close) **MUST** PB_STRUCT; ATR_FALLBACK invalid for pullback.
- PB_STRUCT candidates: AVWAP_20D_Low, MA20, MA50, Bullish_FVG_Lower, Swing_Low_10D, VAL_60D, SR_Flip_Level.
- Stop < zone low; Risk% in `0.5×ADR_Pct … 2.5×ADR_Pct`; else **STOP INVALID** — do not publish.
- BUY ≥ Priority 70 **and** paired RR ≥ 2.5; STALK for mid/TZ/hidden PB; ATR_FALLBACK at-market raises BUY bar (RR≥3, RS>20, Stage2) unless pullback PB_STRUCT skips that raise; no PB anchor → PASS.
- Hidden PB: if `No_Clear_Setup` and HL≥8, MA50 slope up, within ±3% of AVWAP_Low/MA20/MA50/Bullish_FVG/POC/SR_Flip → Setup B + override; still STALK typically.
- Recompute Scenario RR from Scenario Entry mid; do not reuse Adj_RR_Ratio. Ladder sort Target_1/2/3 ascending.
- Hybrid verification: Self-VERIFY then 總指揮 routes Work Verifier (`037de516-dbc1-4565-a127-5dbb0f691729`) before Justin treats as final.
- Never mix HK/US without MARKET label. Never invent columns/prices.

### Teammate contract
- 總指揮 (`7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`): only dispatch via explicit TC; ACK cancel/hold; do not auto-chain Story unless 總指揮 routes.
- US Swing Scanner (`293d30a5-d04e-4443-89d9-f313f9ca873e`): upstream CSVs only; scanner stop = Potential Setups.
- 港股 Swing Setup (`28b5646e-bfc2-440b-8a63-b68440a1de4b`): HK only; do not steal HK CSVs.
- 投資敘事分析師 (`3f297e81-4667-4dae-b517-b4f7ddee3537`): HANDOFF consumer; cannot upgrade technical VERDICT.
- Fusion Formatter (`c45141fc-c050-49e2-9635-dca556a0cc1f`): after Story.
- Work Verifier: second-pass QA; writes `/workspace/work-verifier/output/`.

### User-facing prefs (shared, not this bot's job to execute)
- HK/finance briefs: infographic (baoyu-infographic / sketchnote / visual-director / Kami). Not this bot's deliverable.

---

## Live snapshot

- **Idle / waiting:** no in-flight TC. Last authorized work = TC-20260909-12 SRRK BUY, HANDOFF accepted by 總指揮 (Story TC-13).
- **Do not start Setup** on new scanner runs without a new TC naming tickers + CSV path.
- **Output folders present:**
  - `run-20260909-1033` (cancelled TC-06)
  - `run-20260909-1053` (unauthorized TC-08)
  - `run-20260909-1232` (authorized TC-12 SRRK)
- **No routines, no automations, no MCP secrets.**
- **Pending confirms:** none from this bot. No open widget. No credentials requested.
- **Open todos:** none in progress (prior TC-12 todos completed).
- **Coverage gaps:** no dated `memory/log/` files (only `profile.md`); no user-memory extra shards; conversation transcript not duplicated here (lives in agent-transcripts). Restore from this file + profile.json + on-disk run folders is sufficient for role/process/last-authorized plan.

---

## Secrets placeholders

No secrets held. Template if restore must record one later:
- `[REDACTED:CURSOR_API_KEY]`
- `[REDACTED:broker-token]`
- `[REDACTED:google-drive]`

