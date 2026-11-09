#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =====================================================================
# 🇺🇸 美股 Swing Trade 數據分析系統 v5.5 - 1f.2 "quality inputs for L2 + workflow"
#   - breakout failure state, WIDE swallow fix, max_len, trigger-field reset (base_layer.py)
#   - supply measured from the ENTRY; breakout volume confirmation; risk re-measured after
#     the trigger; buy-stop max stop; true bottom reversal E (gates.py / pullback.py)
#   - S/R flip = real retest (levels.py); per-family invariants + evidence reconciliation
#   - earnings in sessions from the as-of date; RS never shown as 0; ~500 bars of history
# =====================================================================
# 🇺🇸 美股 Swing Trade 數據分析系統 v5.0 - 1d "per-bar levels + breadth header"
# 1d changes:
#   - AVWAP (low/high/HVD), POC/VAH/VAL and the S/R flip are now computed for EVERY bar
#     (levels.py) instead of only the last row. Replay and pullback confluence now see them.
#   - Universe breadth (% of the scanned names above MA50) is printed with the regime header.
# v5.1 - regime now comes from the user's daily dashboard sheet (市況 label + % >50D + 10日比率),
#        with the NASDAQ 10/20EMA read as a second opinion; FVG is per-bar.
# =====================================================================
# v4.9 - 1c "two base families + pullbacks + regime"
# 1c changes:
#   - Base layer now runs TWO detectors: STRICT (5-30d, no gaps) and WIDE (10-40d, <=2 gaps,
#     >=60% compressed, geometry excludes outlier bars). Both exported; gates pick the best.
#   - Pullback family B/D/E/H with explicit PB_STRUCT / MA_STRUCT / VP_STRUCT / SR_STRUCT.
#   - Market regime header (NASDAQ 10EMA vs 20EMA) — a banner, never a score input.
# =====================================================================
# v4.8 - 1b "base + gates" (from v4.7)
# 1b changes:
#   - Base episode layer (base_layer.py): maximal run of compressed bars, 5–30d,
#     frozen geometry, explicit trigger. Replaces the zone machine as the source of
#     Setup_OK. (v5.2) the old Tight_Zone_* / RR / target machinery was deleted outright.
#   - Three gates (gates.py): Leader_OK / Setup_OK / Risk_OK + Candidate_Class,
#     each with a reason string carrying the numbers.
#   - Priority_Score is now leader-quality only (0–65). BUY/STALK/WATCH verdicts are gone:
#     Screen_Flag is a class label, not a verdict.
#   - Contract_US.csv / Trigger_US.csv / Evidence_US.csv added.
# =====================================================================
# v4.7 - 1a "truth pass" (from v4.6)
# 1a changes (design v1, batch 1a — corrections only, no new subjective gates):
#   - RR leaves the score entirely (it measured 1/risk, not reward/risk)
#   - Score_Breakdown emitted; sum(terms) must equal Priority_Score
#   - Room_To_Supply_R: prior-anchored supply distance in R (diagnostic)
#   - Weak_Day_RS_Pct forward-filled (doc promise, code never did it)
#   - RS fetch failure => NaN + RS_Status=UNKNOWN (was silent 0)
#   - Screen_Flag replaces Action_Refined (alias kept, DEPRECATED)
#   - RULEBOOK_US.md generated with provenance + ENFORCED/DOC_ONLY
# NOT in 1a: zone geometry, Prior_Zone_*, gates, Contract/Trigger files
# =====================================================================
# v4.6 - Local CSV Enhanced (lineage: 4.6.1 + 60m-bar fallback)
# Based on US_swing_v4.5.2 + Colab v4.6 reliability, plus bugfixes:
#   - completed-session gate (mcal optional), retry, shared SPY, DQ log
#   - safe column rename (no capitalize mangling)
#   - AVWAP duplicate-date safe
#   - breakdown/slapback zone TTL (no stale zone forever)
#   - earnings failure => UNKNOWN (not CLEAR)
#   - RR div0 guard, prior-day resistance for targets
#   - real FVG fill check, ticker sanitize, vectorized HH/HL + tight zone
#   - Target_1 = Resistance_20D (never Prior/support); T2/T3 extensions ascending
#   - Tight Zone v2.1: vol<0.85×20MA, range≤1.20×ADR, 2–10 days, 2 exceptions,
#     Minervini OR soft trend (Close>MA50 & Close>MA20 & SMA50_Slope>0)
# =====================================================================

import json
import os
import re
import time
import warnings
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import yfinance as yf

import base_layer
import hk_micro
import gates
import levels
import pullback
import regime
import markets

try:
    import pandas_market_calendars as mcal
except ImportError:
    mcal = None

warnings.filterwarnings('ignore')

# =====================================================================
# Config
# =====================================================================
OUTPUT_FOLDER = os.environ.get('SWING_OUTPUT_FOLDER', 'swing_data_us')
DEFAULT_TICKERS = ['AAPL', 'NVDA']
MONTHS = 12          # v5.3 F13: ~500 bars so MA200 / 52W exist on replays
MIN_BARS = 50
LATEST_SESSION_BUFFER_MINUTES = 60
MAX_DOWNLOAD_RETRIES = 3
FETCH_TIMEOUT = 30
TZ_STATE_TTL_DAYS = 5          # trading days after zone ends before stale reset
INTER_TICKER_SLEEP_SEC = 0.35  # gentle on Yahoo

# Tight-zone module v2.1 (loosened hit-rate)
BREAKDOWN_VOL_THRESHOLD = 1.2
TIGHT_VOL_THRESHOLD = 0.85          # was 0.70
TIGHT_RANGE_MULT = 1.20             # daily range <= 1.20 × ADR (was 1.0×)
TZ_MIN_DAYS = 2                     # was 3
TZ_MAX_DAYS = 10                    # was 7
TZ_MAX_EXCEPTIONS = 2               # was 1 non-tight day
MINI_BO_VOL_MULT = 1.5
SLAPBACK_VOL_MULT = 1.5
SLAPBACK_CLOSE_QUALITY = 0.85
BREAKDOWN_DEPTH = 0.015

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    print(f"📁 已創建資料夾: {OUTPUT_FOLDER}")


# =====================================================================
# Small helpers
# =====================================================================
def sanitize_ticker(raw):
    t = str(raw).strip().upper().replace('/', '-').replace('\\', '-')
    t = markets.normalize_ticker(t, PROFILE)      # HK: 700 -> 0700.HK
    if not re.fullmatch(r'[A-Z0-9.\-]{1,15}', t):
        raise ValueError(f"Invalid ticker symbol: {raw!r}")
    return t


def normalize_yf_columns(df):
    """Map yfinance columns to stable names without capitalize() mangling."""
    mapping = {
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume',
        'adj close': 'Adj_Close',
        'adj_close': 'Adj_Close',
        'dividends': 'Dividends',
        'stock splits': 'Stock_Splits',
        'stock_splits': 'Stock_Splits',
    }

    def norm(c):
        if isinstance(c, tuple):
            # (ticker, field) or (field, '')
            for part in c:
                if isinstance(part, str) and part.strip():
                    c = part
                    break
        if not isinstance(c, str):
            return c
        key = c.strip().lower()
        if key in mapping:
            return mapping[key]
        return re.sub(r'\s+', '_', c.strip())

    return df.rename(columns={c: norm(c) for c in df.columns})


def clean_price_rows(df):
    if df is None or len(df) == 0:
        return df
    df = df.copy()
    ohlc_cols = ['Open', 'High', 'Low', 'Close']
    for c in ohlc_cols:
        if c not in df.columns:
            return df
    df = df.dropna(subset=ohlc_cols)
    df = df[df['Close'] > 0]
    return df


def strip_tz_for_export(df):
    """Excel/CSV cannot store timezone-aware datetimes."""
    df = df.copy()
    if hasattr(df.index, 'tz') and df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            try:
                if df[col].dt.tz is not None:
                    df[col] = df[col].dt.tz_localize(None)
            except Exception:
                df[col] = df[col].astype(str)
        elif df[col].dtype == object:
            def strip_cell(v):
                if isinstance(v, pd.Timestamp) and v.tzinfo is not None:
                    return v.tz_localize(None)
                return v
            df[col] = df[col].apply(strip_cell)
    return df


def append_data_quality_record(records, ticker, status, expected_date,
                               actual_date=None, attempts=0, rows=0, error=''):
    if records is None:
        return
    records.append({
        'Ticker': str(ticker).upper(),
        'Status': status,
        'Expected_Date': str(expected_date) if expected_date else '',
        'Actual_Last_Date': str(actual_date) if actual_date else '',
        'Attempts': attempts,
        'Rows': rows,
        'Error': error or '',
    })


def save_data_quality_report(records, output_folder=OUTPUT_FOLDER):
    if not records:
        return None
    quality_df = pd.DataFrame(records)
    quality_path = os.path.join(output_folder, 'Data_Quality_Report.csv')
    quality_df.to_csv(quality_path, index=False)
    print(f"\n📋 Data Quality Report：{quality_path}")
    print(quality_df.to_string(index=False))
    return quality_df


# =====================================================================
# Latest completed US session
# =====================================================================
def get_latest_completed_us_session(buffer_minutes=LATEST_SESSION_BUFFER_MINUTES):
    # SWING_ASOF=YYYY-MM-DD replays the screener as of a past session (used to verify the
    # trigger/contract output on days when no base is live). Earnings days-to is still
    # measured from the real clock, so replay is for structure only.
    override = os.environ.get('SWING_ASOF', '').strip()
    if override:
        return datetime.strptime(override, '%Y-%m-%d').date()
    now_utc = pd.Timestamp.now(tz='UTC')

    if mcal is not None:
        calendar = mcal.get_calendar(PROFILE['calendar'])
        schedule = calendar.schedule(
            start_date=(now_utc - pd.Timedelta(days=14)).date(),
            end_date=now_utc.date(),
        )
        if schedule is None or schedule.empty:
            raise RuntimeError('無法取得美股交易日曆')
        data_ready_time = schedule['market_close'] + pd.Timedelta(minutes=buffer_minutes)
        completed = schedule[data_ready_time <= now_utc]
        if completed.empty:
            raise RuntimeError('找不到已完成且已超過資料緩衝時間的美股交易日')
        return completed.index[-1].date()

    # Fallback without mcal: last Mon–Fri that is fully past US market close
    # (16:00 ET) + buffer. Holidays may make Yahoo miss that date — retry/DQ
    # will surface it; install pandas_market_calendars for exact NYSE calendar.
    now_et = now_utc.tz_convert(PROFILE['tz'])
    day = now_et.date()
    for _ in range(14):
        if day.weekday() < 5:  # Mon–Fri
            ready = pd.Timestamp(year=day.year, month=day.month, day=day.day,
                                 hour=PROFILE['close_hour'], minute=0, tz=PROFILE['tz'])
            ready = ready + pd.Timedelta(minutes=buffer_minutes)
            if now_et >= ready:
                return day
        day = day - timedelta(days=1)
    raise RuntimeError('找不到已完成且已超過資料緩衝時間的美股交易日')


# =====================================================================
# Download with retry / expected-session validation
# =====================================================================
def synthesize_daily_bar(ticker, day, tz=None, silent=True):
    """Rebuild one missing daily bar from Yahoo's 60-minute bars for that session.

    2026-11-03: Yahoo served the daily bar with Open/High/Low/Close all NaN while the 60m series for
    the same day was complete, so every ticker failed `缺少預期交易日` and the whole scan aborted.
    Same provider, same session, no invented price — O/H/L/C/V are aggregated from its own intraday
    bars. Returns a one-row DataFrame (or None when the intraday series is empty/invalid).
    """
    try:
        intra = yf.Ticker(ticker).history(period='7d', interval='60m',
                                          auto_adjust=True, actions=False)
    except Exception:
        return None
    if intra is None or len(intra) == 0:
        return None
    intra = normalize_yf_columns(intra)
    mask = [pd.Timestamp(i).date() == day for i in intra.index]
    sel = intra[mask]
    if len(sel) == 0:
        return None
    sel = sel.dropna(subset=['Open', 'High', 'Low', 'Close'])
    if len(sel) == 0:
        return None
    idx = pd.Timestamp(day)
    if tz is not None:
        idx = idx.tz_localize(tz) if idx.tzinfo is None else idx.tz_convert(tz)
    row = pd.DataFrame({
        'Open': [float(sel['Open'].iloc[0])],
        'High': [float(sel['High'].max())],
        'Low': [float(sel['Low'].min())],
        'Close': [float(sel['Close'].iloc[-1])],
        'Volume': [float(sel['Volume'].sum()) if 'Volume' in sel.columns else 0.0],
    }, index=[idx])
    return row


def try_fetch_us_stock(ticker, start_date, expected_last_date,
                       max_retries=MAX_DOWNLOAD_RETRIES, silent=False):
    ticker = sanitize_ticker(ticker)
    end_exclusive = expected_last_date + timedelta(days=1)
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            df = yf.Ticker(ticker).history(
                start=start_date,
                end=end_exclusive,
                interval='1d',
                auto_adjust=True,
                actions=False,
                timeout=FETCH_TIMEOUT,
            )
            if df is None or len(df) == 0:
                raise RuntimeError('Yahoo 回傳空白 dataframe')

            df = normalize_yf_columns(df)
            missing_cols = [c for c in ['Open', 'High', 'Low', 'Close'] if c not in df.columns]
            if missing_cols:
                raise RuntimeError(f'缺少必要欄位：{missing_cols}')

            invalid_mask = (
                df[['Open', 'High', 'Low', 'Close']].isna().any(axis=1)
                | (df['Close'].fillna(0) <= 0)
            )
            if invalid_mask.any() and not silent:
                invalid_dates = [str(pd.Timestamp(i).date()) for i in df.index[invalid_mask]]
                print(f'⚠️ {ticker} Yahoo 無效 OHLC 日期：{invalid_dates}')

            df = clean_price_rows(df)
            df = df[pd.Index(df.index.date) <= expected_last_date]

            bar_source = 'DAILY'
            df['Bar_Source'] = 'DAILY'
            available_dates = {pd.Timestamp(i).date() for i in df.index}
            if expected_last_date not in available_dates:
                synth = synthesize_daily_bar(ticker, expected_last_date,
                                             tz=getattr(df.index, 'tz', None), silent=silent)
                if synth is not None:
                    df = pd.concat([df, synth])
                    df = df[~df.index.duplicated(keep='last')].sort_index()
                    bar_source = 'SYNTH_60M'      # v6.4: a provisional bar must not fake a signal
                    df.loc[df.index[-1], 'Bar_Source'] = 'SYNTH_60M'
                    if not silent:
                        print(f'⚠️ {ticker} daily bar 缺 {expected_last_date}，已用同日 60m bar 合成'
                              f'（O/H/L/C/V，收 {float(synth["Close"].iloc[0]):.2f}）')
                    available_dates = {pd.Timestamp(i).date() for i in df.index}
                if expected_last_date not in available_dates:
                    actual_last = pd.Timestamp(df.index[-1]).date() if len(df) else None
                    raise RuntimeError(
                        f'缺少預期交易日 {expected_last_date}；目前最後有效日期為 {actual_last}'
                    )

            if attempt > 1 and not silent:
                print(f'✅ {ticker} 第 {attempt} 次下載成功，已取得 {expected_last_date}')
            return df, ticker, attempt, None

        except Exception as e:
            last_error = e
            if not silent:
                print(f'⚠️ {ticker} 下載嘗試 {attempt}/{max_retries} 失敗：{type(e).__name__}: {e}')
            if attempt < max_retries:
                wait_seconds = 5 * attempt
                if not silent:
                    print(f'⏳ 等待 {wait_seconds} 秒後重試')
                time.sleep(wait_seconds)

    error_message = f'{type(last_error).__name__}: {last_error}' if last_error is not None else '未知下載錯誤'
    print(f'❌ {ticker} 在 {max_retries} 次嘗試後仍無法取得 {expected_last_date} 的完整資料：{error_message}')
    return None, None, max_retries, error_message


earnings_overrides = {}        # v6.7: module-level default (was only set inside __main__)


def load_earnings_overrides(path='earnings_overrides.csv'):
    """Manual earnings dates, e.g. read off TradingView. {TICKER: (date, source)}.

    Only consulted when the API returns nothing, so it cannot overwrite a good date.
    HK tickers are the reason this exists: Yahoo leaves ~26% of them UNKNOWN (US: 3%).
    """
    out = {}
    if not os.path.exists(path):
        return out
    try:
        d = pd.read_csv(path, keep_default_na=False, dtype=str)
        for _, r in d.iterrows():
            t = str(r.get('Ticker', '')).strip().upper()
            v = str(r.get('Date', '')).strip()
            if not t or not v:
                continue
            try:
                val = (pd.Timestamp(v).date(), str(r.get('Source', 'override')).strip() or 'override')
            except Exception:
                continue
            # accept every spelling of the same code: 1071 / 1071.HK / 01071 / 01071.HK
            import markets as _mk
            # Aliases are keys only, so normalise with the HK profile even in a US run:
            # an override file may carry 01071 while the scanner keys on 1071.HK.
            prof = _mk.load('hk')
            aliases = {t, t.replace('.HK', ''), t + '.HK'}
            try:
                norm = _mk.normalize_ticker(t, prof)          # 01071 -> 1071.HK
                aliases |= {norm, norm.replace('.HK', '')}
            except Exception:
                pass
            for k in aliases:
                out[k] = val
    except Exception:
        return {}
    return out


def fetch_shared_spy(expected_last_date, months=MONTHS, silent=False):
    start_date = expected_last_date - timedelta(days=months * 30 + 365)
    spy_df, _, attempts, error = try_fetch_us_stock(
        ticker=PROFILE['bench'],
        start_date=start_date,
        expected_last_date=expected_last_date,
        max_retries=MAX_DOWNLOAD_RETRIES,
        silent=silent,
    )
    if spy_df is None:
        print(f"⚠️ {PROFILE['bench']} benchmark 無法取得。相對強度欄位將設為 NaN（RS_Status=UNKNOWN）。原因：{error}")
        return pd.DataFrame()
    if not silent:
        print(
            f"✅ {PROFILE['bench']} benchmark 已下載一次並供整批共用：{len(spy_df)} 日，"
            f'最後日期 {pd.Timestamp(spy_df.index[-1]).date()}，下載次數 {attempts}'
        )
    return spy_df


# =====================================================================
# AVWAP
# =====================================================================
def classify_rs_role(row):
    """leader vs candidate for Potential Setups / HANDOFF. Not a score input.
    Priority: RSNHBP → candidate; else leader; else early candidate; else blank.
    RS_Line_Up = RS_Line 20d change ≥ +1% (not raw Slope>0 — avoids ≈0 float bugs)."""
    rs = row.get('RS_Score', np.nan)
    try:
        rs = float(rs) if pd.notna(rs) else np.nan
    except Exception:
        rs = np.nan
    line_up = bool(row.get('RS_Line_Up', False))
    nh = bool(row.get('RS_Line_NH', False))
    rsnhbp = bool(row.get('RSNHBP', False))
    wdrs = row.get('Weak_Day_RS_Pct', np.nan)
    try:
        wdrs = float(wdrs) if pd.notna(wdrs) else np.nan
    except Exception:
        wdrs = np.nan
    if rsnhbp:
        return 'candidate'
    if pd.notna(rs) and rs > 20 and (line_up or nh):
        return 'leader'
    if line_up and (pd.notna(wdrs) and wdrs >= 60):
        return 'candidate'
    return ''


def _sessions_between(a, b):
    """v5.3 F11: NYSE sessions from as-of date a (exclusive) to date b (inclusive)."""
    a, b = pd.Timestamp(a).date(), pd.Timestamp(b).date()
    if b <= a:
        return 0
    if mcal is not None:
        try:
            sched = mcal.get_calendar(PROFILE['calendar']).schedule(start_date=a + timedelta(days=1), end_date=b)
            return int(len(sched))
        except Exception:
            pass
    return int(np.busday_count(a + timedelta(days=1), b + timedelta(days=1)))


def _date_str(r):
    """v5.3 F12: the session date of a last-row Series (index label or Date column)."""
    for v in (getattr(r, 'name', None), r.get('Date') if hasattr(r, 'get') else None):
        try:
            if v is not None and not isinstance(v, (int, np.integer)):
                return str(pd.Timestamp(v).date())
        except Exception:
            continue
    return ''


CLASS_TO_FLAG = {
    'A_SETUP': 'SETUP',
    'B_LEADER_WAIT': 'LEADER_WAIT',
    'C_WATCH': 'WATCH',
    'X_NONE': 'NONE',
}


def is_extended(row):
    """Red flag #1 only: too far above MA20, RSI overbought, or >25% above MA50."""
    ext20 = row.get('Extension_MA20_Pct', np.nan)
    rsi = row.get('RSI_14', np.nan)
    d50 = row.get('Dist_from_MA50_Pct', np.nan)
    return bool((pd.notna(ext20) and ext20 > 15) or (pd.notna(rsi) and rsi > 75)
                or (pd.notna(d50) and d50 > 25))


def calculate_priority_score(row):
    """Leader-quality score only (1b): a 0-65 sort key, never a verdict.

    Removed from the score in 1b (and why):
      * RR (+20) — measured 1/risk, see 1a;
      * Tight-Zone +20/+10 and Slap_Back +8 — they read the deprecated zone machine;
      * setup-tag +10/+8/+5 and Low_Vol_Grind -10 — those tags still depend on it;
      * volume expansion +5/+3/-5 and the "near 20d high" -10 — these are risk/room
        evidence, now expressed by Risk_OK instead of double-counted here;
      * earnings -30/-15/-5 — now a gate, not a ranking term.
    What remains is what the sources actually call leadership: trend, MA order, RS, RS quality.
    """
    terms = []

    def add(name, pts):
        pts = int(pts)
        if pts:
            terms.append((name, pts))

    if row.get('Minervini_Trend_Basic') == 1:
        add('MN', 20)
    close, ma20, ma50 = row.get('Close'), row.get('MA20'), row.get('MA50')
    if pd.notna(close) and pd.notna(ma20) and pd.notna(ma50) and close > ma20 and ma20 > ma50:
        add('MA', 10)

    rs = row.get('RS_Score', np.nan)
    rs = float(rs) if pd.notna(rs) else np.nan
    if pd.notna(rs):
        if rs > 20:
            add('RS', 30)
        elif rs > 10:
            add('RS', 20)
        elif rs > 0:
            add('RS', 10)

    q = 0
    if bool(row.get('RS_Line_Up', False)) and bool(row.get('RS_Line_NH', False)):
        q += 3
    wdrs = row.get('Weak_Day_RS_Pct', np.nan)
    try:
        wdrs = float(wdrs) if pd.notna(wdrs) else np.nan
    except Exception:
        wdrs = np.nan
    if pd.notna(wdrs) and wdrs >= 60:
        q += 2
    add('Q', min(5, q))

    if is_extended(row):
        add('EXT', -20)

    raw = sum(p for _, p in terms)
    score = max(0, min(100, int(raw)))
    if score != int(raw):
        add('CLAMP', score - int(raw))

    breakdown = '|'.join(f'{name}:{pts:+d}' for name, pts in terms)
    note = 'leader quality only (0-65); RR / zone / setup / earnings live in the gates'
    return score, breakdown, note


# =====================================================================
# Core fetch + indicators
# =====================================================================
def fetch_swing_data_us(ticker, months=MONTHS, silent=False,
                        expected_last_date=None, spy_df=None,
                        data_quality_records=None):
    ticker = sanitize_ticker(ticker)
    if not silent:
        print(f"\n{'=' * 60}\n🔍 正在分析：{ticker}\n{'=' * 60}")

    if expected_last_date is None:
        expected_last_date = get_latest_completed_us_session()

    start_date = expected_last_date - timedelta(days=months * 30 + 365)
    df, actual_ticker, fetch_attempts, fetch_error = try_fetch_us_stock(
        ticker=ticker,
        start_date=start_date,
        expected_last_date=expected_last_date,
        max_retries=MAX_DOWNLOAD_RETRIES,
        silent=silent,
    )

    if df is None or len(df) < MIN_BARS:
        actual_last_date = pd.Timestamp(df.index[-1]).date() if df is not None and len(df) else None
        append_data_quality_record(
            data_quality_records, ticker=ticker, status='FAILED_OR_STALE',
            expected_date=expected_last_date, actual_date=actual_last_date,
            attempts=fetch_attempts, rows=len(df) if df is not None else 0,
            error=fetch_error or f'下載後不足 {MIN_BARS} 個有效交易日',
        )
        if not silent:
            print(f'❌ 無法抓取 {ticker}')
        return None

    raw_len = len(df)
    df = clean_price_rows(df)

    if len(df) < MIN_BARS:
        append_data_quality_record(
            data_quality_records, ticker=ticker, status='FAILED_OR_STALE',
            expected_date=expected_last_date,
            actual_date=pd.Timestamp(df.index[-1]).date() if len(df) else None,
            attempts=fetch_attempts, rows=len(df),
            error=f'清理後不足 {MIN_BARS} 個有效交易日',
        )
        if not silent:
            print(f'❌ {ticker} 清理後無足夠有效數據')
        return None

    available_dates = {pd.Timestamp(i).date() for i in df.index}
    if expected_last_date not in available_dates:
        append_data_quality_record(
            data_quality_records, ticker=ticker, status='FAILED_OR_STALE',
            expected_date=expected_last_date,
            actual_date=pd.Timestamp(df.index[-1]).date(),
            attempts=fetch_attempts, rows=len(df),
            error='清理後缺少預期最新完整交易日',
        )
        if not silent:
            print(f'❌ {ticker} 清理後缺少 {expected_last_date}')
        return None

    removed_rows = raw_len - len(df)
    if not silent:
        print(f'🎯 預期最新完整交易日：{expected_last_date}')
        print(f'🔄 下載次數：{fetch_attempts}')
        print(f'✅ {actual_ticker}：{len(df)} 日，{df.index[0].date()} ~ {df.index[-1].date()}')
        if removed_rows > 0:
            print(f'🧹 已清除 {removed_rows} 行無效/空白尾部價格資料')

    append_data_quality_record(
        data_quality_records, ticker=ticker,
        status='OK' if fetch_attempts == 1 else 'RETRY_OK',
        expected_date=expected_last_date,
        actual_date=pd.Timestamp(df.index[-1]).date(),
        attempts=fetch_attempts, rows=len(df), error='',
    )

    # ---- Moving averages ----
    for w, n in [(10, 'MA10'), (20, 'MA20'), (50, 'MA50'), (150, 'MA150'), (200, 'MA200')]:
        df[n] = df['Close'].rolling(window=w).mean()
    df['MA10_Slope'] = ((df['MA10'] - df['MA10'].shift(10)) / df['MA10'].shift(10)) * 100
    df['MA20_Slope'] = ((df['MA20'] - df['MA20'].shift(10)) / df['MA20'].shift(10)) * 100
    df['SMA50_Slope'] = ((df['MA50'] - df['MA50'].shift(10)) / df['MA50'].shift(10)) * 100

    # ---- ATR (Wilder) ----
    prev_close = df['Close'].shift(1)
    tr = np.maximum(
        df['High'] - df['Low'],
        np.maximum((df['High'] - prev_close).abs(), (df['Low'] - prev_close).abs()),
    )
    df['TR'] = tr
    df['ATR'] = tr.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()

    df['Daily_Range'] = df['High'] - df['Low']
    df['ADR'] = df['Daily_Range'].rolling(window=14).mean()
    df['ADR_Pct'] = (df['ADR'] / df['Close']) * 100
    df['Vol_Avg_20'] = df['Volume'].rolling(window=20).mean()
    df['Vol_Avg_50'] = df['Volume'].rolling(window=50).mean()
    df['Vol_Expansion'] = df['Volume'] / df['Vol_Avg_50']

    # v6.5 (HK only): untraded and early-close sessions must not shape the indicators.
    # A suspension has no range and no volume, so including it shrinks ADR and fakes a dry-up.
    df['Tradable'] = True
    if PROFILE['name'] == 'HK':
        traded = ~hk_micro.untraded_bars(df['High'], df['Low'], df['Volume'])
        df['Tradable'] = np.asarray(traded, bool)

        rng = (df['High'] - df['Low']).where(traded)
        df['Daily_Range'] = rng
        df['ADR'] = rng.rolling(14, min_periods=8).mean()
        df['ADR_Pct'] = (df['ADR'] / df['Close']) * 100
        df['TR'] = tr.where(traded)
        df['ATR'] = df['TR'].ewm(alpha=1 / 14, min_periods=10, adjust=False).mean()
        df['Vol_Avg_20'] = df['Volume'].where(traded).rolling(20, min_periods=10).mean()
        df['Vol_Avg_50'] = df['Volume'].where(traded).rolling(50, min_periods=20).mean()
        df['Vol_Expansion'] = df['Volume'] / df['Vol_Avg_50']

    # ---- Relative strength vs SPY (shared cache) ----
    try:
        if spy_df is not None:
            spy = spy_df.copy()
            if len(spy) == 0:
                raise RuntimeError('共用 benchmark 已下載失敗')
        else:
            spy, _, _, spy_error = try_fetch_us_stock(
                PROFILE['bench'], start_date, expected_last_date,
                max_retries=MAX_DOWNLOAD_RETRIES, silent=silent,
            )
            if spy is None:
                raise RuntimeError(f"{PROFILE['bench']} benchmark 下載失敗：{spy_error}")

        if len(spy) > 0:
            spy = normalize_yf_columns(spy)
            spy = clean_price_rows(spy)
            if 'Close' not in spy.columns:
                raise RuntimeError('benchmark 缺少 Close')
            spy_ret = spy['Close'].squeeze().pct_change(63).reindex(df.index, method='ffill')
            stk_ret = df['Close'].squeeze().pct_change(63)
            df['RS_Score'] = (stk_ret - spy_ret) * 100
            spy_close = spy[['Close']].rename(columns={'Close': 'SPY_Close'})
            df = df.join(spy_close, how='left')
            df['SPY_Close'] = df['SPY_Close'].ffill()
            df['RS_1M'] = df['Close'].pct_change(20) * 100 - df['SPY_Close'].pct_change(20) * 100
            df['RS_3M'] = df['Close'].pct_change(60) * 100 - df['SPY_Close'].pct_change(60) * 100
            # ---- Haber-style RS line details (export/sort; tiny Priority quality only) ----
            df['RS_Line'] = df['Close'] / df['SPY_Close'].replace(0, np.nan)
            df['RS_Line_Slope'] = (df['RS_Line'] - df['RS_Line'].shift(20)) / 20.0
            # Meaningful "slope up": ≥1% RS_Line gain over 20 sessions (avoids float≈0 false positives)
            df['RS_Line_Chg_20'] = df['RS_Line'] / df['RS_Line'].shift(20) - 1.0
            df['RS_Line_Up'] = df['RS_Line_Chg_20'] >= 0.01
            rs_line_max_63 = df['RS_Line'].rolling(63, min_periods=20).max()
            close_max_63 = df['Close'].rolling(63, min_periods=20).max()
            df['RS_Line_NH'] = df['RS_Line'] >= (rs_line_max_63 - 1e-12)
            df['RSNHBP'] = df['RS_Line_NH'] & (df['Close'] < close_max_63)
            stk_d = df['Close'].pct_change()
            spy_d = df['SPY_Close'].pct_change()
            weak_pct = np.full(len(df), np.nan, dtype=float)
            beat_buf = []
            for i in range(len(df)):
                sd = spy_d.iloc[i]
                if pd.notna(sd) and sd < 0:
                    st = stk_d.iloc[i]
                    beat_buf.append(1.0 if (pd.notna(st) and st > sd) else 0.0)
                    if len(beat_buf) > 20:
                        beat_buf.pop(0)
                    if len(beat_buf) >= 20:
                        weak_pct[i] = 100.0 * (sum(beat_buf) / 20.0)
            # 1a: doc promises a forward-filled value (blank only before 20 down days)
            df['Weak_Day_RS_Pct'] = pd.Series(weak_pct, index=df.index).ffill()
            vol_max_252 = df['Volume'].rolling(252, min_periods=60).max()
            df['Highest_Vol_Edge'] = df['Volume'] >= (vol_max_252 * 0.95)
        else:
            df['RS_Score'] = df['RS_1M'] = df['RS_3M'] = np.nan
            df['RS_Line'] = df['RS_Line_Slope'] = df['RS_Line_Chg_20'] = df['Weak_Day_RS_Pct'] = np.nan
            df['RS_Line_NH'] = df['RSNHBP'] = df['Highest_Vol_Edge'] = df['RS_Line_Up'] = False
    except Exception as e:
        if not silent:
            print(f'⚠️ {ticker} 無法計算 SPY 相對強度：{type(e).__name__}: {e}')
        df['RS_Score'] = df['RS_1M'] = df['RS_3M'] = np.nan
        df['RS_Line'] = df['RS_Line_Slope'] = df['RS_Line_Chg_20'] = df['Weak_Day_RS_Pct'] = np.nan
        df['RS_Line_NH'] = df['RSNHBP'] = df['Highest_Vol_Edge'] = df['RS_Line_Up'] = False

    # 1a: RS_Status makes an unavailable RS explicit instead of a legal-looking 0
    df['RS_Status'] = np.where(df['RS_Score'].notna(), 'OK', 'UNKNOWN')

    # v6.6 guard: RS compares 63 stock bars against 63 benchmark bars. If the stock is missing
    # sessions, the two legs cover different windows and the difference is not like-for-like
    # (measured: 3 missing bars ~ +3.3 RS points, 5 ~ +7.7). Do not fix the number — refuse to
    # trust it: Leader_OK becomes UNKNOWN, which is neither a pass nor a fail.
    df['RS_Stale'] = False
    try:
        bench_idx = spy.index[-63:] if spy is not None and len(spy) >= 63 else None
        if bench_idx is not None and (len(bench_idx) - df['Close'].reindex(bench_idx).notna().sum()) >= 3:
            df['RS_Stale'] = True
            df['RS_Status'] = 'STALE'
    except Exception:
        pass

    # ---- Risk / resistance ----
    # (v5.2) the old Suggested_Stop / Risk_* / Reward_* / RR_Ratio family is gone;
    # risk is now the gate's Entry_Ref - Invalidate_Below, in ADR units.
    df['Resistance_20D'] = df['High'].rolling(20).max()
    df['Resistance_20D_Prior'] = df['High'].rolling(20).max().shift(1)

    df['Minervini_Trend_Basic'] = (
        (df['Close'] > df['MA50']) & (df['Close'] > df['MA150']) & (df['Close'] > df['MA200']) &
        (df['MA50'] > df['MA150']) & (df['MA150'] > df['MA200'])
    ).astype(int)
    df['Minervini_Stage2_Strict'] = (
        (df['Minervini_Trend_Basic'] == 1) & (df['Close'] > df['MA10']) &
        (df['MA10'] > df['MA20']) & (df['MA20'] > df['MA50']) & (df['SMA50_Slope'] > 0)
    ).astype(int)

    df['High_52W'] = df['High'].rolling(252).max()
    df['Dist_from_52W_High_Pct'] = ((df['Close'] - df['High_52W']) / df['High_52W']) * 100
    df['High_52W_Prior'] = df['High'].rolling(252).max().shift(1)

    # Vectorized day-over-day HL/HH counts over the prior 20 bars
    low_up = (df['Low'] > df['Low'].shift(1)).astype(float)
    high_up = (df['High'] > df['High'].shift(1)).astype(float)
    df['Higher_Lows_Count'] = low_up.rolling(19).sum().shift(1).fillna(0)
    df['Higher_Highs_Count'] = high_up.rolling(19).sum().shift(1).fillna(0)


    df['Dist_from_MA10_Pct'] = ((df['Close'] - df['MA10']) / df['MA10']) * 100
    df['Dist_from_MA50_Pct'] = ((df['Close'] - df['MA50']) / df['MA50']) * 100
    df['Extension_MA20_Pct'] = ((df['Close'] - df['MA20']) / df['MA20']) * 100
    df['Dist_from_MA200_Pct'] = ((df['Close'] - df['MA200']) / df['MA200']) * 100

    # Wilder RSI
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    df['RSI_14'] = 100 - (100 / (1 + rs))
    df.loc[(avg_loss == 0) & (avg_gain > 0), 'RSI_14'] = 100
    df['Price_Change_Pct'] = df['Close'].pct_change() * 100

    # ---- two base families, running in parallel, both exported ----
    df, base_episodes_strict = base_layer.detect_bases(df, base_layer.STRICT)
    df, base_episodes_wide = base_layer.detect_bases(df, base_layer.WIDE)
    base_snaps = [base_layer.snapshot(df, 'BaseS', cfg_width=base_layer.STRICT['width_atr_max']),
                  base_layer.snapshot(df, 'BaseW', cfg_width=base_layer.WIDE['width_atr_max'])]

    # 1e: every structural level is per-bar now (levels.py).
    df, level_parts = levels.compute(df)

    last_idx = df.index[-1]
    close_now = df.loc[last_idx, 'Close']

    # v5.3 F6: supply is measured from the ENTRY inside gates.find_supply()
    ma10 = df.loc[last_idx, 'MA10']
    ma20 = df.loc[last_idx, 'MA20']
    ma50 = df.loc[last_idx, 'MA50']
    if pd.notna(ma10) and pd.notna(ma20) and pd.notna(ma50) and ma20 and ma50:
        comp1 = abs(ma10 - ma20) / ma20 * 100 < 1.5
        comp2 = abs(ma20 - ma50) / ma50 * 100 < 3.0
        df.loc[last_idx, 'MA_Compression_Zone'] = bool(comp1 and comp2)
    else:
        df.loc[last_idx, 'MA_Compression_Zone'] = False

    # Earnings: failure => UNKNOWN (do not pretend CLEAR); a manual override is the last resort
    # The Date column starts as an all-NaN float; assigning a string to it raises TypeError.
    # (Latent bug found when a single-ticker run had no earnings date at all.)
    if 'Earnings_Date' not in df.columns:
        df['Earnings_Date'] = np.nan
    if df['Earnings_Date'].dtype != object:
        df['Earnings_Date'] = df['Earnings_Date'].astype(object)
    try:
        earnings_date = None
        earnings_src = 'yahoo'
        edf = yf.Ticker(actual_ticker).get_earnings_dates(limit=8)
        if edf is not None and len(edf) > 0:
            edf = edf.sort_index()
            today = expected_last_date   # v5.3 F11: as-of date, not the HK wall clock
            future_idx = [i for i in edf.index if pd.Timestamp(i).date() >= today]
            if future_idx:
                earnings_date = pd.Timestamp(min(future_idx)).date()

        if earnings_date is not None:
            days_to = _sessions_between(expected_last_date, earnings_date)   # v5.3 F11: sessions
            if days_to <= 7:
                flag = 'PASS'
            elif days_to <= 14:
                flag = 'CAUTION'
            else:
                flag = 'CLEAR'
            df.loc[last_idx, 'Earnings_Date'] = str(earnings_date)
            df.loc[last_idx, 'Days_To_Earnings'] = days_to
            df.loc[last_idx, 'Earnings_Proximity_Flag'] = flag
        else:
            df.loc[last_idx, 'Earnings_Date'] = np.nan
            df.loc[last_idx, 'Days_To_Earnings'] = np.nan
            df.loc[last_idx, 'Earnings_Proximity_Flag'] = 'UNKNOWN'
    except Exception:
        df.loc[last_idx, 'Earnings_Date'] = np.nan
        df.loc[last_idx, 'Days_To_Earnings'] = np.nan
        df.loc[last_idx, 'Earnings_Proximity_Flag'] = 'UNKNOWN'

    # Last resort: a manual date (e.g. read off TradingView). Covers BOTH failure paths above —
    # the API raising, and the API returning nothing — because HK names hit either one.
    ov = earnings_overrides.get(str(ticker).upper())
    if ov and ov[0] >= expected_last_date and str(ov[1]).lower() in ('tradingview', 'hkex', 'hkexnews', 'override'):
        # v6.4: an explicit source (TradingView / HKEXnews) outranks Yahoo's estimate,
        # not just fills a gap. Still guarded by "the date must not be in the past".
        yahoo_date = df.loc[last_idx, 'Earnings_Date']
        if (pd.notna(yahoo_date) and pd.Timestamp(ov[0]) > pd.Timestamp(yahoo_date)):
            pass          # v6.7: the override would push the date later (= safer); keep Yahoo
        elif str(yahoo_date) != str(ov[0]):
            earnings_date, earnings_src = ov
            days_to = _sessions_between(expected_last_date, earnings_date)
            df.loc[last_idx, 'Earnings_Date'] = str(earnings_date)
            df.loc[last_idx, 'Days_To_Earnings'] = days_to
            df.loc[last_idx, 'Earnings_Proximity_Flag'] = (
                'PASS' if days_to <= 7 else ('CAUTION' if days_to <= 14 else 'CLEAR'))
            if not silent:
                print(f"  📅 {ticker} 財報日採用 override：{earnings_date}（{earnings_src}）")

    if str(df.loc[last_idx, 'Earnings_Proximity_Flag']) == 'UNKNOWN':
        ov = earnings_overrides.get(str(ticker).upper())
        if ov and ov[0] >= expected_last_date:
            earnings_date, earnings_src = ov
            days_to = _sessions_between(expected_last_date, earnings_date)
            flag = 'PASS' if days_to <= 7 else ('CAUTION' if days_to <= 14 else 'CLEAR')
            df.loc[last_idx, 'Earnings_Date'] = str(earnings_date)
            df.loc[last_idx, 'Days_To_Earnings'] = days_to
            df.loc[last_idx, 'Earnings_Proximity_Flag'] = flag
            if not silent:
                print(f"  📅 {ticker} 財報日由 override 提供：{earnings_date}（{earnings_src}）")

    # ---- 1c: three gates over both base families + the pullback family ----
    pb_out = pullback.evaluate(df.loc[last_idx], df)
    gate_out = gates.evaluate(df.loc[last_idx], base_snaps, pb_out, df=df)   # v5.3
    for k, v in gate_out.items():
        if k == 'Evidence':
            df.loc[last_idx, 'Evidence_JSON'] = json.dumps(v, ensure_ascii=False)
        else:
            df.loc[last_idx, k] = v

    # v6.4 (#1): a bar rebuilt from 60m data has no official close and no auction volume, so it
    # must never produce an actionable trigger. Downgrade the class and say why.
    hk_extra = {}
    if PROFILE['name'] == 'HK':
        # v6.7: the ticket is already tick-aligned inside gates; here we only report the tick
        # and count untraded bars INSIDE the base the engine actually selected (not the last N bars).
        px = df.loc[last_idx, 'Close']
        hk_extra['Tick_Size'] = hk_micro.tick_size(px)
        hk_extra['Tick_Pct'] = hk_micro.tick_pct(px)
        untr = hk_micro.untraded_bars(df['High'], df['Low'], df['Volume'])
        fam = str(df.loc[last_idx, 'Base_Family'] or '')
        prefix = {'STRICT': 'BaseS', 'WIDE': 'BaseW'}.get(fam, fam)   # family name -> column prefix
        sc, ec = f'{prefix}_Start', f'{prefix}_End'
        if fam and sc in df.columns and ec in df.columns:
            # match by calendar date: the index may be tz-aware while the column is a plain date
            dates = np.array([pd.Timestamp(x).date() for x in df.index])
            s_d = pd.Timestamp(df.loc[last_idx, sc]).date()
            e_d = pd.Timestamp(df.loc[last_idx, ec]).date()
            si = int(np.where(dates == s_d)[0][0]) if (dates == s_d).any() else -1
            ei = int(np.where(dates == e_d)[0][0]) if (dates == e_d).any() else -1
            hk_extra['Base_Untraded_Bars'] = (hk_micro.count_untraded_in(untr, si, ei)
                                              if si >= 0 and ei >= si else np.nan)
        else:
            hk_extra['Base_Untraded_Bars'] = np.nan     # no base selected -> not applicable
        for k, v in hk_extra.items():
            df.loc[last_idx, k] = v

    bar_source = str(df.loc[last_idx, 'Bar_Source']) if 'Bar_Source' in df.columns else 'DAILY'
    if bar_source == 'SYNTH_60M':
        if (df.loc[last_idx, 'Candidate_Class'] == 'A_SETUP'
                and df.loc[last_idx, 'Entry_Feasible'] in ('AT_TRIGGER', 'NEXT_DAY')):
            df.loc[last_idx, 'Candidate_Class'] = 'C_WATCH'
            df.loc[last_idx, 'Screen_Flag'] = 'WATCH'          # keep flag and class in step
            df.loc[last_idx, 'Entry_Feasible'] = 'NOT_YET'     # no ticket until a real bar exists
            df.loc[last_idx, 'Volume_Confirm'] = 'UNKNOWN'
            note = str(df.loc[last_idx, 'Class_Note'] or '')
            df.loc[last_idx, 'Class_Note'] = (note + '; SYNTH_60M bar — trigger needs manual confirm').strip('; ')
    else:
        df.loc[last_idx, 'Bar_Source'] = 'DAILY'

    score_val, score_breakdown, score_note = calculate_priority_score(df.loc[last_idx])
    df.loc[last_idx, 'Priority_Score'] = score_val
    df.loc[last_idx, 'Score_Breakdown'] = score_breakdown
    df.loc[last_idx, 'Score_Note'] = score_note
    df.loc[last_idx, 'RS_Role'] = classify_rs_role(df.loc[last_idx])
    # v6.8: read the class AFTER the SYNTH downgrade, not the gate's original value
    screen_flag = CLASS_TO_FLAG.get(df.loc[last_idx, 'Candidate_Class'], 'NONE')
    df.loc[last_idx, 'Screen_Flag'] = screen_flag
    # DEPRECATED alias (one release): slim / sector_wind / Rule 14 / bots still read this
    df.loc[last_idx, 'Action_Refined'] = screen_flag

    return df


# =====================================================================
# Export / summary
# =====================================================================
def write_ticker_csv(df, ticker):
    output_file = os.path.join(OUTPUT_FOLDER, f"{sanitize_ticker(ticker)}_SwingAnalysis.csv")
    df_export = strip_tz_for_export(df)
    df_export.index.name = 'Date'
    df_export.to_csv(output_file)
    print(f'📊 CSV 已輸出：{output_file}')
    return output_file


def export_single_ticker_to_csv(ticker, months=MONTHS):
    expected_last_date = get_latest_completed_us_session()
    data_quality_records = []
    spy_df = fetch_shared_spy(expected_last_date=expected_last_date, months=months, silent=False)
    df = fetch_swing_data_us(
        ticker, months=months, silent=False,
        expected_last_date=expected_last_date, spy_df=spy_df,
        data_quality_records=data_quality_records,
    )
    if df is None or len(df) == 0:
        print(f'❌ {ticker} 無可輸出資料')
        save_data_quality_report(data_quality_records)
        return None
    output_file = write_ticker_csv(df, ticker)
    print(f"✅ 最後一行日期：{strip_tz_for_export(df).index[-1]}")
    print(f"✅ 最後一行 Close：{df['Close'].iloc[-1]}")
    save_data_quality_report(data_quality_records)
    return output_file


def export_multi_tickers_to_csv(tickers, months=MONTHS):
    results = []
    data_quality_records = []
    expected_last_date = get_latest_completed_us_session()
    print(f'\n🎯 本次整批分析預期最新完整交易日：{expected_last_date}')
    spy_df = fetch_shared_spy(expected_last_date=expected_last_date, months=months, silent=False)

    for i, ticker in enumerate(tickers):
        try:
            df = fetch_swing_data_us(
                ticker, months=months, silent=False,
                expected_last_date=expected_last_date, spy_df=spy_df,
                data_quality_records=data_quality_records,
            )
            if df is None or len(df) == 0:
                continue
            write_ticker_csv(df, ticker)
            last_row = strip_tz_for_export(df).iloc[-1]
            results.append({
                'Ticker': sanitize_ticker(ticker),
                'Rows': len(df),
                'Last_Date': str(last_row.name),
                'Close': last_row.get('Close', np.nan),
                'Priority_Score': last_row.get('Priority_Score', np.nan),
                'Action_Refined': last_row.get('Action_Refined', ''),
            })
        except Exception as e:
            print(f'❌ {ticker} 失敗：{e}')
            append_data_quality_record(
                data_quality_records, ticker=ticker, status='PROCESSING_ERROR',
                expected_date=expected_last_date, attempts=0, rows=0,
                error=f'{type(e).__name__}: {e}',
            )
        if i < len(tickers) - 1:
            time.sleep(INTER_TICKER_SLEEP_SEC)

    if results:
        summary_df = pd.DataFrame(results)
        summary_file = os.path.join(OUTPUT_FOLDER, 'SwingAnalysis_Summary.csv')
        summary_df.to_csv(summary_file, index=False)
        print(f'\n📁 Summary 已輸出：{summary_file}')
    save_data_quality_report(data_quality_records)
    return results


def generate_summary(results, output_folder=OUTPUT_FOLDER):
    rows = []
    for ticker, df in results.items():
        if df is None or len(df) == 0:
            continue
        r = df.iloc[-1]

        def g(k, default=np.nan):
            return r[k] if k in r.index and pd.notna(r[k]) else default

        def rnd(v, nd=2):
            return round(float(v), nd) if pd.notna(v) else np.nan

        rows.append({
            'Ticker': ticker,
            'Priority_Score': rnd(g('Priority_Score', 0), 1),
            'Action_Refined': g('Action_Refined', 'PASS'),
            'Screen_Flag': g('Screen_Flag', 'NONE'),
            'Candidate_Class': g('Candidate_Class', 'X_NONE'),
            'Leader_OK': g('Leader_OK', 'UNKNOWN'),
            'Setup_OK': g('Setup_OK', 'UNKNOWN'),
            'Risk_OK': g('Risk_OK', 'UNKNOWN'),
            'Leader_Why': g('Leader_Why', ''),
            'Setup_Why': g('Setup_Why', ''),
            'Risk_Why': g('Risk_Why', ''),
            'Setup_Family': g('Setup_Family', 'NONE'),
            'Setup_Code': g('Setup_Code', 'NONE'),
            'Pullback_Code': g('Pullback_Code', 'NONE'),
            'Stop_Type_Plan': g('Stop_Type_Plan', 'NONE'),
            'Regime_State': g('Regime_State', 'UNKNOWN'),
            'Regime_Label': g('Regime_Label', ''),
            'Regime_Source': g('Regime_Source', ''),
            'Index_Regime_State': g('Index_Regime_State', 'UNKNOWN'),
            'Breadth_50D': rnd(g('Breadth_50D')),
            'Ratio_10D': rnd(g('Ratio_10D')),
            'Momentum_Share': rnd(g('Momentum_Share')),
            'BaseS_State': g('BaseS_State', 'NONE'),
            'BaseW_State': g('BaseW_State', 'NONE'),
            'Entry_Feasible': g('Entry_Feasible', 'NO_SETUP'),
            'Volume_Confirm': g('Volume_Confirm', 'NOT_APPL'),
            'Class_Note': g('Class_Note', ''),
            'Base_Family': g('Base_Family', ''),
            'BuyStop_Max_Stop': rnd(g('BuyStop_Max_Stop')),
            'Entry_Ref': rnd(g('Entry_Ref')),
            'Base_State': g('Base_State', 'NONE'),
            **({k: rnd(g(k)) for k in HK_EXTRA_COLUMNS} if PROFILE['name'] == 'HK' else {}),
            'Setup_Len_Days': rnd(g('Setup_Len_Days'), 0),
            'Base_Width_ATR': rnd(g('Base_Width_ATR')),
            'Risk_ADR_Plan': rnd(g('Risk_ADR_Plan')),
            'Risk_Pct_Plan': rnd(g('Risk_Pct_Plan')),
            'Invalidate_Below': rnd(g('Invalidate_Below')),
            'Trigger_Price': rnd(g('Trigger_Price')),
            'Score_Breakdown': g('Score_Breakdown', ''),
            'Score_Note': g('Score_Note', ''),
            'RS_Status': g('RS_Status', 'UNKNOWN'),
            'Room_To_Supply_R': rnd(g('Room_To_Supply_R')),
            'Tradeable': g('Tradeable', 'PASS'),
            'Tradeable_Why': g('Tradeable_Why', ''),
            'Room_At_Plan_Stop_R': rnd(g('Room_At_Plan_Stop_R')),
            'Room_At_1_2ADR_R': rnd(g('Room_At_1_2ADR_R')),
            'Supply_Source': g('Supply_Source', 'NONE_ABOVE'),
            'Supply_Level': rnd(g('Supply_Level')),
            'Close': rnd(g('Close')),
            'RS_Score': rnd(g('RS_Score'), 1),
            'RS_1M': rnd(g('RS_1M'), 1),
            'RS_3M': rnd(g('RS_3M'), 1),
            'RS_Line': rnd(g('RS_Line'), 6),
            'RS_Line_Slope': rnd(g('RS_Line_Slope'), 8),
            'RS_Line_Chg_20': rnd(g('RS_Line_Chg_20'), 4),
            'RS_Line_Up': bool(g('RS_Line_Up', False)),
            'RS_Line_NH': bool(g('RS_Line_NH', False)),
            'RSNHBP': bool(g('RSNHBP', False)),
            'Weak_Day_RS_Pct': rnd(g('Weak_Day_RS_Pct'), 1),
            'Highest_Vol_Edge': bool(g('Highest_Vol_Edge', False)),
            'RS_Role': g('RS_Role', '') or '',
            'Vol_Expansion': rnd(g('Vol_Expansion')),
            'Minervini_Trend': bool(g('Minervini_Trend_Basic', 0)),
            'SR_Flip_Active': bool(g('SR_Flip_Active', False)),
            'MA_Compression_Zone': bool(g('MA_Compression_Zone', False)),
            'Earnings_Proximity_Flag': g('Earnings_Proximity_Flag', 'UNKNOWN'),
            'Earnings_Date': g('Earnings_Date', 'N/A'),
            'POC_Level': g('POC_60D'),
            'AVWAP_HVD': rnd(g('AVWAP_HVD')),
        })
    summary_df = pd.DataFrame(rows)
    if summary_df.empty:
        # A run where every ticker failed is an error, not an empty result: without this the
        # daily script would exit 0 and the bot would send "no setups" for a broken download.
        print(f'❌ {len(results) if "results" in dir() else 0} 個 ticker 全部失敗 — 沒有任何列可輸出')
        raise SystemExit(1)
    # Tie-break (A): Priority → RSNHBP → Slope → Weak_Day_RS_Pct → Highest_Vol_Edge
    if 'Candidate_Class' in summary_df.columns:
        _order = {'A_SETUP': 0, 'C_WATCH': 1, 'B_LEADER_WAIT': 2, 'X_NONE': 3}
        summary_df = summary_df.assign(_cls=summary_df['Candidate_Class'].map(_order).fillna(4))
    else:
        summary_df = summary_df.assign(_cls=0)
    summary_df = summary_df.assign(
        _rsnhbp=summary_df['RSNHBP'].astype(int),
        _slope=pd.to_numeric(summary_df.get('RS_Line_Chg_20', summary_df['RS_Line_Slope']), errors='coerce').fillna(-999.0),
        _wdrs=pd.to_numeric(summary_df['Weak_Day_RS_Pct'], errors='coerce').fillna(-999.0),
        _hve=summary_df['Highest_Vol_Edge'].astype(int),
    ).sort_values(
        ['_cls', 'Priority_Score', '_rsnhbp', '_slope', '_wdrs', '_hve'],
        ascending=[True, False, False, False, False, False],
    ).drop(columns=['_rsnhbp', '_slope', '_wdrs', '_hve', '_cls'])
    summary_df.to_csv(os.path.join(output_folder, 'Summary_US.csv'), index=False)
    print(f'\n✅ 摘要表：{output_folder}/Summary_US.csv')
    show = [c for c in ['Ticker', 'Candidate_Class', 'Priority_Score', 'Leader_OK', 'Setup_OK',
                        'Risk_OK', 'Entry_Feasible', 'Base_State', 'Close'] if c in summary_df.columns]
    print(summary_df[show].to_string(index=False))
    return summary_df


SLIM_COLS = [
    'Ticker', 'Close', 'Priority_Score', 'Action_Refined',
    'Earnings_Proximity_Flag', 'Earnings_Date',
    'SR_Flip_Active', 'MA_Compression_Zone',
    'Candidate_Class', 'Leader_OK', 'Setup_OK', 'Risk_OK',
    'Setup_Why', 'Risk_Why', 'Entry_Feasible',
    'Risk_ADR_Plan', 'Risk_Pct_Plan', 'Invalidate_Below', 'Trigger_Price',
    'Base_State', 'Setup_Len_Days',
    # Haber-style RS bypass (overlay still appends sector_wind cols after these)
    'RS_Score', 'RS_1M', 'RS_3M',
    'RS_Line', 'RS_Line_Slope', 'RS_Line_Chg_20', 'RS_Line_Up', 'RS_Line_NH', 'RSNHBP',
    'Weak_Day_RS_Pct', 'Highest_Vol_Edge', 'RS_Role',
]


def generate_claude_slim(summary_df, results, output_folder=OUTPUT_FOLDER):
    if summary_df is None or summary_df.empty:
        print('ℹ️ 摘要為空，跳過 Claude_Input_Slim.csv')
        return None
    keep = summary_df['Candidate_Class'].isin(['A_SETUP', 'C_WATCH', 'B_LEADER_WAIT']) \
        if 'Candidate_Class' in summary_df.columns else pd.Series(True, index=summary_df.index)
    buy_stalk = summary_df[keep]['Ticker'].tolist()
    if not buy_stalk:
        print('ℹ️ 沒有可交付的候選，跳過 Claude_Input_Slim.csv 輸出')
        return None
    slim_rows = []
    for ticker in buy_stalk:
        if ticker not in results or results[ticker] is None:
            continue
        r = results[ticker].iloc[-1]
        row_dict = {'Ticker': ticker}
        for col in SLIM_COLS[1:]:
            row_dict[col] = r[col] if col in r.index else np.nan
        slim_rows.append(row_dict)
    slim_df = pd.DataFrame(slim_rows)
    slim_path = os.path.join(output_folder, 'Claude_Input_Slim.csv')
    slim_df.to_csv(slim_path, index=False)
    print(f'\n✅ Claude Slim CSV：{slim_path}（{len(slim_df)} 隻 A_SETUP/C_WATCH/B_LEADER_WAIT）')
    show = [c for c in ['Ticker', 'Candidate_Class', 'Entry_Feasible', 'Setup_Why', 'Risk_Why'] if c in slim_df.columns]
    print(slim_df[show].to_string(index=False))
    return slim_df


def build_rulebook_rows():
    """v6.7: read the live config, so the HK book cannot print US thresholds."""
    return [
        # (name, value, meaning, provenance, status)
        ('Priority_Score', '0-65', 'leader quality only: MN + MA + RS + Q - EXT', 'PICK', 'ENFORCED'),
        ('Leader_OK', f'trend & RS>={gates.CFG["leader"]["rs_min"]:.0f} & '
                      f'{gates.PROFILE_CUR}{gates.CFG["leader"]["price_min"]:.0f}/'
                      f'{gates.PROFILE_CUR}{gates.CFG["leader"]["dollar_vol_min"]/1e6:.0f}M',
         'leadership gate (from the market profile)', 'PICK', 'ENFORCED'),
        ('BASE_STRICT', '5-30d, no gaps', 'maximal run of compressed bars', 'SRC', 'ENFORCED'),
        ('BASE_WIDE', '10-40d, <=2 gaps, >=60% compressed', 'longer bases; geometry drops bars >1.5xADR', 'SRC', 'ENFORCED'),
        ('Base width cap', '3.0xATR strict / 4.0xATR wide', 'a base too wide is not a base', 'PICK', 'ENFORCED'),
        ('Base live window', '30 bars strict / 40 wide', 'stays live while price is inside it', 'PICK', 'ENFORCED'),
        ('Pullback depth', '>=0.5 ATR off the 8-bar high', 'must actually pull back', 'PICK', 'ENFORCED'),
        ('Pullback decline', '<=1.5xADR range, <=1.3x volume', 'reject clearly high-momentum declines', 'SRC', 'ENFORCED'),
        ('PB_STRUCT', 'min(anchor-0.5ATR, 3-bar low)', 'setup B stop', 'DOC', 'ENFORCED'),
        ('MA_STRUCT', 'min(MA20-0.5ATR, 3-bar low)', 'setup D stop', 'DOC', 'ENFORCED'),
        ('VP_STRUCT', 'min(POC-0.5ATR, 3-bar low)', 'setup E (bottom reversal) stop', 'DOC', 'ENFORCED'),
        ('SR_STRUCT', 'min(SR_Flip_Level-0.5ATR, 3-bar low)', 'setup H stop', 'DOC', 'ENFORCED'),
        ('Risk band (BREAKOUT)', '0.3-1.2 x ADR', 'per-family band', 'SRC', 'ENFORCED'),
        ('Risk band (PULLBACK)', '0.8-2.5 x ADR', 'per-family band', 'SRC', 'ENFORCED'),
        ('Room floor', '1.5R breakout & reversal / 1.0R pullback', 'hard supply above the ENTRY: prior 20D high, 52W high, bearish FVG (soft levels = remark)', 'PICK', 'ENFORCED'),
        ('Extended', 'Ext>15% or RSI>75 or >25% over MA50', 'red flag #1', 'DOC', 'ENFORCED'),
        ('Earnings', 'sessions from as-of; PASS<=7 => FAIL; UNKNOWN => UNKNOWN', 'never a silent pass', 'DOC', 'ENFORCED'),
        ('Regime source', 'user dashboard sheet', '市況 label + % >50D + 10日比率', 'SRC', 'ENFORCED'),
        ('Regime mapping', '強->MOMENTUM, 弱->RISK_OFF, 中性->NEUTRAL', 'label first, numbers are evidence', 'PICK', 'ENFORCED'),
        ('Pool breadth', '% of scanned names above MA50', 'hand-picked pool; biased, not market breadth', 'MEA', 'ENFORCED'),
        ('Per-bar levels', 'AVWAP / POC / VAH / VAL / SR flip / FVG', 'levels.py, every bar', 'DOC', 'ENFORCED'),
        ('Breakout volume', '>=1.5x 20d avg on the trigger bar', 'LOW => A_SETUP downgraded to C_WATCH (SWING_VOL_MODE=REMARK keeps it with a note)', 'SRC', 'ENFORCED'),
        ('Breakout failure', 'close < breakout-bar low', 'state BO_FAILED, ticket INVALIDATED', 'SRC', 'ENFORCED'),
        ('Risk after trigger', 'current close -> breakout-bar low', 'next-open proxy for NEXT_DAY / LATE', 'PICK', 'ENFORCED'),
        ('BuyStop_Max_Stop', 'trigger - 1.2xADR', 'lowest acceptable day-low at a buy-stop fill', 'SRC', 'ENFORCED'),
        ('Setup E (reversal)', 'not Minervini; drawdown>=25%; low 5-40 bars old; higher low; close>POC & MA20 rising; up/down vol>=1.2', 'true bottom reversal, family REVERSAL', 'PICK', 'ENFORCED'),
        ('S/R flip', 'old high (bars i-40..i-10) broken, retested within 15 bars, close holds', 'setup H trigger', 'PICK', 'ENFORCED'),
        ('Regime', 'header only', 'never changes a gate or class (user decision 2026-11-05)', 'DOC', 'ENFORCED'),
        ('Entry_Feasible', 'NOT_YET / AT_TRIGGER / NEXT_DAY / LATE / AT_MARKET / MISSED / INVALIDATED', 'ticket state', 'DOC', 'ENFORCED'),
]

RULEBOOK_NOTES = """## How to read the numbers

* `Room_To_Supply_R` — distance to the nearest real supply, in units of the planned risk.
  This is the only "reward" number in the file. There is no RR column any more: the old one
  measured 1/risk, not reward/risk.
* `Priority_Score` (0-65) — leadership only. It is a **sort key**, not a threshold and not a
  quality judgement about the setup.
* `Score_Breakdown` — the exact terms that produced the score; they always sum to it.
* `Risk_ADR_Plan` — planned risk in ADR units. `PENDING` means the stop is the breakout bar's
  low, which does not exist yet.
* `Base_*` — geometry of the episode that Setup_OK is judged on.

## 1a change log (v4.7)

1. RR removed from `Priority_Score` (was up to +20 via `max(T1,T2,T3)`).
2. `Score_Breakdown` / `Score_Note` added; invariant: terms sum to the score.
3. `Room_To_Supply_R` / `Supply_Level` / `Supply_Source` added (prior-anchored).
4. `Weak_Day_RS_Pct` forward-filled (the doc always promised this).
5. RS fetch failure -> NaN + `RS_Status=UNKNOWN` (was a silent, legal-looking 0).
6. `Screen_Flag` is the name to read; `Action_Refined` kept one release as a deprecated alias.
7. BUY needs score>=70 AND `Room_To_Supply_R >= 1R` (NONE_ABOVE passes). The room floor was
   added during 1a because removing the RR gate alone *upgraded* TMO to BUY at 0.29R of room.
   1.0R is definitional (reward >= risk), not a tuned number.

## 1b change log (v4.8)

1. **Base episode layer** replaces the zone machine as the source of `Setup_OK`: a base is a
   maximal run of strictly compressed bars (no exception bars inside), 5-30 sessions, with
   geometry frozen at its last bar and a trigger that is a *later* bar closing above that high.
2. **Three gates** (`Leader_OK` / `Setup_OK` / `Risk_OK`) + `Candidate_Class`
   (`A_SETUP` / `B_LEADER_WAIT` / `C_WATCH` / `X_NONE`), each with a reason string.
3. **`Priority_Score` is now leader-quality only (0-65)**. Zone points, slap-back, setup tags,
   volume and earnings were removed from the score: they are either broken or belong to a gate.
4. `Screen_Flag` is a class label. `BUY` / `STALK` / `AVOID` are no longer emitted by layer 1.
5. New artefacts: `Contract_US.csv` (all fields, all names), `Trigger_US.csv` (tomorrow's
   tickets), `Evidence_US.csv` (one row per check).

## Removed in v5.2 — the whole old machinery is gone

`Tight_Zone_*`, `Playbook_Flag`, `Setup_Type`, `Stop_Type`, `Adjusted_Stop`, `Adj_Risk_*`,
`Adj_RR_Ratio`, `RR_Zone_*`, `RR_Ratio_*`, `Suggested_Stop`, `Risk_*`, `Reward_*`,
`RR_Ratio`, `Target_*`, `Swing_Low_*`, `Mini_Breakout_*`, `Breakdown_*`, `Slap_Back_*`.

Why: none of it fed a gate or the score any more, and every one of them was proved either
inert (freshness could not fail, mini-breakout and breakdown never fired while the zone was
alive) or self-serving (RR measured 1/risk, not reward/risk). Keeping them computed invited
someone to read them again. The base layer, the gates and the tickets replace all of it.

## 1c change log (v4.9)

1. **Two base families** run in parallel: `BaseS_*` (5-30d, no gaps) and `BaseW_*` (10-40d,
   <=2 consecutive gaps, >=60% compressed, geometry excludes bars wider than 1.5xADR).
   The gates use `TRIGGERED` first, then a pullback, then a waiting base.
2. **Pullback family B/D/E/H** with the three previously undefined stop biases
   (`PB_STRUCT`, `MA_STRUCT`, `VP_STRUCT`) plus `SR_STRUCT`. Stops are
   `min(level - 0.5*ATR, 3-bar low)` where a swing low exists.
3. **Market regime** header: NASDAQ 10EMA vs 20EMA. Reported per run, never scored.
4. A `SPENT` base no longer masks a live pullback (it did in the first cut).

## 1f change log (v5.3)
See CHANGELOG_v53.md for the full list with reasons. In short: BO_FAILED state, WIDE swallow
fix, max_len enforced, supply measured from the entry (hard: prior 20D high / 52W high /
bearish FVG; soft levels are remarks), breakout volume confirmation, risk re-measured after the
trigger, BuyStop_Max_Stop for buy-stop entries, setup E rebuilt as a true bottom reversal
(family REVERSAL), S/R flip = real retest, earnings counted in sessions from the as-of date,
per-family invariants and an evidence/contract reconciliation check. Regime stays a header.
"""


def write_rulebook(output_folder=OUTPUT_FOLDER):
    """Emit the threshold table with provenance so every number can be challenged."""
    lines = [f"# RULEBOOK — {PROFILE['name']} swing scanner v6.7", '',
             'Generated by the run itself. `SRC` = from Qullamaggi / CUP / Bonde notes, '
             '`DOC` = playbook, `PICK` = arbitrary, `MEA` = measured.', '',
             '| Rule | Value | Meaning | Source | Status |', '|---|---|---|---|---|']
    for name, val, meaning, prov, status in build_rulebook_rows():
        lines.append(f'| `{name}` | {val} | {meaning} | {prov} | **{status}** |')
    lines += ['', RULEBOOK_NOTES]
    path = os.path.join(output_folder, 'RULEBOOK_US.md')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    print(f'\n📘 RULEBOOK：{path}')
    return path



PROFILE = markets.load()          # SWING_MARKET=us|hk; see markets.py
CONTRACT_VERSION = ('us-contract-1f.5' if PROFILE['name'] != 'HK'
                    else 'hk-contract-1f.5')      # v6.7: HK has 3 extra columns

CONTRACT_FIELDS = [
    'Ticker', 'Date', 'Close', 'Market', 'Benchmark',
    'Candidate_Class', 'Screen_Flag', 'Entry_Feasible',
    'Leader_OK', 'Leader_Why', 'Setup_OK', 'Setup_Why', 'Risk_OK', 'Risk_Why',
    'Priority_Score', 'Score_Breakdown',
    'RS_Score', 'RS_Status', 'RS_1M', 'RS_3M', 'RS_Line_Up', 'RS_Line_NH', 'RSNHBP',
    'Weak_Day_RS_Pct', 'RS_Role', 'Minervini_Trend', 'Minervini_Stage2',
    'Extension_MA20_Pct', 'RSI_14', 'Vol_Expansion', 'Vol_Avg_20', 'ADR_Pct',
    'Setup_Family', 'Setup_Code', 'Pullback_Code', 'Base_State',
    'BaseS_State', 'BaseW_State',
    'Setup_Len_Days', 'Base_Width_ATR', 'Base_Width_Pct', 'Base_Compressed_Pct',
    'Depth_ATR', 'Vol_Ratio_Pullback', 'Confluence_Count',
    'Drawdown_Pct', 'UpDown_Vol', 'HigherLow_Pct',
    'Base_Cleanliness', 'Base_Vol_Decay', 'Base_HigherLows_Pct',
    'Base_Prior_Advance_Pct', 'Base_Count_126',
    'Stop_Type_Plan',
    'Regime_State', 'Regime_Label', 'Regime_Source', 'Regime_Date', 'Index_Regime_State',
    'Breadth_50D', 'Ratio_10D', 'Momentum_Share',
    'Trigger_Date', 'Days_Since_Trigger', 'Trigger_Price', 'Trigger_Min_Vol', 'Trigger_Vol_Ratio',
    'Invalidate_Below', 'Entry_Ref', 'Entry_Src', 'Risk_Pct_Plan', 'Risk_ADR_Plan',
    'Room_To_Supply_R', 'Room_Basis', 'Supply_Level', 'Supply_Source', 'Shares_per_1000_Risk',
    'Tradeable', 'Tradeable_Why', 'Room_At_Plan_Stop_R', 'Room_At_1_2ADR_R',
    'Resistance_20D_Prior', 'High_52W', 'Dist_from_52W_High_Pct',
    'POC_60D', 'Dist_to_POC_Pct', 'AVWAP_20D_Low', 'Dist_to_AVWAP_Low_Pct',
    'MA10', 'MA20', 'MA50', 'SMA50_Slope', 'VAL_60D',
    'AVWAP_HVD', 'VAH_60D', 'SR_Flip_Level',
    'SR_Flip_Live', 'SR_Flip_Age', 'Bullish_FVG1_Upper', 'Bullish_FVG1_Lower',
    'Earnings_Proximity_Flag', 'Earnings_Date', 'Days_To_Earnings',
    'Base_Family', 'Volume_Confirm', 'Bar_Source', 'Class_Note', 'BuyStop_Max_Stop', 'Pullback_Candidates',
    'Supply_Soft_Level', 'Supply_Soft_Source', 'Room_To_Soft_R',
    'contract_version',
]


HK_EXTRA_COLUMNS = ['Tick_Size', 'Tick_Pct', 'Base_Untraded_Bars']


def _row_value(r, key):
    if key == 'contract_version':
        return CONTRACT_VERSION
    if key == 'Market':
        return PROFILE['name']
    if key == 'Benchmark':
        return PROFILE['bench']
    if key == 'Shares_per_1000_Risk':
        if 'Shares_per_1000_Risk' in r.index:   # v5.3: gates owns it (NaN while PENDING)
            v = r['Shares_per_1000_Risk']
            return round(float(v), 0) if pd.notna(v) else np.nan
        try:
            e, v = float(r.get('Entry_Ref')), float(r.get('Invalidate_Below'))
            return round(1000.0 / (e - v), 0) if e > v else np.nan
        except Exception:
            return np.nan
    if key == 'Date':
        return _date_str(r)   # v5.3 F12
    if key not in r.index:
        return np.nan
    v = r[key]
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating, float)):
        return round(float(v), 4) if pd.notna(v) else np.nan
    if isinstance(v, (np.bool_, bool)):
        return bool(v)
    return v


def generate_contract(results, output_folder=OUTPUT_FOLDER):
    rows = []
    for ticker, df in results.items():
        if df is None or len(df) == 0:
            continue
        r = df.iloc[-1]
        fields = CONTRACT_FIELDS + (HK_EXTRA_COLUMNS if PROFILE['name'] == 'HK' else [])
        row = {k: _row_value(r, k) for k in fields}
        row['Ticker'] = ticker
        rows.append(row)
    if not rows:
        return None
    path = os.path.join(output_folder, 'Contract_US.csv')
    fields = CONTRACT_FIELDS + (HK_EXTRA_COLUMNS if PROFILE['name'] == 'HK' else [])
    pd.DataFrame(rows, columns=fields).to_csv(path, index=False)
    print(f'\n📑 Contract：{path}（{len(rows)} 隻 × {len(fields)} 欄）')
    return path


def generate_trigger(results, output_folder=OUTPUT_FOLDER):
    cols = ['Ticker', 'Candidate_Class', 'Setup_OK', 'Risk_OK', 'Tradeable', 'Tradeable_Why',
            'Room_At_Plan_Stop_R', 'Setup_Family', 'Setup_Code',
            'Entry_Feasible', 'Base_State', 'Stop_Type_Plan', 'Trigger_Price', 'Trigger_Min_Vol',
            'Invalidate_Below', 'Entry_Ref', 'Risk_Pct_Plan', 'Risk_ADR_Plan',
            'Room_To_Supply_R', 'Shares_per_1000_Risk', 'Base_Family', 'Volume_Confirm',
            'BuyStop_Max_Stop', 'Supply_Source', 'Class_Note', 'Setup_Why', 'Risk_Why']
    rows = []
    try:
        import json as _json
        for ticker, df in results.items():
            if df is None or len(df) == 0:
                continue
            r = df.iloc[-1]
            if str(r.get('Entry_Feasible', 'NO_SETUP')) not in ('NOT_YET', 'AT_TRIGGER', 'NEXT_DAY', 'LATE', 'AT_MARKET'):
                continue
            if str(r.get('Bar_Source', 'DAILY')) == 'SYNTH_60M':
                continue          # v6.8: a bar rebuilt from 60m data must not become a ticket
            # v6.10 (ported from US v5.5.4): only a risk-sane plan may become a ticket. This was
            # the hole that let 2269.HK sit in the file at 2.72xADR.
            if str(r.get('Tradeable', 'PASS')).upper() != 'PASS':
                continue
            row = {k: _row_value(r, k) for k in cols if k != 'Ticker'}
            row['Ticker'] = ticker
            rows.append(row)
    except Exception as e:
        print(f'⚠️ trigger 表失敗：{e}')
        return None
    if not rows:
        print('\n🎫 Trigger：今日沒有可掛單的標的（無 live base）')
        return None
    df_t = pd.DataFrame(rows, columns=cols)
    order = {'A_SETUP': 0, 'C_WATCH': 1, 'B_LEADER_WAIT': 2, 'X_NONE': 3}
    risk_order = {'PASS': 0, 'PENDING': 1, 'UNKNOWN': 2, 'FAIL': 3}
    df_t = df_t.assign(_c=df_t['Candidate_Class'].map(order).fillna(4),
                       _r=df_t['Risk_OK'].map(risk_order).fillna(4)
                       ).sort_values(['_c', '_r', 'Risk_ADR_Plan']).drop(columns=['_c', '_r'])
    path = os.path.join(output_folder, 'Trigger_US.csv')
    df_t.to_csv(path, index=False)
    print(f'\n🎫 Trigger：{path}（{len(rows)} 張）')
    return path


def generate_evidence(results, output_folder=OUTPUT_FOLDER):
    rows = []
    for ticker, df in results.items():
        if df is None or len(df) == 0:
            continue
        r = df.iloc[-1]
        raw = r.get('Evidence_JSON')
        if not isinstance(raw, str) or not raw:
            continue
        try:
            ev = json.loads(raw)
        except Exception:
            continue
        for block, text, status in ev:
            rows.append({'Ticker': ticker, 'Block': block, 'Check': text, 'Status': status})
    if not rows:
        return None
    path = os.path.join(output_folder, 'Evidence_US.csv')
    pd.DataFrame(rows).to_csv(path, index=False)
    print(f'\n🧾 Evidence：{path}（{len(rows)} 條）')
    return path


def generate_handoff(summary_df, results, regime_info, output_folder=OUTPUT_FOLDER):
    """One page a bot can hand to layer 2: regime header, the actionable rows, file paths."""
    if summary_df is None or summary_df.empty:
        return None
    cols = ['Ticker', 'Candidate_Class', 'Setup_Family', 'Setup_Code', 'Entry_Feasible',
            'Entry_Ref', 'Invalidate_Below', 'Risk_ADR_Plan', 'Room_To_Supply_R',
            'Leader_OK', 'Volume_Confirm', 'BuyStop_Max_Stop', 'Class_Note', 'Setup_Why', 'Risk_Why']
    cols = [c for c in cols if c in summary_df.columns]
    _d = summary_df.get('Date', pd.Series([''])).iloc[0] if 'Date' in summary_df else ''
    lines = [f"# HANDOFF — {PROFILE['name']} swing scan {_d}".strip(), '']
    lines.append(f"REGIME   {regime_info.get('Regime_Label', '?')} / {regime_info.get('Regime_State', '?')} "
                 f"[{regime_info.get('Regime_Source', '?')}] · % >50D {regime_info.get('Breadth_50D', 'n/a')} "
                 f"(prev {regime_info.get('Breadth_Prev', 'n/a')}) · 10D ratio {regime_info.get('Ratio_10D', 'n/a')} "
                 f"· index second opinion {regime_info.get('Index_Regime_State', 'n/a')}")
    vc = summary_df['Candidate_Class'].value_counts()
    lines.append('COUNTS   ' + ' · '.join(f'{k} {int(vc.get(k, 0))}' for k in
                                          ['A_SETUP', 'C_WATCH', 'B_LEADER_WAIT', 'X_NONE']))
    lines.append('')
    for cls in ['A_SETUP', 'C_WATCH', 'B_LEADER_WAIT']:
        sub = summary_df[summary_df['Candidate_Class'] == cls]
        if sub.empty:
            continue
        lines.append(f'## {cls} ({len(sub)})')
        lines.append('')
        lines.append('| ' + ' | '.join(cols) + ' |')
        lines.append('|' + '---|' * len(cols))
        for _, r in sub.iterrows():
            cells = []
            for c in cols:
                v = r.get(c)
                if isinstance(v, float):
                    cells.append('' if pd.isna(v) else f'{v:.2f}')
                else:
                    cells.append(str(v))
            lines.append('| ' + ' | '.join(cells) + ' |')
        lines.append('')
    lines += [
        '## FILES',
        f'- contract: {os.path.join(output_folder, "Contract_US.csv")}',
        f'- evidence: {os.path.join(output_folder, "Evidence_US.csv")}',
        f'- trigger : {os.path.join(output_folder, "Trigger_US.csv")}',
        f'- rulebook: {os.path.join(output_folder, "RULEBOOK_US.md")}',
        '',
        '## LAYER 2 INSTRUCTIONS',
        '1. Read Contract_US.csv (one row per name) and Evidence_US.csv (one row per check).',
        '2. Do not invent levels: every price must come from those files.',
        '3. Quote the evidence you used; name any gate you override and why.',
        '4. Layer 1 issues no verdict. A_SETUP means "structure + usable risk", not "buy".',
        '5. Follow 01_RULES/US_SWING_SETUP_PROMPT_v53.md. Ignore any rule that names Tight_Zone_*, RR_* or Adjusted_Stop: those fields no longer exist.',
        '6. Regime is a header only: mention it, never use it to change a class.',
        '7. Read Volume_Confirm and Class_Note before calling a breakout. BuyStop_Max_Stop = lowest acceptable day-low at a buy-stop fill.',
    ]
    path = os.path.join(output_folder, 'handoff_US.md')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')
    print(f'\n🤝 HANDOFF：{path}')
    return path


def parse_tickers():
    env = os.environ.get('SWING_TICKERS', '').strip()
    if env:
        return [sanitize_ticker(t) for t in env.split(',') if t.strip()]
    try:
        user_input = input('\n📝 輸入股票代號（如 AAPL,NVDA）> ').strip()
    except EOFError:
        user_input = ''
    if not user_input:
        return list(DEFAULT_TICKERS)
    return [sanitize_ticker(t) for t in user_input.split(',') if t.strip()]


# =====================================================================
# Main
# =====================================================================
if __name__ == '__main__':
    print('=' * 60)
    print('🇺🇸 美股 Swing Trade 分析系統 v5.3 - 1f (review fixes; see CHANGELOG_v53.md)')
    print('=' * 60)
    if mcal is None:
        print('ℹ️ 未安裝 pandas_market_calendars，使用週末/收市緩衝近似交易日。')
        print('   建議：pip install pandas_market_calendars')

    tickers = parse_tickers()
    print(f'📋 Tickers: {", ".join(tickers)}')

    results = {}
    data_quality_records = []
    expected_last_date = get_latest_completed_us_session()
    print(f'\n🎯 預期最新完整交易日：{expected_last_date}')
    print(f'⏱️ Yahoo daily bar 緩衝時間：{LATEST_SESSION_BUFFER_MINUTES} 分鐘')

    spy_df = fetch_shared_spy(expected_last_date=expected_last_date, months=MONTHS, silent=False)
    earnings_overrides = load_earnings_overrides()

    # 1c: market regime banner (NASDAQ 10EMA vs 20EMA) — reported, never scored
    # 1e: the user's daily dashboard is the authoritative regime; the index is second opinion.
    gates.configure(PROFILE)
    regime_info = regime.evaluate_sheet(regime.fetch_sheet(), asof=expected_last_date,
                                        key=PROFILE['sheet_key'])
    index_regime = regime.evaluate(regime.fetch_index(PROFILE['index']), asof=expected_last_date)
    if not regime_info:
        regime_info = dict(index_regime)
        regime_info['Regime_Source'] = 'INDEX_FALLBACK'
    regime_info['Index_Regime_State'] = index_regime.get('Regime_State', 'UNKNOWN')
    print(f"🌡️ Regime [{regime_info.get('Regime_Source')}]: "
          f"{regime_info.get('Regime_Label', '?')} / {regime_info['Regime_State']} — {regime_info['Regime_Why']}")
    print(f"   指數第二意見（^IXIC 10/20EMA）: {index_regime.get('Regime_State')}")
    if regime_info['Regime_State'] != 'MOMENTUM':
        print('   ⚠️ 非 momentum mode：突破類候選的歷史期望值最差，清單請只作觀察。')

    for i, t in enumerate(tickers):
        try:
            df = fetch_swing_data_us(
                t, months=MONTHS, silent=False,
                expected_last_date=expected_last_date, spy_df=spy_df,
                data_quality_records=data_quality_records,
            )
            if df is not None:
                for k, v in regime_info.items():
                    df.loc[df.index[-1], k] = v
                results[t] = df
                write_ticker_csv(df, t)
        except Exception as e:
            print(f'❌ {t} 處理失敗：{type(e).__name__}: {e}')
            append_data_quality_record(
                data_quality_records, ticker=t, status='PROCESSING_ERROR',
                expected_date=expected_last_date, attempts=0, rows=0,
                error=f'{type(e).__name__}: {e}',
            )
        if i < len(tickers) - 1:
            time.sleep(INTER_TICKER_SLEEP_SEC)

    if results:
        summary = generate_summary(results)
        # 1d: universe breadth — a second opinion next to the index regime.
        try:
            last = {t: df.iloc[-1] for t, df in results.items() if df is not None and len(df)}
            above = [1 for r in last.values()
                     if pd.notna(r.get('MA50')) and r.get('Close') > r.get('MA50')]
            breadth = round(100.0 * len(above) / len(last), 1) if last else np.nan
        except Exception:
            breadth = np.nan
        if summary is not None and len(summary):
            summary['Pool_Above_MA50_Pct'] = breadth
            summary['Breadth_50D'] = regime_info.get('Breadth_50D', np.nan)
        regime_state = regime_info.get('Regime_State', 'UNKNOWN')
        if pd.notna(breadth):
            print(f"🌡️ Pool: {breadth:.0f}% of the {len(results)} scanned names above MA50 "
                  f"(hand-picked pool, not market breadth). "
                  f"Market % >50D from the sheet: {regime_info.get('Breadth_50D', 'n/a')}%.")
        generate_claude_slim(summary, results)
        generate_contract(results)
        generate_trigger(results)
        generate_evidence(results)
        generate_handoff(summary, results, regime_info)

    save_data_quality_report(data_quality_records)
    write_rulebook()
    print(f'\n✅ 完成。所有檔案已儲存於：{os.path.abspath(OUTPUT_FOLDER)}')
