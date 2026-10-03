---
name: work-verify
description: >-
  Use this to independently verify a Grok Bot deliverable before Justin treats
  it as final — Launch→Doctor→Drive→Evidence→Cleanup; emit PASS |
  PASS_WITH_NOTES | FAIL; write verify-YYYYMMDD-HHMM.md (HKT).
---
# Work verify

Fleet QA harness for **Work Verifier**. Surfaces = producer deliverable types (see `verify-work-verifier/features/`). Drive the real on-disk artifacts the way Justin will read them — not chat claims alone.

**Stack choice:** This skill owns Launch / Doctor / Drive / Evidence / Cleanup. `verify-work-verifier` is a thin control index + feature map only (no duplicate checklist).

## Launch (intake)

From 總指揮 or Justin, capture before any deep check:

| Field | Required |
|-------|----------|
| Producer bot name (and id if known) | yes |
| Claim / summary of what was delivered | yes |
| Paths under `/workspace/...` (deliverable + supporting pack) | yes |
| Done criteria / IO contract (schema, MARKET, handoff fields) | yes |
| Ticket / session date (HKT) | preferred |

Locate every claimed path on disk. Missing primary deliverable → prepare **FAIL** (still write Evidence). Do not invent paths. Scratch only under `/workspace/work-verifier/scratch/<run-id>/`.

Ready signal: intake table complete + primary path `stat`-able.

## Doctor (pre-drive gate)

Read-only. Answer: “is this pack worth deep Drive?”

1. **Paths exist** — primary deliverable + listed supports; note optional absences (e.g. PDF when MD-only is allowed).
2. **Schema sanity** — producer IO contract shape present enough to Drive (required H1/H2, CSV columns, HANDOFF labels, MARKET=HK|US). Empty optional sections OK if producer allows skip.
3. **Session / MARKET label** — date in filename or header matches claimed session; HK vs US not silently mixed.
4. **Source pack coherence** — seed JSON/CSV/extracts that the claim cites are present or explicitly gap-labeled in the deliverable.
5. **ANTI_JOBS smoke** — quick scan for wrong-bot outputs (e.g. Regime TOTAL inside HK brief; baoyu image when Fusion default is MD+prompt only).

Doctor outcomes:

- **GO** — proceed to Drive with the matching feature file.
- **NO-GO** — Evidence with **FAIL** (missing primary / wrong market / unusable schema). Do not “fix” producer files.

Doctor does **not** re-run the producer pipeline.

## Drive

Open `verify-work-verifier/features/<feature>.md` for the producer surface. Execute its checklist:

1. Schema / sections / required fields
2. No-fabricate trace (numbers → on-disk sources or labeled gaps)
3. Seed / CSV / extract cross-check
4. ANTI_JOBS boundary
5. Internal consistency (summary ↔ tables ↔ MARKET)
6. Reversibility flags (orders, posts, deletes)
7. Soft-evidence class → **NOTES** (not auto-FAIL): secondary sources, names absent from seed JSON but not contradicted, rounding, soft mcap notes

Prefer disk evidence over chat. Spot-check; full re-analysis only when needed to prove FAIL.

## Evidence

Write:

`/workspace/work-verifier/output/verify-YYYYMMDD-HHMM.md`

Timestamp = **Asia/Hong_Kong**. Then update:

`/workspace/work-verifier/output/LATEST.txt`

→ single line = report basename (e.g. `verify-20260910-1844.md`).

### Report skeleton

```markdown
# Work Verify Report — <ticket>

- **VERDICT:** PASS | PASS_WITH_NOTES | FAIL
- **Ticket:** …
- **Producer:** …
- **Session:** …
- **Deliverable:** `path`
- **Verified at:** YYYY-MM-DD HH:MM HKT
- **Verifier:** Work Verifier

## Artifacts checked
| Path | Status |

## Doctor
GO | NO-GO + bullets

## Checklist
(feature-map items → PASS / NOTES / FAIL)

## Findings
(3–7 bullets)

## Verdict rationale
## Escalation
```

**VERDICT rules**

| Verdict | When |
|---------|------|
| **PASS** | Schema OK; traces hold; ANTI_JOBS held; no material soft gaps |
| **PASS_WITH_NOTES** | Deliverable usable; soft source / incomplete seed trace / immaterial rounding / soft mcap — labeled |
| **FAIL** | Missing primary; fabricate; schema break; ANTI_JOBS breach; MARKET mix without label; irreversible act without Justin gate |

Never upgrade a producer technical VERDICT (WATCH→BUY). Never mutate producer outputs.

## Cleanup

- Delete only own scratch under `/workspace/work-verifier/scratch/<run-id>/`.
- **Never** delete or edit producer files, input packs, or Evidence reports.
- Evidence and `LATEST.txt` survive Cleanup.

## Reply / escalate

Reply to **總指揮** with VERDICT + 3–7 bullets + report path.  
**FAIL** → 總指揮 escalates to Justin (Work Verifier is the escalator, not a silent fixer).

## Self-VERIFY (this skill)

- [ ] Intake fields captured; paths from disk
- [ ] Doctor run before Drive
- [ ] Feature file used matches producer
- [ ] Report written; LATEST.txt updated (HKT stamp)
- [ ] Only scratch cleaned; producer files untouched
- [ ] VERDICT ∈ {PASS, PASS_WITH_NOTES, FAIL}
