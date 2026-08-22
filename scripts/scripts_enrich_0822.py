#!/usr/bin/env python3
"""数据库殷实化：
A) platforms 表新增 api_docs_url / api_base_url / openai_compatible 三列并填充
B) plans.models_included 用官方实抓数据精确化（含 Copilot 全模型矩阵）"""
import sqlite3

DB = "/mnt/d/PROJECT/AI模型价格库/api_cost.db"
db = sqlite3.connect(DB)
cur = db.cursor()

# ---------- A. platforms 加列 ----------
for col in ("api_docs_url", "api_base_url", "openai_compatible"):
    try:
        cur.execute(f"ALTER TABLE platforms ADD COLUMN {col} TEXT")
    except sqlite3.OperationalError:
        pass  # 列已存在

API_INFO = {
    # name: (docs, base_url, compat说明)
    "OpenAI": ("https://developers.openai.com/api/docs", "https://api.openai.com/v1", "原生"),
    "Anthropic": ("https://platform.claude.com/docs", "https://api.anthropic.com/v1",
                  "原生Messages;另提供OpenAI兼容/v1/chat/completions"),
    "DeepSeek官方": ("https://api-docs.deepseek.com", "https://api.deepseek.com",
                   "OpenAI格式;另有Anthropic格式端点/api.deepseek.com/anthropic"),
    "Google": ("https://ai.google.dev/gemini-api/docs", "https://generativelanguage.googleapis.com/v1beta/openai/",
               "OpenAI兼容层;原生为generateContent"),
    "OpenRouter": ("https://openrouter.ai/docs", "https://openrouter.ai/api/v1", "OpenAI兼容聚合网关"),
    "xAI": ("https://docs.x.ai", "https://api.x.ai/v1", "OpenAI兼容"),
    "Groq": ("https://console.groq.com/docs/openai", "https://api.groq.com/openai/v1", "OpenAI兼容"),
    "Mistral": ("https://docs.mistral.ai", "https://api.mistral.ai/v1", "OpenAI兼容"),
    "Together": ("https://docs.together.ai", "https://api.together.xyz/v1", "OpenAI兼容"),
    "Perplexity": ("https://docs.perplexity.ai", "https://api.perplexity.ai", "OpenAI兼容(chat/completions)"),
    "阿里百炼": ("https://help.aliyun.com/zh/model-studio/getting-started/models",
              "https://dashscope.aliyuncs.com/compatible-mode/v1", "OpenAI兼容模式"),
    "字节豆包": ("https://www.volcengine.com/docs/82379", "https://ark.cn-beijing.volces.com/api/v3",
               "OpenAI兼容(火山方舟)"),
    "智谱": ("https://docs.bigmodel.cn", "https://open.bigmodel.cn/api/paas/v4", "OpenAI兼容"),
    "月之暗面": ("https://platform.moonshot.cn/docs", "https://api.moonshot.cn/v1", "OpenAI兼容"),
    "MiniMax": ("https://platform.minimaxi.com/document/guides", "https://api.minimaxi.com/v1", "OpenAI兼容"),
    "百度千帆": ("https://cloud.baidu.com/doc/WENXINWORKSHOP/index.html", "https://qianfan.baidubce.com/v2",
              "OpenAI兼容v2接口"),
    "硅基流动": ("https://docs.siliconflow.cn", "https://api.siliconflow.cn/v1", "OpenAI兼容"),
    "AWS Bedrock": ("https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html",
                  "https://bedrock-runtime.{region}.amazonaws.com/openai/v1", "OpenAI兼容端点+原生Converse API"),
    "Azure OpenAI": ("https://learn.microsoft.com/azure/ai-services/openai/", None, "原生(部署式端点)"),
    "ElevenLabs": ("https://elevenlabs.io/docs/api-reference/overview", "https://api.elevenlabs.io/v1", "音频专用REST"),
    "HuggingFace": ("https://huggingface.co/docs/inference-providers", "https://router.huggingface.co/v1",
                  "OpenAI兼容路由"),
}
n_api = 0
for name, (docs, base, compat) in API_INFO.items():
    r = cur.execute("SELECT id FROM platforms WHERE name=?", (name,)).fetchone()
    if r:
        cur.execute("UPDATE platforms SET api_docs_url=?, api_base_url=?, openai_compatible=? WHERE id=?",
                    (docs, base, compat, r[0]))
        n_api += 1

# 应用类平台：无公开API的标 N/A 说明
for name, note in [("Cursor","IDE订阅,无独立API"),("Trae","IDE订阅"),("GitHub Copilot","订阅内含Copilot API配额"),
                   ("Manus","Agent产品"),("Lovable","App生成平台"),("Pika","视频产品"),
                   ("Kling","视频产品(有开放API但套餐为C端会员)"),("Midjourney","Discord/Web产品"),
                   ("Adobe Firefly","Creative Cloud体系"),("Coze","Bot平台"),("Dify","可自部署LLMOps"),
                   ("CodeBuddy","IDE"),("通义灵码","IDE插件"),("GeminiCodeAssist","IDE/CLI"),
                   ("MarsCode","IDE"),("讯飞星火","C端App会员"),("GoogleOne","消费级订阅")]:
    cur.execute("""UPDATE platforms SET openai_compatible=? WHERE name=?""", (note, name))

# ---------- B. plans.models_included 精确化 ----------
def set_models(platform, plan_like, models):
    cur.execute("""UPDATE plans SET models_included=? WHERE platform_id=(SELECT id FROM platforms WHERE name=?)
                   AND plan_name LIKE ?""", (models, platform, plan_like))

# GitHub Copilot 官方模型矩阵（docs实抓解码）
set_models("GitHub Copilot", "Copilot Free%",
           "仅自动选模;2000补全/月")
set_models("GitHub Copilot", "Copilot Student%",
           "自动选模;不含第三方agent")
set_models("GitHub Copilot", "Copilot Pro",
           "Haiku4.5/Sonnet4.5/Sonnet4.6/Sonnet5/Gemini3.1Pro/Gemini3.5-3.7Flash/GPT-5mini/"
           "GPT-5.3-Codex/GPT-5.4/GPT-5.4mini")
set_models("GitHub Copilot", "Copilot Pro+",
           "Pro全部+Opus4.7/Opus4.8(含fast)/Opus5/Fable5/GPT-5.4nano")
set_models("GitHub Copilot", "Copilot Max",
           "同Pro+且premium模型优先接入;20000cr/月")
set_models("GitHub Copilot", "Copilot Business",
           "premium模型(Gemini/Opus4.7+/Fable5);1900cr/人")
set_models("GitHub Copilot", "Copilot Enterprise%",
           "premium模型优先;3900cr/人")

# ChatGPT 官方四档
set_models("OpenAI", "ChatGPT Free", "GPT-5.6 Luna;Thinking Mini;27K即时上下文")
set_models("OpenAI", "ChatGPT Go", "GPT-5.6 Luna;Thinking Mini扩展;54K上下文")
set_models("OpenAI", "ChatGPT Plus", "GPT-5.6 Sol/Terra/Luna;legacy模型;256K推理上下文")
set_models("OpenAI", "ChatGPT Pro", "全系无限:Sol/Sol Pro/Terra/Luna;128K即时+400K推理")

# Claude 官方
for p in ["Claude Pro", "Claude Max 5x", "Claude Max 20x"]:
    set_models("Anthropic", p, "Fable5(50%周额度)/Opus5/4.8/4.7/4.6/Sonnet5/4.6/Haiku4.5;200k上下文")
set_models("Anthropic", "Claude Team", "同Pro全模型;500k上下文")
set_models("Anthropic", "Claude Enterprise%", "同Team;500k上下文")
set_models("Anthropic", "Claude Team Premium", "同Team全模型;标准席5倍用量")

# Kimi Code
set_models("月之暗面", "%Moderato%", "Kimi K3(1M上下文)")
set_models("月之暗面", "%Allegretto%", "Kimi K3(1M上下文)")
set_models("月之暗面", "%Allegro%", "Kimi K3(1M上下文)")
set_models("月之暗面", "%Vivace%", "Kimi K3(1M上下文)")

# Cursor / Windsurf / Google
set_models("Cursor", "Hobby", "Composer;有限Agent请求")
set_models("Cursor", "Pro", "前沿模型全量;MCP/skills/hooks;云Agent;Bugbot按量")
set_models("Cursor", "Pro+", "Pro全部×3额度;Grok Bot")
set_models("Cursor", "Ultra", "Pro全部×20额度;新功能优先")
set_models("Windsurf", "Team", "各成员独立额度;Devin Desktop")
set_models("GoogleOne", "Google AI Plus%", "Gemini应用级;基础Veo/Flow额度")
set_models("GoogleOne", "Google AI Pro", "Gemini 3.1 Pro/Flow/Veo更高额;Whisk;NotebookLM加成")
set_models("GoogleOne", "Google AI Ultra%", "全模型最高额;Veo 3;Project Mariner")

db.commit()
print(f"API信息填充 {n_api} 平台 | 模型矩阵更新完成")
print("platforms列:", [c[1] for c in cur.execute("PRAGMA table_info(platforms)")])
mi = db.execute("SELECT COUNT(*) FROM plans WHERE models_included IS NOT NULL AND TRIM(models_included)!=''").fetchone()[0]
print(f"models_included 已填: {mi}/194")
db.close()
