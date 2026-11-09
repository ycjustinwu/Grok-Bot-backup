#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replay the screener as of a past session, from the per-ticker CSVs of a finished run.

Usage: python3 replay.py <run_folder> YYYY-MM-DD

Base detection AND the per-bar levels are recomputed on the truncated history, so the replay
cannot look ahead and always uses the current (v5.3) definitions.

v5.3 (see CHANGELOG_v53.md)
* F12 Date column is the session date (v5.2 wrote the row number after reset_index).
* F12 levels.compute() is re-run on the truncated history (new S/R flip definition).
* F12 supply comes from gates.find_supply (same code path as the live scan).
* F12 a Replay_Note column says what is not historical (earnings) and flags short history
      (< 252 bars => no MA200 / 52-week high, so the trend and supply checks are weaker).
"""
import os
import sys

import numpy as np
import pandas as pd

_FOLDER = sys.argv[1] if len(sys.argv) > 1 else '.'
_ASOF = sys.argv[2] if len(sys.argv) > 2 else '2025-12-31'
os.environ['SWING_OUTPUT_FOLDER'] = os.path.join(_FOLDER, f'asof_{_ASOF}')

try:                                    # import after env so the engine's folder is right
    import us_swing_v55 as engine       # noqa: E402
except ImportError:
    try:
        import us_swing_v54 as engine   # noqa: E402
    except ImportError:
        import us_swing_v53 as engine   # noqa: E402
    except ImportError:
        import us_swing_v52 as engine   # noqa: E402
except ImportError:                     # pragma: no cover
    import us_swing_v52 as engine       # noqa: E402
import base_layer                       # noqa: E402
import gates                            # noqa: E402
import levels                           # noqa: E402
import pullback                         # noqa: E402

TICKET_STATES = ('NOT_YET', 'AT_TRIGGER', 'NEXT_DAY', 'LATE', 'AT_MARKET')
TICKET_COLS = ['Ticker', 'Candidate_Class', 'Setup_Family', 'Setup_Code', 'Setup_OK', 'Risk_OK',
               'Entry_Feasible', 'Base_State', 'Base_Family', 'Volume_Confirm', 'Stop_Type_Plan',
               'Trigger_Price', 'BuyStop_Max_Stop', 'Entry_Ref', 'Invalidate_Below', 'Risk_ADR_Plan',
               'Room_To_Supply_R', 'Supply_Source', 'Class_Note', 'Setup_Why', 'Risk_Why']


def _history_files(folder):
    files = []
    for base in (folder, os.path.join(folder, 'history'), os.path.join(folder, 'samples')):
        if os.path.isdir(base):
            files += [os.path.join(base, f) for f in sorted(os.listdir(base))
                      if f.endswith('_SwingAnalysis.csv')]
    return files


def main(folder, asof):
    out = os.path.join(folder, f'asof_{asof}')
    os.makedirs(out, exist_ok=True)
    o = pd.Timestamp(asof)
    rows, tickets, evidence = [], [], []
    for path in _history_files(folder):
        t = os.path.basename(path).replace('_SwingAnalysis.csv', '')
        d = pd.read_csv(path, parse_dates=['Date'])
        d['Date'] = pd.to_datetime(d['Date'], utc=True, errors='coerce').dt.tz_localize(None)
        d = d[d['Date'] <= o].set_index('Date')
        if len(d) < 80:
            continue
        d, _ = levels.compute(d)
        d, _ = base_layer.detect_bases(d, base_layer.STRICT)
        d, _ = base_layer.detect_bases(d, base_layer.WIDE)
        snaps = [base_layer.snapshot(d, 'BaseS', cfg_width=base_layer.STRICT['width_atr_max']),
                 base_layer.snapshot(d, 'BaseW', cfg_width=base_layer.WIDE['width_atr_max'])]
        r = d.iloc[-1].copy()
        r['Earnings_Proximity_Flag'] = 'CLEAR'        # not historical in the CSV
        pb = pullback.evaluate(r, d)
        g = gates.evaluate(r, snaps, pb, df=d)
        for k, v in g.items():
            if k != 'Evidence':
                r[k] = v
        note = 'earnings forced CLEAR (not historical): Risk_OK is structure-only'
        if len(d) < 252:
            note += f'; only {len(d)} bars: MA200 / 52W high incomplete'
        r['Replay_Note'] = note
        row = {k: engine._row_value(r, k) for k in engine.CONTRACT_FIELDS}
        row['Ticker'] = t
        row['Date'] = str(d.index[-1].date())
        row['Replay_Note'] = note
        rows.append(row)
        if g['Entry_Feasible'] in TICKET_STATES:
            tk = {k: engine._row_value(r, k) for k in TICKET_COLS if k != 'Ticker'}
            tk['Ticker'] = t
            tickets.append(tk)
        for block, text, status in g['Evidence']:
            evidence.append({'Ticker': t, 'Block': block, 'Check': text, 'Status': status})

    con = pd.DataFrame(rows, columns=list(engine.CONTRACT_FIELDS) + ['Replay_Note'])
    con.to_csv(os.path.join(out, 'Contract_US.csv'), index=False)
    pd.DataFrame(evidence).to_csv(os.path.join(out, 'Evidence_US.csv'), index=False)
    if tickets:
        pd.DataFrame(tickets, columns=TICKET_COLS).to_csv(os.path.join(out, 'Trigger_US.csv'), index=False)
    print(f'== replay {folder} as of {asof}: {len(con)} tickers, {len(tickets)} tickets')
    print('   NOTE: earnings forced to CLEAR (not historical) — Risk_OK is structure-only here.')
    if len(con):
        short = con['Replay_Note'].str.contains('bars:').sum()
        if short:
            print(f'   NOTE: {short} tickers have < 252 bars at this date (MA200 / 52W high incomplete).')
        print(con['Candidate_Class'].value_counts().to_string())
        show = con[con['Candidate_Class'].isin(['A_SETUP', 'C_WATCH'])][
            ['Ticker', 'Candidate_Class', 'Entry_Feasible', 'Base_State', 'Setup_Len_Days',
             'Risk_ADR_Plan', 'Room_To_Supply_R', 'Class_Note', 'Setup_Why']]
        if len(show):
            print(show.to_string(index=False))
    print(f'\nwrote {out}/Contract_US.csv (+Evidence, +Trigger)')


if __name__ == '__main__':
    main(_FOLDER, _ASOF)
