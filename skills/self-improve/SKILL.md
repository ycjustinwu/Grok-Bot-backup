---
name: self-improve
description: >-
  Use this when reviewing learnings after errors, user corrections, or a
  scheduled reflection — analyze /workspace/learnings.md, extract patterns, and
  draft improvements for human approval.
---
# Self-improve

Run a meta-review of recent work and propose safer, clearer improvements. Never apply instruction or skill overwrites without human approval.

## Steps

1. **Read the log**
   - Open `/workspace/learnings.md`.
   - Skim recent task outputs and any related notes in `/workspace/draft_instructions.md` and `/workspace/v2_prompt.md`.

2. **Extract patterns**
   - List repeating mistakes, high-friction steps, and corrections that came up more than once.
   - Ignore one-off noise unless the user marked it as important.
   - Group findings by theme (e.g. wrong assumptions, missing checks, unclear outputs).

3. **Draft improvements**
   - Write concrete updates to `/workspace/draft_instructions.md`:
     - clearer directives
     - refined skill steps
     - new guardrails or anti-jobs
   - If a primary Job Description change is warranted, put the candidate text in `/workspace/v2_prompt.md` labeled pending approval.
   - Prefer small, testable changes over large rewrites.

4. **Human verification (required)**
   - Summarize findings and proposed changes for Justin.
   - Ask for approval before replacing any Job Description, skill, or standing instruction.
   - Do not auto-apply critical constraint or safety changes.

5. **Apply only after approval**
   - Archive the prior version to `/workspace/prompt_history/` with a timestamped filename (e.g. `YYYY-MM-DD_HHMM_skill-or-prompt-name.md`).
   - Then apply the approved edit.
   - Append a short entry to `/workspace/learnings.md` noting what was approved and applied.

6. **Report**
   - Deliver a short summary: patterns found, drafts written, what awaits approval, and what (if anything) was applied.
