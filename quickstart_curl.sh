#!/bin/bash
# curl 直接调用示例
curl https://5pcloud.top/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-你的key" \
  -d '{
    "model": "deepseek-v4.1-flash",
    "messages": [{"role":"user","content":"你好"}]
  }'
