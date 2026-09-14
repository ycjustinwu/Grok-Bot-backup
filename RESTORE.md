# Restore

1. Clone this private repo onto the shared cloud computer under `/workspace/memory-manager`.
2. For each bot in `registry.md` with 纳入=是, use `bots/<slug>/agent-spec.md` + `profile.md` to recreate via CreateAgent (or UpdateAgent if already present).
3. Hand each bot its `MEMORY.md` content to re-ingest (never paste secrets; placeholders stay placeholders).
4. Restore shared facts from `shared-user-memory/MEMORY.md` into shared user-memory.
5. Reconfigure weekly routine (Sundays 03:00 Asia/Hong_Kong) and Slack report channel.
6. Run one manual 「存档」 and verify before claiming restore complete.
