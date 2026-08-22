#!/usr/bin/env python3
"""2026-08-22 全面核对后的修正落库。数据来源：各官方页 + OpenRouter 实时API（本日抓取）。
幂等性：更新走 WHERE 精确匹配；新增前查重。"""
import json
import sqlite3
import urllib.request

DB = "/mnt/d/PROJECT/AI模型价格库/api_cost.db"
TODAY = "2026-08-22"
FX = 7.1

db = sqlite3.connect(DB)
cur = db.cursor()

def upd_price(platform_id, model, item, new_usd=None, note_suffix="", peak_cny=None, off_cny=None):
    sets, vals = ["notes = COALESCE(notes,'') || ?"], [f" | {TODAY}复核" + note_suffix]
    if new_usd is not None:
        sets.append("price_usd=?"); vals.append(new_usd)
        sets.append("price_cny=?"); vals.append(round(new_usd * FX, 4))
    if peak_cny is not None:
        sets.append("peak_price_cny=?"); vals.append(peak_cny)
    if off_cny is not None:
        sets.append("offpeak_price_cny=?"); vals.append(off_cny)
    sets.append("collected_at=?"); vals.append(TODAY + " 00:00:00")
    vals += [platform_id, model, item]
    cur.execute(f"UPDATE pricing SET {', '.join(sets)} WHERE platform_id=? AND model_name=? AND item_type=?", vals)

def add_price(platform_id, model, item, usd, item_type_note=""):
    ex = cur.execute("SELECT 1 FROM pricing WHERE platform_id=? AND model_name=? AND item_type=?",
                     (platform_id, model, item)).fetchone()
    if ex:
        return False
    cur.execute("""INSERT INTO pricing (platform_id, model_name, item_type, price_usd, price_cny,
                   source_url, notes, collected_at, effective_at, fx_rate)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (platform_id, model, item, usd, round(usd * FX, 4),
                 "", f"{TODAY}官方页核对新增{item_type_note}", TODAY + " 00:00:00", TODAY, FX))
    return True

# ---------- 1) Anthropic ----------
# Opus 4.7 无 Fast 模式（官方明示 speed=fast 会报错）→ 库内 $30 那条是错的
cur.execute("""UPDATE pricing SET notes = COALESCE(notes,'') || ' | 2026-08-22核实: 官方无此Fast模式(仅Opus5/4.8支持,$10/$50), 本条作废',
               effective_at = effective_at WHERE platform_id=12 AND model_name='Claude Opus 4.7 (Fast)'""")
add_price(12, "Claude Sonnet 5", "综合价·$M", 2.0, "（输出$10；introductory价已转正）")
add_price(12, "Claude Fable 5", "输出·$M", 50.0)

# ---------- 2) DeepSeek（官方USD peak价，off-peak为半价）----------
ds = {"deepseek-v4-flash": {"输入·缓存命中": 0.014, "输入·缓存未命中": 0.44, "输出": 1.32},
      "deepseek-v4-pro": {"输入·缓存命中": 0.044, "输入·缓存未命中": 1.32, "输出": 3.96}}
for model, items in ds.items():
    for item, usd in items.items():
        cur.execute("SELECT price_usd FROM pricing WHERE platform_id=1 AND model_name=? AND item_type=?", (model, item))
        row = cur.fetchone()
        if row:
            if abs(row[0] - usd) / usd > 0.01:
                upd_price(1, model, item, new_usd=usd, note_suffix=f"(原{row[0]})")
        else:
            add_price(1, model, item, usd)
add_price(1, "deepseek-v4-flash-vision-exp", "输入·缓存命中", 0.014, "（2026-08-21新发布,图片≤384token/张）")
add_price(1, "deepseek-v4-flash-vision-exp", "输入·缓存未命中", 0.44)
add_price(1, "deepseek-v4-flash-vision-exp", "输出", 1.32)

# ---------- 3) OpenAI ----------
upd_price(11, "GPT-5.6 Sol", "综合价·$M", new_usd=4.0, note_suffix="(促销价至少到2026-11-21; 输出短上下文$20)")
upd_price(11, "GPT-5.6 Luna", "综合价·$M", new_usd=0.2)
for m, pin, pout in [("gpt-5.6-cyber", 12.5, 75.0), ("gpt-5.5-cyber", 12.5, 75.0)]:
    add_price(11, m, "输入", pin, "（Daybreak网络安全系列,2026-08-22官网在售）")
    add_price(11, m, "输出", pout)

# ---------- 4) xAI ----------
add_price(14, "grok-build-0.1", "输入", 1.0)
add_price(14, "grok-build-0.1", "输出", 2.0)
add_price(14, "grok-imagine-video-1.5", "视频·每秒", 0.08)
add_price(14, "grok-imagine-image-2.0", "图像·每张", 0.04)
cur.execute("""UPDATE pricing SET notes = COALESCE(notes,'') || ' | 2026-08-22核实: 官方模型页已不再列出'
               WHERE platform_id=14 AND model_name='grok-4.1-fast'""")

# ---------- 5) OpenRouter：>1% 的 67 条变动 + 新增模型 ----------
req = urllib.request.Request("https://openrouter.ai/api/v1/models", headers={"User-Agent": "Mozilla/5.0"})
live = json.loads(urllib.request.urlopen(req, timeout=60).read())["data"]
live_map = {}
for m in live:
    p = m.get("pricing") or {}
    try:
        live_map[m["id"]] = (float(p.get("prompt") or 0) * 1e6, float(p.get("completion") or 0) * 1e6)
    except ValueError:
        pass

rows = cur.execute("""SELECT id, model_name, item_type, price_usd FROM pricing
                      WHERE platform_id=2 AND item_type IN ('输入','输出')""").fetchall()
n_upd = n_new = n_gone = 0
db_slugs = {r[1].replace("-latest", "") for r in rows}
live_slugs = {}
for mid, (pi, po) in live_map.items():
    live_slugs[mid.split("/")[-1]] = (mid, pi, po)
seen = set()
for rid, name, item, old in rows:
    hit = None
    for slug, val in live_slugs.items():
        if slug == name or slug.replace("-latest", "") == name.replace("-latest", ""):
            hit = val
            break
    if not hit:
        continue
    seen.add(hit[0].split("/")[-1])
    newp = hit[1] if item == "输入" else hit[2]
    if old > 0 and abs(newp - old) / old > 0.01:
        cur.execute("UPDATE pricing SET price_usd=?, price_cny=?, collected_at=?, notes=COALESCE(notes,'')||? WHERE id=?",
                    (newp, round(newp * FX, 4), TODAY + " 00:00:00", f" | {TODAY}OpenRouter复核({old})", rid))
        n_upd += 1
for slug, (mid, pi, po) in live_slugs.items():
    base = slug.replace("-latest", "")
    if base not in {s.replace("-latest", "") for s in db_slugs}:
        add_price(2, slug, "输入", pi, "（OpenRouter实时API新增）")
        add_price(2, slug, "输出", po)
        n_new += 1

db.commit()
print(f"OpenRouter: 更新{n_upd}条 新增{n_new}个模型")
print("Anthropic/DeepSeek/OpenAI/xAI 修正已应用")
db.close()
