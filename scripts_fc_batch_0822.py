#!/usr/bin/env python3
"""Firecrawl 批量渲染套餐页 → data/fc/<platform>.md"""
import json
import os
import time
import urllib.request

KEY = "fc-ebda30af3d6d46958b8af749faa06e0f"
OUT = "/mnt/d/PROJECT/AI模型价格库/data/fc"
os.makedirs(OUT, exist_ok=True)

TARGETS = {
    "kimi_code": "https://www.kimi.com/code",
    "zhipu_coding": "https://bigmodel.cn/glm-coding",
    "zhipu_pricing": "https://open.bigmodel.cn/pricing",
    "volcano_doubao": "https://www.volcengine.com/product/doubao",
    "trae": "https://www.trae.ai/pricing",
    "chatgpt": "https://chatgpt.com/pricing",
    "google_one_ai": "https://one.google.com/about/google-ai-plans",
    "coze_cn": "https://www.coze.cn/pricing",
    "dify": "https://dify.ai/pricing",
    "elevenlabs": "https://elevenlabs.io/pricing",
    "kling": "https://app.klingai.com/global/membership",
    "manus": "https://manus.im/pricing",
    "lovable": "https://lovable.dev/pricing",
    "windsurf": "https://windsurf.com/pricing",
    "perplexity": "https://www.perplexity.ai/pro",
    "midjourney": "https://www.midjourney.com/imagine/plans",
    "firefly": "https://www.adobe.com/products/firefly/plans.html",
    "huggingface": "https://huggingface.co/pricing",
    "xinghuo": "https://xinghuo.xfyun.cn/deskmember",
    "codebuddy": "https://www.codebuddy.ai/pricing",
}

def scrape(name, url):
    path = f"{OUT}/{name}.md"
    payload = json.dumps({"url": url, "formats": ["markdown"], "waitFor": 5000}).encode()
    req = urllib.request.Request(
        "https://api.firecrawl.dev/v1/scrape", data=payload,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read())
        if d.get("success"):
            md = d["data"]["markdown"]
            with open(path, "w", encoding="utf-8") as f:
                f.write(md)
            return len(md)
        return f"FAIL {str(d)[:120]}"
    except Exception as e:
        return f"ERR {e}"

for i, (name, url) in enumerate(TARGETS.items(), 1):
    size = scrape(name, url)
    print(f"[{i}/{len(TARGETS)}] {name}: {size}", flush=True)
    time.sleep(2)
