# Swing Package 2026-11-09 — INVENTORY

**Mirrored to:** `/workspace/docs/swing-package-2026-11-09/`  
**Built:** 2026-11-09 (Asia/Hong_Kong)  
**Inventoried:** 2026-11-09 16:10 HKT (Asia/Hong_Kong)  
**MANIFEST sha check:** 121/121 OK

## Counts

| Area | Files (MANIFEST) | Notes |
|---|---:|---|
| US/ | 69 | rules + code + sample + manuals |
| HK/ | 42 | flat code + rules + tests + manuals |
| docs/ | 6 | 01–06 |
| root | 4 | README, install.sh, verify.sh, requirements.txt |
| **Total** | **121** | + MANIFEST.json on disk |

## Versions

| Side | Engine file | Bytes | Contract | Regressions |
|---|---|---:|---|---|
| US | `US/02_CODE/us_swing_v55.py` | 75314 | `us-contract-1f.6` (113 cols) | `tests/regressions.py` — 29 |
| HK | `HK/us_swing_v55.py` | 79859 | code still `hk-contract-1f.5` (116 cols, Tradeable present) | `tests/suite.py` — 51 |

## Top entrypoints

| Path | Role |
|---|---|
| `install.sh` | Copy `US/`→`$TARGET/us`, `HK/`→`$TARGET/hk` |
| `verify.sh` | Compile + US regressions + HK suite → `VERIFY: PASS` |
| `US/scan553.sh` | Ad-hoc US scan + L2 prep (portable patch) |
| `US/verify_install.sh` | Deep US offline verify (Python≥3.11, sample invariants, V4/I30) |
| `US/02_CODE/run_daily.sh` / `run_l2.sh` | Hermes-style US daily / L2 |
| `HK/run_daily.sh` / `run_l2.sh` | HK daily / L2 (needs `.swing_market=hk`) |
| `HK/verify_hk.sh` | HK install verify |
| `US/HERMES_MANUAL.md` / `HK/HERMES_HK_MANUAL.md` | Operator manuals (Hermes-shaped) |
| `docs/01_INSTALL.md` … `06_ACCEPTANCE.md` | Canonical operator docs |
| `US/01_RULES/story_search/SKILL.md` | Story-search skill (KB mojibake caveat) |

## Tree sketch

```
swing-package-2026-11-09/
  README.md  install.sh  verify.sh  requirements.txt  MANIFEST.json
  docs/01..06
  US/
    HERMES_MANUAL.md  PATCH_NOTES_v5.5.4.md  scan553.sh  verify_install.sh …
    01_RULES/  (+ story_search/KB + references)
    02_CODE/   (engine + gates + tests)
    03_SAMPLE/run_v56/
  HK/
    HERMES_HK_MANUAL.md  PATCH_NOTES_v6.10.md  verify_hk.sh
    01_RULES/  handoff/  tests/sample/  *.py  us_swing_v55.py
```

## Tradeable gate (both sides)

- `risk ≤ 1.2×ADR`
- `risk% ≤ max(8%, 1.2×ADR%)`
- room / room@plan stop ≥ family floor
- FAIL → forced WATCH; Trigger only `Tradeable=PASS`; I30 + V4d/V4c enforce

## Known extras on disk (not MANIFEST)

- `scan553.sh` (root duplicate from chat attach)
- `_backup_partial/` (pre-Drive chat docs)
- `_tools/drive_index.json`, `download_queue.json`, `sha_report.json`
- `INVENTORY.md`, `TC-20261109-swing-BUGCHECK.md`
