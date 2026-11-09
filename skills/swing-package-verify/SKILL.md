---
name: swing-package-verify
description: Use after swing-package-install (or before any fallback scan) to run root verify.sh and hk/verify_hk.sh; FAIL stops scans.
---
# swing-package-verify

ONE JOB: Prove `/opt/swing` is safe to run. No scan if FAIL.

## Steps
1. `bash verify.sh /opt/swing` from package root — must print `VERIFY: PASS` (US 29 + HK 51).
2. `bash /opt/swing/hk/verify_hk.sh` — ALL CHECKS PASSED (needs `.swing_market=hk`).
3. Spot-check Contract expectations: US `us-contract-1f.6` / 113 cols with Tradeable*; HK v6.10 / 116 cols with Tradeable* (do not invent values).
4. Log under `/workspace/swing-package-ops/logs/YYYYMMDD-verify.txt`.
5. On FAIL → escalate to 總指揮/Justin; **do not** run fallback scan.

## VERIFY
- [ ] Root VERIFY: PASS line present
- [ ] verify_hk PASS (B1 marker)
- [ ] Log path written
- [ ] No scan attempted on FAIL
- [ ] No fabricated suite counts

## HANDOFF
PINNED_INPUTS: `/opt/swing` + verify log path
DECISIONS_MADE: Soft Final=Final; WV skip
OPEN_QUESTIONS: none | FAIL detail
NEXT_GATE: if PASS and Hermes-down declare → swing-package-fallback; else idle
