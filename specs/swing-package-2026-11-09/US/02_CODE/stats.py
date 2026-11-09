#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Descriptive statistics for a scan folder — the ground a reviewer can check against.

Usage: python3 stats.py <run_folder>

Describes what the rules produced (coverage, episodes, gate pass rates, UNKNOWN rates,
risk/room distributions). No performance claim: there is no backtest by design.
v5.3: BO_FAILED column, failed-breakout rate per family, Volume_Confirm / Base_Family counts.
"""
import os
import sys

import numpy as np
import pandas as pd


def load(folder):
    sm = os.path.join(folder, 'Contract_US.csv')
    if not os.path.exists(sm):
        sm = os.path.join(folder, 'Summary_US.csv')
    contract = pd.read_csv(sm)
    frames = []
    for base in (folder, os.path.join(folder, 'history'), os.path.join(folder, 'samples')):
        if not os.path.isdir(base):
            continue
        for f in sorted(os.listdir(base)):
            if f.endswith('_SwingAnalysis.csv'):
                d = pd.read_csv(os.path.join(base, f))
                d['Ticker'] = f.replace('_SwingAnalysis.csv', '')
                frames.append(d)
    return contract, (pd.concat(frames, ignore_index=True) if frames else pd.DataFrame())


def pct(x, n):
    return f'{100.0 * x / n:.1f}%' if n else 'n/a'


def main(folder):
    c, h = load(folder)
    out = []
    A = out.append
    A(f'# STATS — {folder}')
    A('')
    A(f'names: {len(c)}   bars: {len(h)}   period: {h["Date"].iloc[0]} .. {h["Date"].iloc[-1]}'
      if len(h) else f'names: {len(c)}   bars: 0')
    A('')
    if len(h):
        A('## Base coverage (share of all bar-days)')
        A('')
        A('| family | FORMING/READY/ARMED | TRIGGERED | BO_FAILED | FAILED | SPENT | EXPIRED | NONE |')
        A('|---|---|---|---|---|---|---|---|')
        for fam in ('BaseS', 'BaseW'):
            if f'{fam}_State' not in h.columns:
                continue
            st = h[f'{fam}_State'].fillna('NONE')
            n = len(st)
            cells = [pct(st.isin(['FORMING', 'READY', 'ARMED']).sum(), n)] + \
                [pct((st == s).sum(), n) for s in ('TRIGGERED', 'BO_FAILED', 'FAILED', 'SPENT', 'EXPIRED', 'NONE')]
            A(f'| {fam} | ' + ' | '.join(cells) + ' |')
        A('')
        A('## Base episodes')
        A('')
        A('| family | episodes | len p10/p50/p90 | width ATR p50 | trigger rate | failed-breakout rate |')
        A('|---|---|---|---|---|---|')
        for fam in ('BaseS', 'BaseW'):
            if f'{fam}_ID' not in h.columns:
                continue
            sub = h[h[f'{fam}_ID'] > 0]
            if sub.empty:
                continue
            g = sub.groupby(['Ticker', f'{fam}_ID'])
            lens = g[f'{fam}_Len'].max()
            widths = g[f'{fam}_Width_ATR'].last().dropna()
            trig = g[f'{fam}_State'].apply(lambda s: s.isin(['TRIGGERED', 'BO_FAILED', 'SPENT']).any())
            bof = g[f'{fam}_State'].apply(lambda s: (s == 'BO_FAILED').any())
            A(f'| {fam} | {len(lens)} | '
              f'{lens.quantile(.1):.0f} / {lens.median():.0f} / {lens.quantile(.9):.0f} | '
              f'{widths.median():.2f} | {pct(trig.sum(), len(trig))} | {pct(bof.sum(), trig.sum())} |')
        A('')
    A('## Gates (last row per name)')
    A('')
    for col in ('Leader_OK', 'Setup_OK', 'Risk_OK', 'Candidate_Class', 'Setup_Family', 'Setup_Code',
                'Base_Family', 'Volume_Confirm', 'Entry_Feasible'):
        if col in c.columns:
            vc = c[col].fillna('MISSING').value_counts().to_dict()
            A(f'- `{col}`: ' + ', '.join(f'{k} {v}' for k, v in vc.items()))
    A('')
    A('## Uncertainty (this is where a silent pass would hide)')
    A('')
    A(f'- `RS_Status=UNKNOWN`: {int((c.get("RS_Status") == "UNKNOWN").sum())}/{len(c)}')
    A(f'- earnings: {c.get("Earnings_Proximity_Flag", pd.Series(dtype=object)).value_counts().to_dict()}')
    A('')
    A('## Risk and room (last row, only where a setup exists)')
    A('')
    for col in ('Risk_ADR_Plan', 'Room_To_Supply_R', 'Room_To_Soft_R'):
        if col in c.columns:
            v = pd.to_numeric(c[col], errors='coerce').dropna()
            if len(v):
                A(f'- `{col}`: n={len(v)}  p10 {v.quantile(.1):.2f}  p50 {v.median():.2f}  '
                  f'p90 {v.quantile(.9):.2f}  min {v.min():.2f}  max {v.max():.2f}')
    if 'Supply_Source' in c.columns:
        A(f'- `Supply_Source`: {c["Supply_Source"].value_counts().to_dict()}')
    A('')
    A('## Regime (header only — never changes a gate)')
    A('')
    if 'Regime_State' in c.columns and len(c):
        A(f'- state {c["Regime_State"].iloc[0]} · label {c.get("Regime_Label", pd.Series([""])).iloc[0]} '
          f'· source {c.get("Regime_Source", pd.Series([""])).iloc[0]} '
          f'· index second opinion {c.get("Index_Regime_State", pd.Series([""])).iloc[0]}')
    A('')
    A('## What is NOT here')
    A('')
    A('No returns, no expectancy, no win rate. See forward_log.py for the outcome log.')
    text = '\n'.join(out)
    print(text)
    path = os.path.join(folder, 'STATS.md')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text + '\n')
    print(f'\nwrote {path}')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '..')
