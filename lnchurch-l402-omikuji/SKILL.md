---
name: lnchurch-l402-omikuji
description: "Execute LN教 (kari.mayim-mayim.com) Omikuji over the HTTP 402/L402 flow using Probe API plus direct lnd REST invoice payment. Use when Codex needs to call the LN教 Omikuji API without lnget, validate L402 behavior end to end, or build automations that pay LN invoices through lnd REST and retry with an Authorization header."
---

# LN教 L402 Omikuji

## Overview
LN教のおみくじAPIを、`Probe → 402 challenge → lnd RESTでinvoice支払い → Authorization付き再POST` の順で実行する。

## Quick start
1. Read `references/flow.md`.
2. Use `scripts/omikuji_l402.py`.
3. Pass `--agent-id` explicitly.
4. Keep `--max-cost` small for tests (default `10`).

## Execution rules
- 最初に Probe API を通す。
- 最初の `/api/agent/omikuji` は `scheme=L402` `asset=SATS` で POST する。
- 402 を受けたら `WWW-Authenticate` から `macaroon` と `invoice` を抜く。
- invoice は **lnd REST** で払う。`lncli` にはフォールバックしない。
- 再POSTでは **同じ JSON body** を使い、`Authorization: L402 <macaroon>:<preimage>` を追加する。
- `receipt.verify_token` を保存価値のある実行証明として扱う。

## Inputs
- Required: `agentId`
- Optional:
  - `max_cost` (default `10`)
  - `fee_limit_sat` (default `1`)
  - `probe_source`
  - `api_base`
  - `lnd_rest_url`
  - `lnd_tls_cert`
  - `lnd_macaroon_file`

## Script
Run:

```bash
python3 scripts/omikuji_l402.py --agent-id <agentId> --max-cost 10
```

Sensitive values (`probe_token`, `invoice`, `payment_preimage`) are hidden by default. Add `--show-sensitive` only for local debugging.

Environment overrides:
- `LND_REST_URL`
- `LND_TLS_CERT`
- `LND_MACAROON_FILE`

Avoid `--insecure` outside local troubleshooting. Prefer verified TLS in normal use.

## Output
The script prints JSON containing:
- `challenge_amount_sat`
- `payment.status`
- `payment.payment_hash`
- `omikuji.result`
- `omikuji.receipt.verify_token`

Only when `--show-sensitive` is set:
- `probe_token`
- `invoice`
- `payment.payment_preimage`

## Resources
- Protocol summary: `references/flow.md`
- Executor: `scripts/omikuji_l402.py`
