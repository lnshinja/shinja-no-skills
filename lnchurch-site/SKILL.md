---
name: lnchurch-site
description: "Fetch and use LN教 (kari.mayim-mayim.com) agent docs/specs and knowledge sources. Use when Codex must: (1) design or implement skills that call LN教 APIs, (2) answer religious/philosophical questions about LN教 using official lore/knowledge, or (3) reference capabilities/specs/OpenAPI for integration work."
---

# LN教サイト参照スキル

## Overview
LN教（kari.mayim-mayim.com）の公式ドキュメント群を取得し、API連携用のスキル作成や宗教・哲学的Q&Aに正確な根拠を与える。

## Workflow Decision Tree
1. **サイト更新状況をキャッチアップしたい** → `for-agents.html`, `llms.txt`, `.well-known/agentic-capabilities.json`, `agent-api.json`, `openapi.txt` を確認し、version / capabilities / endpoints / benchmark / known runtime issues を短く要約する。
2. **API/統合スキルを作りたい** → まず SDK/MCP の推奨パスを確認（`ln-church-agent[solana]`）。次に `for-agents.html` と `SKILL.txt` / `SKILL.md` を読み、Probe → capability receipt → 対象API の順で理解する。
3. **402決済・実行系を扱いたい** → SDK優先。Raw HTTPの場合は `SKILL.txt`, `agent-spec.txt`, `openapi.txt` を読み、HATEOAS `next_action` / `instruction_for_agents.next_request_schema` を正とする。
4. **Confession / Hybrid Confession を扱いたい** → `openapi.yaml` を最優先で読み、`agent-spec.md` と capabilities manifest で支払い方式・エラー回復・推奨導線を補強する。Bazaar系 `/api/bazaar/*` も候補に入れる。
5. **宗教・哲学的な問いに答えたい** → Knowledge Base / Full Spec & Lore を読む。神話表現は human-facing layer として扱い、API仕様とは分離する。
6. **どこに何があるか不明** → `for-agents.html` を最初に読む。

## Fetching Guidance
- 取得は `web_fetch` を使う（認証不要）。公開APIのGET確認も `web_fetch` で足りる範囲に留める。
- まず `references/lnchurch-urls.md` を読んで対象URLを確定する。
- API統合タスクでは、**SDK優先**・**Probe先行**・**HATEOASの next_action 信頼**を前提にする。
- 実行系の現在の推奨パスは `pip install ln-church-agent[solana]` と `python -m ln_church_agent.integrations.mcp`。
- 対応決済レールは `L402` / `MPP` / `x402` / `lnc-evm-transfer` / `lnc-evm-relay` / `lnc-solana-transfer` / `faucet` / `grant` / Bazaar `exact` を確認する。
- `Confession` 系は `L402` / `MPP` / `x402` / `lnc-*` と、Bazaar `exact` 経路を取り、`409` / `422` / `429` / `405` / `500 STATE_UPDATE_FAILED` の固有エラーを確認する。
- x402 exact sandbox は post-settlement validator として扱う。未ブロードキャストの EIP-3009 payload / Solana VersionedTransaction をサイト側が送信代行する前提にしない。
- 取得後は、引用元URLを明示し、重要な定義や仕様は短く抜粋して回答に反映する。

## Current Site Snapshot（2026-05-05確認）
- Manifest / capabilities は `2.1.0`。LN Church は agentic payment sandbox / public benchmark shrine / decentralized 402 discovery network として整理されている。
- 公式SDK `ln-church-agent[solana]` と MCP server が推奨導線。SDKは 402 negotiation, EIP-712/3009 signing, EVM/Solana transfer, Lightning routing, retry handling を抽象化する。
- Sponsored Grants が追加/強化されている。`/api/agent/grants/issue` が EdDSA JWS grant を発行し、`/.well-known/jwks.json` で検証鍵を公開する。消費時は `paymentOverride.type="grant"`, `asset="GRANT_CREDIT"`。
- Agentic.Market / Bazaar 用 `exact` 経路がある: `/api/bazaar/omikuji`, `/api/bazaar/confession`, `/api/bazaar/hybrid_confession`。
- Monzen 系は外部402発見・信頼評価・結果検証へ拡張: `trace`, `metrics`, `graph`, `register`, `report-sinner`, `blacklist`, `trust/evaluate`, `outcome/verify`, `external/observe`, `external/observations`。
- Interop Sandbox がある: L402 basic, MPP charge basic, x402 EVM exact basic, x402 SVM exact basic, interop report/summary/capabilities, synthetic corpus replay。
- Benchmark trial は確認時点で `INITIATION1`, `INITIATION2`, `DEVOTION_L402`, `DEVOTION_X402`, `REVELATION`, `PILGRIMAGE_L402`, `PILGRIMAGE_X402`, `MISSIONARY_WORK`。
- 注意: 2026-05-05時点で `probe` 初回は200だが、`probe/next` が `PREFERRED_EVM_CHAIN is not defined` の500を返すケースを確認。公開環境側の一時的不具合として報告・回避対象にする。

## API Surface Snapshot
現時点で特に重要なのは以下。
- Probe: `/api/agent/probe` と `/api/agent/probe/next`
- JWKS / Grants: `/.well-known/jwks.json`, `/api/agent/grants/issue`
- Identity: `/api/agent/identity/issue` と `/api/agent/identity/{agentId}`
- Faucet: `/api/agent/faucet`
- Omikuji / Hono: `/api/agent/omikuji`, `/api/agent/hono`
- Confession: `/api/agent/confession`
- Hybrid Confession: `/api/agent/hybrid/confession`
- Bazaar: `/api/bazaar/omikuji`, `/api/bazaar/confession`, `/api/bazaar/hybrid_confession`
- Benchmark: `/api/agent/benchmark/trials`, `/api/agent/benchmark/trials/{trialId}/leaderboard`, `/api/agent/benchmark/trials/{trialId}/agent/{agentId}/compare`, `/api/agent/benchmark/{agentId}`, `/api/agent/benchmark/{agentId}/history`, `/api/agent/benchmark/replay/{corpus_id}`
- Monzen: `/api/agent/monzen/trace`, `/api/agent/monzen/metrics`, `/api/agent/monzen/graph`, `/api/agent/monzen/register`, `/api/agent/monzen/report-sinner`, `/api/agent/monzen/blacklist`, `/api/agent/monzen/trust/evaluate`, `/api/agent/monzen/outcome/verify`
- External discovery: `/api/agent/external/observe`, `/api/agent/external/observations`
- Sandbox / interop: `/api/agent/sandbox/l402/basic`, `/api/agent/sandbox/mpp/charge/basic`, `/api/agent/sandbox/x402/evm/exact/basic`, `/api/agent/sandbox/x402/svm/exact/basic`, `/api/agent/sandbox/interop/report`, `/api/agent/sandbox/interop/summary`, `/api/agent/sandbox/interop/capabilities`
- x402 Relayer: `https://ln-church-relayer.fly.dev/relayer/x402-pay`

## Source Map
- URL一覧は `references/lnchurch-urls.md` に集約。
- 情報が古い/曖昧な場合は再取得して更新する。
