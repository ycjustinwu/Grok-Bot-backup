---
name: Notion DB Lookup
description: >-
  Use when any bot needs facts from Justin's Notion databases without burning
  tokens: SQL properties first, box Final mirror preferred, expandable category
  catalog as more DBs appear.
---
# Notion DB Lookup (fleet, token-cheap)

## Goal
Treat Notion databases as an **index**, not a corpus dump. Answer with a narrow SQL or view query first. Read a page body only when properties are not enough. Prefer the box Final mirror when it exists.

## Catalog (categories grow here)
Before any Notion read, open `/workspace/notion-briefs-import/library-catalog.json`.

Each `libraries.<id>` has `collection`, `preferred_columns`, and optional `box_mirror_glob`, `date_property`, `title_property`.

**New DB later:** append one object under `libraries`. Do not rewrite this skill for each category. Optional: note in memory that the catalog grew.

Write/upsert Finals into Notion stays in skill Notion Final Sync. This skill is **read and lookup only**.

## Escalation (cheap to expensive)
1. **Box mirror** — if Source Path or box_mirror_glob resolves on disk, read that file. Stop if it answers the ask.
2. **Catalog plus SQL** — use notion-query-data-sources (sql):
   - Table = exact `collection://…` from the catalog.
   - SELECT only needed columns from preferred_columns (never SELECT * except one-time schema discovery via fetch).
   - Filter by date / title / tags. Latest default: order by date descending, LIMIT 1.
   - Cap: LIMIT 1–5 for latest; max LIMIT 20 for a short scan.
3. **Saved view** — if a Notion view exists for the ask (e.g. Latest Regime), use view mode with that view_url.
4. **Fetch page body** — only when properties lack the fact. One page at a time. Do not paste full bodies into a coordinator chat; summarize in at most five lines or keep detail in the specialist thread.
5. **Keyword search** — last resort for unknown category or orphan pages. Short distinctive keywords, then SQL on the resolved collection.

## Anti-patterns
- Opening many page bodies just in case
- Re-searching Notion for standing rules (use memory or GBrain)
- Writing or syncing pages in this skill
- Dumping large SQL tables into user chat — return the answer, url, and Source Path only

## Add a category
1. Fetch the database to get `collection://`.
2. Append to library-catalog.json with preferred_columns that hold facts bots need (dates, scores, tags, urls).
3. Set box_mirror_glob when Finals live on the box.
4. No skill rewrite required.

## VERIFY
- Used a catalog id (not a guessed collection string).
- Query respected the row limit; columns were a subset of need.
- If a body was fetched, state why properties were insufficient.
- Coordinator replies stay status plus link only.
