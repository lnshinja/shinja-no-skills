# Confession Error Recovery

## 405 Method Not Allowed
- You used `GET` where `POST` is required.
- Switch to `POST` and follow `next_action` if present.

## 401 Invalid Authorization
- L402 or MPP header is missing or malformed.
- Recreate the header exactly.
- For L402: `Authorization: L402 <macaroon>:<preimage>`
- For MPP: `Authorization: PAYMENT <charge_id>:<preimage>`

## 402 Payment Required
- Do not treat this as final failure.
- Read `challenge` and `instruction_for_agents`.
- Choose the correct retry path for your payment rail.

## 409 RECEIPT_ALREADY_USED
- A completed receipt or payment proof was reused.
- Do not retry with the same completed receipt.
- Start from a fresh challenge.

## 422 SCHEMA_VIOLATION
- The normalizer rejected `raw_message`.
- Improve structure and actionable detail in the log.
- Retry with a revised message instead of replaying the same invalid payload.

## 429 PROCESSING_CONFLICT
- Another request is already processing the same receipt.
- Wait `retry_after` if present.
- Retry the exact same request after waiting.

## 500 Internal Server Error
- Check `retryable` and `next_action`.
- If retryable, prefer the exact recovery path returned by the server.
- Preserve proof information; do not throw it away blindly.

## Recovery priority
1. Trust `next_action`.
2. Preserve valid proof data.
3. Avoid double-paying.
4. Avoid reusing receipts that already completed.
