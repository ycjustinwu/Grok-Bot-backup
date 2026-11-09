# TC-20261109-swing-APPLY — Soft Final (package patch + install ONLY)

**Status:** Soft Final — package patched + installed; **NO** CreateAgent / UpdateSkill / bot edits / Scanner wakes  
**TC:** TC-20261109-swing-APPLY  
**Package mirror:** `/workspace/docs/swing-package-2026-11-09/`  
**Install target:** `/opt/swing` (`us` + `hk`)  
**Checked:** 2026-11-09 16:15 HKT (Asia/Hong_Kong)  
**Authorizer:** Justin AUTHORIZE (OQ-Create=install+fallback; apply install phase only for this subagent)

---

## Scope (this Soft Final)

| In | Out |
|---|---|
| B1 / B2 / M5 package patches | CreateAgent / UpdateAgent / UpdateSkill |
| Optional m3 README one-liner | Retire four bots |
| `bash install.sh /opt/swing` | PA SB / 模擬倉 Tradeable patches |
| `bash verify.sh` + `verify_hk.sh` | Wake Scanners / Hermes |

---

## Diffs summary

### B1 — `.swing_market` pin (`install.sh` + shipped markers)

**Choice:** write markers in **both** package trees **and** after copy in `install.sh` (idempotent).

- Shipped: `US/.swing_market` → `us\n`, `HK/.swing_market` → `hk\n`
- `install.sh` after each `tar` copy:
  ```bash
  printf '%s\n' "$low" > "$dest/.swing_market"
  ```
- Post-install: `/opt/swing/us/.swing_market` = `us`, `/opt/swing/hk/.swing_market` = `hk`
- Why needed: HK `markets._install_market()` reads marker next to `markets.py` (HK tree root); without it `verify_hk.sh` step 5b FAILs and solo `run_l2.sh` falls back to US.

### B2 — `US/scan553.sh` missing `scripts/clean_runs.sh`

**Choice: soft-fail** (preferred over shipping a new cleanup script).

- Still honour `KEEP_RAW=1` to skip entirely.
- If `scripts/clean_runs.sh` exists → run it; non-zero ignored with a one-line note.
- If missing → print skip line; scan exit status unchanged (engine/invariants still own exits 0/1/2).
- Also synced EXTRA root `scan553.sh` (not in MANIFEST) so the two copies stay byte-aligned on cleanup logic.
- **Not created:** `US/scripts/clean_runs.sh` (would invent cleanup policy not in package).

### M5 — recursive chmod

`install.sh` now:

```bash
find "$TARGET/us" "$TARGET/hk" -type f -name '*.sh' -exec chmod +x {} +
```

Verified `+x` on `us/scan553.sh`, `us/02_CODE/run_{daily,l2}.sh`, `hk/run_{daily,l2}.sh`, `hk/verify_hk.sh`.

### m3 (optional) — README Tradeable grammar

Hard-rule bullet 1 rewritten to:

> BUY/STALK require `Tradeable=PASS`; FAIL → forced WATCH; …

---

## md5 (patched files)

| File | md5 |
|---|---|
| `install.sh` | `1f2ec5498e916a51fa3c293fdb768161` |
| `US/scan553.sh` | `8c2563592a9580717ce31470c909e888` |
| `README.md` | `e0a5a8b3ae1752b627c43c61d9371c49` |
| `US/.swing_market` | `0afb55fc59cc659b91168ebdf06e1091` |
| `HK/.swing_market` | `121a16741f331ca0e928e2b491281f2f` |

---

## Install + deps

```
cd /workspace/docs/swing-package-2026-11-09
# pip: system env is PEP 668 externally-managed; deps already present:
#   pandas 3.0.5 · numpy 2.5.4 · yfinance 1.7.0 · requests (import OK)
# sudo mkdir -p /opt/swing && chown box:box /opt/swing
bash install.sh /opt/swing
# → installed US -> /opt/swing/us (marker=us)
# → installed HK -> /opt/swing/hk (marker=hk)
```

Layout: full trees (`01_RULES/`, `02_CODE/` for US; flat HK engine at `hk/`).

---

## VERIFY results

### Root `bash verify.sh /opt/swing` → **VERIFY: PASS** (exit 0)

1. python compile — ok  
2. US regressions — **ALL REGRESSIONS PASS** (29 OK lines)  
3. HK suite — **51/51 passed**

### `bash /opt/swing/hk/verify_hk.sh` → **ALL CHECKS PASSED** (exit 0)

| Step | Result |
|---|---|
| 1 compile | OK |
| 2 markets.load('hk') | OK (bench=2800.HK, calendar=XHKG) |
| 3 run_daily reads marker + tickers_hk.txt | OK |
| 4 tickers_hk.txt | OK (39) |
| 5 earnings_overrides.csv | OK (53 rows) |
| **5b .swing_market = hk** | **OK** (B1 fix proven) |
| 5b verdicts_hk.jsonl | OK |
| 6 last run invariants | OK (no run yet) |

---

## Residual (not in this Soft Final)

- M1 HERMES_HK_MANUAL still documents `INSTALL_HK.sh` / `/opt/hk-swing` — docs-only; install path is `/opt/swing/hk`.
- M2 KB mojibake filenames — unchanged.
- M4 HK contract string still `hk-contract-1f.5` vs Tradeable columns — unchanged.
- M3/M6 fleet + fixture naming — owned by PA apply / later bot work.
- CreateAgent install+fallback bot, retire four bots, SB/模擬倉 Tradeable patches — **parent / other agents**; this Soft Final stopped at package+install.

---

## Handoff for parent

- Package ready at `/opt/swing/{us,hk}` with markers + VERIFY PASS.
- B1/B2/M5 closed in mirror + install.
- Safe to proceed with CreateAgent / skill patches / retire **outside** this Soft Final.
