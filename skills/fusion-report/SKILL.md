---
name: Fusion Report
description: >-
  Use this after Fusion Ingest to write OUTPUT ① — the ≤500-character
  Traditional Chinese Fusion Report with Cantonese closer, tech verdict
  priority, and Adjusted_Stop.
---
# Fusion Report

OUTPUT ① — Fusion Report, **≤500 字** total. 繁體中文書面語; 一句講晒 = 廣東話. Faithful merge only.

## Budgets (hard)

| Block | Max |
|-------|-----|
| 🎯 核心故事 | 80 字 |
| 📊 技術狀態 | 100 字 |
| ⚠️ 主要風險 | 80 字 (≤3 red flags) |
| 🎬 執行劇本 | 150 字 |
| 💬 一句講晒 | 50 字 |
| **Total** | **≤500 字** |

## Template

```
═══════════════════════════════════════════
📌 [代號] [名稱] --- 投資快報
分析日期：[YYYY-MM-DD]
═══════════════════════════════════════════

🎯 核心故事（≤80字）
主線：…（from Story）
次線：…

📊 技術狀態（≤100字） — compact table:
Priority Score | RS Score | Setup Type | Playbook | RR Best | Vol_Expansion | Extension MA20 | RSI 14

⚠️ 主要風險（≤80字，最多3項）
[+ EARNINGS PASS/CAUTION line if needed]

🎬 執行劇本（≤150字）
建議操作：🟢BUY / 🟡STALK / 🟡WATCH / 🔴PASS / 🔴AVOID  （= tech VERDICT）
進場觸發：情境 A/B…
止損：$[ADJUSTED STOP]（標 Stop_Type）
目標：T1/T2/T3 + scale-out 50/75/100 + paired RR
最佳 RR：…

💬 一句講晒（≤50字，廣東話）
「…」
情緒標籤：🚀｜✅｜⚡｜⚠️｜❌
═══════════════════════════════════════════
```

## STALK framing

建議：🟡 STALK · 進場：等量能突破 $[Tight_Zone_High]（收市確認，量 ≥ Zone Avg ×1.5）· 現在：觀望，不追入

## Overrides from tech body

- Breakdown w/o Slap Back → AVOID
- TZ-C + RS>10 + Minervini=1 may keep BUY/high-confidence WATCH even if Priority a bit low
- Prefer RR_Zone_Best when TZ active; else paired RR from handoff
- Prefer story 一句講晒 if it already matches VERDICT; else rewrite to match tech

Count 字 before send; trim if over.
