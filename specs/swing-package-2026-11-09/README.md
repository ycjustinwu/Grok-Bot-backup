# Swing Package 2026-11-09 — US + HK screener & setup

Two independent engines, same rules, no shared state. Install both or only one; they never import
each other and write to separate verdict files (`verdicts_US.jsonl` / `verdicts_hk.jsonl`).

| Part | Engine | Contract | Columns | Regression |
|---|---|---|---|---|
| `US/` | `us_swing_v55.py` v5.5.4 | `us-contract-1f.6` | 113 | `tests/regressions.py` — 29 cases |
| `HK/` | `us_swing_v55.py` v6.10 (HK profile) | HK contract | 116 | `tests/suite.py` — 51 cases |

Both carry the **Tradeable risk gate** (2026-11-08): a name whose plan stop is wider than
`1.2 × ADR` (or than `max(8%, 1.2 × ADR%)` in percent), or which leaves less than the family's
room floor to that stop, is not a ticket — it becomes WATCH with `Tradeable_Why` filled in.

## Install

```bash
cd swing-package-2026-11-09
python3 -m pip install -r requirements.txt
bash install.sh /opt/swing       # -> /opt/swing/us and /opt/swing/hk
bash verify.sh /opt/swing        # must print VERIFY: PASS
```

`install.sh` never deletes `runs/`; re-installing replaces code only.

## Read in this order

1. `docs/01_INSTALL.md` — prerequisites, paths, what `verify.sh` proves.
2. `docs/02_RUN_US.md` / `docs/03_RUN_HK.md` — the exact commands, in order.
3. `docs/04_GATES_AND_CAPS.md` — every gate, cap and environment variable, with the numbers.
4. `docs/05_HANDOFF_S4_S5.md` — the story JSON contract; this is what an LLM must return.
5. `docs/06_ACCEPTANCE.md` — sample-day expected results; if your numbers differ, stop.

## Hard rules

- **A ticket without a tradeable plan is a defect.** BUY/STALK require `Tradeable=PASS`; FAIL → forced WATCH;
  `invariants` I30 fails if a row in `Trigger_US.csv` is not `Tradeable=PASS`.
- **Stale RS never becomes a FAIL.** If the relative-strength window is stale the LEADER gate is
  downgraded to `UNKNOWN` and the run prints a WARN line naming the tickers.
- **Never scan a list you did not receive.** The US engine has no cron; the universe is supplied per
  request. HK runs only when explicitly triggered.
- **`knowledge/`, `portfolio.md` and any real account data are out of scope for this package.**
