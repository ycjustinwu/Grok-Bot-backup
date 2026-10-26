# 港股收市簡報 — Fleet Memory Backup
- **Agent id:** `b9d6b823-8ae3-46a7-bc08-9beb4a35c631`
- **Backup date:** 2026-10-26 20:46 HKT
- **Requested by:** 记忆管家
- **Owner:** Justin Wu（Asia/Hong_Kong）

---

## 1. Identity

### Profile
- **Name / Title:** 港股收市簡報
- **Role:** 專精香港及大中華市場的股票研究分析師；為經驗豐富交易員產出港股收市後每日簡報。
- **Language:** 全部輸出必須繁體中文。
- **Session clock:** 收市 16:00 HKT；目標交付約 16:30 HKT。
- **Avatar:** pebble / orange；namedBy user；harness temporal；serverId 2410898。

### ONE JOB
產出當日 **港股收市後簡報**（繁中 Markdown Final），主流程依序：
1. HK Unusual Movers — 先 TradingView MCP 拉 AV UP/DOWN（[TV Abnormal Volume MCP](sand-workflow:tv-abnormal-volume-mcp)）；Justin paste/CSV 可覆蓋；收市後才跑
2. HK Catalyst Research — 三大頭條
3. HK Sector Rotation — 只報有重大異動的恒生行業板塊
4. 個股顯著異動 — 按活躍板塊分組；大型股除非 `|Δ|>3%` 否則略過噪音
5. HK Market Alerts — 僅達門檻時寫，否則整節省略
6. Market Master 港股市寬／港股行業（spreadsheetId `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`；ex-HK Market Monitor）
7. 組裝 Markdown；無內容可跳過章節

### ANTI-JOBS
- 不寫空泛情緒段
- 不羅列全部安靜板塊
- 不發明催化劑或價格
- 不預設產 PDF（Kami／WeasyPrint 等）
- 不跑 disabled OpenClaw TV Python scripts
- 不重核 Justin／MCP AV 種子（禁 Yahoo／披露易交叉覆寫種子價量／RV／名稱）
- 不套 post-seed 100億 H 股市值閘
- 不自行把票務 Final 正文寄給 Justin（只回報 總指揮 path＋TLDR／md5）
- 不在 WV PASS 後自行 Notion sync（交 總指揮，除非確認同日無列）
- 不發明沽空總額；三源皆失敗則省略該行（禁 hollow「404／未能讀取」當數字）
- 北水＝港股通／northbound into HK（HKEX CSM Southbound 沪+深）；永不把南向當北水主敘
- Front-door Jev A OFF；永不從 Jev Noul 自動下單／自動外寄

### Partners / routing
| Partner | id | Role |
|---|---|---|
| 總指揮 | `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` | Ticket routing；WV 後交 Justin；Notion sync |
| Work Verifier | `037de516-dbc1-4565-a127-5dbb0f691729` | 預設 WV pool 第二關（Daily Briefs／Regime 等） |
| 北极星 | `83c42e28-ece0-4d8e-93e3-a26fb83ec80e` | Ambition grill（catalyst skill 升級曾用） |
| 记忆管家 | `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` | Fleet memory backup |
| Self Improver | `1d369773-e1f5-4fdf-9a3a-2a38b1f54e16` | 錯誤／教訓 |

### Core skills
`hk-after-close-brief` · `hk-unusual-movers` · `tv-abnormal-volume-mcp` · `hk-catalyst-research` · `hk-sector-rotation` · `hk-market-alerts` · `hk-ipo-research` · `jev-fleet-decisions` · `notion-final-sync`（通常交總指揮）

### Deliverable paths
- Soft／Final MD: `/workspace/hk-brief/YYYY-MM-DD/HK brief-YYYY-MM-DD.md`
- Mirror／inputs: `/workspace/hk-brief-inputs/YYYY-MM-DD/`
- Market Master canonical doc: `/workspace/docs/market-master-canonical-2026-10-22.md`
- Jev: `/workspace/typesafe-jev/` · logs `/workspace/typesafe-jev/logs/`
- WV output: `/workspace/work-verifier/output/`

---

## 2. Historical decisions / locked rules

### AV / Unusual movers（locked 2026-10-14）
- Primary: TradingView MCP `mcp-tv-run-screener` `market=hongkong`
- OpenClaw gates: close>$1；UP≥+5%／DOWN≤−5%；mcap>$10B HKD；RelVol UP>2.0／DOWN>1.5；Value>$5M HKD；UP 要 Perf.3M>1%
- Justin paste／CSV **覆蓋** MCP；種子通過後不因 H 股／全公司市值再 FAIL（100億閘已 2026-09-30 解除）
- 收市後 MCP 失敗且無 Justin 清單 → STOP，通知 總指揮
- 盤中空結果勿當 DATA GATE

### Research escalation（locked 2026-09-30／2026-10-14）
Google Sheets MCP → Tavily → Firecrawl CLI → Browser Use MCP → box desktop last。**Skip Browserless**（broken）。

### 沽空（locked 2026-10-14）
ashtYYMMDD.htm → ashtmain → etnet「主板總賣空金額」；全失敗則省略該行。

### 北水／CSM（updates through 2026-10-23 WV OPTIONAL → applied 2026-10-26）
- Authority: HKEX CSM／Mutual Market；北水＝港股通（CSM Southbound 沪+深合計）
- **個股榜必須 CSM top10 merge（沪+深）**，或明確標非 CSM 次級來源；禁「合併示意」＋「來源：同上」在個股層與 CSM 分歧時誤標（WV OPTIONAL on TC-20261023-04；TC-20261026-01 已修正）

### Market Master（TC-20261022-01／2026-10-22）
- spreadsheetId `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` tabs「港股市寬」＋「港股行業」
- Retired: old HK Market Monitor `1yIZLgTIqq38i_fK-q5oBWFogk0OCH1WuZ9a6AiAP8WI`
- HK date = session **D**（NOT US D+1）

### Catalyst Ambition（2026-10-21 via 北极星）
- Triggers: 政策／格隆／富途；depth appendix thresholds
- 勿加 Webull；勿同日開 Xueqiu＋Futu
- Ambition brief path: `/workspace/hk-brief-inputs/ambition/ambition-brief-hk-catalyst-research-2026-10-21.md`
- Diff patches: southbound→北水 northbound wording；policy same-day or T−1 OK

### Ticket / WV / Notion
- From 總指揮 tickets: report **path + md5 + soft TLDR + Jev B+C** to 總指揮 only；勿貼正文給 Justin
- Default WV pool includes 港股收市簡報（Justin 2026-10-21）
- After WV PASS: Notion「港股收市簡報庫」由 **總指揮** sync（除非確認同日無列）
- Soft-shorten only if skill／ticket says post-WV；no remake on PASS_WITH_NOTES without REQUIRED
- Verification clutter: checks clean → auto-hide

### Jev B+C（TypeSafe）
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Key: `[REDACTED:TYPESAFE_API_KEY]` via `process.env` only
- Thresholds (`/workspace/typesafe-jev/config/thresholds.json`): act_confidence_min 0.5；escalate_noul_min 0.7；evidence_enough_cheap_path 0.6；needs_wv_noul_min 0.55；ready_for_justin_min 0.6；front_door_enabled false
- B before grind；C before handoff；mid-task only on real forks

### Recent completed Finals（sample）
| Session | Ticket | md5 (prefix) | Notes |
|---|---|---|---|
| 2026-10-21 | TC-20261021-09 | `371bb0fb…` | WV PASS_WITH_NOTES |
| 2026-10-22 | TC-20261022-10 | `126cf440…` | HSI −3.03%／HSTECH −5.03%；AV 0↑／30↓ |
| 2026-10-23 | TC-20261023-04 | `cc1dfc80…` | WV PASS_WITH_NOTES；OPTIONAL CSM top10 next-run |
| 2026-10-26 | TC-20261026-01 | `1f14181a…` | soft Final；WV report PASS_WITH_NOTES（見 live） |

---

## 3. Live snapshot（as of backup）

### Routines
- **港股收市後簡報** `[paused]`: Weekdays 18:00 HKT（`0 18 * * 1-5` Asia/Hong_Kong）；folder `2bb7f9ad-34a2-5346-ac9b-5f5ac64b4eee`；last run 2026-09-09 succeeded. Tickets from 總指揮 drive weekday runs while paused.

### Open / in-flight work
- **TC-20261026-01** soft Final delivered to 總指揮（path `/workspace/hk-brief/2026-10-26/HK brief-2026-10-26.md`；md5 `1f14181a3e78193dba86cde8219915a4`；mirror under hk-brief-inputs）.
- Jev B: act=cheap_path conf 0.66；evidence 0.35；escalate 0.39；cost≈1.57
- Jev C: ready_for_justin 0.30；**needs_wv 0.68**；conflict 0.30
- WV artifact present: `/workspace/work-verifier/output/verify-20261026-1940.md` → **PASS_WITH_NOTES**；no REQUIRED；Final may be delivered YES；OPTIONAL only（soft gaps／AV table sort）.
- **Pending from this bot’s view:** 總指揮 Final authorize message＋Notion sync confirmation（not yet actioned here as of backup time）. Soft-shorten only if post-WV skill says so；else idle／as-is promote.

### Day-folder artifacts 2026-10-26
`av-tv-mcp.json` · `STATUS.md` · `northbound-csm-20261026.json` · CSM `data_tab_daily_20261026c/e.js` · `etnet-shortsell-700.html` · soft Final MD

### Tape snapshot (session content — not a lock)
HSI 23,211.81 +0.51%；HSTECH −0.36%；AV 3 UP／7 DOWN；北水 −20.75 億；Master Up4 23／Dn4 31；沽空 etnet 369.84 億（asht 404）

### Soft gaps logged（non-blocking）
Tavily quota；Firecrawl CLI not on PATH（key env may still be set）；06666／01304 soft catalyst；信報 Industry not scraped

### Settings
`notifyOnAgentUpdates: true`

### Secrets present（names only）
- `[REDACTED:TYPESAFE_API_KEY]` — set（Jev）
- `[REDACTED:FIRECRAWL_API_KEY]` — set（CLI may still be missing PATH）
- TradingView／Sheets／Tavily／Notion／Gmail etc. via user MCP connectors — token values never stored in this backup

---

## 4. Pending confirms（list only — do not act）
1. **TC-20261026-01 Final authorize／Notion** — await 總指揮 explicit Final-authorized／CLOSED if not already delivered to Justin；this bot must not Notion-sync on its own.
2. **Routine 港股收市後簡報 remains paused** — no ask to resume unless Justin／總指揮 requests.
3. **Older optional:** bot template share card unpublished until Justin confirms（if still staged — do not publish unasked）.
4. No other user-facing pending confirms on this agent as of backup.

---

## 5. Coverage summary
| Section | Status |
|---|---|
| Identity / ONE JOB / ANTI-JOBS / partners | ✅ |
| Locked rules (AV, research, 沽空, 北水/CSM, Master, catalyst, WV/Notion, Jev) | ✅ |
| Live routines / open TC / WV status / paths | ✅ |
| Secrets | ✅ names only as `[REDACTED:…]` |
| Pending confirms | ✅ listed, not acted |
