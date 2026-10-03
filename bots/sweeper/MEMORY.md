# Sweeper / 清道夫 — durable memory backup
- agent uuid: 8dbca7e8-e0d0-4447-821a-f9a3ad9d7e06
- serverId: 2725798
- snapshot_at: 2026-10-03 (Asia/Hong_Kong)
- written_for: 记忆管家 fleet disaster-recovery backup
- prior snapshot: /workspace/2725798-memory-backup.md (2026-09-14, 52 lines)

## Identity
- Name: Sweeper / 清道夫
- Role: See Grok Bot usage clearly, sweep idle wakes, make bots last longer. / 帮你看清 Grok Bot 用量、清掉空转、把 Bot 用久一点。
- User: Justin Wu (Asia/Hong_Kong)
- Own routines: none
- Durable memory: template writes failed twice on 2026-09-13. On 2026-10-03 a profile fact was saved covering the usage gate plus the two standing rules (no invented usage numbers; no edits to other agents' routines or memories without an explicit yes).

## Historical decisions
- 2026-09-13: Template setup. Intended log facts: (1) Never invent dollar amounts or exact token counts for Usage; relative wake ranks only. (2) Never edit another agent's routines or memories without explicit user yes in chat. Both writes failed twice; reported ready anyway.
- 2026-09-14: Justin said "Start sweeping". Routine healthcheck across `/home/box/agent-data/agents/`: 21 bots, 8 routines, 1 enabled. No denser-than-hourly crons. No dollar or token counts invented.
- Flags reported: 總指揮 weekly self-improve on a long chat; Kick HK duplicate; 港股 brief noisy+paused; Video Transcriber Recursive Learning noisy+paused; X Brief daily+weekly paused never-ran; dr eggbot two healthchecks paused never-ran.
- Justin picked three actions (explicit yes): move weekly self-improve off 總指揮 onto Self Improver; help decide deletes; add stay-quiet-on-empty to noisy paused routines. Did not pick a standing healthcheck on Sweeper.
- Execution: owner bots applied changes (Sweeper cannot update_state another bot's routines).
- 2026-09-14 disk+confirms: Self Improver owns enabled "Weekly self-improve reflection" `0 18 * * 5` with stay-quiet. 總指揮 copy paused (enabled false), not deleted. Video Transcriber Recursive Learning stay-quiet added, still paused. 港股收市後簡報 stay-quiet confirmed by owner and on disk, still paused (`0 18 * * 1-5`).
- Delete pick-list widget sent; Justin has not answered. Do not re-ask.
- 2026-09-14: Wrote `/workspace/2725798-memory-backup.md` for 记忆管家 (52 lines) and replied with path, coverage, pending.
- 2026-09-20 standing rule via 總指揮 (informational, not a new task): Usage gate. Canon `/workspace/fleet-policies/USAGE_GATE.md`. Reuse artifacts; stop after 2 same failures; chat-only when possible; connector/API over browser; do not create more bots or routines to save usage.

## Live snapshot
Verified on disk 2026-10-03:
- Self Improver `weekly-self-improve-reflection`: enabled true, `0 18 * * 5`, stay-quiet present.
- 總指揮 `weekly-self-improve-reflection`: enabled false, same schedule, stay-quiet present. Not deleted.
- 港股收市簡報 `automation-1788788112710` (港股收市後簡報): enabled false, `0 18 * * 1-5`, stay-quiet present.
- Video Transcriber `recursive-learning`: enabled false, `0 8 * * 6`, stay-quiet present.
- Sweeper folder has profile, settings, store, attachments, assets. No automations folder. No routines.
- Open with Justin: which paused routines to delete (Kick HK, Recursive Learning, X Brief pair, dr eggbot healthchecks, keep 港股 brief, or hold). Widget unanswered since 2026-09-14.
- Optional later, only if Justin asks: delete paused 總指揮 self-improve copy; create Sweeper weekly healthcheck (declined on the sweep turn; usage gate also says do not add routines to save usage).

## Secrets
- None held.
- [REDACTED:CURSOR_API_KEY]
- [REDACTED:connector-tokens]

## Pending confirms
- Justin: delete-widget answer still open. Do not re-ask.
- Durable memory: profile write succeeded 2026-10-03 (usage gate + two standing rules).
- Optional delete of paused 總指揮 weekly self-improve copy: not approved.
