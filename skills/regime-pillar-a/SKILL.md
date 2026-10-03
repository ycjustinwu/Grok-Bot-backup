---
name: Regime Pillar A
description: >-
  Use this when scoring Regime Pillar A (breadth) for v6.4.5 — A1 parity-first +
  ratio fallback, A2 full Zone×State matrix with McClellan priority + clip[-1,4],
  A3 NYSI-primary + NYSI-only zero-cross; max /12 floor −4.
---
# Regime Pillar A (v6.4.5)

> Scoring math identical to v6.4.3. Version bump tracks orchestrator; do not invent new A rules.

Pillar A Breadth Intelligence — **max /12**, floor **−4** (A1−2 + A2−1 + A3−1). Show every calculation before the score. Source: Stockbee 1A (xlsx) + Breadth 1B (+ CSV helpers). McClellan state via `<mcclellan_rule>` PRIORITY ORDER (CROSS → AGREEMENT → DIVERGENCE NYMO-primary → FLAT). Full matrices: `docs/scoring-matrices.md` + `docs/v6.4.5/regime-scoring-v6.4.5.txt`.

## A1 Immediate Momentum /6 (floor −2)

### A1-i Daily 4% Pulse
- If `# Down 4% = 0` → score **2** + flag `EXTREME RATIO` (ratio_fallback).
- Else Ratio = Up4% ÷ Down4%: ≥4.0→2 | [2.0,4.0)→1 | [1.0,2.0)→0.5 | <1.0→0.
- Weakness note (flag only): ratio <0.8 for 3 consecutive days from **xlsx**.

### A1-ii 5D vs 10D — **parity-first**
1. If `|5D − 10D| < 0.2` → score **0**, **STOP** (exact equality always hits parity).
2. Else only: 5D>10D & 5D≥2→2 | 5D>10D & [1,2)→1 | 5D>10D & 5D<1→0.5 | 5D<10D & 5D≥1→−0.5 | 5D<10D & 5D<1→−1.
Show 5D, 10D, |diff|, which step.

### A1-iii Q25 Structural
- If `# Down 25%+ Q = 0` → score **2** + `EXTREME RATIO`.
- Else Q25 = Up25Q ÷ Down25Q. Direction vs **prev from xlsx**: Improving = today>prev; Deteriorating = today<prev; Unchanged = neither.
- ≥1.8 + improving→2 | ≥1.8 + not improving→1 | [1.2,1.8)→1 | [0.8,1.2)→0 | <0.8 + deteriorating→−1 | <0.8 + not deteriorating→−0.5.

## A2 Intermediate (T2108 × McClellan) /4 (floor −1)

1. **T2108 zone (half-open):** <20 Ext OS | [20,40) Recovery | [40,70) Easy | [70,80] OB | >80 Blow-off.
2. **McClellan state** PR/PF/NR/NF/CU/CD via priority order (show tier matched). Cross: prev<0→today≥0 = CU; prev≥0→today<0 = CD.
3. **FULL MATRIX** Zone×State — see `docs/scoring-matrices.md` (every cell defined).
4. **Patterns** (xlsx + thread McClellan): Breadth thrust −100→+100 in 5d = **flag only**; 3rd higher low **+1**; bearish double top **−1**; zero-line rejection **−1**.
5. **Clip:** `A2_final = clip(raw + adjustment, −1, 4)`. Show raw / adjustment / pre-clip / final.
6. MA breadth flags (SPXA etc.) = no score.

**Post-matrix lock (2026-09-09):** before locking A2, check zero-rejection and other patterns with evidence.

## A3 Summation /2 (floor −1)

NYSI primary, NASI secondary — full grid from prompt. Patterns + clip `A3_final = clip(..., −1, 2)`.
**Zero-cross bonus +1 only if `$NYSI` crosses up today.** NASI-only cross = flag `NASI 率先轉正，待 NYSI 確認`, **no points**.

Output A1+A2+A3 with shown math → **Pillar A /12**.
