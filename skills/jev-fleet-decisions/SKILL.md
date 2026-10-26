---
name: Jev Fleet Decisions
description: >-
  Use when a specialist starts a TC handoff or hits a decision fork, or before
  Final/handoff: call TypeSafe Jev for Choice/Score/Noul gates (Layers B and C).
  Front-door A is disabled.
---
# Jev Fleet Decisions (B + C)

Front-door A is **off** (Justin: 總指揮 routing is enough).

## Before work (Layer B)
1. Read `/workspace/typesafe-jev/config/thresholds.json`.
2. Build small state JSON (message/handoff summary ≤2k, paths, flags — no Final/CSV bodies).
3. Run pre-task questions via `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py pre_task --state '...'` (or SDK equivalent).
4. Branch on `act` + confidence / `escalate` / `cost_tier` per thresholds. Mid-task: call again only when a new fork needs a decide.

## Exit (Layer C)
Same client `exit` mode before Justin Final / WV route.

## Secrets
`TYPESAFE_API_KEY` (or OpenRouter) via secure card → env. Never paste in chat.

## Docs
`/workspace/typesafe-jev/fleet-decision-layer-v1.md`
