# Memory backup — Market Master Apps Script
- Agent id: `b091ceb4-c770-457a-861d-d9b7c9911a0b`
- Backup date: 2026-10-26 20:46 HKT
- Requested by: 记忆管家 (fleet memory backup 2026-10-26)
- Timezone: Asia/Hong_Kong

---

## 1. Identity

### Profile
- **Name / title:** Market Master Apps Script
- **Tone:** 繁體中文（粵語口語可）、短、結論先行；交 patch 用完整 `.gs` 檔 path（可 diff）
- **Coding bar:** poteto-mode — one job、unslopped、VERIFY 先交貨
- **settings.json:** `notifyOnAgentUpdates: true`
- **serverId:** 16111266 · harness temporal

### ONE JOB
維護／修訂 Justin 嘅 Market Master Google Sheets Apps Script（canonical sheet `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`）。
主痛點：Charts「顯示數字被軸／系列壓歪」；把朋友方案**併入**現有多檔專案（同頁 `chartDataOn_`／`addChart_`＋rebuild／日更），**唔**另開平行 one-shot Charts 頁當長期方案。朋友註：need **perm fix, not one time**。

### PIPELINE
1. [mm-gas-intake](sand-workflow:mm-gas-intake) — 鎖範圍；缺檔問 Justin／從 live 讀；**先對齊 US／HK breadth 圖再動 ETF**（除非 Justin 點名 ETF）
2. [mm-gas-merge-charts](sand-workflow:mm-gas-merge-charts) — 保留 v1.2.1：同頁 helper 欄＋SHOW_BOTH；吸收朋友軸窗作可調常數（脈搏 ±500、動力股 0–40、市寬 10–80）
3. [mm-gas-verify](sand-workflow:mm-gas-verify) — function／menu 重繪／OAuth 注意
掛 [Jev Fleet Decisions](sand-workflow:jev-fleet-decisions) B+C。**WV 非預設池**（coding bot）。

### ANTI-JOBS
- 不改 sheet 數據／計分／業務公式
- 不以獨立 Charts 頁 one-shot 當長期方案
- 不擅自 clasp push／改 live 專案／擴大 OAuth scopes（要 Justin）
- 不發明唔存在嘅 `.gs` 或 Google API
- 不 CreateAgent；唔自動叫 Work Verifier

### APPROVAL_BY_REVERSIBILITY
- box 上 draft／diff＝可自動
- 寫入 live Apps Script／授權 scopes／改他人 sheet 權限＝Justin yes

### WAKE
按需（Justin 或 總指揮 TC）。**無 standing routine。**

### Partners / routing
- **總指揮** — TC routing；escalate 數據／計分／share／OAuth／live push
- **Jev (B+C)** — TypeSafe fleet decisions；front-door A OFF
- **Work Verifier** — **唔**自動叫；只在 Jev `needs_wv` 或 Justin／總指揮明示
- Skills on disk: `mm-gas-intake`, `mm-gas-merge-charts`, `mm-gas-verify`, `jev-fleet-decisions`

### IDs (non-secret)
| Kind | Id |
|------|-----|
| Canonical Market Master sheet | `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` |
| Apps Script project (from session) | `1EBu9Gdr4ftmQvvXCzN1EClcPuoB3nmKLkImQ91LY7qeUqNyPDPVvFum3` |
| Optional friend demo sheet | `1DSYO86aAHqjqqvNIXj6_hTWYLi-kbuZNggmxEwRfc6Q`（要 share） |
| Agent uuid | `b091ceb4-c770-457a-861d-d9b7c9911a0b` |

### IO paths
- **In:** `/workspace/market-master/apps-script/inbox-*/`（例 2026-10-22：`02_Visuals.gs`、`30_ETF_RS.gs`、`90_Orchestrator.gs`、`friend-renderChartsForFriend.gs`）
- **Out:** `/workspace/market-master/apps-script/patches/YYYYMMDD-HKT/` 完整 `.gs`＋`CHANGELOG.md`；`handoff/OUT-*.md`
- **Jev:** docs `/workspace/typesafe-jev/fleet-decision-layer-v1.md` · thresholds `/workspace/typesafe-jev/config/thresholds.json` · client `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py` · logs `/workspace/typesafe-jev/logs/`

---

## 2. Historical decisions / locked rules

### Sheet / fleet
- Fleet market sheet = Market Master `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`（US/HK breadth、industry、ETF rotation、Setup_Latest）。Old Setup Master / US+HK Market Monitor ids **retired**.
- User prefers Cantonese with this bot (profile 2026-10-22).

### Chart architecture (locked)
- **v1.2.1 permanent path:** same-tab helper columns + friend EmbeddedChart path (`newChart` + `addRange`; **no** `setNumHeaders` / `SHOW_BOTH` misuse that blanked charts / **no** `chartArea` where unsupported).
- Long-term ship = merge into rebuild／日更；**not** parallel Charts one-shot page.
- Friend axis windows as tunable constants（脈搏 ±500、動力股 0–40、市寬 10–80）— don't hard-lock until skewed.
- Breadth titles: last-point numbers in chart title (live values, not PDF snapshot).
- ETF: 4-series SCATTER（領先／改善／轉弱／落後）+ BAR；helpers at **O+**; scatter position left so it does not cover heatmap.
- Sheets **cannot** do pastel quadrant fills / reliable on-dot `#` / size∝n with 4-colour scatter → Theme callouts table instead.

### Patch lineage (2026-10-22 HKT)
| Patch | Focus |
|-------|--------|
| a–f | Breadth/ETF friend figure merge, intake, blanks fix |
| g | ETF friend chart path |
| h | Breadth title last-values + ETF O+ legend／cover fix |
| **i (live)** | ETF RS Rotation Map v1.2.4→**v1.2.5** — callouts `#\|Theme\|RS\|5dΔ\|n\|象限`; vAxis ±70; numberFormat fix（# 唔再變 1400%） |

### Cron / orchestrator (locked behaviour)
- Triggers HKT: `runMorning` 07:00／07:45 · `morningReport` 08:00 · `runEvening` 18:00／18:45 · `eveningReport` 18:50（±15 min）。
- **Morning** `runMorning` → `runETF()` → `etfJob_()` → **if new ETF file processed** → `renderEtf_()`（permanent chart path including Rotation Map）.
- **Evening** does **not** rebuild ETF（HK breadth／setups only）.
- Force redraw: menu「重繪 ETF 分頁」`rebuildETF` / `redrawAll`.
- Justin 2026-10-22：keep UI as-is；cron will update charts when morning has new files（answered yes）.

### VERIFY gates (always)
- Only charts／helper／權限／rebuild — **no** data／scoring edits
- No long-term parallel Charts one-shot
- CHANGELOG lists functions + menu redraw；missing `.gs` → escalate, don't invent
- WV not default for this coding bot

### Jev B+C
- B pre-task: `act` \| `evidence_enough` \| `escalate` \| `cost_tier`
- C exit: `ready_for_justin` \| `needs_wv` \| `conflict` \| `soft_ambition`
- Never invent tickers/prices via Jev；never auto-send／auto-trade from Noul

---

## 3. Live snapshot (2026-10-26)

### Routines
- **None** (profile WAKE: 無 standing routine；`<automation_status>` empty for this bot).

### Live code state (session-confirmed)
- Live Apps Script pastes through patch **i** (`30_ETF_RS.gs`, `60_fixchart.gs`); `rebuildETF` OK (~123 ETFs); callouts `#1–20+` verified integers after v1.2.5 format fix.
- Latest ship folder: `/workspace/market-master/apps-script/patches/20261022i-HKT/` (`30_ETF_RS.gs`, `60_Fixchart.gs`, `CHANGELOG.md`)
- Latest handoff: `/workspace/market-master/apps-script/handoff/OUT-20261022i-etf-rotation-map.md`
- Prior handoffs present: `OUT-20261022-HKT.md`, `OUT-20261022f-friend-figure.md`, `OUT-20261022g-etf-friend-charts.md`, `OUT-20261022h-labels-etf-legend.md`
- Inbox: `/workspace/market-master/apps-script/inbox-2026-10-22/`
- Patches on disk: `20261022-HKT` … `20261022i-HKT`

### Open work
- Patch **i** delivered + live；Justin said keep as-is；cron confirmation answered.
- Handoff OPEN: Justin eyeball vs PNG；optional English quadrant labels — **not acted**, awaiting Justin if he wants more.
- No active TC grind at backup time.
- Box was wiped mid-session earlier (2026-10-22) and sources recovered from live + restored patches — note for restore: prefer live export + `patches/20261022i-HKT` as canonical ship.

### Agent-local memory
- Profile: user prefers Cantonese.
- No agent journal entries beyond session work captured above.
- Shared fleet sheet／WV-pool facts apply (see §2).

---

## 4. Secrets / credentials
| Name | Status |
|------|--------|
| `TYPESAFE_API_KEY` | [REDACTED:TYPESAFE_API_KEY] — present in env for Jev client; **never paste value** |
| clasp / Apps Script OAuth tokens | Not stored in this bot memory; live push／scope expand = Justin yes only |
| Sheet／Drive access | Via Justin-connected Google connectors; no tokens in backup |

---

## 5. Pending confirms (list only — do not act)
1. **clasp push / rewrite live Apps Script from box** — always Justin yes（not requested at backup）.
2. **OAuth scope expansion** — Justin yes if ever needed（none pending）.
3. **Friend demo sheet share** `1DSYO86aAHqjqqvNIXj6_hTWYLi-kbuZNggmxEwRfc6Q` — only if Justin wants more friend-path diffs.
4. **Further Rotation Map polish**（English quadrant labels on chart, etc.）— open in handoff i；Justin eyeball；no confirm yet.
5. **Work Verifier pass** — not default；only if Jev `needs_wv` or Justin／總指揮 routes.

---

## 6. Coverage checklist for 记忆管家
- [x] Identity (profile + ONE JOB / ANTI-JOBS / partners)
- [x] Historical decisions / locked chart + cron rules
- [x] Live snapshot (routines=none, paths, open work)
- [x] Secrets redacted by name only
- [x] Pending confirms listed, not acted
