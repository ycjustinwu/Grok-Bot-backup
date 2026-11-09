#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch-1 regression tests (v6.1, review 2026-11-06).

    python3 tests/batch1.py

Pure-function tests plus file-level attacks on a temp copy of the sample run.
Exit 0 = every fix holds, 1 = a defect came back.
"""
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.dirname(HERE)
sys.path.insert(0, CODE)

import l2_prep  # noqa: E402

ROOT = os.path.dirname(CODE)
CASES = []


def sample():
    for p in (os.path.join(ROOT, '03_SAMPLE', 'run_v55'),
              os.path.join(ROOT, '04_RUN_US', 'run_v55'),
              os.path.join(ROOT, 'runs', 'run_v55')):
        if os.path.isdir(p):
            return p
    return None


def case(fn):
    CASES.append(fn)
    return fn


def ok(name, cond, detail=''):
    print(f"  {'OK  ' if cond else 'FAIL'} {name}" + (f" — {detail}" if detail and not cond else ''))
    return bool(cond)


def run_check(folder):
    r = subprocess.run([sys.executable, os.path.join(CODE, 'check_verdict.py'), folder],
                       cwd=CODE, capture_output=True, text=True)
    return r.returncode, r.stdout


def fresh():
    src = sample()
    d = tempfile.mkdtemp(prefix='b1_')
    dst = os.path.join(d, 'run')
    shutil.copytree(src, dst)
    subprocess.run([sys.executable, os.path.join(CODE, 'l2_prep.py'), dst],
                   cwd=CODE, capture_output=True, text=True)
    return d, dst


# ---------------------------------------------------------------- pure functions
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
    d, dst = fresh()
    try:
        p = os.path.join(dst, 'L2_Input.csv')
        rows = list(csv.DictReader(open(p, encoding='utf-8')))
        rows[0]['Baseline_Verdict'] = 'BUY'
        w = csv.DictWriter(open(p, 'w', newline='', encoding='utf-8'), fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
        rc, out = run_check(dst)
        return ok('V1b catches a tampered baseline', 'FAIL V1b' in out and rc == 2)
    finally:
        shutil.rmtree(d, ignore_errors=True)


@case
def t_v1c_contract_tamper():
    d, dst = fresh()
    try:
        p = os.path.join(dst, 'Contract_US.csv')
        s = open(p, encoding='utf-8').read().replace('UNH', 'UNH ', 1)
        open(p, 'w', encoding='utf-8').write(s)
        rc, out = run_check(dst)
        return ok('V1c catches a modified contract', 'FAIL V1c' in out and rc == 2)
    finally:
        shutil.rmtree(d, ignore_errors=True)


@case
def t_v9_invented_price():
    d, dst = fresh()
    try:
        p = os.path.join(dst, 'verdicts_US.jsonl')
        rows = [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
        rows[0]['invalidation'] = '收市跌穿 999.99 即離場'
        open(p, 'w', encoding='utf-8').write('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n')
        rc, out = run_check(dst)
        return ok('V9 catches a price that is not in the contract', 'not in the contract' in out, out[-200:])
    finally:
        shutil.rmtree(d, ignore_errors=True)


@case
def t_v6_downgrade_needs_code():
    d, dst = fresh()
    try:
        p = os.path.join(dst, 'verdicts_US.jsonl')
        rows = [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
        u = next(r for r in rows if r['verdict'] == 'BUY')
        u['verdict'] = 'STALK'
        u['downgrade_reason'] = 'Market sentiment bad'      # the old substring attack
        u.pop('downgrade_code', None)
        open(p, 'w', encoding='utf-8').write('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n')
        rc, out = run_check(dst)
        return ok('V6 rejects a free-text downgrade reason', 'FAIL V6' in out and rc == 2)
    finally:
        shutil.rmtree(d, ignore_errors=True)


@case
def t_v6_accepts_a_real_code():
    d, dst = fresh()
    try:
        p = os.path.join(dst, 'verdicts_US.jsonl')
        rows = [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]
        u = next(r for r in rows if r['verdict'] == 'BUY')
        u['verdict'] = 'STALK'
        u['downgrade_code'] = 'THIN_ROOM'
        u['downgrade_reason'] = 'thin room'
        open(p, 'w', encoding='utf-8').write('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n')
        rc, out = run_check(dst)
        return ok('V6 accepts a code l2_prep computed', 'PASS V6' in out, out[-200:])
    finally:
        shutil.rmtree(d, ignore_errors=True)


@case
def t_v4c_stalk_with_failed_risk():
    d, dst = fresh()
    try:
        ip = os.path.join(dst, 'L2_Input.csv')
        rows = list(csv.DictReader(open(ip, encoding='utf-8')))
        tgt = next(r for r in rows if r['Baseline_Verdict'] == 'BUY')
        tgt['Risk_OK'] = 'FAIL'
        tgt['Baseline_Verdict'] = 'STALK'
        w = csv.DictWriter(open(ip, 'w', newline='', encoding='utf-8'), fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
        vp = os.path.join(dst, 'verdicts_US.jsonl')
        vs = [json.loads(l) for l in open(vp, encoding='utf-8') if l.strip()]
        x = next(r for r in vs if r['ticker'] == tgt['Ticker'])
        x['verdict'] = 'STALK'; x['baseline'] = 'STALK'; x['downgrade_code'] = 'THIN_ROOM'
        open(vp, 'w', encoding='utf-8').write('\n'.join(json.dumps(r, ensure_ascii=False) for r in vs) + '\n')
        rc, out = run_check(dst)
        return ok('V4c rejects STALK with Risk_OK=FAIL', 'FAIL V4c' in out, out[-200:])
    finally:
        shutil.rmtree(d, ignore_errors=True)


@case
def t_clean_sample_still_passes():
    d = tempfile.mkdtemp(prefix='b1c_')
    try:
        dst = os.path.join(d, 'run')
        shutil.copytree(sample(), dst)
        subprocess.run([sys.executable, os.path.join(CODE, 'l2_prep.py'), dst], cwd=CODE, capture_output=True)
        rc, out = run_check(dst)
        return ok('clean sample still passes V1–V17', rc == 0, out[-160:])
    finally:
        shutil.rmtree(d, ignore_errors=True)


@case
def t_i29_can_fire():
    d = tempfile.mkdtemp(prefix='b1i_')
    try:
        dst = os.path.join(d, 'run')
        shutil.copytree(sample(), dst)
        p = os.path.join(dst, 'Contract_US.csv')
        rows = list(csv.DictReader(open(p, encoding='utf-8')))
        rows[0]['Volume_Confirm'] = 'NA'
        w = csv.DictWriter(open(p, 'w', newline='', encoding='utf-8'), fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
        r = subprocess.run([sys.executable, os.path.join(CODE, 'invariants.py'), dst],
                           cwd=CODE, capture_output=True, text=True)
        return ok('I29 fires on a literal NA', 'FAIL I29' in r.stdout, r.stdout[-160:])
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == '__main__':
    print('batch-1 regression tests')
    results = [fn() for fn in CASES]
    print(f"\n{sum(results)}/{len(results)} passed")
    sys.exit(0 if all(results) else 1)
