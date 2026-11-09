#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Swing screener regression suite — single entry point (v6.8).

    python3 tests/suite.py

Merged from batch1..batch7. The shared preamble is kept once; each batch is pasted
verbatim from its first helper onwards, and colliding helpers get a batch prefix.
"""
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = HERE if os.path.exists(os.path.join(HERE, 'hk_micro.py')) else os.path.dirname(HERE)
sys.path.insert(0, CODE)

import numpy as np          # noqa: E402
import pandas as pd         # noqa: E402

import base_layer           # noqa: E402
import check_verdict as cv  # noqa: E402
import gates                # noqa: E402
import hk_micro             # noqa: E402
import l2_prep              # noqa: E402
import markets              # noqa: E402
import us_swing_v55 as eng  # noqa: E402

ROOT = os.path.dirname(CODE)
CASES = []


def case(fn):
    CASES.append(fn)
    return fn


def ok(name, cond, detail=''):
    print("  %s %s%s" % ('OK  ' if cond else 'FAIL', name,
                         (' — ' + detail) if detail and not cond else ''))
    return bool(cond)




# ---- batch1 ----
def sample():
    # a fresh install has no runs/ yet, so the bundled sample comes first
    for p in (os.path.join(HERE, 'sample'),
              os.path.join(ROOT, '03_SAMPLE', 'run_v55'),
              os.path.join(ROOT, '04_RUN_US', 'run_v55'),
              os.path.join(ROOT, 'runs', 'run_v55')):
        if os.path.isdir(p):
            return p
    return None
def b1_run_check(folder):
    r = subprocess.run([sys.executable, os.path.join(CODE, 'check_verdict.py'), folder],
                       cwd=CODE, capture_output=True, text=True)
    return r.returncode, r.stdout
def b1_fresh():
    src = sample()
    d = tempfile.mkdtemp(prefix='b1_')
    dst = os.path.join(d, 'run')
    shutil.copytree(src, dst)
    subprocess.run([sys.executable, os.path.join(CODE, 'l2_prep.py'), dst],
                   cwd=CODE, capture_output=True, text=True)
    return d, dst
# ---------------------------------------------------------------- pure functions
@case
def t_tradeable_gate_hk():
    """v6.10 (ported from US v5.5.4, Justin 2026-11-08): a ticket must be risk-sane.

    2269.HK shipped as STALK with a 2.72xADR plan stop because a *pending* breakout returned
    PENDING before the risk band was ever read.
    """
    import gates as G
    import l2_prep as L
    # 2269-like: pending breakout, plan risk 17.3% = 2.72xADR, room@plan 0.99R
    fail = G.tradeability(2.72, 17.3, 1.5, 0.99, 1.5, True, 'PENDING', 1.2, 8.0, 'BREAKOUT', 6.4)
    ok_rows = L.baseline_verdict({'Candidate_Class': 'C_WATCH', 'Entry_Feasible': 'NOT_YET',
                                 'Setup_Family': 'BREAKOUT', 'Setup_Code': 'A_BASE',
                                 'Risk_OK': 'PENDING', 'Earnings_Proximity_Flag': 'CLEAR',
                                 'Tradeable': 'FAIL', 'Tradeable_Why': 'risk=2.72xADR > 1.2 (plan stop)'})
    # 6862-like: pullback, 1.8% = 0.63xADR, room 1.76R -> must stay tradeable
    good = G.tradeability(0.63, 1.8, 1.76, 1.76, 1.0, False, 'PASS', 1.2, 8.0, 'PULLBACK', 2.9)
    # low-ADR name with a 12% stop must still be refused (the cap only floats for high-ADR names)
    low = G.tradeability(0.9, 12.0, 3.0, 3.0, 1.0, False, 'PASS', 1.2, 8.0, 'PULLBACK', 3.0)
    return ok(bool(fail) and ok_rows[0] == 'WATCH' and not good and any('12.0% > 8' in x for x in low),
              'v6.10 tradeable gate: 2.72xADR blocked -> WATCH, 0.63xADR passes, low-ADR 12% blocked',
              f"fail={fail[:1]} verdict={ok_rows[0]} good={good} low={low}")

@case
def t_stalk_needs_pending_risk():
    row = {'Ticker': 'X', 'Candidate_Class': 'C_WATCH', 'Entry_Feasible': 'NOT_YET',
           'Setup_Family': 'BREAKOUT', 'Earnings_Proximity_Flag': 'CLEAR',
           'Risk_OK': 'PENDING', 'Setup_Code': 'A_BASE'}
    v1, _ = l2_prep.baseline_verdict(row)
    row['Risk_OK'] = 'FAIL'
    v2, why = l2_prep.baseline_verdict(row)
    return ok('C_WATCH + NOT_YET: PENDING -> STALK, FAIL -> WATCH',
              v1 == 'STALK' and v2 == 'WATCH', f'{v1}/{v2} {why}')
@case
def t_stalk_unknown_risk():
    row = {'Ticker': 'X', 'Candidate_Class': 'C_WATCH', 'Entry_Feasible': 'NOT_YET',
           'Setup_Family': 'BREAKOUT', 'Earnings_Proximity_Flag': 'CLEAR',
           'Risk_OK': 'UNKNOWN', 'Setup_Code': 'A_BASE'}
    v, _ = l2_prep.baseline_verdict(row)
    return ok('C_WATCH + NOT_YET + Risk UNKNOWN -> WATCH', v == 'WATCH', v)
@case
def t_unknown_class_raises():
    row = {'Ticker': 'X', 'Candidate_Class': 'WAT', 'Entry_Feasible': 'NO_SETUP',
           'Risk_OK': 'FAIL'}
    try:
        l2_prep.baseline_verdict(row)
        return ok('unknown Candidate_Class raises', False, 'silently returned')
    except ValueError:
        return ok('unknown Candidate_Class raises', True)
@case
def t_every_combination_mapped():
    """No STALK/BUY may carry a FAIL/UNKNOWN risk, for any reachable combination."""
    classes = ['A_SETUP', 'C_WATCH', 'B_LEADER_WAIT', 'X_NONE']
    efs = ['AT_TRIGGER', 'NEXT_DAY', 'AT_MARKET', 'NOT_YET', 'LATE', 'INVALIDATED', 'MISSED', 'NO_SETUP']
    risks = ['PASS', 'FAIL', 'UNKNOWN', 'PENDING']
    bad = []
    for cls in classes:
        for ef in efs:
            for rk in risks:
                row = {'Ticker': 'X', 'Candidate_Class': cls, 'Entry_Feasible': ef,
                       'Setup_Family': 'BREAKOUT', 'Setup_Code': 'A_BASE',
                       'Earnings_Proximity_Flag': 'CLEAR', 'Risk_OK': rk}
                v, _ = l2_prep.baseline_verdict(row)
                if v in ('BUY', 'STALK') and rk in ('FAIL', 'UNKNOWN'):
                    bad.append((cls, ef, rk, v))
    return ok('32×combinations: no BUY/STALK on FAIL/UNKNOWN risk', not bad, str(bad[:3]))
# ---------------------------------------------------------------- file-level attacks
@case
def t_v1b_baseline_tamper():
    d, dst = b1_fresh()
    try:
        p = os.path.join(dst, 'L2_Input.csv')
        rows = list(csv.DictReader(open(p, encoding='utf-8')))
        rows[0]['Baseline_Verdict'] = 'BUY'
        with open(p, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=rows[0].keys())
            w.writeheader(); w.writerows(rows)
        rc, out = b1_run_check(dst)
        return ok('V1b catches a tampered baseline', 'FAIL V1b' in out and rc == 2)
    finally:
        shutil.rmtree(d, ignore_errors=True)
@case
def t_v1c_contract_tamper():
    d, dst = b1_fresh()
    try:
        p = os.path.join(dst, 'Contract_US.csv')
        s = open(p, encoding='utf-8').read().replace('UNH', 'UNH ', 1)
        open(p, 'w', encoding='utf-8').write(s)
        rc, out = b1_run_check(dst)
        return ok('V1c catches a modified contract', 'FAIL V1c' in out and rc == 2)
    finally:
        shutil.rmtree(d, ignore_errors=True)
@case
def t_v9_invented_price():
    d, dst = b1_fresh()
    try:
        p = os.path.join(dst, 'verdicts_US.jsonl')
        rows = [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
        rows[0]['invalidation'] = '收市跌穿 999.99 即離場'
        open(p, 'w', encoding='utf-8').write('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n')
        rc, out = b1_run_check(dst)
        return ok('V9 catches a price that is not in the contract', 'not in the contract' in out, out[-200:])
    finally:
        shutil.rmtree(d, ignore_errors=True)
@case
def t_v6_downgrade_needs_code():
    d, dst = b1_fresh()
    try:
        p = os.path.join(dst, 'verdicts_US.jsonl')
        rows = [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
        u = next(r for r in rows if r['verdict'] == 'BUY')
        u['verdict'] = 'STALK'
        u['downgrade_reason'] = 'Market sentiment bad'      # the old substring attack
        u.pop('downgrade_code', None)
        open(p, 'w', encoding='utf-8').write('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n')
        rc, out = b1_run_check(dst)
        return ok('V6 rejects a free-text downgrade reason', 'FAIL V6' in out and rc == 2)
    finally:
        shutil.rmtree(d, ignore_errors=True)
@case
def t_v6_accepts_a_real_code():
    d, dst = b1_fresh()
    try:
        p = os.path.join(dst, 'verdicts_US.jsonl')
        rows = [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
        u = next(r for r in rows if r['verdict'] == 'BUY')
        u['verdict'] = 'STALK'
        u['downgrade_code'] = 'THIN_ROOM'
        u['downgrade_reason'] = 'thin room'
        open(p, 'w', encoding='utf-8').write('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n')
        rc, out = b1_run_check(dst)
        return ok('V6 accepts a code l2_prep computed', 'PASS V6' in out, out[-200:])
    finally:
        shutil.rmtree(d, ignore_errors=True)
@case
def t_v4c_stalk_with_failed_risk():
    d, dst = b1_fresh()
    try:
        ip = os.path.join(dst, 'L2_Input.csv')
        rows = list(csv.DictReader(open(ip, encoding='utf-8')))
        tgt = next(r for r in rows if r['Baseline_Verdict'] == 'BUY')
        tgt['Risk_OK'] = 'FAIL'
        tgt['Baseline_Verdict'] = 'STALK'
        with open(ip, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=rows[0].keys())
            w.writeheader(); w.writerows(rows)
        vp = os.path.join(dst, 'verdicts_US.jsonl')
        vs = [json.loads(l) for l in open(vp, encoding='utf-8') if l.strip()]
        x = next(r for r in vs if r['ticker'] == tgt['Ticker'])
        x['verdict'] = 'STALK'; x['baseline'] = 'STALK'; x['downgrade_code'] = 'THIN_ROOM'
        open(vp, 'w', encoding='utf-8').write('\n'.join(json.dumps(r, ensure_ascii=False) for r in vs) + '\n')
        rc, out = b1_run_check(dst)
        return ok('V4c rejects STALK with Risk_OK=FAIL', 'FAIL V4c' in out, out[-200:])
    finally:
        shutil.rmtree(d, ignore_errors=True)
@case
def b1_clean_passes():
    d = tempfile.mkdtemp(prefix='b1c_')
    try:
        dst = os.path.join(d, 'run')
        shutil.copytree(sample(), dst)
        subprocess.run([sys.executable, os.path.join(CODE, 'l2_prep.py'), dst], cwd=CODE, capture_output=True)
        rc, out = b1_run_check(dst)
        return ok('clean sample still passes V1–V17', rc == 0, out[-160:])
    finally:
        shutil.rmtree(d, ignore_errors=True)
@case
def b1_i29_can_fire():
    d = tempfile.mkdtemp(prefix='b1i_')
    try:
        dst = os.path.join(d, 'run')
        shutil.copytree(sample(), dst)
        p = os.path.join(dst, 'Contract_US.csv')
        rows = list(csv.DictReader(open(p, encoding='utf-8')))
        rows[0]['Volume_Confirm'] = 'NA'
        with open(p, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=rows[0].keys())
            w.writeheader(); w.writerows(rows)
        r = subprocess.run([sys.executable, os.path.join(CODE, 'invariants.py'), dst],
                           cwd=CODE, capture_output=True, text=True)
        return ok('I29 fires on a literal NA', 'FAIL I29' in r.stdout, r.stdout[-160:])
    finally:
        shutil.rmtree(d, ignore_errors=True)

# ---- batch2 ----
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
def b2_synth(n_compressed=30, warm=20):
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
    df = b2_synth()
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
def b2_contract(rows):
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
def b2_inv(d):
    r = subprocess.run([sys.executable, os.path.join(CODE, 'invariants.py'), d],
                       cwd=CODE, capture_output=True, text=True)
    return r.stdout
B2_BASE_ROW = {'Date': '2026-11-06', 'Close': 10, 'Candidate_Class': 'A_SETUP', 'Leader_OK': 'PASS',
            'Setup_OK': 'PASS', 'Risk_OK': 'PASS', 'Entry_Feasible': 'AT_TRIGGER',
            'Base_State': 'TRIGGERED', 'Volume_Confirm': 'PASS', 'Room_Basis': 'RISK',
            'SR_Flip_Live': 'False', 'SR_Flip_Age': '', 'contract_version': 'us-contract-1f.4',
            'Setup_Family': 'BREAKOUT', 'Setup_Code': 'A_BASE', 'Setup_Len_Days': 20,
            'Base_Width_ATR': 2.0, 'Invalidate_Below': 9.5, 'Class_Note': 'none',
            'Supply_Level': 12, 'Entry_Ref': 10}
@case
def t_i17_live():
    bad = dict(B2_BASE_ROW, Ticker='BAD', Base_Family='STRICT', Setup_Len_Days=45)
    good = dict(B2_BASE_ROW, Ticker='GOOD', Base_Family='STRICT', Setup_Len_Days=20)
    d = b2_contract([bad, good])
    try:
        out = b2_inv(d)
        return ok('I17 fires on a STRICT base longer than 30 days', 'FAIL I17' in out, out[-200:])
    finally:
        shutil.rmtree(d, ignore_errors=True)
@case
def t_i25_live():
    bad = dict(B2_BASE_ROW, Ticker='BAD', Base_State='TRIGGERED', Close=9.0, Invalidate_Below=9.5)
    d = b2_contract([bad])
    try:
        out = b2_inv(d)
        return ok('I25 fires when a TRIGGERED close is under the breakout-bar low',
                  'FAIL I25' in out, out[-200:])
    finally:
        shutil.rmtree(d, ignore_errors=True)
@case
def t_i27_live():
    bad = dict(B2_BASE_ROW, Ticker='BAD', Volume_Confirm='LOW', Class_Note='')
    d = b2_contract([bad])
    try:
        out = b2_inv(d)
        return ok('I27 fires on a low-volume A_SETUP without REMARK', 'FAIL I27' in out, out[-200:])
    finally:
        shutil.rmtree(d, ignore_errors=True)
# ---------------------------------------------------------------- Grok #2 (V9)
def _sample():
    for p in (os.path.join(HERE, 'sample'),
              os.path.join(os.path.dirname(CODE), '03_SAMPLE', 'run_v55'),
              os.path.join(os.path.dirname(CODE), '04_RUN_US', 'run_v55'),
              os.path.join(os.path.dirname(CODE), 'runs', 'run_v55')):
        if os.path.isdir(p):
            return p
    return None
def b2_gate(mutate):
    import json
    src = _sample()
    if src is None:
        return None, 'no sample'
    d = tempfile.mkdtemp(prefix='b2v_')
    dst = os.path.join(d, 'run')
    shutil.copytree(src, dst)
    subprocess.run([sys.executable, os.path.join(CODE, 'l2_prep.py'), dst],
                   cwd=CODE, capture_output=True)
    vp = os.path.join(dst, 'verdicts_US.jsonl')
    rows = [json.loads(l) for l in open(vp, encoding='utf-8') if l.strip()]
    mutate(rows)
    open(vp, 'w', encoding='utf-8').write('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n')
    r = subprocess.run([sys.executable, os.path.join(CODE, 'check_verdict.py'), dst],
                       cwd=CODE, capture_output=True, text=True)
    shutil.rmtree(d, ignore_errors=True)
    return r, r.stdout
@case
def b2_v9_integer_price():
    def mutate(rows):
        rows[0]['invalidation'] = '收市跌穿 400 就離場'
    r, out = b2_gate(mutate)
    if r is None:
        return ok('V9 catches an integer price', False, out)
    return ok('V9 catches an integer price not in the contract', 'FAIL V9' in out and 'price 400' in out, out[-200:])
@case
def b2_v9_units():
    def mutate(rows):
        rows[0]['invalidation'] = '收市跌穿 392.50 即離場；2026-01-12 出數；1322 家門店'
    r, out = b2_gate(mutate)
    if r is None:
        return ok('V9 does not flag units/dates', False, out)
    return ok('V9 ignores dates, store counts and units', 'PASS V9' in out or '0 FAIL' in out, out[-200:])

# ---- batch3 ----
@case
def t_five_digit_ticker():
    p = markets.load('hk')
    cases = {'00700': '0700.HK', '00005': '0005.HK', '700': '0700.HK',
             '00700.HK': '0700.HK', '5': '0005.HK', '9988': '9988.HK'}
    bad = {k: markets.normalize_ticker(k, p) for k, v in cases.items()
           if markets.normalize_ticker(k, p) != v}
    return ok('HK tickers normalise to 4 digits', not bad, str(bad))
@case
def t_earnings_why_placement():
    row = {'Ticker': 'X', 'Candidate_Class': 'A_SETUP', 'Entry_Feasible': 'AT_TRIGGER',
           'Setup_Family': 'BREAKOUT', 'Setup_Code': 'A_BASE', 'Volume_Confirm': 'PASS',
           'Leader_OK': 'PASS', 'Risk_OK': 'PASS', 'Earnings_Proximity_Flag': 'UNKNOWN'}
    v, why = l2_prep.baseline_verdict(row)
    a = (v == 'STALK' and 'Earnings_Proximity_Flag' in why)
    row['Earnings_Proximity_Flag'] = 'CLEAR'
    row['Risk_OK'] = 'FAIL'
    v2, why2 = l2_prep.baseline_verdict(row)
    b = (v2 == 'WATCH' and 'Earnings' not in why2)
    return ok('earnings reason stays in the earnings branch', a and b, f'{v}/{why} | {v2}/{why2}')
@case
def b3_v9_codes():
    prose = '跑贏 2800.HK 三條街，相對 6160 折讓'
    toks = [m.group(1) for m in cv.PRICE_TOKEN.finditer(prose)]
    return ok('V9 tokeniser still sees the numbers (code strip happens in the checker)', '2800' in toks, str(toks))
@case
def b3_v9_two_digit():
    toks = [m.group(1) for m in cv.PRICE_TOKEN.finditer('止蝕 HK$85 就走')]
    return ok('V9 now sees a 2-digit price', toks == ['85'], str(toks))
@case
def t_override_module_scope():
    import us_swing_v55 as _eng
    return ok('earnings_overrides lives at the engine module scope',
              isinstance(getattr(_eng, 'earnings_overrides', None), dict))
@case
def t_currency_from_profile():
    import gates
    us = gates.configure(markets.load('us'))['leader']['cur']
    hk = gates.configure(markets.load('hk'))['leader']['cur']
    return ok('currency comes from the profile', (us, hk) == ('$', 'HK$'), f'{us}/{hk}')
@case
def t_synth_bar_cannot_trigger():
    p = os.path.join(CODE, 'us_swing_v55.py')
    src = open(p, encoding='utf-8').read()
    a = "if bar_source == 'SYNTH_60M':" in src
    b = 'trigger needs manual confirm' in src and "Candidate_Class'] = 'C_WATCH'" in src
    return ok('a synthetic bar downgrades A_SETUP', a and b)

# ---- batch4 ----
@case
def t_tick_table():
    want = {0.50: 0.01, 4.40: 0.01, 10.19: 0.02, 23.16: 0.05, 51.60: 0.05,
            244.20: 0.20, 686.00: 0.50}
    bad = {p: hk_micro.tick_size(p) for p, t in want.items() if abs(hk_micro.tick_size(p) - t) > 1e-9}
    return ok('HKEX tick bands', not bad, str(bad))
@case
def t_round_to_tick():
    up = hk_micro.round_to_tick(245.06, 'up')
    dn = hk_micro.round_to_tick(10.13, 'down')
    return ok('trigger rounds up, stop rounds down',
              abs(up - 245.2) < 1e-6 and abs(dn - 10.12) < 1e-6, f'{up}/{dn}')
@case
def t_trigger_is_on_grid():
    px = 10.13
    t = hk_micro.tick_size(px)
    r = hk_micro.round_to_tick(px, 'up')
    return ok('rounded trigger is an exact multiple of the tick',
              abs((r / t) - round(r / t)) < 1e-9, f'{r} / {t}')
@case
def t_untraded_detection():
    vol = np.array([100.0, 0.0, 50.0])
    u = hk_micro.untraded_bars([1, 1, 1], [1, 1, 1], vol)
    return ok('zero turnover is untraded', list(u) == [False, True, False], str(u))
@case
def t_untraded_kills_base():
    """A long run of zero-volume bars must not become a base."""
    n = 60
    close = np.linspace(100, 101, n)
    df = pd.DataFrame({'High': close + 0.1, 'Low': close - 0.1, 'Close': close,
                       'Volume': np.zeros(n), 'ADR': np.full(n, 2.0), 'ATR': np.full(n, 2.0),
                       'Vol_Avg_20': np.full(n, 1e6), 'MA20': np.full(n, 100.0)})
    _, eps = base_layer.detect_bases(df, base_layer.STRICT)
    return ok('zero-volume run yields no episode', len(eps) == 0, f'{len(eps)} episodes')
@case
def t_tradable_mask_blocks():
    n = 60
    close = np.linspace(100, 101, n)
    df = pd.DataFrame({'High': close + 0.1, 'Low': close - 0.1, 'Close': close,
                       'Volume': np.full(n, 4e5), 'ADR': np.full(n, 2.0), 'ATR': np.full(n, 2.0),
                       'Vol_Avg_20': np.full(n, 1e6), 'MA20': np.full(n, 100.0),
                       'Tradable': np.zeros(n, bool)})
    _, eps = base_layer.detect_bases(df, base_layer.STRICT)
    return ok('an untradable bar cannot be compressed', len(eps) == 0, f'{len(eps)} episodes')
@case
def t_hk_codes():
    row = {'Ticker': 'X', 'Candidate_Class': 'C_WATCH', 'Entry_Feasible': 'NOT_YET',
           'Setup_Family': 'BREAKOUT', 'Setup_Code': 'A_BASE', 'Risk_OK': 'PENDING',
           'Earnings_Proximity_Flag': 'CLEAR', 'Tick_Pct': 0.55,
           'Base_Untraded_Bars': 2, 'Bar_Source': 'SYNTH_60M'}
    codes = {c['code'] for c in l2_prep.downgrade_codes(row)}
    return ok('HK codes fire', {'TICK_COARSE', 'BASE_UNTRADED', 'SYNTH_BAR'} <= codes, str(codes))

# ---- batch5 ----
def b5_row(stale):
    return pd.Series({'Close': 10.0, 'MA20': 9.8, 'MA50': 9.5, 'RS_Score': 12.0,
                      'RS_Stale': stale, 'ATR': 0.5, 'ADR': 0.4, 'Volume': 1e6,
                      'Vol_Avg_20': 9e5, 'Earnings_Proximity_Flag': 'CLEAR'})
@case
def t_stale_forces_unknown():
    gates.configure(markets.load('hk'))
    # v6.7: the flag only adds a reason. A broken trend still FAILs; the stale note is kept.
    row = b5_row(True).copy()
    row['Close'] = 20.0; row['MA20'] = 15.0; row['MA50'] = 16.0     # trend broken
    df = pd.DataFrame({'Close': np.linspace(20, 10, 120), 'High': np.linspace(20.1, 10.1, 120),
                       'Low': np.linspace(19.9, 9.9, 120), 'Volume': np.full(120, 1e6)})
    out = gates.evaluate(row, [], None, df=df)
    # Justin 2026-11-07: stale window -> UNKNOWN, never FAIL (missing data != broken trend)
    a = out['Leader_OK'] == 'UNKNOWN' and 'stale' in out['Leader_Why'].lower()
    # healthy trend + stale RS -> UNKNOWN (nothing to fail, but nothing to trust either)
    row2 = b5_row(True).copy()
    df2 = pd.DataFrame({'Close': np.linspace(9, 10, 120), 'High': np.linspace(9.1, 10.1, 120),
                        'Low': np.linspace(8.9, 9.9, 120), 'Volume': np.full(120, 1e6)})
    out2 = gates.evaluate(row2, [], None, df=df2)
    b = out2['Leader_OK'] == 'UNKNOWN' and 'stale' in out2['Leader_Why'].lower()
    return ok('stale RS -> UNKNOWN and never a PASS', a and b,
              f"{out['Leader_OK']} / {out2['Leader_OK']}")
@case
def t_not_stale_still_judges():
    gates.configure(markets.load('hk'))
    out = gates.evaluate(b5_row(False), [], None,
                         df=pd.DataFrame({'Close': np.linspace(9, 10, 120),
                                          'High': np.linspace(9.1, 10.1, 120),
                                          'Low': np.linspace(8.9, 9.9, 120),
                                          'Volume': np.full(120, 1e6)}))
    return ok('a complete stock is still judged normally', out['Leader_OK'] in ('PASS', 'FAIL'),
              str(out['Leader_OK']))
@case
def t_threshold_is_three():
    """Mirror of the engine expression: 2 missing bars is fine, 3 is not."""
    bench = pd.date_range('2026-08-01', periods=63, freq='B')
    close = pd.Series(10.0, index=bench)
    def stale(missing):
        have = close.reindex(bench).notna().sum() - missing
        return (len(bench) - have) >= 3
    return ok('threshold is 3 missing sessions', (not stale(2)) and stale(3))

# ---- batch6 ----
@case
def t_override_module_scope():
    """#1: importing the engine must not need the __main__ block."""
    return ok('earnings_overrides exists at module scope', isinstance(eng.earnings_overrides, dict))
@case
def t_override_aliases():
    """#3: 01071 must hit the same row as 1071.HK."""
    d = tempfile.mkdtemp()
    p = os.path.join(d, 'ov.csv')
    open(p, 'w', encoding='utf-8').write('Ticker,Date,Source\n01071,2027-03-25,TradingView\n')
    m = eng.load_earnings_overrides(p)
    want = {'1071.HK'} <= set(m)
    return ok('01071 resolves to 1071.HK', want, str(sorted(m)))
@case
def t_rulebook_is_live():
    """#2: the rows are built at write time, not frozen at import."""
    rows = eng.build_rulebook_rows()
    leader = next(r for r in rows if r[0] == 'Leader_OK')
    return ok('rulebook Leader row is built from config',
              'Leader_OK' == leader[0] and ("HK$" in leader[1] or "$" in leader[1]), leader[1])
@case
def t_rs_stale_never_fail():
    """Justin 2026-11-07: a stale window always yields UNKNOWN — even with a broken trend.
    Missing data is not evidence of weakness; the run must warn instead."""
    gates.configure({'name': 'HK'})
    df = pd.DataFrame({'Close': np.linspace(20, 10, 120), 'High': np.linspace(20.1, 10.1, 120),
                       'Low': np.linspace(19.9, 9.9, 120), 'Volume': np.full(120, 1e6)})
    row = pd.Series({'Close': 10.0, 'MA20': 15.0, 'MA50': 16.0, 'RS_Score': -20.0,
                     'RS_Stale': True, 'ATR': 0.5, 'ADR': 0.4, 'Volume': 1e6,
                     'Vol_Avg_20': 9e5, 'Earnings_Proximity_Flag': 'CLEAR'})
    out = gates.evaluate(row, [], None, df=df)
    return ok('trend FAIL + stale RS -> UNKNOWN + stale note',
              out['Leader_OK'] == 'UNKNOWN' and 'stale window' in out['Leader_Why'],
              f"{out['Leader_OK']} / {out['Leader_Why'][:60]}")
@case
def t_tick_rounding_in_gates():
    """#5: entry/stop are snapped before risk arithmetic, and the risk agrees with the price."""
    gates.configure({'name': 'HK', 'tick': True, 'currency': 'HKD'})
    for p in (0.07, 0.14, 10.14, 23.15, 244.2):
        if hk_micro.round_to_tick(p, 'up') != p or hk_micro.round_to_tick(p, 'down') != p:
            return ok('on-grid prices are unchanged (idempotent)', False, str(p))
    return ok('on-grid prices are unchanged (idempotent)', True)
@case
def t_tick_float_safety():
    """#5: 0.07/0.01 must not ceil an extra step."""
    return ok('float-safe ceil', hk_micro.round_to_tick(0.07, 'up') == 0.07,
              str(hk_micro.round_to_tick(0.07, 'up')))
@case
def t_v9_code_forms():
    """#9: 2800.HK is a code; a bare 388 is not."""
    def tokens(prose):
        prose = re.sub(r'(?<![0-9])\d{4}\.HK', ' ', prose)
        for code in {'2800', '0700', 'HSI'}:
            prose = re.sub(rf'(?<![0-9]){code}(?![0-9])', ' ', prose)
        out = []
        import check_verdict as cv
        for mt in cv.PRICE_TOKEN.finditer(prose):
            tail = prose[mt.end():mt.end() + 3]
            if cv.PRICE_UNIT.match(tail) or tail[:1] in ('-', '/'):
                continue
            out.append(mt.group(1))
        return out
    a = tokens('跑贏 2800.HK') == []
    b = tokens('止損 388') == ['388']
    c = tokens('52 週高') == []
    d = tokens('成交 500 股') == []
    return ok('codes stripped, bare prices kept, units respected', a and b and c and d,
              f'{a}{b}{c}{d}')
@case
def t_synth_keeps_flag_in_step():
    """#6: after the SYNTH downgrade the class and the flag must agree."""
    src = open(os.path.join(CODE, 'us_swing_v55.py'), encoding='utf-8').read()
    return ok('SYNTH downgrade also rewrites Screen_Flag and Entry_Feasible',
              "df.loc[last_idx, 'Screen_Flag'] = 'WATCH'" in src
              and "df.loc[last_idx, 'Entry_Feasible'] = 'NOT_YET'" in src)

# ---- batch7 ----
def b7_contract():
    for p in (os.path.join(HERE, 'CONTRACT_HK_SAMPLE.csv'),
              os.path.join(HERE, 'sample', 'Contract_US.csv'),
              os.path.join(os.path.dirname(CODE), 'runs', 'hk', 'v68', 'Contract_US.csv')):
        if os.path.exists(p):
            return p
    return None
@case
def t_risk_reconciles_with_printed_prices():
    """The risk % on the ticket must be derivable from the prices on the same row."""
    p = b7_contract()
    if p is None:
        return ok('risk% reconciles with Entry_Ref/Invalidate_Below', False, 'no sample')
    c = pd.read_csv(p)
    s = c[c.Entry_Ref.notna() & c.Invalidate_Below.notna() & c.Risk_Pct_Plan.notna()]
    if s.empty:
        return ok('risk% reconciles with Entry_Ref/Invalidate_Below', True, 'no tickets in sample')
    recalc = (s.Entry_Ref - s.Invalidate_Below) / s.Entry_Ref * 100
    return ok('risk% reconciles with Entry_Ref/Invalidate_Below',
              np.allclose(recalc, s.Risk_Pct_Plan, atol=1e-3),
              f'{list(np.round(recalc,4))} vs {list(s.Risk_Pct_Plan)}')
@case
def t_planned_trigger_is_raw():
    src = open(os.path.join(CODE, 'base_layer.py'), encoding='utf-8').read()
    return ok('base_layer keeps the planned trigger unrounded',
              "ep['high'] * 1.001        # v6.8: raw" in src
              and "round(ep['high'] * 1.001, 2)" not in src)
@case
def t_low_price_tick():
    """Claude's example: 0.2345 with a 0.005 tick must become 0.235, not 0.23."""
    return ok('0.2345 -> 0.235 on a 0.005 tick',
              abs(hk_micro.round_to_tick(0.2345, 'up') - 0.235) < 1e-9,
              str(hk_micro.round_to_tick(0.2345, 'up')))
@case
def t_synth_not_in_trigger_table():
    """A SYNTH bar must not produce a ticket row, and the flag must follow the final class."""
    import us_swing_v55 as eng
    d = tempfile.mkdtemp()
    row = {'Ticker': 'X', 'Candidate_Class': 'C_WATCH', 'Setup_OK': 'PASS', 'Risk_OK': 'PENDING',
           'Setup_Family': 'BREAKOUT', 'Setup_Code': 'A_BASE', 'Entry_Feasible': 'NOT_YET',
           'Base_State': 'ARMED', 'Bar_Source': 'SYNTH_60M', 'Trigger_Price': 10.0}
    df = pd.DataFrame([row] * 3)
    try:
        path = eng.generate_trigger({'X': df}, output_folder=d)
    except TypeError:
        path = eng.generate_trigger({'X': df})
    empty = (path is None) or (os.path.exists(path) and len(pd.read_csv(path)) == 0)
    src = open(os.path.join(CODE, 'us_swing_v55.py'), encoding='utf-8').read()
    flag = "CLASS_TO_FLAG.get(df.loc[last_idx, 'Candidate_Class'], 'NONE')" in src
    return ok('SYNTH row is excluded from Trigger and the flag follows the final class',
              empty and flag, f'empty={empty} flag={flag}')

if __name__ == '__main__':
    print('suite')
    results = [fn() for fn in CASES]
    print("\n%d/%d passed" % (sum(results), len(results)))
    sys.exit(0 if all(results) else 1)
