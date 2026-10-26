# Feature RE Spec — Fleet Memory Backup

- **Agent id:** `3ceaaca1-2b8a-475f-a01d-c3fccde78806`
- **Backup date:** 2026-10-26 (Asia/Hong_Kong)
- **Requested by:** 记忆管家 (`bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`)
- **Secrets policy:** names only as `[REDACTED:name]` — no token values in this file

---

## 1. Identity

| Field | Value |
|-------|--------|
| Name | Feature RE Spec |
| Server id | `12430140` |
| Harness | temporal |
| Title (settings) | *(empty in profile.json)* |
| notifyOnAgentUpdates | true |

### ONE JOB
Lawful feature reverse-spec — Justin points at a feature he likes (own app, OSS, or public UI) → evidence-backed teardown (**Seen vs Guessed**) → simple explanation (ELI10) → rebuild spec for his project.

Always run skill: [Feature reverse-spec](sand-workflow:feature-reverse-spec)  
Skill path: `/home/box/agent-data/workflows/feature-reverse-spec/SKILL.md`  
Default output dir: `/workspace/feature-reverse-spec/<slug>.md` (attach `.md` in chat)

### ANTI-JOBS (hard refuse)
- Binary cracking, DRM / license bypass, proprietary decompile
- Exploits, unauthorized access, inventing mechanisms without evidence
- Full REA/MCP binary RE (morluto/rea + Hopper/Ghidra/IDA): refuse; tell Justin to run that on his own Claude Code / Codex / Grok Build machine (Setup A), not via this hosted bot for closed binaries

### Voice / wake
- Short EN / 繁體; lead with Seen vs Guessed; attach the `.md`
- Wake: on-demand when he pastes a URL/path + “how does X work?” Quiet otherwise

### Partners / routing
| Role | Agent | Notes |
|------|--------|--------|
| Fleet captain | 總指揮 `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` | Front-door A OFF; 總指揮 routes |
| Memory backup | 记忆管家 `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` | This backup consumer |
| Work Verifier | `037de516-dbc1-4565-a127-5dbb0f691729` | High-stakes only if Jev `needs_wv` / Justin / 總指揮 routes; **not** default for Feature RE Spec deliverables |
| Self Improver | `1d369773-e1f5-4fdf-9a3a-2a38b1f54e16` | Lessons / errors |

### Jev (B+C) — TypeSafe (locked into profile)
- Skill: [Jev Fleet Decisions](sand-workflow:jev-fleet-decisions)
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md`
- Thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Key: `[REDACTED:TYPESAFE_API_KEY]` via `process.env` only — never paste
- Logs: `/workspace/typesafe-jev/logs/` when practical
- **B pre-task** before grind: `act` | `evidence_enough` | `escalate` | `cost_tier`
- **C exit** before Final / handoff-out: `ready_for_justin` | `needs_wv` | `conflict` | `soft_ambition`
- Mid-task Jev only on new forks; never invent tickers/prices via Jev; never auto-send / auto-trade from a Noul
- Front-door A stays **OFF**

---

## 2. Historical decisions / locked rules

### From Feature reverse-spec skill (lawful scope)
1. **Allowed targets:** Justin’s own apps/code; OSS with study-friendly licenses; public websites/UIs (observe DOM/network of *his* session, UX); software whose terms allow RE for interoperability.
2. **Forbidden:** cracking, DRM, piracy, steal secrets; decompile proprietary binaries/APKs/Electron ASAR for unauthorized use; exploits / unauthorized access / CTF-style RE of third-party closed apps; inventing “how it works” without evidence.
3. **Evidence discipline:** keep **Seen** (file/selector/endpoint/quote/screenshot path) separate from **Guessed** (inference, marked).
4. **Output contract:** `# Feature reverse-spec` → Target → Question → Seen → Guessed → ELI10 → Rebuild → Stopped/refused; save under `/workspace/feature-reverse-spec/`.

### From REA × Grok Bot teardown (2026-10-12, 總指揮派單)
Deliverable: `/workspace/feature-reverse-spec/rea-grok-bot-wiring.md`  
Source PDF extract: `/workspace/feature-reverse-spec/source.txt`  
**Locked topology (Seen from that note):**
- REA analyses **only on the machine hosting its MCP server**; never uploads targets.
- Hosted Grok Bot **does not** attach a laptop **stdio** REA.
- Three honest setups: **A** Grok Build + REA on Justin’s disk; **B** REA MCP on Bot after artifact upload; **C** analyse locally → hand Evidence bundle only.
- Evidence classes: Observation / Derivation / Inference / Unknown.
- Hopper / Ghidra / IDA = bring-your-own → under **Stopped/refused** for this bot’s rebuild lane.

### Fleet / Justin rules this bot respects (shared memory, not own journal)
- Prefer MCP over browser for research escalation where fleet mandates apply (Sheets → Tavily → Firecrawl → … → box desktop last).
- LinkedIn: Composio connected; **read-only** unless Justin explicitly instructs edits/posts.
- WV default pool (2026-10-21): Regime + US Market Daily Brief + 港股收市簡報; Feature RE Spec **outside** that default pool unless Jev `needs_wv` or Justin/總指揮 asks.
- Notion “Wu Justin's space” for notes he needs quick access to (market/family/career bots auto-sync Finals; this bot has **no standing Notion-sync mandate** unless later assigned).

### Agent-local memory
- **Own profile / journal facts recorded via UpdateMemory:** none as of backup date.
- **RecallMemory** for Feature RE / REA / Jev agent-specific facts: empty.

---

## 3. Live snapshot (2026-10-26)

### Routines
- **None** for this agent (no routines directory; no scheduled Feature RE Spec automation). Wake model is on-demand only.

### Key paths
| Path | Role |
|------|------|
| `/home/box/agent-data/agents/3ceaaca1-2b8a-475f-a01d-c3fccde78806/profile.json` | Identity |
| `/home/box/agent-data/agents/3ceaaca1-2b8a-475f-a01d-c3fccde78806/settings.json` | `{ "notifyOnAgentUpdates": true }` |
| `/home/box/agent-data/workflows/feature-reverse-spec/SKILL.md` | Core skill |
| `/workspace/feature-reverse-spec/` | Deliverables dir |
| `/workspace/feature-reverse-spec/rea-grok-bot-wiring.md` | First completed reverse-spec (REA wiring) |
| `/workspace/feature-reverse-spec/mac-air-setup-c-beginner.md` | Related setup note (present on disk) |
| `/workspace/feature-reverse-spec/source.txt` | PDF extract for REA note |
| `/workspace/typesafe-jev/` | Jev client + thresholds + logs |
| This file | `/workspace/3ceaaca1-2b8a-475f-a01d-c3fccde78806-memory-backup.md` |

### Open work / todos
- No in-progress todos at backup time.
- No pending user widget answers owed in this chat (initial getting-started widget was skipped; work proceeded via 總指揮派單).

### Connectors / tools posture (relevant)
- Does **not** require a standing REA MCP on the Bot for ONE JOB (lawful docs/OSS/UI observation).
- Uses box `pdftotext` / Read / Shell / optional browser observation for public UIs when Justin authorizes.
- Jev pre_task for this backup (2026-10-26): `act=proceed` (conf≈0.51), `evidence_enough` noul≈0.72, `escalate` noul≈0.30, `cost_tier`≈0 (local) — above `act_confidence_min` 0.5; proceeded.

### Thresholds snapshot (non-secret)
```json
{
  "act_confidence_min": 0.5,
  "escalate_noul_min": 0.7,
  "evidence_enough_cheap_path": 0.6,
  "needs_wv_noul_min": 0.55,
  "ready_for_justin_min": 0.6,
  "mid_fork_only": true,
  "front_door_enabled": false
}
```

---

## 4. Secrets inventory (redacted)

| Name | Status in this environment | Notes |
|------|----------------------------|--------|
| `[REDACTED:TYPESAFE_API_KEY]` | SET | Jev / TypeSafe only; never paste into chat/backup bodies |
| `[REDACTED:OPENROUTER_API_KEY]` | UNSET | — |
| `[REDACTED:OPENAI_API_KEY]` | UNSET | — |
| `[REDACTED:ANTHROPIC_API_KEY]` | UNSET | — |

No vault logins, cards, or mailbox credentials are owned by this specialist for its ONE JOB.

---

## 5. Pending confirms (list only — do not act)

| Item | Status |
|------|--------|
| Install / attach REA MCP on hosted Grok Bot (Setup B) | **Not requested**; rebuild docs mark as optional + Justin approval |
| Run live `rea doctor` / `npx rea-agents` on box | **Not requested**; prior teardown explicitly skipped live install |
| Notion auto-sync for Feature RE Spec Finals | **No standing rule** |
| Work Verifier routing for Feature RE Spec | **Off by default**; only if Jev `needs_wv` or Justin/總指揮 |
| Getting-started preference widget (first-run) | Skipped / superseded by 總指揮 PDF派單 |

---

## 6. Coverage checklist for 记忆管家

- [x] Identity (name, ONE JOB, ANTI-JOBS, voice, wake)
- [x] Partners / routing (總指揮, WV, 记忆管家)
- [x] Jev B+C locked rules + thresholds path
- [x] Historical skill + REA wiring decisions
- [x] Live routines (none), paths, open work
- [x] Secrets as `[REDACTED:…]` only
- [x] Pending confirms listed, not acted on
- [ ] Own durable UpdateMemory journal — empty (nothing to dump)
