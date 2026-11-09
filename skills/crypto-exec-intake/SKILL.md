---
name: crypto-exec-intake
description: Use when Crypto Exec receives a TV/webhook alert — HMAC verify, parse JSON, idempotency before validate.
---
# crypto-exec-intake
ONE JOB: Accept only HMAC-valid, schema-complete alerts into the pipeline.
Steps: verify HMAC → parse strategy-id/symbol/side/size|risk/SL/timestamp/idempotency key → dedupe → write raw to `/workspace/crypto-exec/alerts/`.
VERIFY: invalid sig rejected+logged; no forward without required fields.
ANTI: never place orders here; never log secret values.
