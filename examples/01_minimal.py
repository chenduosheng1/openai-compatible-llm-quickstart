"""最小调用：换 base_url 就能换供应商。"""
from openai import OpenAI

client = OpenAI(api_key="sk-你的key", base_url="https://5pcloud.top/v1", timeout=30)
r = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    messages=[{"role": "user", "content": "回复两个字：成功"}],
)
print(r.choices[0].message.content)
