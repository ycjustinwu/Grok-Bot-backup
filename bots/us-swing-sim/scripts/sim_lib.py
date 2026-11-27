#!/usr/bin/env python3
"""Shared helpers for US swing sim daily scripts. No invented prices. No MCP."""
from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ROOT = Path("/workspace/us-swing-sim")
HKT = ZoneInfo("Asia/Hong_Kong")
TV_SHORTLIST_ID = "351605193"

# WATCH_GAP uses documented precedents only — no invented cutoff.
# WATCH_GAP: 11/09 UNTY 2.11%, 11/13 UNTY 2.12%, 11/12 DNA ~2.20%.
# HOLD: 11/12 UNTY 4.25% (pre-trim), TEM 4.48%.
WATCH_GAP_MAX_PCT = 2.20
HOLD_MIN_PCT = 4.25

TERMINAL_ORDER = {"filled", "cancelled", "canceled", "reversed", "expired", "void"}
ACTIVE_ORDER = {"working", "pending", "pending_market_open", "queued", "open", "live"}

KNOWN_EXCHANGE = {
    "UNTY": "NASDAQ",
    "TEM": "NASDAQ",
    "FRSH": "NASDAQ",
    "LIFE": "NASDAQ",
    "AUGO": "NASDAQ",
    "RDWR": "NASDAQ",
    "ABSI": "NASDAQ",
    "ESTC": "NASDAQ",
    "TWST": "NASDAQ",
    "ZETA": "NASDAQ",
    "PANW": "NASDAQ",
    "CRWD": "NASDAQ",
    "ABCL": "NASDAQ",
    "WMG": "NASDAQ",
    "DNA": "NYSE",
    "CRL": "NYSE",
    "EL": "NYSE",
    "DK": "NYSE",
    "FRO": "NYSE",
    "HAFN": "NYSE",
    "NEOG": "NYSE",
    "P": "NYSE",
    "RNG": "NYSE",
    "SNOW": "NYSE",
    "PSX": "NYSE",
}


def money(x: Any) -> float:
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def pct2(x: Any) -> float:
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def room4(x: Any) -> float:
    return float(Decimal(str(x)).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))


def now_hkt() -> str:
    return datetime.now(HKT).strftime("%Y-%m-%d %H:%M HKT")


def load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def iter_json_dir(folder: Path) -> list[tuple[Path, dict]]:
    out = []
    if not folder.is_dir():
        return out
    for p in sorted(folder.glob("*.json")):
        if p.name.startswith("_") or p.name in {"FORMAT.json"}:
            continue
        try:
            d = load_json(p)
        except json.JSONDecodeError:
            continue
        if isinstance(d, dict):
            out.append((p, d))
    return out


def open_positions(root: Path = ROOT) -> list[dict]:
    rows = []
    for p, d in iter_json_dir(root / "positions"):
        if str(d.get("status", "open")).lower() == "open":
            d["_path"] = str(p)
            rows.append(d)
    return rows


def active_orders(root: Path = ROOT) -> list[dict]:
    rows = []
    for p, d in iter_json_dir(root / "orders"):
        st = str(d.get("status") or "").lower()
        if st in TERMINAL_ORDER:
            continue
        if st in ACTIVE_ORDER or (d.get("order_type") and st and st not in TERMINAL_ORDER):
            d["_path"] = str(p)
            rows.append(d)
    return rows


def exchange_of(obj: dict, ticker: str | None = None) -> str:
    t = (ticker or obj.get("ticker") or "").upper()
    ex = obj.get("exchange")
    if ex:
        return str(ex).upper()
    return KNOWN_EXCHANGE.get(t, "")


def tv_symbol(ticker: str, obj: dict | None = None) -> str:
    ex = exchange_of(obj or {}, ticker)
    if not ex:
        return ticker.upper()
    return f"{ex}:{ticker.upper()}"


def desired_shortlist(root: Path = ROOT) -> list[str]:
    seen: list[str] = []
    for pos in open_positions(root):
        s = tv_symbol(pos["ticker"], pos)
        if s not in seen:
            seen.append(s)
    for od in active_orders(root):
        s = tv_symbol(od["ticker"], od)
        if s not in seen:
            seen.append(s)
    pf = load_json(root / "state" / "portfolio.json")
    for t in pf.get("observe") or []:
        if isinstance(t, dict):
            ticker = t.get("ticker")
            s = tv_symbol(ticker, t)
        else:
            s = tv_symbol(str(t), {})
        if s not in seen:
            seen.append(s)
    return seen


def risk_per_share(pos: dict) -> float | None:
    pl, ps = pos.get("plan_limit"), pos.get("plan_stop")
    if pl is not None and ps is not None:
        r = abs(float(pl) - float(ps))
        if r > 0:
            return r
    entry, stop = pos.get("entry"), pos.get("stop")
    if entry is not None and stop is not None:
        r = abs(float(entry) - float(stop))
        if r > 0:
            return r
    return None


def remaining_room_r(pos: dict, close: float) -> float | None:
    supply = pos.get("Supply_Level")
    if supply is None:
        sn = pos.get("structure_notes") or {}
        supply = sn.get("soft_supply") or sn.get("hard_room_level")
    risk = risk_per_share(pos)
    if supply is None or risk is None or risk == 0:
        return None
    return room4((float(supply) - float(close)) / risk)


def classify_watch_gap(near: float | None, stop: float) -> dict:
    """Cushion vs Hard SL. Never an exit. Official Open decides GAP_SL."""
    if near is None:
        return {
            "action": "NO_PM",
            "cushion_usd": None,
            "cushion_pct": None,
            "ask": False,
            "note": "無近價／盤前價，唔 invent；等官方 Open",
        }
    near_f, stop_f = float(near), float(stop)
    cushion_usd = money(near_f - stop_f)
    if stop_f == 0:
        return {
            "action": "TIGHT",
            "cushion_usd": cushion_usd,
            "cushion_pct": None,
            "ask": True,
            "note": "stop=0，無法算 cushion %，ask Justin",
        }
    cushion_pct = pct2((near_f - stop_f) / stop_f * 100.0)
    if near_f < stop_f:
        return {
            "action": "WATCH_GAP",
            "cushion_usd": cushion_usd,
            "cushion_pct": cushion_pct,
            "ask": False,
            "note": f"近價已低過 SL（cushion {cushion_pct}%）但仍唔出場；官方 Open < {stop_f} 先 GAP_SL",
        }
    if cushion_pct <= WATCH_GAP_MAX_PCT:
        return {
            "action": "WATCH_GAP",
            "cushion_usd": cushion_usd,
            "cushion_pct": cushion_pct,
            "ask": False,
            "note": f"距 SL 只得 ${cushion_usd}／{cushion_pct}%（≤{WATCH_GAP_MAX_PCT}% 先例）",
        }
    if cushion_pct >= HOLD_MIN_PCT:
        return {
            "action": "HOLD",
            "cushion_usd": cushion_usd,
            "cushion_pct": cushion_pct,
            "ask": False,
            "note": f"cushion {cushion_pct}%（≥{HOLD_MIN_PCT}% 先例）→ 唔係 WATCH_GAP",
        }
    return {
        "action": "TIGHT",
        "cushion_usd": cushion_usd,
        "cushion_pct": cushion_pct,
        "ask": True,
        "note": f"cushion {cushion_pct}% 介乎 WATCH_GAP 先例 {WATCH_GAP_MAX_PCT}% 同 HOLD 先例 {HOLD_MIN_PCT}% — 唔發明界線，ask Justin 標法；官方 Open < {stop_f} 仍係 GAP_SL",
    }


def better_buy_fill(limit: float, open_: float, low: float) -> float | None:
    """limit_buy: Low ≤ limit → fill. better-price-v1: min(limit, Open). No slippage."""
    if float(low) > float(limit):
        return None
    return money(min(float(limit), float(open_)))


def reanchor_stop(plan_limit: float, plan_stop: float, fill: float) -> tuple[float, float]:
    """better-price-stop-reanchor-v1: keep plan $ risk. Returns (new_stop, risk_per_share)."""
    risk = abs(float(plan_limit) - float(plan_stop))
    new_stop = money(float(fill) - risk) if fill >= plan_stop else money(float(fill) + risk)
    # long book: new_stop = fill - plan_$risk
    new_stop = money(float(fill) - risk)
    return new_stop, risk


def ema9_continue(prev_ema9: float, close: float, k: float = 0.2) -> float:
    return float(close) * k + float(prev_ema9) * (1.0 - k)


def require_ohlc(mark: dict, ticker: str, need: tuple[str, ...] = ("open", "high", "low", "close")) -> list[str]:
    missing = [k for k in need if mark.get(k) is None]
    return [f"{ticker} missing official {k}" for k in missing]


def supply_half_revoked(root: Path = ROOT) -> bool:
    rules = load_json(root / "state" / "rules.json")
    for row in rules.get("revoked_rules") or []:
        if row.get("rule_id") == "supply-half-fill-v1":
            return True
    return "supply-half-fill-v1" not in {
        r.get("rule_id") for r in (rules.get("rules") or []) if isinstance(r, dict)
    }
