---
name: Story Handoff Parse
description: >-
  Use when receiving a handoff for Story: MARKET=HK keeps GEMINI HANDOFF parse;
  MARKET=US (or STORY HANDOFF v5) uses single ENTRY + Invalidate_Below + TARGET
  NONE + SUPPLY ABOVE and rejects ENTRY ZONE / ADJUSTED STOP / PRIMARY TARGET.
---
# Story Handoff Parse

## Package PINNED mode (TC-20261109-story-PKG)
When PINNED_INPUTS include a package `story_handoffs.md` / `L2_Input.csv`:
- Universe = rows with `Story_Needed=True` only (not full Contract).
- Prefer STORY HANDOFF v5 blocks from `story_handoffs.md`.
- HK **package** runs = JSON-only (same v5/JSON path) — do **not** force GEMINI for those.
- Legacy GEMINI remains only for non-package HK chat if ever routed.
- Pass through Tradeable / Tradeable_Why; never upgrade FAIL.

## Contract width / Tradeable

Tolerate **113-col** US Contract (Tradeable era) and prior widths. Do not invent targets from missing cols. MARKET gate unchanged. If `Tradeable` present, pass through; never upgrade FAIL to stalkable.

Parse a Story upstream handoff. Do not redo technical analysis. Do not upgrade VERDICT for a good story.

## MARKET gate (OQ-1 ACK — Justin 2026-11-06)

Infer MARKET from labeled field; if missing: `.HK` → HK; else US.

| MARKET | Contract |
|---|---|
| **HK** | Keep current **GEMINI HANDOFF** parse (below §HK) |
| **US** | **STORY HANDOFF v5** only (below §US). Reject old fields |

---

## §US — STORY HANDOFF v5

Accept header forms like `STORY HANDOFF v5 — TICKER | DATE` or equivalent US v5 handoff.

### Required / accepted fields
- **ENTRY** = **single price** (not a zone)
- **STOP** = `Invalidate_Below` (with Stop_Type_Plan when present)
- **TARGET: NONE** — no primary/secondary targets
- **SUPPLY ABOVE** = `Supply_Level` (+ Supply_Source); soft supply when present
- Setup_Family / Setup_Code · verdict · quality Grade · Room_To_Supply_R · Risk_Pct_Plan / Risk_ADR_Plan · RS · EARNINGS · Speak_Up when present · **MARKET=US**

### Reject (do not silently map)
If the US handoff contains any of:
- `ENTRY ZONE`
- `ADJUSTED STOP`
- `PRIMARY TARGET`

→ **reject parse and report** to Justin/總指揮. Do not convert old fields into v5. Do not invent a single ENTRY from a zone.

### Earnings gate (US)
CLEAR / CAUTION / PASS (≤7d) / UNKNOWN — same spirit as Hermes: PASS → same-week-only narrative; do not upgrade VERDICT.

### Term lock (US)
Entry ≠ Stop · TARGET is NONE · Supply is resistance not a profit target · Tech VERDICT owns the call · never invent targets.

---

## §HK — GEMINI HANDOFF (unchanged)

Parse a **GEMINI HANDOFF** from **港股 Swing Setup** (or Claude Phase 8). HK path remains live.

### Required labeled fields
Header `GEMINI HANDOFF — TICKER | DATE` plus:

VERDICT · SETUP TYPE · STOP TYPE · STOP ANCHOR · SCENARIO ENTRY · ENTRY ZONE · ADJUSTED STOP · PRIMARY TARGET+RR · EARNINGS · KEY SUPPORT · TECHNICAL CONCERN · CLAUDE CONVICTION · RS_SCORE (optional) · **MARKET=HK**

If ENTRY ZONE, ADJUSTED STOP, VERDICT, or EARNINGS missing → ask for complete handoff.

### Earnings gate (HK)
≤14d / CAUTION → pre-earnings catalysts only · PASS≤7d → same-week only · UNKNOWN → search normally + remind user to verify calendar

### Term lock (HK)
RS = Stock%−benchmark (HSI), positive = outperform · Entry ≠ Stop · Tech VERDICT owns the call

---

## Handoff control fields (both markets)

Also parse: **PINNED_INPUTS** · **DECISIONS_MADE** · **OPEN_QUESTIONS** · **NEXT_GATE**

- Missing any → treat as `none` (do not block) and add `"<FIELD> missing in upstream HANDOFF — treated as none"` to OPEN_QUESTIONS.
- **PINNED_INPUTS** → read exactly those absolute paths; never substitute "latest".
- **DECISIONS_MADE** → settled; do not re-open.
- Carry all four forward into the Story output handoff tail for Fusion (HK). US Story auto-route is OFF (S4 outsourced) — if a US parse is requested anyway, still carry the four fields and report.

## VERIFY

- [ ] MARKET inferred or labeled; correct branch (US v5 vs HK GEMINI) used
- [ ] US: rejected ENTRY ZONE / ADJUSTED STOP / PRIMARY TARGET when present (no silent map)
- [ ] US: ENTRY is single price; TARGET NONE; SUPPLY ABOVE used
- [ ] HK: required GEMINI fields present or asked
- [ ] No VERDICT upgrade from story quality
- [ ] PINNED_INPUTS / DECISIONS_MADE / OPEN_QUESTIONS / NEXT_GATE carried
- [ ] Banned tokens absent in any **new US output artifact**: Hermes-deleted underscore fields (risk-reward ratio*, target-N*, setup-type*, adjusted-stop*)
