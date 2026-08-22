#!/usr/bin/env python3
"""套餐第三轮：GitHub Copilot 全档重建（官方docs实抓）+ Cursor 核正 + Kimi去重 + Trae币种修复"""
import sqlite3

DB = "/mnt/d/PROJECT/AI模型价格库/api_cost.db"
TODAY = "2026-08-22"
FX = 7.1
db = sqlite3.connect(DB)
cur = db.cursor()

def pid(name):
    return cur.execute("SELECT id FROM platforms WHERE name=?", (name,)).fetchone()[0]

def add_plan(platform, name, cny, period, quota, src, note):
    ex = cur.execute("SELECT 1 FROM plans WHERE platform_id=? AND plan_name=?", (pid(platform), name)).fetchone()
    if ex:
        cur.execute("""UPDATE plans SET price_cny=?, period=?, quota_desc=?, notes=COALESCE(notes,'')||?
                       WHERE platform_id=? AND plan_name=?""", (cny, period, quota, " | "+note, pid(platform), name))
        return "更新"
    cur.execute("""INSERT INTO plans (platform_id, plan_name, price_cny, period, quota_desc,
                   models_included, source_url, notes, collected_at, effective_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (pid(platform), name, cny, period, quota, "", src, note, TODAY, TODAY))
    return "新增"

# ========== GitHub Copilot（docs.github.com 实抓）==========
GC_SRC = "https://docs.github.com/en/copilot/get-started/plans"
add_plan("GitHub Copilot", "Copilot Pro", round(10*FX,1), "monthly",
         "1500 AI Credits/月(Base1000+Flex500)", GC_SRC, f"{TODAY}✅官方docs实核")
add_plan("GitHub Copilot", "Copilot Pro+", round(39*FX,1), "monthly",
         "7000 AI Credits/月(3900+3100)；premium模型", GC_SRC, f"{TODAY}✅官方docs实核")
add_plan("GitHub Copilot", "Copilot Max", round(100*FX,1), "monthly",
         "20000 AI Credits/月(10000+10000)；premium模型优先", GC_SRC, f"{TODAY}✅官方docs实核")
add_plan("GitHub Copilot", "Copilot Business", round(19*FX,1), "monthly",
         "1900 Credits/人/月；⚠️2026-04-22起新组织自助注册暂停", GC_SRC, f"{TODAY}✅官方docs实核")
add_plan("GitHub Copilot", "Copilot Enterprise", round(39*FX,1), "monthly",
         "3900 Credits/人/月；企业级能力", GC_SRC, f"{TODAY}✅官方docs实核")
add_plan("GitHub Copilot", "Copilot Free", 0.0, "monthly",
         "有限功能；2000补全/月；仅自动选模", GC_SRC, f"{TODAY}✅官方docs实核")
add_plan("GitHub Copilot", "Copilot Student", 0.0, "monthly",
         "认证学生免费", GC_SRC, f"{TODAY}✅官方docs实核")
# 清理旧脏行
for old in ["AI Credits（6/1起）", "Pro·按token"]:
    cur.execute("DELETE FROM plans WHERE platform_id=? AND plan_name=?", (pid("GitHub Copilot"), old))

# ========== Cursor（cursor.com/pricing 实核结构）==========
CUR_SRC = "https://cursor.com/pricing"
cur.execute("""UPDATE plans SET quota_desc='Agent扩展额度', notes=COALESCE(notes,'')||?
               WHERE platform_id=? AND plan_name='Pro'""",
            (f" | {TODAY}✅官方页实核($20/月)", pid("Cursor")))
cur.execute("""UPDATE plans SET quota_desc='Pro的3倍Agent额度', notes=COALESCE(notes,'')||?
               WHERE platform_id=? AND plan_name='Pro+'""",
            (f" | {TODAY}✅官方页实核倍数(价格JS渲染未取到,沿用$60)", pid("Cursor")))
cur.execute("""UPDATE plans SET quota_desc='Pro的20倍Agent额度', notes=COALESCE(notes,'')||?
               WHERE platform_id=? AND plan_name='Ultra'""",
            (f" | {TODAY}✅官方页实核倍数(价格沿用$200)", pid("Cursor")))
add_plan("Cursor", "Teams Standard", round(40*FX,1), "monthly",
         "$40/人/月；团队管理/SSO/Bugbot", CUR_SRC, f"{TODAY}✅官方页实核")

# ========== 月之暗面去重（Kimi前缀 与 裸名 重复对）==========
kimi = pid("月之暗面")
pairs = [("Kimi Andante","Andante"),("Kimi Allegretto","Allegretto"),
         ("Kimi Moderato","Moderato"),("Kimi Allegro","Allegro")]
for keep, drop in pairs:
    cur.execute("UPDATE plans SET plan_name=? WHERE platform_id=? AND plan_name=?", (keep, kimi, drop))
    cur.execute("DELETE FROM plans WHERE platform_id=? AND id NOT IN (SELECT MIN(id) FROM plans WHERE platform_id=? AND plan_name=?) AND plan_name=?",
                (kimi, kimi, keep, keep))
cur.execute("""UPDATE plans SET notes=COALESCE(notes,'')||? WHERE platform_id=?
               AND price_cny IS NULL""",
            (f" | {TODAY}◐官网JS渲染未取到数字,待人工", kimi))
cur.execute("""UPDATE plans SET notes=COALESCE(notes,'')||? WHERE platform_id=?
               AND price_cny IS NOT NULL""",
            (f" | {TODAY}◐数字待官网核验(kimi.com/pricing为JS渲染)", kimi))

# ========== Trae 币种修复（美元数值误存为CNY）==========
trae = pid("Trae")
for plan_name, usd in [("Lite",3),("Pro",10),("Pro+",30),("Ultra",100)]:
    cur.execute("""UPDATE plans SET price_cny=?, quota_desc=COALESCE(quota_desc,'')||?,
                   notes=COALESCE(notes,'')||?
                   WHERE platform_id=? AND plan_name=? AND ABS(price_cny-?)<0.01""",
                (round(usd*FX,1), f"(原记录误存USD${usd})",
                 f" | {TODAY}◐币种修复${usd}→¥{round(usd*FX,1)};待官网核验", trae, plan_name, usd))

db.commit()
n = db.execute("SELECT COUNT(*) FROM plans").fetchone()[0]
print(f"套餐总数: {n}")
print("Copilot:", db.execute("SELECT COUNT(*) FROM plans WHERE platform_id=?", (pid("GitHub Copilot"),)).fetchone()[0], "条")
print("Kimi:", db.execute("SELECT COUNT(*) FROM plans WHERE platform_id=?", (kimi,)).fetchone()[0], "条")
print("Trae币种修复完成 / Cursor Teams 新增")
db.close()
