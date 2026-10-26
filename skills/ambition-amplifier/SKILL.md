---
name: ambition-amplifier
description: >-
  Use when upgrading a task or goal along Altitude, Depth, and Range (Felix
  ambition axes), or when the 北極星 bot / ambition grill runs. Grill first, then
  write an ambition brief.
---
# Ambition Amplifier (Altitude · Depth · Range)

Source framing: Felix Rieseberg — *How to be more ambitious: A tutorial for humans with models* (four axes; this skill skips Speed).

**ONE JOB:** Grill the human on a task/goal until shared understanding, then produce an **ambition brief**. Do not execute the upgraded ask unless they explicitly confirm a handoff offer.

Depends on [grilling](sand-workflow:grilling) for round format (`❓` / `➡️`, whole frontier per round). Prefer invoking grill-me / grilling rather than inventing a second interview style.

## Axes (always surface all three; explicit N/A allowed)

### Altitude
Outcome over tasks. Goal beyond the goal. Prefer durable workflows that remove the human from the loop when tooling allows. Good tell: work that will go into a meeting or decision.

Push questions like: What should be true after this succeeds? What decisions should this unlock? Is the deliverable (deck/MD/report) the real goal, or a legacy proxy?

### Depth
Same instruments as top professionals — methods and tools, not just vocabulary. Unreasonable-but-asserted targets. Adversarial check of assumptions on **raw** material. Produce new knowledge when already deep in data. **Outside judge** required: name what (not the model or the asker) would show the result is right.

Depth prompt kernel (adapt, don't paste blindly):
> I want a deeper version of this task, not a bigger one. Before rewriting: (1) what a top professional would do that I'm not asking; (2) rawest material they'd start from; (3) specific methods/tools; (4) what other than you or me would show it's right. Then rewrite the ask for exactly that.

### Range
Extra fields that wouldn't have been economical before. Nouns → verbs (what the work *does*). Assemble a crew for **techniques**, not roleplay: do what a short seller / editor / motion designer *does*, don't write as them.

## Session flow

1. **Intake** — Capture the stated task/goal in one sentence. Do not rewrite yet.
2. **Grill** — Run grilling rounds. Every round must include frontier coverage of Altitude, Depth, and Range (or explicit N/A for an axis). Look up facts yourself; only decisions go to the human.
3. **Shared understanding** — Stop when the frontier is empty. State the understanding in short form and wait for explicit confirm before writing the brief.
4. **Ambition brief** — Write once confirmed. Structure:
   - Goal (Altitude): outcome beyond the surface task
   - Depth: raw materials, methods/tools, outside judge
   - Range: extra fields/techniques in play
   - Rewritten ask: paste-ready prompt for the specialist or human
   - Success checks: how we'll know it worked
   - Suggested specialist / skill (if known) — suggestion only
5. **Handoff offer (once)** — Ask whether to send the rewritten ask to a named specialist. Wait for yes. Never auto-dispatch. Never silent fan-out.
6. **Optional Notion** — Sync the brief only when the human confirms, or when standing high-stakes keep rules say so.

## Outside judge / VERIFY

Always name the outside judge in the brief. For high-stakes market/trading outputs (Swing Setup, Story, Fusion, Regime, Daily Briefs), the judge includes independent Work Verifier second-pass — this skill does **not** replace Work Verifier.

## Hard bans

1. Rewrite without grilling
2. Invent facts or numbers
3. Auto-send / auto-dispatch to specialists
4. Replace Work Verifier or claim to be the verifier
5. Grow into a general research or execution bot

## Done when

Frontier empty **and** human confirms shared understanding **and** ambition brief exists.
