# Sweeper / 清道夫 — durable memory backup
- agent serverId: 2725798
- agent uuid: 8dbca7e8-e0d0-4447-821a-f9a3ad9d7e06
- snapshot_at: 2026-09-14 (Asia/Hong_Kong context)
- written_for: 记忆管家 disaster-recovery backup

## Identity
- Name: Sweeper / 清道夫
- Title: Sweeper / 清道夫 (profile title field empty)
- Role: See Grok Bot usage clearly, sweep idle wakes, make bots last longer. / 帮你看清 Grok Bot 用量、清掉空转、把 Bot 用久一点。
- User: Justin Wu
- Harness: temporal (from profile.json)
- Standing rules (template / intended durable — durable write failed at first setup; treat as required operating rules):
  1. Never invent dollar amounts or exact token counts for Usage; relative wake ranks only.
  2. Never edit another agent's routines or memories without explicit user yes in chat.

## Historical decisions
- 2026-09-13: Bot template setup requested; introduce + persist two memory facts (tier log). Both `update_state` memory writes failed with "brain docs snapshot was cut short before completing"; setup reported ready with re-apply pending.
- 2026-09-14: User said "Start sweeping". Ran Routine healthcheck skill across fleet (`/home/box/agent-data/agents/`).
- Fleet scan result (no $ / token counts): 21 agents, 8 routines, 1 enabled. Flags delivered to Justin; no denser-than-hourly crons.
- User multi-selected next actions (explicit yes):
  1. Move weekly self-improve off 總指揮 onto Self Improver
  2. Help decide which paused/dead routines to delete
  3. Add stay-quiet-on-empty to noisy paused routines
  (Did not select standing weekly checkup on Sweeper.)
- Execution path: cannot `update_state` other bots' routines; messaged owner bots via SendToAgent to apply changes.
- 總指揮 confirmed pause of "Weekly self-improve reflection" (folder weekly-self-improve-reflection). Kick HK left as-is.
- Observed on disk after handoffs:
  - Self Improver owns enabled "Weekly self-improve reflection" `0 18 * * 5` with quiet-on-empty clause.
  - 總指揮 copy enabled=false.
  - Video Transcriber "Recursive Learning" prompt now includes stay-quiet / no-filler clause (still paused).
  - 港股收市簡報 "港股收市後簡報" still missing explicit stay-quiet (pending owner confirm).
- Delete pick-list widget sent to Justin; awaiting selection (options included Kick HK, Recursive Learning, X Brief pair, dr eggbot healthchecks, keep 港股 brief, or hold).

## Live snapshot
- Own routines: none (Current routines empty).
- Own durable memory store: empty / unwritable at last attempt (RecallMemory returned no facts).
- Active sweep work: wait for (a) 港股 quiet-clause confirm, (b) Justin delete picks, (c) optional later delete of paused 總指揮 self-improve copy once Justin wants cleanup, (d) retry persisting the two standing rules when memory writes work.
- Skills relied on: Routine healthcheck (`routine-healthcheck`), Routines skill before routine changes.
- Teammates messaged this session: Self Improver (2410911), 總指揮 (2410895), Video Transcriber (174592), 港股收市簡報 (2410898).

## Secrets
- None held.
- Placeholders only if needed later: [REDACTED:CURSOR_API_KEY], [REDACTED:connector-tokens]
- Do not store real tokens in this file.

## Pending confirms
- 港股收市簡報: stay-quiet append on "港股收市後簡報" — not yet visible in automation.json
- Justin: delete-widget answer (which paused routines to delete)
- Memory subsystem: re-write two standing rules to durable memory when writes succeed
- Optional: delete paused 總指揮 "Weekly self-improve reflection" after move fully accepted
- Optional: create Sweeper standing `routine-healthcheck` (user declined this run)
