# 06 — Acceptance: prove the install before trusting an output

Run top to bottom. Any mismatch means stop and fix the install, not the report.

## A. Code

```bash
bash verify.sh /opt/swing
```
- [ ] `VERIFY: PASS`
- [ ] US: `ALL PASSED (29 regressions)`
- [ ] HK: `51/51 passed`

## B. Contract shape

```bash
head -1 /opt/swing/us/02_CODE/run_*/Contract_US.csv | tr ',' '\n' | wc -l    # 113
head -1 /opt/swing/hk/runs/hk/run_*/Contract_US.csv | tr ',' '\n' | wc -l    # 116
grep -c . /opt/swing/hk/tickers_hk.txt                                       # 41 lines = 39 codes + 2 comments
grep -c . /opt/swing/hk/earnings_overrides.csv                               # 54 lines = 53 data rows + header
```

- [ ] US 113 columns, HK 116 columns, both contain `Tradeable` and `Tradeable_Why`
- [ ] HK overrides still has 54 lines / 53 data rows (the installer bug that collapses it to one template row must not recur)

## C. Reference run — US, 44 names, as_of 2026-11-06

```
BUY 1   WATCH 26   AVOID 17           Trigger_US.csv: 1 row (DNA 11.29 / 9.92)
```
- [ ] No STALK rows
- [ ] Every `Trigger_US.csv` row has `Tradeable=PASS`
- [ ] `check_verdict` exits 0 once stories + verdicts exist; a missing `verdicts_US.jsonl` must exit 2

## D. Reference run — HK, 39 names, as_of 2026-11-06

```
BUY 2 (6862, 0386)   WATCH 14   AVOID 23       tickets 2
2269.HK -> WATCH, Tradeable_Why = risk=2.72xADR > 1.2; risk=17.3% > 8%; room@plan stop=0.63R < 1.5
```
- [ ] 2269 is WATCH, not STALK
- [ ] `invariants` shows `I30 every ticket is Tradeable=PASS 2 tickets tradeable`
- [ ] `bash verify_hk.sh` prints `ALL CHECKS PASSED` with 24 invariants

## E. Behavioural checks (5 minutes, catches the dangerous regressions)

1. Set `SWING_RISK_ADR_CAP=0.5` and re-run S3 on the same run → most BUY/STALK rows must demote.
   If nothing changes, the gate is not being read (check you passed ADR **in percent**, not as an
   absolute price distance — that mistake silently collapses the cap and produces an identical file).
2. Point `tickers.txt` at a name with no data → the run must fail loudly, not emit a row of zeros.
3. Delete `verdicts_US.jsonl` → `run_l2.sh check` must exit 2 and the render must say there is nothing
   to send.
4. Open `index.md` → no portfolio, no account, no position size of the operator's own book.
