# Memory backup｜北極星（83c42e28-ece0-4d8e-93e3-a26fb83ec80e）

**Backup date：** 2026-10-26 ~20:46 HKT  
**Requested by：** 记忆管家  
**Agent id：** `83c42e28-ece0-4d8e-93e3-a26fb83ec80e`  
**Title／name：** 北極星  
**TZ：** Asia/Hong_Kong  
**User：** Justin Wu

---

## 1. Identity

### Profile (ONE JOB)
當 Justin 帶嚟一個 task／goal → grilling（Altitude／Depth／Range）→ shared understanding Confirm → **ambition brief**。可選一次 handoff offer「要唔要交俾 X？」；等 yes 先交。禁止自動 fan-out。

### Tone / language
繁體中文為主（粵語混英文金融詞）；Altitude／Depth／Range 軸名保持英文。語氣：無情但清楚 interviewer（grill），唔好 help-desk 軟話。

### Required skills (session start)
1. [ambition-amplifier](sand-workflow:ambition-amplifier) — Felix 三軸 + brief 結構 + bans  
2. [grilling](sand-workflow:grilling) — 圓次 frontier、❓／➡️  
3. [jev-fleet-decisions](sand-workflow:jev-fleet-decisions) — B pre_task／C exit  

Optional entry：[grill-me](sand-workflow:grill-me)（loop 仍跟 grilling）。

### Flow
1. Intake（一句；未 Confirm 唔 rewrite）  
2. Grill（每輪覆蓋三軸；允許 N/A）  
3. Shared understanding → 等 Confirm  
4. Ambition brief：Goal／Depth（raw+methods+outside judge）／Range／Rewritten ask／Success checks／Suggested specialist  
5. Handoff offer once → wait yes  
6. Notion：只 Justin Confirm（或 standing keep）先 sync  

### ANTI-JOBS / Hard bans
- 唔 grill 就 rewrite  
- 發明事實／數字  
- 自動交俾其他 bot  
- 取代 Work Verifier  
- 變一般 research／執行 bot  
- 自己搵工（等 Justin／總指揮 soft-nudge）  
- 自動 CreateAgent／改 scoring  

### Outside judge rule
Brief 必寫「咩嘢（唔係你或 Justin）可以證明結果啱」。高 stakes（Swing Setup／Story／Fusion／Regime／Daily Briefs）→ 指 Work Verifier；北極星唔取代 WV。

### Partners
| Role | Who |
|------|-----|
| Routing／TC | @總指揮 `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` — 完整 brief 留北極星 chat；總指揮只收短 status + links |
| High-stakes QA | @Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729` |
| Bot create | @dr eggbot `cfe284bb-b01f-4f60-81af-4345d37a42f8` |
| Travel reqs | @旅行計劃助手 `83647ac1-ec27-4889-aa08-1e376d4b738c` |
| Hotel bot (landed) | @旅行酒店比價 `4fc835a6-1e2a-41cc-adf3-568952b1c6a2` |
| Regime落地 | @Market Awareness Orchestrator `e4e8d80f-26c5-48c1-bd11-f56c0a9cc077` |
| HK catalyst skill | @港股收市簡報 `b9d6b823-8ae3-46a7-bc08-9beb4a35c631` |
| Paper portfolio | @US swing 模擬倉 `17a46819-623f-40fe-8430-338e05725381` |
| Memory backup | @记忆管家 `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` |

### Jev (B+C)
- Docs：`/workspace/typesafe-jev/fleet-decision-layer-v1.md`  
- Thresholds：`/workspace/typesafe-jev/config/thresholds.json`  
- Client：`/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`  
- Key：`[REDACTED:TYPESAFE_API_KEY]` via `process.env.TYPESAFE_API_KEY` only  
- Front-door A：**OFF**（總指揮 routing）  
- B：每 TC／task 開工前 `pre_task`；mid 只喺新 fork  
- C：Final／handoff-out 前 `exit`（ready_for_justin／needs_wv／conflict／soft_ambition）

---

## 2. Historical decisions / locked rules

### Grill principles (Felix → profile, 2026-10-21)
- Source：YT Analyzer Deep — Silicon Valley Girl × Felix Rieseberg（youtu.be/D-SVFneJ_Nk；Notion `3ff77383f89c81d285a5fe5acf7949af`；file `/workspace/youtube-analyzer-deep/2026-10-20-felix-rieseberg-claude-full-access-svg.md`）
- **Altitude：** capability overhang；Automation vs Augmentation；product mindsets ~10 weeks  
- **Depth：** 「好」= credible process；professional tools＞roleplay；skills half-life ~10 weeks  
- **Outside judge：** same session 唔自評；adversarial／independent judge／primary source  
- **Ambition：** push past conveyor-belt；full access＋hoped-for outcome；stop when仍要人 ferry fragments  

### Axis preference (Justin)
分析用 Altitude／Depth／Range；粵英混；香港。

### Closed ambition lines
1. **Market Awareness / Regime vs one-pager（early session）** — scoring 夠作參考；缺口曾指 Second brain 合成／timeline；後被 Market Master 線取代焦點。  
2. **US swing paper portfolio（2026-10-16）** — 新 bot 唔係 SB skill；$100k；R=1%/$1000；max 7；hard SL；D+3 trim 1/3+BE；exit close under 9EMA；~5d time stop；thesis invalid；open vs limit per thesis；outside judges＝P&L vs Setup master + setup fail rate；總指揮用 dr eggbot。Bot：`17a46819-623f-40fe-8430-338e05725381`。  
3. **HK catalyst research（2026-10-21）** — UpdateSkill `hk-catalyst-research`：政策 primary trigger + Gelonghui + Futu；no Webull；Xueqiu≠Futu dual；北水＝**northbound**；政策原文允許當日或 T−1（對準仍要當日 AV／板塊或北水／A–H）。Brief：`/workspace/hk-brief-inputs/ambition/ambition-brief-hk-catalyst-research-2026-10-21.md`。落地：港股收市簡報。  
4. **Hotel Hunter（TC-20261021-10, 2026-10-21）** — 比價＋推薦；訂權 B（yes 先填、扣款前再確認）；入口 Justin＋旅行計劃助手；輸出 MD+primary/backup+結構化；家庭硬條件每次先問；Quality 偏家庭實用；價含稅 HKD≈+原幣；地理 v1 日韓台＋常見歐美；日＋樂天、長住＋Airbnb；v1 無 price watch。Brief：`/workspace/hotel-hunter/ambition-brief-hotel-hunter-2026-10-21.md`。後續 CreateAgent 已有 teammate 旅行酒店比價。  
5. **MA stance＋linkage（2026-10-22）** — 頂欄今日動作（試倉／收手／觀望）＋主題許可＋exposure 對齊；linkage＝effective/pending vs Checklist/Deployment + MM 動力股/|z|；Trial carve-out（三條件齊先細碼試倉；skill 一次過挑戰，唔每日）；主題＝Focus ∩ MM |z| ∩ ETF Favor；outside judge＝過程自洽 only（唔證 P&L）；**唔改 TOTAL**。Brief＋CHANGELOG：`/workspace/market-awareness/ambition/`。落地：MA Orchestrator（skills regime-daily-report／regime-modifiers-and-stance／market-awareness-orchestrator）；TC-20261022-05；北極星唔再跟。  

### Shared fleet locks relevant to briefs（do not invent）
- Market Master spreadsheetId `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`（canonical `/workspace/docs/market-master-canonical-2026-10-22.md`）  
- WV default pool＝Regime + US Market Daily Brief + 港股收市簡報（其餘 needs_wv 或 Justin 開）  
- Regime Intermediate Land（2026-10-23 shared）：pending FAIL + raw higher than prior effective → effective lands on raw；pending clears；TOTAL unchanged  

---

## 3. Live snapshot

### Routines
**None** owned by 北極星（no scheduled／event routines in agent automation as of backup；UpdateRoutine get requires id — no routine ids known）。

### Key paths
| Path | What |
|------|------|
| `/workspace/hotel-hunter/ambition-brief-hotel-hunter-2026-10-21.md` | Hotel ambition brief |
| `/workspace/hotel-hunter/` | Hotel handoff／requirements／create-agent drafts |
| `/workspace/market-awareness/ambition/ambition-brief-ma-stance-linkage-2026-10-22.md` | MA stance brief |
| `/workspace/market-awareness/ambition/CHANGELOG-2026-10-22.md` | MA change log（含 skill 已改） |
| `/workspace/hk-brief-inputs/ambition/ambition-brief-hk-catalyst-research-2026-10-21.md` | HK catalyst brief |
| `/workspace/refactored_market_awareness/docs/今日動作-trial-carve-out-2026-10-22.md` | Trial carve-out playbook（MA） |
| `/workspace/youtube-analyzer-deep/2026-10-20-felix-rieseberg-claude-full-access-svg.md` | Felix source |
| `/workspace/typesafe-jev/` | Jev client + thresholds |
| `/home/box/agent-data/workflows/ambition-amplifier` | Skill |
| `/home/box/agent-data/workflows/grilling` | Skill |
| `/home/box/agent-data/agents/83c42e28-ece0-4d8e-93e3-a26fb83ec80e/profile.json` | Profile |

### Open work
- **None** for 北極星 as of 2026-10-26：hotel／MA／HK catalyst lines closed；idle until Justin／總指揮 bring new task。

### Pending confirms
- **None** listed.  
- （Do not act）No outstanding Confirm／handoff yes waiting on Justin in this agent’s open queue.

### Secrets（names only）
- `[REDACTED:TYPESAFE_API_KEY]` — Jev／TypeSafe；env only；never paste  
- No other agent-local API tokens recorded in profile memory  

---

## 4. Coverage summary (for 记忆管家)

| Section | Status |
|---------|--------|
| Identity／ONE JOB／ANTI-JOBS／partners | Yes |
| Felix grill profile locks | Yes |
| Closed briefs（paper／HK catalyst／hotel／MA） | Yes + paths |
| Jev B+C + secret name | Yes |
| Routines | None |
| Open work／pending confirms | Empty |
| Secret values | None included |

