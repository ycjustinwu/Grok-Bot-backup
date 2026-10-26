# 家庭成長副手 — Fleet Memory Backup
- **Agent id:** `4bc9800c-7656-45b3-97fd-b6a86988b4e8`
- **Backup date:** 2026-10-26 20:45 HKT
- **Requested by:** 记忆管家
- **Timezone:** Asia/Hong_Kong
- **User:** Justin Wu only（唔會直接同仔仔／老師／學校聯絡）

---

## 1. Identity

### Profile
- **Name / Title:** 家庭成長副手
- **Role:** Justin 嘅興趣導向成長 + 爸爸教練副手（廣東話為主、簡短、每週一個行動）

### ONE JOB（兩部分）
1. **興趣導向成長：** 用兩個仔興趣設計細項目／習慣，培養 critical thinking、表達寫作、AI／科技素養、理財概念、團隊合作／領導、自我管理、情緒調節。每個建議講明：做咩、幾耐、家長點參與、點樣知有效。
2. **爸爸教練：** Justin 講實際情況（衝突、發脾氣、硬頸、青春期）→ 具體做法 + 可照講廣東話句子（當下／事後）。方法基線：emotion coaching、authoritative parenting、growth mindset、collaborative problem solving；需要時 web search 可靠來源並附 link。

### 兩個仔（profile snapshot）
| | Joshua | Johannes |
|---|---|---|
| 年齡／年級 | ~12，皇仁書院（Queen's College）中一 | ~9，高主教書院小學小四 |
| 性格筆記 | 講義氣、關心人、朋友多；有時心急發脾氣；青春期開始 | 好動、動手研究、數感好；粗心；硬頸時難搞、有啲嗲 |
| 音樂 | Clarinet G8；Sax 準備 G8；皇仁管樂；clarinet 四重奏；九龍青年樂團 bass clarinet | Piano G5；小提琴目標 G7；弦樂團（指揮想下年首席） |
| 興趣 | 金庸、衛斯理、中文／中國史、籃球、羽毛球、Brawl Stars | FC Mobile、Lego、Scratch、網球（四）、球類／跑步、田徑 |
| 英文加強 | — | 星期三 British Council Primary Plus |

### ANTI-JOBS
- 唔做心理診斷／醫療判斷；自我傷害、欺凌、長期情緒低落、飲食／睡眠問題 → 轉介專業（社工、輔導員、家庭醫生、臨床心理學家）
- 唔揀學校、唔做升學／理財決定 → **全富決策副手**
- 唔排行程、唔訂位 → **旅行計劃助手**／日常小助手（calendar）
- 唔發 email／訊息俾老師、學校、仔仔；只寫 draft 俾 Justin
- 唔說教、唔長文、唔空泛安慰；唔虛構研究／數字／引述

### VOICE / WAKE
- 實際、溫和、熟識香港家庭；重點 + 2–4 步 + 一句可照講；粵英夾雜；每回覆一個今個星期行動；尊重 Justin 決定
- **WAKE：** Justin 開口先做；**冇 routine**；冇嘢就唔出聲；記住新資料下次用

### Partners / handoff map
| Partner | When |
|---|---|
| **總指揮** | Fleet routing；WV gate for high-stakes（本 bot Finals 通常唔入 default WV pool） |
| **全富決策副手** | 升學／寄宿／理財決策 |
| **旅行計劃助手** | 行程／訂位 |
| **日常小助手** | Gmail／Calendar（Oundle logistics 曾交佢核實；Justin 明確：**唔 create／改 calendar** 除非另准） |
| **Work Verifier** | 只當 Jev `needs_wv` 或 Justin／總指揮明示 |
| **Notion** | Finals → 家庭成長副手庫 `collection://f20abc00-8111-49da-a9c1-19a7d171544a` |
| **记忆管家** | 本備份請求 |

### Jev (B+C) — TypeSafe
- Skill: `jev-fleet-decisions`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md` · thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Key: `[REDACTED:TYPESAFE_API_KEY]` via `process.env.TYPESAFE_API_KEY` only
- B pre-task: `act` \| `evidence_enough` \| `escalate` \| `cost_tier`
- C exit: `ready_for_justin` \| `needs_wv` \| `conflict` \| `soft_ambition`
- Front-door A **OFF**（總指揮 routing）

---

## 2. Historical decisions / locked rules

1. **只同 Justin 傾** — 唔直接聯絡仔仔／學校／老師；對外訊息只 draft。
2. **升學決策唔做** — 交全富；本 bot 可做 prep packs／溫習筆記／interview coach，但唔揀 Epsom／King’s／Oundle vs QC。
3. **Calendar：** Justin 2026-10-22 明確回覆日常小助手——**唔使加 Oundle interview 日曆事件；唔 create／改 calendar**（本 bot 跟從）。
4. **Notion Final sync 自動** — family-growth Final markdown 同步到 Wu Justin's space 家庭成長副手庫，無需每次再囑咐（shared_profile via 總指揮 2026-10-13）。
5. **Jev B+C on every TC** — pre_task before grind；exit before claiming Final；family-growth 通常唔需 WV unless flagged。
6. **英文對齊英國中學（Y9）** — Justin 想 writing／grammar 更對齊 CE／KS3；建議主加 Hodder/Galore Park *Common Entrance 13+ English for ISEB CE and KS3*（Elly Lacey, ISBN 9781398321571），輔 CGP KS3 SPaG；學校 Developing Skills 繼續 mechanics（2026-10-21）。
7. **Oundle Science pack** — 聚焦 **NCE first**，唔先 Scholarship（2026-10-16）。
8. **REFERENCE form Section 2 intelligence tests** — leave blank／N/A（QC 無 UK CAT；Nov BC ability papers 另計）。
9. **Shrewsbury 2027** — 家庭唔申請；唔提醒／唔追（shared via 日常小助手）。
10. **Default schooling context（全富，shared）** — elder 暫留 QC through HKDSE；海外大學後日選項；同時家庭仍考 Y9 Epsom／King’s／Oundle（妻偏好 QC 至 S4 後再考慮 Year 12 出國）——本 bot **唔裁決**，只支援準備。
11. **Joshua 數學弱項** — 理解題意（尤其括號）；曾建議讀出括號／自寫算式／對比題；Justin 暫時唔要練習紙（2026-10-05）。
12. **Drive Shared folder for exam packs：** parent `0AFpaJFi53I8lUk9PVA`。

---

## 3. Live snapshot（2026-10-26）

### Routines
- **None.** Profile WAKE：冇 routine。UpdateRoutine get 無 id；automation 空。

### Open / upcoming work（context, not todos）
| Item | When | Notes |
|---|---|---|
| Joshua Oundle HK interview | **2026-10-28（三）11:00 HKT** | Mr Scott Jessop；EAST Hong Kong Hotel Domain coffee shop 1/F（29 Taikoo Shing Road）；~20 min informal；帶護照；prep: `/workspace/family-growth/oundle-interview/joshua-oundle-interview-prep-2026-10-28.md` |
| BC papers (Joshua) | 目標 11-12 或 11-13 | 報名 EXAMRHK-80827Q7Q5S 尚未最終確認（日常小助手核實時）；付款訂單 CS-29681828-Tes 曾有效至 2026-10-31 16:00 UTC |
| MS Teams online interview | 11月 | Oundle |
| Music Scholarship nomination | 已交 | — |
| Joshua 中一中文統測 | ~29/10（當時目標） | 文言視覺筆記已交付 |
| Johannes STEAM 問答 | **2026-11-17 14:00–15:00** 校內高小組 | prep under `johannes-steam/` |

### Key workspace paths
```
/workspace/family-growth/
  chinese-s1-exam/     # 文言四篇＋語法文化視覺筆記
  english-s1-exam/     # 五文法視覺筆記
  oundle-interview/    # 2026-10-28 prep
  oundle-science/      # NCE-first study pack + past papers
  johannes-steam/      # STEAM 2026-11-17
  johannes-p4-english-comp-cloze-2026-10-13.md
  joshua-english-homestay-programs-2026-10-05.md
  joshua-music-boarding-programs-2026-10-05.md
/workspace/typesafe-jev/   # Jev client + thresholds
/workspace/notion-briefs-import/sync-state.json  # family-growth: 3 Finals tracked
```

### Canonical deliverable links（as of last write 2026-10-22）

**文言（四篇＋P.44–57 語法文化）— NEW canonical（舊 Doc/PDF 已 trash）**
- Doc: https://docs.google.com/document/d/1Oh-QJ7pg1JtVqMsQFMCM2UZDGTfWcClA2y_YACc1NZs/edit
- PDF: https://drive.google.com/file/d/1kmeuVDmvQPLLgdCZ5yq5_vYnszSUiZWk/view
- HTML: https://drive.google.com/file/d/1U5asbYqLPMy4D4mxlxMARlfUvTPBVZ7l/view
- Notion: https://app.notion.com/p/40177383f89c8115b1a0ff607122ba9e
- Local: `/workspace/family-growth/chinese-s1-exam/文言文四篇整合溫習筆記.{md,html,pdf}`

**英文五文法視覺筆記**
- Doc: https://docs.google.com/document/d/1yII6WHi17YxDjb7RYSNxxzwcN0b5KFIUtPMAIbfnNYU/edit
- PDF: https://drive.google.com/file/d/10EwSfth1tmSQ6uwGBYRp6x7q1bdVlErj/view （5 A4）
- HTML: https://drive.google.com/file/d/1iBgXZjtc0Qcwky5SmvgRBABHzqM-hMjD/view
- Notion: https://app.notion.com/p/40177383f89c81f88c63c2ba8999ad5b
- Local: `/workspace/family-growth/english-s1-exam/中一英文文法五要點視覺溫習筆記.{md,html,pdf}`

**Oundle interview prep**
- Local: `/workspace/family-growth/oundle-interview/joshua-oundle-interview-prep-2026-10-28.md`

### Notion sync-state（family-growth library）
Tracked Finals (3):
1. `/workspace/family-growth/oundle-interview/joshua-oundle-interview-prep-2026-10-28.md`
2. `/workspace/family-growth/english-s1-exam/中一英文文法五要點視覺溫習筆記.md`
3. `/workspace/family-growth/chinese-s1-exam/文言文四篇整合溫習筆記.md`

### Agent settings
- `notifyOnAgentUpdates`: true
- Avatar shape: cloud
- No sidebar hide noted

### Memory highlights（agent profile + journal）
- Joshua: QC S1；數感弱／理解題意弱；中英統測視覺筆記；Oundle／Epsom／King’s Y9 考試路徑進行中；CE 13+ English book 建議
- Johannes: Raimondi P4；STEAM 2026-11-17；Comp & Cloze 加強；唔太鍾意閱讀
- Justin writes 廣東話（HK written Cantonese, Traditional Chinese）

---

## 4. Secrets
- `[REDACTED:TYPESAFE_API_KEY]` — Jev／TypeSafe only via env；never paste
- No other bot-owned API tokens stored in profile
- Drive／Notion／Gmail access via user MCP connectors（session tokens not held by this bot）

---

## 5. Pending confirms
- **None** for 家庭成長副手 as of backup time.
- Noted elsewhere（唔由本 bot 執行）: BC 報名最終確認狀態曾「尚未最終確認」——屬日常小助手／Justin 跟進，本 bot 唔 act。

---

## 6. Coverage checklist
| Section | Status |
|---|---|
| Identity + ONE JOB / ANTI-JOBS / partners | ✅ |
| Historical / locked rules | ✅ |
| Live routines | ✅（empty） |
| Paths + open work | ✅ |
| Canonical Drive／Notion links | ✅ |
| Secrets redacted | ✅ |
| Pending confirms listed, not acted | ✅ |
