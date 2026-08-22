#!/usr/bin/env python3
"""2026-08-22 套餐全面整理：
1) 全部 178 条补规范官方出处 URL
2) Claude 官方页核实修正（claude.com/pricing 实抓）
3) 补录：Claude Team Premium 席位、MiniMax 语音资源包 ×6
4) 每条打核验状态标记（✅实核 / ◐仅出处 / ○未核）"""
import sqlite3

DB = "/mnt/d/PROJECT/AI模型价格库/api_cost.db"
TODAY = "2026-08-22"
FX = 7.1
db = sqlite3.connect(DB)
cur = db.cursor()

# 平台名 → 规范官方套餐页
SRC = {
    "OpenAI": "https://chatgpt.com/pricing",
    "Anthropic": "https://claude.com/pricing",
    "Google": "https://one.google.com/about/google-ai-plans",
    "GoogleOne": "https://one.google.com/about/google-ai-plans",
    "Vertex AI": "https://cloud.google.com/vertex-a i/generative-ai/pricing".replace(" ", ""),
    "月之暗面": "https://www.kimi.com/pricing",
    "MiniMax": "https://platform.minimaxi.com/document/price",
    "智谱": "https://open.bigmodel.cn/pricing",
    "火山套餐": "https://www.volcengine.com/product/doubao",
    "Trae": "https://www.trae.ai/pricing",
    "Coze": "https://www.coze.cn/pricing",
    "Dify": "https://dify.ai/pricing",
    "ElevenLabs": "https://elevenlabs.io/pricing",
    "Kling": "https://app.klingai.com/global/membership",
    "GitHub Copilot": "https://github.com/features/copilot/plans",
    "Adobe Firefly": "https://www.adobe.com/products/firefly/plans.html",
    "Pika": "https://pika.art/pricing",
    "Manus": "https://manus.im/pricing",
    "Midjourney": "https://docs.midjourney.com/hc/en-us/articles/27870494071693",
    "Windsurf": "https://windsurf.com/pricing",
    "Cursor": "https://cursor.com/pricing",
    "Lovable": "https://lovable.dev/pricing",
    "DeepBricks": "https://deepbricks.ai/pricing",
    "MarsCode": "https://www.marscode.cn/pricing",
    "HuggingFace": "https://huggingface.co/pricing",
    "Perplexity": "https://www.perplexity.ai/pro",
    "DeepSeek官方": "https://platform.deepseek.com/",
    "CodeBuddy": "https://www.codebuddy.ai/pricing",
    "通义灵码": "https://tongyi.aliyun.com/lingma/buy",
    "GeminiCodeAssist": "https://developers.google.com/gemini-code-assist/docs/pricing",
    "讯飞星火": "https://xinghuo.xfyun.cn/deskmember",
    "硅基流动": "https://cloud.siliconflow.cn/account/token",
    "阶跃星辰": "https://platform.stepfun.com/interface-manage",
    "OpenRouter": "https://openrouter.ai/docs/faq",
}

# ---- 1) 全量补出处 + 核验标记 ----
rows = cur.execute("""SELECT pl.id, p.name FROM plans pl JOIN platforms p ON p.id=pl.platform_id""").fetchall()
n_src = n_marked = 0
for pid, pname in rows:
    url = SRC.get(pname)
    if url:
        cur.execute("UPDATE plans SET source_url=? WHERE id=?", (url, pid))
        n_src += 1
    # 核验标记：Anthropic 本轮实核；其余标待核
    tag = f"{TODAY}套餐复核✅官方页实核" if pname == "Anthropic" else f"{TODAY}套餐复核◐出处已规范·数字未逐条核"
    cur.execute("UPDATE plans SET notes = COALESCE(notes,'') || ? WHERE id=?", (" | " + tag, pid))
    n_marked += 1

# ---- 2) Anthropic 官方页实核修正（USD→CNY @7.1）----
def set_plan(name, price_cny, quota, usd_note):
    cur.execute("""UPDATE plans SET price_cny=?, quota_desc=?, notes=COALESCE(notes,'')||?
                   WHERE platform_id=(SELECT id FROM platforms WHERE name='Anthropic') AND plan_name=?""",
                (price_cny, quota, " | " + usd_note, name))
set_plan("Claude Pro", round(17 * FX, 1), "年付$17/月($200年)；月付$20；含Claude Code/Cowork/Design/Science；用量≥Free的5倍/5h窗口", "实核")
set_plan("Claude Max 5x", round(100 * FX, 1), "Pro用量的5倍/5h窗口；高优先级接入", "实核")
set_plan("Claude Max 20x", round(200 * FX, 1), "Pro用量的20倍/5h窗口", "实核")
set_plan("Claude Team", round(20 * FX, 1), "Standard席$20/席/月(年付,$25月付)：比Pro更多用量", "实核：Team拆双席位制")
cur.execute("""SELECT COUNT(*) FROM plans WHERE plan_name='Claude Team Premium'""")
if not cur.fetchone()[0]:
    cur.execute("""INSERT INTO plans (platform_id, plan_name, price_cny, period, quota_desc,
                   models_included, source_url, notes, collected_at, effective_at, currency)
                   SELECT id, 'Claude Team Premium', ?, 'monthly', ?,
                   '', 'https://claude.com/pricing', ?, ?, ?, 'USD'
                   FROM platforms WHERE name='Anthropic'""",
                (round(100 * FX, 1), "Premium席$100/席/月(年付,$125月付)=标准席5倍用量",
                 f" | {TODAY}套餐复核✅新增(官方Team双席位)", TODAY, TODAY))
set_plan("Claude Enterprise", round(20 * FX, 1), "$20/席/月+按API费率计使用量；SCIM/审计/HIPAA等", "实核")

# ---- 3) MiniMax 语音资源包（官方价目页实抓）----
mm = [("MiniMax 语音HD包一", 630, "¥700原价省10%；200万字符/T2A v2/RPM60/赠10克隆音色/1个月"),
      ("MiniMax 语音HD包二", 5950, "¥7000省15%；2000万字符/RPM200/赠30音色/3个月"),
      ("MiniMax 语音HD包三", 56000, "¥70000省20%；2亿字符/RPM500/赠300音色/1年"),
      ("MiniMax 语音Turbo包一", 360, "¥400省10%；200万字符/Turbo系列/RPM60/1个月"),
      ("MiniMax 语音Turbo包二", 3400, "¥4000省15%；2000万字符/RPM200/3个月"),
      ("MiniMax 语音Turbo包三", 32000, "¥40000省20%；2亿字符/RPM500/1年")]
for name, cny, desc in mm:
    ex = cur.execute("SELECT 1 FROM plans WHERE plan_name=?", (name,)).fetchone()
    if not ex:
        cur.execute("""INSERT INTO plans (platform_id, plan_name, price_cny, period, quota_desc,
                       models_included, source_url, notes, collected_at, effective_at, currency)
                       SELECT id, ?, ?, 'monthly', ?, 'T2A', ?, ?, ?, ?, 'CNY'
                       FROM platforms WHERE name='MiniMax'""",
                    (name, cny, desc, SRC["MiniMax"],
                     f"{TODAY}套餐复核✅官方页实抓", TODAY, TODAY))

db.commit()
print(f"出处规范化 {n_src} 条 | 核验标记 {n_marked} 条 | Claude修正5条+新增Premium席 | MiniMax语音包新增")
n = db.execute("SELECT COUNT(*) FROM plans").fetchone()[0]
nosrc = db.execute("SELECT COUNT(*) FROM plans WHERE source_url IS NULL OR source_url=''").fetchone()[0]
print(f"套餐总数 {n} / 缺出处 {nosrc}")
db.close()
