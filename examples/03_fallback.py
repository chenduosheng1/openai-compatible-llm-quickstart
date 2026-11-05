"""双通道：官方做基准，备用只在 401/超时顶上。"""
from openai import OpenAI, APIError, APITimeoutError

ENDPOINTS = [
    ("https://api.deepseek.com/v1", "deepseek-chat", "sk-官方key"),
    ("https://5pcloud.top/v1", "deepseek-v4.1-flash", "sk-备用key"),
]

def chat(messages):
    for base, model, key in ENDPOINTS:
        try:
            c = OpenAI(api_key=key, base_url=base, timeout=20)
            return c.chat.completions.create(model=model, messages=messages)
        except (APITimeoutError, APIError):
            continue
    raise RuntimeError("两条通道都不通")

if __name__ == "__main__":
    print(chat([{"role": "user", "content": "回复：通了"}]).choices[0].message.content)
