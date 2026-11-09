#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Layer-2 invariants (v5.5). Checks verdicts_<market>.jsonl against L2_Input.csv.

Usage:  python3 check_verdict.py <run_folder>
Exit:   0 all PASS · 2 any FAIL (the bot must NOT send the trade book; it sends this report instead)

V1 no upgrade: verdict <= Baseline_Verdict
V2 prices copied: entry / stop equal the contract within 0.01
V3 cited_fields exist in the contract
V4 BUY only when Risk_OK=PASS, earnings not PASS/UNKNOWN, Entry_Feasible actionable
V5 one line per ticker, <= MAX_BUYS BUY, NO_TRADE alone and with a valid reason
V6 every downgrade has a reason that names a contract field (or STORY_RISK with a source URL)
V7 STORY_RISK downgrade only BUY->STALK, only with conviction=CHALLENGE and a dated source
V8 every BUY/STALK in the baseline appears in the output (nothing silently dropped)
V9 the prose fields obey their rules (length, emotion tag, no retired terms, risks are
   story/fundamental only: no technical field, no contract price restated)
V10 when l2_status.json is not OK, the only legal output is one NO_TRADE line with that reason
V11 conviction is one of CONFIRM / CHALLENGE / NEUTRAL
V12 every sources[].url appears in the story's search_log hits
V13 every numbers[] item has a url + date, and that url is in the search log
V14 BUY/STALK with CONFIRM/CHALLENGE needs >= 2 sources and a conviction_why that cites one
V15 no simplified-Chinese characters in the story text
V16 Earnings UNKNOWN needs an earnings_check (date + url, or the words 未能確認)
V17 story field lengths (story_main<=200, why_now<=60, story_sub<=120, risks<=4)
Conviction in verdicts must equal the story file (spec v5.5.2 §3).
"""
import json
import markets
import os
import re
import sys

import pandas as pd

RANK = {'AVOID': 0, 'WATCH': 1, 'STALK': 2, 'BUY': 3}
EMO = {'BUY': ('🚀火箭升空', '✅穩陣上車'), 'STALK': ('⚡觀望等位',), 'WATCH': ('⚡觀望等位',),
       'AVOID': ('❌敬而遠之', '⚠️刀口舔血')}
LIMITS = {'closer': 50, 'invalidation': 100}   # story_main is a story.json field (V17: <=200)
BANNED_RE = re.compile(r'(目標價|目標\s*\$?\d|Target\s*(?:Price|:\s*\$?\d)|\bT[123]\b|\bRR\b)')
# A5: quoting a broker's own target is evidence, not an invented target price. The ban is on
# the system making one up, so a hit preceded by an attributable source is allowed.
ATTRIB_RE = re.compile(r'(分析師|共識|券商|賣方|機構|投行|大行|目標價\s*來源)')
# 目標價 / 目標 480 / Target Price / T1-T3 / RR — but not ARR, and not the business word 目標
CONVICTIONS = {'CONFIRM', 'CHALLENGE', 'NEUTRAL'}
# a price-like token: has a decimal, or is a 3+ digit integer (400), never part of an id
PRICE_TOKEN = re.compile(r'(?<![A-Za-z0-9._/-])(\d[\d,]*\.\d+|\d{2,})(?!\d)')
PRICE_UNIT = re.compile(r'\s*(?:%|％|家|次|億|萬|元|年|月|日|倍|季|個|隻|檔|點|天|週|周|股|蚊|手|厘|仙)')
STORY_LIMITS = {'story_main': 200, 'why_now': 60, 'story_sub': 120}
# common simplified forms that must never appear in Traditional-Chinese copy
SIMPLIFIED = set('压们这为说时实发经业产资价场级报应与关门东个国会学习对开关头长见样还进运动产')
STORY_TEXT = ('story_main', 'why_now', 'moat', 'story_sub', 'conviction_why', 'market_line')
# A3: L2 may write story / fundamental risks only — never restate a technical number
TECH_RE = re.compile(r'(RSI|Ext(?:ension)?[_ ]?MA|\bADR\b|×\s*ADR|x\s*ADR|量比|volume\s*ratio|'
                     r'\bMA\d+\b|BuyStop|Invalidate|止損|停損|\bstop\b|\d+(\.\d+)?\s*R\b)', re.I)
MAX_BUYS = int(os.environ.get('SWING_MAX_BUYS', '3'))
NO_TRADE_REASONS = {'NO_SETUP', 'ALL_DOWNGRADED', 'RUN_FAILED', 'DATA_STALE'}
KEEP_NA = dict(keep_default_na=False, na_values=[''])


def load_json(path):
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)
    except Exception:
        return None


def log_urls(folder, t):
    d = load_json(os.path.join(folder, 'stories', f'{t}_search_log.json')) or {}
    out = set()
    for q in d.get('queries', []):
        for h in q.get('hits', []):
            if h.get('url'):
                out.add(h['url'])
    return out


def zlen(text):
    """Claude's counter: whitespace and punctuation are free; tickers and digits count 1 each."""
    import unicodedata
    return sum(1 for ch in str(text) if not unicodedata.category(ch).startswith(('Z', 'P')))


def f(x):
    try:
        return float(x)
    except Exception:
        return float('nan')


def main(folder):
    c = pd.read_csv(os.path.join(folder, 'L2_Input.csv'), **KEEP_NA).set_index('Ticker')
    path = markets.verdicts_path(folder)   # v6.9: verdicts_<market>.jsonl
    if not os.path.exists(path):
        print(f'FAIL  no {os.path.basename(markets.verdicts_path(folder))} in {folder} — layer 2 has not run yet')
        return 2
    rows, res = [], []
    with open(path, encoding='utf-8') as fh:
        for n, line in enumerate(fh, 1):
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as e:
                    res.append(('V0', 'FAIL', f'line {n} is not JSON: {e}'))

    def add(cid, ok, detail):
        res.append((cid, 'PASS' if ok else 'FAIL', detail))

    # ---- V10: a failed/prep-status run may only produce one NO_TRADE line ----
    st_path = os.path.join(folder, 'l2_status.json')
    status = {}
    if os.path.exists(st_path):
        try:
            status = json.load(open(st_path, encoding='utf-8'))
        except Exception:
            status = {}
    run_status = str(status.get('status', 'OK'))
    if run_status not in ('OK', ''):
        ok = (len(rows) == 1 and rows[0].get('verdict') == 'NO_TRADE'
              and rows[0].get('reason') == run_status)
        add('V10', ok, f"status={run_status} lines={len(rows)} "
                       f"reason={rows[0].get('reason') if rows else None}")

    # ---- V1b/V1c: baseline must be what l2_prep would compute, from an untouched contract ----
    flags = status.get('flags', {}) if isinstance(status, dict) else {}
    hashes = status.get('sha256', {}) if isinstance(status, dict) else {}
    if run_status in ('OK', ''):
        try:
            import l2_prep as _lp
            _lp.INDEX_20EMA_RULE = bool(flags.get('SWING_INDEX_20EMA_RULE', False))
            _lp.WEAK_BUY_RULE = bool(flags.get('SWING_WEAK_BUY_RULE', False))
            con_path = os.path.join(folder, 'Contract_US.csv')
            con = pd.read_csv(con_path, **KEEP_NA)
            rec = _lp.compute_baseline(con).set_index('Ticker')['Baseline_Verdict']
            mis = [(t, c.loc[t, 'Baseline_Verdict'], rec.get(t)) for t in c.index
                   if rec.get(t) is not None and rec.get(t) != c.loc[t, 'Baseline_Verdict']]
            add('V1b', not mis, f'baseline recomputed from contract: {len(mis)} mismatches {mis[:3]}')
            bad_h = []
            for name, want in hashes.items():
                fp = os.path.join(folder, name)
                if not os.path.exists(fp):
                    bad_h.append(f'{name} missing')
                elif _lp.sha256_of(fp) != want:
                    bad_h.append(f'{name} changed')
            add('V1c', not bad_h, f'file hashes: {bad_h or "contract and L2_Input unchanged"}')
        except Exception as exc:
            add('V1b', False, f'baseline recompute failed: {str(exc)[:90]}')

    # v6.4 (#5): every ticker in this run is a code, not a price
    # Only unambiguous code forms are stripped: a zero-padded 4-digit code (0700) or anything
    # carrying .HK. A bare 388 must stay in the text — it could be a fabricated price.
    CODE_TOKENS = {str(t_).split('.')[0] for t_ in c.index if str(t_)[:1] == '0'}
    CODE_TOKENS |= {'2800', '0700', 'HSI'}

    nt = [r for r in rows if r.get('verdict') == 'NO_TRADE']
    names = [r for r in rows if r.get('verdict') != 'NO_TRADE']
    if nt:
        add('V5', len(rows) == 1 and nt[0].get('reason') in NO_TRADE_REASONS,
            f"NO_TRADE reason={nt[0].get('reason')}, lines={len(rows)}")
        if nt[0].get('reason') == 'NO_SETUP':
            missed = c.index[c['Baseline_Verdict'].isin(['BUY', 'STALK'])].tolist()
            add('V8', not missed, f'NO_SETUP but baseline has BUY/STALK: {missed}' if missed else 'consistent')
    else:
        tick = [r.get('ticker') for r in names]
        dup = sorted({t for t in tick if tick.count(t) > 1})
        nbuy = sum(r.get('verdict') == 'BUY' for r in names)
        add('V5', not dup and nbuy <= MAX_BUYS, f'dups={dup} BUY={nbuy} (max {MAX_BUYS})')
        need = set(c.index[c['Baseline_Verdict'].isin(['BUY', 'STALK'])])
        missing = sorted(need - set(tick))
        add('V8', not missing, f'missing from output: {missing}' if missing else f'{len(need)} baseline BUY/STALK covered')

    for r in names:
        t, v = r.get('ticker'), r.get('verdict')
        if t not in c.index:
            add('V0', False, f'{t}: ticker not in contract')
            continue
        k = c.loc[t]
        base = k['Baseline_Verdict']
        if v not in RANK:
            add('V1', False, f'{t}: verdict {v} invalid')
            continue
        add('V1', RANK[v] <= RANK[base], f'{t}: {v} vs baseline {base}')
        want_entry = f(k['Trigger_Price']) if k.get('Entry_Feasible') == 'NOT_YET' else f(k['Entry_Ref'])
        for key, want in (('entry', want_entry), ('stop', f(k['Invalidate_Below']))):
            got = f(r.get(key))
            if want == want:   # not NaN
                add('V2', abs(got - want) <= 0.01, f'{t}: {key} {got} vs contract {want}')
        bad = [x for x in r.get('cited_fields', []) if x not in c.columns]
        add('V3', not bad and len(r.get('cited_fields', [])) > 0, f'{t}: cited {r.get("cited_fields")} unknown={bad}')
        if v == 'BUY':
            ok = (k['Risk_OK'] == 'PASS' and k['Earnings_Proximity_Flag'] not in ('PASS', 'UNKNOWN')
                  and k['Entry_Feasible'] not in ('NOT_YET', 'INVALIDATED', 'MISSED'))
            add('V4', ok, f"{t}: Risk_OK={k['Risk_OK']} earnings={k['Earnings_Proximity_Flag']} EF={k['Entry_Feasible']}")
        if v == 'STALK':
            # v6.1 (C6): C_WATCH + NOT_YET used to become STALK even when Risk_OK was FAIL.
            ok = str(k['Risk_OK']) in ('PENDING', 'PASS')
            add('V4c', ok, f"{t}: STALK with Risk_OK={k['Risk_OK']} EF={k['Entry_Feasible']}")
        if v in ('BUY', 'STALK'):
            # v6.10 (ported from US v5.5.4): a ticket must carry Tradeable=PASS. Risk_OK alone
            # let a 2.72xADR pending breakout through as a STALK (2269.HK, 2026-11-07).
            if 'Tradeable' in c.columns:
                ok = str(k['Tradeable']).upper() == 'PASS'
                add('V4d', ok, f"{t}: {v} with Tradeable={k['Tradeable']}")
        if k['Earnings_Proximity_Flag'] == 'PASS' and v in ('BUY', 'STALK'):
            # A1: a buy-stop on the earnings day is the same mistake as a BUY.
            # WATCH/AVOID carry no order, so they are not blocked here.
            add('V4b', False, f'{t}: earnings PASS cannot carry a ticket ({v})')
        # ---- V11: conviction vocabulary (Grok must end every report with one) ----
        add('V11', r.get('conviction') in CONVICTIONS,
            f"{t}: conviction={r.get('conviction')}")

        # ---- V12-V17: the story file (spec v5.5.2 §4) ----
        story = load_json(os.path.join(folder, 'stories', f'{t}_story.json'))
        if story is None:
            need = set(c.index[c['Baseline_Verdict'].isin(['BUY', 'STALK'])])
            if t in need:
                add('V12', False, f'{t}: no stories/{t}_story.json but the baseline is BUY/STALK')
        else:
            urls = log_urls(folder, t)
            srcs = story.get('sources') or []
            bad_src = [x.get('url') for x in srcs if x.get('url') not in urls]
            add('V12', not bad_src, f'{t}: {len(srcs)} sources, not in search log: {bad_src or "none"}')

            nums = story.get('numbers') or []
            bad_num = [x.get('text') for x in nums
                       if not x.get('url') or not x.get('date') or x.get('url') not in urls]
            add('V13', not bad_num, f'{t}: {len(nums)} numbers, bad: {bad_num or "none"}')

            conv = story.get('conviction')
            add('V11b', conv == r.get('conviction'),
                f'{t}: verdicts {r.get("conviction")} vs story {conv}')
            n_src = len(srcs)
            cited = False
            why = str(story.get('conviction_why', '')).lower()
            for x in srcs:
                title = str(x.get('title', ''))
                dom = re.sub(r'^https?://(www\.)?', '', str(x.get('url', ''))).split('/')[0].lower()
                if (x.get('url') and x['url'] in why) or (dom and dom in why) \
                        or (len(title) > 12 and title[:12].lower() in why):
                    cited = True
                    break
            if v in ('BUY', 'STALK') and conv in ('CONFIRM', 'CHALLENGE'):
                add('V14', n_src >= 2 and cited,
                    f'{t}: sources={n_src} conviction_why_cites={cited}')
            else:
                add('V14', True, f'{t}: not applicable ({v}/{conv})')

            blob = ' '.join(str(story.get(k, '')) for k in STORY_TEXT)
            blob += ' '.join(map(str, story.get('risks', []))) + str(story.get('moat', ''))
            simp = sorted({ch for ch in blob if ch in SIMPLIFIED})
            add('V15', not simp, f'{t}: simplified chars {simp or "none"}')

            if str(k.get('Earnings_Proximity_Flag')) == 'UNKNOWN':
                ec = story.get('earnings_check') or {}
                ok = (isinstance(ec, dict) and ec.get('url') and ec.get('date')) or '未能確認' in str(ec)
                add('V16', bool(ok), f'{t}: earnings UNKNOWN, earnings_check={ec}')
            else:
                add('V16', True, f'{t}: earnings {k.get("Earnings_Proximity_Flag")} (not UNKNOWN)')

            errs17 = [f'{fld}={len(str(story.get(fld, "")))}>{lim}'
                      for fld, lim in STORY_LIMITS.items() if len(str(story.get(fld, ''))) > lim]
            if len(story.get('risks', [])) > 4:
                errs17.append(f'risks={len(story["risks"])}>4')
            add('V17', not errs17, f'{t}: ' + ('; '.join(errs17) if errs17 else 'lengths ok'))

        # ---- V9: prose rules (lengths, emotion, retired terms, risks are not technical) ----
        errs = []
        for fld, lim in LIMITS.items():
            if zlen(r.get(fld, '')) > lim:
                errs.append(f'{fld}={zlen(r.get(fld, ""))}>{lim}')
        if r.get('emotion') not in EMO.get(v, ()):
            errs.append(f'emotion {r.get("emotion")} not allowed for {v}')
        text = str(r.get('closer', '')) + str(r.get('invalidation', ''))
        if story:
            # market_line carries KB trend codes (T1..T15); a target would appear in prose
            text += ' '.join(str(story.get(x, '')) for x in STORY_TEXT if x != 'market_line')
            text += ''.join(map(str, story.get('risks', [])))
            text += ' '.join(str(x.get('text', '')) for x in (story.get('numbers') or []))
        for hit in BANNED_RE.finditer(text):
            if ATTRIB_RE.search(text[max(0, hit.start() - 10):hit.start()]):
                continue                      # e.g. 分析師平均目標 65.50 — a citation
            errs.append(f'retired term {hit.group(0)!r}')
            break
        # v6.2 (C4/V2 + Grok #2): every price-like number in the prose must exist in this
        # ticker's contract. Tolerance is tight (0.02% or 1 cent) because MA levels cluster
        # around price — a 0.5% window let 47.65 pass by matching MA10 at 47.677.
        allowed_px = []
        for col in ('Entry_Ref', 'Invalidate_Below', 'Trigger_Price', 'BuyStop_Max_Stop',
                    'Supply_Level', 'Supply_Soft_Level', 'Close', 'MA10', 'MA20', 'MA50',
                    'POC_60D', 'VAL_60D', 'SR_Flip_Level'):
            if col in k.index:
                x = f(k.get(col))
                if x == x:
                    allowed_px.append(x)
        prose = str(r.get('closer', '')) + ' ' + str(r.get('invalidation', ''))
        # v6.4 (#5): a bare code (2800, 0700, 6160) is not a price. Codes come from the
        # universe itself, so they are stripped before the scan instead of being whitelisted.
        prose = re.sub(r'(?<![0-9])\d{4}\.HK', ' ', prose)          # 6862.HK is a code
        for code in CODE_TOKENS:
            prose = re.sub(rf'(?<![0-9]){code}(?![0-9])', ' ', prose)  # 0700 / 2800
        for mt in PRICE_TOKEN.finditer(prose):
            tok = mt.group(1).replace(',', '')
            tail = prose[mt.end():mt.end() + 3]
            if PRICE_UNIT.match(tail):
                continue                       # 1322 家 / 223.37 億元 / 7.9%
            if tail[:1] in ('-', '/'):
                continue                       # dates: 2026-01-12
            x = float(tok)
            if not any(abs(x - y) <= max(0.011, abs(y) * 0.0002) for y in allowed_px):
                errs.append(f'price {tok} in prose is not in the contract for {t}')
                break

        for risk in (r.get('risks') or []):
            if TECH_RE.search(str(risk)):
                errs.append(f'technical wording in risks: {risk!r}')
                continue
            for numtxt in re.findall(r'\d+(?:\.\d+)?', str(risk)):
                x = float(numtxt)
                for col in ('Close', 'Entry_Ref', 'Invalidate_Below', 'Trigger_Price'):
                    y = f(k.get(col))
                    if y == y and abs(x - y) <= max(0.01, abs(y) * 0.005):
                        errs.append(f'restates contract {col} ({risk!r})')
                        break
        add('V9', not errs, f'{t}: ' + ('; '.join(errs) if errs else 'prose ok'))

        if RANK[v] < RANK[base]:
            reason = str(r.get('downgrade_reason', ''))
            if reason.startswith('STORY_RISK'):
                ok = (base == 'BUY' and v == 'STALK' and r.get('conviction') == 'CHALLENGE'
                      and re.search(r'https?://', reason) and re.search(r'\d{4}-\d{2}-\d{2}', reason))
                add('V7', bool(ok), f'{t}: story downgrade {base}->{v} conviction={r.get("conviction")}')
            else:
                # v6.1 (C4/V6): the reason must be one of the codes l2_prep computed for this
                # name from the contract. A free sentence ("Market sentiment bad") is not enough.
                try:
                    allowed = {x['code']: x for x in json.loads(k.get('Downgrade_Codes', '[]') or '[]')}
                except Exception:
                    allowed = {}
                code = str(r.get('downgrade_code', '')).strip()
                ok = code in allowed
                detail = (f'{t}: downgrade {base}->{v} code={code or "MISSING"}'
                          + (f' ({allowed[code]["why"]})' if ok else f' not in {sorted(allowed) or "no codes"}'))
                add('V6', ok, detail)
    # v6.2 (Grok #7): record how often L2 actually downgrades. No gate, just visibility —
    # a 0% rate means the gate is decorative and a human should look.
    tickets = [t for t in c.index if c.loc[t, 'Baseline_Verdict'] in ('BUY', 'STALK')]
    down = [t for t in tickets if RANK.get(c.loc[t, 'Baseline_Verdict'], 0)
            > RANK.get(next((r.get('verdict') for r in rows if r.get('ticker') == t),
                            c.loc[t, 'Baseline_Verdict']), 0)]
    rate = (len(down) / len(tickets)) if tickets else 0.0
    if isinstance(status, dict):
        status['downgrade_rate'] = round(rate, 3)
        status['downgrades'] = down
        try:
            with open(os.path.join(folder, 'l2_status.json'), 'w', encoding='utf-8') as fh:
                json.dump(status, fh, ensure_ascii=False, indent=1)
        except Exception:
            pass
    if tickets and not down:
        print(f'WARN downgrade_rate=0.0 ({len(tickets)} tickets, none downgraded) — '
              'check whether layer 2 is adding anything')

    fails = [x for x in res if x[1] == 'FAIL']
    lines = [f'# L2 check — {folder}', '', '| ID | Status | Detail |', '|---|---|---|']
    lines += [f'| {a} | **{b}** | {d} |' for a, b, d in res]
    with open(os.path.join(folder, 'L2_Check_Report.md'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')
    for a, b, d in res:
        print(f'{b:4} {a:3} {d}')
    print(f'\n{len(fails)} FAIL -> ' + ('DO NOT SEND the trade book' if fails else 'OK to send'))
    return 2 if fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else '.'))
