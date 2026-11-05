"""流式输出：必须查 finish_reason，断流别当成功。"""
from openai import OpenAI

client = OpenAI(api_key="sk-你的key", base_url="https://5pcloud.top/v1", timeout=30)
stream = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    messages=[{"role": "user", "content": "写一句诗"}],
    stream=True,
)

finish = None
for chunk in stream:
    finish = chunk.choices[0].finish_reason or finish
    print(chunk.choices[0].delta.content or "", end="", flush=True)

if finish is None:
    raise RuntimeError("断流了，别存，重跑")
