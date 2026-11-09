# 01 — Install

## Prerequisites

- Python **3.11+** (`python3 --version`). The engines use only stdlib + pandas/numpy/yfinance.
- Network access to Yahoo Finance (yfinance) — that is the only external dependency at runtime.
- **No API key, no login, no token.** Nothing in this package authenticates anywhere.

```bash
python3 -m pip install -r requirements.txt
```

## Install

```bash
bash install.sh /opt/swing
```

Creates:

```
/opt/swing/us/          # US engine (v5.5.4, us-contract-1f.6, 113 columns)
/opt/swing/hk/          # HK engine (v6.10, 116 columns)
```

`install.sh` is idempotent: it replaces code and never touches an existing `runs/` directory.
To install only one side, copy `US/` or `HK/` and skip the other — they share no imports.

## Verify (do not proceed until this prints PASS)

```bash
bash verify.sh /opt/swing
```

Expected output:

```
== 2. US regressions (expect ALL PASSED, 29 cases)
   ALL PASSED (29 regressions)
== 3. HK suite (expect 51/51 passed)
   51/51 passed
VERIFY: PASS
```

If either suite fails, the install is wrong — do not run a scan and do not report verdicts.

## Paths the scripts use

| Variable | Meaning | Default |
|---|---|---|
| `SWING_HOME` | replaces the box-specific `/opt/data` HOME the original scripts assumed | `$HOME` |
| `SWING_ROOT` | root used inside the scripts where `/opt/data` was hard-coded | `$PWD` |
| `SWING_OUTPUT_FOLDER` | run directory | `runs/run_<YYYYMMDD>` (US), `runs/hk/run_<YYYYMMDD>` (HK) |

## What is deliberately NOT in this package

`runs/`, `__pycache__`, `*.bak-*`, and any account/portfolio data. The engines produce all of that
on your own machine.
