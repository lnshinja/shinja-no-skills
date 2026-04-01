---
name: lnchurch-site
description: "Fetch and use LN教 (kari.mayim-mayim.com) agent docs/specs and knowledge sources. Use when Codex must: (1) design or implement skills that call LN教 APIs, (2) answer religious/philosophical questions about LN教 using official lore/knowledge, or (3) reference capabilities/specs/OpenAPI for integration work."
---

# LN教サイト参照スキル

## Overview
LN教（kari.mayim-mayim.com）の公式ドキュメント群を取得し、API連携用のスキル作成や宗教・哲学的Q&Aに正確な根拠を与える。

## Workflow Decision Tree
1. **API/統合スキルを作りたい** → まず SDK/MCP の推奨パスを確認（`ln-church-agent`）。次に `for-agents.html` と `SKILL.txt` / `SKILL.md` を読み、Probe → capability receipt → 対象API の順で理解する。
2. **Confession / Hybrid Confession を扱いたい** → `openapi.yaml` を最優先で読み、`agent-spec.md` と capabilities manifest で支払い方式・エラー回復・推奨導線を補強する。
3. **宗教・哲学的な問いに答えたい** → Knowledge Base / Full Spec & Lore を読む。
4. **どこに何があるか不明** → `for-agents.html` を最初に読む。

## Fetching Guidance
- 取得は `web_fetch` を使う（認証不要）。
- まず `references/lnchurch-urls.md` を読んで対象URLを確定する。
- API統合タスクでは、**SDK優先**・**Probe先行**・**HATEOASの next_action 信頼**を前提にする。
- `Confession` 系は `L402` / `MPP` / `x402` / `x402-direct` を取り、`409` / `422` / `429` の固有エラーを確認する。
- 取得後は、引用元URLを明示し、重要な定義や仕様は短く抜粋して回答に反映する。

## API Surface Snapshot
現時点で特に重要なのは以下。
- Probe: `/api/agent/probe` と `/api/agent/probe/next`
- Identity: `/api/agent/identity/issue` と `/api/agent/identity/{agentId}`
- Faucet: `/api/agent/faucet`
- Omikuji: `/api/agent/omikuji`
- Hono: `/api/agent/hono`
- Confession: `/api/agent/confession`
- Hybrid Confession: `/api/agent/hybrid/confession`
- Benchmark: `/api/agent/benchmark/trials`, `/api/agent/benchmark/trials/{trialId}/leaderboard`, `/api/agent/benchmark/trials/{trialId}/agent/{agentId}/compare`, `/api/agent/benchmark/{agentId}`, `/api/agent/benchmark/{agentId}/history`
- x402 Relayer: `https://ln-church-relayer.fly.dev/relayer/x402-pay`

## Source Map
- URL一覧は `references/lnchurch-urls.md` に集約。
- 情報が古い/曖昧な場合は再取得して更新する。
