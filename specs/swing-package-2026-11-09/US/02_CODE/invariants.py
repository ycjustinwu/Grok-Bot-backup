#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Invariant checks for a US swing scan folder (v5.3).

Usage:  python3 invariants.py <run_folder>

These checks prove *internal consistency*, never edge. They never abort a run; the report is
written to <folder>/Invariant_Report.md and run_daily.sh greps for lines starting 'FAIL '.

v5.3 (see CHANGELOG_v53.md)
* I17 checks each A_SETUP breakout against its OWN family limits (STRICT 5-30d / 3.0 ATR,
      WIDE 10-40d / 4.0 ATR). v5.2 applied the strict limits to every row, so any WIDE
      A_SETUP raised a false FAIL and exit code 2.
* I25 a TRIGGERED row must not have closed below its breakout-bar low (BO_FAILED exists).
* I26 hard supply, when present, sits above the entry.
* I27 VOL_MODE=WATCH: no A_SETUP breakout with Volume_Confirm=LOW.
* I28 the long table agrees with the wide one: for every ticker the Evidence rows of each
      block reduce (FAIL > UNKNOWN > PENDING > PASS) to the gate value in the Contract.
* The deprecated zone/RR checks (I4-I9, I13) were removed with the machinery they tested.
"""
import os
import sys

import numpy as np
import pandas as pd

try:
    import base_layer
    LIMITS = {f['name']: (f['min_len'], f['max_len'], f['width_atr_max'])
              for f in (base_layer.STRICT, base_layer.WIDE)}
except Exception:                                   # pragma: no cover
    LIMITS = {'STRICT': (5, 30, 3.0), 'WIDE': (10, 40, 4.0)}

FAIL, WARN, PASS = 'FAIL', 'WARN', 'PASS'
ORDER = {'FAIL': 0, 'UNKNOWN': 1, 'PENDING': 2, 'PASS': 3}


def load(folder):
    path = os.path.join(folder, 'Contract_US.csv')
    if not os.path.exists(path):
        path = os.path.join(folder, 'Summary_US.csv')
    contract = pd.read_csv(path)
    frames = {}
    for base in (folder, os.path.join(folder, 'history'), os.path.join(folder, 'samples')):
        if not os.path.isdir(base):
            continue
        for f in sorted(os.listdir(base)):
            if f.endswith('_SwingAnalysis.csv'):
                frames[f.replace('_SwingAnalysis.csv', '')] = os.path.join(base, f)
    return contract, frames


def parse_breakdown(s):
    if not isinstance(s, str) or not s.strip():
        return None
    total = 0
    for part in s.split('|'):
        part = part.strip()
        if part:
            total += int(part.partition(':')[2])
    return total


def main(folder):
    c, frames = load(folder)
    results = []

    def check(cid, title, status, detail):
        results.append((cid, title, status, detail))

    num = lambda col: pd.to_numeric(c.get(col, pd.Series(np.nan, index=c.index)), errors='coerce')

    # I1 — score equals the sum of its published terms
    if 'Score_Breakdown' in c.columns and 'Priority_Score' in c.columns:
        bad = [f"{r['Ticker']}({parse_breakdown(r['Score_Breakdown'])}!={int(r['Priority_Score'])})"
               for _, r in c.iterrows()
               if parse_breakdown(r.get('Score_Breakdown')) is not None
               and parse_breakdown(r.get('Score_Breakdown')) != int(r['Priority_Score'])]
        check('I1', 'Score_Breakdown sums to Priority_Score', FAIL if bad else PASS,
              ', '.join(bad) if bad else 'all rows reconcile')
    else:
        check('I1', 'Score_Breakdown sums to Priority_Score', WARN, 'column absent')

    # I3 — layer 1 issues no verdict labels
    if 'Screen_Flag' in c.columns:
        bad = c[c['Screen_Flag'].fillna('').isin(['BUY', 'STALK', 'AVOID', 'PASS'])]
        check('I3', 'no verdict labels emitted by layer 1', FAIL if len(bad) else PASS,
              ', '.join(bad['Ticker']) if len(bad) else 'class labels only')

    # I10 / I12 — status columns never silently blank
    for col in ('RS_Status', 'Earnings_Proximity_Flag', 'Screen_Flag', 'Weak_Day_RS_Pct'):
        if col in c.columns:
            n_null = int(c[col].isna().sum())
            check('I10', f'{col} populated', PASS if n_null == 0 else WARN, f'{n_null}/{len(c)} blank')

    # I11 — negative room is a failed gate, never a silent number
    if 'Room_To_Supply_R' in c.columns:
        neg = c[num('Room_To_Supply_R') < 0]
        bad = neg[neg.get('Risk_OK') != 'FAIL'] if len(neg) else neg
        check('I11', 'negative room implies Risk_OK=FAIL', FAIL if len(bad) else PASS,
              f'neg={len(neg)} unexplained={len(bad)}')

    # I14-I16 — class consistency
    if 'Candidate_Class' in c.columns:
        check('I14', 'Candidate_Class populated', FAIL if c['Candidate_Class'].isna().any() else PASS,
              f"{int(c['Candidate_Class'].isna().sum())}/{len(c)} blank")
        a = c[c['Candidate_Class'] == 'A_SETUP']
        bad = a[(a.get('Setup_OK') != 'PASS') | (a.get('Risk_OK') != 'PASS')]
        check('I15', 'A_SETUP implies Setup_OK and Risk_OK', FAIL if len(bad) else PASS,
              ', '.join(bad['Ticker']) if len(bad) else f'{len(a)} A_SETUP rows consistent')
        if 'Base_State' in c.columns:
            nb = c[c['Base_State'].fillna('NONE') == 'NONE']
            bad = nb[nb.get('Setup_OK') == 'PASS']
            check('I16', 'no setup => Setup_OK is not PASS', FAIL if len(bad) else PASS,
                  ', '.join(bad['Ticker']) if len(bad) else 'none')

        # I17 — per-family limits
        ab = a[a.get('Setup_Family', pd.Series('', index=a.index)).fillna('') == 'BREAKOUT']
        bad, warn = [], 0
        for _, r in ab.iterrows():
            fam = str(r.get('Base_Family', '') or '').upper()
            if fam not in LIMITS:
                fam, warn = 'WIDE', warn + 1
            lmin, lmax, wmax = LIMITS[fam]
            ln, wd = pd.to_numeric(r.get('Setup_Len_Days'), errors='coerce'), \
                pd.to_numeric(r.get('Base_Width_ATR'), errors='coerce')
            if (pd.notna(ln) and not (lmin <= ln <= lmax)) or (pd.notna(wd) and wd > wmax):
                bad.append(f"{r['Ticker']}({fam} len={ln} width={wd})")
        check('I17', 'A_SETUP breakout obeys its family limits', FAIL if bad else (WARN if warn else PASS),
              ', '.join(bad) if bad else f'{len(ab)} breakout rows ok'
              + (f'; {warn} without Base_Family (checked as WIDE)' if warn else ''))

    # I18 / I19 — contract shape
    need = ['Ticker', 'Candidate_Class', 'Leader_OK', 'Setup_OK', 'Risk_OK', 'Entry_Feasible',
            'Base_State', 'Base_Family', 'Volume_Confirm', 'Room_Basis',
            'SR_Flip_Live', 'SR_Flip_Age', 'contract_version']
    missing = [x for x in need if x not in c.columns]
    check('I18', 'Contract has the filterable fields', FAIL if missing else PASS,
          f'missing={missing}' if missing else f'{len(c)} rows x {len(c.columns)} cols')
    check('I19', 'Contract rows carry a ticker', FAIL if c['Ticker'].isna().any() else PASS,
          f"{int(c['Ticker'].isna().sum())} blank")

    # I29 — no status value may be one pandas NA token (v5.4; fixed v6.1)
    #
    # The first version read the contract through load(), where pandas had already turned a
    # literal "NA" into NaN, so the bug it was written to catch was invisible to it.
    # It now re-reads the raw CSV with keep_default_na=False and inspects status columns only.
    NA_TOKENS = {'NA', 'N/A', 'NULL', 'NaN', 'None', 'nan', '', 'null', '#N/A'}
    status_cols = [x for x in ('Leader_OK', 'Setup_OK', 'Risk_OK', 'Candidate_Class',
                               'Screen_Flag', 'Entry_Feasible', 'Setup_Family', 'Setup_Code',
                               'Base_State', 'BaseS_State', 'BaseW_State', 'Volume_Confirm',
                               'RS_Status', 'Earnings_Proximity_Flag', 'Supply_Source',
                               'Regime_State', 'Stop_Type_Plan', 'Room_Basis')
                   if x in c.columns]
    bad = {}
    raw_path = os.path.join(folder, 'Contract_US.csv')
    if not os.path.exists(raw_path):
        raw_path = os.path.join(folder, 'Summary_US.csv')
    try:
        raw = pd.read_csv(raw_path, keep_default_na=False, dtype=str)
        for col in status_cols:
            if col not in raw.columns:
                continue
            hits = sorted({str(v).strip() for v in raw[col]} & NA_TOKENS)
            if hits:
                bad[col] = hits
    except Exception as exc:
        bad['_read'] = [str(exc)[:80]]
    check('I29', 'no status value is a pandas NA token', FAIL if bad else PASS,
          str(bad) if bad else f'{len(status_cols)} status columns clean (raw read)')

    # I20 / I21 / I30 — tickets
    trg_path = os.path.join(folder, 'Trigger_US.csv')
    if os.path.exists(trg_path):
        trg = pd.read_csv(trg_path)
        allowed = {'NOT_YET', 'AT_TRIGGER', 'NEXT_DAY', 'LATE', 'AT_MARKET'}
        bad = trg[~trg['Entry_Feasible'].isin(allowed)]
        check('I20', 'Trigger rows are actionable states', FAIL if len(bad) else PASS, f'{len(trg)} tickets')
        inv = int((pd.to_numeric(trg['Invalidate_Below'], errors='coerce') >=
                   pd.to_numeric(trg['Entry_Ref'], errors='coerce')).sum())
        check('I21', 'stop below entry on every ticket', FAIL if inv else PASS, f'{inv} tickets with stop >= entry')
        # I30 (2026-11-07): risk is a gate. A ticket without Tradeable=PASS is the defect Hermes
        # found — 19 tickets where 16 carried Risk_OK=FAIL and 16 were above 1.2xADR.
        if 'Tradeable' in trg.columns:
            nt = trg[trg['Tradeable'].astype(str) != 'PASS']
            check('I30', 'every ticket is Tradeable=PASS', FAIL if len(nt) else PASS,
                  ', '.join(nt['Ticker'].astype(str)) if len(nt) else f'{len(trg)} tickets tradeable')
        else:
            check('I30', 'Tradeable column present on tickets', WARN, 'column absent')
    else:
        check('I20', 'Trigger_US.csv present', WARN, 'no actionable ticket on this date (expected some days)')
        check('I30', 'no ticket, nothing to be untradeable', PASS, '0 tickets')

    # I22 / I23 — families
    if 'Setup_Family' in c.columns:
        ok = c['Setup_Family'].fillna('NONE').isin(['BREAKOUT', 'PULLBACK', 'REVERSAL', 'NONE'])
        check('I22', 'Setup_Family in {BREAKOUT, PULLBACK, REVERSAL, NONE}', PASS if ok.all() else FAIL,
              f'{int((~ok).sum())} bad')
        a = c[c.get('Candidate_Class') == 'A_SETUP']
        bad = a[a['Setup_Family'].fillna('NONE') == 'NONE']
        check('I23', 'A_SETUP has a named family', FAIL if len(bad) else PASS,
              ', '.join(bad['Ticker']) if len(bad) else f'{len(a)} ok')

    # I24 — regime is a valid header value
    if 'Regime_State' in c.columns:
        ok = c['Regime_State'].fillna('').isin(['MOMENTUM', 'NEUTRAL', 'FLATTENING', 'RISK_OFF', 'UNKNOWN'])
        check('I24', 'Regime_State valid', PASS if ok.all() else WARN,
              str(c['Regime_State'].value_counts().to_dict()))

    # I25 — a TRIGGERED row has not closed below its breakout-bar low
    if {'Base_State', 'Close', 'Invalidate_Below'} <= set(c.columns):
        t = c[c['Base_State'] == 'TRIGGERED']
        bad = t[num('Close').loc[t.index] < num('Invalidate_Below').loc[t.index]]
        check('I25', 'TRIGGERED never below the breakout-bar low', FAIL if len(bad) else PASS,
              ', '.join(bad['Ticker']) if len(bad) else f'{len(t)} triggered rows ok')

    # I26 — supply above entry
    if {'Supply_Level', 'Entry_Ref'} <= set(c.columns):
        s, e = num('Supply_Level'), num('Entry_Ref')
        bad = c[(s.notna()) & (e.notna()) & (s <= e)]
        check('I26', 'hard supply sits above the entry', FAIL if len(bad) else PASS,
              ', '.join(bad['Ticker']) if len(bad) else f'{int(s.notna().sum())} rows with supply')

    # I27 — low breakout volume never A_SETUP unless REMARK mode
    if {'Volume_Confirm', 'Class_Note'} <= set(c.columns):
        a = c[(c['Candidate_Class'] == 'A_SETUP') & (c['Volume_Confirm'] == 'LOW')]
        note_txt = a['Class_Note'].fillna('').astype(str)
        bad = a[~note_txt.str.contains('REMARK')]
        check('I27', 'low-volume breakout is not A_SETUP (WATCH mode)', FAIL if len(bad) else PASS,
              ', '.join(bad['Ticker']) if len(bad) else f'{len(a)} REMARK rows')

    # I28 — evidence long table reduces to the contract gates
    ev_path = os.path.join(folder, 'Evidence_US.csv')
    if os.path.exists(ev_path):
        ev = pd.read_csv(ev_path)
        gate_of = {'LEADER': 'Leader_OK', 'SETUP': 'Setup_OK', 'RISK': 'Risk_OK'}
        red = (ev[ev['Block'].isin(gate_of)]
               .assign(_o=lambda d: d['Status'].map(ORDER))
               .groupby(['Ticker', 'Block'])['_o'].min().reset_index())
        inv_order = {v: k for k, v in ORDER.items()}
        bad = []
        cc = c.set_index('Ticker')
        for _, r in red.iterrows():
            if r['Ticker'] in cc.index:
                want = cc.at[r['Ticker'], gate_of[r['Block']]]
                got = inv_order.get(r['_o'])
                if want != got:
                    bad.append(f"{r['Ticker']}/{r['Block']}({got}!={want})")
        check('I28', 'Evidence reduces to the Contract gates', FAIL if bad else PASS,
              ', '.join(bad[:10]) if bad else f'{red["Ticker"].nunique()} tickers reconcile')
    else:
        check('I28', 'Evidence_US.csv present', WARN, 'not written')

    lines = [f'# Invariant report — {folder}', '',
             'Internal consistency only. This is not a profitability test.', '',
             '| ID | Check | Status | Detail |', '|---|---|---|---|']
    lines += [f'| {cid} | {title} | **{status}** | {detail} |' for cid, title, status, detail in results]
    out = os.path.join(folder, 'Invariant_Report.md')
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')
    width = max(len(t) for _, t, _, _ in results) + 2
    for cid, title, status, detail in results:
        print(f'{status:4} {cid:4} {title.ljust(width)} {detail}')
    print(f'\nwrote {out}')
    return results


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
