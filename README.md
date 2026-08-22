<div align="center">

# 🗄️ AI API Pricing Database

**Every AI model price, verified and traceable — from DeepSeek to OpenAI, subscriptions included.**

[![Platforms](https://img.shields.io/badge/platforms-92-blue)](#-data-overview)
[![Models](https://img.shields.io/badge/models-581-green)](#-data-overview)
[![Pricing rows](https://img.shields.io/badge/API_prices-1,323-orange)](#-data-overview)
[![Plans](https://img.shields.io/badge/subscriptions-194-purple)](#-data-overview)
[![Verified](https://img.shields.io/badge/officially_verified-55%E2%9C%93-brightgreen)](#-methodology)
[![Updated](https://img.shields.io/badge/updated-2026--08--22-yellow)](#-changelog)
[![License](https://img.shields.io/badge/License-MIT-informational)](LICENSE)

[🌐 Interactive Explorer](#-interactive-explorer) · [Quick Start](#-quick-start) · [Schema](#-schema) · [Methodology](#-methodology) · [中文文档](README.zh-CN.md)

<a href="https://moyu-good.github.io/llm-price-atlas/"><img src="docs/explorer_screenshot.png" alt="AI Price Atlas — Interactive Explorer" width="100%"></a>

**▶ [Open the live interactive explorer — no install, works on mobile](https://moyu-good.github.io/llm-price-atlas/)**

</div>

---

A single SQLite database covering **API token pricing, subscription plans, plan→model matrices, and API endpoint metadata** across 92 providers — with dual timestamps on every row so you can replay price history instead of guessing.

Unlike scraped-and-forgotten pricing lists, every change here is **verified against live sources** (OpenRouter diffing API, Firecrawl-rendered official pages) and **attributed** (`source_url` + audit notes on every mutation).

## ✨ Highlights

- 🏬 **Chinese AI providers, fully covered** — DeepSeek (incl. peak/off-peak cache pricing), Zhipu GLM, Moonshot Kimi, MiniMax, Doubao/Ark, Qwen/Bailian, Baidu Qianfan, SiliconFlow — alongside OpenAI / Anthropic / Google / xAI / Mistral / Groq / Together…
- 💳 **Subscriptions, not just tokens** — 194 plans from ChatGPT Go→Pro, Claude Pro→Max 20x, GitHub Copilot's 7 tiers with per-tier model matrices, Kimi Code, Cursor, Trae, ElevenLabs
- 🧠 **Plan → model mapping** — which models each tier unlocks (e.g. Copilot Pro+ adds `Opus 4.7+/Fable 5/GPT-5.4-nano`)
- 🔌 **API endpoint triplets** — docs URL, base URL, and OpenAI-compatibility notes for 21 platforms
- ⏱️ **Dual timestamps** — `collected_at` + `effective_at` on every price; CNY↔USD dual currency with fixed FX rate kept in a column
- 🔍 **Audit trail** — every correction appends date + action + original value to `notes`; rendered snapshots of official pages archived under [`data/fc/`](data/fc/)

## 📊 Data Overview

| Table | Rows | Content |
|---|---|---|
| `platforms` | 92 | Providers + API triplet (docs / base_url / compatibility) |
| `models` | 581 | Model catalog incl. context windows |
| `pricing` | 1,323 | Per-token prices: input/output/cache-hit/range, USD+CNY |
| `plans` | 194 | Subscriptions: price, quota, **models_included**, source URL |

## 🌐 Interactive Explorer

The repo ships a zero-dependency single-file app — **[`index.html`](index.html)** — with the full dataset embedded (works offline):

```bash
open index.html   # macOS    |    start index.html   # Windows
```

- 💰 **API prices**: full-text search + platform/type filters + sortable columns across 1,323 rows
- 📦 **Subscriptions**: collapsible cards per provider showing quota & unlocked models per tier
- 🔌 **API access**: copy BaseURL with one click, jump straight to official docs

Also perfect for hosting: enable GitHub Pages on `master` root and you're done.

## 🚀 Quick Start

```sql
-- Cheapest input+output text models right now
SELECT model_name, platform,
       SUM(CASE WHEN item_type LIKE '输入%' THEN price_usd END) AS in_$,
       SUM(CASE WHEN item_type='输出' THEN price_usd END)      AS out_$
FROM pricing WHERE price_usd > 0
GROUP BY platform, model_name
HAVING in_$ IS NOT NULL AND out_$ IS NOT NULL
ORDER BY in_$ + out_$ ASC LIMIT 10;
```

```python
import sqlite3
db = sqlite3.connect("api_cost.db")
# All channels selling deepseek-v4-pro, newest effective prices only
for r in db.execute("""
    SELECT p.name, pr.item_type, pr.price_usd, pr.source_url
    FROM pricing pr JOIN platforms p ON p.id = pr.platform_id
    WHERE pr.model_name LIKE '%deepseek-v4-pro%'
      AND pr.effective_at <= date('now')"""):
    print(r)
```

## 📐 Schema

```
platforms 1 ──┬── n models     (catalog)
              ├── n pricing    (per-token prices w/ source_url)
              └── n plans      (subscriptions w/ models_included)

Key conventions:
  pricing.collected_at / effective_at   collection vs. effective time
  pricing.price_usd / price_cny         dual currency (fx=7.1, fx_rate kept per row)
  pricing.peak/offpeak_price_cny        DeepSeek off-peak system
  plans.models_included                 models unlocked by this tier
  platforms.api_docs_url / api_base_url API docs & endpoint
```

## 🔍 Methodology

| Layer | Technique | Coverage |
|---|---|---|
| L1 Full diff | OpenRouter `/api/v1/models` live API, row-by-row compare | 1,033 rows (81%) |
| L2 Official pages | Firecrawl-rendered JS pages + manual verification | Anthropic, OpenAI, DeepSeek, xAI, Google, ElevenLabs, Kimi, Zhipu, Trae, Windsurf… |
| L3 Source hygiene | Every plan carries an official URL; blog/YouTube sources purged | 194/194 |

Full audit trail: [`data/verify_report_2026-08-22.md`](data/verify_report_2026-08-22.md)

## 📅 Changelog

| Date | Notes |
|---|---|
| **2026-08-22** | Full verification round: prices 1,278→1,323; plans 178→194 (100% sourced); added API triplets & model matrices; fixed 9 data defects incl. phantom "Opus 4.7 Fast" tier, ElevenLabs Creator halved to $11, Trae currency mix-up |
| 2026-08-17 | Snapshot: 84 platforms / 571 models / 1,266 prices / 164 plans |

## ⚠️ Disclaimer

This is a **verified snapshot**, not a live feed — always check `effective_at` before relying on a price. CNY values use a fixed FX rate; actual billing follows each provider's currency. Peak/off-peak fields are defined only within DeepSeek's official system.

## License

[MIT](LICENSE) © 2026
