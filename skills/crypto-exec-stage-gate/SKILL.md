---
name: crypto-exec-stage-gate
description: Use after validate — Stage0 paper/testnet auto; Stage1 Ask-first with timeout=cancel; Stage2 only on new Justin ticket. No live MCP orders until connected.
---
# crypto-exec-stage-gate
ONE JOB: Enforce stage machine; never skip Ask-first timeout=cancel on Stage1.
Stage0: paper/testnet log only until ≥5 trade days zero security violations (sig-fail rejects OK).
Stage1: preview Justin; timeout=cancel; risk% must be Justin-locked; kill/day-loss drill once.
Stage2: new ticket only.
VERIFY: no live order if MCP not connected; timeout never fills; kill drill timestamp if claimed.
ANTI: no Stage2 auto; no master key; isolate equity desk.
