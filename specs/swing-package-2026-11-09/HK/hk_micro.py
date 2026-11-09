#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HK market microstructure helpers (v6.5).

Everything here is used only when the profile is HK. US behaviour is untouched.

Three facts drive this module:
  1. HK tick sizes are price-banded, so a trigger price of 245.06 on a 244.20 stock
     is not a price anyone can enter.
  2. HK has early-close sessions (Christmas Eve, Lunar New Year Eve ...) whose volume is
     roughly half a normal day, which the compression test would otherwise read as dry-up.
  3. Suspended or untraded sessions leave zero-volume bars; a run of them looks like a
     perfectly quiet base.
"""
from datetime import timedelta

import numpy as np
import pandas as pd

# HKEX tick table (spread table), by price band lower bound.
_TICK_BANDS = [
    (0.01, 0.001), (0.25, 0.005), (0.50, 0.010), (10.0, 0.020),
    (20.0, 0.050), (100.0, 0.100), (200.0, 0.200), (500.0, 0.500),
    (1000.0, 1.000), (2000.0, 2.000), (5000.0, 5.000),
]


def tick_size(price):
    """Legal minimum price increment for a HK stock at this price."""
    if not np.isfinite(price) or price <= 0:
        return np.nan
    tick = _TICK_BANDS[0][1]
    for lower, t in _TICK_BANDS:
        if price >= lower:
            tick = t
    return tick


def round_to_tick(price, side='up'):
    """Snap a price to a legal tick. side='up' for a buy-stop, 'down' for a stop-loss."""
    t = tick_size(price)
    if not np.isfinite(t) or not np.isfinite(price):
        return price
    # float safety: 0.07/0.01 == 7.000000000000001 would ceil to 8
    n = round(price / t, 6)
    n = np.ceil(n) if side == 'up' else np.floor(n)
    return round(n * t, 6)


def tick_pct(price):
    t = tick_size(price)
    return (t / price * 100) if np.isfinite(t) and price else np.nan


def untraded_bars(high, low, vol):
    """True where a bar carries no turnover at all (suspension / no trading)."""
    high = np.asarray(high, float)
    low = np.asarray(low, float)
    vol = np.asarray(vol, float)
    return ~(np.isfinite(vol) & (vol > 0) & np.isfinite(high) & np.isfinite(low))


def count_untraded_in(untraded, start, end):
    """How many untraded bars sit inside a base span (inclusive)."""
    if start is None or end is None or end < start:
        return 0
    return int(np.sum(untraded[int(start):int(end) + 1]))
