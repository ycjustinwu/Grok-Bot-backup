#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Per-bar structural levels: anchored VWAP, volume profile, S/R flip, FVG.

Everything here is a pure function of history up to bar i, so replay and the pullback
confluence see the same values the live scan sees.

v5.3 (see CHANGELOG_v53.md)
* F7  sr_flip_levels() now marks a *retest*: the 40-bar high was broken within the last
      RETEST_WINDOW bars, price has since come back to within touch_pct of that level, and the
      close is still holding it. v5.2 marked the breakout bar itself, so setup H almost never
      fired. New columns: SR_Flip_Live (level broken and not yet failed), SR_Flip_Age.
"""
import numpy as np
import pandas as pd

AVWAP_LOOKBACK = 20      # anchor = lowest low / highest high of the trailing 20 bars
HVD_LOOKBACK = 126       # anchor = highest-volume day of the trailing 126 bars
VP_LOOKBACK = 60         # volume profile window
VP_VALUE_AREA = 0.70

SR_LOOKBACK = 40         # the level = prior 40-bar high that was broken
SR_RETEST_WINDOW = 15    # a flip is retestable for this many bars after the break
SR_TOUCH_PCT = 2.0       # retest = a low within 2% above the level (or below it)
SR_HOLD_PCT = 1.0        # ...while the close holds within 1% under the level or above
SR_FAIL_PCT = 3.0        # a close >3% under the level kills the flip


def avwap_levels(df, lookback=AVWAP_LOOKBACK, hvd_lookback=HVD_LOOKBACK):
    """Per-bar AVWAP anchored at the trailing low, the trailing high, and the HVD."""
    n = len(df)
    high = df['High'].to_numpy(float)
    low = df['Low'].to_numpy(float)
    close = df['Close'].to_numpy(float)
    vol = df['Volume'].fillna(0).to_numpy(float)
    tp = (high + low + close) / 3.0
    p_tpv = np.concatenate([[0.0], np.cumsum(tp * vol)])
    p_vol = np.concatenate([[0.0], np.cumsum(vol)])
    out = {
        'AVWAP_20D_Low': np.full(n, np.nan),
        'AVWAP_20D_High': np.full(n, np.nan),
        'AVWAP_HVD': np.full(n, np.nan),
        'Dist_to_AVWAP_Low_Pct': np.full(n, np.nan),
        'Dist_to_AVWAP_High_Pct': np.full(n, np.nan),
        'Dist_to_AVWAP_HVD_Pct': np.full(n, np.nan),
    }

    def avwap_at(anchor, i):
        v = p_vol[i + 1] - p_vol[anchor]
        if not np.isfinite(v) or v <= 0:
            return np.nan
        return (p_tpv[i + 1] - p_tpv[anchor]) / v

    def rolling_anchor(values, window, mode):
        idx = np.full(n, -1, dtype=int)
        if n < window:
            return idx
        sw = np.lib.stride_tricks.sliding_window_view(values, window)
        pos = np.argmin(sw, axis=1) if mode == 'min' else np.argmax(sw, axis=1)
        idx[window - 1:] = pos + np.arange(0, n - window + 1)
        return idx

    a_low = rolling_anchor(low, lookback, 'min')
    a_high = rolling_anchor(high, lookback, 'max')
    a_hvd = rolling_anchor(vol, hvd_lookback, 'max')
    for i in range(n):
        for anchors, key, dkey in ((a_low, 'AVWAP_20D_Low', 'Dist_to_AVWAP_Low_Pct'),
                                   (a_high, 'AVWAP_20D_High', 'Dist_to_AVWAP_High_Pct'),
                                   (a_hvd, 'AVWAP_HVD', 'Dist_to_AVWAP_HVD_Pct')):
            if anchors[i] >= 0:
                v = avwap_at(int(anchors[i]), i)
                out[key][i] = v
                if np.isfinite(v) and v:
                    out[dkey][i] = (close[i] - v) / v * 100
    for k in list(out):
        if k.startswith('AVWAP'):
            out[k] = np.round(out[k], 2)
    return out


def volume_profile_levels(df, lookback=VP_LOOKBACK, value_area=VP_VALUE_AREA):
    """Per-bar POC / VAH / VAL over a trailing window."""
    n = len(df)
    high = df['High'].to_numpy(float)
    low = df['Low'].to_numpy(float)
    close = df['Close'].to_numpy(float)
    vol = df['Volume'].fillna(0).to_numpy(float)
    out = {k: np.full(n, np.nan) for k in ('POC_60D', 'VAH_60D', 'VAL_60D', 'Dist_to_POC_Pct',
                                           'Volume_Above_POC_Pct')}
    for k in ('Price_Relative_to_POC', 'POC_Acting_As'):
        out[k] = np.array([None] * n, dtype=object)
    for k in ('Inside_Value_Area', 'At_POC_Confluence'):
        out[k] = np.zeros(n, dtype=bool)
    for i in range(lookback - 1, n):
        s = i - lookback + 1
        lo, hi = float(np.min(low[s:i + 1])), float(np.max(high[s:i + 1]))
        if not (np.isfinite(lo) and np.isfinite(hi)) or hi <= lo or lo <= 0:
            continue
        nb = max(20, min(200, int((hi - lo) / (lo * 0.01)) + 1))
        bins = np.linspace(lo, hi, nb)
        vp = np.zeros(nb - 1)
        for j in range(s, i + 1):
            lb = max(0, min(np.searchsorted(bins, low[j], side='right') - 1, nb - 2))
            hb = max(0, min(np.searchsorted(bins, high[j], side='left'), nb - 1))
            if hb <= lb:
                continue
            vp[lb:hb] += vol[j] / (hb - lb)
        total = vp.sum()
        if total <= 0:
            continue
        pi = int(np.argmax(vp))
        poc = (bins[pi] + bins[pi + 1]) / 2
        cum, vi, hi_i = vp[pi], pi, pi
        while cum < total * value_area:
            cd, cu = vi > 0, hi_i < nb - 2
            if not cd and not cu:
                break
            up = vp[hi_i + 1] if cu else -1
            dn = vp[vi - 1] if cd else -1
            if cd and (not cu or dn >= up):
                vi -= 1
                cum += vp[vi]
            elif cu:
                hi_i += 1
                cum += vp[hi_i]
        val = (bins[vi] + bins[vi + 1]) / 2
        vah = (bins[hi_i] + bins[hi_i + 1]) / 2
        cp = close[i]
        out['POC_60D'][i] = round(poc, 2)
        out['VAH_60D'][i] = round(vah, 2)
        out['VAL_60D'][i] = round(val, 2)
        out['Dist_to_POC_Pct'][i] = round((cp - poc) / poc * 100, 2) if poc else np.nan
        out['Volume_Above_POC_Pct'][i] = round(vp[pi:].sum() / total * 100, 1)
        out['Inside_Value_Area'][i] = bool(val <= cp <= vah)
        out['At_POC_Confluence'][i] = bool(abs(cp - poc) / poc * 100 <= 2.0) if poc else False
        if cp > poc * 1.02:
            recent = close[max(0, i - 4):i + 1]
            out['Price_Relative_to_POC'][i] = 'Above'
            out['POC_Acting_As'][i] = 'Support' if bool(np.all(recent > poc)) else 'Neutral'
        elif cp < poc * 0.98:
            out['Price_Relative_to_POC'][i] = 'Below'
            out['POC_Acting_As'][i] = 'Resistance'
        else:
            out['Price_Relative_to_POC'][i] = 'At'
            out['POC_Acting_As'][i] = 'Neutral'
    return out


def sr_flip_levels(df, lookback=SR_LOOKBACK, window=SR_RETEST_WINDOW, touch_pct=SR_TOUCH_PCT,
                   hold_pct=SR_HOLD_PCT, fail_pct=SR_FAIL_PCT, min_level_age=10):
    """Per-bar S/R flip retest (F7).

    1. A *break*: the first close above the highest high of bars [i-lookback, i-min_level_age)
       — an old high that acted as resistance. That high becomes the flip level.
    2. The flip stays *live* for `window` bars after the break, unless a close falls more than
       `fail_pct` under the level (failed flip). A live level is not re-anchored.
    3. SR_Flip_Active (the retest) on bar i: the flip is live, i is after the break bar, the
       bar's low came back to within `touch_pct` above the level (or under it), and the close
       holds no more than `hold_pct` under the level.
    """
    n = len(df)
    high = df['High'].to_numpy(float)
    low = df['Low'].to_numpy(float)
    close = df['Close'].to_numpy(float)
    out = {'SR_Flip_Active': np.zeros(n, dtype=bool),
           'SR_Flip_Live': np.zeros(n, dtype=bool),
           'SR_Flip_Level': np.full(n, np.nan),
           'SR_Flip_Age': np.full(n, np.nan)}
    if n < lookback + 2:
        return out
    # the level = highest high of the window [i-lookback, i-min_level_age): an OLD high that acted
    # as resistance, not yesterday's high printed by the rally that is breaking it
    level_src = pd.Series(high).rolling(lookback - min_level_age).max().shift(min_level_age).to_numpy()
    level, born = np.nan, -1
    for i in range(lookback, n):
        if np.isfinite(level) and (i - born > window or close[i] < level * (1 - fail_pct / 100)):
            level, born = np.nan, -1                      # expired or failed flip
        sh = level_src[i]
        if not np.isfinite(level) and np.isfinite(sh) and close[i] > sh \
                and close[i - 1] <= sh:                   # first close through the old high
            level, born = float(sh), i
        if not np.isfinite(level):
            continue
        age = i - born
        out['SR_Flip_Live'][i] = True
        out['SR_Flip_Level'][i] = round(level, 2)
        out['SR_Flip_Age'][i] = age
        if age >= 1 and low[i] <= level * (1 + touch_pct / 100) and close[i] >= level * (1 - hold_pct / 100):
            out['SR_Flip_Active'][i] = True
    return out


def fvg_levels(df, max_age=90, max_open=200):
    """Per-bar nearest unfilled fair-value gaps (bullish below price, bearish above)."""
    n = len(df)
    high = df['High'].to_numpy(float)
    low = df['Low'].to_numpy(float)
    close = df['Close'].to_numpy(float)
    keys = ['Bullish_FVG1_Upper', 'Bullish_FVG1_Lower', 'Bullish_FVG1_Height_Pct',
            'Bearish_FVG1_Upper', 'Bearish_FVG1_Lower', 'Bearish_FVG1_Height_Pct']
    out = {k: np.full(n, np.nan) for k in keys}
    bull, bear = [], []      # (upper, lower, born_index)
    for i in range(n):
        bull = [g for g in bull if not (low[i] <= g[0])]
        bear = [g for g in bear if not (high[i] >= g[1])]
        if i >= 2:
            if low[i] > high[i - 2]:
                bull.append((low[i], high[i - 2], i))
            if high[i] < low[i - 2]:
                bear.append((low[i - 2], high[i], i))
        bull = [g for g in bull if i - g[2] <= max_age][-max_open:]
        bear = [g for g in bear if i - g[2] <= max_age][-max_open:]
        c = close[i]
        below = [g for g in bull if g[0] <= c]
        if below:
            u, l, _ = max(below, key=lambda g: g[0])
            out['Bullish_FVG1_Upper'][i] = round(u, 2)
            out['Bullish_FVG1_Lower'][i] = round(l, 2)
            out['Bullish_FVG1_Height_Pct'][i] = round((u - l) / l * 100, 2) if l else np.nan
        above = [g for g in bear if g[1] >= c]
        if above:
            u, l, _ = min(above, key=lambda g: g[1])
            out['Bearish_FVG1_Upper'][i] = round(u, 2)
            out['Bearish_FVG1_Lower'][i] = round(l, 2)
            out['Bearish_FVG1_Height_Pct'][i] = round((u - l) / l * 100, 2) if l else np.nan
    return out


def compute(df, want=('avwap', 'vp', 'sr', 'fvg')):
    """Attach every requested level set as columns and return (df, parts)."""
    parts = {}
    if 'avwap' in want:
        parts.update(avwap_levels(df))
    if 'vp' in want:
        parts.update(volume_profile_levels(df))
    if 'sr' in want:
        parts.update(sr_flip_levels(df))
    if 'fvg' in want:
        parts.update(fvg_levels(df))
    stale = [c for c in parts if c in df.columns]      # idempotent: never duplicate columns
    if stale:
        df = df.drop(columns=stale)
    return pd.concat([df, pd.DataFrame(parts, index=df.index)], axis=1), parts
