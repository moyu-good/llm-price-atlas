#!/usr/bin/env python3
"""套餐第四轮：Firecrawl 渲染实抓落库（2026-08-22）
来源: data/fc/*.md（api.firecrawl.dev v1/scrape, waitFor=5000）"""
import sqlite3

DB = "/mnt/d/PROJECT/AI模型价格库/api_cost.db"
TODAY = "2026-08-22"
FX = 7.1
db = sqlite3.connect(DB)
cur = db.cursor()

def pid(name):
    r = cur.execute("SELECT id FROM platforms WHERE name=?", (name,)).fetchone()
    return r[0] if r else None

def upsert(platform, name, cny, quota, src, note, period="monthly"):
    p = pid(platform)
    ex = cur.execute("SELECT id FROM plans WHERE platform_id=? AND plan_name=?", (p, name)).fetchone()
    tag = f" | {note}"
    if ex:
        cur.execute("""UPDATE plans SET price_cny=?, quota_desc=?, source_url=?, collected_at=?,
                       notes=COALESCE(notes,'')||? WHERE id=?""", (cny, quota, src, TODAY, tag, ex[0]))
    else:
        cur.execute("""INSERT INTO plans (platform_id, plan_name, price_cny, period, quota_desc,
                       models_included, source_url, notes, collected_at, effective_at)
                       VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (p, name, cny, period, quota, "", src, note, TODAY, TODAY))

def mark(platform, name_or_like, note):
    cur.execute("""UPDATE plans SET notes=COALESCE(notes,'')||? 
                   WHERE platform_id=? AND plan_name LIKE ?""", (f" | {note}", pid(platform), name_or_like))

# ========== Kimi Code（kimi.com/code 实抓：月付价，年付省至$480）==========
K_SRC = "https://www.kimi.com/code"
upsert("月之暗面", "Kimi Code Moderato", round(19*FX,1), "$19/月(年付$15=$180)；周刷新额度；K3可用", K_SRC, f"{TODAY}✅Firecrawl实抓")
upsert("月之暗面", "Kimi Code Allegretto", round(39*FX,1), "$39/月(年付$31=$372)；更高并发", K_SRC, f"{TODAY}✅Firecrawl实抓")
upsert("月之暗面", "Kimi Code Allegro", round(99*FX,1), "$99/月(年付$79=$948)", K_SRC, f"{TODAY}✅Firecrawl实抓")
upsert("月之暗面", "Kimi Code Vivace", round(199*FX,1), "$199/月(年付$159=$1908)；最高周额度", K_SRC, f"{TODAY}✅Firecrawl实抓·新增档位")
mark("月之暗面", "%Andante%", f"{TODAY}⚠️官方套餐页已无Andante档(现为Moderato/Allegretto/Allegro/Vivace)")
mark("月之暗面", "%最高档%", f"{TODAY}◐C端会员与Code套餐分线,待核")

# ========== ChatGPT（chatgpt.com/pricing 实抓）==========
G_SRC = "https://chatgpt.com/pricing"
for name, quota in [("ChatGPT Go", "$8/月;Go档含广告"), ("ChatGPT Plus", "$20/月;GPT-5.6全模型"),
                    ("ChatGPT Pro", "From $100/月起(5x);另有20x档;Sol Pro推理")]:
    cur.execute("""UPDATE plans SET notes=COALESCE(notes,'')||? WHERE platform_id=? AND plan_name=?""",
                (f" | {TODAY}✅Firecrawl实核", pid("OpenAI"), name))
cur.execute("""UPDATE plans SET quota_desc='From $100/月起(Pro 5x档,另有20x);Sol Pro/无限图像' 
               WHERE platform_id=? AND plan_name='ChatGPT Pro'""", (pid("OpenAI"),))

# ========== Google AI（one.google.com 实抓：四档全 lineup）==========
GO_SRC = "https://one.google.com/about/google-ai-plans"
upsert("GoogleOne", "Google AI Plus", round(4.99*FX,1), "$4.99/月", GO_SRC, f"{TODAY}✅Firecrawl实抓")
upsert("GoogleOne", "Google AI Pro", round(19.99*FX,1), "$19.99/月;含5TB存储", GO_SRC, f"{TODAY}✅Firecrawl实抓")
upsert("GoogleOne", "Google AI Ultra 5x", round(99.99*FX,1), "$99.99/月;20TB起", GO_SRC, f"{TODAY}✅Firecrawl实抓")
upsert("GoogleOne", "Google AI Ultra 20x", round(199.99*FX,1), "$199.99/月", GO_SRC, f"{TODAY}✅Firecrawl实抓")
cur.execute("""DELETE FROM plans WHERE platform_id=? AND plan_name NOT IN 
               ('Google AI Plus','Google AI Pro','Google AI Ultra 5x','Google AI Ultra 20x')""", (pid("GoogleOne"),))

# ========== ElevenLabs（elevenlabs.io/pricing 实抓：Creator砍半！）==========
E_SRC = "https://elevenlabs.io/pricing"
upsert("ElevenLabs", "Free", 0.0, "10k credits/月", E_SRC, f"{TODAY}✅Firecrawl实抓")
upsert("ElevenLabs", "Starter", round(6*FX,1), "30k credits/月", E_SRC, f"{TODAY}✅实抓·原$5涨价至$6")
upsert("ElevenLabs", "Creator", round(11*FX,1), "121k credits/月", E_SRC, f"{TODAY}✅实抓·原$22降价至$11")
upsert("ElevenLabs", "Pro", round(99*FX,1), "600k credits/月", E_SRC, f"{TODAY}✅Firecrawl实抓")
upsert("ElevenLabs", "Scale", round(299*FX,1), "1.8M credits/月", E_SRC, f"{TODAY}✅Firecrawl实抓")
upsert("ElevenLabs", "Business", round(990*FX,1), "6M credits/月", E_SRC, f"{TODAY}✅实抓·新增档位")
cur.execute("""UPDATE plans SET quota_desc='企业定制', source_url=? WHERE platform_id=? AND plan_name='Enterprise'""",
            (E_SRC, pid("ElevenLabs")))

# ========== Kling（官方会员页实抓：首购折扣价结构）==========
KL_SRC = "https://app.klingai.com/global/membership"
for tier, usd in [("Standard", 8.8), ("Pro", 32.56), ("Premier", 80.96)]:
    upsert("Kling", f"Kling {tier}", round(usd*FX,1), f"${usd}/月(首单再享7折)", KL_SRC,
           f"{TODAY}✅Firecrawl实抓(首购价体系)")

# ========== HuggingFace（huggingface.co/pricing 实抓）==========
upsert("HuggingFace", "PRO", round(9*FX,1), "$9/月", "https://huggingface.co/pricing",
       f"{TODAY}✅Firecrawl实抓")

# ========== Windsurf（windsurf.com/pricing 实抓）==========
W_SRC = "https://windsurf.com/pricing"
upsert("Windsurf", "Free", 0.0, "$0", W_SRC, f"{TODAY}✅Firecrawl实抓")
upsert("Windsurf", "Pro", round(20*FX,1), "$20/月", W_SRC, f"{TODAY}✅实抓·原¥106.5为旧价")
upsert("Windsurf", "Max", round(200*FX,1), "$200/月", W_SRC, f"{TODAY}✅Firecrawl实抓")
upsert("Windsurf", "Team", round(80*FX,1), "$80/月+$40/全职开发席;含Devin Desktop", W_SRC, f"{TODAY}✅实抓·新增档位")
cur.execute("DELETE FROM plans WHERE platform_id=? AND plan_name IN ('Pro·2026-03后','Max') AND plan_name='Pro·2026-03后'",
            (pid("Windsurf"),))

# ========== 智谱 GLM Coding（bigmodel.cn/glm-coding 实抓：数字全对+年付价）==========
Z_SRC = "https://bigmodel.cn/glm-coding"
for name, annual, monthly in [("GLM Coding Plan Lite", 94.4, 118), ("GLM Coding Plan Pro", 430.4, 538),
                              ("GLM Coding Plan Max", 862.4, 1078)]:
    cur.execute("""UPDATE plans SET price_cny=?, quota_desc=COALESCE(quota_desc,'')||?, notes=COALESCE(notes,'')||?
                   WHERE platform_id=? AND plan_name=?""",
                (monthly, f"(年付¥{annual}/月)", f" | {TODAY}✅Firecrawl实抓", pid("智谱"), name))
mark("智谱", "Pro·国际版", f"{TODAY}◐国际版定价未在主站出现,待核")

# ========== Trae（trae.ai/pricing 实抓：USD 数值全部实锤）==========
T_SRC = "https://www.trae.ai/pricing"
for name, usd, usage in [("Lite", 3, "$5基础用量"), ("Pro", 10, "$20基础用量"),
                         ("Pro+", 30, ""), ("Ultra", 100, "$400基础用量")]:
    cur.execute("""UPDATE plans SET price_cny=?, quota_desc=COALESCE(quota_desc,'')||?, notes=COALESCE(notes,'')||?,
                   source_url=? WHERE platform_id=? AND plan_name=?""",
                (round(usd*FX,1), f"({usage})" if usage else "",
                 f" | {TODAY}✅Firecrawl实抓${usd}/月(Pro有7天试用)", T_SRC, pid("Trae"), name))

db.commit()
n = db.execute("SELECT COUNT(*) FROM plans").fetchone()[0]
ok = db.execute("SELECT COUNT(*) FROM plans WHERE notes LIKE '%✅%'").fetchone()[0]
print(f"套餐总数 {n} | ✅实核 {ok} 条")
print(f"GoogleOne: {db.execute('SELECT COUNT(*) FROM plans WHERE platform_id=?',(pid('GoogleOne'),)).fetchone()[0]}条")
print(f"ElevenLabs: {db.execute('SELECT COUNT(*) FROM plans WHERE platform_id=?',(pid('ElevenLabs'),)).fetchone()[0]}条")
db.close()
