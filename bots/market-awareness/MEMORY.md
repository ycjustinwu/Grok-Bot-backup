# Market Awareness Orchestrator — Fleet Memory Backup
- **Backup date:** 2026-10-26 (HKT)
- **Agent id:** `e4e8d80f-26c5-48c1-bd11-f56c0a9cc077`
- **ServerId:** `2410919`
- **Owner:** Justin Wu（via 總指揮 routing）

---

## 1. Identity

### Profile
| Field | Value |
|---|---|
| Name | Market Awareness Orchestrator |
| Title | Regime Scoring v6.4.6 |
| ONE JOB | Daily US Regime Scoring v6.4.6 end-to-end when Justin pastes Stockbee / attaches TradingView US-ETF-complete CSV / asks for 市場制度日報 or regime score — Stockbee T2108 → Breadth Daily + FRED VIX → score → 繁體中文 daily |
| Caps | Pillar A `/12` + Pillar B `/9.5` = **TOTAL `/21.5`** |
| Version | v6.4.6 = v6.4.3 scoring + v6.4.5 FT/ChangeC/LS + multi-band hysteresis confirm + Index Drawdown Gate (2026-10-01) + Intermediate Land (2026-10-23) + 今日動作/Trial (2026-10-22) |

### ANTI-JOBS（boundary）
- **NOT** US Market Daily Brief theme package / AV movers brief（→ US Market Daily Brief bot）
- **NO** Pillar C
- **NO** Section 5D trade-unit table
- Never invent tickers/prices via Jev; never auto-send / auto-trade from a Noul
- Never invent past DATA GATE failures — notify 總指揮
- Monitor / ETF RS overlay **never** into TOTAL / band / hysteresis / FT / numeric Exposure ceiling
- Notion sync owned by **總指揮** (not this bot)
- WV self-route forbidden — hand path/md5 to 總指揮（Regime ∈ default WV pool）

### Partners / routing
| Role | Agent | Notes |
|---|---|---|
| Captain / TC router | 總指揮 `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` | Layer A OFF; TCs, AUTHORIZE, WV route, Notion |
| Work Verifier | `037de516-dbc1-4565-a127-5dbb0f691729` | Default WV pool = Regime + US Market Daily Brief + 港股收市簡報 |
| Ambition grill | 北極星 `83c42e28-ece0-4d8e-93e3-a26fb83ec80e` | 今日動作 ambition handoff TC-20261022-05 |
| Memory steward | 记忆管家 `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` | This backup request |
| Adjacent（do not own） | US Market Daily Brief `44fb5c78-…` | Theme brief boundary |

### Jev (B+C) — TypeSafe
- Skill: `jev-fleet-decisions`
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md`
- Thresholds: `/workspace/typesafe-jev/config/thresholds.json`  
  `act_confidence_min=0.5` · `escalate_noul_min=0.7` · `evidence_enough_cheap_path=0.6` · `needs_wv_noul_min=0.55` · `ready_for_justin_min=0.6` · `front_door_enabled=false`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Secret: `[REDACTED:TYPESAFE_API_KEY]` via `process.env.TYPESAFE_API_KEY` only
- Branch sketch: `escalate≥0.7 OR act.conf<0.5 → ask 總指揮`; cheap_path = MCP/Sheets/xlsx only
- Standing: Regime default WV pool **overrides** low `needs_wv` Noul when TC says do not skip WV

---

## 2. Historical decisions / locked rules

### Scoring spine（do not “upgrade” math）
- Source: `/workspace/refactored_market_awareness/docs/v6.4.3/regime-scoring-v6.4.3.txt` + `CHANGELOG-v6.4.5.md` + `CHANGELOG-v6.4.6.md` + `regime-bands.md`
- Floors: A1 −2 · Pillar A −4 · B1 −2 · B2 −3 · B3 −1.5 · Pillar B −6.5
- Literal `MARKET=US` under title; TOTAL multiples of 0.5; range [−10.5, 21.5]
- A2 clip [−1,4]; A3 clip [−1,2]; B2-i = 7 offensive names（no MAGS）; B1-iii = HYG vs LQD; P5 Defensive = XLU/XLP/XLV only
- Prior-day Stockbee revision（2026-09-29）: re-score prior A on xlsx PREV ≠ archive; hysteresis still uses archived prior TOTAL
- End every daily: `不構成投資建議`

### Locked 2026-09-09 checklist（profile）
A2 post-matrix zero-rejection −1; Pair3 near-zero fail −1; never skip B3 RSP±0.5; hysteresis from latest-state.json; PRE-FOMC if ≤7d; Layer2 cooling list; BUG vs IGV split on short.

### US Market Monitor — Market Master（LOCKED 2026-10-22）
- SpreadsheetId: `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`
- Tabs every run: **`美股市寬`** + **`美股行業`**
- Retired primary: `1XqUuQ4Q0cj1BwORSLeUbRi6c1zjHMUt6cghy9N1BdYk`（and older `1NMWO4-…`）
- Docs: `/workspace/docs/market-master-canonical-2026-10-22.md` · `/workspace/refactored_market_awareness/docs/cup-market-monitor.md`
- Non-scoring 附加觀察: Up4/Down4, SMA20/50, MLI, **動力股佔比**, **SPY/QQQ ATR**, Sector/Industry tops, IndustryGroup |z|>1.96
- US date lock: for session D prefer History Date=D or D+1 stamp + disclose（Justin forever 2026-09-18; sheet→Market Master 2026-10-22）
- Drive unreachable → DATA GAP line under 重要旗號; do **not** fail whole Regime DATA GATE

### ETF RS Overlay
- Prefer Market Master tab **`ETF 輪動`**（same spreadsheetId）
- Legacy Drive `1cgrNJNg0hX7mQV9H-0gU6dcGQ5OCwVaU9aTkVrq2iLQ` **only if Justin says**
- Favor/Avoid + 2d∩5d 趨勢觀察; never into TOTAL/band/hysteresis/FT/Exposure
- Also feeds 主題許可／禁止（Focus ∩ MM |z| ∩ ETF Favor）

### Index Drawdown Gate（2026-10-01）
When T2108<20, before V-REVERSAL: SPX dd vs 252d high from Stockbee — PASS ≥8% / NEUTRAL 5–8%→首注輕試+Exp 10% cap / FAIL <5%→forbid V-REVERSAL + ⚠️ 非底部訊號. Stance-only.

### Hysteresis v6.4.6 + Intermediate Land（2026-10-23 Justin）
- Upgrade pending target = today’s **raw** band; 2 consecutive same raw → effective may jump multi-band; **no** day-1 one-band ladder
- Downgrade immediate
- **Intermediate Land:** pending FAIL + today’s raw **>** prior effective → land effective at raw today + clear pending（TOTAL unchanged）
- Canon: `/workspace/refactored_market_awareness/docs/hysteresis-intermediate-land-2026-10-23.md` + `regime-bands.md`
- Example applied 2026-10-22 amend: Deep Bear + pending Cautious FAIL + raw Bear/Avoid → effective Bear/Avoid

### 今日動作 + Trial carve-out（2026-10-22 Justin / 北極星）
- Top bar: **准 swing 試倉**／**觀望**／**收手**
- Trial 三條件齊才細碼試倉: pending升級中 ∧ 動力股↑ vs昨/P50 ∧ 風險胃納 B2↑/B2-i改善；缺一→觀望／收手
- Exposure 旁註 ∈ {字面 0%, 試倉例外開, 試倉例外唔開}
- Playbook: `/workspace/refactored_market_awareness/docs/今日動作-trial-carve-out-2026-10-22.md`
- WV feature: `regime-today-action`
- **Never** into TOTAL / hysteresis

### Delivery workflow
1. Jev B →（escalate gate may need AUTHORIZE PROCEED）→ grind cheap_path
2. Soft Final under `/workspace/market-awareness/YYYY-MM-DD/regime-daily-YYYY-MM-DD.md` + md5
3. Jev C → HANDOFF path/md5 to 總指揮 for WV（do not skip）
4. After WV PASS / PASS_WITH_NOTES → soft-shorten Final+TLDR in chat
5. Notion sync by 總指揮

### Soft-shorten / chat
繁體中文; TLDR then full Final body; Notion URL when 總指揮 DONE.

---

## 3. Live snapshot（as of backup）

### Status
- **Idle** — no open Regime TC
- Last closed ticket: **TC-20261024-03**（session 2026-10-23）

### Last scored session — 2026-10-23
| Field | Value |
|---|---|
| TOTAL | **−1.0 / 21.5**（A +1.0 / B −2.0）|
| raw / effective | Deep Bear / Deep Bear |
| Hysteresis | ⬇️ immediate downgrade from prior Bear/Avoid; pending **none**; Intermediate Land N/A |
| Exposure | 字面 0%／試倉例外唔開 |
| 今日動作 | **收手** |
| Trial | CLOSED（缺 pending 升級 + B2 惡化）|
| T2108 | 39.72 Recovery |
| McClellan | DIVERGENCE→PF（NAMO 穿零）|
| VIX/VXV | 0.9497 Justin same-session CALM AUTHORITY |
| 動力股佔比 | 15.1% |
| Final path | `/workspace/market-awareness/2026-10-23/regime-daily-2026-10-23.md` |
| md5 | `fe6a8d8f933ff4d498b51cdf01bad454` |
| Mirror | `/workspace/regime-output/2026-10-23/` |
| WV | PASS_WITH_NOTES · `/workspace/work-verifier/output/verify-20261024-0834.md` |
| Notion | https://app.notion.com/p/40377383f89c81f88192c6be0f49d903 （body_verified）|

### Prior session — 2026-10-22（amended Intermediate Land）
| Field | Value |
|---|---|
| TOTAL | +4.5 / 21.5（A +4.5 / B 0.0）|
| raw / effective | Bear/Avoid / **Bear/Avoid**（land）|
| md5 amended | `b945a2e58966506fbf15f4e3840ad4af`（supersedes WV-verified `488255e9…`）|
| Notion | https://app.notion.com/p/40277383f89c810191f0cd43ad486c19 |

### Key paths
```
/workspace/market-awareness/YYYY-MM-DD/     # session Finals + inputs
/workspace/market-awareness/inbox/          # inbound T2108 xlsx
/workspace/market-awareness/inputs/         # Justin breadth pastes
/workspace/regime-output/YYYY-MM-DD/        # mirrors + latest-state.json
/workspace/refactored_market_awareness/docs/
/workspace/typesafe-jev/
/workspace/work-verifier/output/
```

### Skills（orchestrator chain）
`market-awareness-orchestrator` → `regime-data-ingest` / `stockbee-t2108-*` / `breadth-daily-report` / `fred-vix-term-structure` → `regime-pillar-a` → `regime-pillar-b` → `regime-layer-context` → `regime-modifiers-and-stance` → `etf-rs-overlay-ingest` + `etf-rs-theme-tilt` → `regime-daily-report`

### Routines
- **None active** for this bot at backup time（no cron Regime auto-run; ticket-driven via 總指揮）

### Connectors commonly used（no secret values）
- Google Sheets MCP（Market Master）
- Google Drive MCP（US-ETF complete folder `1k5dJy7ny5n-W_EV5Aglt0QeeXS_-5Ijn`）
- TypeSafe Jev API via `[REDACTED:TYPESAFE_API_KEY]`

---

## 4. Secrets inventory（redacted）
| Name | Status | Usage |
|---|---|---|
| `TYPESAFE_API_KEY` | `[REDACTED:TYPESAFE_API_KEY]` · present in env at backup | `jev_client.py` pre_task / exit only |
| Sheet / Drive IDs | Public spreadsheet/folder ids above — not secrets | Market Master + ETF CSV ingest |

**Never paste token values into chat, Notion, or this backup.**

---

## 5. Pending confirms（list only — do not act）
1. **Soft note 3 — hysteresis wording for 總指揮**（older open item from pre-Intermediate-Land era）: clarify/confirm wording with 總指揮 if still wanted; superseded in part by Intermediate Land lock 2026-10-23 + WV soft note on 10/22 md5 drift — **still listed until Justin/總指揮 explicitly close**.
2. **No open AUTHORIZE / TC** at backup time.
3. **No pending Notion** — 2026-10-23 sync DONE.

---

## 6. Coverage checklist
- [x] Identity / ONE JOB / ANTI-JOBS / partners
- [x] Locked scoring + Monitor + ETF + DD Gate + Intermediate Land + 今日動作/Trial
- [x] Jev B/C thresholds + secret redaction
- [x] Live last Final pins + paths + WV/Notion
- [x] Routines（none）
- [x] Pending confirms listed without acting
- [x] Secrets as `[REDACTED:…]` only

