#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L1 -> L2 bridge (v5.5). Pure function of Contract_US.csv; adds no new market data.

Usage:  python3 l2_prep.py <run_folder> [prev_run_folder]

Writes into <run_folder>:
  L2_Input.csv        Contract + Baseline_Verdict, Setup_Quality(+_Detail), Grade, Change_vs_Prev, Story_Needed
  story_handoffs.md   one STORY HANDOFF v5 block per name with Story_Needed=True (feed to Grok story-search)
  l2_status.json      run status for L2: OK / RUN_FAILED / DATA_STALE, counts

Rules live in 01_RULES/WORKFLOW_v55.md §3-§4. This script is the only place they are computed.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

KEEP_NA = dict(keep_default_na=False, na_values=[''])   # never turn NOT_APPL / NONE into NaN
VERDICT_RANK = {'AVOID': 0, 'WATCH': 1, 'STALK': 2, 'BUY': 3}
INDEX_20EMA_RULE = os.environ.get('SWING_INDEX_20EMA_RULE', '0') == '1'   # default OFF
WEAK_BUY_RULE = os.environ.get('SWING_WEAK_BUY_RULE', '0') == '1'         # v5.5.2 §3.1: default OFF


def isval(x):
    """NaN-safe truthiness: an empty CSV cell reads as NaN, and NaN is truthy."""
    if x is None:
        return False
    try:
        if pd.isna(x):
            return False
    except Exception:
        pass
    return str(x).strip() not in ('', 'nan', 'None', 'MISSING')


def num(v, d=np.nan):
    try:
        return float(v) if v not in (None, '') and pd.notna(v) else d
    except Exception:
        return d


def baseline_verdict(r):
    """WORKFLOW §3.1 — the class -> verdict table, computed, never left to the LLM."""
    cls, ef = r.get('Candidate_Class', ''), r.get('Entry_Feasible', '')
    fam, code = r.get('Setup_Family', ''), r.get('Setup_Code', '')
    epf = r.get('Earnings_Proximity_Flag', 'UNKNOWN')
    why = []
    if ef in ('INVALIDATED', 'MISSED'):
        v, why = 'AVOID', [f'Entry_Feasible={ef}']
    elif cls == 'A_SETUP':
        if ef in ('AT_TRIGGER', 'NEXT_DAY'):
            v = 'BUY'
            if r.get('Volume_Confirm') == 'LOW':
                v, why = 'STALK', ['Volume_Confirm=LOW (REMARK mode)']
        elif ef == 'LATE':
            ok = num(r.get('Risk_ADR_Plan'), 9) <= 1.0 and num(r.get('Room_To_Supply_R'), 0) >= 2
            v = 'BUY' if ok else 'WATCH'
            why = [] if ok else ['LATE entry without Risk<=1.0xADR and Room>=2R']
        elif ef == 'AT_MARKET' and fam == 'REVERSAL':
            ok = r.get('Leader_OK') != 'FAIL' and num(r.get('Room_To_Supply_R'), 0) >= 2
            v = 'BUY' if ok else 'STALK'
            why = [] if ok else ['REVERSAL needs Leader_OK!=FAIL and Room>=2R for BUY']
        elif ef == 'AT_MARKET':
            v = 'BUY'
        else:
            v = 'WATCH'
    elif cls == 'C_WATCH':
        # v6.1 (C6): a buy-stop is a live order, so it is only legitimate while the stop is
        # still undefined (PENDING). C_WATCH means Setup PASS + Risk FAIL, and a FAIL reason
        # (extended, RSI, thin room) does not disappear by waiting for the trigger.
        pending_risk = str(r.get('Risk_OK')) == 'PENDING'
        v = 'STALK' if (ef == 'NOT_YET' and pending_risk) else 'WATCH'
        if ef == 'NOT_YET' and not pending_risk:
            why = [f"Risk_OK={r.get('Risk_OK')} (not PENDING) — no live buy-stop"]
    elif cls == 'B_LEADER_WAIT':
        v = 'WATCH'
    elif cls in ('X_NONE', 'NONE', ''):
        v = 'AVOID'
    else:
        # v6.1 (C6): an unknown class used to fall through to AVOID silently
        raise ValueError(f'unknown Candidate_Class {cls!r}')
    # A1 (2026-11-06): the earnings override has to cover STALK too. A pending base with
    # risk PENDING lands on C_WATCH -> STALK, and a STALK ticket is a live buy-stop; letting
    # it through on the earnings day is the most dangerous shape of this bug because the
    # ticket looks completely normal. PLAYBOOK §2: PASS => AVOID, UNKNOWN => never BUY.
    if v in ('BUY', 'STALK') and epf in ('PASS', 'UNKNOWN'):
        v = 'AVOID' if epf == 'PASS' else 'STALK'
        why.append(f'Earnings_Proximity_Flag={epf}')
    # v6.2 (Grok #1): the earnings override can turn BUY into STALK *after* the risk check
    # ran, so re-assert it last. A ticket on a known-bad risk is never legitimate, reachable
    # from L1 or not — this is a pure function and must hold for every input.
    # 2026-11-07: risk is a gate. L1 publishes Tradeable = PASS/FAIL using the plan stop
    # (which exists before the trigger), so a pending breakout is judged too, not exempted.
    if str(r.get('Tradeable', 'PASS')) != 'PASS' and v in ('BUY', 'STALK'):
        v = 'WATCH'
        why.append(f"not tradeable: {r.get('Tradeable_Why') or 'risk/room outside caps'}")
    if v in ('BUY', 'STALK') and str(r.get('Risk_OK')) not in ('PASS', 'PENDING'):
        v = 'WATCH'
        why.append(f"Risk_OK={r.get('Risk_OK')} (no live ticket)")
    if v == 'BUY' and r.get('Risk_OK') != 'PASS':
        v = 'WATCH'
        why.append(f"Risk_OK={r.get('Risk_OK')}")
    if INDEX_20EMA_RULE and v == 'BUY' and fam == 'BREAKOUT' and str(r.get('Index_Below_20EMA')) == 'True':
        v = 'STALK'
        why.append('Index_Below_20EMA=True (breakout rule)')
    return v, '; '.join(why)


QUALITY = {   # WORKFLOW §3.2 — display only, never changes class or baseline
    'BREAKOUT': [
        ('Base_Vol_Decay', lambda x: x < 0.7, 'volume dried up (<0.7)'),
        ('Base_HigherLows_Pct', lambda x: x >= 0.6, 'higher lows >=60%'),
        ('Base_Cleanliness', lambda x: x >= 0.8, 'clean (>=80% above MA20)'),
        ('Base_Prior_Advance_Pct', lambda x: x >= 25, 'prior advance >=25%'),
        ('Base_Count_126', lambda x: x <= 2, '<=2nd base in 126 bars'),
    ],
    'PULLBACK': [
        ('Vol_Ratio_Pullback', lambda x: x <= 0.8, 'pullback volume <=0.8x'),
        ('Depth_ATR', lambda x: 1 <= x <= 3, 'depth 1-3 ATR'),
        ('Confluence_Count', lambda x: x >= 2, 'support confluence >=2'),
        ('RS_Line_NH', lambda x: x == 1, 'RS line at new high'),
        ('Room_To_Supply_R', lambda x: x >= 2, 'room >=2R'),
    ],
    'REVERSAL': [
        ('Drawdown_Pct', lambda x: x >= 35, 'drawdown >=35%'),
        ('UpDown_Vol', lambda x: x >= 1.5, 'up/down volume >=1.5'),
        ('HigherLow_Pct', lambda x: x >= 3, 'higher low >=3% above low'),
        ('Dist_to_AVWAP_Low_Pct', lambda x: x > 0, 'above AVWAP from the low'),
        ('Room_To_Supply_R', lambda x: x >= 2, 'room >=2R'),
    ],
}


def setup_quality(r):
    fam = r.get('Setup_Family', 'NONE')
    if fam not in QUALITY or r.get('Candidate_Class') not in ('A_SETUP', 'C_WATCH'):
        return np.nan, 'NA', ''
    score, parts, missing = 0, [], 0
    for col, test, label in QUALITY[fam]:
        raw = r.get(col)
        if isinstance(raw, str) and raw in ('True', 'False'):
            raw = 1.0 if raw == 'True' else 0.0
        x = num(raw)
        if not np.isfinite(x):
            parts.append(f'?{label}')
            missing += 1
        elif test(x):
            score += 1
            parts.append(f'+{label}')
        else:
            parts.append(f'-{label}')
    grade = 'A+' if score >= 4 else ('A' if score == 3 else 'B')
    if missing >= 3:
        grade = 'NA'
    return score, grade, ' | '.join(parts)


def change_vs_prev(r, prev):
    t = r['Ticker']
    if prev is None:
        # no previous run: nothing "changed", it is the first observation
        return 'BASELINE' if r.get('Candidate_Class') in ('A_SETUP', 'C_WATCH') else 'UNCHANGED'
    if t not in prev.index:
        return 'NEW' if r.get('Candidate_Class') in ('A_SETUP', 'C_WATCH') else 'UNCHANGED'
    p = prev.loc[t]
    if r.get('Base_State') == 'TRIGGERED' and p.get('Base_State') != 'TRIGGERED':
        return 'TRIGGERED'
    if r.get('Entry_Feasible') == 'INVALIDATED' and p.get('Entry_Feasible') != 'INVALIDATED':
        return 'INVALIDATED'
    a, b = VERDICT_RANK.get(r['Baseline_Verdict'], 0), VERDICT_RANK.get(p.get('Baseline_Verdict', 'AVOID'), 0)
    if a > b:
        return 'UPGRADED'
    if a < b:
        return 'DOWNGRADED'
    if r.get('Candidate_Class') in ('A_SETUP', 'C_WATCH') and p.get('Candidate_Class') not in ('A_SETUP', 'C_WATCH'):
        return 'NEW'
    return 'UNCHANGED'


def fmt(v, nd=2):
    x = num(v)
    return f'{x:.{nd}f}' if np.isfinite(x) else 'MISSING'


def handoff_block(r):
    v = r['Baseline_Verdict']
    epf = r.get('Earnings_Proximity_Flag', 'UNKNOWN')
    entry = r.get('Trigger_Price') if v == 'STALK' and r.get('Entry_Feasible') == 'NOT_YET' else r.get('Entry_Ref')
    supply = (f"{fmt(r.get('Supply_Level'))} ({r.get('Supply_Source')}, {fmt(r.get('Room_To_Supply_R'))}R)"
              if np.isfinite(num(r.get('Supply_Level'))) else 'NONE_ABOVE (blue sky)')
    concern = '; '.join(str(x) for x in (r.get('Risk_Why', ''), r.get('Class_Note', ''), r.get('Speak_Up', ''))
                        if isinstance(x, str) and x) or 'none'
    vc = r.get('Volume_Confirm')
    vol = ('NOT_APPL' if r.get('Setup_Family') != 'BREAKOUT' else
           f"{vc} (not triggered yet; needs >= {fmt(r.get('Trigger_Min_Vol'), 0)} shares)" if vc == 'PENDING' else
           f"{vc} ({fmt(r.get('Trigger_Vol_Ratio'))}x 20d avg)")
    pending = r.get('Entry_Feasible') == 'NOT_YET'
    stop = (f"breakout-day low (set at fill); skip if that low < {fmt(r.get('BuyStop_Max_Stop'))}; "
            f"base low {fmt(r.get('Invalidate_Below'))}") if pending else \
        f"{fmt(r.get('Invalidate_Below'))} ({r.get('Stop_Type_Plan', 'MISSING')})"
    lines = [
        '```',
        'STORY HANDOFF v5',
        f"TICKER: {r['Ticker']}",
        f"MARKET: {r.get('Market') if isval(r.get('Market')) else 'US'}",
        f"HANDOFF DATE: {r.get('Date', 'MISSING')}",
        f"VERDICT: {v}",
        f"SETUP: {r.get('Setup_Family')}/{r.get('Setup_Code')}"
        + (f" {r['Base_Family']}" if str(r.get('Base_Family', '')).strip() not in ('', 'nan', 'MISSING') else '')
        + f" · state {r.get('Base_State')} · {r.get('Entry_Feasible')}",
        f"ENTRY: {fmt(entry)} ({'buy-stop' if v == 'STALK' and r.get('Entry_Feasible') == 'NOT_YET' else r.get('Entry_Src', 'entry')})",
        f"STOP: {stop}",
        f"SUPPLY ABOVE: {supply}",
        'TARGET: NONE (v5 has no target; never invent one)',
        f"EARNINGS: {epf} · {(r.get('Earnings_Date') if isval(r.get('Earnings_Date')) else 'MISSING')} · "
        f"{int(num(r.get('Days_To_Earnings'), -1)) if np.isfinite(num(r.get('Days_To_Earnings'))) else 'MISSING'} sessions",
        f"RS (vs {r.get('Benchmark') if isval(r.get('Benchmark')) else 'SPY'}): {fmt(r.get('RS_Score'), 1)}",
        f"BASE VOLUME DRY-UP: {fmt(r.get('Base_Vol_Decay'))} (low = good)" if r.get('Setup_Family') == 'BREAKOUT' else 'BASE VOLUME DRY-UP: NOT_APPL',
        f"BREAKOUT VOLUME: {vol}",
        f"QUALITY: {r.get('Setup_Quality_Grade')} ({fmt(r.get('Setup_Quality'), 0)}/5) {r.get('Setup_Quality_Detail', '')}",
        f"TECHNICAL CONCERN: {concern}",
        '```',
    ]
    return '\n'.join(lines)


def speak_up(r):
    """WORKFLOW §4.4 red flags that layer 2 must mention. Computed so they are never forgotten."""
    out = []
    if num(r.get('RSI_14')) > 75:
        out.append(f"RSI {fmt(r.get('RSI_14'), 0)}")
    if num(r.get('Extension_MA20_Pct')) > 10:
        out.append(f"extended {fmt(r.get('Extension_MA20_Pct'), 1)}% over MA20")
    if r.get('Volume_Confirm') == 'LOW':
        out.append(f"low breakout volume {fmt(r.get('Trigger_Vol_Ratio'))}x")
    room = num(r.get('Room_To_Supply_R'), 9)
    if np.isfinite(room) and room < 1.5:
        out.append(f"thin room {fmt(r.get('Room_To_Supply_R'))}R to {r.get('Supply_Source')}")
    if num(r.get('Room_To_Soft_R'), 9) < 1:
        out.append(f"soft supply {r.get('Supply_Soft_Source')} at {fmt(r.get('Room_To_Soft_R'))}R")
    if r.get('Leader_OK') == 'FAIL':
        out.append('not a leader (Leader_OK=FAIL)')
    if r.get('Earnings_Proximity_Flag') == 'CAUTION':
        out.append('earnings within 8-14 sessions: shorten hold')
    if r.get('Earnings_Proximity_Flag') == 'UNKNOWN':
        out.append('earnings date UNKNOWN: story-search must find it')
    return '; '.join(out)


DOWNGRADE_CODES = (
    ('RSI_HOT', 'RSI_14'), ('EXT_MA20', 'Extension_MA20_Pct'), ('THIN_ROOM', 'Room_To_Supply_R'),
    ('SOFT_LEVEL', 'Room_To_Soft_R'), ('NOT_LEADER', 'RS_Score'), ('LOW_VOLUME', 'Trigger_Vol_Ratio'),
    ('EARNINGS_CAUTION', 'Earnings_Proximity_Flag'), ('EARNINGS_UNKNOWN', 'Earnings_Proximity_Flag'),
    ('WEAK_QUALITY', 'Setup_Quality'), ('PROV_RISK', 'Room_Basis'), ('BASE_FAILED', 'Base_State'),
    ('EARNINGS_SOON', 'Earnings_Proximity_Flag'),
    # v6.5 (HK): market-microstructure reasons
    ('TICK_COARSE', 'Tick_Pct'), ('BASE_UNTRADED', 'Base_Untraded_Bars'),
    ('SYNTH_BAR', 'Bar_Source'),
)


def downgrade_codes(r):
    """The only reasons layer 2 may cite when it downgrades (spec v6.1, C4/V6).

    Each entry carries the contract field and the value at scan time, so the gate can check
    that the cited reason matches the data instead of a substring.
    """
    out = []

    def add(code, field, value, why):
        out.append({'code': code, 'field': field, 'value': value, 'why': why})

    rsi, ext = num(r.get('RSI_14')), num(r.get('Extension_MA20_Pct'))
    room, soft = num(r.get('Room_To_Supply_R')), num(r.get('Room_To_Soft_R'))
    rs, vc = num(r.get('RS_Score')), r.get('Volume_Confirm')
    epf, base = r.get('Earnings_Proximity_Flag'), r.get('Base_State')
    grade = r.get('Setup_Quality_Grade')
    if np.isfinite(rsi) and rsi > 75:
        add('RSI_HOT', 'RSI_14', round(float(rsi), 2), f'RSI {rsi:.1f} > 75')
    if np.isfinite(ext) and ext > 10:
        add('EXT_MA20', 'Extension_MA20_Pct', round(float(ext), 2), f'extended {ext:.1f}% over MA20')
    if np.isfinite(room) and room < 1.5:
        add('THIN_ROOM', 'Room_To_Supply_R', round(float(room), 2), f'room {room:.2f}R < 1.5R')
    if np.isfinite(soft) and soft < 1:
        add('SOFT_LEVEL', 'Room_To_Soft_R', round(float(soft), 2), f'soft level {soft:.2f}R')
    if np.isfinite(rs) and rs < 10:
        add('NOT_LEADER', 'RS_Score', round(float(rs), 1), f'RS {rs:.1f} < 10')
    if vc == 'LOW':
        add('LOW_VOLUME', 'Trigger_Vol_Ratio', num(r.get('Trigger_Vol_Ratio')), 'breakout volume LOW')
    if epf == 'CAUTION':
        add('EARNINGS_CAUTION', 'Earnings_Proximity_Flag', epf, 'earnings in 8-14 sessions')
    if epf == 'UNKNOWN':
        add('EARNINGS_UNKNOWN', 'Earnings_Proximity_Flag', epf, 'earnings date unknown')
    if epf == 'PASS':
        add('EARNINGS_SOON', 'Earnings_Proximity_Flag', epf, 'earnings within 7 sessions')
    if grade in ('B', 'NA'):
        add('WEAK_QUALITY', 'Setup_Quality', num(r.get('Setup_Quality')), f'grade {grade}')
    if r.get('Room_Basis') == 'PROV_1ADR':
        add('PROV_RISK', 'Room_Basis', 'PROV_1ADR', 'risk is provisional (1xADR)')
        if np.isfinite(room) and room < 1.5:
            add('PROV_THIN', 'Room_To_Supply_R', round(float(room), 2),
                f'room {room:.2f}R measured with a provisional R — re-check at the fill')
    if base in ('FAILED', 'BO_FAILED'):
        add('BASE_FAILED', 'Base_State', base, f'base {base}')
    # v6.5 (HK): one tick is a large share of the price, so the risk band is meaningless
    tp = num(r.get('Tick_Pct'))
    if np.isfinite(tp) and tp > 0.3:
        add('TICK_COARSE', 'Tick_Pct', round(float(tp), 3),
            f'one tick is {tp:.2f}% of the price (band too coarse for a stop)')
    ub = num(r.get('Base_Untraded_Bars'))
    if np.isfinite(ub) and ub > 0:
        add('BASE_UNTRADED', 'Base_Untraded_Bars', int(ub),
            f'{int(ub)} untraded bar(s) inside the base')
    if r.get('Bar_Source') == 'SYNTH_60M':
        add('SYNTH_BAR', 'Bar_Source', 'SYNTH_60M', 'last bar rebuilt from 60m data')
    return out


def compute_baseline(c):
    """The single implementation of the class -> verdict table (used by S3 and by S6)."""
    bv = c.apply(baseline_verdict, axis=1, result_type='expand')
    c = c.copy()
    c['Baseline_Verdict'], c['Baseline_Why'] = bv[0], bv[1]
    q = c.apply(setup_quality, axis=1, result_type='expand')
    c['Setup_Quality'], c['Setup_Quality_Grade'], c['Setup_Quality_Detail'] = q[0], q[1], q[2]
    if WEAK_BUY_RULE:
        weak = ((c['Baseline_Verdict'] == 'BUY')
                & c['Setup_Quality_Grade'].isin(['B', 'NA'])
                & (pd.to_numeric(c['Room_To_Supply_R'], errors='coerce') < 1.5)
                & (c['Leader_OK'] == 'FAIL'))
        if weak.any():
            c.loc[weak, 'Baseline_Verdict'] = 'STALK'
            c.loc[weak, 'Baseline_Why'] = c.loc[weak, 'Baseline_Why'].fillna('').astype(str) \
                + 'weak BUY: grade/room/leader; '
    return c


def sha256_of(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def main(folder, prev_folder=None):
    status = {'folder': folder, 'status': 'OK', 'reason': ''}
    inv = os.path.join(folder, 'invariants.txt')
    if os.path.exists(inv) and any(l.startswith('FAIL ') for l in open(inv, encoding='utf-8')):
        status.update(status='RUN_FAILED', reason='an invariant FAILED')
    c = pd.read_csv(os.path.join(folder, 'Contract_US.csv'), **KEEP_NA)
    for col in ('Risk_Why', 'Class_Note', 'Setup_Why', 'Earnings_Date'):
        if col in c.columns:
            c[col] = c[col].fillna('').astype(str)
    prev = None
    if prev_folder and os.path.exists(os.path.join(prev_folder, 'L2_Input.csv')):
        prev = pd.read_csv(os.path.join(prev_folder, 'L2_Input.csv'), **KEEP_NA).set_index('Ticker')
    c = compute_baseline(c)
    c['Downgrade_Codes'] = c.apply(lambda r: json.dumps(downgrade_codes(r), ensure_ascii=False), axis=1)
    c['Speak_Up'] = c.apply(speak_up, axis=1)
    c['Change_vs_Prev'] = c.apply(lambda r: change_vs_prev(r, prev), axis=1)
    c['Story_Needed'] = c['Baseline_Verdict'].isin(['BUY', 'STALK'])
    dates = pd.to_datetime(c.get('Date'), errors='coerce').dropna()
    status['as_of'] = str(dates.max().date()) if len(dates) else 'MISSING'
    exp = os.environ.get('SWING_EXPECTED_DATE')
    if exp and status['as_of'] != exp and status['status'] == 'OK':
        status.update(status='DATA_STALE', reason=f"contract {status['as_of']} != expected {exp}")
    status['counts'] = c['Baseline_Verdict'].value_counts().to_dict()
    status['story_needed'] = int(c['Story_Needed'].sum())
    c.to_csv(os.path.join(folder, 'L2_Input.csv'), index=False)
    status['flags'] = {'SWING_INDEX_20EMA_RULE': INDEX_20EMA_RULE,
                       'SWING_WEAK_BUY_RULE': WEAK_BUY_RULE}
    try:
        status['sha256'] = {'Contract_US.csv': sha256_of(os.path.join(folder, 'Contract_US.csv')),
                            'L2_Input.csv': sha256_of(os.path.join(folder, 'L2_Input.csv'))}
    except Exception as exc:
        status['sha256'] = {'error': str(exc)[:80]}
    blocks = [f"# STORY HANDOFFS — {status['as_of']}", '',
              'Feed each block to Grok story-search v3.2. Do not edit the values.', '']
    for _, r in c[c['Story_Needed']].sort_values('Baseline_Verdict').iterrows():
        blocks += [handoff_block(r), '']
    if not c['Story_Needed'].any():
        blocks.append('No BUY / STALK today: no story search needed.')
    with open(os.path.join(folder, 'story_handoffs.md'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(blocks) + '\n')
    with open(os.path.join(folder, 'l2_status.json'), 'w', encoding='utf-8') as fh:
        json.dump(status, fh, ensure_ascii=False, indent=1)
    print(json.dumps(status, ensure_ascii=False))
    return status


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.', sys.argv[2] if len(sys.argv) > 2 else None)
