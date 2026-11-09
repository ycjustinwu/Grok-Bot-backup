#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Every contract field the playbook names must actually exist in Contract_US.csv.

    python3 check_fields.py ../01_RULES/PLAYBOOK_v5.4.md ../03_RUN/run_v54/Contract_US.csv

Why: a layer-2 rule that reads a field nobody exports is unenforceable, and the failure is
silent — the LLM simply cannot check that rule. This turns it into a visible warning.

Exit 0 = every referenced field exists (or no playbook found). Exit 1 = at least one missing.
"""
import re
import sys

import pandas as pd

# CamelCase-ish identifiers with at least one underscore: Leader_OK, Room_To_Soft_R, ...
FIELD_RE = re.compile(r'`([A-Z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+|contract_version)`')
# identifiers that are deliberately not contract columns: enum values, stop-type names, and
# the retired v4.6 field names that the playbook lists as "do not use".
NON_COLUMN = {
    # classes / verdicts / states / feasibility
    'A_SETUP', 'C_WATCH', 'B_LEADER_WAIT', 'X_NONE', 'BUY', 'STALK', 'WATCH', 'AVOID',
    'READY', 'ARMED', 'TRIGGERED', 'SPENT', 'FAILED', 'EXPIRED', 'BO_FAILED', 'NONE',
    'NOT_YET', 'AT_TRIGGER', 'AT_MARKET', 'NEXT_DAY', 'LATE', 'MISSED', 'INVALIDATED',
    'NO_SETUP', 'NONE_ABOVE', 'NOT_APPL', 'PASS', 'FAIL', 'UNKNOWN', 'PENDING',
    # stop-type names (values of Stop_Type_Plan)
    'PB_STRUCT', 'MA_STRUCT', 'VP_STRUCT', 'SR_STRUCT', 'TRIGGER_LOW', 'BASE_LOW',
    # room basis values
    'RISK', 'PROV_1ADR',
    # supply sources
    'RES20_PRIOR', 'HIGH52W_PRIOR', 'BEAR_FVG',
    # retired v4.6 names quoted only as "do not use"
    'Action_Refined', 'Adjusted_Stop', 'Playbook_Flag', 'Setup_Type', 'Stop_Type',
    'Suggested_Stop', 'Tight_Zone_Low', 'Tight_Zone_Days', 'RR_Ratio_Best', 'RR_Zone_Best',
    'contract_version',
}


def playbook_fields(path):
    with open(path, encoding='utf-8') as fh:
        text = fh.read()
    names = set(FIELD_RE.findall(text))
    # SWING_* are environment switches documented next to the rules, not contract columns
    return {n for n in names if n not in NON_COLUMN and not n.startswith('SWING_')}


def main(playbook, contract):
    cols = set(pd.read_csv(contract, nrows=0).columns)
    want = playbook_fields(playbook)
    missing = sorted(want - cols - NON_COLUMN)
    print(f'playbook: {playbook}')
    print(f'contract: {contract} ({len(cols)} columns)')
    print(f'fields referenced by the playbook: {len(want)}')
    if missing:
        print(f'MISSING ({len(missing)}): ' + ', '.join(missing))
        print('A rule that reads a missing field cannot be followed.')
        return 1
    print('all referenced fields exist')
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(0)
    sys.exit(main(sys.argv[1], sys.argv[2]))
