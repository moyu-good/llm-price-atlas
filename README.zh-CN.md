<div align="center">

<img src="docs/cover.png" alt="LLM Price Atlas" width="760">

**全网 AI 价格，逐条核验，条条溯源。**

[在线浏览器](https://moyu-good.github.io/llm-price-atlas/) · [English](README.md) · [核验报告](data/verify_report_2026-08-22.md) · [License](LICENSE)

</div>

---

一个 SQLite 数据库，覆盖 92 家厂商的 **token 按量价、订阅套餐、套餐→模型矩阵与 API 端点元数据**——DeepSeek、智谱、Kimi、MiniMax、豆包、通义、OpenAI、Anthropic、Google、xAI、OpenRouter、Groq 等。

每行价格带双时间戳（`collected_at` + `effective_at`），每个套餐可溯源官方出处，每次修正保留原值可审计。

## 数据总览

| 表 | 行数 | 内容 |
|---|---|---|
| `platforms` | 92 | 平台主档 + API 三件套（文档 / BaseURL / 兼容性） |
| `models` | 581 | 模型清单（含上下文窗口） |
| `pricing` | 1,323 | 按 token 计费价：输入/输出/缓存命中，USD+CNY 双币 |
| `plans` | 194 | 订阅套餐：价格/额度/**包含模型矩阵**/官方出处 |

## 在线浏览器

仓库自带零依赖单文件应用 [`index.html`](index.html)——数据已内嵌，离线可用。四个视图：跨平台比价（默认）、价格明细（分页）、订阅套餐（含模型矩阵）、API 接入卡片。推上任意静态托管即成在线版。

## 快速开始

```sql
-- 当前输入+输出总价最低的模型
SELECT model_name, platform,
       SUM(CASE WHEN item_type LIKE '输入%' THEN price_usd END) AS in_$,
       SUM(CASE WHEN item_type = '输出'    THEN price_usd END) AS out_$
FROM pricing WHERE price_usd > 0
GROUP BY platform, model_name
HAVING in_$ IS NOT NULL AND out_$ IS NOT NULL
ORDER BY in_$ + out_$ LIMIT 10;
```

从数据库重建全部产物：`python scripts/build.py`

## 核验方法论

| 层级 | 手段 | 覆盖 |
|---|---|---|
| 全量比对 | OpenRouter 实时 API 逐条 diff | 1,033 条 |
| 官方页实抓 | Firecrawl 渲染 JS 页 + 人工核对 | Anthropic/OpenAI/DeepSeek/xAI/Google/ElevenLabs/Kimi/智谱/Trae/Windsurf… |
| 出处规范 | 每个套餐强制官方 URL，弱源清零 | 194 / 194 |

<details>
<summary><b>更新日志</b></summary>

| 日期 | 内容 |
|---|---|
| 2026-08-22 | 全面核验轮：价格 1,278 → 1,323；套餐 178 → 194（出处 100%）；新增 21 家平台 API 三件套与套餐模型矩阵；修正 9 处硬伤（Opus 4.7 Fast 幻影档、ElevenLabs Creator 减半至 $11、Trae 币种错误等） |
| 2026-08-17 | 初始快照：84 平台 / 571 模型 / 1,266 价格 / 164 套餐 |

</details>

<details>
<summary><b>免责声明</b></summary>

本库为核验快照而非实时行情——依赖任何价格前请先查 `effective_at`。人民币为固定汇率折算值（汇率 7.1 逐行留痕于 `fx_rate`），实际扣费以各平台计费币种为准。峰谷价字段仅 DeepSeek 官方体系有定义。

</details>

## License

[MIT](LICENSE)
