# 4. 看 token 消耗

每次请求写一个 `ai-service/logs/trace_*.json`，和成本有关的是这几项：

```json
{
  "steps": {"context": 0.01, "route": 0.02, "sql": 1.8, "answer": 2.1},
  "token_usage": {"prompt_tokens": 1200, "completion_tokens": 140, "total_tokens": 1340},
  "llm_calls": 2,
  "route": "rule",
  "sql": "SELECT ..."
}
```

`llm_calls` 是这次调了几次模型。规则命中意图时是 2 次（生成 SQL + 组织回答），
规则判断不了才多一次 planner。

## 4.1 一条命令看平均

```powershell
Get-ChildItem ai-service\logs\trace_*.json |
  ForEach-Object { Get-Content $_.FullName -Raw | ConvertFrom-Json } |
  Measure-Object -Property {$_.token_usage.total_tokens} -Average -Sum
```

## 4.2 逐条看

```powershell
Get-ChildItem ai-service\logs\trace_*.json |
  ForEach-Object {
    $t = Get-Content $_.FullName -Raw | ConvertFrom-Json
    [pscustomobject]@{
      calls = $t.llm_calls
      route = $t.route
      prompt = $t.token_usage.prompt_tokens
      total  = $t.token_usage.total_tokens
      intent = $t.intent
    }
  } | Format-Table
```

## 4.3 三个判断标准

`route` 应该是 `rule`。出现 `model` 说明规则没覆盖这个问法，可以补关键词。

`llm_calls` 应该是 2。出现 3 说明走了 planner，或者触发了一次重试。

`prompt_tokens` 在 1200 上下。超过 2000 说明 schema 或历史变长了，回头看 `prompts/schema.txt` 和 `conversation_memory.MAX_HISTORY`。

## 4.4 估算成本

单次成本 ≈ `total_tokens` × 单价。输入里命中上下文缓存的部分更便宜，
schema 固定在提示词最前面就是为了吃这个折扣。

论文里写“平均每次问答 X token”，数据从上面这条命令来。
