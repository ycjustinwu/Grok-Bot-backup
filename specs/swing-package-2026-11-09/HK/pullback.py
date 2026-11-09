#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pullback family (B / D / H) and the bottom-reversal setup (E) — v5.3.

Stop formulas (one place, so layer 2 and the user read the same thing):

  PB_STRUCT = min( support confluence - 0.5*ATR , lowest low of the last 3 bars )   # B
  MA_STRUCT = min( MA20 - 0.5*ATR              , lowest low of the last 3 bars )   # D
  SR_STRUCT = min( SR_Flip_Level - 0.5*ATR     , lowest low of the last 3 bars )   # H
  VP_STRUCT = min( POC - 0.5*ATR               , lowest low of the last 3 bars )   # E

"min" is deliberate: the stop sits below both the level and the swing low it protects.

B / D / H (pullbacks in an uptrend) share three preconditions: uptrend (Minervini or soft),
a real pullback (>= 0.5 ATR off the 8-bar high) and a *low-momentum* decline.

E (v5.3, F8) is a true bottom reversal and deliberately does NOT require an uptrend:
  * the stock is NOT in a Minervini trend (otherwise it is not a bottom);
  * a meaningful decline: the 60-bar low sits >= 25% under the prior 252-bar high;
  * the low is 5-40 bars old, and a higher low (>= 1% above it) has formed since;
  * the stock has reclaimed value: close > POC_60D and close > MA20, MA20 rising;
  * accumulation since the low: up-day volume >= 1.2 x down-day volume.
It lives in its own family REVERSAL (own risk band and room floor in gates.py).

v5.3 also returns a per-candidate `valid` flag (F5): a pullback only competes with a base
when it passes its own checks; gates.py no longer lets a failing pullback mask a live base.
"""
import numpy as np
import pandas as pd

PULLBACK_DEPTH_ATR = 0.5
PULLBACK_LOOKBACK = 8
RECENT_LOW_BARS = 3
NEAR_PCT = 3.0
MAX_RANGE_ADR = 1.5
MAX_VOL_RATIO = 1.3
STOP_ATR_BUFFER = 0.5

# E — bottom reversal (all PICK, see CHANGELOG_v53.md)
REV_LOOKBACK = 60
REV_MIN_DRAWDOWN_PCT = 25.0
REV_LOW_AGE = (5, 40)
REV_HIGHER_LOW_PCT = 1.0
REV_UPDOWN_VOL = 1.2


def _num(v, d=np.nan):
    try:
        return float(v) if pd.notna(v) else d
    except Exception:
        return d


def _uptrend(row):
    if _num(row.get('Minervini_Trend_Basic'), 0) == 1:
        return True, 'Minervini'
    close, ma20, ma50 = _num(row.get('Close')), _num(row.get('MA20')), _num(row.get('MA50'))
    slope = _num(row.get('SMA50_Slope'))
    if all(np.isfinite(x) for x in (close, ma20, ma50, slope)) and \
            close > ma50 and close > ma20 and slope > 0:
        return True, 'soft trend'
    return False, 'no trend'


def bottom_reversal(row, df):
    """Setup E. Returns a candidate dict (valid True/False with reasons) or None."""
    if _num(row.get('Minervini_Trend_Basic'), 0) == 1:
        return None
    close, atr = _num(row.get('Close')), _num(row.get('ATR'))
    if not (np.isfinite(close) and np.isfinite(atr) and atr > 0) or len(df) < REV_LOOKBACK + 5:
        return None
    win = df.tail(REV_LOOKBACK)
    lows = win['Low'].to_numpy(float)
    li = int(np.argmin(lows))
    L = float(lows[li])
    age = len(win) - 1 - li
    if not (REV_LOW_AGE[0] <= age <= REV_LOW_AGE[1]):
        return None
    pre = df['High'].iloc[:len(df) - len(win) + li + 1].tail(252)
    hi_before = float(pre.max()) if len(pre) else np.nan
    dd = (hi_before - L) / hi_before * 100 if np.isfinite(hi_before) and hi_before > 0 else np.nan
    if not (np.isfinite(dd) and dd >= REV_MIN_DRAWDOWN_PCT):
        return None
    after = win.iloc[li + 3:] if li + 3 < len(win) else win.iloc[0:0]
    hl = float(after['Low'].min()) if len(after) else np.nan

    poc, ma20 = _num(row.get('POC_60D')), _num(row.get('MA20'))
    ma20_slope = _num(row.get('MA20_Slope'))
    since = win.iloc[li + 1:]
    up = since['Close'].diff() > 0
    vol_up = float(since['Volume'][up].sum())
    vol_dn = float(since['Volume'][~up].sum())
    ud = vol_up / vol_dn if vol_dn > 0 else np.nan

    checks = [
        (np.isfinite(hl) and hl >= L * (1 + REV_HIGHER_LOW_PCT / 100),
         f'higher low {hl:.2f} vs low {L:.2f}' if np.isfinite(hl) else 'no higher low yet'),
        (np.isfinite(poc) and close > poc, f'close {close:.2f} vs POC {poc:.2f}'),
        (np.isfinite(ma20) and close > ma20 and np.isfinite(ma20_slope) and ma20_slope > 0,
         f'close vs MA20 {ma20:.2f}, MA20 slope {ma20_slope:+.1f}%'),
        (np.isfinite(ud) and ud >= REV_UPDOWN_VOL, f'up/down volume {ud:.2f} (need {REV_UPDOWN_VOL})'),
    ]
    valid = all(ok for ok, _ in checks)
    swing3 = float(df['Low'].tail(RECENT_LOW_BARS).min())
    stop_poc = poc - STOP_ATR_BUFFER * atr if np.isfinite(poc) else np.nan
    stop = float(np.nanmin([stop_poc, swing3]))
    fails = [t for ok, t in checks if not ok]
    return dict(
        code='E', name='Bottom Reversal', family='REVERSAL', stop_type='VP_STRUCT',
        anchor=poc, stop=float(stop), valid=valid,
        why=(f'drawdown {dd:.0f}% to {L:.2f} ({age} bars ago); ' + '; '.join(t for _, t in checks))
        if valid else ('bottom reversal incomplete: ' + '; '.join(fails)),
        drawdown_pct=dd, reversal_low=L, higher_low=hl,
        higher_low_pct=((hl / L - 1) * 100) if (np.isfinite(hl) and L) else np.nan,
        updown_vol=ud,
    )


def evaluate(row, df):
    """Return the best setup dict (valid ones first), or None. Never raises."""
    close = _num(row.get('Close'))
    atr = _num(row.get('ATR'))
    adr = _num(row.get('ADR'))
    vol20 = _num(row.get('Vol_Avg_20'))
    if not (np.isfinite(close) and np.isfinite(atr) and atr > 0):
        return None

    candidates = []
    rev = bottom_reversal(row, df)
    if rev is not None:
        candidates.append(rev)

    ok_trend, trend_src = _uptrend(row)
    recent = df.tail(PULLBACK_LOOKBACK)
    depth_atr = rng_ratio = vol_ratio = np.nan
    low_momentum = False
    swing_low = float(df['Low'].tail(RECENT_LOW_BARS).min()) if len(df) else np.nan
    if ok_trend and len(recent) >= 4:
        hi8 = float(recent['High'].max())
        depth_atr = (hi8 - close) / atr
        last3 = recent.tail(RECENT_LOW_BARS)
        rng3 = float((last3['High'] - last3['Low']).mean())
        vol3 = float(last3['Volume'].mean())
        rng_ratio = rng3 / adr if np.isfinite(adr) and adr > 0 else np.nan
        vol_ratio = vol3 / vol20 if np.isfinite(vol20) and vol20 > 0 else np.nan
        low_momentum = bool((rng_ratio <= MAX_RANGE_ADR) and (vol_ratio <= MAX_VOL_RATIO))

    if ok_trend and np.isfinite(depth_atr) and depth_atr >= PULLBACK_DEPTH_ATR:
        ma10, ma20 = _num(row.get('MA10')), _num(row.get('MA20'))
        poc = _num(row.get('POC_60D'))
        avwap_low = _num(row.get('AVWAP_20D_Low'))
        sr_level = _num(row.get('SR_Flip_Level'))
        sr_active = bool(row.get('SR_Flip_Active', False))
        dist_ma10 = _num(row.get('Dist_from_MA10_Pct'))
        stage2 = _num(row.get('Minervini_Stage2_Strict'), 0) == 1
        momo = f'decline {rng_ratio:.2f}xADR range, {vol_ratio:.2f}x volume'

        def near(level):
            return np.isfinite(level) and level > 0 and abs(close - level) / level * 100 <= NEAR_PCT

        def below(level):
            return np.isfinite(level) and level < close

        anchors = [a for a in (ma20, avwap_low, poc, sr_level) if below(a) and near(a)]
        if anchors:
            anchor = max(anchors)
            candidates.append(dict(
                code='B', name='Pullback Support', family='PULLBACK', stop_type='PB_STRUCT',
                anchor=anchor, stop=min(anchor - STOP_ATR_BUFFER * atr, swing_low), valid=low_momentum,
                why=f'pullback {depth_atr:.1f}ATR to support {anchor:.2f}; {momo}'))
        if stage2 and np.isfinite(dist_ma10) and -2 <= dist_ma10 <= 3 and np.isfinite(ma20) and ma20 > 0:
            candidates.append(dict(
                code='D', name='Trend Respect', family='PULLBACK', stop_type='MA_STRUCT',
                anchor=ma10, stop=min(ma20 - STOP_ATR_BUFFER * atr, swing_low), valid=low_momentum,
                why=f'Stage2, close {dist_ma10:+.1f}% vs MA10, stop below MA20; {momo}'))
        if sr_active and np.isfinite(sr_level) and near(sr_level):
            candidates.append(dict(
                code='H', name='S/R Flip Retest', family='PULLBACK', stop_type='SR_STRUCT',
                anchor=sr_level, stop=min(sr_level - STOP_ATR_BUFFER * atr, swing_low), valid=low_momentum,
                why=f'retest of flipped level {sr_level:.2f} (age {_num(row.get("SR_Flip_Age"), -1):.0f} bars); {momo}'))

    if not candidates:
        return None
    # valid first; then B > H > D > E; ties broken by the tighter stop
    order = {'B': 0, 'H': 1, 'D': 2, 'E': 3}
    candidates.sort(key=lambda c: (not c['valid'], order[c['code']], close - c['stop']))
    best = dict(candidates[0])
    best.update({
        'confluence_count': len(anchors) if 'anchors' in locals() else np.nan,
        'entry': close,
        'entry_src': 'at market (close)',
        'depth_atr': depth_atr,
        'low_momentum': low_momentum if best['code'] != 'E' else True,
        'range_ratio': rng_ratio,
        'vol_ratio': vol_ratio,
        'swing_low': swing_low,
        'trend_src': trend_src,
        'risk_pct': (close - best['stop']) / close * 100 if close else np.nan,
        'candidates': ','.join(c['code'] + ('' if c['valid'] else '-') for c in candidates),
    })
    return best
