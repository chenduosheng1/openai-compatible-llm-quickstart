# -*- coding: utf-8 -*-
"""Ara API 快速接入示例 — 兼容 OpenAI SDK, 改 base_url 即用
站: https://5pcloud.top  注册送 1000 万 token
pip install openai
"""
from openai import OpenAI

client = OpenAI(
    api_key="sk-你的key",           # 注册后在 https://5pcloud.top 令牌页创建
    base_url="https://5pcloud.top/v1"
)

resp = client.chat.completions.create(
    model="deepseek-v4.1-flash",    # 官网2.5-5折; 也有 deepseek-v4-pro / gpt 系列
    messages=[{"role": "user", "content": "你好,介绍一下你自己"}],
)
print(resp.choices[0].message.content)

# 流式
stream = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    messages=[{"role": "user", "content": "写一句诗"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
