#!/bin/bash
# Windows 命令行直接带中文容易乱码，写文件再传最稳
cat > req.json <<'JSON'
{"model":"deepseek-v4.1-flash","messages":[{"role":"user","content":"用一句话解释 SSE"}]}
JSON
curl https://5pcloud.top/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-你的key" \
  --data-binary @req.json
