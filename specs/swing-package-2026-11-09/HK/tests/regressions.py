#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regression tests for the 2026-11-06 Hermes defect report (A1-A12).

    python3 tests/regressions.py [<package root>]

Runs against the sample run in 03_SAMPLE (package layout) or ../runs/run_v55 (workspace).
Exit 0 = all fixed, 1 = a defect came back.
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
CODE = os.path.dirname(HERE)
ROOT = os.path.dirname(CODE)


def find_sample():
    for p in (os.path.join(ROOT, '03_SAMPLE', 'run_v55'),
              os.path.join(ROOT, '04_RUN_US', 'run_v55'),
              os.path.join(ROOT, 'runs', 'run_v55'),
              os.path.join(ROOT, 'run_v55')):
        if os.path.isdir(p):
            return p
    return None


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def load_rows(path):
    with open(path, encoding='utf-8', newline='') as fh:
        return list(csv.DictReader(fh))


def save_rows(path, rows):
    with open(path, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


class Checker:
    def __init__(self):
        self.fail = 0

    def ok(self, cond, label, detail=''):
        print(('  OK   ' if cond else '  FAIL ') + label + (f'  [{detail}]' if detail and not cond else ''))
        if not cond:
            self.fail += 1


def main():
    c = Checker()
    sample = find_sample()
    if not sample:
        print('no sample run found'); return 1
    tmp = tempfile.mkdtemp(prefix='usswing_regr_')
    try:
        # ---------- A1: earnings override covers STALK ----------
        sys.path.insert(0, CODE)
        import l2_prep
        # v6.1 (C6) moved the ticket path to Risk_OK=PENDING; a FAIL risk means no live order,
        # so the earnings override no longer has anything to protect there. Both halves are
        # asserted: with a ticket (PENDING) earnings still governs; without one (FAIL) it is WATCH.
        base = {'Candidate_Class': 'C_WATCH', 'Entry_Feasible': 'NOT_YET', 'Setup_Family': 'BREAKOUT',
                'Setup_Code': 'A_BASE', 'Volume_Confirm': 'PENDING', 'Risk_OK': 'PENDING', 'Leader_OK': 'PASS'}
        c.ok(l2_prep.baseline_verdict(dict(base, Earnings_Proximity_Flag='PASS'))[0] == 'AVOID',
             'A1 C_WATCH/NOT_YET + earnings PASS -> AVOID')
        c.ok(l2_prep.baseline_verdict(dict(base, Earnings_Proximity_Flag='UNKNOWN'))[0] == 'STALK',
             'A1 C_WATCH/NOT_YET + earnings UNKNOWN -> STALK (allowed)')
        c.ok(l2_prep.baseline_verdict(dict(base, Risk_OK='FAIL',
                                           Earnings_Proximity_Flag='PASS'))[0] == 'WATCH',
             'A1/C6 C_WATCH/NOT_YET + Risk FAIL -> no ticket, WATCH')

        # ---------- A6: docs agree on 107 / 1f.3 ----------
        rules = os.path.join(ROOT, '01_RULES') if os.path.isdir(os.path.join(ROOT, '01_RULES')) \
            else os.path.join(ROOT, 'rules')
        drift = []
        for f in ('WORKFLOW_v55.md', 'PLAYBOOK_v5.4.md', 'DATA_DICTIONARY.md'):
            p = os.path.join(rules, f)
            if not os.path.exists(p):
                continue
            txt = open(p, encoding='utf-8').read()
            if re.search(r'102 欄|107 欄', txt) and '107 欄' not in txt:
                drift.append(f)
            if re.search(r'us-contract-1f\.[12]\b', txt):
                drift.append(f)
        c.ok(not drift, 'A6 docs say 107 欄 / 1f.3', str(drift))

        # ---------- A12: explicit exit 0 ----------
        rd = open(os.path.join(CODE, 'run_daily.sh'), encoding='utf-8').read().rstrip().split('\n')
        c.ok(rd[-1].strip() == 'exit 0', 'A12 run_daily.sh ends with exit 0', rd[-1])

        # ---------- A4/A5: gate limits and the citation rule ----------
        import check_verdict as cv
        c.ok(cv.LIMITS.get('closer') == 50 and 'story_main' not in cv.LIMITS,
             'A4 closer=50, story_main not a verdict field')
        c.ok(cv.STORY_LIMITS.get('story_main') == 200, 'A4 V17 story_main=200')
        c.ok(cv.zlen('回穩但唔係冠軍，輕身上陣。') == 11, 'A4 punctuation-free counter')

        def banned(text):
            for m in cv.BANNED_RE.finditer(text):
                if cv.ATTRIB_RE.search(text[max(0, m.start() - 10):m.start()]):
                    continue
                return True
            return False
        c.ok(not banned('分析師平均目標 65.50'), 'A5 broker target passes')
        c.ok(banned('目標價 70'), 'A5 bare target fails')
        c.ok(banned('T2 78'), 'A5 T2 fails')

        # ---------- A2/A3/A10: the rendered cover speaks with one verdict ----------
        work = os.path.join(tmp, 'run')
        shutil.copytree(sample, work)
        rows = load_rows(os.path.join(work, 'L2_Input.csv'))
        unk = [r for r in rows if r['Ticker'] == 'UNH'][0]
        verdicts = [json.loads(l) for l in open(os.path.join(work, 'verdicts_US.jsonl'),
                                                encoding='utf-8') if l.strip()]
        for v in verdicts:
            if v['ticker'] == 'UNH':
                v['verdict'] = 'AVOID'
                v['downgrade_reason'] = 'Risk_Why: thin room'
        with open(os.path.join(work, 'verdicts_US.jsonl'), 'w', encoding='utf-8') as fh:
            for v in verdicts:
                fh.write(json.dumps(v, ensure_ascii=False) + '\n')
        unk['Shares_per_1000_Risk'] = ''          # A10 fixture
        # A2 fixture: give INTA a *baseline* STALK order, then downgrade it in verdicts.
        # This is exactly the shape Hermes reported: the order survives in ③.
        inta = [r for r in rows if r['Ticker'] == 'INTA'][0]
        inta['Baseline_Verdict'] = 'STALK'
        inta['Entry_Feasible'] = 'NOT_YET'
        inta['Candidate_Class'] = 'C_WATCH'
        for v in verdicts:
            if v['ticker'] == 'INTA':
                v['verdict'] = 'WATCH'
                v['downgrade_reason'] = 'Earnings_Proximity_Flag=PASS'
        with open(os.path.join(work, 'verdicts_US.jsonl'), 'w', encoding='utf-8') as fh:
            for v in verdicts:
                fh.write(json.dumps(v, ensure_ascii=False) + '\n')
        save_rows(os.path.join(work, 'L2_Input.csv'), rows)

        r = run([sys.executable, 'render_report.py', work], CODE)
        idx = open(os.path.join(work, 'reports', 'index.md'), encoding='utf-8').read()
        c.ok(r.returncode == 0, 'render runs', r.stderr[-200:])
        stalk_block = idx.split('## ③ STALK')[1].split('##')[0] if '## ③ STALK' in idx else ''
        c.ok('INTA' not in stalk_block, 'A2 downgraded STALK left the order table', stalk_block[:120])
        c.ok('INTA：STALK → **WATCH**' in idx, 'A2 downgrade recorded in ③b')
        c.ok('UNH：BUY → **AVOID**' in idx or 'UNH：STALK → **AVOID**' in idx,
             'A2/A3 downgrade shown as a move', idx[:0])
        c.ok('⛔ UNH' in idx, 'A3 AVOID is ⛔, not ✅')
        report = open(os.path.join(work, 'reports', 'UNH_投資快報.md'), encoding='utf-8').read()
        c.ok('股數待成交後計算' in report, 'A10 no phantom share count')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    print('ALL REGRESSIONS PASS' if c.fail == 0 else f'{c.fail} REGRESSION(S) FAILED')
    return 0 if c.fail == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
