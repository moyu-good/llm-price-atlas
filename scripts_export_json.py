#!/usr/bin/env python3
"""db → data/db.json（供交互式浏览器嵌入）"""
import json
import sqlite3

DB = "/mnt/d/PROJECT/AI模型价格库/api_cost.db"
OUT = "/mnt/d/PROJECT/AI模型价格库/data/db.json"
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row

platforms = [dict(r) for r in db.execute(
    "SELECT id, name, region, url, api_docs_url, api_base_url, openai_compatible FROM platforms ORDER BY id")]

plat_name = {p["id"]: p["name"] for p in platforms}

pricing = []
for r in db.execute("""SELECT platform_id, model_name, item_type, price_usd, price_cny,
                       peak_price_cny, offpeak_price_cny, source_url FROM pricing"""):
    d = dict(r)
    d["platform"] = plat_name.get(d.pop("platform_id"), "?")
    pricing.append(d)

plans = []
for r in db.execute("""SELECT platform_id, plan_name, price_cny, period, quota_desc,
                       models_included, source_url FROM plans ORDER BY platform_id, price_cny"""):
    d = dict(r)
    d["platform"] = plat_name.get(d.pop("platform_id"), "?")
    plans.append(d)

models_n = db.execute("SELECT COUNT(*) FROM models").fetchone()[0]
data = {
    "meta": {
        "updated": "2026-08-22",
        "platforms": len(platforms),
        "models": models_n,
        "pricing_rows": len(pricing),
        "plan_rows": len(plans),
        "fx_note": "CNY=USD×7.1 固定汇率折算；peak/offpeak 为 DeepSeek 峰谷价(¥)",
    },
    "platforms": platforms,
    "pricing": pricing,
    "plans": plans,
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
print(f"db.json 导出完成: platforms={len(platforms)} pricing={len(pricing)} plans={len(plans)}")
