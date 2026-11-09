#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Base episode layer (v5.3 / 1f) — two coexisting detectors.

Why an episode and not a per-day flag
-------------------------------------
The v4.6 zone was a per-day counter that (a) could start on a non-tight bar, (b) reset its
exception budget on every tight bar, (c) merged exception bars into its own high/low, and
(d) kept counting past its own maximum. All four make zone geometry a moving target.

Two families
------------
* STRICT — maximal run of strictly compressed bars, no gaps, 5-30 sessions.
* WIDE   — 10-40 sessions, up to 2 consecutive non-compressed bars allowed inside, must be
  >= 60% compressed, and must *start* on a compressed bar. Geometry uses the in-span bars
  whose range <= 1.5 x ADR, so one wild bar cannot define the base.

Both freeze geometry at the last bar of the run and trigger on a *later* bar closing above
the frozen high, so the breakout and the base can never be the same bar.

v5.3 changes (see CHANGELOG_v53.md)
-----------------------------------
* F1  A breakout that closes back below the breakout-bar low becomes BO_FAILED (it used to
      stay TRIGGERED -> A_SETUP purely by bar count).
* F2  WIDE: a non-compressed bar that CLOSES outside the running base range ends the run
      before that bar. It can no longer be absorbed as a "gap" and swallow its own breakout.
* F3  max_len is enforced (a run longer than max_len is not a base of that family).
* F4  Trigger fields are cleared when a new episode starts; a newer episode always wins
      over the post-window of an older one (no inherited Trigger_Date).
"""
import numpy as np
import pandas as pd

COLS = [
    'ID', 'State', 'Len', 'Start', 'End',
    'High', 'Low', 'Width_ATR', 'Width_Pct',
    'Vol_Decay', 'Cleanliness', 'HigherLows_Pct', 'Prior_Advance_Pct',
    'Count_126', 'Has_Trigger', 'Compressed_Pct',
    'Trigger_Date', 'Trigger_Close', 'Trigger_Vol_Ratio', 'Trigger_Risk_ADR',
    'Days_Since_Trigger', 'Invalidate_Below', 'Planned_Trigger',
]
TRIGGER_COLS = ('Trigger_Date', 'Trigger_Close', 'Trigger_Vol_Ratio', 'Trigger_Risk_ADR')

STRICT = dict(
    name='STRICT', prefix='BaseS',
    allow_gaps=0, min_len=5, max_len=30,
    range_mult=1.0, vol_mult=0.85,
    width_atr_max=3.0, min_compressed_frac=1.0,
    geometry_range_mult=None,        # None = use every bar in the run
    live_bars=30, late_after=2, post_trigger_bars=10,
)
WIDE = dict(
    name='WIDE', prefix='BaseW',
    allow_gaps=2, min_len=10, max_len=40,
    range_mult=1.0, vol_mult=0.85,
    width_atr_max=4.0, min_compressed_frac=0.60,
    geometry_range_mult=1.5,         # include in-span bars up to 1.5 x ADR, drop outliers
    live_bars=40, late_after=3, post_trigger_bars=12,
)
FAMILIES = {'STRICT': STRICT, 'WIDE': WIDE}
BY_PREFIX = {STRICT['prefix']: STRICT, WIDE['prefix']: WIDE}


def _cols(prefix):
    return [f'{prefix}_{c}' for c in COLS]


def _blank(n, prefix):
    out = {}
    for c in COLS:
        k = f'{prefix}_{c}'
        if c in ('ID', 'Len', 'Count_126'):
            out[k] = np.zeros(n, dtype=np.int64)
        elif c == 'Days_Since_Trigger':
            out[k] = np.full(n, -1, dtype=np.int64)
        elif c == 'State':
            out[k] = np.array(['NONE'] * n, dtype=object)
        elif c in ('Start', 'End', 'Trigger_Date'):
            out[k] = np.full(n, np.nan, dtype=object)
        elif c == 'Has_Trigger':
            out[k] = np.zeros(n, dtype=bool)
        else:
            out[k] = np.full(n, np.nan, dtype=float)
    return out


def _attach(df, cols):
    return pd.concat([df, pd.DataFrame(cols, index=df.index)], axis=1)


def _geo_ok(i, high, low, adr, cfg):
    if cfg['geometry_range_mult'] is None:
        return True
    return bool(np.isfinite(adr[i]) and (high[i] - low[i]) <= adr[i] * cfg['geometry_range_mult'])


def _find_runs(compressed, high, low, close, adr, cfg):
    """Pass 1: runs of compressed bars with up to cfg['allow_gaps'] consecutive gaps.

    F2: a gap bar whose CLOSE leaves the running geometry range ends the run *before* that
    bar — a close outside the base is an event (trigger or break), never part of the base.
    """
    n = len(compressed)
    runs, start, gaps = [], None, 0
    run_hi, run_lo = -np.inf, np.inf
    for i in range(n):
        if compressed[i]:
            if start is None:
                start, run_hi, run_lo = i, -np.inf, np.inf
            gaps = 0
            run_hi, run_lo = max(run_hi, high[i]), min(run_lo, low[i])
            continue
        if start is None:
            continue
        # F2b: only a READY base can be triggered or broken. Before the run reaches
        # min_len there is no live signal, so the v5.2 gap tolerance still applies: a close
        # outside a still-forming range is noise, not a breakout. No buffer and no volume
        # condition here on purpose — a buffer would let a READY base swallow a low-volume
        # breakout and change the signal after the fact, which is the bug this fixes.
        ready = (i - start - gaps) >= cfg['min_len']
        if ready and (close[i] > run_hi or close[i] < run_lo):
            runs.append((start, i - 1 - gaps))
            start, gaps = None, 0
            continue
        gaps += 1
        if gaps > cfg['allow_gaps']:
            runs.append((start, i - gaps))
            start, gaps = None, 0
            continue
        if _geo_ok(i, high, low, adr, cfg):                 # tolerated gap inside the base
            run_hi, run_lo = max(run_hi, high[i]), min(run_lo, low[i])
    if start is not None:
        runs.append((start, n - 1 - gaps))
    return runs


def detect_bases(df, cfg=STRICT):
    """Return (df_with_<prefix>_columns, episodes). Pure function of the price history."""
    prefix = cfg['prefix']
    stale = [c for c in _cols(prefix) if c in df.columns]
    if stale:
        df = df.drop(columns=stale)
    n = len(df)
    cols = _blank(n, prefix)
    if n < max(40, cfg['min_len']):
        return _attach(df, cols), []

    high = df['High'].to_numpy(float)
    low = df['Low'].to_numpy(float)
    close = df['Close'].to_numpy(float)
    vol = df['Volume'].to_numpy(float)
    adr = df['ADR'].to_numpy(float)
    atr = df['ATR'].to_numpy(float)
    vol20 = df['Vol_Avg_20'].to_numpy(float)
    ma20 = df['MA20'].to_numpy(float) if 'MA20' in df.columns else np.full(n, np.nan)

    # v6.3 (HK): a bar with no turnover is not "compressed", it is untraded (suspension,
    # halt, or a dead illiquid name). Yahoo omits most suspended sessions entirely, but it
    # does return zero-volume rows for illiquid HK tickers, and a run of them would look
    # like a perfect base. Harmless for US, where zero-volume bars do not occur.
    traded = np.isfinite(vol) & (vol > 0)
    compressed = (
        (high - low <= adr * cfg['range_mult'])
        & (vol < vol20 * cfg['vol_mult'])
        & traded
        & np.isfinite(adr) & np.isfinite(vol20)
    )
    runs = _find_runs(compressed, high, low, close, adr, cfg)

    episodes = []
    for (s, e) in runs:
        if e < s:
            continue
        span = e - s + 1
        if span < cfg['min_len']:
            continue
        if span > cfg['max_len']:
            # F3b: a cap trims, it does not delete. Keep the most recent max_len bars and
            # recompute the geometry on those bars only. The trimmed base must still start
            # on a compressed bar, otherwise it is not this family's base at all.
            s = e - cfg['max_len'] + 1
            while s < e and not compressed[s]:
                s += 1
            span = e - s + 1
            if span < cfg['min_len']:
                continue
        comp_idx = np.array([i for i in range(s, e + 1) if compressed[i]], dtype=int)
        if len(comp_idx) == 0:
            continue
        frac = len(comp_idx) / span
        if frac < cfg['min_compressed_frac']:
            continue
        geo_idx = np.array([i for i in range(s, e + 1) if _geo_ok(i, high, low, adr, cfg)], dtype=int)
        if len(geo_idx) == 0:
            geo_idx = comp_idx
        bh, bl = float(np.max(high[geo_idx])), float(np.min(low[geo_idx]))
        a = atr[e] if np.isfinite(atr[e]) else np.nan
        width_atr = (bh - bl) / a if np.isfinite(a) and a > 0 else np.nan
        pre_vol = np.nanmean(vol[max(0, s - 20):s]) if s > 0 else np.nan
        run_vol = np.nanmean(vol[comp_idx])
        decay = run_vol / pre_vol if np.isfinite(pre_vol) and pre_vol > 0 else np.nan
        clean = float(np.mean(close[geo_idx] > ma20[geo_idx])) if np.isfinite(ma20[geo_idx]).any() else np.nan
        hl_pct = float(np.mean(low[comp_idx[1:]] > low[comp_idx[:-1]])) if len(comp_idx) > 1 else np.nan
        adv_s = max(0, s - 63)
        low_before = float(np.min(low[adv_s:s])) if s > adv_s else np.nan
        prior_adv = ((bh / low_before) - 1) * 100 if np.isfinite(low_before) and low_before > 0 else np.nan
        episodes.append({
            'start': s, 'end': e, 'len': span, 'compressed_frac': frac,
            'high': bh, 'low': bl, 'width_atr': width_atr,
            'width_pct': (bh - bl) / close[e] * 100 if close[e] else np.nan,
            'vol_decay': decay, 'cleanliness': clean, 'higher_lows_pct': hl_pct,
            'prior_advance_pct': prior_adv, 'state': 'FORMING',
        })
    if not episodes:
        return _attach(df, cols), []

    P = lambda name: f'{prefix}_{name}'
    live_bars, late_after = cfg['live_bars'], cfg['late_after']

    def clear_trigger(j):
        for c in TRIGGER_COLS:
            cols[P(c)][j] = np.nan
        cols[P('Has_Trigger')][j] = False
        cols[P('Days_Since_Trigger')][j] = -1

    def frozen(j, ep, bid):
        cols[P('ID')][j] = bid
        cols[P('Len')][j] = ep['len']
        cols[P('Start')][j] = df.index[ep['start']]
        cols[P('End')][j] = df.index[ep['end']]
        cols[P('High')][j] = ep['high']
        cols[P('Low')][j] = ep['low']
        cols[P('Width_ATR')][j] = ep['width_atr']
        cols[P('Planned_Trigger')][j] = round(ep['high'] * 1.001, 2)

    # Episodes are processed in time order and a later episode always overwrites (F4).
    for bid, ep in enumerate(episodes, start=1):
        s, e = ep['start'], ep['end']
        ep['id'] = bid
        for i in range(s, e + 1):
            clear_trigger(i)                                   # F4
            cols[P('ID')][i] = bid
            cols[P('Len')][i] = i - s + 1
            cols[P('Start')][i] = df.index[s]
            cols[P('End')][i] = df.index[i]
            geo = [k for k in range(s, i + 1) if _geo_ok(k, high, low, adr, cfg)] or list(range(s, i + 1))
            cols[P('High')][i] = float(np.max(high[geo]))
            cols[P('Low')][i] = float(np.min(low[geo]))
            a = atr[i]
            if np.isfinite(a) and a > 0:
                cols[P('Width_ATR')][i] = (cols[P('High')][i] - cols[P('Low')][i]) / a
            cols[P('State')][i] = 'READY' if (i - s + 1) >= cfg['min_len'] else 'FORMING'
            cols[P('Invalidate_Below')][i] = cols[P('Low')][i]
            cols[P('Planned_Trigger')][i] = round(cols[P('High')][i] * 1.001, 2)

        trig = broke = None
        for j in range(e + 1, min(n, e + 1 + live_bars)):
            if close[j] > ep['high']:
                trig = j
                break
            if close[j] < ep['low']:
                broke = j
                break

        if trig is not None:
            ep['trigger'] = trig
            ep['state'] = 'TRIGGERED'
            vr = vol[trig] / vol20[trig] if np.isfinite(vol20[trig]) and vol20[trig] > 0 else np.nan
            risk_pct_t = (close[trig] - low[trig]) / close[trig] * 100 if close[trig] else np.nan
            adr_pct_t = adr[trig] / close[trig] * 100 if close[trig] and np.isfinite(adr[trig]) else np.nan
            # bars between the base end and the trigger are ARMED
            for j in range(e + 1, trig):
                clear_trigger(j)
                frozen(j, ep, bid)
                cols[P('State')][j] = 'ARMED'
                cols[P('Invalidate_Below')][j] = ep['low']
            failed_at = None
            for j in range(trig, min(n, trig + cfg['post_trigger_bars'] + 1)):
                dsb = j - trig
                frozen(j, ep, bid)
                if failed_at is None and j > trig and close[j] < low[trig]:   # F1
                    failed_at = j
                if failed_at is not None:
                    st = 'BO_FAILED'
                else:
                    st = 'TRIGGERED' if dsb <= late_after else 'SPENT'
                cols[P('State')][j] = st
                cols[P('Has_Trigger')][j] = True
                cols[P('Trigger_Date')][j] = df.index[trig]
                cols[P('Trigger_Close')][j] = close[trig]
                cols[P('Days_Since_Trigger')][j] = dsb
                cols[P('Invalidate_Below')][j] = float(low[trig])
                cols[P('Trigger_Vol_Ratio')][j] = vr
                cols[P('Trigger_Risk_ADR')][j] = risk_pct_t / adr_pct_t if adr_pct_t else np.nan
            if failed_at is not None:
                ep['state'] = 'BO_FAILED'
        else:
            last = min(n - 1, e + live_bars)
            ep['state'] = 'FAILED' if broke is not None else 'EXPIRED'
            for j in range(e + 1, last + 1):
                clear_trigger(j)
                frozen(j, ep, bid)
                if broke is not None and j >= broke:
                    st = 'FAILED'
                elif j >= e + live_bars:
                    st = 'EXPIRED'
                else:
                    st = 'ARMED'
                cols[P('State')][j] = st
                cols[P('Invalidate_Below')][j] = ep['low']

    for i in range(n):
        bid = cols[P('ID')][i]
        if bid:
            ep = episodes[int(bid) - 1]
            cols[P('Vol_Decay')][i] = ep['vol_decay']
            cols[P('Cleanliness')][i] = ep['cleanliness']
            cols[P('HigherLows_Pct')][i] = ep['higher_lows_pct']
            cols[P('Prior_Advance_Pct')][i] = ep['prior_advance_pct']
            cols[P('Width_Pct')][i] = ep['width_pct']
            cols[P('Compressed_Pct')][i] = ep['compressed_frac']
    ends = np.array([ep['end'] for ep in episodes])
    for i in range(n):
        cols[P('Count_126')][i] = int(((ends <= i) & (ends > i - 126)).sum())
    return _attach(df, cols), episodes


def snapshot(df, prefix='BaseS', idx=-1, cfg_width=np.nan):
    """The last-row view used by the gates. Carries the family's own limits (v5.3)."""
    r = df.iloc[idx]
    fam = BY_PREFIX.get(prefix, {})
    P = lambda name: f'{prefix}_{name}'

    def get(name, d=np.nan):
        return r[P(name)] if P(name) in r.index else d

    def num(name, d=np.nan):
        v = get(name, d)
        try:
            return float(v) if pd.notna(v) else d
        except Exception:
            return d

    wmax = cfg_width if np.isfinite(cfg_width) else fam.get('width_atr_max', np.nan)
    return {
        'family': prefix,
        'family_name': fam.get('name', prefix),
        'width_max': wmax,
        'len_min': fam.get('min_len', 5),
        'len_max': fam.get('max_len', 40),
        'id': int(num('ID', 0) or 0),
        'state': str(get('State', 'NONE')),
        'len': int(num('Len', 0) or 0),
        'high': num('High'),
        'low': num('Low'),
        'width_atr': num('Width_ATR'),
        'width_pct': num('Width_Pct'),
        'vol_decay': num('Vol_Decay'),
        'cleanliness': num('Cleanliness'),
        'higher_lows_pct': num('HigherLows_Pct'),
        'prior_advance_pct': num('Prior_Advance_Pct'),
        'count_126': int(num('Count_126', 0) or 0),
        'compressed_pct': num('Compressed_Pct'),
        'trigger_date': get('Trigger_Date'),
        'trigger_close': num('Trigger_Close'),
        'trigger_vol_ratio': num('Trigger_Vol_Ratio'),
        'trigger_risk_adr': num('Trigger_Risk_ADR'),
        'days_since_trigger': int(num('Days_Since_Trigger', -1)),
        'invalidate_below': num('Invalidate_Below'),
        'planned_trigger': num('Planned_Trigger'),
    }
