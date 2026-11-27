#!/usr/bin/env bash
# pytest-free acceptance for size_position.py
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$DIR/size_position.py" --self-test
python3 "$DIR/size_position.py" --entry 58.10 --stop 56.654 --json | python3 -c '
import json,sys
o=json.load(sys.stdin)
assert o["shares"]==344, o
assert abs(o["r_usd"]-497.76)<=0.5, o
print("CLI UNTY OK", o["shares"], round(o["r_usd"],4))
'
echo "test_size_position.sh PASS"
