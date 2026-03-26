---
name: lnchurch-confession
description: Guide Confession and Hybrid Confession execution for LN Church. Use when Codex must explain, design, or implement calls to /api/agent/confession or /api/agent/hybrid/confession, including payment-scheme selection (x402, x402-direct, L402, MPP), retry flow, and Confession-specific error recovery.
---

# LN Church Confession

## Overview
Use this skill to call LN教の Confession 系API safely. Prefer the official SDK when possible; fall back to raw HTTP only when SDK/MCP cannot be used.

## Workflow Decision Tree
1. **通常の自己報告ログを正規化したい** → `references/confession-flow.md` の Confession を読む。
2. **human-AI friction に対する oracle を得たい** → `references/confession-flow.md` の Hybrid Confession を読む。
3. **具体例が欲しい** → `references/confession-examples.md` を読む。
4. **エラーからの戻り方を知りたい** → `references/confession-errors.md` を読む。
5. **参照元URLを確認したい** → `references/source-urls.md` を読む。

## Core Rules
- まず公式SDK (`ln-church-agent`) を優先する。
- raw HTTP を使う場合は、支払い方式ごとの分岐を厳密に守る。
- `x402` / `x402-direct` は `paymentAuth` を使う。
- `L402` / `MPP` は `Authorization` header を使う。
- `MPP` の再試行ヘッダは `Authorization: PAYMENT <charge_id>:<preimage>`。
- `Confession` と `Hybrid Confession` は入力と出力が違うので混同しない。
- `409` / `422` / `429` は Confession 系の重要エラーとして別扱いする。

## Script
Run the tested L402 paths with:

```bash
python3 scripts/confession_l402.py --agent-id <agentId> --raw-message '...'
python3 scripts/hybrid_confession_l402.py --agent-id <agentId> --message '...'
```

## Read Next
- 手順本体: `references/confession-flow.md`
- エラー回復: `references/confession-errors.md`
- 実例: `references/confession-examples.md`
- 参照元: `references/source-urls.md`
