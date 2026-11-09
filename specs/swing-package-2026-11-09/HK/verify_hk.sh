#!/usr/bin/env bash
# 港股安裝驗證（不需要網路）
set -uo pipefail
cd "$(dirname "$0")"
fail=0
ok(){ printf '  OK   %s\n' "$1"; }
bad(){ printf '  FAIL %s\n' "$1"; fail=1; }

echo "== 1. 編譯 =="
python3 -m py_compile *.py 2>/tmp/hk_c.err && ok "所有 .py 編譯通過" || { bad "編譯失敗"; head -3 /tmp/hk_c.err; }

echo "== 2. 市場常數 =="
python3 - <<'PY' && ok "markets.load('hk') 正確" || bad "市場常數不對"
import sys; sys.path.insert(0,'.')
import markets
p = markets.load('hk')
assert p['bench'] == '2800.HK', p['bench']
assert p['calendar'] == 'XHKG', p['calendar']
assert p['sheet_key'] == '港股', p['sheet_key']
PY

echo "== 3. 固定港股模式 =="
grep -q ".swing_market" run_daily.sh && ok "run_daily.sh 讀 .swing_market" || bad "run_daily.sh 未讀 .swing_market"
grep -q 'LIST="tickers_hk.txt"' run_daily.sh && ok "清單固定 tickers_hk.txt" || bad "清單不是 tickers_hk.txt"

echo "== 4. 清單 =="
n=$(grep -vc '^#' tickers_hk.txt 2>/dev/null || echo 0)
[ "$n" -gt 0 ] && ok "tickers_hk.txt 有 $n 隻" || bad "tickers_hk.txt 空白"

echo "== 5. 財報 override =="
n_ov=$(grep -vc '^Ticker' earnings_overrides.csv 2>/dev/null || echo 0)
python3 - <<'PY' && ok "earnings_overrides.csv 可解析（$n_ov 行）" || bad "earnings_overrides.csv 有問題"
import pandas as pd
d = pd.read_csv('earnings_overrides.csv', keep_default_na=False, dtype=str)
need = {'Ticker', 'Date'}
assert need <= set(d.columns), d.columns.tolist()
bad = d[~d['Date'].astype(str).str.match(r'^\d{4}-\d{2}-\d{2}$')]
assert bad.empty, f'bad dates: {bad.to_dict("records")[:2]}'
print('   overrides:', len(d))
if len(d) < 5:
    print('   WARN 只有 %d 行——可能被重裝覆蓋，備份在 *.bak-*' % len(d))
PY

echo "== 5b. 市場鎖定 =="
if [ "$(cat .swing_market 2>/dev/null | tr -d ' \r\n')" = "hk" ]; then
  ok ".swing_market = hk"
else
  bad ".swing_market 不是 hk（單獨跑 run_l2.sh 會回退 US）"
fi
v=$(python3 -c "import markets;print(markets.verdicts_filename())" 2>/dev/null)
[ "$v" = "verdicts_hk.jsonl" ] && ok "verdicts 檔名 = $v" || bad "verdicts 檔名 = ${v:-?}" 

echo "== 6. 最近一次 run 的不變量 =="
last=$(ls -d runs/hk/run_* 2>/dev/null | sort | tail -1)
if [ -n "${last:-}" ]; then
  python3 invariants.py "$last" >/tmp/hk_inv.txt 2>&1
  if grep -qE '^FAIL ' /tmp/hk_inv.txt; then bad "不變量有 FAIL"; else ok "$(grep -cE '^PASS' /tmp/hk_inv.txt) 條全過"; fi
else
  ok "尚未有 run（第一次跑之後再驗）"
fi

rm -f /tmp/hk_c.err /tmp/hk_inv.txt
echo
[ "$fail" -eq 0 ] && echo "ALL CHECKS PASSED" || echo "SOME CHECKS FAILED"
exit "$fail"
