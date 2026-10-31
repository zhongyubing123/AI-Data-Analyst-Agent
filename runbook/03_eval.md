# 3. 评测

## 3.1 安全自测（零成本）

```bash
cd C:\Users\zhong\Desktop\AI-Data-Analyst-Agent
python evaluation/test_guard.py
```

期望：`通过：危险 12 条全拦，正常 3 条放行`。

## 3.2 业务问题集（12 条，约 12 次调用）

```powershell
$env:MODE="fast"; $env:CASES="biz_cases.json"
python evaluation\evaluator.py
```

结果在 `evaluation/results/fast_biz_cases_results.json`，看 `accuracy`。

逐条看哪条没过：

```powershell
$r = Get-Content evaluation\results\fast_biz_cases_results.json -Raw | ConvertFrom-Json
$r.results | Where-Object { -not $_.success } | Select-Object id, error, sql
```

## 3.3 完整链路（10 条，约 40 次调用）

```powershell
$env:MODE="full"; $env:CASES="agent_test_cases.json"
python evaluation\evaluator.py
```

## 3.4 清环境变量

```powershell
Remove-Item Env:MODE -ErrorAction SilentlyContinue
Remove-Item Env:CASES -ErrorAction SilentlyContinue
```

## 3.5 常见失败

`accuracy` 低但每条都有 SQL：多半是表名对但字段名不对，核对 `prompts/schema.txt` 和 `mysql_all.sql` 的列名。

`SQL执行失败`：冒号后面是真实原因，通常是列名拼错或表没建。

`NO_AVAILABLE_FIELD`：问题要的指标表里真没有，属于正常回答，不是崩溃。
