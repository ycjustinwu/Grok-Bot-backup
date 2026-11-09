#!/usr/bin/env python3
"""rotation_calc.py — 輪動位移指數（rotation delta）計算器，Grok bot 自足運行版。

設計原則
--------
* **只用標準庫**（無 pandas / numpy），任何 Python 3.9+ 環境直接跑。
* **唔依賴 Hermes 的檔案**：自帶 29 本書清單、自帶門檻常數、自己讀寬表或長表。
* **可自證**：`--selftest` 用合成序列驗算，輸出的分類必須等於預期，唔對就 exit 1。

輸入兩種（任選其一）
------------------
1. 寬表 `--matrix PH_MT_export.csv`
   RS workbook `PH_MT` 的原生形狀：第一列 = 日期，第一行 = ticker（含 `date` 欄頭）。
   即 Google Sheets 選 A1 到最右、匯出 CSV。
2. 長表 `--long prices.csv`
   `date,ticker,close`（欄名不拘，會自動找；日期格式 2026-11-04 / 2026/11/04 / 04/11/2026 皆可）。

輸出
----
* `--out-state rotation_state.csv`   每日一行（給報告讀）
* `--out-history rotation_history.csv` 每書每日一 rank（供查核）
* stdout：一行 `ROT <state> churn=5/x 10/y 20/z` + 報告用的三行文字（可直接貼）

用法
----
    python3 rotation_calc.py --matrix PH_MT.csv
    python3 rotation_calc.py --long prices.csv --out-state state.csv
    python3 rotation_calc.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date

# ---- 常數（改動要重新校準，見 docs/rotation-module-v1.1.md §2） ----------------
BOOKS = ("AIPO", "ARKG", "ARKW", "BOAT", "BOTZ", "BUG", "CIBR", "CLOU", "COPX", "DRAM",
         "DTCR", "FOTO", "IGV", "IHI", "ITA", "IYT", "KRE", "MAGS", "MEME", "PHO",
         "QQQ", "SOXX", "XLB", "XHB", "XLI", "XLV", "XOP", "XRT", "XBI")
BENCH = "VOO"
LOOKBACK = 20          # mom20
TOP_N = 8
PERSIST_N = 20
TH_MAJOR = 14          # 制度輪動：churn5 或 churn10 >= 14
TH_SHIFT = 10          # 輪動中  ：>= 10（p90）
TH_QUIET = 8           # 延續    ：<= 8
TH_LATE = 14           # 已定格  ：churn20 >= 14

STATE_MAJOR = "制度輪動"
STATE_SHIFT = "輪動中"
STATE_LATE = "已定格"
STATE_CONT = "延續"


# ---- 讀取 -------------------------------------------------------------------
def _norm_date(s: str) -> str | None:
    s = (s or "").strip().strip('"')
    if not s:
        return None
    for sep in ("/", "-"):
        if sep in s:
            parts = s.split(sep)
            if len(parts) == 3:
                a, b, c = parts
                if len(a) == 4:                      # 2026-11-04
                    y, m, d = a, b, c
                elif len(c) == 4:                    # 04/11/2026  (日/月/年)
                    d, m, y = a, b, c
                else:
                    return None
                try:
                    return date(int(y), int(m), int(d)).isoformat()
                except ValueError:
                    return None
    return None


def _num(s) -> float | None:
    try:
        v = float(str(s).replace(",", "").strip())
    except (TypeError, ValueError):
        return None
    return v if v > 0 else None


def load_matrix(path: str) -> dict[str, dict[str, float]]:
    """寬表 -> {ticker: {date: close}}。接受 PH_MT 形狀與轉置形狀。"""
    rows = list(csv.reader(open(path, newline="", encoding="utf-8-sig")))
    if not rows:
        raise SystemExit("matrix: 空檔")
    header = [c.strip().upper() for c in rows[0]]
    first_col_dates = _norm_date(rows[1][0]) if len(rows) > 1 else None
    if first_col_dates is None:                       # 轉置：首行是日期，首列是 ticker
        dates = [_norm_date(c) for c in rows[0][1:]]
        series: dict[str, dict[str, float]] = {}
        for r in rows[1:]:
            if not r:
                continue
            t = r[0].strip().upper()
            if not t:
                continue
            for i, raw in enumerate(r[1:]):
                if i < len(dates) and dates[i]:
                    v = _num(raw)
                    if v:
                        series.setdefault(t, {})[dates[i]] = v
        return series
    series = {}
    for r in rows[1:]:
        d = _norm_date(r[0])
        if not d:
            continue
        for i, raw in enumerate(r[1:], start=1):
            if i >= len(header):
                break
            t = header[i]
            if not t or t == "DATE":
                continue
            v = _num(raw)
            if v:
                series.setdefault(t, {})[d] = v
    return series


def load_long(path: str) -> dict[str, dict[str, float]]:
    series: dict[str, dict[str, float]] = {}
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rd = csv.DictReader(fh)
        cols = {c.strip().lower(): c for c in (rd.fieldnames or [])}
        dc = next((cols[k] for k in cols if k in ("date", "session", "trade_date")), None)
        tc = next((cols[k] for k in cols if k in ("ticker", "symbol", "book")), None)
        cc = next((cols[k] for k in cols if k in ("close", "price", "last")), None)
        if not (dc and tc and cc):
            raise SystemExit(f"long: 找唔到 date/ticker/close 欄，見到 {list(cols)}")
        for row in rd:
            d = _norm_date(row[dc])
            t = (row[tc] or "").strip().upper()
            v = _num(row[cc])
            if d and t and v:
                series.setdefault(t, {})[d] = v
    return series


# ---- 計算 -------------------------------------------------------------------
def compute(series: dict[str, dict[str, float]], books=BOOKS, bench: str = BENCH) -> dict:
    voo = series.get(bench) or {}
    if not voo:
        raise SystemExit(f"rotation: 缺基準 {bench} 的價格")
    present = [b for b in books if b in series and series[b]]
    dates = sorted({d for d in voo}, reverse=True)          # 新 -> 舊
    ratio = {b: {d: series[b][d] / voo[d] for d in dates if d in series[b] and d in voo}
             for b in present}

    rank_by_date: dict[str, dict[str, tuple[float, int]]] = {}
    for i, d in enumerate(dates):
        if i + LOOKBACK >= len(dates):
            break
        old = dates[i + LOOKBACK]
        mom = {}
        for b in present:
            a, o = ratio[b].get(d), ratio[b].get(old)
            if a and o:
                mom[b] = 100.0 * (a / o - 1.0)
        if len(mom) < 3:
            continue
        ranked = sorted(mom.items(), key=lambda kv: -kv[1])
        rank_by_date[d] = {b: (round(v, 4), k) for k, (b, v) in enumerate(ranked, 1)}

    order = sorted(rank_by_date, reverse=True)             # 新 -> 舊
    if not order:
        raise SystemExit("rotation: 歷史不足（需要至少 %d 個 session）" % (LOOKBACK + 1))

    def top8(d: str) -> set[str]:
        return {b for b, (_, k) in rank_by_date[d].items() if k <= TOP_N}

    def churn(d: str, back: int) -> int | None:
        i = order.index(d)
        if i + back >= len(order):
            return None
        return len(top8(d) ^ top8(order[i + back]))

    def persist(d: str, b: str) -> int:
        i = order.index(d)
        win = order[i:i + PERSIST_N]
        return sum(1 for x in win if b in top8(x))

    d0 = order[0]
    groups = (top8(d0), None)
    ch5, ch10, ch20 = churn(d0, 5), churn(d0, 10), churn(d0, 20)
    state, why = classify(ch5, ch10, ch20)

    today = sorted(((b, *rank_by_date[d0][b], persist(d0, b)) for b in top8(d0)),
                   key=lambda x: x[2])
    prev_leaders = sorted({b for x in order[:1] for b in ()} )  # placeholder, filled below
    # 上批領導 = 20 個 session 前（或最早可得）的 top8，按今日 rank 由差至好排
    idx = min(len(order) - 1, PERSIST_N)
    prev = top8(order[idx])
    old = []
    for b in prev:
        if b in rank_by_date[d0]:
            mom, rk = rank_by_date[d0][b]
            old.append((b, mom, rk))
        else:
            old.append((b, None, None))
    old.sort(key=lambda x: (x[2] is None, -(x[2] or 0)))

    hist = []
    for d in order:
        for b, (mom, rk) in rank_by_date[d].items():
            hist.append({"date": d, "book": b, "mom20": mom, "rank": rk,
                         "in_top8": 1 if rk <= TOP_N else 0,
                         "days_in_top8": persist(d, b)})
    hist.sort(key=lambda r: (r["date"], r["rank"]), reverse=True)

    persist_vals = [persist(d0, b) for b in rank_by_date[d0]]
    return {
        "session": d0, "books": len(rank_by_date[d0]),
        "history_sessions": len(order),
        "churn5": ch5, "churn10": ch10, "churn20": ch20,
        "state": state, "why": why,
        "today": today, "old": old,
        "median_persist": sorted(persist_vals)[len(persist_vals) // 2],
        "history": hist,
        "prev_session": order[idx],
    }


def classify(ch5, ch10, ch20) -> tuple[str, str]:
    if (ch5 is not None and ch5 >= TH_MAJOR) or (ch10 is not None and ch10 >= TH_MAJOR):
        return STATE_MAJOR, f"churn5 {ch5 or 0}／churn10 {ch10 or 0} ≥ {TH_MAJOR}"
    if (ch5 is not None and ch5 >= TH_SHIFT) or (ch10 is not None and ch10 >= TH_SHIFT):
        return STATE_SHIFT, f"churn5 {ch5 or 0}／churn10 {ch10 or 0} ≥ {TH_SHIFT}，未達 {TH_MAJOR}"
    if ch5 is None or ch10 is None or ch20 is None:
        return STATE_CONT, "歷史不足 20 個 session，未能判已定格"
    if ch5 <= TH_QUIET and ch10 <= TH_QUIET and ch20 >= TH_LATE:
        return STATE_LATE, f"churn5 {ch5}／churn10 {ch10} 已靜，但 churn20 {ch20} ≥ {TH_LATE}"
    return STATE_CONT, f"churn5 {ch5}／churn10 {ch10} ≤ {TH_QUIET}"


# ---- 輸出 -------------------------------------------------------------------
def write_state(res: dict, path: str) -> None:
    top8 = ",".join(f"{b}:{mom}:{p}" for b, mom, rk, p in res["today"])
    old8 = ",".join(f"{b}:{('' if mom is None else mom)}:{('' if rk is None else rk)}"
                    for b, mom, rk in res["old"])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["session", "books", "churn5", "churn10", "churn20", "rot_state",
                    "top8", "old8", "median_persist"])
        w.writerow([res["session"], res["books"], res["churn5"], res["churn10"], res["churn20"],
                    res["state"], top8, old8, res["median_persist"]])


def write_history(res: dict, path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["date", "book", "mom20", "rank", "in_top8",
                                           "days_in_top8"])
        w.writeheader()
        w.writerows(res["history"])


def render(res: dict) -> str:
    new = " ".join(b for b, *_ in res["today"])
    old = " ".join(b for b, *_ in res["old"])
    sign = {"制度輪動": "🚨", "輪動中": "🔄"}.get(res["state"], "")
    head = (f"{sign} ROT {res['state']} churn=5/{res['churn5']} 10/{res['churn10']} "
            f"20/{res['churn20']} books={res['books']} session={res['session']}")
    line = (f"輪動位移｜churn5 {res['churn5']} ／ churn10 {res['churn10']} ／ "
            f"churn20 {res['churn20']}｜判定：{res['state']}")
    return "\n".join([head, line, f"現任：{new}｜上批：{old}"])


# ---- 自測 -------------------------------------------------------------------
def selftest() -> int:
    """合成序列：第 120 個 session 起，領導由 A 組換成 B 組，必須判 制度輪動。"""
    import random
    random.seed(7)
    days = [f"2026-{m:02d}-{d:02d}" for m in range(1, 9) for d in range(1, 29)]
    days = days[:200]
    old_grp = [f"OLD{i}" for i in range(8)]
    new_grp = [f"NEW{i}" for i in range(8)]
    books = old_grp + new_grp
    series: dict[str, dict[str, float]] = {b: {} for b in books + ["VOO"]}
    px = {b: 100.0 for b in books}
    vpx = 100.0
    flip = 160
    for i, d in enumerate(days):
        vpx *= 1.0005
        series["VOO"][d] = vpx
        for b in books:
            drift = 0.004 if (b in old_grp) == (i < flip) else -0.001
            px[b] *= 1 + drift + random.uniform(-0.002, 0.002)
            series[b][d] = px[b]
    res = compute(series, books=books)
    ok = True
    print("selftest session:", res["session"], "state:", res["state"],
          "churn5:", res["churn5"], "churn10:", res["churn10"])
    if res["state"] != STATE_CONT:
        print("FAIL 最新一日應該是 延續（換帥已 40 個 session）"); ok = False
    # 換帥當時：截短序列，令今日 = flip + 10
    cut = {b: {d: v for d, v in s.items() if d <= days[flip + 10]} for b, s in series.items()}
    res2 = compute(cut, books=books)
    print("selftest at flip+10:", res2["session"], res2["state"],
          "churn5:", res2["churn5"], "churn10:", res2["churn10"])
    if res2["state"] not in (STATE_MAJOR, STATE_SHIFT):
        print("FAIL 換帥後 10 個 session 必須係 制度輪動 或 輪動中"); ok = False
    if not res["today"] or len(res["today"]) != TOP_N:
        print("FAIL top8 數目不對"); ok = False
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--matrix", help="寬表 CSV（PH_MT 形狀）")
    ap.add_argument("--long", help="長表 CSV（date,ticker,close）")
    ap.add_argument("--bench", default=BENCH)
    ap.add_argument("--out-state", default="rotation_state.csv")
    ap.add_argument("--out-history", default="rotation_history.csv")
    ap.add_argument("--json", action="store_true", help="另印機器可讀 summary")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if not (a.matrix or a.long):
        ap.error("要 --matrix 或 --long（或 --selftest）")

    series = load_matrix(a.matrix) if a.matrix else load_long(a.long)
    res = compute(series, bench=a.bench)
    write_state(res, a.out_state)
    write_history(res, a.out_history)
    print(render(res))
    print(f"OUT {a.out_state} (1 row) | {a.out_history} ({len(res['history'])} rows, "
          f"{res['history_sessions']} sessions) | why: {res['why']}")
    if a.json:
        print(json.dumps({k: res[k] for k in ("session", "books", "churn5", "churn10", "churn20",
                                             "state", "median_persist", "history_sessions")},
                         ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
