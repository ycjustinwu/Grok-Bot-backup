---
name: crypto-exec-validate
description: Use after crypto-exec-intake — allowlist, per-trade risk, exchange SL, day/total caps, kill-switch hard rejects.
---
# crypto-exec-validate
ONE JOB: Hard-reject unsafe alerts; emit accept or reject sample.
Hard rejects (brief): no allowlist hit; no risk cap or no exchange SL; no day/total cap or kill on; vaultTransfer; non-dedicated account; master key path.
VERIFY: every reject has reason code + logged sample path; accepts carry PINNED fields forward.
ANTI: do not invent Justin risk%; do not bypass kill.
