# Soft Final PLAN — TC-20261109-swing-PA

**Status:** PLAN ONLY — Soft Final = Final. **WV skip.**  
**Do NOT:** UpdateAgent / UpdateSkill / CreateAgent / overwrite live profiles / install `/opt/swing` / invent tickers·prices·verdicts.  
**When:** 2026-11-09 HKT · Prompt Architect  
**Package:** Drive folder id `1wHl8gEEledw-6irNhpXP4nfze5HnMwow` · box mirror `/workspace/docs/swing-package-2026-11-09/`  
**Versions:** US **v5.5.4** `us-contract-1f.6` **113 cols** / 29 regressions · HK **v6.10** **116 cols** / 51 suite  
**ready_for_justin:** YES — **ALL OQs locked** (US/HK Hermes-primary+standby; Create=install+fallback new bot; Retire=4 bots). **APPLY AUTHORIZED 2026-11-09** — see `TC-20261109-swing-APPLY.md`.
**OQ-US ACK (2026-11-09 via 總指揮):** **A primary + B cold-standby fallback** — Hermes in use; when Hermes down, Grok US Scanner may run local v5.5.4. Not dual-run. No CreateAgent unless Justin opens later. **Still PLAN ONLY — no apply.**
**OQ-HK ACK (2026-11-09):** Hermes-primary + fallback (symmetric to US). See addendum `/workspace/docs/swing-package-2026-11-09/TC-20261109-swing-PA-ADDENDUM.md`.

### Jev B (pre_task)
- `act=cheap_path` (conf≈0.63) · `evidence_enough` noul≈0.39 · `escalate` noul≈0.57 · `cost_tier≈1`
- Branch taken: **cheap_path** on package docs + prior Soft Final + live skill heads; **escalate** flagged because evidence thin (mirror partial, BUGCHECK absent, `/opt/swing` not installed). Plan does **not** invent bugs or assume install done.

---

## 1. Conflicts with live fleet (MUST resolve via OQs before apply)

| Live (v5.5.2 APPLY TC-20261106) | Package 2026-11-09 | Conflict |
|---|---|---|
| US chain: **Hermes → Second brain (`d354ccee-…`) → 模擬倉 (`17a46819-…`)** | US engine v5.5.4 + Tradeable gate | Live skills/`hermes_soft_final.py` know **Risk_OK / Room_To_Supply_R** only — **zero `Tradeable` hits** in live US skills/script |
| US Swing Scanner `293d30a5-…` / 美股 Swing Setup `747b3374-…` **DEPRECATED** | Package is a local `/opt/swing/us` scanner+setup engine | Reopening Grok Scanner (OQ-US B) fights the deprecate banner unless Justin re-opens |
| Story `3f297e81-…` + Fusion `c45141fc-…` **US auto-route OFF** (HK live) | S4/S5 story still required by package (`docs/05`) on Hermes/DeepSeek side | Grok Story must stay off US unless Justin re-routes |
| PINNED Drive `US_Stock_Data/<Mon D>/` (`verdicts_US.jsonl`, `Contract_US.csv`, `L2_Input.csv`, `Trigger_US.csv`, `index.md`) | Contract shape **113 cols** (+ `Tradeable`, `Tradeable_Why`, `Room_At_Plan_Stop_R`, `Room_At_1_2ADR_R`) | Old Hermes packs without Tradeable cols will fail I30/V4d if mixed; SB/sim must not treat pre-gate STALK as openable |
| HK: Grok chain **HK Swing Scanner + 港股 Swing Setup + 投資敘事分析師 + Fusion Formatter** | HK engine v6.10 at `/opt/swing/hk` with same Tradeable rules | Dual truth risk if Grok Setup still emits STALK on 2.72×ADR names while package would WATCH |
| Soft Final=Final; WV skip; script-first Connector→Script→Browser Script→CU last | `verify.sh` → `VERIFY: PASS` is install gate | Apply must not claim PASS without running verify after real install |
| Prior Soft Final `/workspace/docs/us-swing-v55/TC-20261106-v55-APPLY-SOFT-FINAL.md` | This TC is **plan-only** delta on top of that apply | Do not re-litigate v5.5.2 deprecate; only add Tradeable / path / HK scope |

**Hard rule from package (Tradeable, 2026-11-08):**  
`risk ≤ 1.2×ADR` **AND** `risk% ≤ max(8%, 1.2×ADR%)` **AND** room floors (BREAKOUT/REVERSAL 1.5R, PULLBACK 1.0R) measured at **plan stop**. BUY/STALK must `Tradeable=PASS` else force **WATCH**; `Trigger_*` only PASS rows; **I30** + **V4d** enforce.

---

## 2. Scope matrix — bot / skill

Legend: **改** = patch on apply · **唔改** = leave · **deprecate** = keep/refresh banner · **重開** = only if Justin picks OQ that says so · **dr eggbot** = CreateAgent ownership after ACK (Justin note 2026-11-09)

| Target | id / path | Action | Notes |
|---|---|---|---|
| **Second brain** | `d354ccee-dcf7-4655-bbde-016bc5db7654` | **改** (profile + skills) — OQ-US A/C primary | Tradeable-aware bar; consume Hermes **or** Scanner-fallback Drive packs (same PINNED set); never stalk `Tradeable=FAIL` |
| **US swing 模擬倉** | `17a46819-623f-40fe-8430-338e05725381` | **改** | Open gate: verdict∈{BUY,STALK} **and** `Tradeable=PASS` (or Trigger row present ⇒ PASS by I30); FAIL/missing → skip |
| **US Swing Scanner** | `293d30a5-d04e-4443-89d9-f313f9ca873e` | **deprecate** daily · **B fallback cold standby** (OQ-US ACK) | Keep deprecate banner for normal days. Fallback only when Hermes down/unreachable: run local v5.5.4 `/opt/swing/us` (or box mirror) → Drive PINNED packs. Setup stays deprecated. **No CreateAgent** unless Justin later asks → **dr eggbot**. |
| **美股 Swing Setup** | `747b3374-ada7-44d7-8cf4-73098b1c10af` | **deprecate** stay (even on B fallback) | Package L2/render replaces Setup Master; fallback Scanner does not wake Setup |
| **投資敘事分析師 (Story)** | `3f297e81-4667-4dae-b517-b4f7ddee3537` | **唔改** US OFF · HK **live** | S4 Hermes/DeepSeek for US; HK GEMINI unchanged (OQ-HK = Hermes-primary + Scanner fallback, not Story rewrite) |
| **Fusion Formatter** | `c45141fc-c050-49e2-9635-dca556a0cc1f` | **唔改** US OFF · HK **live** | |
| **HK Swing Scanner** | `162f41b3-b93f-4d05-abdf-07b938f6ab56` | **Hermes-primary daily** · **cold-standby fallback** (OQ-HK ACK) | Daily follow Hermes HK L1. Fallback only when Hermes HK down: Grok Scanner and/or `/opt/swing/hk` after VERIFY. **Not dual-run. No CreateAgent.** |
| **港股 Swing Setup** | `28b5646e-bfc2-440b-8a63-b68440a1de4b` | **唔改** daily narrative · **小改** Tradeable-aware when Contract has cols | Stays Grok HK chain; fallback package Contract must not ship 2269-class as STALK |
| **總指揮 routing** | `7aa7a8a6-…` | **改** (總指揮 owns) after ACK | Encode OQ-US choice + Tradeable hard gate in routing memory; C9-style ownership like v55 APPLY |
| **dr eggbot** | (CreateAgent helper) | **ACK — CreateAgent install+fallback package bot** | Owns `/opt/swing` install+verify + Hermes-down US/HK scan. PA drafts JD only; does not CreateAgent. Retire 4 bots after LIVE. |
| `us-second-brain-3-picks` | workflows | **改** | Tradeable PASS filter; never upgrade WATCH; copy `Tradeable_Why` into demote notes; Contract 113-col tolerant |
| `us-swing-sim-open` | workflows | **改** | 四問 + `Tradeable=PASS` (or Trigger membership); NO_TRADE if verdicts missing |
| `us-swing-sim-track` | workflows | **唔改** core exits · **小改** optional | Keep Supply/room exits; note Trigger rows are already Tradeable-filtered upstream |
| `us-swing-sim-reconcile` | workflows | **小改** | Outside-judge classes may show more WATCH post-gate; still ground truth = `verdicts_US.jsonl` |
| `us-swing-session-overview` | workflows | **唔改** / optional climate note | Still `Room_To_Supply_R`; may mention Tradeable demotions as climate one-liner if present |
| `story-handoff-parse` | workflows | **小改** | US STORY HANDOFF: accept/ignore new Contract cols; still reject invented prices; HK GEMINI keep |
| `hermes_soft_final.py` | `/workspace/second-brain/scripts/` | **改** | Exclude / hard-fail stalks with `Tradeable=FAIL` or missing when col present; pass through Why |
| `hk-swing-trade-analysis` | workflows | **小改** | When reading package Contract: force WATCH on Tradeable FAIL; keep GEMINI handoff for HK Story |
| `hk-swing-setup-playbook` | workflows | **小改** | Document Tradeable floors / no ticket without plan when cols present |
| `hk-swing-csv-validate` | workflows | **小改** | Expect 116 cols + Tradeable* when reading package `/opt/swing/hk` Contract |
| `hk-swing-scenario-stop` | workflows | **唔改** default | Stop math ≠ Tradeable gate; gate is post-plan |
| `fusion-*` | workflows | **唔改** | US auto-route already OFF |

---

## 3. Tradeable gate hang — skills / VERIFY / handoff

### Force PASS (ticket may exist)
| Layer | Rule |
|---|---|
| Engine `generate_trigger` | Only `Tradeable=PASS` rows → `Trigger_US.csv` / HK trigger |
| `l2_prep.tradeable_gate` | `Tradeable=FAIL` → **any class → WATCH** |
| `check_verdict` **V4d** | BUY/STALK require `Tradeable=PASS` (package `docs/04`; US PATCH_NOTES labels this V4c — treat **docs/04 / HK notes as canonical V4d**) |
| `invariants` **I30** | Every Trigger row is `Tradeable=PASS` or run FAIL |
| Second brain / `hermes_soft_final.py` | May list ≤3 stalks only from PASS (or Trigger-listed) names; **never upgrade** WATCH/AVOID |
| 模擬倉 `us-swing-sim-open` | Open/working-order only if verdict∈{BUY,STALK} **and** Tradeable PASS / Trigger row |

### WATCH demote wording (copy, do not invent)
- Use engine `Tradeable_Why` verbatim when present, e.g.  
  `risk=2.40xADR > 1.2 (plan stop); risk=9.9% > 8%; room@plan stop=1.05R < 1.5` (GME ref in US PATCH)  
  `risk=2.72xADR > 1.2; risk=17.3% > 8%; room@plan stop=0.63R < 1.5` (2269.HK ref in HK PATCH)
- Chat/handoff: **「暫不掛單／要等／原因：{Tradeable_Why}」** — no entry/stop/shares on WATCH/AVOID (render_report B5).
- Pending breakout **not exempt** — plan stop judged before fill.

### Caps (env, not code edits)
- `SWING_RISK_ADR_CAP=1.2` · `SWING_RISK_PCT_CAP=8.0` (pct floats to `max(8%, 1.2×ADR%)`)

---

## 4. Path migration

| Role | Current | Target after Justin ACK + install | Notes |
|---|---|---|---|
| US engine home | Hermes host (opaque to Grok) + Drive pin | **`/opt/swing/us`** (package) or box mirror `…/swing-package-2026-11-09/US` until install | `/opt/swing` **NOT** installed on this box today |
| HK engine home | Grok Scanner/Setup + Hermes HK L1 | **Daily Hermes**; fallback **`/opt/swing/hk`** after VERIFY | Prefer package path over legacy `/opt/hk-swing` (M1) |
| Scan US | Hermes-owned | `cd /opt/swing/us/02_CODE && SWING_OUTPUT_FOLDER=… bash run_daily.sh` or `./scan553.sh "…"` | US has **no cron** — universe supplied per request |
| Scan HK | Grok / manual | `SWING_OUTPUT_FOLDER=runs/hk/run_<date> bash run_daily.sh` | Pin `SWING_MARKET=hk` via script |
| Verify | n/a on box | `bash verify.sh /opt/swing` → **`VERIFY: PASS`** (29 US + 51 HK) | Do not scan/report if FAIL |
| Drive upload US | `US_Stock_Data/<Mon D>/` PINNED set | **Same folder contract**; file set unchanged | **Column contract changes:** Contract **113** cols must include `Tradeable`, `Tradeable_Why`, `Room_At_Plan_Stop_R`, `Room_At_1_2ADR_R` |
| Drive upload HK | per existing HK ops | If package used: 116-col Contract + same Tradeable* cols | Do not mix US/HK verdict filenames |

**New columns (both markets):** `Tradeable` · `Tradeable_Why` · `Room_At_Plan_Stop_R` · `Room_At_1_2ADR_R`  
**Consumers to teach:** `hermes_soft_final.py`, `us-second-brain-3-picks`, `us-swing-sim-open` (+ HK `hk-swing-csv-validate` when reading package Contract on fallback).

**Env path vars:** `SWING_HOME` · `SWING_ROOT` · `SWING_OUTPUT_FOLDER` · `SWING_ASOF` · `SWING_MARKET` (see `docs/01`).

---

## 5. Open questions for Justin (≤5)

### ANSWERED
1. **OQ-US (ACK 2026-11-09):** **A primary + B cold-standby fallback** — Hermes L1 → SB → 模擬倉 daily; US Scanner `293d30a5-…` only when Hermes down; Setup stays deprecate; not dual-run; **no new Scanner bot**.
2. **OQ-HK (ACK 2026-11-09):** **hermes-primary + fallback** (symmetric) — follow Hermes HK L1 when present; when down use Grok HK Scanner `162f41b3-…` and/or `/opt/swing/hk`; not dual-run; **no new Scanner bot**.
3. **OQ-Install / Create (ACK 2026-11-09):** **install+fallback** new bot via **dr eggbot**. Owns `/opt/swing` install+verify, B1/B2/M5 fixes, Hermes-down US/HK package scan. **總指揮只路由** — 唔跑 install.
4. **OQ-Retire (ACK 2026-11-09):** Retire **all four**: `293d30a5` US Scanner · `747b3374` 美股 Setup · `162f41b3` HK Scanner · `28b5646e` 港股 Setup. Retire = deprecate/hide + ANTI accept-TC; function → new install+fallback bot. **UpdateAgent retire banners after new bot LIVE** (or sync 總指揮).

### STILL OPEN
5. **(none for OQ)** — Apply in flight. B1/B2/M5 install owned by package bot / 總指揮 executor parallel. PA holds Scanner/Setup retire UpdateAgent until LIVE.


---

## 6. Bug→plan hooks (from BUGCHECK Soft Final)

**Source:** `/workspace/docs/swing-package-2026-11-09/TC-20261109-swing-BUGCHECK.md` (checked 2026-11-09 16:10 HKT; SHA **121/121 OK**).  
**Status:** mapped below — **still not executed** (PLAN ONLY).

| ID | Sev | Hook into apply | PASS criteria |
|---|---|---|---|
| **B1** | BLOCKER | Apply #0 / install.sh patch: write `$TARGET/hk/.swing_market=hk` (+ us marker) | `verify_hk.sh` step 5b PASS; HK run does not emit US defaults |
| **B2** | BLOCKER | Apply #0 / `US/scan553.sh`: ship `scripts/clean_runs.sh` **or** optional `-x` / `KEEP_RAW=1` documented | Fallback scan exits 0 after success without missing-script fail |
| **M1** | MAJOR | Docs patch `HK/HERMES_HK_MANUAL.md` → `install.sh /opt/swing` + `verdicts_hk.jsonl` | Manual matches root installer; no `INSTALL_HK.sh` |
| **M2** | MAJOR | Install rename/glob for KB mojibake; skills open `00_*.md` not hard Chinese path | Story KB open-by-glob works post-install |
| **M3** | MAJOR | **Satisfied by OQ-US ACK** ownership matrix (Hermes primary / Scanner fallback / Setup deprecate) | Routing memory + this PLAN §2/§8 encode matrix |
| **M4** | MAJOR | Optional: bump HK `CONTRACT_VERSION` + DATA_DICTIONARY when touching HK | Version string matches Tradeable columns |
| **M5** | MAJOR | Apply #0: recursive `chmod +x` on `**/*.sh` under `/opt/swing` | Nested `02_CODE/*.sh` executable |
| **M6** | MAJOR | Doc-only: HK `tests/sample/*_US*` = shared fixture | No bot wires HK sample as live HK Contract |
| **m1–m5** | MINOR | README Tradeable sentence; V4d align US docs; acceptance≠sample label; root `verify.sh` vs `verify_hk.sh` note | Docs clean; no silent dual-PASS confusion |

**Known doc tension:** US PATCH_NOTES **V4c** vs `docs/04` **V4d** for Tradeable → follow **`docs/04` / HK** (BUGCHECK m2).


---

## 7. Mirror / install inventory

| | Count |
|---|---|
| MANIFEST files | **121** (`us_files` 69 + `hk_files` 42) |
| Present on box (BUGCHECK) | **121/121** sha256 OK |
| `/opt/swing` | **NOT installed** (do not assume) |

**Extras (not in MANIFEST):** root `scan553.sh` duplicate, `_backup_partial/`, `_tools/`, BUGCHECK, this PLAN.  
**Rule:** Apply step 0 still = install + `VERIFY: PASS` **after** B1/B2/M5 fixes — mirror completeness ≠ install readiness.


---

## 8. Numbered apply order (DO NOT EXECUTE)

Each step: owner · artifact · PASS criteria. Execution only after Justin ACK + OQ answers.

| # | Owner | Action | PASS criteria |
|---|---|---|---|
| 0 | **Package bot** (OQ-Install lean; CreateAgent via dr eggbot after card) — **not 總指揮** | Mirror OK (121/121). Patch **B1/B2/M5**; `bash install.sh /opt/swing`; root + `verify_hk.sh`. Retire list after bot lives. | VERIFY PASS + HK marker; 113/116 Tradeable*; no install by 總指揮 |
| 0c | **dr eggbot** (after Justin OQ-Create card) | **CreateAgent** package-owner bot; hand JD/skills from this Soft Final; **not** Prompt Architect CreateAgent | New bot id exists; ONE_JOB = install/verify/fallback package; 總指揮 does not run install |
| 1 | Prompt Architect | Patch `hermes_soft_final.py` Tradeable hard exclude + Why passthrough | Unit/self-check: FAIL rows never in stalk list when col present; banned-field grep still clean |
| 2 | Prompt Architect | UpdateSkill `us-second-brain-3-picks` (+ sand/MM mirrors) | SKILL text requires Tradeable PASS; never upgrade WATCH; Drive pin paths unchanged |
| 3 | Prompt Architect | UpdateSkill `us-swing-sim-open` (+ mirrors) | Open/四問 require Tradeable PASS or Trigger membership; NO_TRADE on missing verdicts |
| 4 | Prompt Architect | UpdateSkill `us-swing-sim-reconcile` (+ optional track/overview/story-handoff-parse) | Docs mention post-gate WATCH inflation; parse tolerates 113 cols |
| 5 | Prompt Architect | UpdateAgent Second brain `d354ccee-…` profile ONE_JOB/IO/red-lines | Profile cites Tradeable; still Hermes Drive IO; no Scanner wake |
| 6 | Prompt Architect | UpdateAgent 模擬倉 `17a46819-…` profile | Tradeable in entry gate; no Setup Master; paper only |
| 7 | Prompt Architect | **OQ-US ACK — A primary + B fallback:** keep Scanner/Setup **deprecate** banners for daily path; UpdateAgent Scanner profile with **fallback runbook only** (no CreateAgent) | Daily: Hermes→SB→sim. Banner still says DEPRECATED for normal TCs |
| 7f | Prompt Architect | **US fallback runbook**: wake `293d30a5-…` **only** when Hermes US down/unreachable; `VERIFY: PASS` (+ B1/B2/M5); `/opt/swing/us` (or box mirror); Drive `US_Stock_Data/<Mon D>/` PINNED 113-col Tradeable*; Setup not woken; announce; stop when Hermes returns | Wake/VERIFY/commands/Drive/stop documented |
| 8 | Prompt Architect | **HK Hermes-primary** note on Scanner `162f41b3-…` (keep live for HK chain; not US-style deprecate unless Justin asks) | Profile: Hermes HK L1 primary; no daily dual-run |
| 8f | Prompt Architect | **HK fallback runbook** (symmetric to #7f): wake `162f41b3-…` and/or `/opt/swing/hk` **only** when Hermes HK down; VERIFY-first (+ B1); `run_daily.sh`/`run_l2.sh`; HK Drive/ops (116-col Tradeable* if package); Setup `28b5646e-…` Tradeable-aware only; announce; stop when Hermes returns | Symmetric to US #7f |
| 8s | Prompt Architect | Small HK skill patches (`hk-swing-csv-validate` / analysis / playbook) for 116-col + Tradeable when reading package Contract | 2269-class cannot ship STALK when Tradeable FAIL |
| 9 | 總指揮 | Routing memory / C9-equivalent: encode OQ-US + Tradeable hard gate | Fleet routes match chosen path; WV still skip unless Justin changes |
| 10 | Prompt Architect | Docs stage under `/workspace/docs/swing-package-2026-11-09/` + `/workspace/prompt-architect/TC-20261109-swing-PA/` | Soft Final apply note + md5; link this PLAN |
| 11 | Prompt Architect | Execute §6 bug hooks (B1/B2 required; M*/m* per Justin) | Each BUGCHECK id CLOSED or DEFERRED with Justin note in apply Soft Final |
| 12 | Self-VERIFY | Banned grep + matrix audit | No live apply leaked into PLAN TC; no invented tickers; OQs unanswered → stop |

**ANTI (restate):** This PLAN TC executes **none** of #0–#12.

---

## 9. Self-VERIFY checklist (this PLAN document)

- [x] Header: TC, PLAN ONLY, Soft Final=Final, WV skip, Jev B note, `ready_for_justin`
- [x] Conflicts: live v5.5.2 Hermes→SB→sim vs package v5.5.4 Tradeable; deprecate/OFF bots named with ids
- [x] Scope matrix covers Scanner, Setup, HK Scanner, 港股 Setup, Story, Fusion, SB, 模擬倉, 總指揮, story-handoff-parse, sim/session skills, `hermes_soft_final.py`, dr eggbot
- [x] Tradeable hang: V4d/I30/Trigger/WATCH demote wording + caps
- [x] Path migration: `/opt/swing/{us,hk}`, Drive 113 vs old, new cols listed
- [x] OQs locked: US/HK Hermes-primary+standby; Create=install+fallback via dr eggbot; Retire=4 bots; APPLY AUTHORIZED
- [x] Bug→plan mapped from BUGCHECK Soft Final (B1/B2/M1–M6/m*) — no invented bugs
- [x] Apply order numbered with PASS criteria — **not executed**
- [x] Mirror 121/121; `/opt/swing` still absent until apply #0
- [x] No UpdateAgent/UpdateSkill/CreateAgent/SendToAgent in this TC
- [x] No invented ticker/price/verdict beyond package reference demotions (GME/DNA/2269/6862/0386 as **docs citations only**)

---

## 10. Sources read

- `/workspace/docs/swing-package-2026-11-09/{README,install.sh,verify.sh,MANIFEST.json}`
- `docs/01_INSTALL.md` … `06_ACCEPTANCE.md`
- `US/PATCH_NOTES_v5.5.4.md`, `US/HERMES_MANUAL.md` (§4b Tradeable)
- `HK/PATCH_NOTES_v6.10.md`, `HK/HERMES_HK_MANUAL.md`
- Prior: `/workspace/docs/us-swing-v55/TC-20261106-v55-APPLY-SOFT-FINAL.md` (+ PLAN sibling)
- Live skill heads: `us-second-brain-3-picks`, `us-swing-sim-{open,track,reconcile}`, `us-swing-session-overview`, `story-handoff-parse`, `hk-swing-*`, `fusion-*`
- `hermes_soft_final.py` (no Tradeable today)
- BUGCHECK: **absent**

---

*TC-20261109-swing-PA Soft Final PLAN — Prompt Architect. ALL OQs locked 2026-11-09. APPLY AUTHORIZED — see TC-20261109-swing-APPLY.md. CreateAgent via dr eggbot; PA does Tradeable skills/profiles + drafts.*
