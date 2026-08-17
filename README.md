# AI 模型价格库 · AI API Pricing Database

> **全网 AI 模型 / API / 套餐价格数据库** — 覆盖 92 平台、581 模型、1,278 条按量价、178 条订阅套餐，全部带采集时间戳与价格生效时间戳。

![Platforms](https://img.shields.io/badge/平台-92-blue)
![Models](https://img.shields.io/badge/模型-581-green)
![Pricing](https://img.shields.io/badge/按量价-1,278-orange)
![Plans](https://img.shields.io/badge/套餐-178-purple)
![Updated](https://img.shields.io/badge/更新-2026--08--17-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📌 为什么用这个库

- **全**：国内 + 海外 + 中转矩阵 + 编程工具 + 生成式 AI + 搜索订阅 + Agent 平台，无一遗漏
- **新**：每条记录双时间戳（`collected_at` 采集时间 + `effective_at` 价格生效时间）
- **准**：价格标注口径（官方价 / 渠道价 / 峰谷价 / 综合价 / 区域价），来源 URL 可溯
- **全模态**：文本 / 视频(按秒) / 图像(按张) / 语音(按字符/分钟) / Embedding(按 token)

## ⚡ 快速对比

### DeepSeek V4 Flash — 全网渠道价对比（双币，$ / ¥ 每百万 token）

> ⚠️ DeepSeek 官方 2026-08-17 起峰谷定价：输出高峰 ¥9 / 闲时 ¥4.5。高峰时段 = 每日 9-12、14-18 点。汇率 fx=7.1（2026-08 参考）。

| 渠道 | 输入 | 输出 | 缓存命中 | 备注 |
|---|---|---|---|---|
| **OpenRouter** | $0.0603 / ¥0.4281 | $0.1206 / ¥0.8563 | $0.015719 | ≈0.43元/M |
| **DeepInfra** | $0.09 / ¥0.639 | $0.18 / ¥1.278 | $0.002 | API直拉：cents_per_input_token=9e-06 |
| **Cloudflare** | $0.027 / ¥0.1917 | $0.1 / ¥0.71 | — | 范围$0.027-4.88/M，Neurons计费，免费日额度 |
| **Fireworks** | $0.14 / ¥0.994 | $0.28 / ¥1.988 | — | 新用户$6+1亿token |
| **Parasail** | $0.14 / ¥0.994 | $0.28 / ¥1.988 | — |  |
| **Cerebras** | $0.14 / ¥0.994 | $0.28 / ¥1.988 | — |  |
| **Novita** | $0.14 / ¥0.994 | $0.28 / ¥1.988 | — |  |
| **SambaNova** | $0.26 / ¥1.846 | $0.52 / ¥3.692 | — | 最低gpt-oss-120b $0.26起 |
| **Together** | $0.27 / ¥1.917 | $0.54 / ¥3.834 | — | V4 1M ctx，自托管盈亏平衡~75M/月 |
| **Groq** | $0.3 / ¥2.13 | $0.5 / ¥3.55 | — | 缓存命中$0.03 |
| **阿里百炼** | $0.140845 / ¥1 | $0.28169 / ¥2 | — | 8/17前，峰谷后待确认 |
| **DeepSeek官方** | — | $1.26761 / ¥9 | $0.014085 | 峰谷：高峰9/闲时4.5；批量5折 |
| **硅基流动** | $0.28169 / ¥2 | — | — | DeepSeek 3.2时代对比 |

### 主流旗舰模型官方 API 价

| 模型 | 输入 | 输出 | 上下文 | 来源 |
|---|---|---|---|---|
| **gpt-5.6-sol** | $5 / ¥35.5 | $30 / ¥213 | ~1M | OpenAI |
| **gpt-5.5** | $5 / ¥35.5 | $30 / ¥213 | 1.05M ctx | OpenAI |
| **gpt-5.2** | $0.03 / ¥0.213 | $0.05 / ¥0.355 | — | OpenAI |
| **claude-fable-5** | $10 | $50 | OR路由 | Anthropic |
| **claude-opus-5** | $10 | $50 | OR路由 | Anthropic |
| **claude-opus-4.7** | $5 / ¥35.5 | $25 / ¥177.5 | 200k | Anthropic |
| **claude-sonnet-4.6** | $3 / ¥21.3 | $15 / ¥106.5 | 200k | Anthropic |
| **claude-haiku-4.5** | $1 / ¥7.1 | $5 / ¥35.5 | 200k | Anthropic |
| **gemini-3.6-flash** | $1.5 / ¥10.65 | $7.5 / ¥53.25 | — | Google |
| **gemini-3.1-pro** | $2 / ¥14.2 | $12 / ¥85.2 | — | Google |
| **gemini-3.5-flash-lite** | $0.3 / ¥2.13 | $2.5 / ¥17.75 | — | Google |
| **grok-4.6** | $2 | $6 | OR路由 | xAI |
| **grok-4.3** | $1.25 / ¥8.875 | $2.5 / ¥17.75 | 2M ctx | xAI |
| **grok-4.1-fast** | $0.2 / ¥1.42 | $0.4 / ¥2.84 | — | xAI |
| **deepseek-v4-pro** | — | $3.80282 / ¥27 | — | DeepSeek官方 |
| **deepseek-v4-flash** | — | $1.26761 / ¥9 | — | DeepSeek官方 |
| **qwen3.7-max** | $0.929577 / ¥6.6 | $5.07042 / ¥36 | — | 阿里百炼 |
| **qwen3.7-plus** | $0.28169 / ¥2 | $1.12676 / ¥8 | — | 阿里百炼 |
| **minimax-m3** | $0.24 / ¥1.704 | $0.96 / ¥6.816 | 1M | MiniMax |
| **minimax-m2.7** | $0.06 / ¥0.426 | — | 1M ctx | MiniMax |
| **kimi-k3** | — | $15 / ¥100 | 1M ctx | 月之暗面 |
| **glm-5** | $0.95 / ¥6.745 | $2.5 / ¥17.75 | — | 智谱 |
| **mistral-large-3** | $0.5 / ¥3.55 | $1.5 / ¥10.65 | — | Mistral |
| **open-mistral-nemo** | $0.02 / ¥0.142 | $0.04 / ¥0.284 | — | Mistral |

> `OR路由` = OpenRouter 路由价；`—` = 该平台无此口径价，详见 data/pricing.csv。

### 订阅套餐快查（¥ / 月）

| 产品 | 套餐 | 价格 | 币种 | 额度/说明 |
|---|---|---|---|---|
| HuggingFace | 免费用户月额度 | $0.1 / ¥0.71 | USD | $0.10/月 |
| Trae | Lite | ¥3 / $0.422535 | CNY |  |
| 美团LongCat | 2.0-Preview 付费包 | ¥9.9 / $1.39437 | CNY | 5000万tokens |
| Trae | Pro | ¥10 / $1.40845 | CNY |  |
| CodeBuddy | 基础套餐 | ¥10 / $1.40845 | CNY | 1000 credits |
| HuggingFace | PRO用户月额度 | $2 / ¥14.2 | USD | $2/月 |
| 通义灵码 | 专业版 | ¥20 / $2.8169 | CNY | 估算 |
| MarsCode | Pro·国际版 | ¥20 / $2.8169 | CNY | ACU按量，每ACU $2.25 |
| MiniMax | Coding Plan Starter | ¥29 / $4.08451 | CNY |  |
| Trae | Pro+ | ¥30 / $4.22535 | CNY |  |
| OpenAI | ChatGPT Plus·印度 | $4.8 / ¥34.08 | USD | ₹399约$4.8 |
| Poe | 订阅起步 | $4.99014 / ¥35.43 | USD | 积分制，最高830万积分/月 |
| ElevenLabs | Starter | $5 / ¥35.5 | USD | 年付$5/月 |
| 火山套餐 | Agent Plan Small | ¥40 / $5.6338 | CNY | 限时9.9元起活动 |
| 火山套餐 | Coding Plan 入门 | ¥40 / $5.6338 | CNY | 活动折上9折低至8.9元 |
| 火山套餐 | Coding Plan Lite | ¥40 / $5.6338 | CNY | 18000次/月 |
| MiniMax | Token Plan Plus | ¥49 / $6.90141 | CNY | 官方文档确认¥49/月 |
| Kling | 低价入门 | $6.99014 / ¥49.63 | USD | $6.99/月起 |
| Vertex AI | Gemini Workspace Starter | $7 / ¥49.7 | USD | Google Workspace 集成 |
| Google | Gemini Workspace Starter | $7 / ¥49.7 | USD |  |
| OpenAI | ChatGPT Go | $8 / ¥56.8 | USD | 基础额度 |
| Sourcegraph | Cody Pro | $9 / ¥63.9 | USD | ~$9/user/mo |
| Coze | Premium(国际版) | $9 / ¥63.9 | USD | 每天100条信息信用点 |
| 字节豆包 | 豆包专业版(C端) | ¥68 / $9.57746 | CNY | 2026-06-24上线 |
| Adobe Firefly | Standard | $9.99014 / ¥70.93 | USD | credits |
| GitHub Copilot | Pro | $10 / ¥71 | USD | AI Credits按token |
| Midjourney | Basic | $10 / ¥71 | USD | Fast小时 |
| Suno | Pro | $10 / ¥71 | USD | Basic/Premier |
| Kling | Standard | $10 / ¥71 | USD | 最小月度credit池 |
| GitHub Copilot | Pro·按token | $10 / ¥71 | USD | AI Credits按模型扣 |

## 📊 数据规模

| 维度 | 数量 |
|---|---|
| 平台 | 92（无一空壳） |
| 模型 | 581（含 OpenRouter 全目录 414） |
| 按量价 | 1,278 条 |
| 订阅套餐 | 178 条 |
| 区域标注 | 16 条（国内外/区域差异） |
| 时间戳覆盖 | 100%（collected_at + effective_at） |
| 币种 | 统一双币（USD/CNY，fx=7.1 标注在 pricing.fx_rate） |

## 🗂️ 覆盖范围

| 类别 | 平台 |
|---|---|
| **国内 API** | DeepSeek官方 / 火山方舟 / 字节豆包 / 阿里百炼 / 腾讯混元 / 百度千帆 / 智谱 / 月之暗面 / MiniMax / 讯飞星火 / 阶跃星辰 / 硅基流动 / 美团LongCat / 零一万物 / 百川 / 华为盘古 / 商汤 / 昆仑万维 / 360智脑 / DeepBricks / 无问芯穹 / Z.ai |
| **海外 API** | OpenAI / Anthropic / Google / xAI / Mistral / Cohere / Perplexity / Nous Research / Meta Llama / Voyage / Jina / Stability / Flux / Manus |
| **DeepSeek 中转矩阵** | OpenRouter / DeepInfra / Groq / Novita / Parasail / Fireworks / Together / Cerebras / SambaNova / Cloudflare / Replicate / Modal / NVIDIA NIM / AWS Bedrock / Azure OpenAI / HuggingFace |
| **AI 编程工具** | Cursor / Windsurf / Replit / Bolt / v0 / Devin / Sourcegraph / Amazon Q / Gemini Code Assist / 通义灵码 / CodeGeeX / Comate / CodeBuddy / Trae / MarsCode / GitHub Copilot |
| **生成式 AI** | Midjourney / Runway / Kling / 即梦 / Suno / ElevenLabs / HeyGen / 海螺 / Sora / Veo |
| **搜索/订阅/Agent** | Google One / Microsoft Copilot / Lovable / Coze / Dify / OpenClaw / n8n / Poe |

## 📐 计费口径（pricing.item_type）

| 模态 | 口径 | 示例 |
|---|---|---|
| 文本 | 每百万 token | OpenAI $5/$30、DeepSeek ¥1.5-9 |
| 视频 | 每秒 | Seedance $0.04/s、Veo $0.10/s、Sora $0.10-0.50/s |
| 图像 | 每张 / 每兆像素 | DALL-E $0.04-0.12、Flux $0.003-0.03 |
| 语音 TTS | 每百万字符 / token | OpenAI $15-30/M字符、MiniMax ¥3.2/M |
| ASR | 每分钟 | Whisper $0.006/min |
| Embedding | 每百万 token | OpenAI 3-small $0.02、3-large $0.13 |
| VLM | 每次调用 | MiniMax api-vlm ¥0.025/次 |

## 💾 数据文件

| 文件 | 说明 |
|---|---|
| `api_cost.db` | SQLite 主库（4 表：platforms/models/pricing/plans） |
| `data/platforms.csv` | 平台清单 |
| `data/models.csv` | 模型 + 上下文窗口 |
| `data/pricing.csv` | 按量价全口径 |
| `data/plans.csv` | 订阅套餐 |

### 快速查询示例

```sql
-- DeepSeek V4 Flash 全网最便宜渠道
SELECT p.name, pr.price_usd FROM pricing pr
JOIN platforms p ON p.id = pr.platform_id
WHERE pr.model_name LIKE '%deepseek-v4-flash%' AND pr.item_type = '输入'
ORDER BY pr.price_usd LIMIT 5;

-- 某价格生效时间
SELECT model_name, item_type, effective_at FROM pricing
WHERE platform_id = (SELECT id FROM platforms WHERE name='DeepSeek官方');
```

## 🕐 数据时效

- **2026-08-17 快照**：DeepSeek 官方峰谷定价生效当日采集
- 每条记录带 `collected_at`（采集）+ `effective_at`（生效）
- 已知缺口（README 内附）：火山账号折扣价需登录、部分国内平台峰谷跟随未公告、即梦/可灵/海螺国际版价未公开

## 📄 License

MIT
