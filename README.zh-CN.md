<div align="center">

[English](README.md) | 简体中文

# 🗄️ AI 模型价格库 · AI API Pricing Database

**全网 AI 模型 / API / 套餐价格数据库 — 每条价格可溯源，每个套餐可对账**

[![Platforms](https://img.shields.io/badge/平台-92-blue)](#-数据总览)
[![Models](https://img.shields.io/badge/模型-581-green)](#-数据总览)
[![Pricing](https://img.shields.io/badge/按量价-1,323-orange)](#-数据总览)
[![Plans](https://img.shields.io/badge/订阅套餐-194-purple)](#-数据总览)
[![Verified](https://img.shields.io/badge/官方实核-55✓-brightgreen)](#-核验方法论)
[![Updated](https://img.shields.io/badge/更新-2026--08--22-yellow)](#-更新日志)
[![License](https://img.shields.io/badge/License-MIT-informational)](LICENSE)

[🌐 在线浏览器](#-交互式浏览器) · [快速开始](#-快速开始) · [数据模型](#-数据模型) · [核验方法论](#-核验方法论) · [更新日志](#-更新日志)

</div>

---

## ✨ 为什么用这个库

- **全**：国内大厂（DeepSeek/智谱/Kimi/MiniMax/豆包/百炼/千帆）+ 海外（OpenAI/Anthropic/Google/xAI）+ 聚合网关（OpenRouter/Groq/Together）+ 编程工具（Cursor/Copilot/Trae）+ 视频图像（Kling/Pika/Firefly），一库打尽
- **新**：每条记录双时间戳 —— `collected_at` 采集时间 + `effective_at` 价格生效时间，历史可回放
- **准**：2026-08-22 全量核验 —— OpenRouter API 逐条比对 1,033 条 + 官方页实抓修正（详见[核验报告](data/verify_report_2026-08-22.md)）
- **殷实**：不止价格 —— 套餐→包含模型矩阵、API 端点三件套（文档/BaseURL/兼容性）、峰谷价、缓存价、批量价

## 📊 数据总览

| 表 | 行数 | 内容 |
|---|---|---|
| `platforms` | 92 | 平台主档 + **API 三件套**（文档地址/BaseURL/OpenAI兼容性） |
| `models` | 581 | 模型清单（含上下文窗口） |
| `pricing` | 1,323 | 按 token 计费价：输入/输出/缓存命中/区间价，USD+CNY 双币 |
| `plans` | 194 | 订阅套餐：价格/额度/**包含模型矩阵**/官方出处 |

<details>
<summary><b>📦 套餐覆盖亮点</b>（点击展开）</summary>

| 类别 | 代表条目 |
|---|---|
| 编程订阅 | Claude Pro $17 / Max 5x $100 / 20x $200 · Cursor Pro $20/Ultra $200 · Copilot 七档(Pro+/Max 含 Credits 明细) · Kimi Code 四档(Moderato~Vivace) · GLM Coding 三档 · Trae 四档 |
| C端会员 | ChatGPT Go/Plus/Pro($100起) · Google AI Plus/Pro/Ultra 5x·20x · Kimi K3 会员 |
| 音视频 | ElevenLabs 六档(Creator 刚降价至$11) · Kling 会员 · Sora/Veo 按秒价 |
| API资源包 | MiniMax 语音包六档 · DeepSeek 峰谷价体系 |

</details>

## 🌐 交互式浏览器

仓库根目录的 **[`index.html`](index.html)** 是零依赖单文件应用（数据已内嵌，离线可用）：

```bash
# 直接打开
start index.html        # Windows
open index.html         # macOS
```

三大视图：

| 视图 | 能力 |
|---|---|
| 💰 **模型 API 价格** | 全文搜索 + 平台/类型筛选 + 点列排序，1323 条秒查 |
| 📦 **订阅套餐** | 按平台分组折叠卡片，每档展示额度与**包含模型** |
| 🔌 **API 接入** | 各家 BaseURL 一键复制 + 文档直链 + 兼容性说明 |

> 部署到 GitHub Pages 即得在线版；数据更新后重跑 `scripts_export_json.py` + 注入脚本即可再生成。

## 🚀 快速开始

**SQL**（比谁便宜）：

```sql
-- 输入+输出总价最低的前 10 个"标准档"文本模型
SELECT model_name, platform,
       SUM(CASE WHEN item_type LIKE '输入%' THEN price_usd END) AS in_$,
       SUM(CASE WHEN item_type='输出' THEN price_usd END) AS out_$
FROM pricing WHERE price_usd > 0
GROUP BY platform, model_name
HAVING in_$ IS NOT NULL AND out_$ IS NOT NULL
ORDER BY in_$ + out_$ ASC LIMIT 10;
```

**Python**（找某模型的全部报价渠道）：

```python
import sqlite3
db = sqlite3.connect("api_cost.db")
for r in db.execute("""
    SELECT p.name, pr.item_type, pr.price_usd, pr.source_url
    FROM pricing pr JOIN platforms p ON p.id = pr.platform_id
    WHERE pr.model_name LIKE '%deepseek-v4-pro%'
      AND pr.effective_at <= date('now')"""):
    print(r)
```

## 📐 数据模型

```
platforms 1 ──┬── n models          （模型清单）
              ├── n pricing         （按量价，quote 可溯源 source_url）
              └── n plans           （订阅套餐，models_included 模型矩阵）

关键字段约定：
  pricing.collected_at / effective_at   双时间戳（采集/生效）
  pricing.price_usd + price_cny         双币（fx=7.1 折算，fx_rate 留痕）
  pricing.peak/offpeak_price_cny        峰谷价（DeepSeek 体系）
  plans.models_included                 该套餐可用的模型清单
  platforms.api_docs_url/base_url       API 文档与端点
```

## 🔍 核验方法论

| 层级 | 手段 | 覆盖 |
|---|---|---|
| L1 全量比对 | OpenRouter `/api/v1/models` 实时 API 逐条 diff | 1,033 条（81%） |
| L2 官方页实抓 | Firecrawl 渲染 JS 页 + 人工核对 | Anthropic/OpenAI/DeepSeek/xAI/Google/ElevenLabs/Kimi/智谱/Trae/Windsurf… |
| L3 出处规范 | 每条套餐强制官方 URL，糊弄源（youtube/自媒体）清零 | 194/194 |

- 每次修改在 `notes` 追加 `日期+动作+原值`，**可追溯可回滚**
- 官方渲染快照存档于 [`data/fc/`](data/fc/)（20 个平台）
- 完整核验过程：[`data/verify_report_2026-08-22.md`](data/verify_report_2026-08-22.md)

## 📅 更新日志

| 日期 | 内容 |
|---|---|
| **2026-08-22** | 全面核验轮：价格 1,278→1,323；套餐 178→194（出处 100%）；新增 API 三件套与模型矩阵；发现并修正 Opus4.7-Fast 幻影档 / ElevenLabs Creator 减半 / Trae 币种错误等 9 处硬伤 |
| 2026-08-17 | 快照：84 平台 / 571 模型 / 1,266 价格 / 164 套餐；币种统一双币 fx=7.1 |

## ⚠️ 免责声明

- 价格以各官方页为准，本库为**采集快照**（非实时）；使用前请核对 `effective_at`
- CNY 为固定汇率折算值，实际扣费以平台计费币种为准
- 峰谷价仅 DeepSeek 官方体系有定义，其他平台的该字段为空

## License

[MIT](LICENSE) © 2026
