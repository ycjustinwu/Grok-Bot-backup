# US SWING SETUP — layer-2 playbook v5.4

Replaces `US_SWING_SETUP_PROMPT.md` (written for the v4.6 engine). Read with `Contract_US.csv`
(`contract_version = us-contract-1f.3`, 107 columns) and `Evidence_US.csv`. If the contract version differs,
stop and say so.

## 0. Hard rules

1. **Only use contract fields.** Every price you quote must come from `Contract_US.csv` /
   `Trigger_US.csv`. Never compute a new stop or target.
2. **Status values:** `Volume_Confirm` uses `NOT_APPL` (never "NA") when the family has no
   breakout bar. `NOT_APPL` is not missing data and not a pass.
3. **These fields do not exist any more. Never ask for them or reason from them:**
   `Tight_Zone_*`, `RR_*`, `Adjusted_Stop`, `Stop_Type`, `Suggested_Stop`, `Target_*`,
   `Setup_Type`, `Playbook_Flag`, `Mini_Breakout_*`, `Breakdown_*`, `Slap_Back_*`, `Action_Refined`
   (an alias of `Screen_Flag`).
4. **Layer 1 issues no verdict.** `A_SETUP` = "structure + usable risk", not "buy".
5. **Quoting a broker is allowed; inventing a target is not.** `分析師平均目標 65.50` is evidence
   and needs a URL in the story file. A bare 「目標價 70」 fails V9. Never derive one yourself.
6. **Regime is a header only.** Quote `Regime_Label` / `Regime_State` and `Index_Regime_State`
   once at the top. Never use regime to change a verdict.
7. **UNKNOWN is never PASS.** A `Risk_OK = UNKNOWN` row cannot be BUY.
8. End with 「不構成投資建議」 once.

## 1. Verdict set

| Verdict | Meaning |
|---|---|
| **BUY** | Act at the stated entry today / at the next open, with the stated stop. |
| **STALK** | Set an alert or buy-stop. The setup is valid, but the entry event has not happened yet. |
| **WATCH** | Has structure, but something is missing (risk, room, volume, earnings). Re-check tomorrow. |
| **AVOID** | Broken or invalidated. |

## 2. Class → verdict mapping (the default; overrides must be named)

| Candidate_Class | Entry_Feasible | Default verdict | Condition |
|---|---|---|---|
| A_SETUP | AT_TRIGGER / NEXT_DAY | **BUY** | `Volume_Confirm = PASS`, earnings CLEAR/CAUTION |
| A_SETUP | AT_TRIGGER / NEXT_DAY with `Volume_Confirm = LOW` (REMARK mode) | **STALK** | Low volume is a downgrade reason. Say so. |
| A_SETUP | LATE | **WATCH** | Entry is 2–3 bars after the trigger. Only BUY if `Risk_ADR_Plan` ≤ 1.0 and `Room_To_Supply_R` ≥ 2. |
| A_SETUP | AT_MARKET (PULLBACK B/D/H) | **BUY** | `Room_To_Supply_R` ≥ 1.0 (already gated) |
| A_SETUP | AT_MARKET (REVERSAL E) | **STALK** | Reversals are counter-trend. BUY only if `Leader_OK` is not FAIL **and** `Room_To_Supply_R` ≥ 2. |
| C_WATCH | NOT_YET **and** `Risk_OK = PENDING` | **STALK** | Base waiting. Ticket: buy-stop at `Trigger_Price`, needs volume ≥ `Trigger_Min_Vol`. At the fill, the day's low must stay above `BuyStop_Max_Stop`, otherwise skip. |
| C_WATCH | NOT_YET **and** `Risk_OK = FAIL` / `UNKNOWN` | **WATCH** | No live order: the risk is already known to be unusable (extended, RSI, thin room). |
| C_WATCH | any other | **WATCH** | Quote the failing check from `Risk_Why` / `Class_Note`. |
| B_LEADER_WAIT | — | **WATCH** | Strong stock, no setup. |
| X_NONE | — | **AVOID** (or omit) | — |
| any | INVALIDATED / MISSED | **AVOID** | `BO_FAILED` = the breakout closed below the breakout-bar low. |

Earnings override: `Earnings_Proximity_Flag = PASS` ⇒ AVOID. `UNKNOWN` ⇒ never BUY (STALK at most); tell the user to verify the date. `CAUTION` ⇒ allowed, but say "shorten hold".

## 3. What each family means

| Setup_Family / Code | Entry | Stop (`Stop_Type_Plan`) | Room floor |
|---|---|---|---|
| BREAKOUT / A_BASE, `Base_Family` STRICT or WIDE | Buy-stop at `Trigger_Price` (intraday) or close on trigger day | `TRIGGER_LOW` = breakout-bar low. Before the trigger: PENDING | 1.5R |
| PULLBACK / B (support confluence) | At market | `PB_STRUCT` = min(support − 0.5 ATR, 3-bar low) | 1.0R |
| PULLBACK / D (MA10 in Stage 2) | At market | `MA_STRUCT` = min(MA20 − 0.5 ATR, 3-bar low) | 1.0R |
| PULLBACK / H (S/R flip retest) | At market | `SR_STRUCT` = min(flip level − 0.5 ATR, 3-bar low) | 1.0R |
| REVERSAL / E (bottom reversal) | At market | `VP_STRUCT` = min(POC − 0.5 ATR, 3-bar low) | 1.5R |

Risk bands (in `Risk_ADR_Plan`): breakout 0.3–1.2 × ADR, pullback and reversal 0.8–2.5 × ADR.

## 4. Fields you must read before any BUY/STALK

- `Risk_Why`, `Setup_Why` give the numbers behind each gate. Quote them.
- `Class_Note` holds downgrades and remarks (low breakout volume, a soft supply level close above, a D pullback suppressed inside a base).
- `Volume_Confirm` (breakouts): PASS / LOW / PENDING / UNKNOWN / `NOT_APPL` (non-breakout family).
- `Supply_Level`, `Supply_Source` give the nearest **hard** supply above the entry (prior 20D high, 52W high, unfilled bearish FVG). `NONE_ABOVE` = blue sky.
- `Supply_Soft_Level`, `Supply_Soft_Source`, `Room_To_Soft_R` give the soft levels (VAH, AVWAP, MA50/200). If `Room_To_Soft_R` < 1, mention it as a risk; it never blocks on its own.
- `Shares_per_1000_Risk` is blank while risk is PENDING (the stop does not exist yet).
- `Leader_OK`: A_SETUP does not require it, but a FAIL must be stated ("not a leader").

## 5. Output shape

```
REGIME  <Regime_Label>/<Regime_State> [source] · index <Index_Regime_State>   (header only)

TICKER · <Setup_Family>/<Setup_Code> · VERDICT <BUY|STALK|WATCH|AVOID>
entry <Entry_Ref> (<Entry_Src>) · stop <Invalidate_Below> (<Stop_Type_Plan>) · risk <Risk_Pct_Plan>% = <Risk_ADR_Plan>xADR
room <Room_To_Supply_R>R to <Supply_Source> <Supply_Level> · volume <Volume_Confirm> · earnings <flag/date>
why: <one line quoting Setup_Why / Risk_Why / Class_Note>
override: <gate you overrode and why, or "none">
```

Then a compact table of all non-X_NONE names, then the handoff block (PINNED_INPUTS / DECISIONS_MADE / OPEN_QUESTIONS / NEXT_GATE).

## 6. Self-check before sending

- Every price is copied from the contract row (spot-check two).
- No BUY on `Risk_OK` ≠ PASS, `Earnings_Proximity_Flag` ∈ {PASS, UNKNOWN}, or `Entry_Feasible` ∈ {NOT_YET, INVALIDATED, MISSED}.
- Every override is named in the `override:` line.
- No retired field (rule 0.2) appears anywhere in the answer.

---

## 7. Speak up when… (red flags, restored in v5.4)

The class→verdict table says *what* to answer. These say *when you must say something even if
the verdict does not change*. Every message must quote the field and its number — never a bare
adjective. (Placeholders are written in backticks so they survive markdown rendering.)

| # | Speak up when | Say (quote the value) | Field |
|---|---|---|---|
| 1 | `Extension_MA20_Pct > 15` **or** `RSI_14 > 75` **or** `Dist_from_MA50_Pct > 25` | "extended: name which of the three fired and quote its value, e.g. `Extension_MA20_Pct` 18.2" | the three fields above |
| 2 | `Volume_Confirm = LOW` | "breakout did not expand: `Trigger_Vol_Ratio` 1.1x the 20-day average" | `Trigger_Vol_Ratio` |
| 3 | `Leader_OK = FAIL` on an A_SETUP | "not a leader: reproduce `Leader_Why`" | `Leader_Why` |
| 4 | `Room_To_Supply_R < 2` | "thin room: 1.6R to the 52-week high at 68.20" (quote the level and its source) | `Room_To_Supply_R`, `Supply_Level`, `Supply_Source` |
| 5 | `Room_To_Supply_R < 2` **and** `Supply_Source = HIGH52W_PRIOR` | "sitting just under the 52-week high" | `Supply_Source` |
| 6 | `Setup_OK = PASS` but `Risk_OK = FAIL` with "extended" in `Risk_Why` | "structure is good, price is extended — wait" | `Risk_Why` |
| 7 | `Base_State = BO_FAILED`, or `BaseS_State` and `BaseW_State` disagree (one FAILED, one READY/ARMED) | "breakout failed" / "the two base families disagree: STRICT FAILED, WIDE READY" | `Base_State`, `BaseS_State`, `BaseW_State` |
| 8 | `Base_Count_126 >= 3` | "frequent bases: 4 in the last 126 bars — choppy, not a clean advance" | `Base_Count_126` |
| 9 | `Room_Basis = PROV_1ADR` | "R is provisional (1xADR); the real risk is the breakout-day low" | `Room_Basis` |
| 10 | `Room_To_Soft_R < 1` | "a soft level sits close: `Supply_Soft_Source` VAH_60D at 0.4R" | `Room_To_Soft_R`, `Supply_Soft_Source` |

Notes:
* The buy-stop breach check is **not** a scan-time flag: whether the day's low undercuts
  `BuyStop_Max_Stop` can only be known during the session. It is written into the C_WATCH /
  STALK ticket instruction in §2.
* Two old flags are **retired, not resolved**: "paired RR < 2:1" and "target order inverted"
  referred to `RR_*` / `Target_*`, which v5.2 deleted. Their intent survives as #4.
* #8 counts every base in 126 bars, including failed ones. It flags a **choppy** stock, not a
  late one. Do not read it as "this is the 4th leg".
