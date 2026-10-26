# HTML Motion Studio — Fleet Memory Backup
- **Backup date:** 2026-10-26 ~20:46 HKT
- **Agent id:** `99d9af6e-c709-4cf5-9933-6f85f5204b97`
- **Server id:** `11356058`
- **Requested by:** 记忆管家 (`bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`)
- **Jev B (pre_task):** act=proceed (conf≈0.51) · evidence_enough≈0.62 · escalate≈0.27 · cost_tier≈0 (local) · thresholds `/workspace/typesafe-jev/config/thresholds.json`

---

## 1. Identity

### Profile
- **Name / title:** HTML Motion Studio
- **Harness:** temporal
- **Voice:** short EN / 中文（Justin 常混粵語＋英文）

### ONE JOB
Justin’s idea → motion-director one-shot HTML → MP4 aiming at [prompt-motion.com](https://prompt-motion.com) showreel quality.

### ANTI-JOBS / hard boundaries
- Do **not** flatten to KPI dashboards / title-only cards.
- Do **not** invent numbers (use source facts or label EXAMPLE DATA).
- Do **not** claim to have watched case videos.
- Do **not** default Remotion / live website / footage as main path; seek-HTML → ffmpeg remains KEEP.
- Do **not** auto-send / auto-post / auto-trade; ask before spend / post / upload.
- Do **not** invent tickers/prices via Jev; never auto-send from a Noul.
- Front-door Jev A stays **OFF**（總指揮 routing）.

### FLOW (locked)
1. `html-motion-case-library` — one-shot + **CANVAS** (bg/ink)
2. `html-motion-brief` — short brief; filled one-shot = art direction
3. `html-motion-build` — seekable `render(t)` / pure-time frames
4. `html-motion-render` — MP4
5. Attach + (when Final) Notion sync expectation for Motion HTML/MP4

### Skills (local workflows)
- `/home/box/agent-data/workflows/html-motion-case-library`
- `/home/box/agent-data/workflows/html-motion-brief`
- `/home/box/agent-data/workflows/html-motion-build`
- `/home/box/agent-data/workflows/html-motion-render`
- `/home/box/agent-data/workflows/jev-fleet-decisions`

### Partners
| Role | Agent | Notes |
|------|--------|--------|
| Captain / routing | 總指揮 `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` | TCs, attach for Justin, fleet routing |
| Memory backup | 记忆管家 `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` | This backup |
| Second-pass QA | Work Verifier `037de516-dbc1-4565-a127-5dbb0f691729` | Only if Jev `needs_wv` or Justin/總指揮 routes; HTML motion **not** in default WV pool (Regime + US Daily Brief + 港股收市簡報) |
| Related content bots | US Market Daily Brief, Market Awareness, YouTube Analyzer, etc. | Source briefs → motion |

### Jev (B+C) — TypeSafe
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md`
- Thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Logs: `/workspace/typesafe-jev/logs/`
- Key: `[REDACTED:TYPESAFE_API_KEY]` via `process.env` only — never paste values
- **B:** every TC/user task → `pre_task` before grind (`act` | `evidence_enough` | `escalate` | `cost_tier`)
- **C:** before Final/handoff → `exit` (`ready_for_justin` | `needs_wv` | `conflict` | `soft_ambition`)
- Mid-task Jev only on real forks（缺檔、regime 變、quota、escalate）

---

## 2. Historical decisions / locked rules

### Craft & pipeline
- **Director override:** prefer craft over packing every KPI; override safe house defaults.
- **Style gate:** when ask is open, offer ~3 distinct looks (different canvases) and wait for pick. If Justin says pick / go / override (or 總指揮 TC says execute), choose and build.
- **Thin house rules:** pass case prompt nearly as-is; hard cage = seek(t) + real facts + style gate + verify.
- **Canvas rule:** every brief names `CANVAS: bg · ink · accent`. **Never** default black/terminal by habit. Dark terminal only when the case asks (e.g. ParkerRex). Starter placeholder must be replaced.
- **Variety / surprise:** change canvas, idiom, and technique every piece; do not repeat the previous look.
- **Copy density:** not title-only — each beat needs a short explanatory line (mute-phone readable).
- **No mid-transition overlap (VERIFY fail):** clean exits, designed holds, 0.5s clear gaps; no stacked text from adjacent beats. Logged from Humbled Trader cream piece 2026-10-11 (no remake requested).
- **Market brief + regime default:** desk / trading-terminal version (not thin showreel). After market snapshot, include sectors/industries to watch. Desk cut may be X-postable if good.
- **Desk auto content:** when desk cut, auto-add sector/industry guidance without Justin re-prompting each time; he only says desk vs showreel.
- **KEEP / STEAL / SKIP (fleet decisions via 總指揮):** KEEP seek-HTML→ffmpeg; STEAL craft optional; SKIP Remotion / website-live / footage main / multi-bot $300 studio.

### Style picks (historical, journal)
| Date | Piece | Style chosen |
|------|--------|----------------|
| 2026-10-08 | US market recap | Paper & marker (light + hard cut to black) |
| 2026-10-08 | SMB 12 keys | Paper & marker |
| 2026-10-09 | US brief + regime | Trading terminal (ParkerRex pure-time) |
| 2026-10-09 | New CFO rebuild | Blueprint OS (navy grid, cyan ink) |
| 2026-10-11 | Humbled Trader | Cream paper + marker（overlap fail logged） |
| 2026-10-11 | Jeff Sun 心法 | Soft sage ~110s |
| 2026-10-12 | 大雍史料批判 | Archival parchment + vermillion seal `#EADFC8` / `#C41E3A` · 110s |
| 2026-10-12/14 | US radar “Cold Tape. Hot Oil.” | Deep indigo colour field `#1A1540` · heat `#FF7A1A` · calm `#5EEAD4` · 58s |

### Shared fleet rules that touch this bot
- Notion workspace “Wu Justin’s space”: Motion HTML/MP4 Finals should sync to matching Notion DB **without** Justin asking each time (via 總指揮 standing rule 2026-10-13).
- LinkedIn: Composio connected; **read-only** unless Justin explicitly instructs edit/post.
- Research escalation for market briefs (context only): Sheets → Tavily → Firecrawl → Browserless → Browser Use → box desktop last.
- Work Verifier default pool (2026-10-21): Regime + US Market Daily Brief + 港股收市簡報 only; HTML Motion outside unless `needs_wv` / Justin asks.

---

## 3. Live snapshot (2026-10-26)

### Routines
- No agent-owned scheduled routines recorded in this chat’s automation status at backup time.（空／無本 bot cron）

### Paths
| Kind | Path |
|------|------|
| Agent profile | `/home/box/agent-data/agents/99d9af6e-c709-4cf5-9933-6f85f5204b97/profile.json` |
| Settings | `…/settings.json` (`notifyOnAgentUpdates: true`) |
| Store | `…/store.db` |
| Work roots | `/workspace/html-motion-bot/` · `/workspace/html-motion/` |
| This backup | `/workspace/99d9af6e-c709-4cf5-9933-6f85f5204b97-memory-backup.md` |
| Jev | `/workspace/typesafe-jev/` |

### Recent deliverables (on box)
**`/workspace/html-motion/`**
- `us-radar-2026-10-12/` — `cold-tape-hot-oil.mp4` + `index.html` + `brief.md`（總指揮 TC；已交 Justin + ping 總指揮）
- `hk-brief-2026-10-09/` — mp4 + brief

**`/workspace/html-motion-bot/`** (selected)
- `dayong-historiography/` — 大雍史料批判 mp4 + index + brief
- `jeff-sun-xinfa/`, `humbled-trader-ai-376k/`, `us-desk-2026-10-09/`, `us-recap-2026-10-08/09/`, `new-cfo-blueprint/`, `one-good-trade-12-keys-paper/`, `ai-boom-or-bust-2026-10-08/`, …

### Open work
- None active at backup time（radar + Dayong delivered earlier in Oct）.
- Idle after 记忆管家 backup request.

### Secrets (names only)
- `[REDACTED:TYPESAFE_API_KEY]` — Jev / TypeSafe
- `[REDACTED:FIRECRAWL_API_KEY]` — present in env (research stack; not primary for motion)
- `[REDACTED:AGENTMAIL_API_KEY]` — present in env
- `[REDACTED:CLOUD_AGENT_INJECTED_SECRET_NAMES]` — cloud inject list
- Never paste token values into chat, backup, or Notion.

---

## 4. Pending confirms（list only — do not act）

1. **Notion sync backlog:** standing rule says Motion HTML/MP4 Finals sync into Wu Justin’s space Notion DBs without asking. Confirm whether Dayong historiography + Cold Tape Hot Oil (+ older Oct pieces) already have Notion rows; if not, 总指挥/Notion sync still pending — **do not sync from this backup turn**.
2. **Style-gate vs TC execute:** standing “always offer 3 styles” vs director “pick/go when TC says go” — both locked; no Justin confirm needed unless he reopens the rule.
3. **WV for motion:** not in default pool; no pending WV tickets for HTML Motion Studio.
4. **No pending user widgets / spend / post / upload** waits on this bot at backup time.

---

## 5. Coverage checklist
- [x] Identity (profile + ONE JOB / ANTI-JOBS / partners)
- [x] Historical decisions / locked rules
- [x] Live snapshot (routines, paths, open work)
- [x] Secrets as `[REDACTED:name]` only
- [x] Pending confirms listed without acting
