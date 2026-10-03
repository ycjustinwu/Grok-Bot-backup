---
name: Telegram Xlsx Send
description: >-
  Use this whenever sending an Excel xlsx to Justin (Telegram or chat) —
  explicit filename.xlsx, send as document, short caption; never hash names or
  oversize captions.
---
# Telegram Xlsx Send

How to deliver an `.xlsx` so the user can open it. Applies to Stockbee T2108, volume-spike, pine screener, or any xlsx.

## Grok chat (default here)

Attach the file with its **real name** `Something_YYYY-MM-DD.xlsx`. Short caption. Long audit text in a **second** message.

## Telegram (only if env is set)

Use `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` from the environment — **never hardcode tokens**. If missing, attach in Grok chat instead.

Must set all three:

1. `filename="Readable_Name.xlsx"` — without this, Telegram hashes the name and Excel won’t open
2. Send as **document** (`asDocument` / `sendDocument`) — skip auto-compression
3. Caption **≤1024 chars** (4096 hard fail kills the whole send)

Long commentary = message 2, not the caption.

Never: missing filename · missing document flag · stuffing tables into the caption.
