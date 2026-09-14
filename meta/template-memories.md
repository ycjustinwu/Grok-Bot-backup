# Template memories (pending durable write)

Platform `update_state` memory writes failed with: brain docs snapshot was cut short.
Keep here until durable agent memory accepts them.

1. Standard disaster-recovery archive layout under `/workspace/memory-manager`: README, RESTORE, CHANGELOG, registry, shared-user-memory/MEMORY.md, bots/<slug>/{agent-spec,profile,MEMORY,archive}, meta/memory-manager-self.md.

2. Maintain a registry of bots the user opted into backup; only back up those marked included. Shared/global user memory is backed up at shared-user-memory/MEMORY.md, separate from per-bot memories under bots/.

3. Weekly full backups plus gap-filling checks for bot memories are scheduled every Sunday at 3:00 AM (user's timezone), with a report afterward; manual runs via saying 「存档」.

4. Hard gate: never claim disaster recovery is complete until a private Git remote is configured. Tokens/secrets/cookies must never enter Git; backups use placeholders only. Modes: cold-start, restore-from-repo, or join-existing-fleet.
