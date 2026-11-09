# Quality checklist (run silently before send)

Tick every item. If one fails, fix the report. Do not show this list to the user.

- [ ] RS reading correct? Benchmark not assumed? Missing RS printed as MISSING?
- [ ] Entry zone ≠ stop?
- [ ] Vol_Expansion << 1 named as 縮量 if the handoff has it?  ← **v3.2 已刪除，見下方**
- [ ] 一句講晒 matches VERDICT and stays ≤50 characters?
- [ ] Main story passed Why Now + moat + numbers?
- [ ] HK transmission layer scored? US core / edge / none scored?
- [ ] Pharma names ran KB D searches?
- [ ] EARNINGS ≤14 / ≤7 rules applied?
- [ ] None of the five narrative traps unmarked?
- [ ] Every verifiable claim has `[SEARCH]` + URL, or an explicit 「無搜尋結果」?
- [ ] No invented numbers, fake sources, or fabricated analyst targets?
- [ ] Claude VERDICT / prices untouched?
- [ ] Both bull and bear news present if both exist?
- [ ] Output can drop into Fusion Prompt v1.1 as-is?
- [ ] Emotion tag matches VERDICT?
- [ ] CONVICTION cites a search result, not vibes?
- [ ] Did not redo TA or upgrade WATCH/AVOID to BUY?

---

## v3.2 修訂（覆蓋上面第 3 項）

`Vol_Expansion << 1 = 縮量風險` 這條**作廢**。v5 的量能有兩個意思，不可混用：

- `BASE VOLUME DRY-UP` 低（<0.7）= 賣壓衰竭 = **好**，不可寫成縮量風險。
- `BREAKOUT VOLUME: LOW` = 突破未確認 = **風險**，必須寫進風險敘事。
- `PENDING` / `NOT_APPL` = 不評論量能。

## v5.5.2 追加（機器檢查，會自動跑）

- [ ] `stories/<T>_search_log.json` 存在，且每個 `sources[]` / `numbers[]` 的 URL 都在裡面（V12／V13）
- [ ] BUY/STALK 且 CONFIRM/CHALLENGE → `sources` ≥2，`conviction_why` 引用其中一條（V14）
- [ ] 沒有簡體字（V15）
- [ ] Earnings UNKNOWN → `earnings_check` 有日期+URL 或「未能確認」（V16）
- [ ] 長度：story_main ≤200、why_now ≤60、story_sub ≤120、risks ≤4（V17）
- [ ] 最後一行 `CONVICTION: CONFIRM | CHALLENGE | NEUTRAL`（V11）
- [ ] `python3 check_verdict.py run_X` 全 PASS
