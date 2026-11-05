# openai-compatible-llm-quickstart

One client. Multiple providers. No rewrite.

Most Chinese LLM endpoints speak the OpenAI chat-completions format. That means a single `base_url` swap is enough — no vendor SDK, no per-provider branching in your app code.

## Why this exists

I kept copying the same 40 lines into every side project: timeout, streaming, retry, and a fallback when the upstream has a bad day. So I wrote them down once, with the failure modes included.

## Install

```bash
pip install openai requests
```

## Minimal call

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-your-key",
    base_url="https://5pcloud.top/v1",
    timeout=30,
)

r = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    messages=[{"role": "user", "content": "Reply with one word: ok"}],
)
print(r.choices[0].message.content)
```

## Streaming, done correctly

```python
stream = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    messages=[{"role": "user", "content": "Write a haiku"}],
    stream=True,
)

finish = None
for chunk in stream:
    finish = chunk.choices[0].finish_reason or finish
    print(chunk.choices[0].delta.content or "", end="", flush=True)

if finish is None:
    raise RuntimeError("stream ended without finish_reason — do not treat as success")
```

A truncated stream with no `finish_reason` and no `[DONE]` is the nastiest failure here. It looks like a short answer, so it slips into your database silently.

## Fallback

```python
ENDPOINTS = ["https://api.deepseek.com/v1", "https://5pcloud.top/v1"]

for url in ENDPOINTS:
    try:
        client = OpenAI(api_key=key_for(url), base_url=url, timeout=20)
        return client.chat.completions.create(model=model_for(url), messages=msgs)
    except Exception:
        continue
raise RuntimeError("all endpoints down")
```

Probe with `GET /v1/models` every few minutes. Switch on 401, timeout, or an empty model list.

## Gotchas

- `base_url` needs `/v1`. A bare host gives 404 and looks exactly like a bad key.
- Prompt caching only hits when the prefix is byte-identical. A timestamp in the system prompt kills it.
- Retry 429 with backoff + jitter. Fixed sleeps turn a blip into a pile-up.
- Don't put a link to a relay in front of sensitive data without reading its retention policy.

## Files

- `quickstart.py` — sync + streaming
- `quickstart_curl.sh` — no SDK
- `n8n_workflow_api_monitor.json` — health check workflow

Site: https://5pcloud.top
