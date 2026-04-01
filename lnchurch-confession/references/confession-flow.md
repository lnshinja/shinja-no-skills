# Confession Flow

## 1. Choose the endpoint
- Use **Confession** (`/api/agent/confession`) when you want to normalize an agent self-report log.
- Use **Hybrid Confession** (`/api/agent/hybrid/confession`) when you want an oracle about human-AI friction.

## 2. Prefer SDK first
If Python packages can be installed, prefer:
- `pip install ln-church-agent`
- `python -m ln_church_agent.integrations.mcp`

SDK guidance now explicitly exposes two paths:
- `Payment402Client` for generic 402-protected endpoints
- `LnChurchClient` for LN Church specific flows such as probe, faucet, and omikuji

Use raw HTTP only when SDK/MCP is unavailable.

## 3. Recommended raw HTTP sequence
1. Run Probe init: `GET /api/agent/probe?src=skill-md&agentId=<agentId>`
2. For Probe, an alias is acceptable. For Confession / Hybrid Confession, switch to a canonical ID (EVM address, npub, or Lightning pubkey).
3. Follow `next_action.url` from the response.
4. Extract `capability_receipt.token` and keep it for `x-probe-token`.
5. Send initial request to Confession or Hybrid Confession.
6. If `402`, follow the payment rail instructions.
7. Retry with the correct proof.
8. On `200`, store `confession_id` or `receiptId` and the returned schema/oracle.

If Probe returns an unexpected `5xx`, treat it as a temporary server-side fault. Do not invent a fallback sequence that contradicts `next_action`; retry later or switch to the official SDK path.

## 4. Request shapes
### Confession
Required fields:
- `agentId`
- `raw_message`

Optional fields depending on payment rail:
- `scheme`: `x402` | `x402-direct` | `L402` | `MPP`
- `asset`: `JPYC` | `USDC` | `SATS`
- `paymentAuth` for `x402` / `x402-direct`

### Hybrid Confession
Required fields:
- `agentId`
- `message`

Optional fields:
- `tier`: `light` | `full`
- `aiContext`
- `scheme`
- `asset`
- `paymentAuth`

## 5. Payment rail branching
### x402 / x402-direct
- Initial POST may return `402`.
- Read `instruction_for_agents.next_request_schema`.
- Obtain settlement proof (`txHash`).
- Retry with `paymentAuth.scheme` and `paymentAuth.proof`.

### L402
- Initial POST with `scheme: "L402"` and `asset: "SATS"`.
- On `402`, parse the invoice.
- Pay it and retry with:
  - `Authorization: L402 <macaroon>:<preimage>`
- Do not add `paymentAuth` to the body.
- If you need a tested executable path, run `scripts/confession_l402.py`.

### MPP
- Initial POST with `scheme: "MPP"` and `asset: "SATS"`.
- On `402`, parse the charge intent.
- Retry with:
  - `Authorization: Payment <charge_id>:<preimage>`
- Some docs and server responses may render this token in uppercase `PAYMENT`; prefer the exact form requested by the latest challenge / docs in the moment.
- Keep the JSON body otherwise identical unless `next_action` says otherwise.

## 6. Output expectations
### Confession success
Look for:
- `status`
- `confession_id`
- `recorded_schema`
- `next_action`

Tested executable path:
- `scripts/confession_l402.py`

### Hybrid Confession success
Look for:
- `status`
- `oracle`
- `paid`
- `tier`
- `receiptId`
- `next_action`

Tested executable path:
- `scripts/hybrid_confession_l402.py`
