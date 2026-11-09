# TC-20261109-swing-BUGCHECK — Soft Final

**Status:** Soft Final (plan-only; no `/opt/swing` install; no bot/skill edits)  
**Package:** `swing-package-2026-11-09`  
**Mirror:** `/workspace/docs/swing-package-2026-11-09/`  
**Checked:** 2026-11-09 16:10 HKT (Asia/Hong_Kong)  
**SHA vs MANIFEST:** **121/121 OK**, 0 missing, 0 mismatch  
**Extras (not in MANIFEST):** `scan553.sh` (root; from chat attach), `_backup_partial/`, `_tools/`, this report, `INVENTORY.md`

---

## Pull summary

| Item | Result |
|---|---|
| Drive root | `1wHl8gEEledw-6irNhpXP4nfze5HnMwow` |
| MANIFEST counts | us_files=69, hk_files=42, total=121 (+ MANIFEST itself) |
| Local mirror | 121/121 files present; sha256 all match |
| Root `scan553.sh` on Drive | **Absent** (only under `US/scan553.sh`) |
| Chat-attach leftover | Root `scan553.sh` kept as EXTRA (byte-identical to `US/scan553.sh`) |

---

## Findings (by severity)

### BLOCKER

#### B1. Fresh HK tree has no `.swing_market` → defaults to US
- **Paths:** `HK/markets.py`, `HK/run_daily.sh`, `HK/run_l2.sh`, `HK/verify_hk.sh`, root `install.sh`
- **Evidence:** `markets.load()` with no `SWING_MARKET` and no `.swing_market` returns **US** (`bench=SPY`, `verdicts_us.jsonl`). `verify_hk.sh` step 5b explicitly fails if marker ≠ `hk`. Root `install.sh` only `tar` copies trees — it never writes `.swing_market=hk`.
- **Impact after naive install:** `/opt/swing/hk` can emit US-shaped outputs / currency; `verify_hk.sh` → FAIL; solo `run_l2.sh` falls back to US (script comment warns this).
- **Fix (recommended):** `install.sh` should write `hk` into `$TARGET/hk/.swing_market` (and `us` into `$TARGET/us/.swing_market`). Ship the marker in `HK/` (and optionally `US/`). Document in `docs/01_INSTALL.md`.

#### B2. `US/scan553.sh` calls missing `scripts/clean_runs.sh`
- **Path:** `US/scan553.sh:33` → `${SWING_ROOT:-$PWD}/scripts/clean_runs.sh`
- **Evidence:** No `scripts/` directory anywhere in package / MANIFEST.
- **Impact:** After a successful engine run, cleanup fails. With `set -uo pipefail`, the pipeline can exit non-zero even when the scan itself succeeded (unless `KEEP_RAW=1`).
- **Fix:** Either ship `US/scripts/clean_runs.sh`, or make cleanup optional (test `-x` before call), or remove the call from the portable patch.

---

### MAJOR

#### M1. `HERMES_HK_MANUAL.md` documents a different installer than this package
- **Path:** `HK/HERMES_HK_MANUAL.md`
- **Evidence:** Instructs `./INSTALL_HK.sh /opt/hk-swing`. **No `INSTALL_HK.sh` exists.** Package installer is root `install.sh` → `/opt/swing/hk`.
- **Also:** Manual still says S4/S5 land in `verdicts_US.jsonl` while `markets.verdicts_filename()` for HK is `verdicts_hk.jsonl` (legacy US name still honoured on read).
- **Fix:** Rewrite manual to `bash install.sh /opt/swing` + `verify_hk.sh`; align verdict filename guidance.

#### M2. Story-search KB filenames are mojibake; docs reference correct Chinese names
- **Paths:** `US/01_RULES/story_search/KB/00_*.md` … `03_*.md`; also `US/03_SAMPLE/run_v56/reports/*_µèòΦ│çσ┐½σá▒.md`
- **Evidence:** On-disk / MANIFEST / Drive names decode (cp437←UTF-8) to `00_核心敘事指南.md`, `01_2026全球大趨勢.md`, `02_十五五宏觀政策.md`, `03_2026生物醫藥.md`, `*_投資快報.md`. `KB/README.md` and `kb-routes.md` reference the **correct** Chinese names → open-by-path breaks.
- **Fix:** Rename files to the Chinese names (re-upload to Drive + regenerate MANIFEST). Until then, bots/skills must open via glob/`00_*.md` or a rename step on install.

#### M3. Hermes-shaped package vs current Grok bot fleet (routing conflict)
- **Paths:** `US/HERMES_MANUAL.md`, `HK/HERMES_HK_MANUAL.md`, `docs/05_HANDOFF_S4_S5.md`
- **Package assumes:** Hermes daemon owns S1–S3/S6–S7/S9; DeepSeek does S4/S5; daily windows 05:30 US / 17:30+ HK; install under `/opt/us-swing` or `/opt/hk-swing` (manual) / `/opt/swing/{{us,hk}}` (root install).
- **Current Grok context (from parent):** US Swing Scanner / Setup **DEPRECATED**; live chain **Hermes → Second brain → 模擬倉**; HK Swing Scanner still live. Re-enabling this package as “US/HK Swing Scanner skills” without a stage map will double-run or fight DEPRECATED flags.
- **Fix (for PA plan, not this TC):** Explicit ownership matrix: which Grok bot owns S1 scan, which owns S4 story, which owns S5 verdict, what is deprecated, where `/opt/swing` lives relative to Hermes.

#### M4. HK engine contract version lag vs Tradeable columns
- **Path:** `HK/us_swing_v55.py` (`CONTRACT_VERSION` still `hk-contract-1f.5` / `us-contract-1f.5`)
- **Evidence:** v6.10 adds Tradeable four columns (PATCH_NOTES) but version string not bumped to match US `us-contract-1f.6`. `HK/01_RULES/DATA_DICTIONARY.md` still cites `us-contract-1f.4`.
- **Impact:** Version gates / docs drift; not necessarily a runtime break (columns exist).
- **Fix:** Bump HK contract id when Tradeable landed; refresh DATA_DICTIONARY.

#### M5. `install.sh` chmod misses nested US scripts
- **Path:** `install.sh:20` → only top-level `$TARGET/us/*.sh` and `$TARGET/hk/*.sh`
- **Evidence:** US runners live at `US/02_CODE/run_daily.sh`, `run_l2.sh` — not chmod’d. Drive downloads land mode `644`.
- **Impact:** `./run_daily.sh` from `02_CODE` may fail without `bash` prefix after install.
- **Fix:** Recursive `find … -name '*.sh' -exec chmod +x`.

#### M6. HK `tests/sample/*_US*` is US-market fixture with stale contract
- **Paths:** `HK/tests/sample/Contract_US.csv`, `Evidence_US.csv`, `Trigger_US.csv`, `verdicts_US.jsonl`, stories `INTA_*` / `UNH_*`
- **Evidence:** `Market=US`, `Benchmark=SPY`, tickers RVTY/INTA/…, `contract_version=us-contract-1f.4` (pre-Tradeable). Suite/regressions **hard-code** these US names — so not a suite break, but naming is misleading for an HK package and can confuse bot wiring.
- **Fix:** Rename to `*_fixture.csv` / document “shared US-shaped fixture for unit tests”; or add a true HK sample alongside. Prefer not renaming without suite updates.

---

### MINOR

#### m1. Root vs US `scan553.sh` duplication / Drive gap
- Drive root has **no** `scan553.sh`; MANIFEST `portability_patches` lists only `US/scan553.sh`.
- Chat attach placed a copy at package root. Running root copy from DEST root fails (expects sibling `02_CODE/`).
- **Fix:** Document “run from `US/` only”; delete root extra or add symlink note in README.

#### m2. V4c / V4d naming inconsistency
- US `PATCH_NOTES_v5.5.4.md` + US `check_verdict.py`: Tradeable check labelled **V4c**.
- HK + `docs/04_GATES_AND_CAPS.md`: **V4c** = Risk_OK for STALK; **V4d** = Tradeable.
- US `WORKFLOW_v55.md` lists two different V4c rows.
- **Fix:** Align US code/docs to V4d for Tradeable (match docs/04 + HK).

#### m3. README hard-rule sentence is garbled
- **Path:** `README.md` Hard rules bullet 1: “`Tradeable=PASS` is required for any BUY/STALK is moved to WATCH”
- **Fix:** e.g. “BUY/STALK require `Tradeable=PASS`; FAIL → forced WATCH.”

#### m4. Acceptance day vs sample day differ (not a defect, easy to misread)
- `docs/06_ACCEPTANCE.md`: US BUY **DNA**; HK BUY **6862/0386**, 2269→WATCH.
- `US/03_SAMPLE/run_v56`: RVTY ticket (1f.6). Different session — OK if labelled; easy for bots to treat sample as acceptance.

#### m5. `verify.sh` (root) can PASS while `verify_hk.sh` FAILs
- Root verify only: py_compile + US regressions + HK suite.
- Does **not** run `verify_hk.sh` (marker / earnings_overrides / tickers_hk checks).
- **Fix:** Optionally invoke both side verifiers after install.

---

### NOTE (intentional / non-bugs)

#### N1. US vs HK `us_swing_v55.py` size/sha differ — intentional
- US: 75314 B, sha `4e9f6c0f…` (v5.5.4, `us-contract-1f.6`, 113 cols)
- HK: 79859 B, sha `1aa7fb31…` (v6.10 HK profile, 116 cols)
- README states independent engines / no shared imports. **Not a sync bug.**

#### N2. Tradeable gate consistency — logic aligned
- Docs `04`, US/HK PATCH_NOTES, both `gates.tradeability()`, `l2_prep.tradeable_gate`, I30, generate_trigger PASS-only: **consistent** on 1.2×ADR, `max(8%, 1.2×ADR%)`, room floors, FAIL→WATCH.
- Residual: V4c/V4d label drift (m2) only.

#### N3. `install.sh` copies **whole** `US/` and `HK/` trees (not flat 02_CODE)
- `tar -C "$HERE/$part"` → `/opt/swing/us` keeps `01_RULES/`, `02_CODE/`, `03_SAMPLE/`.
- Root `verify.sh` correctly uses `$TARGET/us/02_CODE` for regressions. Path model is coherent.

#### N4. Output CSV basenames stay `Contract_US.csv` / `Trigger_US.csv` even on HK
- Historical; HK distinguishes via `verdicts_hk.jsonl` + `runs/hk/`. Confusing but wired through suite.

---

## What would FAIL after a naive `install.sh /opt/swing`?

| Check | Likely result |
|---|---|
| `bash verify.sh /opt/swing` | Likely **PASS** (compile + 29 + 51) if deps installed |
| `bash /opt/swing/hk/verify_hk.sh` | **FAIL** — missing `.swing_market=hk` (B1) |
| `US/scan553.sh …` then cleanup | **FAIL/noisy** — missing `scripts/clean_runs.sh` (B2) unless `KEEP_RAW=1` |
| Story-search open `KB/01_2026全球大趨勢.md` | **FAIL** — file not found (M2) |
| Following `HERMES_HK_MANUAL` `INSTALL_HK.sh` | **FAIL** — script absent (M1) |
| Nested `./02_CODE/run_daily.sh` without bash | May **FAIL** exec bit (M5) |

---

## Recommended fix order (no bot edits in this TC)

1. **B1** write `.swing_market` in `install.sh` (+ ship marker files)
2. **B2** ship or soft-fail `clean_runs.sh`
3. **M2** rename mojibake KB/report files; regenerate MANIFEST
4. **M1** rewrite `HERMES_HK_MANUAL` to this package’s install paths
5. **M5** recursive chmod on `*.sh`
6. **M4/m2/m3** contract bump + V4d label + README grammar
7. Hand to PA for bot/skill plan under **M3** ownership matrix

---

## Out of scope (this TC)

- No install to `/opt/swing`
- No Grok bot / skill edits
- No PA plan authorship (separate deliverable)
