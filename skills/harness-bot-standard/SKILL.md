---
name: harness-bot-standard
description: >-
  Use this when creating or rewriting any Grok Bot Job Description or reusable
  skill — enforce ONE_JOB, ANTI_JOBS, IO paths, VERIFY, handoff/escalation, and
  approval-by-reversibility (harness/loop engineering).
---
# Harness Bot Standard

Use this whenever creating or rewriting a Grok Bot Job Description or a reusable skill. Refuse to ship if any required gate fails.

## Required gates (all must pass)

1. **ONE_JOB** — single primary objective in one sentence.
2. **ANTI_JOBS** — explicit list of what not to do / who owns adjacent work.
3. **IO_CONTRACT** — concrete `/workspace/...` (or connector) inputs and outputs; named next bot if any.
4. **SKILLS_LOOP** — multi-step work lives in skills, not a monolith JD (JD ≤ ~400 words when possible).
5. **VERIFY** — every production skill ends with a VERIFY checklist (schema, no-fabricate, paths exist, ANTI_JOBS held) before user-facing delivery.
6. **HANDOFF / ESCALATE** — when to message the next bot vs Justin (money, deletes, ambiguity, FAIL from Work Verifier).
7. **APPROVAL_BY_REVERSIBILITY** — reversible acts may auto-run; irreversible / money / external post need Justin.

## Fleet-wide handoff rule (TC + HANDOFF)

Every TC (task card) and every bot-to-bot HANDOFF must carry these labeled fields (English labels), in addition to its own contract fields:

```text
PINNED_INPUTS:  absolute paths of the exact data files used (scanner CSVs, Summary_US/Summary_HK, regime file)
DECISIONS_MADE: Justin/coordinator rulings already settled for this job, e.g. "NBIS Stop_Type=TZ pullback exception approved 2026-10-05" | none
OPEN_QUESTIONS: unresolved items | none
NEXT_GATE:      who checks next and what passes, e.g. "Work Verifier → PASS/PASS_WITH_NOTES before Final"
```

- **Pinned inputs:** downstream bots read exactly the PINNED_INPUTS files, never "latest". A downstream bot that needs a file which is not pinned notes the path it used under OPEN_QUESTIONS. (Why: on 2026-10-05 Swing used the Oct 3 Summary_US while Story used Oct 4 → NBIS sector conflict.)
- **Decisions made:** settled rulings; downstream must not re-open them.
- **Missing field on receive:** treat as `none` and note `"<FIELD> missing upstream — treated as none"` under OPEN_QUESTIONS.
- Carry all four forward on each hop (Swing Setup → Story Search → Fusion → Work Verifier).

## Coordinator: unresponsive bot

For 總指揮 when a TC sent with priority gets no reply:
1. Re-ping the owner bot once.
2. Still silent → check the bot's transcript (ReadTranscript) for progress, errors, or a stuck step.
3. Only then run a stand-in, following the skills literally (same PINNED_INPUTS, same DECISIONS_MADE).
4. When a stand-in runs, send the owner bot a CANCEL for that TC id so only one run exists.
5. If both runs land anyway, the owner bot's run is primary; Work Verifier picks which one ships.

## Hybrid verification

- **Self-VERIFY** (every bot/skill): cheap checklist before delivery.
- **Work Verifier** (high-stakes only): independent second pass for Swing Setup, Story, Fusion, Regime, Daily Briefs, and anything Justin flags. Output `VERDICT: PASS | PASS_WITH_NOTES | FAIL`.

## Creation owners

- **總指揮** — enforces this gate when CreateAgent / UpdateAgent / skill write happens in orchestration.
- **Prompt Architect** — refactors must emit ONE_JOB, ANTI_JOBS, VERIFY, IO.
- **dr eggbot** — may not CreateAgent without these fields filled.

## Minimal JD skeleton

```text
ONE JOB: ...
PIPELINE / SKILLS: ...
IO: in ... / out ...
VERIFY: ...
HANDOFF: ... (+ PINNED_INPUTS / DECISIONS_MADE / OPEN_QUESTIONS / NEXT_GATE)
ANTI-JOBS: ...
ESCALATE TO JUSTIN WHEN: ...
```

## Done criteria for this skill

Return PASS only if the new/updated bot or skill text includes all seven gates. Otherwise return FAIL with the missing gates listed. A JD or skill that defines a TC or HANDOFF template must also carry the four fleet-wide handoff fields; list any missing ones in the FAIL.
