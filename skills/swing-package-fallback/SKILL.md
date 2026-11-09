---
name: swing-package-fallback
description: >-
  Use when Hermes US/HK L1 is down OR Justin/總指揮 supplies a full ticker list:
  /opt/swing scan → Drive PINNED → Story gate → after stories
  sync+check+render+Drive (incl. GPT image_pack).
---
# swing-package-fallback

ONE JOB: Local package scan → PINNED → Story gate → post-story S5 (verdicts + check + render + Drive, incl. GPT image packs). Never dual-run Hermes healthy daily without a Justin full-list override.

## Wake
- Hermes US/HK L1 down/unreachable **declared**, **or**
- Justin / 總指揮 **complete** US or HK ticker list (no Hermes-down announce required when list is complete)
- Missing declare **and** no list → STOP

## Prerequisites
1. `swing-package-verify` PASS on `/opt/swing`
2. Universe supplied — never invent tickers
3. Script-first: Connector → Script → Browser Script → Computer Use last

## Scan (scripts)
- **US:** `cd /opt/swing/us/02_CODE` → `scan553.sh` / `run_daily.sh` with output under `/opt/swing/us/run_*`
  - Pin `SWING_ROOT=/home/box` (or box home that has yfinance user-site) if scan553 exits 1 after `HOME→02_CODE` breaks imports
- **HK:** `cd /opt/swing/hk` → `run_daily.sh` + `run_l2.sh prep` (`SWING_MARKET=hk`)
- L2 prep → `L2_Input.csv` + `story_handoffs.md` + Contract/Trigger

## After scan — Story gate
If `Story_Needed=True` and `stories/<T>_story.json` missing:
1. Announce Story_Needed list + run path + Drive date folder
2. `NEXT_GATE: Story` — do **not** write narrative; do **not** wake SB/sim
3. Wait Soft Final stories (+ search logs)

If no Story_Needed → PINNED Contract/Trigger/index; `NEXT_GATE: 總指揮`

## After Story Soft Final — Ops owns S5 (scripts)

### Reality check (installed code vs docs)
- Docs say `python3 story_search_sync.py <run>` merges → `verdicts_*.jsonl`
- Installed `story_search_sync.py` only builds Sheets rows **from** existing verdicts (`--rows`)
- **Ops must build `verdicts_<market>.jsonl` by script** from Contract/L2 baseline + story conviction:
  - `entry`/`stop` = Contract `Entry_Ref` / `Invalidate_Below` (exact)
  - `verdict` ≤ `Baseline_Verdict` (no upgrades)
  - `conviction` = story.conviction
  - prose (`closer`/`emotion`/`invalidation`) within check_verdict limits; emotion vocabulary per verdict
  - Cover every baseline BUY/STALK (V8)

### Story schema normalize (mechanical, not narrative)
`check_verdict` expects `sources`/`numbers` as **objects** with `url` (+ `date` for numbers) ⊆ search_log urls. Soft Final may ship docs/05 string shapes — backup then objectify from existing search_log urls only. Do **not** rewrite `conviction_why` / story prose.

### V14
BUY/STALK + CONFIRM/CHALLENGE needs `conviction_why` citing a source domain/url/title[:12]. Fail → route Story fix (or Justin waive). Do not invent cite text.

### Commands
```bash
cd /opt/swing/us/02_CODE   # or hk
# build verdicts_*.jsonl via small Python merge (prices from Contract only)
bash run_l2.sh check <run>    # must exit 0
bash run_l2.sh render <run>   # reports/<T>_投資快報.md + <T>_image_pack.md + index
```
Optional: `python3 story_search_sync.py --rows <run>` → Story_Search_DB CSV rows (not a substitute for verdicts).

## Drive PINNED
`UploadFile` only accepts `/workspace` (or agent dir) — stage copies first, then upload.

**Always include:**
- `verdicts_US.jsonl` / `verdicts_hk.jsonl`
- `Contract_*.csv`, `L2_Input.csv`, `Trigger_*_PASS.csv` (or Trigger)
- `index.md`, `story_handoffs.md`, `L2_Check_Report.md`
- `stories/<T>_story.json` + `_search_log.json`
- `reports/<T>_投資快報.md` **and** `reports/<T>_image_pack.md` (GPT Image paste blocks)

US folder pattern: `US_Stock_Data/<Mon D>/`. Tradeable FAIL → WATCH + Why; never invent prices.

## Stop / anti
- Hermes healthy **and** no Justin list → stop fallback
- No unattended dual-run vs Hermes daily
- No Story narrative / Fusion / SB picks / sim opens from this skill
- No SB/sim wake unless Justin asks

## Known bugs / traps (2026-11-09)
1. **scan553 HOME/yfinance:** default cwd/HOME can break imports → pin `SWING_ROOT`
2. **story_search_sync ≠ verdicts writer** — docs ahead of code; write verdicts with a merge script
3. **Soft Final schema vs V12/V13** — string sources/numbers fail check; normalize to objects
4. **V14 cite** — CONFIRM without domain in `conviction_why` fails; Story patches
5. **PINNED miss image_pack** — render creates packs; always upload them with 快報
6. **as_of vs run day** — engine Date may lag calendar day; report both

## VERIFY
- [ ] Wake condition present
- [ ] Prior verify PASS; no dual-run
- [ ] Story_Needed without stories → NEXT_GATE Story (not silent skip)
- [ ] Post-story: verdicts from Contract prices; check exit 0; render; Drive incl. image_pack
- [ ] No invented tickers/prices/upgrades; no SB/sim wake
- [ ] Handoff 4 fields filled

## HANDOFF
PINNED_INPUTS: run folder + Drive dated folder  
DECISIONS_MADE: list/Hermes-down path; Story_Needed→Story; Ops S5 script merge  
OPEN_QUESTIONS: none | Story JSON incomplete | V14 cite | upload fail  
NEXT_GATE: Story (S4 gap) else 總指揮 → SB/sim when verdicts present
