# Soft Final PLAN — TC-20261109-story-PKG

**Status:** Soft Final = Final · **WV skip** · **PLAN ONLY — do NOT apply**  
**When:** 2026-11-09 Asia/Hong_Kong · Prompt Architect  
**ready_for_justin:** YES (OQs below block apply)  
**Bot:** 投資敘事分析師 `3f297e81-4667-4dae-b517-b4f7ddee3537`  
**Sibling:** Swing Package Ops `9c97ff04-9fd8-44af-8613-9b1f96e64d07` · Fusion `c45141fc-c050-49e2-9635-dca556a0cc1f`  
**Parent locks:** Hermes US L1→S4→L2 primary · Grok US Story auto-route OFF (v5.5.2) · Package Ops LIVE on-demand · Tradeable gate LIVE · Soft Final APPLY swing md5 `2b73a18a…`  
**Evidence:** Ops US Nov 9 `run_jfsrev_20261109` — `Story_Needed` = EL,BAX = Trigger PASS; `story_handoffs.md` present; **no** `<T>_story.json` / `verdicts_US.jsonl` (Ops ANTI: do not wake Story).

---

## ONE_JOB (proposed, apply later)

When Package Ops (or Hermes-down standby) pins a run that needs S4, produce package-schema `<TICKER>_story.json` + `_search_log.json` from PINNED `L2_Input` / `story_handoffs.md` — never invent prices, never upgrade Tradeable FAIL / WATCH / AVOID.

## Gap (why this TC)

| Path today | S4 owner | Verdicts |
|---|---|---|
| Hermes healthy daily US | Hermes outsource (SuperGrok/DeepSeek) | Hermes S5 |
| Package Ops on-demand / Justin full-list | **Nobody** (Ops ANTI wakes Story) | Missing → SB/sim cannot ground on verdicts |
| HK legacy GEMINI | Grok Story ← 港股 Setup (RETIRED 2026-11-09) | Fusion HK still live but Setup dead |

Justin ask: wire Story bot to Swing Package workflow.

---

## 1. Which PINNED files Story reads

### Required (US package pack)
| File | Role |
|---|---|
| `story_handoffs.md` | Primary parse — STORY HANDOFF v5 blocks (same as sample / Nov 9) |
| `L2_Input.csv` | Universe filter: `Story_Needed=True`; pass-through `Tradeable` / `Tradeable_Why` / baseline prices |
| `Contract_US.csv` | Price/verdict ground truth only (no invent); 113-col Tradeable* |
| `index.md` (optional) | Session context / as_of |

### Output (write into **same run folder**, then sync)
| File | Role |
|---|---|
| `stories/<TICKER>_story.json` | Schema = `docs/05_HANDOFF_S4_S5.md` |
| `stories/<TICKER>_search_log.json` | queries + urls + retrieved |
| *(not Story alone)* `verdicts_*.jsonl` | Produced by `story_search_sync.py` after merge |

### Also pin on HANDOFF out
`PINNED_INPUTS` = absolute run path + Drive dated folder copies of the four reads above.  
`DECISIONS_MADE` / `OPEN_QUESTIONS` / `NEXT_GATE` fleet fields mandatory.

### Do **not** treat as Story inputs
- Raw `*_SwingAnalysis.csv` alone  
- `Trigger_US.csv` as sole universe (see §2)  
- Hermes `S4_handoff/` folder on healthy Hermes days (different owner)

---

## 2. Trigger_PASS vs Tradeable vs Story_Needed

| Gate | Meaning | Story rule (recommended) |
|---|---|---|
| **Tradeable** | PASS = risk/room caps OK; FAIL → program forces WATCH + `Tradeable_Why` | Never upgrade FAIL/WATCH/AVOID. Copy Why into narrative risk/traps if present. |
| **Trigger_US / Trigger_PASS** | PASS-only actionable tickets (`generate_trigger`) | **Subset** of Tradeable PASS that is hangable. SB/sim consume this. |
| **Story_Needed** | `l2_prep` flag on `L2_Input` | **Default Story universe** = `Story_Needed=True` rows only. |

**Observed Nov 9:** Story_Needed {EL, BAX} == Trigger PASS == Tradeable PASS BUY. Sample run_v56: Story_Needed only RVTY (BUY+PASS).

**Recommended default:** Story runs **Story_Needed only** (not full Contract, not all Tradeable PASS). Trigger_PASS is usually equal today but is the **sim/SB** gate, not the Story selector — engine already chose Story_Needed.

**OQ-1 (blocking):** Confirm universe = `Story_Needed` only · or force `Trigger_PASS` only · or all Tradeable PASS with Baseline BUY/STALK.

---

## 3. When to wake Story

| Event | Wake Story? |
|---|---|
| **A. Package Ops scan DONE** (Justin full-list override **or** Hermes-down) + `story_handoffs.md` exists + ≥1 `Story_Needed` + no stories yet | **YES** — 總指揮 routes TC with PINNED run path |
| **B. Hermes healthy daily US** (Hermes L1→S4→L2) | **NO** — keep v5.5.2 US auto-route OFF; Hermes S4 owns |
| **C. Justin / 總指揮 explicit Story TC** with PINNED_INPUTS | **YES** |
| **D. Ops install/verify only / empty Trigger / no Story_Needed** | **NO** (idle) |
| **E. SB / 模擬倉 wake** | **NO** — they consume Drive after verdicts exist |

**Ops profile change (apply later):** today’s ANTI「唔喚醒 Story」must flip for event A → announce + `NEXT_GATE: Story` (總指揮 still routes; Ops does not UpdateAgent Story).

**OQ-2 (blocking):** On Hermes-healthy days, keep Grok Story **permanently OFF** for US even if a package pack appears, or allow Justin opt-in package S4?

---

## 4. Hermes S4 vs Grok Story — priority

```
US daily (Hermes up):     Hermes S4 outsource  >>>  Grok Story OFF
US package on-demand / Hermes-down:   Grok Story (this bot)  >>>  fill docs/05 JSON
Never: dual S4 writers for same ticker+as_of
```

| Owner | Writes | Downstream |
|---|---|---|
| Hermes S4 | Hermes `S4_handoff` → fetch → L2 check/render | Hermes Drive pack → SB/sim |
| Grok Story (package mode) | `stories/*_story.json` + `_search_log.json` in `/opt/swing/.../run_*` | **Ops** (or Story shell) runs `story_search_sync.py` → `run_l2.sh check|render` → Drive PINNED refresh including `verdicts_US.jsonl` |

Grok live skills today (theme/web/validate/report) produce **chat MD / Fusion handoff**, not package JSON. Apply must add a **package-S4 skill** (or port `US/01_RULES/story_search` v3.2 output template) so artifacts pass V12/V13.

**OQ-3 (blocking):** After JSON land, who runs sync+check+render+Drive re-upload — **Package Ops** (recommended) · Story bot Shell · 總指揮 only?

---

## 5. US vs HK

| Market | Today | Proposed package mode |
|---|---|---|
| **US** | Hermes S4 primary; Grok Story OFF | Package wake only (§3A); output English per `docs/05` rule 5; no Fusion US |
| **HK** | GEMINI from 港股 Setup → Story → Fusion (Setup **RETIRED**) | When Ops runs HK package: same JSON S4 (`handoff/S4_INSTRUCTION_HK.md` + `docs/05`); TC 繁中. Legacy GEMINI/Fusion only if Justin keeps a non-package HK path. |

**OQ-4 (blocking):** HK package runs — **JSON-only** (drop GEMINI/Fusion for those runs) · or keep Fusion chat parallel?

Fusion US stays OFF. Fusion HK stays only if OQ-4 keeps GEMINI.

---

## 6. Scope matrix (apply later — not now)

| Asset | Action | Note |
|---|---|---|
| Story profile `3f297e81` | **UpdateAgent** | Dual mode banner: US Hermes-OFF + **package-S4 ON when routed**; HK package JSON (+ optional GEMINI) |
| New skill `story-package-s4` (name TBD) | **UpdateSkill** | Read PINNED handoffs/L2; write stories JSON+log; VERIFY vs `docs/05`; ANTI invent prices |
| `story-handoff-parse` | **小改** | Accept package `story_handoffs.md` / L2 row as US input (already STORY HANDOFF v5); pass Tradeable |
| `story-theme-match` / `web-search` / `narrative-validate` / `search-report` | **小改 or leave** | Reuse research; final emit via package-S4 skill not Fusion MD |
| Package Ops profile + `swing-package-fallback` | **UpdateAgent / UpdateSkill** | Event A → NEXT_GATE Story; after stories → sync/check/render/Drive (per OQ-3) |
| Fusion `c45141fc` | **唔改** US OFF | HK only if OQ-4 |
| Hermes / SB / 模擬倉 | **唔改** | SB/sim already Tradeable; need verdicts present for sim open |
| CreateAgent | **唔使** | |

### Apply order (after OQs + Justin AUTHORIZE)
1. Lock OQ-1..4 into ADDENDUM  
2. Write `story-package-s4` skill (+ mirrors)  
3. UpdateSkill `story-handoff-parse` tolerance  
4. UpdateAgent Story profile  
5. UpdateAgent/Skill Package Ops wake + post-story sync ownership  
6. Soft Final APPLY.md · self-VERIFY · no WV  

---

## 7. ANTI_JOBS (Story package mode)

- No US Story on Hermes-healthy daily auto-route  
- No invent entry/stop/target/RR/ADR numbers  
- No upgrade Tradeable FAIL / WATCH / AVOID / Baseline  
- No Scanner/Setup/Ops install  
- No wake SB/sim (總指揮 after verdicts)  
- No dual S4 with Hermes for same ticker+date  

## 8. VERIFY (PLAN gates — this Soft Final)

- [x] ONE_JOB + gap + PINNED file table  
- [x] Trigger vs Tradeable vs Story_Needed distinguished  
- [x] Wake matrix + Hermes priority + US/HK  
- [x] Scope matrix + apply order + ANTI  
- [x] OQs blocking apply listed  
- [x] No UpdateAgent / UpdateSkill / CreateAgent this turn  
- [x] No invented tickers/prices/verdicts  
- [x] Harness fields: PINNED_INPUTS / DECISIONS_MADE / OPEN_QUESTIONS / NEXT_GATE below  

---

## Fleet handoff fields (this PLAN)

```
PINNED_INPUTS:
  /workspace/docs/swing-package-2026-11-09/docs/05_HANDOFF_S4_S5.md
  /workspace/docs/swing-package-2026-11-09/docs/02_RUN_US.md
  /workspace/docs/swing-package-2026-11-09/TC-20261109-swing-APPLY.md
  /opt/swing/us/run_jfsrev_20261109/{L2_Input.csv,story_handoffs.md,Trigger_US.csv,Contract_US.csv,index.md}
  /workspace/swing-package-ops/logs/run_jfsrev_20261109/index.md
  Story profile 3f297e81… · Ops 9c97ff04… · Fusion c45141fc…
DECISIONS_MADE:
  Hermes US primary S4; Grok US auto-route OFF (v5.5.2);
  Package Ops LIVE; Tradeable gate LIVE; four scanners/setups RETIRED;
  Soft Final=Final / WV skip; PLAN only this TC
OPEN_QUESTIONS:
  OQ-1 Story universe (Story_Needed vs Trigger_PASS vs Tradeable PASS)
  OQ-2 Hermes-healthy: Grok Story stay OFF forever vs Justin opt-in package
  OQ-3 sync+check+render+Drive owner (Ops vs Story vs 總指揮)
  OQ-4 HK package: JSON-only vs keep GEMINI/Fusion parallel
NEXT_GATE:
  Justin via 總指揮 locks OQ-1..4 + AUTHORIZE apply → PA APPLY Soft Final
```

## Jev B (this PLAN)

`act=cheap_path` conf~0.74 · `evidence_enough`~0.45 · `escalate`~0.67 · cost_tier local. Thin evidence on OQs → escalate to Justin cards, not invent answers.
