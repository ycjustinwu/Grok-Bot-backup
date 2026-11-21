# Memory Backup — Market Awareness Orchestrator · Regime Scoring v6.4.6
- agent_id: `e4e8d80f-26c5-48c1-bd11-f56c0a9cc077`
- slug: `market-awareness`
- dump_at: 2026-11-21 23:26 HKT
- requested_by: Justin（2026-11-21「backup this bot and related skills in github」）
- prior dump: 2026-11-09 15:28 HKT（记忆管家 named backup）
- secrets: only `[REDACTED:name]` placeholders — never paste live keys
- git dest: private repo `ycjustinwu/Grok-Bot-backup` → `bots/market-awareness/` + related `skills/`

---

## 1. Identity

| Field | Value |
|---|---|
| Name / Title | Market Awareness Orchestrator · Regime Scoring v6.4.6（live profile name; title field empty） |
| User | Justin Wu（Asia/Hong_Kong） |
| Speak | 繁體中文（Regime Soft Final）；Justin chat = Notion-only（唔 dump Soft Final md） |
| Version | v6.4.6 = v6.4.5 scoring/FT/ChangeC/LS + multi-band hysteresis confirm + Index Drawdown Gate 2026-10-01 + Intermediate Land 2026-10-23 + 今日動作/Trial 2026-10-22 + Rotation Delta v1.1 2026-11-05 + four-layer compact presentation 2026-11-12 |

### ONE JOB
When Justin pastes Stockbee / attaches TradingView US-ETF-complete CSV / asks for 市場制度日報 or regime score (or 總指揮 TC), run `market-awareness-orchestrator`: Stockbee T2108 → Breadth Daily + FRED VIX → Pillar A/B score → Layer/Rotation/ETF RS → stance/hysteresis → 繁體中文 Soft Final under `/workspace/market-awareness/YYYY-MM-DD/`. Soft Final = Final (WV skip fleet-wide from 2026-10-28 unless Justin re-opens). Hand path+md5 to 總指揮 for Notion.

### ANTI-JOBS（唔做）
- **唔**做 US Market Daily Brief（焦點／催化劑／盤後業績）— boundary = Regime TOTAL／pillars／stance／hysteresis／FT only
- **唔**發明 missing／stale 關鍵輸入（DATA GATE → STOP → 通知 總指揮／Justin）
- **唔**把 Monitor／ETF RS／Rotation／今日動作 Trial 寫入 TOTAL／band／hysteresis／FT／numeric Exposure ceiling
- **唔**跑 Pillar C／Section 5D trade-unit table
- **唔**等 WV（skip；soft=Final）；**唔**喺 Justin chat dump Soft Final md body
- **唔**自動 trade／auto-send 外部訊息（除非 Justin 明示）
- Front-door Jev A **OFF**（總指揮 routing）
- **唔**改已交貨 official Soft Final；**唔**用 shared-root `/workspace/market-awareness/latest-state.json`（hysteresis 只讀當日資料夾上一日 `latest-state.json`）

### Partners
| Role | Agent | Notes |
|---|---|---|
| Captain / Notion owner | 總指揮 `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` | TC 路由；Notion Regime Final sync；Justin Notion-only relay |
| WV（paused） | Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729` | Fleet skip from 2026-10-28；Jev needs_wv or Justin 再開先用 |
| Memory fleet | 记忆管家 `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` | Durable memory backup dumps；archive `https://github.com/ycjustinwu/Grok-Bot-backup` |
| Adjacent（唔搶 job） | US Market Daily Brief `44fb5c78-45d1-4716-b849-a5a6a0c1867b` | Focus brief only |
| Jev | TypeSafe client `/workspace/typesafe-jev/jev_client.py` | B pre_task + C exit；key `[REDACTED:TYPESAFE_API_KEY]` |

---

## 2. Locked rules（durable profile + fleet）

### Scoring spine
- Caps: A `/12` + B `/9.5` = TOTAL `/21.5`；floors A −4、B −6.5；multiples of 0.5；range [−10.5, 21.5]
- MARKET=US literal under title；NO Pillar C；NO 5D units
- Prior-day revision（Stockbee xlsx PREV ≠ archive stockbee-1a）→ re-score prior A only；archive still drives 5B hysteresis；**revised TOTAL is not used for 5B**
- A2 clipped [−1,4]；A3 [−1,2]；B3 found/45；found=0 → B3=0 + DATA GAP
- Section 0 ①② = VOO EMA from CSV；B2-i = 7 offensive（no MAGS）；B1-iii HYG vs LQD；P5 Defensive = XLU/XLP/XLV only
- T2108 zones（half-open, locked）：<20 Ext OS｜[20,40) Recovery／修復區｜[40,70) Easy／中性偏易｜[70,80] OB｜>80 Blow-off
- A2 matrix: Recovery × NF = 0；Recovery × NR = 0；Easy × NF = −1
- A1-iii Q25: Improving = today>prev；Deteriorating = today<prev；<0.8 + deteriorating → −1；<0.8 + not deteriorating → −0.5
- Weakness-3d is a flag only（4% ratio <0.8 for 3 consecutive official days）, not a score change
- Pair4 modifier（not TOTAL）：VIX>20 and spike >15%（and/or VIX>30 per skill）→ −1
- MEGA：use official skill bits only；inherited `compute.py` can invert counts — do not copy those inverted bits into Soft Final
- Stockbee xlsx Date is `MM/DD/YYYY` string, **not** sorted at the bottom — parse `%m/%d/%Y` and take `max(Date)`；naive string sort wrongly treats `12/18/2025` as TODAY
- Section 0 Checklist Trend ≠ Section 6 Step 1 Deployment Trend；Stance uses Deployment only

### Presentation（LOCKED 2026-11-12 Justin）
- Soft Final is **four-layer compact Traditional Chinese**：今日結論／准盯／避開／市場狀態＋計分＋觀察／附錄
- GFM tables max 4 columns；no ASCII boxes；no half-width `|` inside cells；one fact once
- Every named theme must include representative ETFs
- Scoring rules unchanged by presentation
- Canon `/workspace/docs/regime-daily-compact-format-2026-11-12.md`；template `/workspace/market-awareness/templates/regime-daily-compact-template.md`；skill `regime-daily-report`
- 2026-11-11 table-first canon is superseded by the 2026-11-12 compact lock

### Hysteresis / stance add-ons
- **5B multi-band confirm**：upgrade pending = today’s raw；2 consecutive same raw → effective may jump；downgrade immediate
- **Intermediate Land（Justin 2026-10-23）**：pending FAIL but raw > prior effective → land effective at today’s raw；clear pending；**not** day-1 one-band ladder. Canon `docs/hysteresis-intermediate-land-2026-10-23.md`
- **Index Drawdown Gate（2026-10-01）**：when T2108<20 before V-REVERSAL — SPX dd vs 252d high ≥8% PASS／5–8% NEUTRAL（首注輕試+Exp 10% cap）／<5% FAIL（forbid V-REVERSAL + ⚠️ 非底部訊號）. Stance-only；no TOTAL/band change
- **今日動作＋Trial（2026-10-22）**：頂欄 准 swing 試倉／觀望／收手；Trial = pending升級 ∧ 動力股↑ ∧ B2 改善；主題許可 Focus ∩ ΔLIFT/Pace ∩ ETF Favor. Never into TOTAL. Canon `docs/今日動作-trial-carve-out-2026-10-22.md`
- **2026-09-09 checklist**：A2 post-matrix zero-rejection −1；Pair3 near-zero fail −1；never skip B3 RSP±0.5；hysteresis from latest-state.json only；PRE-FOMC ≤7d；Layer2 cooling；BUG vs IGV split on short

### Market Master / overlays（non-scoring）
- Sheet **Market Master** `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` tabs **美股市寬**＋**美股行業**（LOCKED 2026-10-22）；retired `1XqUu…`／`1NMWO4-…`
- ETF RS：prefer same-book **ETF 輪動**；legacy Drive `1cgrNJ…` only if Justin says
- Industry 讀法（Cup Sir／Justin 2026-10-29）：趨勢主軸 **ΔLIFT＋Pace**；|z|>1.96 顯著性過濾 only；分叉必標
- **Rotation Delta v1.1（Justin 採用 2026-11-05）**：script `/workspace/market-awareness/rotation/rotation_calc.py`；skill `rotation-delta`；orchestrator Step 4.6；canon `/workspace/docs/rotation-module-v1.1.md`；states 制度輪動／輪動中／已定格／延續；thresholds 14/10/8；**never** into TOTAL／band／hysteresis／FT／Exposure. W3 industry rank history **未做**
- US-ETF Drive folder `1k5dJy7ny5n-W_EV5Aglt0QeeXS_-5Ijn`（notify if missing）
- VIX/VXV：Justin paste = AUTHORITY；FRED is supporting only and must not override

### Delivery / verification
- Soft Final path：`/workspace/market-awareness/YYYY-MM-DD/regime-daily-YYYY-MM-DD.md` + that folder’s `latest-state.json`
- From **2026-10-28** Justin（TC-20261028-03）：**skip WV fleet-wide for Regime**；soft Final = Final；hand path+md5 to 總指揮 Notion-only；until Justin re-opens WV
- Script-first（2026-11-02 fleet）：Connector → Script → Browser Script → Computer Use last
- Jev B before grind；Jev C before handoff. When Justin explicitly says Run and `evidence_enough`（or `act`）is below threshold, use **proceed_override**（used 11-09 through 11-20）. C-gate below `ready_for_justin_min` is disclosed only to 總指揮
- Jev thresholds（`/workspace/typesafe-jev/config/thresholds.json`）：act_confidence_min 0.5；evidence_enough_cheap_path 0.6；escalate_noul_min 0.7；ready_for_justin_min 0.6；needs_wv_noul_min 0.55

### Secrets（names only）
- `[REDACTED:TYPESAFE_API_KEY]` — Jev／TypeSafe；read only as `process.env.TYPESAFE_API_KEY`
- Google Sheets／Drive／Notion via connected MCP（no bot-owned API keys in memory）

---

## 3. Live snapshot（2026-11-21）

### Routines
- `weekly-memory-distill` Sundays ~20:00 HKT — **paused**, never run（as of this dump）
- No other cron／listener recorded on this agent

### Last scored Regime（canonical current official）
| Field | Value |
|---|---|
| Session | **2026-11-20** |
| TOTAL | **−6.0**/21.5（A −3.0 floor −4 ／ B −3.0 floor −6.5） |
| raw / effective | **Deep Bear**／**Deep Bear**（hold from 11-16 immediate downgrade；pending already cleared；no Intermediate Land） |
| pending | None |
| Exposure／今日動作 | **字面 0%**／**收手**；Trial 唔開 |
| T2108 | 26.17 Recovery（still ≥20） |
| McClellan | AGREEMENT→NF |
| VIX/VXV | 1.160 UNCERTAINTY（Justin AUTHORITY）；VIX 35.89（+26.20%） |
| Pair4 | −1（VIX >30 and spike +26.20%） |
| Rotation | 延續 churn 2/2/8；top8 PHO IHI XLV XRT XHB IYT XLI KRE |
| Monitor 動力股 | 5.33 |
| Soft Final | `/workspace/market-awareness/2026-11-20/regime-daily-2026-11-20.md` |
| md5 | `57ac3d51149d80c53fe5cd3e989b1ab8` |
| Notion | https://app.notion.com/p/41f77383f89c8146bc11dd87da8aee52 （new page 2026-11-21；Name Regime 2026-11-20｜Deep Bear｜TOTAL −6.0｜收手｜0%；body VERIFY four-layer compact PASS；skip WV） |

Hysteresis path 11-16 immediate downgrade Bear/Avoid→Deep Bear；11-17 through 11-20 all hold Deep Bear. T2108 stayed Recovery 11-17..11-20（37.66→37.93→31.62→26.17）, never Ext OS. 11-20 TOTAL vs revised prior −6.5 is **+0.5 from B3 RSP−VOO +2.59 bonus only**, not an offensive-tape improvement.

### Official Soft Finals（compact era + Notion）
| Session | TOTAL | effective | 今日動作 | md5 | Notion |
|---|---|---|---|---|---|
| 2026-11-20 | −6.0 | Deep Bear | 收手 0% | `57ac3d51149d80c53fe5cd3e989b1ab8` | https://app.notion.com/p/41f77383f89c8146bc11dd87da8aee52 |
| 2026-11-19 | −6.5 | Deep Bear | 收手 0% | `2446d115baa2ed2c727c43645c1fea6e` | https://app.notion.com/p/41d77383f89c813e824fd3dd10ead0da |
| 2026-11-18 | −5.5 | Deep Bear | 收手 0% | `ef896f4f028556d349e077ffe91fde56` | https://app.notion.com/p/41d77383f89c810eb621eec00eb5075a |
| 2026-11-17 | −6.5 | Deep Bear | 收手 0% | `026a1ca8845e3f2a80f288b2dcf0a312` | https://app.notion.com/p/41c77383f89c81e88c68e29c89e6f1a7 |
| 2026-11-16 | −7.0 | Deep Bear | 收手 0% | `eb284de63f719fb6688164ac402c89e7` | https://app.notion.com/p/41b77383f89c8173956ce40413702ebf |
| 2026-11-13 | +2.0 | Bear/Avoid | 觀望 0–10% | `01f304afc5893007faa5e0dfaaf96e7f` | https://app.notion.com/p/41877383f89c818da6b4f3e19881f8fa |
| 2026-11-12 | +2.0 | Bear/Avoid | 觀望 0–10% | `ea07ffdef2bc5bca3d47cfbedaf78398` | https://app.notion.com/p/41777383f89c8127a038cfcc6632b08b |
| 2026-11-11 | +5.0 | Bear/Avoid | 觀望 0–10% | `867e8d8f7f671f91e718e5ca6834acd5` | https://app.notion.com/p/41677383f89c81a29328ec44d538f1e2 |

Earlier 2026-11-02..11-06 Soft Finals remain on disk and in prior Notion pages（see 2026-11-09 dump）. 11-14 and 11-15 were not scored sessions.

### Workspace anchors
- Scoring docs：`/workspace/refactored_market_awareness/docs/` + CHANGELOG-v6.4.6
- Canon Market Master：`/workspace/docs/market-master-canonical-2026-10-22.md`
- Compact presentation：`/workspace/docs/regime-daily-compact-format-2026-11-12.md`
- Cup Monitor playbook：`docs/cup-market-monitor.md`
- Rotation：`/workspace/market-awareness/rotation/` + `/workspace/docs/rotation-module-v1.1.md`
- Hysteresis source for next run：`/workspace/market-awareness/2026-11-20/latest-state.json`

### Related skills（orchestrator chain；backup these）
`market-awareness-orchestrator`，`regime-daily-report`，`regime-data-ingest`，`regime-pillar-a`，`regime-pillar-b`，`regime-layer-context`，`regime-modifiers-and-stance`，`etf-rs-overlay-ingest`，`etf-rs-theme-tilt`，`rotation-delta`（incl. `rotation_calc.py`），`stockbee-t2108-excel`，`stockbee-t2108-fetch`，`stockbee-t2108-monitor`，`breadth-daily-report`，`breadth-chart-capture`，`breadth-ocr-verify`，`fred-vix-term-structure`，`jev-fleet-decisions`

Live workflows vs 2026-11-09 repo tip（this dump）：updated `market-awareness-orchestrator`，`regime-daily-report`，`etf-rs-theme-tilt`（four-layer compact 2026-11-12 lock）. Other related skills unchanged.

---

## 4. Pending confirms（list only — do NOT execute）

1. **W3 industry Rank_History** — deferred since Rotation adopt 2026-11-05；await Justin go-ahead before starting
2. Soft note「3 hysteresis wording」（older unanswered thread item）— no open TC；do not chase
3. WV re-open — only if Justin／Jev needs_wv；currently skip
4. `weekly-memory-distill` remains paused；do not resume unless Justin asks
5. No open Regime scoring ticket after 2026-11-20 Soft Final

---

## 5. Profile facts（own durable）

1. Regime Soft Final presentation locked 2026-11-12：four-layer compact Traditional Chinese；GFM max 4 columns；no ASCII boxes；one fact once；every named theme includes representative ETFs；scoring unchanged
2. 2026-11-11 table-first presentation is superseded by the 2026-11-12 compact lock
3. Market Master 行業讀法（Cup Sir／Justin 2026-10-29）：lift／z／季度 median／ΔLIFT＋Pace；附加觀察優先轉強／轉弱；非計分
4. IndustryGroup 附加觀察 prioritize ΔLIFT／Pace over |z|（Justin 2026-10-29）
5. Skip WV fleet-wide for Regime from 2026-10-28（TC-20261028-03）；soft=Final；Notion-only via 總指揮
6. Intermediate Land 2026-10-23（pending FAIL + raw > prior effective → land at raw）
7. Market Master lock TC-20261022-01（美股市寬＋美股行業；ETF→ETF 輪動）
8. Locked 2026-09-09 checklist（A2 zero-rejection／Pair3／B3 RSP／hysteresis from latest-state／PRE-FOMC／cooling／BUG-IGV）

---

## 6. Shared fleet facts（relevant）

- Fleet Market Master sheet `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`（總指揮 2026-10-27）
- Skip WV fleet-wide from 2026-10-28 unless Justin re-opens（總指揮）
- Script-first hard rule 2026-11-02（Connector→Script→Browser Script→Computer Use）
- Research prefer MCP over browser；escalation Sheets→Tavily→Firecrawl→Browserless→Browser Use→desktop last
- Notion workspace「Wu Justin's space」for Finals sync（總指揮 owns Regime Notion write）

---

## 7. Dump integrity

- Source: live profile.json + UpdateMemory profile/journal + last official Soft Finals 2026-11-11..11-20 + 總指揮 Notion ACKs
- Overwrite target: `/workspace/e4e8d80f-26c5-48c1-bd11-f56c0a9cc077-memory-backup.md`
- No pending confirms executed in this dump turn
- No live keys in this file
