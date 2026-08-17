# AI 模型价格库 · AI API Pricing Database

> **全网 AI 模型 / API / 套餐价格数据库** — 覆盖 84 平台、571 模型、1,266 条按量价、164 条订阅套餐，全部带采集时间戳与价格生效时间戳。

![Platforms](https://img.shields.io/badge/平台-84-blue)
![Models](https://img.shields.io/badge/模型-571-green)
![Pricing](https://img.shields.io/badge/按量价-1,266-orange)
![Plans](https://img.shields.io/badge/套餐-164-purple)
![Updated](https://img.shields.io/badge/更新-2026--08--17-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📌 为什么用这个库

- **全**：国内 + 海外 + 中转矩阵 + 编程工具 + 生成式 AI + 搜索订阅 + Agent 平台，无一遗漏
- **新**：每条记录双时间戳（`collected_at` 采集时间 + `effective_at` 价格生效时间）
- **准**：价格标注口径（官方价 / 渠道价 / 峰谷价 / 综合价 / 区域价），来源 URL 可溯
- **全模态**：文本 / 视频(按秒) / 图像(按张) / 语音(按字符/分钟) / Embedding(按 token)

## ⚡ 快速对比

### DeepSeek V4 Flash — 全网渠道价对比（$ / 百万 token）

> ⚠️ DeepSeek 官方 2026-08-17 起峰谷定价：输出高峰 ¥9 / 闲时 ¥4.5。高峰时段 = 每日 9-12、14-18 点。

| 渠道 | 输入 | 输出 | 缓存命中 | 备注 |
|---|---|---|---|---|
| **OpenRouter** | $0.0603 | $0.1206 | $0.015719 | ≈0.43元/M |
| **DeepInfra** | $0.09 | $0.18 | $0.002 | API直拉：cents_per_input_token=9e-06 |
| **Cloudflare** | $0.027 | $0.1 | — | 范围$0.027-4.88/M，Neurons计费，免费日额度 |
| **Fireworks** | $0.14 | $0.28 | — | 新用户$6+1亿token |
| **Parasail** | $0.14 | $0.28 | — |  |
| **Cerebras** | $0.14 | $0.28 | — |  |
| **Novita** | $0.14 | $0.28 | — |  |
| **SambaNova** | $0.26 | $0.52 | — | 最低gpt-oss-120b $0.26起 |
| **Together** | $0.27 | $0.54 | — | V4 1M ctx，自托管盈亏平衡~75M/月 |
| **Groq** | $0.3 | $0.5 | — | 缓存命中$0.03 |
| **阿里百炼** | ¥1 | ¥2 | — | 8/17前，峰谷后待确认 |
| **DeepSeek官方** | — | ¥9 | — | 峰谷：高峰9/闲时4.5；批量5折 |
| **硅基流动** | ¥2 | — | — | DeepSeek 3.2时代对比 |

### 主流旗舰模型官方 API 价

| 模型 | 输入 | 输出 | 上下文 | 来源 |
|---|---|---|---|---|
| **gpt-5.6-sol** | $5 | $30 | ~1M | OpenAI |
| **gpt-5.5** | $5 | $30 | 1.05M ctx | OpenAI |
| **gpt-5.2** | $0.03 | $0.05 | — | OpenAI |
| **claude-fable-5** | $10 | $50 | OR路由 | Anthropic |
| **claude-opus-5** | $10 | $50 | OR路由 | Anthropic |
| **claude-opus-4.7** | $5 | $25 | 200k | Anthropic |
| **claude-sonnet-4.6** | $3 | $15 | 200k | Anthropic |
| **claude-haiku-4.5** | $1 | $5 | 200k | Anthropic |
| **gemini-3.6-flash** | $1.5 | $7.5 | — | Google |
| **gemini-3.1-pro** | $2 | $12 | — | Google |
| **gemini-3.5-flash-lite** | $0.3 | $2.5 | — | Google |
| **grok-4.6** | $2 | $6 | OR路由 | xAI |
| **grok-4.3** | $1.25 | $2.5 | 2M ctx | xAI |
| **grok-4.1-fast** | $0.2 | $0.4 | — | xAI |
| **deepseek-v4-pro** | — | ¥27 | — | DeepSeek官方 |
| **deepseek-v4-flash** | — | ¥9 | — | DeepSeek官方 |
| **qwen3.7-max** | ¥6.6 | ¥36 | — | 阿里百炼 |
| **qwen3.7-plus** | ¥2 | ¥8 | — | 阿里百炼 |
| **minimax-m3** | $0.24 | $0.96 | 1M | MiniMax |
| **minimax-m2.7** | $0.06 | — | 1M ctx | MiniMax |
| **kimi-k3** | — | $15 | 1M ctx | 月之暗面 |
| **glm-5** | $0.95 | $2.5 | — | 智谱 |
| **mistral-large-3** | $0.5 | $1.5 | — | Mistral |
| **open-mistral-nemo** | $0.02 | $0.04 | — | Mistral |

> `OR路由` = OpenRouter 路由价；`—` = 该平台无此口径价，详见 data/pricing.csv。

### 订阅套餐快查（¥ / 月）

| 产品 | 套餐 | 价格 | 额度/说明 |
|---|---|---|---|
| HuggingFace | 免费用户月额度 | ¥0.1 | $0.10/月 |
| HuggingFace | PRO用户月额度 | ¥2 | $2/月 |
| Trae | Lite | ¥3 |  |
| OpenAI | ChatGPT Plus·印度 | ¥4.8 | ₹399约$4.8 |
| Poe | 订阅起步 | ¥4.99 | 积分制，最高830万积分/月 |
| ElevenLabs | Starter | ¥5 | 年付$5/月 |
| Kling | 低价入门 | ¥6.99 | $6.99/月起 |
| OpenAI | ChatGPT Go | ¥8 | 基础额度 |
| Sourcegraph | Cody Pro | ¥9 | ~$9/user/mo |
| Coze | Premium(国际版) | ¥9 | 每天100条信息信用点 |
| 美团LongCat | 2.0-Preview 付费包 | ¥9.9 | 5000万tokens |
| GitHub Copilot | Pro | ¥10 | AI Credits按token |
| Midjourney | Basic | ¥10 | Fast小时 |
| Suno | Pro | ¥10 | Basic/Premier |
| Trae | Pro | ¥10 |  |
| CodeBuddy | 基础套餐 | ¥10 | 1000 credits |
| Kling | Standard | ¥10 | 最小月度credit池 |
| GitHub Copilot | Pro·按token | ¥10 | AI Credits按模型扣 |
| Runway | Standard | ¥12 | credits |
| Windsurf | Pro | ¥15 | 500提示/月，可+$10/250提示 |
| OpenAI | ChatGPT Plus·菲律宾区 | ¥16.31 | 玻区涨后唯一低价区 ₱999；无税 |
| GitHub Copilot | Business | ¥19 | 按token |
| Sourcegraph | Cody Enterprise | ¥19 | $19/user/mo |
| AmazonQ | Q Developer Pro | ¥19 | 超4000行转换+$0.003/行 |
| GoogleOne | AI Pro | ¥19.99 | 2TB存储+Gemini 3 Pro+Veo2 |
| Anthropic | Claude Pro | ¥20 | 标准用量 |
| Anthropic | Claude Enterprise | ¥20 | 每人+API用量计费 |
| OpenAI | ChatGPT Plus | ¥20 | 标准额度 |
| Cursor | Pro | ¥20 | $20 credits |
| Replit | Core | ¥20 | 教育邮箱$10 |

## 📊 数据规模

| 维度 | 数量 |
|---|---|
| 平台 | 84（无一空壳） |
| 模型 | 571（含 OpenRouter 全目录 414） |
| 按量价 | 1,266 条 |
| 订阅套餐 | 164 条 |
| 区域标注 | 16 条（国内外/区域差异） |
| 时间戳覆盖 | 100%（collected_at + effective_at） |

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
