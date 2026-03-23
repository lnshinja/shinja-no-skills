# LN Church L402 Omikuji flow

## Purpose
Execute LN Church Omikuji over HTTP 402/L402 without `lnget`, using direct HTTP calls plus lnd REST payment.

## Flow
1. `GET /api/agent/probe?src=<source>&agentId=<agentId>`
2. Follow `next_action.url`
3. Extract `capability_receipt.token`
4. `POST /api/agent/omikuji` with:
   - `Content-Type: application/json`
   - `x-probe-token: <token>`
   - body:
     ```json
     {
       "agentId": "<agentId>",
       "clientType": "AI",
       "scheme": "L402",
       "asset": "SATS"
     }
     ```
5. Expect `402 Payment Required`
6. Parse `WWW-Authenticate` for:
   - `macaroon`
   - `invoice`
7. Pay the invoice via lnd REST `POST /v2/router/send`
8. Re-POST the exact same body with:
   - `Authorization: L402 <macaroon>:<preimage>`
   - `x-probe-token: <token>`
9. Store `receipt.verify_token`

## Important constraints
- Enforce a `max_cost` guard before payment.
- Keep `scheme=L402` and `asset=SATS` unchanged between initial request and retry.
- Do not add `paymentAuth` for L402 retries.
- Prefer lnd REST over `lncli` when both are available.

## Tested endpoints
- LN Church API base: `https://kari.mayim-mayim.com`
- Omikuji path: `/api/agent/omikuji`
- Probe path: `/api/agent/probe`
- lnd REST status check: `GET https://localhost:8080/v1/getinfo`
- lnd REST pay endpoint: `POST https://localhost:8080/v2/router/send`
