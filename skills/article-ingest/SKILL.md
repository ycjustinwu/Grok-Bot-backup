---
name: article-ingest
description: >-
  Use when 文章分析 receives a URL or pasted article: fetch/normalize into a
  working copy under /workspace/article-analysis/input/ before the report skill.
---
# Article Ingest

## Steps
1. If Justin pasted full text → save as `/workspace/article-analysis/input/{slug}-{stamp}-raw.md` (stamp = Asia/Hong_Kong `YYYYMMDD-HHMM`).
2. If URL only → fetch public web (prefer connector/Tavily/Firecrawl over browser). Save markdown body + note URL. Paywall/empty → stop and ask Justin.
3. Capture appendix fields when present: URL, 作者, 發布時間, 發布平台. Missing → write `未知` — never invent.
4. `slug` = short ASCII from title or host+date; no spaces.

## ANTI
- No login/paywall bypass.
- Do not start the 9-section report here.

## VERIFY
- [ ] Working copy path exists and is non-empty
- [ ] URL recorded or explicitly `無 URL（貼文）`
- [ ] No fabricated author/date/platform
