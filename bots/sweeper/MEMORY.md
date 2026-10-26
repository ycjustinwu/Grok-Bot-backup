# Sweeper / 清道夫 — durable memory backup
- agent uuid: 8dbca7e8-e0d0-4447-821a-f9a3ad9d7e06
- serverId: 2725798
- snapshot_at: 2026-10-26 ~20:46 HKT (Asia/Hong_Kong)
- written_for: 记忆管家 fleet disaster-recovery backup
- prior snapshots: /workspace/2725798-memory-backup.md (2026-09-14, 52 lines); this path last written 2026-10-03 (44 lines)

## Identity
- Name / title: Sweeper / 清道夫
- ONE JOB: See Grok Bot usage clearly, sweep idle wakes, make bots last longer. / 帮你看清 Grok Bot 用量、清掉空转、把 Bot 用久一点。
- ANTI-JOBS: Do not invent Usage $ or exact token counts (relative wake ranks only). Do not edit another agent's routines or memories without explicit Justin yes in chat. Do not create extra bots/routines "to save usage" (Usage gate). Do not re-ask unanswered delete-widget.
- Partners: 總指揮 (liaison / TC tickets); 记忆管家 (memory backups); Self Improver (owns weekly self-improve after move); fleet bots only via owner messaging for routine changes.
- User: Justin Wu (Asia/Hong_Kong)
- Profile path: /home/box/agent-data/agents/8dbca7e8-e0d0-4447-821a-f9a3ad9d7e06/profile.json (harness temporal, avatarShape pebble, avatarColor blue)
- Settings: notifyOnAgentUpdates true
- Own routines: none (no automations folder; UpdateRoutine list empty)
- Durable memory (profile, 2026-10-03): Usage gate + no invented Usage numbers + no cross-agent edits without yes

## Historical decisions / locked rules
- 2026-09-13: Template setup. Intended standing rules (no invented Usage $ / tokens; no cross-agent routine/memory edits without yes). Early writes failed; later saved 2026-10-03 into profile.
- 2026-09-14: Justin "Start sweeping". Fleet healthcheck then: 21 bots / 8 routines / 1 enabled; no denser-than-hourly crons. Justin approved three: (1) move weekly self-improve off 總指揮 onto Self Improver; (2) help decide deletes; (3) add stay-quiet-on-empty to noisy paused routines. Declined standing Sweeper healthcheck.
- Execution note: Sweeper cannot update_state other bots' routines — owners applied patches after messaging.
- 2026-09-14 outcomes on disk: Self Improver owns enabled Weekly self-improve `0 18 * * 5` + stay-quiet; 總指揮 copy paused (not deleted); Video Transcriber Recursive Learning stay-quiet + paused; 港股收市後簡報 stay-quiet + paused.
- Delete pick-list widget sent 2026-09-14; Justin unanswered. Do not re-ask.
- 2026-09-20 Justin locked Usage gate via 總指揮 (canon /workspace/fleet-policies/USAGE_GATE.md): reuse fresh artifact; stop after same approach fails twice; chat-only when no tools needed; connector/API over browser; do not create more bots or routines to save usage.
- 2026-10-03: Wrote prior version of this backup file for 记忆管家; profile memory write succeeded.
- 2026-10-21 TC-20261021-04 (總指揮): X Monitor Weekday ~07:19 HKT showed Activity task failed (wake fired; no executor handoff body). Sweeper reply: cannot see plan Usage meters; only visible morning Activity fail was that X Monitor wake (before bot tools); public X OK by ~07:22 (oneshot artifacts under /workspace/x-monitor/weekday-oneshot-2026-10-21-*); assessed infra Activity failure, not idle-wake waste or provable pool exhaustion. No changes made.

## Live snapshot (verified on disk 2026-10-26)
Fleet disk sample (agents with automations folders: 6; automation.json files found in sample: 9). Sweeper folder: profile, settings, store.db (+shm/wal), assets, attachments — no automations.

| Owner | Routine id / name | enabled | schedule | stay-quiet | notes |
|---|---|---|---|---|---|
| Self Improver | weekly-self-improve-reflection / Weekly self-improve reflection | true | 0 18 * * 5 | yes | lastRunAt null on disk |
| 總指揮 | weekly-self-improve-reflection | false | 0 18 * * 5 | yes | paused duplicate; optional delete not approved |
| 總指揮 | kick-hk-after-close-brief / Kick HK after-close brief | false | 5 18 * * 1-5 | yes | paused; delete-widget candidate |
| 港股收市簡報 | automation-1788788112710 / 港股收市後簡報 | false | 0 18 * * 1-5 | yes | keep unless Justin says delete |
| Video Transcriber | recursive-learning / Recursive Learning | false | 0 8 * * 6 | yes | delete-widget candidate |
| X Brief | daily-x-brief | false | 0 9 * * 1-5 | no | never-ran; delete-widget candidate |
| X Brief | weekly-x-recap | false | 0 9 * * 5 | no | never-ran; delete-widget candidate |
| dr eggbot | routine-healthcheck | false | 49 8 * * 1 | yes | never-ran; delete-widget candidate |
| dr eggbot | transcript-healthcheck | false | 44 8 * * 1-5 | yes | never-ran; delete-widget candidate |
| X Monitor | (server-kept; no automations folder on disk) | n/a disk | Weekday known to fire ~morning HKT | n/a | 2026-10-21 Activity task failed ~07:19; oneshot recovery artifacts present |
| Sweeper | — | — | — | — | no routines |

Paths of note:
- Usage gate canon: /workspace/fleet-policies/USAGE_GATE.md
- This backup: /workspace/8dbca7e8-e0d0-4447-821a-f9a3ad9d7e06-memory-backup.md
- Prior serverId-named backup: /workspace/2725798-memory-backup.md
- X Monitor recovery: /workspace/x-monitor/weekday-oneshot-2026-10-21-{body,acc,softshort}.*

Open work with Justin:
- Delete-widget answer still open (Kick HK, Recursive Learning, X Brief pair, dr eggbot healthchecks; keep 港股 brief; or hold). Do not re-ask.
- Optional if asked: delete paused 總指揮 weekly self-improve copy; Sweeper weekly healthcheck (declined + Usage gate discourages).

## Secrets
- None held by Sweeper.
- [REDACTED:CURSOR_API_KEY]
- [REDACTED:connector-tokens]

## Pending confirms
- Justin: delete-widget answer still open since 2026-09-14. Do not re-ask; do not act.
- Optional delete of paused 總指揮 weekly-self-improve-reflection: not approved.
- Optional Sweeper standing healthcheck routine: declined; Usage gate says do not add routines to save usage.
- No pending confirms from 记忆管家 on this write (snapshot only).
