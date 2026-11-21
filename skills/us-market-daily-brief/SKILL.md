---
name: US Market Daily Brief
description: >-
  Use this when Justin wants the US daily market-focus brief (美股市場每日簡報) from
  US-ETF CSV + tvscreener AV script (Justin paste overrides), X Monitor AH seed,
  cash Focus, 盤後業績, section contracts/evidence/verdict — Traditional Chinese;
  prefer tables and bullets over wall-of-text.
---
# US Market Daily Brief

Produce **美股市場每日簡報** for an experienced trader. Entire user-facing report in **繁體中文**. Analysis Steps 1–5 are **silent** (no screening tables, no self-check dump). Start output at `## 美股市場每日簡報`.

**Upgrade lock (2026-10-31):** Keep all prior locked inputs and section order (Parts 1–6 + 盤後業績). Add section **contracts**, **failure ladders**, **evidence ledger**, **headline 觸發→傳導→為何＋falsifier**, **mega-cap sweep**, **breadth 10-session path**, **投資機會 verdict**, **明日價位**, **6–8k character** length, and **table／bullet layout** (Justin 2026-10-31). Do **not** remake old Finals when skills change.

## Presentation (locked 2026-10-31 — Justin)

**Prefer Markdown tables and short bullets** to illustrate. Content must stay **rich and complete** (all contract fields) — do **not** thin the brief into slogans.

Hard rules:

1. **No wall-of-text.** Avoid multi-sentence paragraphs that pack tape + 震央 + breadth into one block. Split into: short lead (≤2 sentences) → **table** → **bullets**.
2. **Default shapes by section:**
   - Opening tape → index/VIX **table** + 1–2 震央 as **bullets** (觸發／傳導／為何／falsifier each on own line)
   - Part 1 themes → **table**（主題｜ETF｜1D｜1W｜YTD｜聯動｜代表股）+ optional 1-line 驅動 per theme
   - Part 2 Focus → per ticker: header line + **bullet facts** (not a prose essay); optional mini table for price/RV/mcap
   - Part 3 flows → **in/out tables**; RSP/SCHD/MEME as bullets
   - Part 4 policy → **bullets only** (3–6)
   - Part 5 structure → index/VIX table + breadth **path table** (≈10 sessions when available)
   - Part 6 港股 → **mapping table**（US 主題｜強弱｜港股留意）
   - 盤後業績 → **table**（ticker｜cash%｜AH%｜print vs est｜隔夜含義）
   - 投資機會／明日價位 → verdict line + **trigger table**
3. **Density without walls:** put numbers in cells; put mechanism in one tight bullet — never delete required fields to look “short.”
4. Still no Step 1–5 working screener dumps; user-facing tables are **curated** (themes, Focus, flows, breadth, AH, setups).

## Inputs (preserve — do not drop)

- `US-ETF_[DATE].csv` — pull latest from Google Drive folder `1k5dJy7ny5n-W_EV5Aglt0QeeXS_-5Ijn` when not attached; notify Justin／總指揮 if missing. Report **quoted X/N** when some Tier-1 names are unresolved — never silently shrink the universe. Tier-1 Cyclicals use **WELD** (not RSHO; locked 2026-10-31).
- **Abnormal volume (locked 2026-10-14 gates; source switched 2026-11-20):** **Primary** = [TV Abnormal Volume MCP](sand-workflow:tv-abnormal-volume-mcp) / [US Abnormal Volume](sand-workflow:us-abnormal-volume) via **`/workspace/scripts/tv_av_screener.py`** (tvscreener, not TradingView MCP) **before** analysis. Justin paste/CSV **overrides** if he supplies one. Do **not** run disabled Python OpenClaw scripts, do **not** call TradingView MCP for AV/mega, and do not browser-scrape TV when the script works. **Also run mega-cap sweep** (same script): mcap≥$50B, |Δ|≥3%, drop OTC — for same-industry clusters that may be epicenter even if RelVol≤2.
- VIX: user paste **or** [FRED VIX Term Structure](sand-workflow:fred-vix-term-structure) / [Breadth Daily Report](sand-workflow:breadth-daily-report) / TradingView `CBOE:VIX`
- **Market Master** sheet `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` tabs 美股市寬／美股行業／ETF 輪動 — breadth/industry/rotation when needed.
- **X Monitor (AH seed, locked 2026-10-22):** Prefer same-session / evening X Monitor soft Final (or weekday softshort) for **盤後／after-hours large-cap earnings** names and first-pass reaction notes. Treat as a **seed list** — still verify prints vs est and AH % with IR／wires／Tavily; do **not** invent from tweets alone. If X Monitor missing, still run AH search (below).

If the AV script fails after US close and Justin did not paste, **STOP** and notify 總指揮. Do not retry via TradingView MCP. Empty UP with non-empty DOWN (or vice versa) can be valid — continue. If only ETF is missing, say which and still deliver what is verifiable. **No** `[待補充]` / `[工具搜尋結果]` placeholders.

## Section contracts (before gathering)

Each section is either **complete** or **explicitly omitted** under `### 資料缺口` — **never half-fill**. Required fields:

| Section | Required fields |
|---|---|
| Opening tape | VIX prev→today (pts + %), SPX/NDX or Comp/QQQ/Dow/IWM closes + %, 1–2 震央 with trigger |
| ① 市場大主題 | Theme name, representative ETF 1D/1W/YTD when available, 2–3 reps (price, %, RV when AV), 聯動 強｜中｜弱 — only themes that actually moved |
| ② 三大焦點股 | Price, %, RV, catalyst 1+source, catalyst 2+source, **傳導機制** one line, 板塊對照, 可行動洞察 |
| ③ 板塊輪動 | Sector/ETF, 1D/1W/YTD, 2–3 drivers — only |move| material or 5d trend reverse |
| ④ 政策／Trump | Named event, affected themes, verifiable figure — omit if no named event |
| ⑤ 市場結構 | Index closes, VIX, **breadth with ≥10-session path** (not single print), RSP/SPY etc. when material |
| ⑥ 港股影響 | US strong/weak → HK theme map; label 情緒傳導／留意 — never invent HK same-day causation |
| 盤後業績 | Ticker, EPS/rev vs est, AH level/%, source — no AH source → say so; never invent AH volume |
| 投資機會 | First line **有／冇** verdict; ≤3 trigger rows with price levels; then 唔好做 |
| 明日價位 | 2–3 if-then: trigger → meaning → action |

One missing required field → omit that section + list under 資料缺口. Never pad with 「據悉」「市場預期」.

## Failure ladders

| Datum | Primary | Fallback | All fail |
|---|---|---|---|
| Index closes | TradingView / tape | Second wire (AP/Yahoo/Reuters) | Omit that line; rest of brief continues |
| VIX | `CBOE:VIX` OHLCV / FRED | CBOE site / breadth report | Omit VIX |
| AV screener | tvscreener script, OpenClaw gates | Justin paste | **STOP + notify 總指揮** — never invent movers; no MCP fallback |
| Mega-cap sweep | tvscreener script mcap≥50B \|Δ\|≥3% | Wire tape scan | Omit cluster note |
| Breadth path | Market Master 美股市寬 | Stockbee/breadth skills | Omit multi-day path; single-day OK if sourced |
| AH prints | Justin paste (authoritative) → IR/wires | X Monitor seed + verify | Omit name or whole AH block with explicit line |

Distinguish **data broken** (OMIT/STOP) from **market quiet** (still write; say quiet).

## Evidence ledger

- Internally: every figure tagged `[source, session-date]` before Final. One-decimal figures (close, %, VIX, turnover) need **two independent sources** when available.
- A source that still shows the **prior** session is **not** today’s source.
- User-facing: keep **one-line** `來源：…` (no footnote dump). Figures that fail ledger check are **deleted**, never softened.
- Quiet internal checks that pass may stay in `_draft_notes.md` only.

## Pipeline (complete each; mark ✅ internally)

1. [US ETF Theme Scan](sand-workflow:us-etf-theme-scan) — Tier 1 39 always; Tier 2 confirm; Tier 3 on trigger; report X/N quoted
2. [US Abnormal Volume](sand-workflow:us-abnormal-volume) — tvscreener AV seeds + **mega-cap sweep** + ETF linkage
3. [US Focus Catalyst](sand-workflow:us-focus-catalyst) — 3 **cash** Focus + live web search (epicenter boost; ≥2 sourced facts + 傳導機制 each). Cash Focus stays AV-ranked; do **not** force Mag7／named AH reporters into Part 2 solely because they reported after the close.
4. Trump / **major policy** search — **include Part 4 when material**; omit only if nothing material
5. [US Rotation Structure](sand-workflow:us-rotation-structure) — flows 1D+1W+YTD, RSP/SPY, SCHD/IWM, MEME, tape+VIX, **breadth 10-session path**
6. 港股影響 — **default include** US→HK theme map; omit only if Part 1 has no usable theme signal
7. **盤後業績** — **default include** after Part 6 (Justin 2026-10-22)
8. **投資機會** + **明日價位** — after 盤後業績 (or after Part 6 if AH omitted)

## Header

Prefer:
`**YYYY年M月D日（星期X，反映[session date]收市） | 香港時間翌日早上7:00**`

Session date = US cash close date. Short form `**[DATE] 收市 | 香港時間翌日早上7:00**` is OK.

## Opening (before Part 1)

**Layout:** ≤2-sentence lead (定調 only) → **tape table** (VIX path + SPX/Dow/Comp or NDX/QQQ/IWM closes + %) → **1–2 震央 as bullets** (not embedded in the lead). Prefer mega-cap **same-industry cluster** or AV epicenter as 震央 — do not open with only “themes were mixed.”

Each 震央 bullet block uses **four lines**:
1. **觸發** — named event (filing / policy / earnings / deal / upgrade|downgrade)
2. **傳導機制** — why that event reprices peers
3. **為何係板塊／為何咁大** — proving number (RV, ETF move, cluster count, mcap wipe)
4. **Falsifier** — what price/level tomorrow would prove this wrong

**Never infer cause from price.** Verify trigger via search/IR first. If unverified → `原因未核實`.

If material AH large-cap earnings exist, one short forward pointer to `### 盤後業績`.

## Part 4 — Trump / major policy (material gate; **not limited to tariffs**)

**Do NOT omit** when any of these hold for the session:

- Same-day **tariff effective** / **retaliation**, or other trade measures
- Major White House / UN / campaign **policy statements** with market read-through (energy export bans or ban *intent*, Iran/geo economic isolation, Fed/Treasury-linked remarks, AI regulation or naming mandates, security/base deals, pharma/pricing, immigration/labor that moves keepers)
- Named executive action tied to day’s sectors

Still omit pure noise. Prefer 3–6 **bullets**: what was said → which US themes. No named event → OMIT Part 4 (contract).

## Part 6 — 港股影響（US→HK theme map; Justin 2026-09-23）

**Default: include** as a **mapping table** (US 主題｜今日強弱｜港股主題／代表股留意) + one-line 情緒傳導 disclaimer.

1. Recap which US sectors/themes were strong and weak (from Part 1).
2. For each, name **HK-relevant themes / representative tickers or sub-sectors to watch** next session.
3. Label **主題對照／留意清單** — not verified same-day HK price causation.
4. Omit **only** if Part 1 has no usable theme signal.

## 盤後業績 — after-hours large-cap earnings (locked 2026-10-22)

**Why:** Mag7／mega-cap／key semi-equipment prints **after cash close** drive **tonight’s** futures／NQ／sector beta.

**Default: include** `### 盤後業績` after Part 6 as a **table** (+ short 隔夜含義 bullets).

### Who to cover

1. **Justin-named** tickers — always cover if he named them.
2. Else seed from **X Monitor** same-session／evening soft.
3. Else search Mag7, mega-cap, material semi-equipment／AI-hardware with session-date AH earnings.

Prefer large caps for overnight tape. Skip micros unless Justin asked.

### What each name needs (table columns)

- Ticker｜Cash close ±%｜AH % / level｜Print vs est｜隔夜含義｜來源
- Omit AH volume when not uniformly reported — say so once; do not invent

Label **盤後／after-hours（非現金 AV）**.

### Omit only when

No material large-cap／key-sector AH **and** Justin named none — then one line: `盤後：無重大大型股業績`.

### Do not

- Replace cash Part 2 Focus with AH names solely because they reported AH
- Skip because keepers “weren’t in AV”
- Mix cash RelVol／epicenter claims into AH without labeling

## 投資機會（after 盤後業績）

First line must be a **verdict**: `有` or `冇`（今日冇可執行 setup）.

Then a **table**（路徑｜觸發｜價位｜動作）≤3 rows — never a vague 觀察名單 essay.

- If **冇**: still give 2–3 objective trigger paths in the table.
- If **有**: ≤3 setups with entry/invalidation grounded in today’s tape.
- Then short **唔好做** bullets.
- Two-sided structures: name which side is the variable — do not average them away.

## 明日價位

**Table** 2–3 rows: **觸發價／事件｜意義｜動作**. Prefer levels that falsify today’s 震央 or mark first re-rate after a flush (RV fading + reclaim 5-day). Do not invent levels without a tape/structure basis.

## Length discipline

Target **6,000–8,000 Chinese characters** for the user-facing Final (programmatic `len` before deliver). Cap is not a goal to pad to 14–18k.

If short (<~5.5k): add **領導層行業組成** and **multi-session breadth sequence** (as tables) — **not** more prose headlines.
If long: cut redundant prose first; keep curated tables that carry argument.

## Report skeleton

```markdown
## 美股市場每日簡報
**[header]**

[≤2 句定調]

| 標的 | 收市 | 日變 |
| ... tape / VIX table ... |

**震央**
- **TICKER ±%：** 觸發：…／傳導：…／為何：…／Falsifier：…

### 第一部分：市場大主題
| 主題 | ETF | 1D | 1W | YTD | 聯動 | 代表股 |
| ... |
- 驅動（每主題一行，可選）

### 第二部分：三大焦點股
#### 1. TICKER 名 ±%（個股｜聯動）
| 價 | % | RelVol | 市值 |
- 催化劑1（來源）
- 催化劑2（來源）
- 傳導機制：…
- 板塊對照／可行動洞察：…

### 第三部分：板塊輪動
| ETF | 1D | 1W | YTD | 流入/出 |
- RSP/SPY｜SCHD/IWM｜MEME｜整體判斷（短 bullet）

### 第四部分：Trump／重大政策   ← material only（bullets）
### 第五部分：市場結構
| 指數/VIX | … |
| 日期 | UP4/DN4 | %>50D | 動力股% | … |  ← breadth path

### 第六部分：港股影響
| US 主題 | 強弱 | 港股留意 |

### 盤後業績
| Ticker | Cash% | AH% | vs est | 隔夜 |

### 投資機會
**Verdict：有／冇**
| 路徑 | 觸發 | 價位 | 動作 |
- 唔好做：…

### 明日價位
| 觸發 | 意義 | 動作 |

### 資料缺口   ← only if needed

**數據來源**：…
```

## Boundary vs Market Awareness Orchestrator

- YOU = themes, movers, catalysts, rotation narrative for the cash session **plus** AH large-cap earnings, opportunity verdict, and next-day levels.
- Orchestrator = regime TOTAL / pillars / stance. Do **not** emit TOTAL/21.5.

## Commodity / futures tape (locked 2026-10-02)

1. Name the contract month when continuous ticker rolled.
2. % change must be **same-contract** settle-to-settle (or label snapshot).
3. Never mix continuous after a roll against a prior-month settle without 更正註記.

## Traps (correctness)

- Indices can diverge (NDX vs press tape) — print both with sources; never silently pick one.
- Point change from **stored prior close**, never a rounded headline.
- Low RV ≠ harmless: −5% on RV 1.1 vs RV 6.5 are different findings.
- Do not buy “it fell a lot” — sector flush needs first re-rate (RV fading + reclaim 5-day) before bottom signal; else say none.
- Price against flow/rating = first-class **背離**.
- Official name from data-source description — never infer from a peer.
- Suspended/stale prints: exclude and state count.
- Quantify weight concentration in points when one name drives the index.
- Closing auction: huge volume + flat close = auction story, not a breakout.

## Self-VERIFY checklist (write into `_draft_notes.md`)

- [ ] Each section complete or OMIT + 資料缺口
- [ ] Evidence ledger passed (1-decimal dual-source when available)
- [ ] Headlines have 觸發→傳導→為何 + falsifier; no price-inferred causes
- [ ] Character count 6–8k (programmatic)
- [ ] 投資機會 first line is 有／冇
- [ ] Breadth has multi-session path when Market Master available
- [ ] Mega-cap sweep ran; same-industry cluster in 震央 if present
- [ ] Screener dropped OTC; mcap gates consistent; ETF X/N quoted noted
- [ ] 盤後 only with sources; Justin-named AH covered
- [ ] X Monitor used as seed only (verified)
- [ ] No regime TOTAL; no invented numbers; Part 6 present when themes exist
- [ ] **Layout:** tape/themes/flows/breadth/AH/setups use tables or bullets — no wall-of-text opening or Part 2 essays

## Anti-jobs

Do not print Step 1–5 working tables. Do not invent prices, RelVol, mcap, VIX, or catalysts. Do not dump full search transcripts or footnote lists. Do not invent HK same-day prices or fake causal spillover. Do not omit Part 6 when Part 1 has clear themes. Do not omit `### 盤後業績` on material AH nights (or when Justin named AH tickers). Do not treat “optional cash Focus” as skip-AH. Do not limit Part 4 to tariffs only. Do not use fuzzy index ranges when one verified close exists. English is not the main report. Do not replace Orchestrator’s regime daily. Do not run disabled Python OpenClaw AV scripts. Do not report commodity % across contract months unlabeled. Do not drop X Monitor / Drive ETF / Justin paste / Market Master inputs. Do not replace the locked Part 1–6 order with a different skeleton — only **append** 投資機會／明日價位／資料缺口. Do not pack the whole tape into one dense paragraph when a table + bullets can carry the same facts. Do not thin required contract fields just to look short.
