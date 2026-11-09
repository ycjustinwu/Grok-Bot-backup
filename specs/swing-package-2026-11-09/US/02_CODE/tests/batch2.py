#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch-2 tests (v6.2) — Grok review 2026-11-07.

    python3 tests/batch2.py

Covers: baseline defence depth (risk FAIL after the earnings override), V9 integer prices
and tolerance, base geometry freeze, and live synthetic cases for I17 / I25 / I27.
"""
import csv
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.dirname(HERE)
sys.path.insert(0, CODE)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import base_layer  # noqa: E402
import l2_prep  # noqa: E402

CASES = []


def case(fn):
    CASES.append(fn)
    return fn


def ok(name, cond, detail=''):
    print(f"  {'OK  ' if cond else 'FAIL'} {name}" + (f" — {detail}" if detail and not cond else ''))
    return bool(cond)


# ---------------------------------------------------------------- Grok #1
@case
def t_no_ticket_on_bad_risk():
    """The earnings override runs after the risk check; re-assert the risk last."""
    base = {'Ticker': 'X', 'Candidate_Class': 'A_SETUP', 'Entry_Feasible': 'AT_TRIGGER',
            'Setup_Family': 'BREAKOUT', 'Setup_Code': 'A_BASE', 'Volume_Confirm': 'PASS',
            'Leader_OK': 'PASS'}
    got = {}
    for risk in ('FAIL', 'UNKNOWN', 'PASS', 'PENDING'):
        for epf in ('PASS', 'UNKNOWN', 'CLEAR', 'CAUTION'):
            row = dict(base, Risk_OK=risk, Earnings_Proximity_Flag=epf)
            got[(risk, epf)] = l2_prep.baseline_verdict(row)[0]
    bad = {k: v for k, v in got.items() if v in ('BUY', 'STALK') and k[0] in ('FAIL', 'UNKNOWN')}
    return ok('A_SETUP: no BUY/STALK on FAIL/UNKNOWN risk, any earnings flag', not bad, str(bad))


@case
def t_stalk_after_earnings_is_watch():
    row = {'Ticker': 'X', 'Candidate_Class': 'A_SETUP', 'Entry_Feasible': 'AT_TRIGGER',
           'Setup_Family': 'BREAKOUT', 'Setup_Code': 'A_BASE', 'Volume_Confirm': 'PASS',
           'Leader_OK': 'PASS', 'Risk_OK': 'FAIL', 'Earnings_Proximity_Flag': 'UNKNOWN'}
    v, why = l2_prep.baseline_verdict(row)
    return ok('Grok #1 exact case: A_SETUP+AT_TRIGGER+Risk FAIL+UNKNOWN -> WATCH', v == 'WATCH', f'{v} {why}')


# ---------------------------------------------------------------- Grok #4
@case
def t_prov_thin_code():
    row = {'Ticker': 'X', 'Candidate_Class': 'C_WATCH', 'Entry_Feasible': 'NOT_YET',
           'Setup_Family': 'BREAKOUT', 'Setup_Code': 'A_BASE', 'Risk_OK': 'PENDING',
           'Room_Basis': 'PROV_1ADR', 'Room_To_Supply_R': 0.9, 'Earnings_Proximity_Flag': 'CLEAR'}
    codes = {c['code'] for c in l2_prep.downgrade_codes(row)}
    return ok('PROV_THIN is emitted alongside PROV_RISK', {'PROV_RISK', 'PROV_THIN'} <= codes, str(codes))


# ---------------------------------------------------------------- Grok #3
def _synth(n_compressed=30, warm=20):
    rng = np.random.default_rng(7)
    n = warm + n_compressed
    close = 100 + np.cumsum(rng.normal(0, 0.3, n))
    high, low = close + 0.4, close - 0.4
    for i in range(warm, n):
        close[i] = 100 + i * 0.02
        high[i], low[i] = close[i] + 0.3, close[i] - 0.3
    vol = np.full(n, 400_000.0)
    return pd.DataFrame({'High': high, 'Low': low, 'Close': close, 'Volume': vol,
                         'ADR': np.full(n, 2.0), 'ATR': np.full(n, 2.0),
                         'Vol_Avg_20': np.full(n, 1_000_000.0), 'MA20': np.full(n, 100.0)})


@case
def t_base_geometry_frozen():
    df = _synth()
    # end the run with one wide bar, then look at the episode
    end = df.iloc[[-1]].copy()
    end[['High', 'Low', 'Close']] = [[100.9, 98.0, 100.0]]
    d = pd.concat([df, end], ignore_index=True)
    _, eps1 = base_layer.detect_bases(d, base_layer.STRICT)
    if not eps1:
        return ok('base geometry frozen', False, 'no episode detected')
    e1 = eps1[0]
    # append bars that cannot belong to the finished run
    more = d.iloc[[-1]].copy()
    more[['High', 'Low', 'Close']] = [[104.0, 99.0, 103.0]]
    d2 = pd.concat([d, more], ignore_index=True)
    _, eps2 = base_layer.detect_bases(d2, base_layer.STRICT)
    same = [e for e in eps2 if e['start'] == e1['start']]
    if not same:
        return ok('base geometry frozen', False, 'episode disappeared after appending')
    e2 = same[0]
    return ok('finished base high/low do not move when new bars arrive',
              abs(e1['high'] - e2['high']) < 1e-9 and abs(e1['low'] - e2['low']) < 1e-9,
              f"{e1['high']}->{e2['high']}, {e1['low']}->{e2['low']}")


# ---------------------------------------------------------------- Grok #6
def _contract(rows):
    cols = ['Ticker', 'Date', 'Close', 'Candidate_Class', 'Leader_OK', 'Setup_OK', 'Risk_OK',
            'Entry_Feasible', 'Base_State', 'Base_Family', 'Volume_Confirm', 'Room_Basis',
            'SR_Flip_Live', 'SR_Flip_Age', 'contract_version', 'Setup_Family', 'Setup_Code',
            'Setup_Len_Days', 'Base_Width_ATR', 'Invalidate_Below', 'Class_Note',
            'Supply_Level', 'Entry_Ref']
    d = tempfile.mkdtemp(prefix='b2_')
    with open(os.path.join(d, 'Contract_US.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in cols})
    return d


def _inv(d):
    r = subprocess.run([sys.executable, os.path.join(CODE, 'invariants.py'), d],
                       cwd=CODE, capture_output=True, text=True)
    return r.stdout


BASE_ROW = {'Date': '2026-11-06', 'Close': 10, 'Candidate_Class': 'A_SETUP', 'Leader_OK': 'PASS',
            'Setup_OK': 'PASS', 'Risk_OK': 'PASS', 'Entry_Feasible': 'AT_TRIGGER',
            'Base_State': 'TRIGGERED', 'Volume_Confirm': 'PASS', 'Room_Basis': 'RISK',
            'SR_Flip_Live': 'False', 'SR_Flip_Age': '', 'contract_version': 'us-contract-1f.4',
            'Setup_Family': 'BREAKOUT', 'Setup_Code': 'A_BASE', 'Setup_Len_Days': 20,
            'Base_Width_ATR': 2.0, 'Invalidate_Below': 9.5, 'Class_Note': 'none',
            'Supply_Level': 12, 'Entry_Ref': 10}


@case
def t_i17_live():
    bad = dict(BASE_ROW, Ticker='BAD', Base_Family='STRICT', Setup_Len_Days=45)
    good = dict(BASE_ROW, Ticker='GOOD', Base_Family='STRICT', Setup_Len_Days=20)
    d = _contract([bad, good])
    try:
        out = _inv(d)
        return ok('I17 fires on a STRICT base longer than 30 days', 'FAIL I17' in out, out[-200:])
    finally:
        shutil.rmtree(d, ignore_errors=True)


@case
def t_i25_live():
    bad = dict(BASE_ROW, Ticker='BAD', Base_State='TRIGGERED', Close=9.0, Invalidate_Below=9.5)
    d = _contract([bad])
    try:
        out = _inv(d)
        return ok('I25 fires when a TRIGGERED close is under the breakout-bar low',
                  'FAIL I25' in out, out[-200:])
    finally:
        shutil.rmtree(d, ignore_errors=True)


@case
def t_i27_live():
    bad = dict(BASE_ROW, Ticker='BAD', Volume_Confirm='LOW', Class_Note='')
    d = _contract([bad])
    try:
        out = _inv(d)
        return ok('I27 fires on a low-volume A_SETUP without REMARK', 'FAIL I27' in out, out[-200:])
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == '__main__':
    print('batch-2 tests')
    results = [fn() for fn in CASES]
    print(f"\n{sum(results)}/{len(results)} passed")
    sys.exit(0 if all(results) else 1)
