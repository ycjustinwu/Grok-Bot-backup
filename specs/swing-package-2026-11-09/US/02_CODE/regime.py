#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Market regime (1c) — the header every list should carry.

Qullamäggi's only market filter: NASDAQ Composite 10-EMA above 20-EMA, both rising. When it
is not in "momentum mode" he simply does not take breakout trades — and says a third to a
half of the year looks like that.

This is a header, not a score input: it does not change any gate, it tells you whether the
day's list deserves attention at all.
"""
import numpy as np
import pandas as pd

REGIME_INDEX = '^IXIC'
RISING_BARS = 10

# The user maintains this dashboard daily; it is the authoritative regime input.
SHEET_URL = ('https://docs.google.com/spreadsheets/d/'
             '1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk/export?format=csv')


def fetch_index(ticker=REGIME_INDEX, start=None, end=None):
    try:
        import yfinance as yf
        if start is None or end is None:
            df = yf.Ticker(ticker).history(period='2y', interval='1d',
                                           auto_adjust=True, actions=False)
        else:
            df = yf.Ticker(ticker).history(start=start, end=end, interval='1d',
                                           auto_adjust=True, actions=False)
        if df is None or len(df) == 0:
            return None
        df = df.rename(columns={c: c.title().replace(' ', '_') for c in df.columns})
        need = {'Close'}
        if not need <= set(df.columns):
            return None
        return df[['Close']].dropna()
    except Exception:
        return None


def evaluate(index_df, asof=None):
    """Return {'Regime_State', 'Regime_Why', 'Regime_Index'} for the last available bar."""
    empty = {'Regime_State': 'UNKNOWN', 'Regime_Why': 'index unavailable', 'Regime_Index': REGIME_INDEX}
    if index_df is None or len(index_df) < 30:
        return empty

    d = index_df
    if asof is not None:
        ts = pd.Timestamp(asof)
        tz = getattr(d.index, 'tz', None)
        if tz is not None:
            ts = ts.tz_localize(tz) if ts.tzinfo is None else ts.tz_convert(tz)
        d = d[d.index <= ts]
        if len(d) < 30:
            return empty

    close = d['Close'].astype(float)
    ema10 = close.ewm(span=10, adjust=False).mean()
    ema20 = close.ewm(span=20, adjust=False).mean()

    e10, e20 = float(ema10.iloc[-1]), float(ema20.iloc[-1])
    e10_prev = float(ema10.iloc[-1 - RISING_BARS])
    e20_prev = float(ema20.iloc[-1 - RISING_BARS])
    above = e10 > e20
    rising10 = e10 > e10_prev
    rising20 = e20 > e20_prev

    if above and rising10 and rising20:
        state = 'MOMENTUM'
        why = f'{REGIME_INDEX}: 10EMA {e10:.0f} > 20EMA {e20:.0f}, both rising'
    elif above:
        state = 'FLATTENING'
        why = f'{REGIME_INDEX}: 10EMA above 20EMA but not both rising'
    else:
        state = 'RISK_OFF'
        why = f'{REGIME_INDEX}: 10EMA {e10:.0f} < 20EMA {e20:.0f}'
    return {'Regime_State': state, 'Regime_Why': why, 'Regime_Index': REGIME_INDEX}


# ---------------------------------------------------------------------------
# Regime from the user's daily dashboard sheet
# ---------------------------------------------------------------------------
def fetch_sheet(url=None, timeout=20):
    """Return the sheet as text, or None. No credentials: the sheet must be link-readable."""
    import urllib.request
    url = url or SHEET_URL
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode('utf-8', errors='replace')
    except Exception:
        return None


def _first_float(text, default=np.nan):
    import re
    m = re.search(r'[-+]?\d+(?:\.\d+)?', str(text).replace(',', ''))
    return float(m.group()) if m else default


def parse_sheet(text, key='美股'):
    """Parse one market block of the dashboard. Returns {} when it cannot be read.

    v6.0: the block is located by `key`, and the columns are read from that block's own
    header row (`% 企穩 50 日線`, ...) instead of fixed positions. Two consequences:
      * the HK block no longer inherits the US block's 前一日 / 樣本;
      * `Breadth_Prev` now comes from the 50-day column, not the 20-day one (old bug:
        the report said 48.2% with prev 66.3%, where 66.3 was the 20-day series).
    """
    import io
    import re
    if not text:
        return {}
    try:
        d = pd.read_csv(io.StringIO(text), header=None, dtype=str).fillna('')
    except Exception:
        return {}
    if d.empty:
        return {}

    def cells(i):
        return [str(x).strip() for x in d.iloc[i].tolist()]

    # 1) locate this market's block
    bi = None
    for i in range(min(len(d), 25)):
        line = ' '.join(c for c in cells(i) if c)
        if key in line and ('市況' in line or '% >50D' in line):
            bi = i
            break
    if bi is None:
        return {}

    def num(x):
        t = str(x).replace('−', '-').replace('－', '-').replace(',', '')
        m = re.search(r'-?\d+(?:\.\d+)?', t)
        return float(m.group(0)) if m else np.nan

    header = ' '.join(c for c in cells(bi) if c)
    date = re.search(r'(\d{4}-\d{2}-\d{2})', header)
    label = re.search(r'市況[：:]\s*([^｜|\s]+)', header)
    breadth = re.search(r'>50D\s*([\d.]+)%', header)
    ratio = re.search(r'10日比率\s*([\d.]+)', header)
    mom = re.search(r'動力股佔比\s*([\d.]+)%', header)

    # 2) the header row of the numbers, then its value / 前一日 rows
    hdr_i = val_i = prev_i = None
    for i in range(bi + 1, min(bi + 4, len(d))):
        if any('企穩 50 日線' in c for c in cells(i)):
            hdr_i = i
            break
    if hdr_i is not None:
        cols = cells(hdr_i)
        col50 = next((j for j, c in enumerate(cols) if '企穩 50 日線' in c), None)
        col20 = next((j for j, c in enumerate(cols) if '企穩 20 日線' in c), None)
        if hdr_i + 2 < len(d):
            val_i, prev_i = hdr_i + 1, hdr_i + 2

    prev_breadth = prev_chg = sample = np.nan
    breadth20 = np.nan
    if val_i is not None and col50 is not None:
        val, prv = cells(val_i), cells(prev_i)
        if col50 < len(val):
            breadth20 = num(cells(val_i)[col20]) if col20 is not None and col20 < len(val) else np.nan
        if col50 < len(prv):
            prev_breadth = num(prv[col50])
            m = re.search(r'[(（]\s*([-−+]?\d+(?:\.\d+)?)\s*[)）]', prv[col50].replace('−', '-'))
            if m:
                prev_chg = float(m.group(1))
        if prv and '樣本' in prv[0]:
            m = re.search(r'([\d,]+)', prv[0])
            if m:
                sample = float(m.group(1).replace(',', ''))

    state = 'UNKNOWN'
    if label:
        if '強' in label.group(1):
            state = 'MOMENTUM'
        elif '弱' in label.group(1):
            state = 'RISK_OFF'
        elif any(w in label.group(1) for w in ('中性', '震', '整')):
            state = 'NEUTRAL'
    return {
        'Regime_State': state,
        'Regime_Label': label.group(1) if label else '',
        'Regime_Date': date.group(1) if date else '',
        'Regime_Source': 'SHEET',
        'Breadth_50D': float(breadth.group(1)) if breadth else np.nan,
        'Breadth_20D': breadth20,
        'Breadth_Prev': prev_breadth,
        'Breadth_Chg': prev_chg,
        'Ratio_10D': float(ratio.group(1)) if ratio else np.nan,
        'Momentum_Share': float(mom.group(1)) if mom else np.nan,
        'Breadth_Sample': sample,
        'Regime_Why': (f"sheet {date.group(1)}: 市況 {label.group(1)}, "
                       f"% >50D {float(breadth.group(1)) if breadth else float('nan')}% "
                       f"(prev {prev_breadth}%), 10日比率 {float(ratio.group(1)) if ratio else float('nan')}")
                      if date and label else 'sheet parsed',
    }


def evaluate_sheet(text, asof=None, key='美股'):
    """Sheet first; mark STALE when the sheet date lags the scanned session."""
    info = parse_sheet(text, key=key)
    if not info:
        return {}
    if asof is not None and info.get('Regime_Date'):
        try:
            lag = (pd.Timestamp(asof) - pd.Timestamp(info['Regime_Date'])).days
            if lag > 3:
                info['Regime_Why'] = f"STALE by {lag}d — " + info['Regime_Why']
                info['Regime_Stale'] = True
        except Exception:
            pass
    return info
