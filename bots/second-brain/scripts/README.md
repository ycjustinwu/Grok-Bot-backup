# Second-brain Hermes Soft Final scripts

## `hermes_soft_final.py`

**Intent:** cut token burn on ranking / hard-exclude / §3.3 handoff copy **and** the locked 書面語 Soft Final skeleton. Model decides; script executes filters + rank + Contract field copy + draft + judgment flags. Soft-demote is a *suggestion in the draft only*.

Single CLI (a sibling module `soft_final_draft.py` is imported automatically):

```bash
python3 /workspace/second-brain/scripts/hermes_soft_final.py   --pack-dir /workspace/second-brain/hermes-packs/hermes-YYYY-MM-DD   --out-dir /workspace/second-brain/YYYY-MM-DD   --prior-dir /workspace/second-brain/YYYY-MM-DD-prev   --prior-pack-dir /workspace/second-brain/hermes-packs/hermes-PREV-DATE   --drive-folder <Drive folder URL or id>   --book TEM@72.21,UNTY@57.46   --run-date YYYY-MM-DD
```

Flags:
- `--pack-dir` (required) — local Hermes pack (`verdicts_US.jsonl`, `L2_Input.csv`, `Contract_US.csv`, …)
- `--out-dir` — default: dated parent of pack, else `./<Contract Date>`
- `--max-stalks` — default `3`
- `--prior-stalks T1,T2` — no-repeat remark only
- `--no-repeat-exclude` — actually drop prior tickers from stalks
- `--prior-dir` — previous Soft out-dir (has `ranked_candidates.json`). Auto-discovered when out-dir is `/workspace/second-brain/YYYY-MM-DD` (looks at the previous calendar day, plus `hermes-packs/hermes-<prior contract date>`).
- `--prior-pack-dir` — previous Hermes pack (for Leader_OK / Close when the prior ranked file is from an older script).
- `--book` — default `TEM@72.21,UNTY@57.46`. Never auto-wake 模擬倉.
- `--drive-folder` — Drive folder URL or id, used in the header / PINNED.
- `--tc` — optional; default `TC-YYYYMMDD-SB-novN` from `--run-date` + contract month/day.
- `--run-date` — default: today `Asia/Hong_Kong`.

Exit codes: `0` OK · `2` missing primary / date mismatch · `3` no *script* survivors (still writes cannot-find draft; soft-demote to 0 stalks is still exit `0` if the script had stalks).

### Writes

| File | Role |
|------|------|
| `ranked_candidates.json` | Full universe: `stalk_candidate` / `observe` / `excluded` + reasons + rank components + Close / Leader / away_pct / quality_pass_total / l_near_sl. **Script stalks stay pre-demote.** |
| `handoff_blocks.md` | Hermes §3.3 blocks for **script** stalks (pre-soft-demote). LLM may later overwrite this after confirming a demote. |
| `handoff_blocks.script.md` | Exact copy of the script handoff, so a later LLM demote can overwrite `handoff_blocks.md` without losing the original. |
| `judgment_flags.json` | Compact flags for the LLM (main token-save): counts, script stalks, `soft_demote` reasons, remaining Soft-stalk suggestion, index conflicts, story_in_pack, do_not_upgrade, prior_changes, book_remarks. |
| `attention-3-picks.draft.md` | 書面語 Soft Final in the locked template (`/workspace/second-brain/templates/soft-final-output.md`). Soft-demoted script stalks go to 觀察; survivors keep §3.3 blocks. PINNED at the bottom (paths only). |
| `attention-3-picks-notion.md` | Same draft minus PINNED. |
| `soft_final_stub.md` | **Deprecated** one-line pointer to `attention-3-picks.draft.md` (keeps old callers from breaking). |
| `script_verify.json` | Date match, banned-token scan (handoff + draft), counts, handoff md5, `draft_path`, `soft_demoted`, `flag_counts`. |

CSV reads use `pandas.read_csv(..., keep_default_na=False)`.

`verdicts_US.jsonl` is authoritative over `index.md`. The script flags index lies (A_SETUP / BUY vs STALK / “no story commissioned”) and tells the LLM: never treat index BUY as buyable.

### Soft-demote rules (draft only; standing Justin prefs)

Applied as *suggestions*; they do **not** drop names from `ranked_candidates.json` / `handoff_blocks.md`:

1. `Leader_OK FAIL` → `leader_wait` (2026-11-07)
2. `away_pct ≥ 5` → fillable gate, observe only (2026-11-01). `away_pct = abs(close-entry_ref)/close*100`
3. `l_near_sl` → demote (limit vs stop <0.5%, or `Risk_Pct_Plan < 0.5`)
4. `thin_room` (1 ≤ room < 2) **and** Grade not in {A, A+} → `thin_room_weak_grade`. Grade A / A+ thin_room stays a Soft-stalk *suggestion* (LLM still owns “not can’t-miss”).
5. Story stance is information / 獨立判斷 fuel, **not** an automatic demote.

Never lower the bar to fill 3. Never upgrade WATCH/AVOID. Never stalk Tradeable FAIL. Never invent targets. Copy Contract numbers.

### Self-test fixtures (write only to `/tmp`; do not touch published Softs)

```bash
# 1) Nov 5 golden — script stalks ['UNTY'] thin_room; never upgrade ECVT/HOMB
python3 /workspace/second-brain/scripts/hermes_soft_final.py   --pack-dir /workspace/second-brain/2026-11-05/hermes-nov5   --out-dir /tmp/sb-draft-test-nov5
# expect: exit 0, selected ['UNTY'] thin_room. Draft may soft-demote UNTY if Leader_OK FAIL and/or B-grade thin_room actually fire.

# 2) Nov 12 — cannot-find after soft-demote + index conflict + GME / SWKS / book
python3 /workspace/second-brain/scripts/hermes_soft_final.py   --pack-dir /workspace/second-brain/hermes-packs/hermes-2026-11-12   --out-dir /tmp/sb-draft-test-nov12   --prior-dir /workspace/second-brain/2026-11-12   --prior-pack-dir /workspace/second-brain/hermes-packs/hermes-2026-11-11   --drive-folder 115jAKT2geqUKmR-kitwjyOiWALeIoFAU   --book TEM@72.21,UNTY@57.46   --run-date 2026-11-13
# expect: ranked stalk_candidate ['RBLX']; draft Soft stalks = 無 after thin_room_weak_grade;
#   index_conflicts (A_SETUP none vs 1; BUY 1 vs STALK; story already on disk);
#   GME do_not_upgrade; SWKS window closed; TEM/UNTY book remarks; RBLX story CHALLENGE.

# 3) Nov 11 — SUNB leader_wait demote; SWKS A-grade thin_room stays a suggestion
python3 /workspace/second-brain/scripts/hermes_soft_final.py   --pack-dir /workspace/second-brain/hermes-packs/hermes-2026-11-11   --out-dir /tmp/sb-draft-test-nov11
# expect: script stalks include SUNB and SWKS; soft-demote SUNB (leader_wait);
#   SWKS remains a Soft-stalk suggestion; APG do_not_upgrade (thicker-room WATCH).
```

Published Soft Finals under `/workspace/second-brain/2026-11-12/attention-3-picks.md` and `2026-11-13/attention-3-picks.md` must not be overwritten by tests.

### What the LLM must still do

After script output exists:

1. Do **not** re-rank from raw CSV/jsonl.
2. Start from `attention-3-picks.draft.md` + `judgment_flags.json` (plus `ranked_candidates.json` / `script_verify.json` as needed).
3. May **confirm or undo** a *soft* demote of a script STALK. Never upgrade WATCH/AVOID; never invent prices/targets — Contract copy in handoff wins.
4. Do **not** recap regime / US Brief / Market Master / RS overview. Do not load those full reports unless a flag says a conflict must be checked. PINNED already lists paths only.
5. Polish 獨立判斷 wording if needed; optional short X dig; Notion sync from `attention-3-picks-notion.md`; Jev C gates when that environment is available.
6. Session overview stays skipped unless Justin asks.
7. Download Hermes pack stays **Connector (Drive MCP)** — see `download_notes.md`.

### Token-save

No longer needs LLM for: hard-exclude loop, Grade→Room→RS sort, thin_room tagging, §3.3 field copy, banned-token scan, PINNED pack + context *paths*, index-vs-verdicts conflict detection, story-in-pack stance, soft-demote suggestions, 書面語 draft skeleton (header / tables / 獨立判斷 bullets from flags), book remarks, prior window-closed / do_not_upgrade flags.
