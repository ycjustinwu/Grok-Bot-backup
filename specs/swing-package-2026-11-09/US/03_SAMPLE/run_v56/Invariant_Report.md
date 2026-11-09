# Invariant report — /opt/data/us-swing553/03_SAMPLE/run_v56

Internal consistency only. This is not a profitability test.

| ID | Check | Status | Detail |
|---|---|---|---|
| I1 | Score_Breakdown sums to Priority_Score | **PASS** | all rows reconcile |
| I3 | no verdict labels emitted by layer 1 | **PASS** | class labels only |
| I10 | RS_Status populated | **PASS** | 0/34 blank |
| I10 | Earnings_Proximity_Flag populated | **PASS** | 0/34 blank |
| I10 | Screen_Flag populated | **PASS** | 0/34 blank |
| I10 | Weak_Day_RS_Pct populated | **PASS** | 0/34 blank |
| I11 | negative room implies Risk_OK=FAIL | **PASS** | neg=0 unexplained=0 |
| I14 | Candidate_Class populated | **PASS** | 0/34 blank |
| I15 | A_SETUP implies Setup_OK and Risk_OK | **PASS** | 1 A_SETUP rows consistent |
| I16 | no setup => Setup_OK is not PASS | **PASS** | none |
| I17 | A_SETUP breakout obeys its family limits | **PASS** | 0 breakout rows ok |
| I18 | Contract has the filterable fields | **PASS** | 34 rows x 113 cols |
| I19 | Contract rows carry a ticker | **PASS** | 0 blank |
| I29 | no status value is a pandas NA token | **PASS** | 18 status columns clean (raw read) |
| I20 | Trigger rows are actionable states | **PASS** | 1 tickets |
| I21 | stop below entry on every ticket | **PASS** | 0 tickets with stop >= entry |
| I30 | every ticket is Tradeable=PASS | **PASS** | 1 tickets tradeable |
| I22 | Setup_Family in {BREAKOUT, PULLBACK, REVERSAL, NONE} | **PASS** | 0 bad |
| I23 | A_SETUP has a named family | **PASS** | 1 ok |
| I24 | Regime_State valid | **PASS** | {'NEUTRAL': 34} |
| I25 | TRIGGERED never below the breakout-bar low | **PASS** | 0 triggered rows ok |
| I26 | hard supply sits above the entry | **PASS** | 22 rows with supply |
| I27 | low-volume breakout is not A_SETUP (WATCH mode) | **PASS** | 0 REMARK rows |
| I28 | Evidence reduces to the Contract gates | **PASS** | 34 tickers reconcile |
