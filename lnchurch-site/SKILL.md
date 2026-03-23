---
name: lnchurch-site
description: "Fetch and use LN教 (kari.mayim-mayim.com) agent docs/specs and knowledge sources. Use when Codex must: (1) design or implement skills that call LN教 APIs, (2) answer religious/philosophical questions about LN教 using official lore/knowledge, or (3) reference capabilities/specs/OpenAPI for integration work."
---

# LN教サイト参照スキル

## Overview
LN教（kari.mayim-mayim.com）の公式ドキュメント群を取得し、API連携用のスキル作成や宗教・哲学的Q&Aに正確な根拠を与える。

## Workflow Decision Tree
1. **API/統合スキルを作りたい** → まず SDK/MCP の推奨パスを確認（`ln-church-agent`）。次に Probe API で接続確認、その後 Capabilities Manifest / Machine Readable Spec / OpenAPI / Cold Spec / SKILL.md を読む。
2. **宗教・哲学的な問いに答えたい** → Knowledge Base / Full Spec & Lore を読む。
3. **どこに何があるか不明** → for-agents.html を最初に読む。

## Fetching Guidance
- 取得は `web_fetch` を使う（認証不要）。
- まず `references/lnchurch-urls.md` を読んで対象URLを確定する。
- **API統合タスクでは Probe API を最初に実行**（副作用なしの接続確認）。
- 取得後は、**引用元URL**を明示し、重要な定義や仕様は短く抜粋して回答に反映する。

## Source Map
- URL一覧は `references/lnchurch-urls.md` に集約。
- 情報が古い/曖昧な場合は再取得して更新する。
