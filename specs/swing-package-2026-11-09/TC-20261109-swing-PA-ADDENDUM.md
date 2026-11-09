# Soft Final ADDENDUM — TC-20261109-swing-PA

**Status:** PLAN ONLY addendum — Soft Final = Final. **WV skip. Do NOT apply.**  
**When:** 2026-11-09 HKT · Prompt Architect  
**Parent PLAN:** `/workspace/docs/swing-package-2026-11-09/TC-20261109-swing-PA-PLAN.md` md5 `635610caa6a932516fcb816043fc396a`  
**BUGCHECK:** `/workspace/docs/swing-package-2026-11-09/TC-20261109-swing-BUGCHECK.md` md5 `0d52182e251d5215a6f0eea76db874c4` · SHA **121/121 OK**  
**ready_for_justin:** ALL OQs locked. Create=**install+fallback**. Retire=**4 bots**. **APPLY AUTHORIZED** → `TC-20261109-swing-APPLY.md`.

---

## 1. OQs locked

| OQ | Justin answer | Meaning |
|---|---|---|
| **OQ-US** | **Hermes primary + B cold standby** | Daily: Hermes L1 → Second brain (`d354ccee-…`) → 模擬倉 (`17a46819-…`). US Scanner `293d30a5-…` / Setup `747b3374-…` **stay DEPRECATED** for normal days. **Only when Hermes down/unreachable:** Scanner may run local package **v5.5.4** `/opt/swing/us` (or box mirror) → Drive PINNED packs. **Not dual-run. No CreateAgent** unless later TC. |
| **OQ-HK** | **hermes-primary + fallback** (symmetric) | Daily: follow **Hermes HK L1** when present. **Only when Hermes HK down:** Grok HK Swing Scanner (`162f41b3-…`) and/or `/opt/swing/hk` package. 港股 Setup (`28b5646e-…`) + Story/Fusion stay on Grok HK narrative path unless a later ACK says otherwise. **Not dual-run.** |

| **OQ-Install / Create** | **ACK: install+fallback** (2026-11-09) | **dr eggbot CreateAgent** new bot owns `/opt/swing` install+verify, B1/B2/M5, Hermes-down US/HK package scan. **總指揮只路由.** |
| **OQ-Retire** | **ACK: all four** | `293d30a5` · `747b3374` · `162f41b3` · `28b5646e` — deprecate/hide after new bot LIVE; function → package bot. |

**Still open for PA:** none on OQs. Retire UpdateAgent **after** package bot LIVE. Install/B1/B2 parallel via package bot / 總指揮 executor.

---

## 2. Bug → apply rows (from BUGCHECK)

| ID | Sev | Apply artifact | PASS criteria |
|---|---|---|---|
| **B1** | BLOCKER | Patch `install.sh` (+ ship markers): write `$TARGET/hk/.swing_market=hk` and `$TARGET/us/.swing_market=us` | `verify_hk.sh` market-lock PASS; HK does not default to SPY/`verdicts_us` |
| **B2** | BLOCKER | Ship `US/scripts/clean_runs.sh` **or** soft-fail/`KEEP_RAW=1` in `US/scan553.sh` | Fallback US scan exits 0 after success without missing-script fail |
| **M1** | MAJOR | Rewrite `HK/HERMES_HK_MANUAL.md` → `bash install.sh /opt/swing` + `verdicts_hk.jsonl` | No `INSTALL_HK.sh` / `/opt/hk-swing` as required path |
| **M2** | MAJOR | Rename mojibake KB/report files **or** install-time rename + skills glob `00_*.md` | Open-by-glob works; regenerate MANIFEST if renamed |
| **M3** | MAJOR | Ownership = this addendum §1 (already ACK’d) | Routing memory encodes Hermes primary / Scanner fallback both markets |
| **M4** | MAJOR | Optional: bump HK `CONTRACT_VERSION` + DATA_DICTIONARY to Tradeable era | String matches 116-col Tradeable contract |
| **M5** | MAJOR | `install.sh`: recursive `chmod +x` on `**/*.sh` | Nested `US/02_CODE/*.sh` executable |
| **M6** | MAJOR | Doc-only: HK `tests/sample/*_US*` = shared fixture | No bot treats sample as live HK Contract |
| **m1–m5** | MINOR | README Tradeable grammar; align US V4d label; label acceptance≠sample; note root `verify.sh` ≠ `verify_hk.sh` | Docs clean |

Canonical Tradeable check id: **V4d** (`docs/04` / HK); US PATCH_NOTES “V4c” is alias drift (m2).

---

## 3. Fallback runbook (both markets)

### Wake conditions
- **US:** Hermes US L1 **down / unreachable** (總指揮 or Justin declares) → wake US Scanner `293d30a5-…` **once** for that session.  
- **HK:** Hermes HK L1 **down / unreachable** → wake HK Scanner `162f41b3-…` and/or run `/opt/swing/hk` **once**.  
- **Never** schedule dual daily runs while Hermes is healthy.

### Prerequisites (hard)
1. Mirror 121/121 (done).  
2. **B1 + B2 + M5** fixed in package copy used for install.  
3. `bash install.sh /opt/swing` then:
   - `bash verify.sh /opt/swing` → `VERIFY: PASS` (29 + 51)
   - `bash /opt/swing/hk/verify_hk.sh` → ALL CHECKS PASSED (needs `.swing_market=hk`)
4. If verify FAIL → **do not scan**; escalate to Justin/總指揮.

### Commands (after VERIFY)
- **US:** `cd /opt/swing/us/02_CODE` → `SWING_OUTPUT_FOLDER=runs/us/run_<YYYYMMDD> bash run_daily.sh` (or `US/scan553.sh "…"` with cleanup fixed); then L2 prep/check/render per `docs/02`.  
- **HK:** `cd /opt/swing/hk` → `SWING_OUTPUT_FOLDER=runs/hk/run_<YYYYMMDD> bash run_daily.sh`; `run_l2.sh` (pins `SWING_MARKET=hk`).

### Drive / handoff
- **US upload:** `Drive US_Stock_Data/<Mon D>/` PINNED set — `verdicts_US.jsonl`, `Contract_US.csv` (**113 cols** + Tradeable*), `L2_Input.csv`, `Trigger_US.csv` (PASS-only), `index.md`.  
- **HK:** keep existing HK Drive/ops contract; if package used, Contract **116 cols** + Tradeable*; verdicts file **`verdicts_hk.jsonl`**.  
- Consumers (SB / 模擬倉 / HK Setup) read **Drive truth**; never invent prices. Tradeable FAIL → WATCH wording from `Tradeable_Why` verbatim.

### Stop condition
When Hermes returns healthy → **stop** Scanner fallback; return to Hermes-primary routing; leave deprecate banners on US Scanner/Setup for normal TCs.

### Announce
Each fallback wake: one line to 總指揮 + Justin (who woke, market, verify md5/PASS, Drive folder date).

---

## 4. Apply order (updated — DO NOT EXECUTE)

| # | Owner | Action | PASS |
|---|---|---|---|
| 0 | **Package bot** (after CreateAgent) — **not 總指揮** | Fix **B1/B2/M5** (+ optional M*); `install.sh /opt/swing`; root + HK verify | VERIFY PASS; 113/116 Tradeable*; install not on 總指揮 |
| 0c | **dr eggbot** | CreateAgent package-owner per Justin OQ-Create card; PA supplies JD/skills Soft Final only | Bot id live; then retire list applied |
| 1 | PA | `hermes_soft_final.py` Tradeable hard exclude + Why passthrough | FAIL never in stalk list when col present |
| 2 | PA | UpdateSkill `us-second-brain-3-picks` (+ mirrors) | Tradeable PASS filter; Drive pin unchanged |
| 3 | PA | UpdateSkill `us-swing-sim-open` (+ mirrors) | Open requires Tradeable PASS / Trigger membership |
| 4 | PA | UpdateSkill reconcile (+ optional track/overview/`story-handoff-parse`) | 113-col tolerant; no invent targets |
| 5 | PA | UpdateAgent Second brain `d354ccee-…` | Tradeable red-line; Hermes **or** fallback Drive packs |
| 6 | PA | UpdateAgent 模擬倉 `17a46819-…` | Same entry gate; Setup stays out |
| 7 | PA | US Scanner `293d30a5-…`: **keep deprecate** + US fallback runbook §3 / PLAN #7f (no CreateAgent) | Banner intact; wake only Hermes-down |
| 7f | PA | US fallback runbook detail (VERIFY → `/opt/swing/us` → Drive PINNED 113-col → announce → stop) | Documented in §3 |
| 8 | PA | HK Scanner `162f41b3-…`: **Hermes-primary** profile note (live HK chain kept; not US-deprecate) | Hermes HK L1 primary; no dual-run |
| 8f | PA | **HK fallback runbook** (symmetric to US #7f): wake Scanner and/or `/opt/swing/hk` only when Hermes HK down; VERIFY-first (+ B1); Drive/ops 116-col; announce; stop when Hermes returns | Same structure as US #7f |
| 8s | PA | HK skills (`hk-swing-csv-validate` / analysis / playbook) for 116-col + Tradeable when reading package Contract | 2269-class cannot ship STALK on Tradeable FAIL |
| 9 | PA | (fold into 8s if thin) | — |
| 10 | 總指揮 | Routing memory both markets: Hermes primary / Scanner cold standby; Tradeable hard gate | Fleet routes match §1 |
| 11 | PA | Close BUGCHECK rows in apply Soft Final (CLOSED/DEFERRED) | Every B/M/m id accounted |
| 12 | Self-VERIFY | Banned grep; no live apply in PLAN TC; OQ-US/HK locked text matches Justin | PASS |

**ANTI:** This addendum executes **none** of #0–#12.

---

## 5. Self-VERIFY (addendum)

- [x] OQ-US + OQ-HK locked as Hermes-primary + fallback (symmetric)
- [x] OQ-Install lean = new package bot (not 總指揮); CreateAgent lean YES via dr eggbot — card + retire list still open
- [x] Bug→apply rows for B1/B2/M1–M6 (+ minor pointer)
- [x] Fallback runbook: wake / VERIFY-first / commands / Drive pin / stop / announce
- [x] Apply order updated; **not executed**
- [x] Parent PLAN + BUGCHECK md5 cited; WV skip; Soft Final=Final

---

*TC-20261109-swing-PA ADDENDUM — Prompt Architect. ALL OQs locked. APPLY AUTHORIZED. CreateAgent via dr eggbot; retire UpdateAgent after LIVE.*
