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
HANDOFF: ...
ANTI-JOBS: ...
ESCALATE TO JUSTIN WHEN: ...
```

## Done criteria for this skill

Return PASS only if the new/updated bot or skill text includes all seven gates. Otherwise return FAIL with the missing gates listed.
