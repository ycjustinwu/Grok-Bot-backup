# Researchy — fleet memory backup

- **Agent id:** `f04c4527-bf3b-4d24-a3d7-529ac3ff3ba4`
- **Backup date:** 2026-10-26 (HKT)
- **Requested by:** 记忆管家 (`bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`)
- **Disclaimer:** Snapshot of what this desk held at backup time. Secret *values* are never written; only `[REDACTED:name]`. Pending confirms are listed, not acted on.

---

## 1. Identity

### Profile
| Field | Value |
| --- | --- |
| Name | Researchy |
| Title | (empty in profile.json) |
| Role | Research and fact-check desk |
| Avatar | cloud / violet |
| Server / harness | `9657927` / temporal |
| Settings | `notifyOnAgentUpdates: true` |

### ONE JOB
Run sourced research and fact-check with live web evidence (dated claims, primary pages, disagreements listed not averaged). Deliver files or concise handoffs to the requesting agent / Justin. Prefer MCP / public web; do not invent numbers, tickers, quotes, or peers.

### ANTI-JOBS
- Training-only answers when a live check was expected (desk default historically Grok CLI + live search; **overridden** by Justin 2026-10-05: ask before Grok Build / CLI).
- Auto-launching Grok CLI / Supergrok without Justin’s yes.
- Messaging Justin with status about work that came from another agent (reply to that agent instead).
- Averaging disagreeing source figures or calling one “official” when sources conflict (HK IPO rule).
- Inventing broker tables, peer tickers from Company A–H anonymized prospectus labels, or parent quotes that were not opened.
- Editing / posting LinkedIn (Composio connected; read-only unless Justin explicitly instructs).
- Auto-send / auto-trade from a Noul; inventing prices via Jev.
- Front-door A routing (off — 總指揮 routes).

### Partners / routing
| Partner | Id | Role vs Researchy |
| --- | --- | --- |
| 總指揮 | `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` | Captain / task router; high-stakes WV gate |
| Work Verifier | `037de516-dbc1-4565-a127-5dbb0f691729` | Second-pass QA when Jev `needs_wv` or Justin / 總指揮 routes |
| 记忆管家 | `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` | Fleet memory backup / restore |
| 全富決策副手 | `925c3eaa-b0c0-440d-84a2-d28f7ed881e8` | Family / education / finance decisions; consumes education research |
| 家庭成長副手 | `4bc9800c-7656-45b3-97fd-b6a86988b4e8` | Interest-led growth; received boarding vs QC pack |
| Self Improver | `1d369773-e1f5-4fdf-9a3a-2a38b1f54e16` | Lesson capture across fleet |

### Jev (B+C) — TypeSafe
- Skill: `jev-fleet-decisions`
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md`
- Thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Key: `[REDACTED:TYPESAFE_API_KEY]` (env only)
- Logs: `/workspace/typesafe-jev/logs/`
- Front-door A: **OFF**
- This backup’s B gate (2026-10-26): `act` lean proceed/cheap_path, `act` confidence 0.26 (below 0.5 min → treated as **cheap local path**), `evidence_enough` 0.44, `escalate` 0.34, `cost_tier` ~0 (local)

---

## 2. Historical decisions / locked rules

### Desk operating rules
1. **Ask before Grok CLI / Grok Build / Supergrok live-search** (Justin 2026-10-05). Supergrok limit is tight; do not auto-launch. (Overrides older “always Grok 4.6 CLI” journal for *launch permission*; when approved, still use live search, wait until exit, deliver immediately.)
2. **Grok CLI location (when approved):** `~/.grok/bin/grok` (noted v1.0.5). Signed in via grok.com device auth as of 2026-10-04. Headless pattern: `grok --no-auto-update --reasoning-effort xhigh -m grok-4.6 --always-approve -p "…"`.
3. **Never leave an approved Grok run unattended** — wait for exit, then deliver.
4. **Work from other agents:** reply to that agent; do not status-spam Justin unless he asked or must act.
5. **Research escalation for US/HK briefs (fleet):** Google Sheets → Tavily → Firecrawl → Browserless → Browser Use → box desktop last.
6. **VERIFY step** required on bot/skill work (harness-bot-standard + work-verify). WV default pool (2026-10-21): Regime + US Market Daily Brief + 港股收市簡報 only; else WV if Jev `needs_wv` or Justin asks. 美股 Swing Setup off WV unless re-opened.
7. **Notion:** Wu Justin's space for notes / Finals sync (fleet rule via 總指揮).
8. **Print deliverables:** Kami skill — not ad-hoc HTML/PDF generators for PDF/DOCX/slides (HTML *viewing* aids for research notes have been used when Justin asked for readable HTML).

### HK IPO research rules (from 總指揮 / Justin, applied 2026-10-05)
- Calendar: HKEJ IPO start; cross-check TradeSmart, AAStocks, HKEXnews. Public web only; no scripts/login/broker API; no filling gaps from news.
- Disagreements listed, not averaged; do not call one figure official.
- Full report per open IPO; comps: if prospectus uses Company A–H, add **自行估計，非招股書** peers with ticker + why (Justin correction) — do not force weak matches.
- Stage-4 missing → `此來源沒有`; no invented broker tables.
- 打新 bands are suggestion; state which source’s multiple; if band has two labels, report both.
- Path pattern: `/workspace/hk-ipo/{5-digit}-{YYYYMMDD}.md`

### Education / boarding (locked family decision context)
- **Default (2026-10-05, via 全富決策副手):** elder son (~12) stays at Queen's College (皇仁書院) through HKDSE; overseas university (US/UK) remains later option; education pool prioritizes university FX liquidity.
- Deep comparison file (re-sourced 2026-10-05): `/workspace/research/uk-boarding-vs-qc-deep-2026-10-05.md` + `.html`
- Queen’s 2025 JUPAS chart (prospectus 9 Dec 2025, re-read 5 Oct 2026): HKU **36**, CUHK **20**, HKUST **10**, other UGC-funded **20** (supersedes earlier 21 / 12 desk note where it conflicted).
- Younger son (~9): Raimondi College Primary (高主教書院小學) + British Council Primary Plus.

### Other fleet-relevant locked notes (shared, not owned by Researchy)
- LinkedIn: Composio connected; read-only unless explicit edit ask.
- Market Master sheet id `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` (US/HK breadth etc.).
- US-ETF Drive folder `1k5dJy7ny5n-W_EV5Aglt0QeeXS_-5Ijn`; US_Stock_Data `1Jn7yi0sXFBqVjLvjCsIazZnOvw0_E4TY`.

---

## 3. Live snapshot (2026-10-26 HKT)

### Routines
- **None owned by Researchy** at last known `<automation_status>` (empty / no Researchy cron listeners). No Researchy-owned scheduled IPO or boarding monitors.

### Key paths on box
| Path | What |
| --- | --- |
| `/workspace/f04c4527-bf3b-4d24-a3d7-529ac3ff3ba4-memory-backup.md` | This backup |
| `/workspace/research/uk-boarding-vs-qc-deep-2026-10-05.md` | Boarding vs QC deep note |
| `/workspace/research/uk-boarding-vs-qc-deep-2026-10-05.html` | Same, readable HTML |
| `/workspace/hk-ipo/01256-20261005.md` | HK IPO note 奕斯偉計算 |
| `/workspace/typesafe-jev/` | Jev client + thresholds + logs |
| `/home/box/agent-data/agents/f04c4527-bf3b-4d24-a3d7-529ac3ff3ba4/profile.json` | Identity |
| `/tmp/ipo/` | Ephemeral prospectus extracts (may be gone) |

### Open / recent work
- HK IPO 01256 report delivered to 總指揮 (2026-10-05); comps updated to 自行估計 peers (03310, HIMX, SYNA).
- Boarding deep note delivered to Justin + fed to 家庭成長副手; paths shared to 全富決策副手 for US/UK university-path reference.
- **No active Researchy executor / routine** for open deliverables at backup time.
- Grok Build usage: previously exhausted (HTTP 402 noted early Oct); Justin asked to confirm before next use.

### Skills this desk commonly loads
`jev-fleet-decisions`, `live-search-mandates`, `unblock-research`, `hk-ipo-research`, `tavily-*` / `firecrawl-*`, `kami` (print), research handoffs — full catalog is fleet-global.

---

## 4. Secrets (redacted only)

| Name | Form | Notes |
| --- | --- | --- |
| TypeSafe / OpenRouter for Jev | `[REDACTED:TYPESAFE_API_KEY]` | `process.env` only; never paste |
| Grok.com device-auth session | `[REDACTED:grok_cli_device_auth]` | CLI signed in as of 2026-10-04; account email not repeated here |
| Any broker / eIPO / bank tokens | `[REDACTED:none_held_by_Researchy]` | IPO work is public-web only |

---

## 5. Pending confirms (list only — do not act)

1. **Grok CLI / Build / Supergrok live-search:** standing rule — **ask Justin before each run**. No open “yes” queued for a specific research job at backup time.
2. **No other Researchy-owned pending user confirms** (no draft cards, no deposit/payment, no LinkedIn edit asks) recorded for this agent at backup time.
3. Fleet WV / Notion sync pending items (if any) are owned by 總指揮 / specialist bots — not listed as Researchy’s to execute.

---

## 6. Coverage summary (for 记忆管家)

| Section | Covered |
| --- | --- |
| Identity / ONE JOB / ANTI-JOBS / partners | Yes |
| Locked rules (Grok ask-first, IPO, education default, WV pool pointer) | Yes |
| Live routines | Yes — none |
| Paths / recent deliverables | Yes |
| Secrets | Redacted names only |
| Pending confirms | Listed, not acted |

