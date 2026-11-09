#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S7 renderer (v5.5) — 投資快報 + GPT Image pack, built from data, not hand-written.

Usage:  python3 render_report.py <run_folder> [TICKER ...]
Reads:  L2_Input.csv (numbers, from L1) + verdicts_<market>.jsonl (story text, from L2)
Writes: <run>/reports/<TICKER>_投資快報.md and <TICKER>_image_pack.md, + index.md
Exit 2 if a text field breaks a length / tag rule (Hermes must not send that ticker).

Rule: every price, ratio and status comes from L2_Input.csv. L2 supplies prose only.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

KEEP_NA = dict(keep_default_na=False, na_values=[''])
EMO = {'BUY': ('🚀火箭升空', '✅穩陣上車'), 'STALK': ('⚡觀望等位',), 'WATCH': ('⚡觀望等位',),
       'AVOID': ('❌敬而遠之', '⚠️刀口舔血')}
VERDICT_ZH = {'BUY': 'BUY 買入', 'STALK': 'STALK 掛單等觸發', 'WATCH': 'WATCH 觀察', 'AVOID': 'AVOID 避開'}
SETUP_ZH = {'A_BASE': '平台突破', 'B': '回調至支撐', 'D': '沿 MA10 趨勢回調', 'H': '阻力轉支撐回測',
            'E': '底部反轉'}
LIMITS = {'story_main': 150, 'closer': 60, 'invalidation': 100}
SEP = '───────────────────────────────────────────'
BAR = '══════════════════════════════════════════════'


def n(v):
    try:
        return float(v) if v not in ('', None) else np.nan
    except Exception:
        return np.nan


_CUR = '$'          # set per row: HK rows report in HK$


def p(v, nd=2, pre=None):
    x = n(v)
    pre = _CUR if pre is None else pre
    return f'{pre}{x:,.{nd}f}' if np.isfinite(x) else '—'


def fx(v, nd=2):
    x = n(v)
    return f'{x:.{nd}f}' if np.isfinite(x) else '—'


def isval(x):
    """NaN-safe truthiness: pandas reads an empty cell as NaN, and NaN is truthy."""
    if x is None:
        return False
    try:
        if pd.isna(x):
            return False
    except Exception:
        pass
    return str(x).strip() not in ('', 'nan', 'None', 'MISSING')


def stars(grade):
    return {'A+': '⭐⭐⭐', 'A': '⭐⭐', 'B': '⭐'}.get(grade, '—')


def zlen(s):
    return len(str(s).replace(' ', ''))


def validate(v, r):
    errs = []
    for k, lim in LIMITS.items():
        if zlen(v.get(k, '')) > lim:
            errs.append(f'{k} {zlen(v.get(k, ""))}>{lim} chars')
    if v.get('emotion') not in EMO.get(v['verdict'], ()):
        errs.append(f"emotion {v.get('emotion')} not allowed for {v['verdict']}")
    if len(v.get('risks', [])) > 4:
        errs.append('more than 4 risks')
    for bad in ('目標', 'Target', 'T1', 'T2', 'T3', 'RR'):
        if bad in v.get('story_main', '') + v.get('closer', '') + ''.join(v.get('risks', [])):
            errs.append(f"retired term '{bad}' in text (v5 has no target / RR)")
    return errs


def entry_lines(v, r):
    ef, verdict = r['Entry_Feasible'], v['verdict']
    if ef == 'NOT_YET':
        return [f"- ① buy-stop：{p(r['Trigger_Price'])}（收市或盤中突破平台高）",
                f"- 條件：成交量 ≥ {p(r.get('Trigger_Min_Vol'), 0, '')} 股；成交當日低需高於 {p(r.get('BuyStop_Max_Stop'))}，否則放棄"]
    lines = [f"- ① {r.get('Entry_Src') or 'entry'}：{p(r['Entry_Ref'])}"
             + ('' if verdict == 'BUY' else '（暫不建議）')]
    if verdict != 'BUY' and isval(r.get('Speak_Up')):
        lines.append(f"- ② 重新評估條件：{r['Speak_Up']}")
    return lines


def stop_line(r):
    if r['Entry_Feasible'] == 'NOT_YET':
        return f"止損：突破日低（成交後確定）｜平台失效位 {p(r['Invalidate_Below'])}"
    return f"止損：{p(r['Invalidate_Below'])}（{r.get('Stop_Type_Plan', '')}）"


def supply_text(r):
    if np.isfinite(n(r.get('Supply_Level'))):
        return f"上方阻力 {p(r['Supply_Level'])}（{r.get('Supply_Source')}，{fx(r.get('Room_To_Supply_R'), 2)}R" \
               + ('，以 1×ADR 作 R' if r.get('Room_Basis') == 'PROV_1ADR' else '') + '）'
    return '上方無硬阻力（藍天）'


LADDER = (('MA10', 'MA10'), ('MA20', 'MA20'), ('MA50', 'MA50'),
          ('AVWAP_20D_Low', 'AVWAP_20D_Low'), ('POC_60D', 'POC_60D'),
          ('VAL_60D', 'VAL_60D'), ('SR_Flip_Level', 'SR_Flip_Level'))


def ladder(r):
    """Every L1 level below the close, nearest first. Filled by the program, never by L2."""
    close = n(r.get('Close'))
    out = []
    for col, label in LADDER:
        x = n(r.get(col))
        if np.isfinite(x) and np.isfinite(close) and 0 < x < close:
            out.append((label, x, (close - x) / close * 100))
    out.sort(key=lambda t: -t[1])
    return out


def trend_line(r):
    parts = []
    if isval(r.get('Minervini_Trend')):
        parts.append('Minervini ' + ('Y' if str(r.get('Minervini_Trend')) in ('1', 'True', '1.0') else 'N'))
    if isval(r.get('Minervini_Stage2')):
        parts.append('Stage2 ' + ('Y' if str(r.get('Minervini_Stage2')) in ('1', 'True', '1.0') else 'N'))
    slope = n(r.get('SMA50_Slope'))
    if np.isfinite(slope):
        parts.append(f'MA50 斜率 {slope:+.2f}%（10 日）')
    return ' ／ '.join(parts)


def tech_table(r):
    rs = f"{fx(r.get('RS_Score'), 1)}（1M {fx(r.get('RS_1M'), 1)} / 3M {fx(r.get('RS_3M'), 1)}）" \
        if np.isfinite(n(r.get('RS_Score'))) else 'UNKNOWN'
    code = r.get('Setup_Code', 'NONE')
    setup = f"{r.get('Setup_Family')}/{code} {SETUP_ZH.get(code, '')}".strip()
    if isval(r.get('Base_Family')):
        setup += f"｜{r['Base_Family']} base {r.get('Setup_Len_Days') or '—'} 日，{fx(r.get('Base_Width_ATR'), 1)}×ATR"
    vol = (f"突破量 {r.get('Volume_Confirm')}" + (f" {fx(r.get('Trigger_Vol_Ratio'), 2)}×" if np.isfinite(n(r.get('Trigger_Vol_Ratio'))) else '')
           if r.get('Setup_Family') == 'BREAKOUT' else '不適用（非突破）')
    dry = f"｜底部量縮 {fx(r.get('Base_Vol_Decay'), 2)}（低=好）" if np.isfinite(n(r.get('Base_Vol_Decay'))) else ''
    days = n(r.get('Days_To_Earnings'))
    earn = f"{r.get('Earnings_Proximity_Flag')}" + (
        f" · {r['Earnings_Date']} · {int(days)} 個交易日" if isval(r.get('Earnings_Date')) and np.isfinite(days)
        else (' · 日期未知' if not isval(r.get('Earnings_Date')) else f" · {r['Earnings_Date']}"))
    rows = [
        ('質素', (f"NA（資料不足）" if str(r.get('Setup_Quality_Grade')) == 'NA'
                  else f"{r.get('Setup_Quality_Grade')}（{p(r.get('Setup_Quality'), 0, '')}/5）"),
         stars(r.get('Setup_Quality_Grade'))),
        (f"RS（對 {r.get('Benchmark') if isval(r.get('Benchmark')) else 'SPY'}）", rs,
         f"Leader {r.get('Leader_OK')}"),
        ('Setup', setup, f"{r.get('Base_State')} · {r.get('Entry_Feasible')}"),
        ('三閘', f"Leader {r.get('Leader_OK')} · Setup {r.get('Setup_OK')} · Risk {r.get('Risk_OK')}", r.get('Candidate_Class')),
        ('風險 / 空間', f"{fx(r.get('Risk_Pct_Plan'), 1)}% = {fx(r.get('Risk_ADR_Plan'), 2)}×ADR", supply_text(r)),
        ('量能', vol + dry, ''),
        ('延伸 / RSI', f"Ext_MA20 {fx(r.get('Extension_MA20_Pct'), 1)}%｜RSI_14 {fx(r.get('RSI_14'), 1)}", ''),
        ('財報', earn + ('（未能確認，請自行核實）' if r.get('Earnings_Proximity_Flag') == 'UNKNOWN' else ''), ''),
        ('今日變化', r.get('Change_vs_Prev', ''), ''),
    ]
    if trend_line(r):
        rows.insert(1, ('趨勢', trend_line(r), ''))
    lad = ladder(r)
    if lad:
        rows.append(('支撐梯級', '｜'.join(f"{lab} {p(x, 0)}（-{d:.1f}%）" for lab, x, d in lad[:4]), ''))
    if isval(r.get('Supply_Soft_Level')):
        rows.append(('軟阻力', f"{p(r['Supply_Soft_Level'])}（{r.get('Supply_Soft_Source')}，"
                                f"{fx(r.get('Room_To_Soft_R'), 2)}R）", ''))
    return '\n'.join(f'| {a} | {b} | {c} |' for a, b, c in rows)


def render(v, r, st):
    """The report. Every price comes from L2_Input; every sentence comes from the story file."""
    d = r.get('Date', '')
    comp = v.get('company', '')
    head = f"📌 {r['Ticker']}" + (f" {comp}" if isval(comp) and str(comp).upper() != str(r['Ticker']).upper() else '') + " --- 投資快報"
    st = st or {}
    global _CUR
    _CUR = 'HK$' if str(r.get('Market')) == 'HK' else '$'
    L = [BAR, head, f"分析日：{d} ｜ 敘事日：{st.get('story_date', '—')} ｜ "
                    f"市場：{r.get('Market') if isval(r.get('Market')) else 'US'}"]
    if str(r.get('Market')) == 'HK':
        # v6.8: fixed text, no detection and no arithmetic (user decision)
        L.append('註：平安夜、除夕、農曆年前夕為半日市，當日成交量偏低，量能判斷請自行留意。')
    L += [BAR,
         '🎯 核心故事',
         f"市場主線：{st.get('market_line', '—')}（{st.get('route_tag', '—')}）",
         f"主線（{st.get('story_main_score', '—')}/10）：{st.get('story_main', '敘事待查，主要基於技術面')}"]
    if isval(st.get('why_now')):
        L.append(f"　Why Now：{st['why_now']}")
    if isval(st.get('moat')):
        L.append(f"　護城河：{st['moat']}")
    nums = st.get('numbers') or []
    if nums:
        L.append('　數字驗證：' + '；'.join(f"{x.get('text', '')}（{x.get('date', '')}）" for x in nums))
    L += [f"次線（{st.get('story_sub_score', '—')}/10）：{st.get('story_sub', '—')}",
          f"敘事信念：{st.get('conviction', '—')}｜{st.get('conviction_why', '—')}",
          SEP, '📊 技術狀態', f"現價 {p(r.get('Close'))}", '| 項目 | 數值 | 備註 |', '|---|---|---|',
          tech_table(r), SEP, '⚠️ 技術風險（由 L1 提供，不可改寫）']
    tech = [x.strip() for x in str(r.get('Speak_Up', '')).split(';') if x.strip() and isval(r.get('Speak_Up'))]
    L += [f'{i}. {x}' for i, x in enumerate(tech, 1)] or ['—']
    L += [SEP, '🧭 故事／基本面風險（由 L2 提供）']
    L += [f'{i}. {x}' for i, x in enumerate(st.get('risks', []), 1)] or ['—']

    # ---- execution ----
    ef, verdict = r.get('Entry_Feasible'), v['verdict']
    fam = str(r.get('Setup_Family'))
    lad = ladder(r)
    L += [SEP, '🎬 執行劇本',
          f"建議：{VERDICT_ZH[v['verdict']]}｜基準 {v.get('baseline')}｜質素 {r.get('Setup_Quality_Grade')}"
          f"｜排名 {v.get('rank', '—')}"
          + (f"｜降級：{v.get('baseline')}→{v['verdict']}（{v.get('downgrade_reason')}）"
             if isval(v.get('downgrade_reason')) and v.get('baseline') != v['verdict'] else '')]

    if verdict in ('WATCH', 'AVOID'):
        # B5: a verdict that says "do not act" must not carry a price to act on.
        why = str(v.get('downgrade_reason') or r.get('Tradeable_Why') or r.get('Risk_Why') or '')[:90]
        L.append('**暫不掛單**（未達可交易風險或未觸發）')
        L.append(f"要等：{supply_text(r)}" if np.isfinite(n(r.get('Supply_Level'))) else '要等：結構成立')
        L.append(f"原因：{why or '未達門檻'}")
        if fam in ('PULLBACK', 'REVERSAL') and lad:
            L.append(f"參考支撐：{' / '.join(f'{x[0]} {p(x[1], 1)}' for x in lad[:2])}")
    else:
        L.append('進場：')
        if ef == 'NOT_YET':
            L += [f"- ① buy-stop：{p(r.get('Trigger_Price'))}（收市或盤中突破平台高）",
                  f"- 條件：成交量 ≥ {p(r.get('Trigger_Min_Vol'), 0, '')} 股；成交當日低需高於 "
                  f"{p(r.get('BuyStop_Max_Stop'))}，否則放棄"]
        else:
            L.append(f"- ① {r.get('Entry_Src') or 'entry'}：{p(r.get('Entry_Ref'))}"
                     + ('' if verdict == 'BUY' else '（暫不建議）'))
            if fam in ('PULLBACK', 'REVERSAL') and len(lad) >= 2:
                two = lad[:2]
                L.append(f"- ② 回調參考：{p(two[-1][1], 1)}–{p(two[0][1], 1)}"
                         f"（{' / '.join(x[0] for x in two)}）")
            elif fam in ('PULLBACK', 'REVERSAL') and len(lad) == 1:
                L.append(f"- ② 回調參考：{p(lad[0][1], 1)}（{lad[0][0]}）")
        L.append(f"止損：突破日低（成交後確定）｜平台失效位 {p(r.get('Invalidate_Below'))}"
                 if ef == 'NOT_YET' else
                 f"止損：{p(r.get('Invalidate_Below'))}（{r.get('Stop_Type_Plan', '')}）")
        stop_px = n(r.get('Invalidate_Below'))
        below = [x for x in lad if np.isfinite(stop_px) and x[1] < stop_px]
        if below:
            L.append(f"止損備援（不改主止損）：{' / '.join(f'{x[0]} {p(x[1], 1)}' for x in below[:2])}")
        shares = n(r.get('Shares_per_1000_Risk'))
        tail = (f"｜每 $1,000 風險 ≈ {p(shares, 0, '')} 股" if np.isfinite(shares)
                else '｜股數待成交後計算（止損未定）')
        L += [f"風險：{fx(r.get('Risk_Pct_Plan'), 1)}%（{fx(r.get('Risk_ADR_Plan'), 2)}×ADR）" + tail,
              f"空間：{supply_text(r)}（v5 不設目標價）",
              '管理：收市跌穿止損即走｜收市跌穿 MA10 減半｜+2R 後止損移至成本']

    L += [SEP, '🧨 無效與紀律（≤100字）', str(v.get('invalidation', '—')),
          SEP, '💬 一句講晒（≤60字，粵語）', f"「{v.get('closer', '')}」", f"情緒標籤：{v.get('emotion')}"]

    srcs = (st.get('sources') or [])[:5]
    if srcs:
        L += [SEP, '📚 搜尋來源']
        for x in srcs:
            stale = ' ⚠️ 資訊可能過時' if x.get('stale') else ''
            L.append(f"- {x.get('title', '')} · {x.get('date', '')} · {x.get('url', '')}{stale}")
    L += ['☐ 人工看圖：形態鬆散 / 跳空缺口（L1 看不到）', BAR, '此分析僅供參考，不構成投資建議。']
    return '\n'.join(L)


def image_pack(v, r, st):
    """Paste-ready data block in Justin's GPT-Image-2 shape (2026-11-07).

    No prompt scaffolding: GPT Image 2 reads the block directly. Every value is pulled from
    L2_Input/Contract; a missing value drops its line rather than printing a placeholder.
    """
    st = st or {}
    tick = r['Ticker']
    verdict = v['verdict']

    def val(x, nd=2):
        y = n(x)
        return fx(x, nd) if np.isfinite(y) else ''

    lines = [f"股票：{tick} US"]
    theme = st.get('market_line') if isval(st.get('market_line')) else ''
    if theme:
        lines.append(f"行業／主題：{theme}")
    title = v.get('title') or tick
    hook = str(st.get('why_now') or '').strip()
    hook = hook.split('；')[0] if hook else ''
    if len(hook) > 26:
        cut = hook[:26]
        for sep in ('）', '，', '、', ' '):
            i = cut.rfind(sep)
            if i >= 14:
                cut = cut[:i + 1]
                break
        hook = cut.rstrip('，、')
    lines.append(f"標題：{title}" + (f" -- {hook}" if hook else ''))

    lines += ["主題故事："]
    main = str(st.get('why_now') or st.get('story_main') or '').strip()
    if main:
        lines.append(f"- 主線：{main}")
    if isval(v.get('finance_line')):
        lines.append(f"- 數字：{v['finance_line']}")
    if isval(v.get('driver_line')):
        lines.append(f"- 驅動力：{v['driver_line']}")

    flag = r.get('Earnings_Proximity_Flag')
    days = val(r.get('Days_To_Earnings'), 0)
    if isval(flag):
        tail = f"約 {days} 天後" if days else (str(r.get('Earnings_Date', '')) if isval(r.get('Earnings_Date')) else '')
        lines.append(f"時間線：財報 {flag}" + (f"（{tail}）" if tail else ''))

    lines += ["關鍵維度："]
    if np.isfinite(n(r.get('RS_Score'))):
        role = str(r.get('RS_Role') or '').strip()
        role = '' if role.lower() in ('nan', 'none', 'na') else role
        lines.append(f"- RS Score：{val(r.get('RS_Score'), 1)}" + (f"（{role}）" if role else ''))
    grade = str(r.get('Setup_Quality_Grade') or '').strip()
    if grade:
        q = val(r.get('Setup_Quality'), 1)
        lines.append(f"- 質素：{grade}" + (f"（quality {q}/5）" if q else ''))
    mt, ms2 = str(r.get('Minervini_Trend', '')).strip(), str(r.get('Minervini_Stage2', '')).strip()
    if mt or ms2:
        lines.append(f"- 趨勢：Minervini Trend={mt or '—'}，Stage2_Strict={ms2 or '—'}")
    vp = r.get('Vol_Ratio_Pullback') if isval(r.get('Vol_Ratio_Pullback')) else r.get('Trigger_Vol_Ratio')
    if np.isfinite(n(vp)):
        word = '收縮' if n(vp) < 1 else '放大'
        conf = str(r.get('Volume_Confirm') or '').strip()
        conf = '' if conf in ('NOT_APPL', 'nan', '') else f"（{conf}）"
        lines.append(f"- 成交量：{val(vp, 2)}x ➡️ {word}{conf}")
    elif np.isfinite(n(r.get('Base_Vol_Decay'))):
        lines.append(f"- 成交量：基石量能衰減 {val(r.get('Base_Vol_Decay'), 2)}x（突破日需 ≥{int(n(r.get('Trigger_Min_Vol'))):,} 股）")
    rp, radr = val(r.get('Risk_Pct_Plan'), 1), val(r.get('Risk_ADR_Plan'), 2)
    close = val(r.get('Close'), 2)
    if rp:
        mark = '✅ 可控' if str(r.get('Risk_OK', '')).upper() == 'PASS' and n(r.get('Risk_ADR_Plan')) <= 1.2 else '⚠️ 偏闊'
        lines.append(f"- Risk%：@{close} ≈{rp}%（{radr}×ADR）{mark}" if radr else f"- Risk%：@{close} ≈{rp}% {mark}")

    # v5.5.3 scoring: three gates + Priority/65 + quality grade/score (no star bands, no targets)
    gates = [f"{lbl} {str(r.get(k, '')).upper() or '—'}"
             for lbl, k in (("Leader", 'Leader_OK'), ("Setup", 'Setup_OK'), ("Risk", 'Risk_OK'))]
    if any(g.split()[1] != '—' for g in gates):
        lines.append("三閘：" + " · ".join(gates))
    lines += ["操作劇本："]
    fam = f"{r.get('Setup_Family', '')}／{r.get('Setup_Code', '')}".strip('／')
    feas = str(r.get('Entry_Feasible', ''))
    if verdict in ('WATCH', 'AVOID'):
        sup = val(r.get('Supply_Level'), 2)
        lines.append(f"建議：{verdict} | {fam}（唔掛單）")
        lines.append(f"入場：暫不掛單" + (f"（要等 ${sup} 突破／結構確認）" if sup else ''))
        lines.append("止損：未設（無持倉）")
        tail = []
        room = val(r.get('Room_To_Supply_R'), 2)
        if room:
            tail.append(f"硬 {room}R 至 ${sup}（{r.get('Supply_Source', '')}）")
        prio = val(r.get('Priority_Score'), 0)
        if prio:
            tail.append(f"Priority {prio}/65")
        if tail:
            lines.append("空間：" + "｜".join(tail))
        closer = str(v.get('closer') or '').strip()
        if closer:
            lines += ["一句講晒：", f"「{closer}」"]
        return "\n".join(lines)
    if verdict == 'STALK' or feas == 'NOT_YET':
        entry = f"${val(r.get('Trigger_Price'), 2)} buy-stop（突破觸發，未成交）"
        stop = "突破日低位（成交後才設定）"
    else:
        entry = f"${val(r.get('Entry_Ref'), 2)}（{r.get('Entry_Src', 'at market')}）"
        stop = f"${val(r.get('Invalidate_Below'), 2)}（{r.get('Stop_Type_Plan', '')}）"
    lines.append(f"建議：{verdict} | {fam}" + ("（等觸發，唔追現價）" if verdict == 'STALK' else ''))
    lines.append(f"入場：{entry}")
    lines.append(f"止損：{stop}")
    room = val(r.get('Room_To_Supply_R'), 2)
    prio = val(r.get('Priority_Score'), 0)
    tail = []
    if room:
        tail.append(f"硬 {room}R 至 ${val(r.get('Supply_Level'), 2)}（{r.get('Supply_Source', '')}）")
    soft = val(r.get('Room_To_Soft_R'), 2)
    if soft:
        tail.append(f"軟 {soft}R 至 ${val(r.get('Supply_Soft_Level'), 2)}（{r.get('Supply_Soft_Source', '')}）")
    if prio:
        tail.append(f"Priority {prio}/65")
    if tail:
        lines.append("空間：" + "｜".join(tail))

    closer = str(v.get('closer') or '').strip()
    if closer:
        lines += ["一句講晒：", f"「{closer}」"]
    return "\n".join(lines)


def _pos_rows(folder, c):
    """Open positions from positions.csv (optional). R = (Close - entry) / (entry - stop)."""
    path = os.path.join(folder, 'positions.csv')
    if not os.path.exists(path):
        return []
    pos = pd.read_csv(path, **KEEP_NA)
    out = []
    for _, q in pos.iterrows():
        t = str(q.get('ticker', '')).strip().upper()
        if not t:
            continue
        entry, stop = n(q.get('entry_price')), n(q.get('stop'))
        close = n(c.loc[t, 'Close']) if t in c.index else np.nan
        R = (close - entry) / (entry - stop) if (np.isfinite(close) and np.isfinite(entry)
                                                 and np.isfinite(stop) and entry > stop) else np.nan
        out.append((t, q.get('entry_date', '—'), entry, stop, q.get('shares', '—'), close, R))
    return out


def final_map(vs):
    """Ticker -> the verdict layer 2 actually output. Missing names fall back to baseline."""
    return {v.get('ticker'): v.get('verdict') for v in vs
            if v.get('verdict') and v.get('verdict') != 'NO_TRADE'}


def why_map(vs):
    return {v.get('ticker'): v.get('downgrade_reason') for v in vs if v.get('ticker')}


def cover(folder, c, vs, rendered):
    """index.md — the one page Hermes sends: what changed, what to hang, what to watch."""
    date = str(c['Date'].iloc[0]) if len(c) else ''
    regime = (f"{c.get('Regime_Label', pd.Series([''])).iloc[0]} / {c.get('Regime_State', pd.Series([''])).iloc[0]}"
              f" · 指數 {c.get('Index_Regime_State', pd.Series([''])).iloc[0]}"
              f" · %>50D {c.get('Breadth_50D', pd.Series([''])).iloc[0]}") if len(c) else ''
    fmap, wmap = final_map(vs), why_map(vs)
    c = c.copy()
    c['Final_Verdict'] = [fmap.get(t, b) for t, b in zip(c['Ticker'], c['Baseline_Verdict'])]
    base = c['Final_Verdict'].value_counts().to_dict()
    L = [BAR, f'📌 每日交易簿 — {date}', f'市場：{regime}', BAR,
         '## ① 今日概況',
         f"- BUY {base.get('BUY', 0)} · STALK {base.get('STALK', 0)} · WATCH {base.get('WATCH', 0)} · AVOID {base.get('AVOID', 0)}",
         f"- 已出報告：{len(rendered)} 檔（見 ⑥）", '']

    ch = c[c['Change_vs_Prev'].fillna('UNCHANGED').isin(['NEW', 'TRIGGERED', 'UPGRADED', 'DOWNGRADED', 'INVALIDATED'])]
    L += ['## ② 今日變化']
    if len(ch):
        L += ['| 檔 | 變化 | 基準 | Setup | 備註 |', '|---|---|---|---|---|']
        for _, r in ch.iterrows():
            why = next((x for x in (r.get('Baseline_Why'), r.get('Risk_Why'), r.get('Speak_Up')) if isval(x)), '')
            L.append(f"| {r['Ticker']} | {r['Change_vs_Prev']} | {r['Final_Verdict']} | "
                     f"{r.get('Setup_Family')}/{r.get('Setup_Code')} | {str(why)[:70]} |")
    else:
        L.append('- 無（全部 UNCHANGED 或首次執行）')
    L.append('')

    L += ['## ③ STALK 掛單（未觸發）']
    st = c[(c['Final_Verdict'] == 'STALK') & (c['Entry_Feasible'] == 'NOT_YET')]
    if len(st):
        L += ['| 檔 | 觸發價 | 最低量 | 停損上限 | 平台失效 | 質素 |', '|---|---|---|---|---|---|']
        for _, r in st.iterrows():
            L.append(f"| {r['Ticker']} | {p(r.get('Trigger_Price'))} | {p(r.get('Trigger_Min_Vol'), 0, '')} | "
                     f"{p(r.get('BuyStop_Max_Stop'))} | {p(r.get('Invalidate_Below'))} | {r.get('Setup_Quality_Grade')} |")
    else:
        L.append('- 今日沒有待觸發的掛單')
    L.append('')

    down = c[(c['Final_Verdict'] != c['Baseline_Verdict'])]
    if len(down):
        L += ['## ③b 已降級（不再行動）']
        for _, r in down.iterrows():
            why = wmap.get(r['Ticker']) or r.get('Baseline_Why') or r.get('Risk_Why') or ''
            L.append(f"- {r['Ticker']}：{r['Baseline_Verdict']} → **{r['Final_Verdict']}**（{str(why)[:70]}）")
        L.append('')
    L += ['## ④ 觀察清單（WATCH）']
    wt = c[c['Final_Verdict'] == 'WATCH'].sort_values('Room_To_Supply_R', ascending=False)
    if len(wt):
        L += ['| 檔 | Setup | 為何仍是 WATCH |', '|---|---|---|']
        for _, r in wt.head(12).iterrows():
            why = next((x for x in (r.get('Risk_Why'), r.get('Baseline_Why'), r.get('Speak_Up')) if isval(x)), '')[:80]
            L.append(f"| {r['Ticker']} | {r.get('Setup_Family')}/{r.get('Setup_Code')} | {why} |")
        if len(wt) > 12:
            L.append(f'| … | | 另有 {len(wt) - 12} 檔 |')
    else:
        L.append('- 無')
    L.append('')

    pos = _pos_rows(folder, c)
    L += ['## ⑤ 持倉（來自 positions.csv）']
    if pos:
        L += ['| 檔 | 進場日 | 進場 | 止損 | 股數 | 現價 | R |', '|---|---|---|---|---|---|---|']
        for t, d0, e, s0, sh, cl, R in pos:
            L.append(f"| {t} | {d0} | {p(e)} | {p(s0)} | {sh} | {p(cl)} | {fx(R, 2)} |")
    else:
        L.append('- 未有 positions.csv（略過）')
    L.append('')

    L += ['## ⑥ 個股報告', '']
    L += [f'- {x}' for x in rendered] or ['- 今日沒有可發送的報告']
    L += ['', BAR, '此分析僅供參考，不構成投資建議。']
    return '\n'.join(L)


def main(folder, only=None):
    c = pd.read_csv(os.path.join(folder, 'L2_Input.csv'), **KEEP_NA).set_index('Ticker', drop=False)
    vpath = os.path.join(folder, 'verdicts_US.jsonl')   # v6.9
    vs = [json.loads(l) for l in open(vpath, encoding='utf-8') if l.strip()] if os.path.exists(vpath) else []
    out = os.path.join(folder, 'reports')
    os.makedirs(out, exist_ok=True)
    rendered, skipped = [], []
    for v in vs:
        if v.get('verdict') == 'NO_TRADE':
            continue
        t = v.get('ticker')
        if only and t not in only:
            continue
        if t not in c.index:
            skipped.append(f'❌ {t}: ticker not in the contract')
            continue
        r = c.loc[t]
        sp = os.path.join(folder, 'stories', f'{t}_story.json')
        st = json.load(open(sp, encoding='utf-8')) if os.path.exists(sp) else None
        open(os.path.join(out, f'{t}_投資快報.md'), 'w', encoding='utf-8').write(render(v, r, st) + '\n')
        open(os.path.join(out, f'{t}_image_pack.md'), 'w', encoding='utf-8').write(image_pack(v, r, st) + '\n')
        card = os.path.exists(os.path.join(out, f'{t}_card.png'))
        mark = {'BUY': '✅', 'STALK': '✅', 'WATCH': '👁', 'AVOID': '⛔'}.get(v['verdict'], '•')
        rendered.append(f"{mark} {t} · {v['verdict']} · 質素 {r.get('Setup_Quality_Grade')}"
                        f" → `{t}_投資快報.md`" + ('' if card else '（🖼️ 待人手生成）'))
    page = cover(folder, c, vs, rendered + skipped)
    open(os.path.join(out, 'index.md'), 'w', encoding='utf-8').write(page + '\n')
    print(page)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '.', set(sys.argv[2:]) or None))
