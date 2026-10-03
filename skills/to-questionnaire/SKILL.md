---
name: to-questionnaire
description: >-
  Use this when turning a decision the user cannot fully answer into a
  questionnaire for someone else to fill in (/to-questionnaire).
disable-model-invocation: true
---
# To Questionnaire

User-invoked (`/to-questionnaire`). Turn a blocked decision into a **discovery questionnaire** for one other person (async or meeting).

**Grill the send, not the subject.**

1. **Who is it going to?** One exchange: role, expertise, relationship. Done when you know what they know that the user doesn't.
2. **What do you need back?** One exchange: concrete decisions/facts the user can't resolve alone.
3. **Write** `to-questionnaire-<slug>.md` under `/workspace/` (or the user's named dir). Cover every item from step 2.

## Document shape

- Purpose + From/To + how answers will be used
- Short Context for a recipient who wasn't in the user's head
- How to answer (deadline, effort; "I don't know" is useful)
- Themed `##` sections, questions most-important-first, one idea each, answer stub beneath, _why this matters_ only when needed
- Closing catch-all: anything we didn't ask?

Full template: `/home/box/agent-data/workflows/to-questionnaire/UPSTREAM.md`.
Source: mattpocock/skills `skills/productivity/to-questionnaire`.
