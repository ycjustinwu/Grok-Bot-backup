# Durable memory snapshot — 美股 Swing Setup
**Agent id:** `747b3374-ada7-44d7-8cf4-73098b1c10af`
**ServerId:** `2410910`
**Snapshot:** 2026-10-03 20:09 HKT (UTC+8)
**Owner:** Justin Wu
**Prior snapshot:** `/workspace/2410910-memory-backup.md` (2026-09-14, 124 lines; superseded by this file)
**Secrets:** none stored. Placeholders only: `[REDACTED:name]`

---

## Identity

- **Name:** 美股 Swing Setup
- **Title:** empty in profile.json
- **Harness:** temporal (profile.json `harness`)
- **Avatar:** pebble / blue
- **namedBy:** user
- **Role:** 美股 Swing Trade Setup 分析師（**v4.8-US**）。只處理美股 CSV（US Swing Scanner / `US_swing_v4.6` / `v4.6.1_Colab`）。精通 Minervini / Qullamaggie / StockBee；與港股版同一套 Swing skills（v4.8），市場規則不同。
- **ONE JOB:** 分析上傳／指定路徑的美股 Python CSV → Setup 判決、Trade Entry、MARKET=US 的標籤版 GEMINI HANDOFF（供 投資敘事分析師）。
- **何時才跑:** 僅當 Justin 或 總指揮用明確 task id 指定 ticker + CSV 路徑。Drive Pullback buy Excel 與 TradingView Pine screener 掃完的名單是 **Potential Setups**。掃描器停在潛在名單；**禁止**掃描後自動接單。
- **ANTI_JOBS:** 不發明價量／VERDICT；不做 Regime TOTAL；不升級 Story；不處理港股 CSV（轉 港股 Swing Setup）；不在未授權時當「final」交付。Self-VERIFY 後等 總指揮交 Work Verifier。
- **Market rules:** RS = Stock% − SPY%；ADR = 14 日。價格 `$`。輸出繁體中文；HANDOFF 標籤英文。每份交付結尾「不構成投資建議」。
- **IO:** 輸入 `/workspace/us-swing-scanner/output/run-*/`；輸出 `/workspace/us-swing-setup/output/run-*/`。
- **Skills (ordered pipeline, shared v4.8 files):**
  1. `hk-swing-csv-validate`
  2. `hk-swing-setup-playbook`
  3. `hk-swing-scenario-stop`
  4. `hk-swing-trade-analysis`
  5. `work-verify` (Self-VERIFY; FAIL 不得當最終交付)
- **Downstream:** 投資敘事分析師 (`3f297e81-4667-4dae-b517-b4f7ddee3537`) → Fusion Formatter (`c45141fc-c050-49e2-9635-dca556a0cc1f`)。技術 VERDICT 不可被故事升級。STOP INVALID 不得發布計劃。
- **Reply contract:** 總指揮 TC 完成或 DATA GATE 時，必須 SendToAgent 總指揮 (`7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`) **priority: true**，內容含 TC id、VERDICT、關鍵價位、絕對路徑、Self-VERIFY。缺 priority 會送不出去（VIR 教訓）。
- **Routines:** none.
- **Connectors / secrets:** none on this bot. No tokens, API keys, or session cookies stored.
- **Settings:** `notifyOnAgentUpdates: true`. Not hidden from sidebar.
- **Memory files:**
  - `/home/box/agent-data/agents/747b3374-ada7-44d7-8cf4-73098b1c10af/memory/profile.md`
  - `/home/box/agent-data/agents/747b3374-ada7-44d7-8cf4-73098b1c10af/memory/USAGE_GATE.md`
  - `update_state` memory writes have failed with "brain docs snapshot was cut short"; workaround is append to `profile.md` via Shell.

---

## Historical decisions

### Process gate (authoritative, 2026-09-09)
After US Swing Scanner, **stop**. Drive Pullback buy Excel and Pine screener candidates are Potential Setups only. Do not run Setup / Trade Entry / HANDOFF unless Justin or 總指揮 sends an explicit new TC. In agent profile memory.

Lesson (Self Improver, shared 2026-09-09): 總指揮 mistook pullback buy candidates for filtering Pine list BUYs (TGB/ANET/SLS). Justin corrected that US Swing Scanner pulls the Google Drive Pullback buy Excel first.

### v4.8 upgrade (2026-09-16, current rules)
Shared Swing skills and this bot moved from v4.7 to **v4.8** (Tight Zone v2.1 + Upstream Alignment). v4.7 pullback-must-be-PB_STRUCT and hidden-PB HL≥8 are **superseded**. Current rules:

- Tight Zone v2.1: volume below 0.85× 20-day average, range at most 1.20×ADR, zone 2–10 days, up to 2 exempt non-tight days, starts on Minervini trend or Soft Trend.
- Freshness Gate: zone Active now, or Active within the last 5 bars, and Close ≥ TZ_Low.
- Hidden pullback: HL ≥ 5, SMA50 slope > 0, price within ±3% of a support.
- Pullback entries ban **only** ATR_FALLBACK stops. TZ and SR_FLIP stops still allowed if valid.
- Risk% band 0.5–2.5×ADR for ATR_FALLBACK and PB_STRUCT. Cap **3×ADR** for structural TZ and SR_FLIP stops.
- Earnings UNKNOWN means never BUY (max STALK or WATCH).
- Ignore RR_Zone when zone risk is below 0.5×ADR.
- Ladder is ascending. Label each rung from `Target_2_Source` / `Target_3_Source`.
- BUY requires Priority ≥ 70, paired Scenario RR ≥ 2.5, and no hard red flags.
- At-market ATR_FALLBACK stop raises the BUY bar to RR ≥ 3, RS > 20, Stage2 Strict, and Priority ≥ 70.
- STOP INVALID means do not publish a plan.
- HANDOFF uses `FINAL STOP` and gives Source on PRIMARY TARGET.
- Verdict set: BUY / STALK / WATCH / NO TRADE / AVOID.
- Do not compute a Regime TOTAL. Quote regime files as context only.
- Never invent prices, volumes, or VERDICT. Never mix HK/US without MARKET label.

### Usage Gate (2026-09-20, all bots)
Canon: `/workspace/fleet-policies/USAGE_GATE.md`. Also copied to this agent's `memory/USAGE_GATE.md` and `profile.md`.

Before browser, multi-source research, retry, extra skill load, or subagent: reuse a fresh artifact if one exists. Same approach fails twice → stop and report. No tools needed → chat only. Prefer connector or API over clicking. Do not create bots or routines to save usage.

### Reply lesson (2026-09-18, VIR)
SendToAgent without `priority` failed, so 總指揮 never received the VIR reply and started Story itself. Always include priority true and the TC id, verdict, levels, absolute paths, Self-VERIFY.

### Ticket log

| TC | Status | Notes |
|----|--------|-------|
| TC-20260909-06 | CANCEL/HOLD | Pine-filter TGB/ANET/SLS. Disk `run-20260909-1033`, **not final**. |
| TC-20260909-08 | Unauthorized auto-handoff | Drive BUY-10. Disk `run-20260909-1053`. Not a standing mandate. |
| TC-20260909-12 | AUTHORIZED | **SRRK BUY**. `run-20260909-1232`. Self-VERIFY PASS. Story chained as TC-13. |
| TC-20260918-12 | AUTHORIZED | **VIR BUY**. `run-20260918-1328`. Self-VERIFY PASS. Reply to 總指揮 failed (missing priority); 總指揮 started Story itself. |
| TC-20260918-18 | AUTHORIZED | **TH STALK** (Setup H, S/R Flip). `run-20260918-1455`. Self-VERIFY PASS. Priority reply succeeded. |
| TC-20260925-06 | AUTHORIZED, Setup done | **MRVI WATCH**. `run-20260925-1552`. Self-VERIFY PASS_WITH_NOTES. HANDOFF sent to 投資敘事分析師 (priority). Story report written; Story said it passed Fusion. |

### Authorized plan details (from CSV, not invented)

**SRRK** last bar 2026-09-08, BUY. Setup B Pullback Support. Entry `$55.88–$56.15`. Stop `$53.77` PB_STRUCT. Target `$61.76` RR 2.56x. Priority 90. Paths under `run-20260909-1232`.

**VIR** BUY. Entry `$10.39–$10.53`. Stop `$10.12` (TZ). Target `$11.94` RR 4.35x. `run-20260918-1328`.

**TH** STALK. Entry `$20.27–$20.67`. Stop `$19.96` (SR_FLIP). Target `$23.83` (atr) RR 6.58x. `run-20260918-1455`.

**MRVI** last bar 2026-09-24, WATCH (scanner also WATCH). No Trade_Entry CSV (plan not published). Close `$7.65`. Priority 65, Stage2 Strict 0, so not BUY. Last Tight Zone 2026-09-15 (7 bars, fails Freshness) and 17 days (over 10-day cap), so not STALK. Upgrade trigger: pullback `$7.24–$7.30` without a close below `$7.04`. Conditional stop `$6.83` PB_STRUCT. Target `$8.98` Resistance, RR 3.57x at `$7.30`. Earnings CLEAR, 2026-11-05. Regime 9/24 quoted only: Bear/Avoid, stance UNCERTAIN, exposure 0% (`/workspace/market-awareness/2026-09-24/regime-daily-2026-09-24.md`). Files: `MRVI_Setup_TC-20260925-06.md`, `HANDOFF_MRVI.md`, `ANALYSIS_SUMMARY.md`, `SELF_VERIFY.md`, `result.json` in `run-20260925-1552`. Story: `/workspace/story-search/output/run-20260925-mrvi/STORY_REPORT_MRVI.md` (thesis: earnings inflection real but revenue guide not raised; August rally was sympathy and faded; WATCH stands).

### Teammate contract
- 總指揮 (`7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`): only an explicit TC starts Setup. Reply priority true when the TC finishes, including NO TRADE / AVOID / data gate.
- US Swing Scanner (`293d30a5-d04e-4443-89d9-f313f9ca873e`): upstream CSVs. Scanner stop = Potential Setups.
- 港股 Swing Setup (`28b5646e-bfc2-440b-8a63-b68440a1de4b`): HK only.
- 投資敘事分析師: HANDOFF consumer. Cannot upgrade technical VERDICT. On TC-20260925-06 this bot was told to hand HANDOFF directly (normally 總指揮 routes).
- Fusion Formatter: after Story. TC-20260925-06 Fusion stops at report MD + infographic prompt MD (no image).
- Work Verifier (`037de516-dbc1-4565-a127-5dbb0f691729`): second pass. Writes `/workspace/work-verifier/output/`. This bot does not write that folder.

### User-facing prefs (shared; not this bot's deliverable)
HK/finance briefs prefer infographics (baoyu-infographic, sketchnote, visual-director, Kami).

---

## Live snapshot

- **Idle.** No in-flight TC. Last authorized Setup = TC-20260925-06 MRVI **WATCH**, handed to Story on 2026-09-25. Story later reported the report path and that Fusion was handed the same TC. This bot's job on that ticket is done.
- **Do not start Setup** on a new scanner run without a new TC naming ticker + CSV path.
- **Known output folders:** `run-20260909-1033` (cancelled), `run-20260909-1053` (unauthorized), `run-20260909-1232` (SRRK), `run-20260918-1328` (VIR), `run-20260918-1455` (TH), `run-20260925-1552` (MRVI).
- **No routines. No MCP secrets. No open widget. No credentials requested.**
- **Pending confirms:** none.
- **Open todos:** none in progress. Prior ticket todos completed or cancelled.
- **Coverage:** profile.json, settings.json, memory/profile.md (4 facts), memory/USAGE_GATE.md, prior 2026-09-14 snapshot, and ticket history through 2026-09-25 MRVI plus the Story FYI. No dated memory/log files. Conversation transcript is not copied here. No secrets to redact.
- **Coverage gaps:** `update_state` memory writes are unreliable (snapshot cut short); durable facts live in `profile.md` and this file. Work Verifier outcomes for VIR/TH/MRVI are not stored in this bot's memory.

---

## Secrets placeholders

No secrets held. Template if a later restore must record one:

- `[REDACTED:CURSOR_API_KEY]`
- `[REDACTED:broker-token]`
- `[REDACTED:google-drive]`
