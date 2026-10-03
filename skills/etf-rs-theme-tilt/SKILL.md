---
name: ETF RS Theme Tilt
description: >-
  Use this after ETF RS Overlay Ingest when writing Market Awareness regime
  daily — emit Favor/Avoid ETF RS theme tilt plus 趨勢觀察 (2d+5d both-Rising /
  both-Declining-while-leading); overlay only, never score input.
---
# ETF RS Theme Tilt (Market Awareness)

Adds a short **non-scoring** section to the Regime daily after CUP Monitor observation (before Modifier Notes). Depends on [ETF RS Overlay Ingest](sand-workflow:etf-rs-overlay-ingest).

## Placement

In [Regime Daily Report](sand-workflow:regime-daily-report) output order, insert:

`### 附加觀察｜ETF RS 主題傾斜（非計分）`

immediately **after** `### 附加觀察｜US Market Monitor（CUP／股票層）` and **before** `### 🔔 Modifier Notes`.

English internal name: **ETF RS theme tilt**. Chinese heading above is canonical for the 繁體中文 daily.

## Aggregation rules (Favor / Avoid)

From `theme_agg` (exclude Benchmark, Macro Vol-only noise unless narrative asks):

**Favor** (pick **2–3** themes):

- avg or median **RS actual ≥ 70**, **and**
- meaningful **5-day Rising** share (prefer ≥30% of theme names, or clear leaders Rising), **and**
- avg **vs VOO 5d > 0** (or top RS names clearly leading vs VOO 5d)

**Avoid** (pick **2–3** themes):

- avg **RS < 30**, **or**
- mostly **5-day Declining**, **or**
- avg **vs VOO 20d** deeply negative (judgment: roughly ≤ −3% relative or worse across theme)

Use existing **P1–P7 / L2** labels exactly as on the sheet (same as Layer 1 / regime reports). Prefer equity theme pillars over pure Macro/Risk for Favor; Avoid may include weak Risk Appetite / Defensive / Macro when aggregates qualify.

**P4 Speculation / crypto-heavy:** may appear in Favor narrative if aggregates qualify, but label clearly as speculation — do **not** imply ordinary equity exposure should chase crypto RS.

If fewer than 2 themes qualify on a side, print what qualifies + one line `不足 2 個主題達標`.


## 趨勢觀察（2d + 5d same-direction）— Justin 2026-10-02

Horizon pair = sheet columns **`2-day trend` + `5-day trend`** (labels `Rising` / `Declining` / `No Trend`).  
Justin wrote “5d and 2d”; Dashboard has a literal **2-day trend** column (col after `RS 5d ago`) — **use 5d+2d**. Do **not** invent a 20-day trend label (`vs VOO 20d` is a return, not Rising/Declining).

Place as a short **`趨勢觀察`** block **after Favor and Avoid**, still under the same `### 附加觀察｜ETF RS 主題傾斜（非計分）` heading, **before** the non-scoring 註.

### A — Both Rising（強化趨勢）
- Flag tickers where **2-day trend = Rising AND 5-day trend = Rising**.
- Not required to be top RS — purpose is early strengthening (example pattern: names that were both-Rising days ago and later led).
- Cite **2–5 concrete tickers** from **this session’s sheet** with theme + RS actual + both trend labels. Prefer equity P1–P7 / L2 over Macro Vol noise when space is tight.
- If Justin named examples (e.g. FOTO, SOXX): cite them **only if** the sheet shows both Rising; otherwise omit or note actual labels (never invent Rising).

### B — Both Declining while still leading（領導版塊有機會轉弱）
- Flag tickers where **2-day = Declining AND 5-day = Declining**, **and** still in a leading position: **RS actual ≥ 70**, and/or in a Favor theme, and/or top of that theme’s RS rank.
- Narrative: `領導版塊有機會轉弱` — leading block may be rolling over.
- Cite 2–4 tickers with theme + RS + both Declining labels. If none qualify, one line `今日無「雙降且仍領先」標的`.

Overlay only — same ANTI-JOB as Favor/Avoid (no TOTAL / band / hysteresis / FT / CC / Exposure).

## Must cite

1. **US trade date** = sheet stamp  
2. Per Favor theme: **2–3 example tickers** with **RS actual** + **vs VOO 5d** (and 5d trend if space)
3. **趨勢觀察**: both-Rising and (if any) both-Declining-while-leading tickers with **actual** 2d+5d labels from sheet — never invent

## ANTI-JOB (critical)

- Do **not** feed this section into TOTAL / band / hysteresis / Fast-Track / Change C / Exposure Ceiling.
- Do **not** invent RS numbers; omit section with DATA GAP line if ingest gated.
- Do **not** replace US Market Daily Brief theme package.

## Subsection template (exact)

```text
### 附加觀察｜ETF RS 主題傾斜（非計分）
US trade date：{YYYY-MM-DD}（sheet；非港股下載日）
來源：ETF Relative Strength Dashboard（Drive `1cgrNJNg0hX7mQV9H-0gU6dcGQ5OCwVaU9aTkVrq2iLQ`）

Favor（2–3）：
- {Theme}：avg/med RS {..}；5d Rising {k}/{n}；avg vs VOO 5d {+x.x%}
  例：{TKR} RS{..} vsVOO5d{+..%} [{Rising|…}]；{TKR2} …；{TKR3} …
- …

Avoid（2–3）：
- {Theme}：avg RS {..} / 5d Declining {k}/{n} / avg vs VOO 20d {−x.x%}
- …

趨勢觀察（sheet 2-day + 5-day trend；非 20d）：
- 雙升（2d Rising ∩ 5d Rising）：{TKR} RS{..} [{theme}]；… — 強化趨勢（未必最高 RS）
- 雙降且仍領先（2d Declining ∩ 5d Declining 且 RS≥70 / Favor / 主題前列）：{TKR} RS{..} [{theme}]；… — 領導版塊有機會轉弱
  （若無雙降領先：今日無「雙降且仍領先」標的）

註：本節為 overlay 敘事，不進入 TOTAL／制度帶／hysteresis／曝險數學。
```

DATA GAP variant (one block):

```text
### 附加觀察｜ETF RS 主題傾斜（非計分）
⚠️ DATA GAP — ETF RS Dashboard 缺失或 US trade date 過期（預期 US session {D}，sheet {got or none}）。本節省略；Regime TOTAL 不受影響。
```

## VERIFY

- [ ] Section after CUP Monitor, before Modifier Notes
- [ ] Favor 2–3 + Avoid 2–3 (or explicit shortfall note)
- [ ] US trade date stamped from sheet
- [ ] Each Favor theme has 2–3 tickers with RS actual + vs VOO 5d
- [ ] Theme labels match P1–P7 / L2 sheet names
- [ ] Explicit non-scoring note present
- [ ] 趨勢觀察 present (2d+5d both-Rising; both-Declining-while-leading or explicit none) — labels from sheet only
- [ ] No change to TOTAL / band / hysteresis / exposure from this section
