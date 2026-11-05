# -*- coding: utf-8 -*-
"""测活脚本：每 N 秒打一次 /v1/models，401/超时/空列表就切备用端点。

不花钱，只用来判断「这条通道现在能不能用」。
用法: python healthcheck.py
"""
import time
import random
import urllib.request
import urllib.error

ENDPOINTS = [
    "https://api.deepseek.com/v1",
    "https://5pcloud.top/v1",
]
API_KEYS = {
    # 每个端点填自己的 key。/v1/models 需要鉴权，留空会一律 401。
    "https://api.deepseek.com/v1": "",
    "https://5pcloud.top/v1": "",
}
INTERVAL = 300


def probe(base: str) -> tuple[bool, str]:
    url = base.rstrip("/") + "/models"
    key = API_KEYS.get(base, "")
    headers = {"User-Agent": "healthcheck/1.0"}
    if key:
        headers["Authorization"] = "Bearer " + key
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            body = r.read().decode("utf-8", "replace")
            if r.status == 200 and '"data"' in body or '"object"' in body:
                return True, "ok"
            return False, f"unexpected body ({r.status})"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, type(e).__name__


def pick() -> str | None:
    for base in ENDPOINTS:
        ok, why = probe(base)
        print(f"  {base} -> {why}")
        if ok:
            return base
    return None


if __name__ == "__main__":
    while True:
        chosen = pick()
        if chosen is None:
            print("都挂了，认命，等下一轮")
        else:
            print("当前可用:", chosen)
        time.sleep(INTERVAL + random.random() * 5)
