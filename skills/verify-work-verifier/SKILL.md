---
name: verify-work-verifier
description: >-
  Fleet-QA control skill for Work Verifier — feature map of high-stakes Grok Bot
  deliverable types; drive proofs via work-verify
  Launch→Doctor→Drive→Evidence→Cleanup.
---
# Verify Work Verifier (fleet QA control)

Thin control index for **Work Verifier** fleet QA. Surfaces = producer **deliverable types** on disk (not a web UI).

## Stack choice (locked for TC-20260911-01)

| Piece | Role |
|-------|------|
| **`work-verify`** | Full harness: Launch → Doctor → Drive → Evidence → Cleanup + VERDICT |
| **`verify-work-verifier`** | This file + `features/` map only — which surface to Drive and gotchas |
| **No second checklist** | Do not duplicate Doctor/Evidence here |

Refine existing bot **Work Verifier** (`037de516-dbc1-4565-a127-5dbb0f691729`); do not CreateAgent a duplicate.

## When to use

總指揮 (or Justin) assigns high-stakes QA: 港股收市簡報 · US Market Daily Brief · Market Awareness Orchestrator · 港股/美股 Swing Setup · 投資敘事分析師 + Fusion Formatter · any flagged published brief.

Skip routine scanner scoreboards unless asked.

## How to run one proof

1. **Launch** — intake via `work-verify` (producer, claim, paths, done criteria).
2. **Doctor** — `work-verify` path/schema GO|NO-GO.
3. **Drive** — open the matching file under `features/`; execute its harness bullets.
4. **Evidence** — `work-verify` writes `/workspace/work-verifier/output/verify-YYYYMMDD-HHMM.md` (HKT) + `LATEST.txt`.
5. **Cleanup** — scratch only under `/workspace/work-verifier/scratch/`.

## Feature map

See [features/README.md](features/README.md).

## Maintenance

When a producer IO contract changes, update the matching `features/*.md` first, then spot-check Doctor schema lines in `work-verify`. Prefer `/maintain-verification-skill` cadence only if 總指揮 asks.
