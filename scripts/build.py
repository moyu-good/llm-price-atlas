#!/usr/bin/env python3
"""统一构建入口：db → data/db.json → index.html（模板注入）
用法: python3 scripts/build.py"""
import json
import sqlite3
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "api_cost.db"
OUT_JSON = ROOT / "data" / "db.json"
TEMPLATE = ROOT / "docs" / "explorer_template.html"
OUT_HTML = ROOT / "index.html"

# ---------- 1) db -> json ----------
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row
platforms = [dict(r) for r in db.execute(
    "SELECT id,name,region,url,api_docs_url,api_base_url,openai_compatible FROM platforms ORDER BY id")]
plat_name = {p["id"]: p["name"] for p in platforms}

pricing = []
for r in db.execute("""SELECT platform_id,model_name,item_type,price_usd,price_cny,
                       peak_price_cny,offpeak_price_cny,source_url FROM pricing"""):
    d = dict(r); d["platform"] = plat_name.get(d.pop("platform_id"), "?"); pricing.append(d)

plans = []
for r in db.execute("""SELECT platform_id,plan_name,price_cny,period,quota_desc,
                       models_included,source_url FROM plans ORDER BY platform_id, price_cny"""):
    d = dict(r); d["platform"] = plat_name.get(d.pop("platform_id"), "?"); plans.append(d)

models_n = db.execute("SELECT COUNT(*) FROM models").fetchone()[0]
data = {"meta": {"updated": str(date.today()), "platforms": len(platforms), "models": models_n,
                 "pricing_rows": len(pricing), "plan_rows": len(plans)},
        "platforms": platforms, "pricing": pricing, "plans": plans}
OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"✓ {OUT_JSON.name}: platforms={len(platforms)} pricing={len(pricing)} plans={len(plans)}")

# ---------- 2) json -> html ----------
html = TEMPLATE.read_text(encoding="utf-8")
payload = OUT_JSON.read_text(encoding="utf-8").replace("</", "<\\/")
if "__DATA__" not in html:
    raise SystemExit("✗ 模板缺少 __DATA__ 占位符")
OUT_HTML.write_text(html.replace("__DATA__", payload), encoding="utf-8")
print(f"✓ {OUT_HTML.name}: {(len(html)+len(payload))//1024} KB")
