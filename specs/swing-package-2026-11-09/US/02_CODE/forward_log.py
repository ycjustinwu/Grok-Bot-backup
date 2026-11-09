#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Forward outcome log (v5.3, F14) — not a backtest, a running record.

Usage (run_daily.sh calls it after the scan):
    python3 forward_log.py <run_folder> [forward_log.csv]

1. Appends today's A_SETUP and C_WATCH tickets (one row per ticker per scan date).
2. For every open row, reads the newest <TICKER>_SwingAnalysis.csv in <run_folder> and
   fills what happened after the scan date: close return at +5/+10/+20 sessions, maximum
   favourable / adverse excursion in R (R = Entry_Ref - Invalidate_Below), and whether the
   stop or the entry was touched first.

Entry is assumed at Entry_Ref (planned trigger for NOT_YET, so a NOT_YET row only counts as
filled once a later high reaches it). Nothing here feeds a gate; it only lets you see, after a
few months, whether A_SETUP behaves differently from C_WATCH.
"""
import os
import sys

import numpy as np
import pandas as pd

KEEP = ('A_SETUP', 'C_WATCH')
HORIZONS = (5, 10, 20)
COLS = ['Scan_Date', 'Ticker', 'Candidate_Class', 'Setup_Family', 'Setup_Code', 'Entry_Feasible',
        'Volume_Confirm', 'Leader_OK', 'Entry_Ref', 'Invalidate_Below', 'Room_To_Supply_R',
        'Filled', 'Fill_Date', 'Stopped', 'Stop_Date', 'Bars_Seen',
        'Ret5_Pct', 'Ret10_Pct', 'Ret20_Pct', 'MFE_R', 'MAE_R', 'Status']


def _hist(folder, ticker):
    for base in (folder, os.path.join(folder, 'history')):
        p = os.path.join(base, f'{ticker}_SwingAnalysis.csv')
        if os.path.exists(p):
            d = pd.read_csv(p, usecols=lambda c: c in ('Date', 'High', 'Low', 'Close'))
            d['Date'] = pd.to_datetime(d['Date'], utc=True, errors='coerce').dt.tz_localize(None).dt.normalize()
            return d.dropna(subset=['Date']).set_index('Date')
    return None


def update(row, d):
    e, s = float(row['Entry_Ref']), float(row['Invalidate_Below'])
    if not (np.isfinite(e) and np.isfinite(s) and e > s):
        row['Status'] = 'NO_RISK'
        return row
    r = e - s
    after = d[d.index > pd.Timestamp(row['Scan_Date'])]
    row['Bars_Seen'] = len(after)
    if after.empty:
        return row
    if row['Entry_Feasible'] == 'NOT_YET':
        hit = after[after['High'] >= e]
        if hit.empty:
            row['Filled'], row['Status'] = False, 'WAITING' if len(after) < 20 else 'NEVER_FILLED'
            return row
        after = after.loc[hit.index[0]:]
    row['Filled'], row['Fill_Date'] = True, str(after.index[0].date())
    stop_hit = after[after['Low'] <= s]
    if len(stop_hit):
        row['Stopped'], row['Stop_Date'] = True, str(stop_hit.index[0].date())
    else:
        row['Stopped'] = False
    win = after.head(max(HORIZONS))
    row['MFE_R'] = round((win['High'].max() - e) / r, 2)
    row['MAE_R'] = round((win['Low'].min() - e) / r, 2)
    for h in HORIZONS:
        if len(after) >= h:
            row[f'Ret{h}_Pct'] = round((after['Close'].iloc[h - 1] / e - 1) * 100, 2)
    row['Status'] = 'DONE' if len(after) >= max(HORIZONS) else 'OPEN'
    return row


def main(folder, log_path):
    con_path = os.path.join(folder, 'Contract_US.csv')
    log = pd.read_csv(log_path) if os.path.exists(log_path) else pd.DataFrame(columns=COLS)
    if os.path.exists(con_path):
        c = pd.read_csv(con_path)
        c = c[c['Candidate_Class'].isin(KEEP)].copy()
        c['Scan_Date'] = pd.to_datetime(c['Date'], utc=True, errors='coerce').dt.tz_localize(None).dt.date.astype(str)
        new = c.reindex(columns=COLS)
        new['Status'] = 'OPEN'
        key = set(zip(log.get('Scan_Date', []), log.get('Ticker', [])))
        new = new[[(a, b) not in key for a, b in zip(new['Scan_Date'], new['Ticker'])]]
        log = pd.concat([log, new], ignore_index=True) if len(log) else new
    log = log.astype(object)
    cache = {}
    for i, row in log.iterrows():
        if row.get('Status') in ('DONE', 'NEVER_FILLED', 'NO_RISK'):
            continue
        t = row['Ticker']
        if t not in cache:
            cache[t] = _hist(folder, t)
        if cache[t] is not None:
            log.loc[i] = update(row.copy(), cache[t])
    log.to_csv(log_path, index=False)
    done = log[log['Status'] == 'DONE']
    print(f'forward log: {len(log)} rows ({len(done)} complete) -> {log_path}')
    if len(done):
        print(done.groupby('Candidate_Class')[['Ret10_Pct', 'MFE_R', 'MAE_R']].median().round(2).to_string())


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.',
         sys.argv[2] if len(sys.argv) > 2 else 'forward_log.csv')
