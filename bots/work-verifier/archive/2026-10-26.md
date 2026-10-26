# Work Verifier — durable memory disaster-recovery snapshot

- **Bot:** Work Verifier
- **Agent id:** `037de516-dbc1-4565-a127-5dbb0f691729`
- **Server id:** `2410896`
- **Slug (fleet):** work-verifier
- **Snapshot at:** 2026-10-03 20:10 HKT (UTC+8)
- **Writer:** Work Verifier (self) for 记忆管家 full-fleet backup
- **Supersedes:** `/workspace/2410896-memory-backup.md` (2026-09-14 20:32 HKT)
- **Secrets:** placeholders only — no real tokens in this file

---

## Identity

- **Name:** Work Verifier
- **Title:** empty in profile.json
- **User:** Justin Wu (Asia/Hong_Kong, UTC+8)
- **Voice:** short / technical
- **Harness (profile.json):** temporal. Work surface is the shared box (`/workspace`, `/home/box`).
- **Avatar:** pebble / brown. No custom picture at snapshot.
- **namedBy:** user
- **Settings:** `notifyOnAgentUpdates: true`. Not hidden from sidebar. Drafts not disabled in settings.json.
- **ONE JOB:** Independent second-pass QA. Audit another bot’s **on-disk** deliverable BEFORE Justin treats it as final. Issue `VERDICT: PASS | PASS_WITH_NOTES | FAIL`. Escalator on FAIL via 總指揮 → Justin; not a silent fixer.
- **When to run (high-stakes):** 港股/美股 Swing Setup · 投資敘事分析師 · Fusion Formatter · Market Awareness Orchestrator · US Market Daily Brief · 港股收市簡報 · any published brief Justin flags. Skip routine scanner scoreboards unless asked.
- **When NOT to run Swing Setup verify:** only after an explicit Setup TC Justin authorized. Drive pullback-buy Excel + Pine screener lists are Potential Setups only. Auto-handoff Setup outputs are archival/reference, not pipeline finals.
- **Pipeline:** Launch → Doctor → Drive → Evidence → Cleanup
  - Skills: `work-verify` + matching feature map under `verify-work-verifier/features/`
  - Regime overlay checklist: `/workspace/work-verifier/checklists/ETF-RS-overlay-TC-20260924-08.md`
  - Evidence: `/workspace/work-verifier/output/verify-YYYYMMDD-HHMM.md` (HKT) + update `LATEST.txt`
  - Scratch only: `/workspace/work-verifier/scratch/<run-id>/` — cd out before delete. Never mutate producer files.
- **IO:** In = producer `/workspace/...` paths + intake from 總指揮 or Justin. Out = verify reports + `LATEST.txt` only.
- **Reply contract:** Always reply 總指揮 with VERDICT + report path + 3–7 bullets. FAIL escalates to Justin via 總指揮. PASS_WITH_NOTES is safe-for-Justin-with-notes, not FAIL.
- **VERIFY axes:** Schema/IO · no-fabricate · ANTI_JOBS · MARKET label · handoff fields · reversibility. Soft labelled gaps (secondary source, seed-absent names, rounding, soft mcap, labelled stale series) → PASS_WITH_NOTES. Missing primary deliverable / fabrication / schema break / wrong TOTAL or band / unsourced wrong figure stated as fact → FAIL.
- **ANTI-JOBS:** Do not re-do the producer’s full analysis unless needed to prove FAIL. Do not upgrade a technical VERDICT (WATCH→BUY). Do not invent missing data. Do not post externally. Do not produce Regime reports (if Justin asks Work Verifier to “run Market Awareness”, forward to 總指揮).
- **Fusion default check:** report MD + infographic prompt; no baoyu image unless Justin asked.
- **Orchestrator:** 總指揮 (`7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`)
- **Backup peer:** 记忆管家 (`bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`)
- **Routines:** none.
- **Connectors owned:** none for delivery. Disk QA only. No tokens stored in agent memory.
- **Durable profile memory:** `/home/box/agent-data/agents/037de516-dbc1-4565-a127-5dbb0f691729/memory/profile.md`
- **Usage gate file (fleet, 2026-09-20):** same folder `memory/USAGE_GATE.md` — reuse a fresh artifact; stop after the same approach fails twice; chat-only if no tools needed; prefer connector/API over clicking; do not create extra bots or routines to save usage.
- **User-memory shard:** `/home/box/agent-data/user-memory/by-agent/037de516-dbc1-4565-a127-5dbb0f691729` — empty at snapshot.

---

## Historical decisions

### Process / policy (durable)

1. **Hybrid verification live (2026-09-08, via 總指揮):** Every bot/skill includes a VERIFY step (`harness-bot-standard` + `work-verify`). Work Verifier is the independent second-pass. Writes `/workspace/work-verifier/output/`. 總指揮 routes high-stakes before Justin treats as final.
2. **Swing Setup authorization gate (2026-09-09, TC-20260909-09 HOLD):** Independent verify only after an explicit Setup TC Justin authorized. Drive pullback-buy Excel + Pine lists = Potential Setups. Auto-handoff Setup outputs = archival/reference. A technical PASS on an unauthorized auto-handoff becomes PROCESS_HOLD / not a pipeline final.
3. **US scanner lesson (2026-09-09, via Self Improver):** Justin corrected that US Swing Scanner pulls the Google Drive Pullback buy Excel first. Do not treat pullback-buy candidates as Pine-list BUY filters (TGB/ANET/SLS confusion).
4. **JD refine (2026-09-11, TC-20260911-03):** Launch→Doctor→Drive→Evidence→Cleanup + feature maps under `verify-work-verifier/features/`.
5. **Usage gate (2026-09-20, Justin, all bots):** see Identity. Saved as `USAGE_GATE.md` on this agent.
6. **HK after-close brief rule change (2026-09-30, via 總指揮, effective next HK brief; first applied on the 2026-10-02 brief):** Remove the 100億 H-share market-cap gate. Do not FAIL seeds on H-cap. Justin TradingView AV UP/DOWN inputs are always valid — do not FAIL on Yahoo price/RV/name mismatch if the brief keeps Justin’s numbers and labels the gap. If checks find no problem, verification detail auto-hides. HK Market Monitor is same-day, not D+1. Markdown-only is fine.
7. **US Daily Brief (standing):** Justin TradingView prices/RV/names are authoritative. Do not FAIL on Yahoo mismatch if the brief keeps Justin’s numbers and labels the gap. Market-cap gate remains $10B (US only). Soft-FAIL must be labelled. Epicenter: |1D| ≥ 10% AND RV ≥ 4× on Justin’s tape. Abnormal volume only from Justin’s manual list (no TradingView screener). ≥2 sourced catalyst facts per focus name. No Regime TOTAL in the brief. Part 6 is the US→HK theme map (no invented HK prices). Part 4 covers major policy, not only tariffs. Watch contract-roll errors (Yahoo `BZ=F` / `GC=F` can roll early; compare the same contract).
8. **Research escalation (2026-09-30, via 總指揮):** Prefer MCP over browser. Google Sheets → Tavily → Firecrawl → Browserless → Browser Use → box desktop last. Browser-first is a soft note unless it caused fabrication.
9. **Infographic / print prefs (shared, not this bot’s deliverable):** HK/finance briefs prefer infographic (baoyu-infographic dashboard or dense-modules). Sketchnote for cream-paper educational. visual-director for other visuals. Kami for PDF/DOCX/print. Do not use ad-hoc HTML/PDF generators.
10. **Verdict semantics:** PASS_WITH_NOTES = safe-for-Justin-with-notes. FAIL escalates. Never change producer files.

### Regime v6.4.6 rules this bot enforces

- A out of 12 (floor −4). B out of 9.5 (floor −6.5). TOTAL out of 21.5. Scores in 0.5 increments.
- Bands: Deep Bear below 0; Bear/Avoid 0–4.5; Cautious starts at 5.0.
- Upgrade needs 2 consecutive days at the same raw band. Downgrade is immediate, lands on the new band’s floor, no ratchet.
- If raw band improves but confirmation is incomplete, effective stays the prior band with pending N/2.
- Confirmed Bear/Avoid exposure floor is 0% (stance DEFENSIVE / no new positions).
- Index DD Gate: V-REVERSAL blocked when SPX drawdown from the recent high is under 5% (stance-only). As of the 2026-10-02 skill, the gate only runs when T2108 is below 20; at or above 20 it is N/A.
- ETF RS overlay is advisory only and never counts toward TOTAL. No auto-Favor on crypto. Stale sheet → N/A + DATA GAP.
- Stockbee revises the prior day’s row. Producer should disclose it and print the revised prior score. Recurring soft note: the daily sometimes does not restate the revised score, or does not print “floor −4” on the score line even when summary JSON has `pillar_a_floor`.
- FRED VIX/VXV is often stale. If labelled, it cannot move TOTAL.
- `MARKET=US` literal expected. No Pillar C. No 5D trade-unit.
- Justin’s breadth paste is authoritative. Do not FAIL on a cross-check overwrite of those exact inputs.

### Early ticket log (from 2026-09-14 snapshot; those report files were not re-listed on disk at this snapshot)

| Ticket | Producer | Verdict | Report |
|--------|----------|---------|--------|
| TC-20260908-02 | 港股收市簡報 2026-09-08 | PASS_WITH_NOTES | `verify-20260908-1822.md` |
| TC-20260909-02 | Regime 2026-09-08 | PASS_WITH_NOTES | `verify-20260909-0756.md` |
| TC-20260909-04 | US brief 2026-09-08 | PASS_WITH_NOTES | `verify-20260909-0941.md` |
| TC-20260909-09 | US Swing Setup run-20260909-1053 (unauthorized auto) | tech PASS_WITH_NOTES → PROCESS_HOLD | `verify-20260909-1100.md` + HOLD note |
| TC-20260909-15 | SRRK Setup→Story→Fusion (authorized) | PASS_WITH_NOTES | `verify-20260909-1237.md` |
| TC-20260909-17 | 港股收市簡報 2026-09-09 | PASS_WITH_NOTES | `verify-20260909-1903.md` |
| TC-20260910-02 | 港股收市簡報 2026-09-10 (MD only) | PASS_WITH_NOTES | `verify-20260910-1844.md` |

### Verdicts confirmed in this agent’s working memory (2026-09-29 through 2026-10-03). Reports exist on disk.

| TC | Target | VERDICT | Report |
|----|--------|---------|--------|
| TC-20260929-04 | Regime 9/28, TOTAL −3.5, Deep Bear | PASS_WITH_NOTES | `verify-20260929-0728.md` |
| TC-20260929-06 | Amended Regime 9/28 (ETF RS tilt, prior 4.5→3.5, floor −4, MARKET=US) | PASS_WITH_NOTES | `verify-20260929-0808.md` |
| TC-20260929-08 | HK brief 9/29 (old H-share gate still applied) | PASS_WITH_NOTES | `verify-20260929-1851.md` |
| TC-20260930-02 | US brief 9/29 (FICO epicenter; ANDG drop) | PASS_WITH_NOTES | `verify-20260930-0734.md` |
| TC-20260930-04 | Regime 9/29, TOTAL −2.5, Deep Bear HOLD | PASS_WITH_NOTES | `verify-20260930-0802.md` |
| TC-20260930-07 | HK brief 9/30 | PASS_WITH_NOTES | `verify-20260930-1853.md` |
| TC-20261001-02 | US brief 9/30 (UTHR epicenter; CBRS=Cerebras) | PASS_WITH_NOTES | `verify-20261001-1213.md` |
| TC-20261001-04 | Regime 9/30, TOTAL −5.0, Deep Bear HOLD, Index DD Gate blocks V-REV | PASS_WITH_NOTES | `verify-20261001-1259.md` |
| TC-20261002-02 | US brief 10/01 (ACN epicenter) | PASS_WITH_NOTES | `verify-20261002-0727.md` (superseded) |
| TC-20261002-04 | US brief 10/01 SNPS rewrite (Ansys ~$35B, closed 2025-07-17) | PASS_WITH_NOTES | `verify-20261002-0737.md` |
| TC-20261002-05 | Forward only | Justin asked Work Verifier to run Market Awareness; forwarded to 總指揮. Not a verify. Became TC-20261002-06. |
| TC-20261002-06 | Regime 10/01, TOTAL +2.0, raw Bear/Avoid, effective Deep Bear pending 1/2 | PASS_WITH_NOTES | `verify-20261002-0803.md` |
| TC-20261002-09 | HK brief 10/02 (no 100億 gate; TV trust) | PASS_WITH_NOTES | `verify-20261002-1859.md` |
| TC-20261003-02 | US brief session 2026-10-02 | PASS_WITH_NOTES | `verify-20261003-1345.md` |
| TC-20261003-04 | Regime session 2026-10-02 | PASS_WITH_NOTES | `verify-20261003-1357.md` |

### Latest two results (restore context)

**TC-20261003-02 US brief, session 2026-10-02.** AV exact: UP HPE/VSH/LW/IBRX/ALGM/ON; DOWN CTVA (paste name Celanese)/STX/WDC/GDS. Epicenter NONE (STX/WDC |1D|≥10 but RV under 4×). Focus STX/WDC/HPE catalysts sourced. HPE gap labelled (brief keeps Justin 176.95; Yahoo ~69.33). CTVA labelled (Justin name Celanese kept; Yahoo is Corteva; mcap ~$7.95B soft FAIL plus Vylor pattern). SPX +0.73%, Nasdaq +1.19%, VIX 16.39→15.31. Soft note: HPE growth wording slightly blends FY26–29 CAGR with FY27 outlook.

**TC-20261003-04 Regime, session 2026-10-02.** TOTAL +0.5/21.5 (A −1.0 / B +1.5). Δ −1.5 vs revised prior +2.0. Raw Bear/Avoid. Effective confirms Bear/Avoid day 2 (up from Deep Bear). Exposure 0%. Stance DEFENSIVE. FT off. T2108 20.53 exits Reversal Watch. Index DD Gate N/A (T2108≥20). Ref dd 0.96% informational. Justin breadth all 9 exact: VIX 15.31; VIX/VXV 0.882 labelled 1d stale (10/1); SPXA50R 25.00; SPXA200R 45.40; SPXA20R 26.60; NYSI −767.23; NYMO −14.55; NAMO −11.80; NASI −624.11. Overlay fresh 2026-10-02. Favor P7/P2/L2 Japan (no crypto). Avoid Nuclear/Defense/Gold. Non-scoring. Stockbee 10/1 revision disclosed (T2108 18.9→18.99); re-score still +2.0. MARKET=US present. Soft note: daily does not print “(floor −4)” on the score line; summary JSON has `pillar_a_floor: −4`.

### Other notes that must survive restore

- Producer skill edits on 2026-09-29 (orchestrator, daily report, data ingest) only added floor wording, prior-day revision print, and MARKET line. Backups in `_skill-backups-TC-20260929-05/`.
- 02889 on the 2026-09-29 HK brief is 博泰/PATEO, not 奧園. That run still used the old H-share gate.
- Lesson: relay the verdict to 總指揮 as soon as the check finishes. TC-20260926-07 reply was missed and only sent late on 2026-09-28.
- Informational acks from 總指揮 (“shipping Final, no further action”) need no reply.
- Recurring soft gaps (not FAIL): secondary tape, seed-absent names, rounding, labelled stale FRED, soft US mcap, score line missing “floor −4” when JSON has it.

### Reports present on disk at this snapshot (`/workspace/work-verifier/output/`)

`verify-20260918-2053.md`, `verify-20260918-self-us-brief.md`, `verify-20260919-0804.md`, `verify-20260919-0816.md`, `verify-20260921-1909.md`, `verify-20260922-0710.md`, `verify-20260922-0727.md`, `verify-20260922-1918.md`, `verify-20260923-0709.md`, `verify-20260923-0729.md`, `verify-20260923-0732.md`, `verify-20260923-0745.md`, `verify-20260923-1843.md`, `verify-20260924-0711.md`, `verify-20260924-0721.md`, `verify-20260924-1848.md`, `verify-20260925-0739.md`, `verify-20260925-0806.md`, `verify-20260925-1602.md`, `verify-20260925-1726.md`, `verify-20260925-1858.md`, `verify-20260926-0940.md`, `verify-20260926-0944.md`, `verify-20260926-1008.md`, `verify-20260928-1941.md`, `verify-20260929-0710.md`, `verify-20260929-0728.md`, `verify-20260929-0808.md`, `verify-20260929-1851.md`, `verify-20260930-0734.md`, `verify-20260930-0802.md`, `verify-20260930-1853.md`, `verify-20261001-1213.md`, `verify-20261001-1259.md`, `verify-20261002-0727.md`, `verify-20261002-0737.md`, `verify-20261002-0803.md`, `verify-20261002-1859.md`, `verify-20261003-1345.md`, `verify-20261003-1357.md`.

Verdicts for files not named in the tables above were not re-read for this dump. Restore the verdict from the report file, do not invent it.

---

## Live snapshot

- **Idle.** No in-flight verify. Waiting for the next 總指揮 ticket.
- **LATEST.txt:** `verify-20261003-1357.md` (TC-20261003-04 Regime 2026-10-02, PASS_WITH_NOTES).
- **Last two delivered:** TC-20261003-02 and TC-20261003-04, both replied to 總指揮 and Justin.
- **Todos:** none open. Prior TCs through TC-20261003-04 marked complete.
- **Routines:** none.
- **Scratch:** ephemeral under `/workspace/work-verifier/scratch/`. Safe to empty on restore.
- **Profile memory fact (only line):** Swing Setup verifies only after an explicit Setup TC Justin authorized (2026-09-09).
- **No dated `memory/log/` files.** No extra user-memory shard files.
- **Pending confirms:** none from Work Verifier. No open widget. No credential request. No secret request.
- **Coverage gaps:** full chat transcript is not copied here (lives with the agent). Reports dated before 2026-09-18 that the 2026-09-14 snapshot named were not in the output directory listing at this snapshot. Mid-September verdicts between TC-20260910-02 and TC-20260929-04 are on disk as files but were not re-summarized in this dump.

---

## Secrets placeholders only

Work Verifier does not store API keys, bot tokens, or session cookies.

- `[REDACTED:CURSOR_API_KEY]` — not held
- `[REDACTED:any-mcp-token]` — not held
- `[REDACTED:github_token_or_credential]` — not held (fleet git is 记忆管家’s)
- `[REDACTED:user-session-cookie]` — never copy into verify reports or this backup

Restore: rehydrate Identity + Historical decisions + the one profile.md fact + `USAGE_GATE.md`. Re-attach skills from workflows. Do not expect secrets in this file.

---

## Coverage / pending confirms

- [x] Identity (role, IO, pipeline, ANTI-JOBS, settings, paths)
- [x] Historical decisions (authorization gate, HK/US/Regime rules through 2026-10-03, ticket verdicts this agent actually holds)
- [x] Live snapshot (LATEST, idle, no routines, no open confirms)
- [x] Secrets as `[REDACTED:name]` only
- [ ] Pending confirms: none owed by Work Verifier. 记忆管家 still needs to ingest this path into the fleet archive.
