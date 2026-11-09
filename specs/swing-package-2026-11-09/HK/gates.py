#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Three-gate evaluation (v5.3). Gates are facts about the setup's state — not a verdict.

* Four states: PASS / FAIL / UNKNOWN / PENDING. UNKNOWN is never a silent pass.
* Family selection (F5): TRIGGERED breakout > *valid* pullback/reversal > waiting base >
  invalid pullback (shown so you see why) > failed base > none. A Trend-Respect (D) pullback
  never masks a live base: inside a base, the base is the setup.
* Supply (F6) is measured from the ENTRY, not from today's close, and highs printed on or after
  the breakout bar are not "supply". Hard levels gate; soft levels are reported only.
* Breakout volume (F9): a trigger day under VOL_CONFIRM_MULT x 20-day volume is LOW.
  VOL_MODE='WATCH' downgrades A_SETUP to C_WATCH; VOL_MODE='REMARK' keeps the class and
  writes the remark into Class_Note.
* Risk for a breakout already triggered (F10) is re-measured from today's close (the
  next-open proxy) to the breakout-bar low. Before the trigger, Risk stays PENDING and the
  ticket carries BuyStop_Max_Stop: if, at your buy-stop fill, the day's low is below this
  price, the stop is wider than the band allows.
* The regime is a header only; it never changes a gate (user decision, 2026-11-05).
"""
import os

import numpy as np
import pandas as pd

PASS, FAIL, UNKNOWN, PENDING = 'PASS', 'FAIL', 'UNKNOWN', 'PENDING'

VOL_CONFIRM_MULT = 1.5
VOL_MODE = os.environ.get('SWING_VOL_MODE', 'WATCH').upper()   # 'WATCH' or 'REMARK'
PENDING_RISK_ADR = 1.0      # provisional breakout risk used ONLY to express room in R

CFG = {
    'leader': {'rs_min': 10.0, 'price_min': 5.0, 'dollar_vol_min': 20e6},
    'risk': {
        'band': {'BREAKOUT': (0.3, 1.2), 'PULLBACK': (0.8, 2.5), 'REVERSAL': (0.8, 2.5)},
        'room_min_r': {'BREAKOUT': 1.5, 'PULLBACK': 1.0, 'REVERSAL': 1.5},
        'ext_max_pct': 15.0,
        'rsi_max': 75.0,
        'ma50_ext_max_pct': 25.0,
        # v6.10 (ported from US v5.5.4, Justin 2026-11-08): a ticket must be risk-sane even
        # when Risk_OK=PENDING — a pending breakout used to skip the whole risk band.
        'cap_adr': float(os.environ.get('SWING_RISK_ADR_CAP', 1.2)),
        'cap_pct': float(os.environ.get('SWING_RISK_PCT_CAP', 8.0)),
    },
}

TICK_UP = None            # v6.7: set by configure() when the market has price bands
TICK_DOWN = None
PROFILE_CUR = '$'          # v6.4: set by configure(), used by the rulebook and the Leader_Why text


def configure(profile):
    """Per-market leader thresholds (markets.py). US defaults are the historical values."""
    CFG['leader']['rs_min'] = profile.get('rs_min', CFG['leader']['rs_min'])
    CFG['leader']['price_min'] = profile.get('price_min', CFG['leader']['price_min'])
    CFG['leader']['dollar_vol_min'] = profile.get('dollar_vol_min', CFG['leader']['dollar_vol_min'])
    CFG['leader']['cur'] = profile.get('cur') or __import__('markets').currency_symbol(profile)
    global PROFILE_CUR, TICK_UP, TICK_DOWN
    PROFILE_CUR = CFG['leader']['cur']
    if profile.get('tick'):
        import hk_micro
        TICK_UP = lambda p: hk_micro.round_to_tick(p, 'up')
        TICK_DOWN = lambda p: hk_micro.round_to_tick(p, 'down')
    else:
        TICK_UP = TICK_DOWN = None
    return CFG


TRIGGERED_STATES = ('TRIGGERED', 'SPENT', 'BO_FAILED')
WAITING_STATES = ('READY', 'ARMED', 'FORMING')
FAMILY_LABEL = {'BaseS': 'STRICT', 'BaseW': 'WIDE'}


def _num(v, d=np.nan):
    try:
        return float(v) if pd.notna(v) else d
    except Exception:
        return d


def _verdict(checks):
    if any(s == FAIL for s, _ in checks):
        return FAIL
    if any(s == UNKNOWN for s, _ in checks):
        return UNKNOWN
    if any(s == PENDING for s, _ in checks):
        return PENDING
    return PASS


def _why(checks, limit=3):
    bad = [t for s, t in checks if s != PASS]
    if not bad:
        return '; '.join(t for _, t in checks if t)
    return '; '.join(bad[:limit])


def _best(snaps, states):
    pool = [s for s in snaps if s['state'] in states and s.get('len', 0)]
    if not pool:
        return None
    return min(pool, key=lambda s: _num(s.get('width_atr'), 99))


# ---------------------------------------------------------------- supply (F6)
def find_supply(row, entry, df=None, exclude_from=None, family='BREAKOUT'):
    """Nearest overhead supply strictly above `entry`.

    Hard (gate): prior 20-bar high, prior 252-bar high, nearest unfilled bearish FVG.
    Soft (remark only): VAH_60D, AVWAP_HVD, AVWAP_20D_High, MA50/MA200 above entry.
    `exclude_from` = trigger date; bars on/after it are excluded from the high windows,
    because a breakout's own excursion is not supply.
    Returns dict(level, source, soft_level, soft_source).
    """
    out = {'level': np.nan, 'source': 'NONE_ABOVE', 'soft_level': np.nan, 'soft_source': 'NONE_ABOVE'}
    if not np.isfinite(entry) or entry <= 0:
        out['source'] = out['soft_source'] = 'NO_ENTRY'
        return out
    floor = entry * 1.002
    hard = []
    if df is not None and len(df) > 1:
        hist = df.iloc[:-1]
        if exclude_from is not None and pd.notna(exclude_from):
            try:
                hist = hist[hist.index < exclude_from]
            except Exception:
                pass
        if len(hist):
            hard.append((float(hist['High'].tail(20).max()), 'RES20_PRIOR'))
            if len(hist) >= 120:
                hard.append((float(hist['High'].tail(252).max()), 'HIGH52W_PRIOR'))
    else:
        hard += [(_num(row.get('Resistance_20D_Prior')), 'RES20_PRIOR'),
                 (_num(row.get('High_52W_Prior')), 'HIGH52W_PRIOR')]
    hard.append((_num(row.get('Bearish_FVG1_Lower')), 'BEAR_FVG'))
    soft = [(_num(row.get('VAH_60D')), 'VAH_60D'), (_num(row.get('AVWAP_HVD')), 'AVWAP_HVD'),
            (_num(row.get('AVWAP_20D_High')), 'AVWAP_20D_HIGH'), (_num(row.get('MA50')), 'MA50'),
            (_num(row.get('MA200')), 'MA200')]
    above = [(l, s) for l, s in hard if np.isfinite(l) and l > floor]
    if above:
        out['level'], out['source'] = min(above)
    sabove = [(l, s) for l, s in soft if np.isfinite(l) and l > floor]
    if sabove:
        out['soft_level'], out['soft_source'] = min(sabove)
    return out


def tradeability(risk_adr, risk_pct, room_r, room_plan, floor, pending, risk_ok,
                 cap_adr, cap_pct, family, adr=None):
    """Why a ticket is or is not tradeable. Ported from US v5.5.4 (2026-11-08).

    HK already refuses an out-of-band stop when Risk_OK is decided, but a *pending* breakout
    returns PENDING before the band is checked — which is how 2269.HK shipped as a STALK with a
    2.72xADR plan stop. The plan stop exists before the fill, so it can be judged now.

    The % cap floats up to `cap_adr x ADR`: a structural stop on an 11%-ADR name is ~12% by
    construction, and high-ADR names are the momentum cohort. Low-ADR names keep the strict cap.
    """
    f = []
    if adr is not None and np.isfinite(adr) and adr > 0:
        cap_pct = max(cap_pct, cap_adr * adr)
    if family == 'NONE':
        f.append('no setup')
    if not np.isfinite(risk_adr):
        f.append('risk unknown')
    elif risk_adr > cap_adr:
        f.append(f'risk={risk_adr:.2f}xADR > {cap_adr:g} (plan stop)')
    if np.isfinite(risk_pct) and risk_pct > cap_pct:
        f.append(f'risk={risk_pct:.1f}% > {cap_pct:g}%')
    if np.isfinite(room_r) and room_r < floor:
        f.append(f'room={room_r:.2f}R < {floor:g}')
    if np.isfinite(room_plan) and room_plan < floor:
        f.append(f'room@plan stop={room_plan:.2f}R < {floor:g}')
    if not pending and risk_ok != PASS:
        f.append(f'Risk_OK={risk_ok}')
    return f


def evaluate(row, snaps, pb=None, df=None, cfg=CFG, vol_mode=None):
    """snaps: base snapshots (STRICT + WIDE). pb: pullback.evaluate() result or None.
    df: the ticker history up to and including `row` (used for supply windows)."""
    vol_mode = (vol_mode or VOL_MODE).upper()
    if isinstance(snaps, dict):
        snaps = [snaps]
    out, ev, notes = {}, [], []

    # ---------------- family selection (F5) ----------------
    trig_base = _best(snaps, ('TRIGGERED',))
    wait_base = _best(snaps, WAITING_STATES)
    dead_base = _best(snaps, ('BO_FAILED', 'FAILED', 'EXPIRED', 'SPENT'))
    pb_valid = pb is not None and bool(pb.get('valid'))
    if pb_valid and pb['code'] == 'D' and wait_base is not None:
        pb_valid = False
        notes.append('D pullback inside a live base: base preferred')
    if trig_base is not None:
        family, snap, use_pb = 'BREAKOUT', trig_base, False
    elif pb_valid:
        family, snap, use_pb = pb.get('family', 'PULLBACK'), None, True
    elif wait_base is not None:
        family, snap, use_pb = 'BREAKOUT', wait_base, False
    elif pb is not None:
        family, snap, use_pb = pb.get('family', 'PULLBACK'), None, True
    elif dead_base is not None:
        family, snap, use_pb = 'BREAKOUT', dead_base, False
    else:
        family, snap, use_pb = 'NONE', None, False

    # ---------------- Leader ----------------
    close = _num(row.get('Close'))
    ma20, ma50 = _num(row.get('MA20')), _num(row.get('MA50'))
    slope50 = _num(row.get('SMA50_Slope'))
    mn = _num(row.get('Minervini_Trend_Basic'), 0)
    rs = _num(row.get('RS_Score'))
    rs_status = row.get('RS_Status', 'OK')
    line_up = bool(row.get('RS_Line_Up', False))
    nhigh = bool(row.get('RS_Line_NH', False))
    vol20 = _num(row.get('Vol_Avg_20'))
    dollar_vol = close * vol20 if np.isfinite(close) and np.isfinite(vol20) else np.nan
    soft = all(np.isfinite(x) for x in (close, ma20, ma50, slope50)) and \
        close > ma50 and close > ma20 and slope50 > 0
    checks = [(PASS, f"trend={'Minervini' if mn == 1 else 'soft'}")] if (mn == 1 or soft) \
        else [(FAIL, 'trend=broken (Close<=MA50/MA20 or slope<=0)')]
    if rs_status == UNKNOWN or not np.isfinite(rs):
        checks.append((UNKNOWN, 'RS=UNKNOWN (benchmark unavailable)'))
    elif rs >= cfg['leader']['rs_min']:
        checks.append((PASS, f"RS={rs:.1f}>={cfg['leader']['rs_min']:.0f}"
                             f" (line {'up' if line_up else 'flat'}{', at high' if nhigh else ''})"))
    else:
        checks.append((FAIL, f"RS={rs:.1f} < {cfg['leader']['rs_min']:.0f}"))
    if not np.isfinite(dollar_vol):
        checks.append((UNKNOWN, 'dollar volume=UNKNOWN'))
    elif close >= cfg['leader']['price_min'] and dollar_vol >= cfg['leader']['dollar_vol_min']:
        cur = cfg['leader'].get('cur', '$')
        checks.append((PASS, f'liq: {cur}{dollar_vol/1e6:.0f}M/day, px {cur}{close:.2f}'))
    else:
        cur = cfg['leader'].get('cur', '$')
        checks.append((FAIL, f'liq: {cur}{dollar_vol/1e6:.0f}M/day '
                             f'(need >={cur}{cfg["leader"]["dollar_vol_min"]/1e6:.0f}M), px {cur}{close:.2f}'))
    if str(row.get('RS_Stale', '')).lower() not in ('false', 'nan', 'none', ''):
        # v6.7: insert the reason and let _verdict decide (FAIL > UNKNOWN). Overwriting the
        # result turned a broken trend into UNKNOWN and broke I28's Evidence reconciliation.
        checks.insert(0, (UNKNOWN, 'RS window stale: >=3 missing sessions in 63; not like-for-like'))
        # Justin 2026-11-07: a stale window must yield UNKNOWN, never FAIL — missing data is
        # not a broken trend. Downgrade the whole LEADER block's FAILs (incl. trend=broken)
        # so the Evidence table and the verdict stay consistent with I28.
        checks = [(UNKNOWN if st == FAIL else st,
                   txt + ('；stale window — 資料不足，不作 FAIL' if st == FAIL else ''))
                  for st, txt in checks]
    out['Leader_OK'] = _verdict(checks)
    out['Leader_Why'] = _why(checks)
    ev += [('LEADER', t, s) for s, t in checks]

    # ---------------- Setup ----------------
    checks = []
    vol_confirm = 'NOT_APPL'   # never 'NA': pandas reads that as a missing value
    if family == 'BREAKOUT':
        state, blen = snap['state'], int(snap.get('len', 0))
        width = _num(snap.get('width_atr'))
        fname = FAMILY_LABEL.get(snap['family'], str(snap['family'])).lower()
        if state == 'BO_FAILED':
            checks.append((FAIL, f"breakout failed: closed below the breakout-bar low "
                                 f"{_num(snap.get('invalidate_below')):.2f}"))
        elif state == 'FAILED':
            checks.append((FAIL, f"base FAILED (close broke {_num(snap.get('low')):.2f})"))
        elif state == 'SPENT':
            checks.append((FAIL, f"base spent ({snap.get('days_since_trigger')} bars since trigger)"))
        elif state == 'EXPIRED':
            checks.append((FAIL, 'base expired without a trigger'))
        else:
            checks.append((PASS, f"{fname} base {state.lower()}, {blen}d long"))
            lmin, lmax = int(snap.get('len_min', 5)), int(snap.get('len_max', 40))
            if state != 'FORMING' and not (lmin <= blen <= lmax):
                checks.append((FAIL, f'len={blen}d outside {fname} {lmin}-{lmax}'))
            wmax = _num(snap.get('width_max'), 4.0)
            if not np.isfinite(width):
                checks.append((UNKNOWN, 'width=UNKNOWN (ATR missing)'))
            elif width > wmax:
                checks.append((FAIL, f'{fname} width={width:.1f}xATR > {wmax:.1f}'))
            else:
                checks.append((PASS, f'width={width:.1f}xATR'))
            if state == 'TRIGGERED':                                   # F9
                vr = _num(snap.get('trigger_vol_ratio'))
                if not np.isfinite(vr):
                    vol_confirm = 'UNKNOWN'
                elif vr >= VOL_CONFIRM_MULT:
                    vol_confirm = 'PASS'
                    checks.append((PASS, f'breakout volume {vr:.2f}x avg'))
                else:
                    vol_confirm = 'LOW'
                    notes.append(f'breakout volume {vr:.2f}x avg < {VOL_CONFIRM_MULT}x')
            else:
                vol_confirm = 'PENDING'
    elif use_pb:
        label = 'reversal' if family == 'REVERSAL' else 'pullback'
        if pb.get('valid'):
            checks.append((PASS, f"{label} setup {pb['code']} ({pb['name']}): {pb['why']}"))
        else:
            reason = pb['why'] if family == 'REVERSAL' else \
                f"pullback {pb['code']} was high-momentum ({pb['why']})"
            checks.append((FAIL, reason))
    else:
        checks.append((FAIL, 'no base in range and no pullback/reversal setup'))
    out['Setup_OK'] = _verdict(checks)
    out['Setup_Why'] = _why(checks)
    out['Setup_Family'] = family
    out['Setup_Code'] = pb['code'] if use_pb else ('A_BASE' if family == 'BREAKOUT' else 'NONE')
    ev += [('SETUP', t, s) for s, t in checks]

    # ---------------- Risk ----------------
    checks = []
    adr_pct = _num(row.get('ADR_Pct'))
    ext20 = _num(row.get('Extension_MA20_Pct'))
    d50 = _num(row.get('Dist_from_MA50_Pct'))
    rsi = _num(row.get('RSI_14'))
    epf = row.get('Earnings_Proximity_Flag', 'UNKNOWN')
    days_since = int(_num(snap.get('days_since_trigger'), -1)) if snap else -1
    state = snap['state'] if snap else 'NONE'
    triggered = family == 'BREAKOUT' and state in TRIGGERED_STATES
    pending = family == 'BREAKOUT' and state in WAITING_STATES
    exclude_from = None
    buystop_max_stop = np.nan
    entry_from_planned = False

    if use_pb:
        entry, inval = _num(pb.get('entry')), _num(pb.get('stop'))
        entry_src, risk_basis = 'at market (close)', pb.get('stop_type', 'STRUCT')
    elif triggered:
        inval = _num(snap.get('invalidate_below'))
        exclude_from = snap.get('trigger_date')
        if days_since <= 0:
            entry, entry_src = _num(snap.get('trigger_close')), 'trigger close'
        else:                                                           # F10
            entry, entry_src = close, f'current close (next-open proxy, {days_since}d after trigger)'
        risk_basis = 'TRIGGER_LOW'
    elif snap is not None:
        entry, inval = _num(snap.get('planned_trigger')), _num(snap.get('low'))
        entry_src, risk_basis = 'planned trigger (buy-stop)', 'BASE_LOW'
        entry_from_planned = True
    else:
        entry = inval = np.nan
        entry_src, risk_basis = 'none', 'NONE'

    # v6.8: snap the ticket to legal prices BEFORE any risk arithmetic, so Risk_OK,
    # Risk_Why, Risk_Pct_Plan and Risk_ADR_Plan all describe the price you can enter.
    if TICK_UP is not None:
        if np.isfinite(entry):
            entry = TICK_UP(entry)
        if np.isfinite(inval):
            inval = TICK_DOWN(inval)
    elif entry_from_planned and np.isfinite(entry):
        # US keeps its historical 2dp planned entry (v6.8 keeps the US contract identical)
        entry = round(entry, 2)

    lo, hi = cfg['risk']['band'].get(family, (0.3, 1.2))
    adr_abs = entry * adr_pct / 100 if np.isfinite(entry) and np.isfinite(adr_pct) else np.nan
    risk_pct = risk_adr = np.nan
    if not (np.isfinite(entry) and np.isfinite(inval)) or entry <= 0 or entry <= inval:
        checks.append((UNKNOWN if family != 'NONE' else FAIL,
                       'entry/invalidation unavailable' if family != 'NONE' else 'no setup, no ticket'))
    else:
        risk_pct = (entry - inval) / entry * 100
        risk_adr = risk_pct / adr_pct if np.isfinite(adr_pct) and adr_pct > 0 else np.nan
        if pending:
            buystop_max_stop = round(entry - hi * adr_abs, 2) if np.isfinite(adr_abs) else np.nan
            if TICK_UP is not None and np.isfinite(buystop_max_stop):
                buystop_max_stop = TICK_UP(buystop_max_stop)
            checks.append((PENDING, f'risk pending: stop = breakout-day low; at a buy-stop fill the '
                                    f'low must hold above {buystop_max_stop:.2f} ({hi}xADR)'))
        elif not np.isfinite(risk_adr):
            checks.append((UNKNOWN, 'ADR unavailable'))
        elif risk_adr < lo:
            checks.append((FAIL, f'risk={risk_adr:.2f}xADR < {lo} (stop inside noise)'))
        elif risk_adr > hi:
            checks.append((FAIL, f'risk={risk_adr:.2f}xADR > {hi} (stop too wide)'))
        else:
            checks.append((PASS, f'risk={risk_adr:.2f}xADR in [{lo},{hi}]'))

    sup = find_supply(row, entry, df=df, exclude_from=exclude_from, family=family)
    supply = sup['level']
    room_r = room_soft = np.nan
    floor = cfg['risk']['room_min_r'].get(family, 1.5)
    if pending and np.isfinite(adr_abs) and adr_abs > 0:
        unit, unit_txt = PENDING_RISK_ADR * adr_abs, f' (R = provisional {PENDING_RISK_ADR}xADR)'
    elif np.isfinite(entry) and np.isfinite(inval) and entry > inval:
        unit, unit_txt = entry - inval, ''
    else:
        unit, unit_txt = np.nan, ''
    if family == 'NONE':
        pass
    elif not np.isfinite(supply):
        checks.append((PASS, f"room: no hard supply above {entry:.2f} (blue sky)"
                       if np.isfinite(entry) else 'room: n/a'))
    elif not np.isfinite(unit):
        checks.append((UNKNOWN, 'room: risk unavailable'))
    else:
        room_r = (supply - entry) / unit
        if room_r < floor:
            checks.append((FAIL, f"room={room_r:.2f}R < {floor} ({sup['source']} {supply:.2f}){unit_txt}"))
        else:
            checks.append((PASS, f"room={room_r:.2f}R to {sup['source']} {supply:.2f}{unit_txt}"))
    if np.isfinite(sup['soft_level']) and np.isfinite(unit) and unit > 0:
        room_soft = (sup['soft_level'] - entry) / unit
        if room_soft < floor and (not np.isfinite(supply) or sup['soft_level'] < supply):
            notes.append(f"soft level {sup['soft_source']} {sup['soft_level']:.2f} at {room_soft:.2f}R")

    if epf == 'PASS':
        checks.append((FAIL, 'earnings within 7 sessions'))
    elif epf in ('CLEAR', 'CAUTION'):
        checks.append((PASS, f'earnings {epf}'))
    else:
        checks.append((UNKNOWN, 'earnings date UNKNOWN'))
    if np.isfinite(ext20) and ext20 > cfg['risk']['ext_max_pct']:
        checks.append((FAIL, f'extended {ext20:.1f}% > {cfg["risk"]["ext_max_pct"]:.0f}% above MA20'))
    elif np.isfinite(rsi) and rsi > cfg['risk']['rsi_max']:
        checks.append((FAIL, f'RSI {rsi:.0f} > {cfg["risk"]["rsi_max"]:.0f}'))
    elif np.isfinite(d50) and d50 > cfg['risk']['ma50_ext_max_pct']:
        checks.append((FAIL, f'extended {d50:.1f}% > {cfg["risk"]["ma50_ext_max_pct"]:.0f}% above MA50'))
    else:
        checks.append((PASS, 'not extended'))
    out['Risk_OK'] = _verdict(checks)
    out['Risk_Why'] = _why(checks)
    ev += [('RISK', t, s) for s, t in checks]

    # ---------------- Tradeable: can this be a ticket at all? (v6.10) ----------------
    _cap_adr, _cap_pct = cfg['risk']['cap_adr'], cfg['risk']['cap_pct']
    _floor = cfg['risk']['room_min_r'].get(family, 1.5)
    _room_plan = ((supply - entry) / (entry - inval)
                  if (np.isfinite(supply) and np.isfinite(entry) and np.isfinite(inval) and entry > inval)
                  else np.nan)
    _room_12 = ((supply - entry) / (_cap_adr * adr_abs)
                if (np.isfinite(supply) and np.isfinite(entry) and np.isfinite(adr_abs) and adr_abs > 0)
                else np.nan)
    _t_fail = tradeability(risk_adr, risk_pct, room_r, _room_plan, _floor, pending,
                           out['Risk_OK'], _cap_adr, _cap_pct, family, adr_pct)
    out['Tradeable'] = 'FAIL' if _t_fail else 'PASS'
    out['Tradeable_Why'] = '; '.join(_t_fail) if _t_fail else 'risk and room inside caps'
    out['Room_At_Plan_Stop_R'] = round(_room_plan, 4) if np.isfinite(_room_plan) else np.nan
    out['Room_At_1_2ADR_R'] = round(_room_12, 4) if np.isfinite(_room_12) else np.nan
    ev += [('TRADEABLE', out['Tradeable_Why'], out['Tradeable'])]

    # ---------------- Class + ticket ----------------
    L, S, R = out['Leader_OK'], out['Setup_OK'], out['Risk_OK']
    if S == PASS:
        cls = 'A_SETUP' if R == PASS else 'C_WATCH'
    elif S == UNKNOWN:
        cls = 'C_WATCH' if L == PASS else 'X_NONE'
    else:
        cls = 'B_LEADER_WAIT' if L == PASS else 'X_NONE'
    if cls == 'A_SETUP' and vol_confirm == 'LOW':                       # F9
        if vol_mode == 'REMARK':
            notes.append('REMARK: kept A_SETUP despite low breakout volume (SWING_VOL_MODE=REMARK)')
        else:
            cls = 'C_WATCH'
            notes.append('downgraded A_SETUP -> C_WATCH: breakout volume not confirmed')
    ev.append(('CONFIRM', f'breakout volume {vol_confirm}', {'PASS': PASS, 'LOW': FAIL,
                                                             'PENDING': PENDING}.get(vol_confirm, UNKNOWN)
               if vol_confirm != 'NOT_APPL' else PASS))

    if use_pb:
        feasible = 'AT_MARKET' if S == PASS else 'NO_SETUP'
    elif state == 'TRIGGERED':
        ds = max(days_since, 0)
        feasible = 'AT_TRIGGER' if ds == 0 else ('NEXT_DAY' if ds == 1 else 'LATE')
    elif state == 'SPENT':
        feasible = 'MISSED'
    elif state in ('BO_FAILED', 'FAILED', 'EXPIRED'):
        feasible = 'INVALIDATED'
    elif family == 'BREAKOUT':
        feasible = 'NOT_YET'
    else:
        feasible = 'NO_SETUP'

    shares = round(1000.0 / (entry - inval), 0) \
        if (not pending and np.isfinite(entry) and np.isfinite(inval) and entry > inval) else np.nan
    # v5.5: the six inputs the L2 quality score needs (computed in pullback.py, not new data)
    out.update({
        # v5.5.2 §5.1: the trend line reads these; they existed in the summary but not per row
        'Minervini_Trend': bool(_num(row.get('Minervini_Trend_Basic'), 0)),
        'Minervini_Stage2': bool(_num(row.get('Minervini_Stage2_Strict'), 0)),
        'Depth_ATR': _num(pb.get('depth_atr')) if pb and family in ('PULLBACK', 'REVERSAL') else np.nan,
        'Vol_Ratio_Pullback': _num(pb.get('vol_ratio')) if pb and family in ('PULLBACK', 'REVERSAL') else np.nan,
        'Confluence_Count': _num(pb.get('confluence_count')) if pb and family == 'PULLBACK' else np.nan,
        'Drawdown_Pct': _num(pb.get('drawdown_pct')) if pb and family == 'REVERSAL' else np.nan,
        'UpDown_Vol': _num(pb.get('updown_vol')) if pb and family == 'REVERSAL' else np.nan,
        'HigherLow_Pct': _num(pb.get('higher_low_pct')) if pb and family == 'REVERSAL' else np.nan,
    })
    out.update({
        'Candidate_Class': cls,
        'Class_Note': '; '.join(notes),
        'Volume_Confirm': vol_confirm,
        'Base_Family': FAMILY_LABEL.get(snap['family'], '') if snap else '',
        'Setup_Len_Days': int(snap.get('len', 0)) if snap else 0,
        'Base_Width_ATR': _num(snap.get('width_atr')) if snap else np.nan,
        'Base_Width_Pct': _num(snap.get('width_pct')) if snap else np.nan,
        'Base_Compressed_Pct': _num(snap.get('compressed_pct')) if snap else np.nan,
        'Base_Cleanliness': snap.get('cleanliness') if snap else np.nan,
        'Base_Vol_Decay': snap.get('vol_decay') if snap else np.nan,
        'Base_HigherLows_Pct': snap.get('higher_lows_pct') if snap else np.nan,
        'Base_Prior_Advance_Pct': snap.get('prior_advance_pct') if snap else np.nan,
        'Base_Count_126': snap.get('count_126') if snap else np.nan,
        'Base_State': state if snap else (family if use_pb else 'NONE'),
        'BaseS_State': next((s['state'] for s in snaps if s['family'] == 'BaseS'), 'NONE'),
        'BaseW_State': next((s['state'] for s in snaps if s['family'] == 'BaseW'), 'NONE'),
        'Pullback_Code': pb['code'] if pb else 'NONE',
        'Pullback_Candidates': pb.get('candidates', '') if pb else '',
        'Entry_Ref': entry,
        'Entry_Src': entry_src,
        'Invalidate_Below': inval,
        'Stop_Type_Plan': risk_basis,
        'Risk_Pct_Plan': risk_pct,
        'Risk_ADR_Plan': risk_adr,
        'Risk_Basis': risk_basis,
        'BuyStop_Max_Stop': buystop_max_stop,
        'Room_To_Supply_R': room_r,
        'Tradeable': out['Tradeable'],
        'Tradeable_Why': out['Tradeable_Why'],
        'Room_At_Plan_Stop_R': out['Room_At_Plan_Stop_R'],
        'Room_At_1_2ADR_R': out['Room_At_1_2ADR_R'],
        'Room_Basis': 'PROV_1ADR' if pending else ('RISK' if np.isfinite(room_r) else 'NONE'),
        'SR_Flip_Live': bool(row.get('SR_Flip_Live', False)),
        'SR_Flip_Age': _num(row.get('SR_Flip_Age')),
        'SR_Flip_Level': _num(row.get('SR_Flip_Level')),
        'Supply_Level': round(supply, 2) if np.isfinite(supply) else np.nan,
        'Supply_Source': sup['source'],
        'Supply_Soft_Level': round(sup['soft_level'], 2) if np.isfinite(sup['soft_level']) else np.nan,
        'Supply_Soft_Source': sup['soft_source'],
        'Room_To_Soft_R': room_soft,
        'Shares_per_1000_Risk': shares,
        'Entry_Feasible': feasible,
        'Trigger_Price': (TICK_UP(_num(snap.get('planned_trigger')))
                          if snap and np.isfinite(_num(snap.get('planned_trigger'))) and TICK_UP is not None
                          else (round(_num(snap.get('planned_trigger')), 2)
                                if snap and np.isfinite(_num(snap.get('planned_trigger')))
                                else (TICK_UP(entry) if (TICK_UP is not None and np.isfinite(entry))
                                      else (round(entry, 2) if np.isfinite(entry) else np.nan)))),
        'Trigger_Min_Vol': round(vol20 * VOL_CONFIRM_MULT) if np.isfinite(vol20) else np.nan,
        'Trigger_Date': snap.get('trigger_date') if snap else np.nan,
        'Days_Since_Trigger': days_since,
        'Trigger_Vol_Ratio': snap.get('trigger_vol_ratio') if snap else np.nan,
        'Evidence': ev,
    })
    return out
