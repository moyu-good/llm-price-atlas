#!/usr/bin/env python3
"""价格库核对器：拉 OpenRouter 实时 API，逐条对比库内 1033 条价格。

输出: data/verify_report_<date>.md
判定: |差价|/库内价 ≤1% → 一致; >1% → 变动; 库有API无 → 下架?; API有库无 → 新模型
"""
import json
import sqlite3
import urllib.request
from datetime import date

DB = "/mnt/d/PROJECT/AI模型价格库/api_cost.db"
OUT = f"/mnt/d/PROJECT/AI模型价格库/data/verify_report_{date.today()}.md"

req = urllib.request.Request("https://openrouter.ai/api/v1/models", headers={"User-Agent": "Mozilla/5.0"})
live = json.loads(urllib.request.urlopen(req, timeout=60).read())["data"]
print(f"OpenRouter 在线模型: {len(live)}")

live_map = {}
for m in live:
    p = m.get("pricing") or {}
    try:
        pin = float(p.get("prompt", 0) or 0) * 1e6
        pout = float(p.get("completion", 0) or 0) * 1e6
    except ValueError:
        continue
    live_map[m["id"]] = (pin, pout)

db = sqlite3.connect(DB)
rows = db.execute("""SELECT model_name, item_type, price_usd FROM pricing
                     WHERE platform_id=2 AND item_type IN ('输入','输出')""").fetchall()

match = diff = gone = 0
diffs, gones = [], []
for name, item, old in rows:
    key = None
    for cand in (name, name.replace("-latest", "")):
        if cand in live_map:
            key = cand
            break
    if not key:
        # slug 模糊: 取前缀匹配
        cands = [k for k in live_map if k.split("/")[-1] == name or k.endswith(name)]
        key = cands[0] if cands else None
    if not key:
        gone += 1
        gones.append((name, old))
        continue
    newp = live_map[key][0 if item == "输入" else 1]
    if old == 0:
        continue
    chg = abs(newp - old) / old
    if chg <= 0.01:
        match += 1
    else:
        diff += 1
        diffs.append((name, item, old, newp, (newp - old) / old * 100))

db_ids = set()
for r in db.execute("SELECT model_name FROM pricing WHERE platform_id=2"):
    db_ids.add(r[0])
new_models = [mid for mid in live_map if mid.split("/")[-1].replace("-latest", "") not in
              {d.split("/")[-1].replace("-latest", "") for d in db_ids}]

with open(OUT, "w", encoding="utf-8") as f:
    f.write(f"# OpenRouter 价格核对报告 {date.today()}\n\n")
    f.write(f"- 在线模型 {len(live)} / 库内条目 {len(rows)}\n")
    f.write(f"- ✅ 一致(≤1%): {match}\n- 🔴 变动(>1%): {diff}\n- ❓ 库有在线无: {gone}\n")
    f.write(f"- 🆕 在线新增模型: {len(new_models)}\n\n## 价格变动\n\n| 模型 | 项 | 库内$ | 现价$ | 变幅 |\n|---|---|---|---|---|\n")
    for n, it, o, nw, pc in sorted(diffs, key=lambda x: -abs(x[4])):
        f.write(f"| {n} | {it} | {o:.3f} | {nw:.3f} | {pc:+.1f}% |\n")
    f.write("\n## 库有在线无（疑似下架）\n\n")
    for n, o in gones:
        f.write(f"- {n} (${o})\n")
    f.write("\n## 在线新增（前50）\n\n")
    for m in new_models[:50]:
        pi, po = live_map[m]
        f.write(f"- {m}: ${pi:.3f}/${po:.3f} per Mtok\n")
print(f"一致 {match} / 变动 {diff} / 消失 {gone} / 新增 {len(new_models)}")
print(f"报告 → {OUT}")
