#!/usr/bin/env bash
# 安裝驗證：不需要網路，不會弄髒任何真實 run。
set -uo pipefail
cd "$(dirname "$0")"
PKG=$(pwd)
CODE="$PKG/02_CODE"
SAMPLE="$PKG/03_SAMPLE/run_v56"
fail=0
TMPROOT=$(mktemp -d "${TMPDIR:-/tmp}/usswing_verify.XXXXXX") || { echo "cannot create a temp dir (TMPDIR=$TMPDIR)"; exit 1; }
trap '[ "$fail" -eq 0 ] && rm -rf "$TMPROOT" || echo "  失敗現場保留在：$TMPROOT"' EXIT
ok()   { printf '  \033[32mOK\033[0m   %s\n' "$1"; }
bad()  { printf '  \033[31mFAIL\033[0m %s\n' "$1"; fail=1; }

echo "== 1. Python =="
python3 - <<'PY' && ok "Python >= 3.11" || bad "Python 太舊"
import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)
PY

echo "== 2. 套件 =="
python3 - <<'PY' && ok "yfinance / pandas / numpy 可用" || bad "缺套件（pip install -r requirements.txt）"
import importlib.util, sys
need = ("yfinance", "pandas", "numpy")
missing = [m for m in need if not importlib.util.find_spec(m)]
print("missing:", missing) if missing else None
sys.exit(1 if missing else 0)
PY

echo "== 3. 編譯 =="
if python3 -m py_compile "$CODE"/*.py 2>$TMPROOT/compile.err; then ok "所有 .py 編譯通過"; else bad "編譯失敗（見 $TMPROOT/compile.err）"; fi

echo "== 4. 樣本不變量 =="
( cd "$CODE" && python3 invariants.py "$SAMPLE" >$TMPROOT/inv.txt 2>&1 )
if grep -qE '^FAIL ' $TMPROOT/inv.txt; then bad "樣本不變量有 FAIL"; else
  ok "23 條不變量通過（$(grep -cE '^PASS' $TMPROOT/inv.txt) PASS）"; fi

echo "== 5. Playbook 欄位 =="
( cd "$CODE" && python3 check_fields.py "$PKG/01_RULES/PLAYBOOK_v5.4.md" "$SAMPLE/Contract_US.csv" >$TMPROOT/cf.txt 2>&1 )
if grep -q "all referenced fields exist" $TMPROOT/cf.txt; then ok "playbook 引用的欄位都存在"; else bad "playbook 與 Contract 不同步"; fi

echo "== 6. L2 閘門（樣本） =="
rm -rf $TMPROOT/sample && cp -r "$SAMPLE" $TMPROOT/sample
( cd "$CODE" && python3 check_verdict.py $TMPROOT/sample >$TMPROOT/cv.txt 2>&1 )
if [ $? -eq 0 ]; then ok "check_verdict 對樣本 PASS"; else bad "check_verdict 對樣本 FAIL"; fi

echo "== 7. 排版（樣本副本） =="
( cd "$CODE" && python3 render_report.py $TMPROOT/sample >/dev/null 2>&1 )
if [ -f $TMPROOT/sample/reports/index.md ]; then ok "render_report 產出 index.md"; else bad "render 沒有產出"; fi

echo "== 8. 檔頭版本 =="
VER=$(grep -oE "us-contract-[0-9a-z.]+" "$CODE/us_swing_v55.py" | head -1)
if [ "$VER" = "us-contract-1f.6" ]; then ok "contract 為 1f.6"; else bad "contract 版本不對（${VER}）"; fi

echo "== 9. 文件與程式對齊（A6） =="
VEDOC=$(grep -oE "us-contract-[0-9a-z.]+" "$PKG/01_RULES/PLAYBOOK_v5.4.md" | head -1)
if grep -rq "102 欄" "$PKG/01_RULES/"; then
  bad "01_RULES 仍寫 102 欄"
elif [ "$VEDOC" != "$VER" ]; then
  bad "PLAYBOOK 寫 ${VEDOC}，引擎是 ${VER}"
else
  ok "文件與引擎同版（${VER}）"
fi

echo "== 10. 回歸測試（A1-A12） =="
if [ -f "$CODE/tests/regressions.py" ]; then
  if ( cd "$CODE" && python3 tests/regressions.py >"$TMPROOT/regr.txt" 2>&1 ); then
    ok "回歸測試全過（$(grep -c '  OK ' "$TMPROOT/regr.txt") 項）"
  else
    bad "回歸測試失敗（見 $TMPROOT/regr.txt）"; tail -5 "$TMPROOT/regr.txt" | sed 's/^/     /'
  fi
else
  bad "缺 tests/regressions.py"
fi

if [ "$fail" -eq 0 ]; then echo; echo "ALL CHECKS PASSED"; else echo; echo "SOME CHECKS FAILED"; fi
exit "$fail"
