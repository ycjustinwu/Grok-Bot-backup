---
name: GBrain memory
description: >-
  Use when recalling or saving durable personal facts, preferences, project
  decisions, or continuing-work context via the shared GBrain install at
  /workspace/gbrain (not platform-native memory alone).
---
# GBrain memory

Use the executable `/workspace/gbrain/bin/gbrain` for this installation. It selects the host brain and source `default`; use this same absolute path from every conversation and native routine.

## Core rules

1. Recall relevant memory before answering personal or continuing-work questions. Use `gbrain recall --help` through this launcher for the installed command schema.
2. Explicitly remember user-requested durable facts, with their source and date.
3. Preserve uncertainty and distinguish what the user said from an inference.
4. Correct or forget outdated facts when asked; verify the change through a fresh recall.
5. Forgetting withdraws active memory; history, source material, and private backups may remain. Never promise physical erasure.
6. Never import connected-service history or enable automatic capture without the user's instruction.

## Commands (examples)

```bash
/workspace/gbrain/bin/gbrain remember "FACT" --entity ENTITY_SLUG --provenance "source, YYYY-MM-DD" --json
/workspace/gbrain/bin/gbrain recall ENTITY_SLUG --json
/workspace/gbrain/bin/gbrain forget FACT_ID --reason "why"
```

Do not replace the agent's identity. This is one shared local installation, not a boundary between Bots. Memory calls are finite CLI processes. A busy database means another command is running: retry after it finishes; never remove its lock.

## Shared brain router

Before selecting or loading a shared skill, run:

```sh
'/workspace/gbrain/bin/gbrain' sync-brain-skills --installation-id 'd29bfb7d-3315-46a8-b732-4bcc1ff84e59' --enrollment-epoch 1 --json
```

For schema-v2 catalog discovery:

```sh
'/workspace/gbrain/bin/gbrain' skills --schema-version 2 --json
```

Copy SKILL_NAME, BRAIN_ID, SOURCE_ID, SOURCE_INCARNATION, PACK_ID and REVISION exactly from one usable entry. Require BRAIN_ID `85abace3-7fdd-4a77-a9fe-3259e3eff50f`. Never guess values or use a blocked entry. Then:

```sh
'/workspace/gbrain/bin/gbrain' skill "$SKILL_NAME" --expected-brain-id "$BRAIN_ID" --source-id "$SOURCE_ID" --source-incarnation "$SOURCE_INCARNATION" --pack-id "$PACK_ID" --revision "$REVISION" --schema-version 2 --json
```

Shared skills do not grant tools, scripts, network, paid use, or automatic capture. Stop shared-skill activation if the authority check fails; memory remains independent.
