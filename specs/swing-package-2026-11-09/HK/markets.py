#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Market profiles (v6.0) — the only place a market is described.

Why this file exists
--------------------
The engine is market-agnostic except for six constants: the relative-strength benchmark,
the regime index, the trading calendar, the time zone, the sheet block key, and the
leader-gate thresholds (price / turnover / RS). Instead of forking the engine, those live
here and the engine reads `PROFILE`.

  SWING_MARKET=us  (default)  SPY vs ^IXIC, NYSE calendar
  SWING_MARKET=hk            2800.HK vs 2800.HK, XHKG calendar

Benchmark note (HK)
-------------------
2800.HK (Tracker Fund) is used instead of ^HSI on purpose: every stock is fetched with
`auto_adjust=True` (dividends included), while ^HSI is a price index (dividends excluded).
Mixing the two hands every dividend payer a free edge in RS. Measured on 16 HK names,
switching from ^HSI to 2800.HK moves RS by a constant -0.7 and flips **zero** names across
the 10.0 leader threshold — same signal, consistent accounting.
"""
import os
import re

PROFILES = {
    'us': {
        'name': 'US', 'currency': 'USD',
        'bench': 'SPY', 'index': '^IXIC',
        'calendar': 'NYSE', 'tz': 'America/New_York', 'close_hour': 16,
        'sheet_key': '美股',
        # leader gate
        'rs_min': 10.0, 'price_min': 5.0, 'dollar_vol_min': 20e6,
    },
    'hk': {
        'name': 'HK', 'currency': 'HKD',
        'bench': '2800.HK', 'index': '2800.HK',
        'calendar': 'XHKG', 'tz': 'Asia/Hong_Kong', 'close_hour': 16,
        'sheet_key': '港股',
        # liquidity is pre-filtered in TradingView (user decision, 2026-11-06),
        # so the scanner records turnover but does not gate on it
        'rs_min': 10.0, 'price_min': 1.0, 'dollar_vol_min': 0.0, 'tick': True,
    },
}


MARKER = '.swing_market'      # v6.9: an install pins its market here


def _install_market():
    """Read the marker next to this file so any single script knows its market.

    A HK-only install must not fall back to US just because SWING_MARKET is unset:
    run_l2.sh is a sibling of run_daily.sh, so run_daily's export never reaches it.
    """
    try:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), MARKER)
        if os.path.exists(p):
            v = open(p, encoding='utf-8').read().strip().lower()
            if v in PROFILES:
                return v
    except Exception:
        pass
    return None


def verdicts_filename(name=None):
    """verdicts_<market>.jsonl — HK never looks for a file called *_US.jsonl."""
    return 'verdicts_%s.jsonl' % load(name)['name'].lower()


def verdicts_path(folder, name=None):
    """The verdicts file for this run; a legacy verdicts_US.jsonl is still honoured."""
    primary = os.path.join(folder, verdicts_filename(name))
    legacy = os.path.join(folder, 'verdicts_US.jsonl')
    if os.path.exists(primary):
        return primary
    if os.path.exists(legacy):
        return legacy
    return primary


def load(name=None):
    """Return the profile dict. Unknown/missing name falls back to US."""
    key = (name or os.environ.get('SWING_MARKET') or _install_market() or 'us').strip().lower()
    return dict(PROFILES.get(key, PROFILES['us']), key=key if key in PROFILES else 'us')


CUR = {'USD': '$', 'HKD': 'HK$'}


def currency_symbol(profile):
    """v6.4: one place that turns 'HKD' into 'HK$'."""
    return CUR.get(profile.get('currency', 'USD'), '$')


def normalize_ticker(ticker, profile):
    """HK codes come as 700 / 0700 / 9988 / 9988.HK; Yahoo wants 4-digit + .HK."""
    t = str(ticker).strip().upper()
    if profile.get('name') != 'HK':
        return t
    if t.startswith('^'):
        return t
    if t.endswith('.HK'):
        head = t[:-3]
        return f'{head.lstrip("0").zfill(4)}.HK' if head.isdigit() else t
    if t.isdigit():
        # '00700' / '00005' must become 0700 / 0005, not 00700 / 00005 (v6.4, #8)
        return f'{t.lstrip("0").zfill(4)}.HK'
    return t


def display_ticker(ticker, profile):
    """Strip the exchange suffix for file names and the contract."""
    t = str(ticker).strip().upper()
    return re.sub(r'\.HK$', '', t) if profile.get('name') == 'HK' else t
