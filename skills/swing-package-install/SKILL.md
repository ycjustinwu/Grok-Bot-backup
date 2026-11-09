---
name: swing-package-install
description: Use when installing or reinstalling /opt/swing from the 2026-11-09 package mirror: patch B1/B2/M5 then install.sh + pip deps.
---
# swing-package-install

ONE JOB: Patch blockers then install US+HK engines under `/opt/swing` from the box mirror. Idempotent; never deletes `runs/`.

## Inputs
- Mirror: `/workspace/docs/swing-package-2026-11-09/` (expect MANIFEST 121/121)
- Target: `/opt/swing` (default)

## Steps
1. Confirm mirror present (`MANIFEST.json`, `install.sh`, `US/`, `HK/`). If incomplete → STOP + escalate.
2. **B1:** Ensure `install.sh` writes `$TARGET/us/.swing_market=us` and `$TARGET/hk/.swing_market=hk` after tar copy. Prefer patching the mirror `install.sh` before install.
3. **B2:** Under `US/`: either ship `scripts/clean_runs.sh` **or** soft-fail in `scan553.sh` (`test -x` before call / allow `KEEP_RAW=1`). Prefer soft-fail if no clean script content is known.
4. **M5:** After install (or in install.sh), recursive `find "$TARGET" -name '*.sh' -exec chmod +x {} +`.
5. `bash install.sh /opt/swing` from the mirror root.
6. `python3 -m pip install -r requirements.txt` (mirror root).
7. Hand off to `swing-package-verify` before any scan.

## VERIFY
- [ ] `.swing_market` files exist and match market
- [ ] Nested `02_CODE/*.sh` executable
- [ ] `scan553.sh` cleanup cannot fail a successful scan solely for missing `clean_runs.sh`
- [ ] `runs/` directories preserved on reinstall
- [ ] No invent tickers/prices; no SB/sim/Story edits

## ANTI
- Do not scan in this skill
- Do not dual-run Hermes-healthy days
- Do not follow obsolete `INSTALL_HK.sh` / `/opt/hk-swing` paths

## HANDOFF
PINNED_INPUTS: mirror path + install target
DECISIONS_MADE: B1/B2/M5 required on apply
OPEN_QUESTIONS: none | list
NEXT_GATE: swing-package-verify → VERIFY: PASS
