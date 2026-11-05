# Troubleshooting

Sorted by how easy they are to mistake for something else.

## 404, but the key is fine

`base_url` is missing `/v1`. Open `base_url + "/models"` in a browser. A JSON list means host and key are both fine — you wrote the path wrong. Don't regenerate the key. I did that three times once.

## 401

`print(repr(key))`. Copy-paste often leaves a trailing newline or space. Also check the key belongs to the `base_url` you're actually hitting; one shared env var across endpoints is the usual culprit.

## 402 Insufficient Balance

Not a code problem. Check the balance and whether a trial quota expired. Some trial grants show `0` without saying "expired" and still return 402.

## Half an answer, no error

The stream ended mid-sentence with no `finish_reason` and no `[DONE]`. No exception is raised. Your code stores the half answer and you pay full price.

```python
finish = None
for chunk in stream:
    finish = chunk.choices[0].finish_reason or finish
    out.append(chunk.choices[0].delta.content or "")
if finish is None:
    raise RuntimeError("truncated stream — do not treat as success")
```

See also [sse-streaming.html](https://5pcloud.top/sse-streaming.html).

## Constant 429

Fixed-interval retries wake every job on the same second and hammer together. Use backoff with jitter:

```python
time.sleep(min(2 ** attempt * 0.5, 8) + random.random() * 0.4)
```

## Prompt cache never hits

The prefix must be byte-identical. A timestamp in the system prompt kills the hit rate silently. Check the response usage for a cached-token split — don't trust the docs.

## Params silently overwritten

Some gateways inject default `max_tokens` / `temperature` over yours. Same prompt, different style across endpoints: compare the raw response before blaming the model.

## Chinese turns into mojibake on Windows

Write the body to `req.json` and use `--data-binary @req.json` instead of inline `-d`.

## Probing order

`/v1/models` → one non-streaming minimal call → then streaming. Reverse the order and you can't tell address, balance, and truncation apart.

`/v1/models` needs auth on most endpoints — leaving the key blank returns 401 everywhere. `healthcheck.py` in this repo handles that.

More: https://5pcloud.top/faq.html
