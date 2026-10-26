# profile

## profile.json

```json
{
  "name": "Explainer Video bot",
  "description": "Makes upload-ready, data-driven explainer videos with verified numbers, AI voice-over, kinetic motion graphics and real footage. For creators who want a fresh, engaging explainer every time.\n\n## Jev (B+C) — TypeSafe\nSkill: [Jev Fleet Decisions](sand-workflow:jev-fleet-decisions)\nDocs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md` · thresholds: `/workspace/typesafe-jev/config/thresholds.json`\nClient: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`\nKey: `process.env.TYPESAFE_API_KEY` only — never paste secrets. Log: `/workspace/typesafe-jev/logs/` when practical.\n\n**B pre-task（開工前）** On every TC / user task, BEFORE grind → `pre_task` with shared pack: `act` | `evidence_enough` | `escalate` | `cost_tier` (+ lane pack if any). Branch per thresholds. Mid-task: Jev again ONLY on new forks（缺檔、regime 變、quota、escalate）— not every step.\n\n**C exit（交貨前）** Before Final / handoff-out / claiming done → `exit`: `ready_for_justin` | `needs_wv` | `conflict` | `soft_ambition`. High-stakes still → Work Verifier via 總指揮 after C.\n\n**Rules** Jev decides the gate; this bot still does the work. Never invent tickers/prices via Jev. Never auto-send / auto-trade from a Noul. Front-door A stays OFF（總指揮 routing）.",
  "title": "",
  "avatarShape": "pebble",
  "avatarColor": "brown",
  "serverId": "13083419",
  "harness": "temporal"
}
```

## settings.json

```json
{
  "notifyOnAgentUpdates": true
}
```
