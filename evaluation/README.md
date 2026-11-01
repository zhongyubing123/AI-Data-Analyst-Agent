# 评测与对比实验

两件事：跑用例看准确率，跑对比看每个设计点值多少。

## 一、用例

`test_cases.json` 共 28 条，分五类：

| 类型 | 条数 | 考什么 |
|---|---|---|
| sql | 14 | 能不能选对表、选对字段 |
| chart | 4 | 能不能产出可渲染的图表配置 |
| rag | 6 | 知识问答是否命中知识库 |
| advice | 4 | 建议是否带数字、是否给出动作 |
| 边界 | 2 | 历史时间问法、不存在的指标 |

每条用例的 `assert` 里可以写四类断言：

`table` 生成的 SQL 里必须出现这张表。
`keywords` 文本里必须出现的词，多个用列表。
`forbid` 不允许出现的词。
`has_number` 回答里必须有数字（只在 full 模式检查）。
`chart` 必须返回带 series 的图表结构（只在 full 模式检查）。
`expect_no_sql` 应该拒绝生成 SQL，用于不存在的指标。

判定是关键词与结构检查，不是语义等价判断。这个局限要在论文里写明。

## 二、跑法

只测语句生成，快、省：

```powershell
$env:MODE="fast"; $env:CASES="test_cases.json"
python evaluation\evaluator.py
```

走完整链路，慢、贵，但能验证图表和回答：

```powershell
$env:MODE="full"; $env:CASES="test_cases.json"
python evaluation\evaluator.py
```

只看前几条调试：

```powershell
$env:MODE="fast"; $env:LIMIT="5"; python evaluation\evaluator.py
```

结果写到 `evaluation/results/{模式}_{用例集}.json`，里面按类型分组统计准确率。

## 三、对比实验

`ablation.py` 用同样十二个问题，换三种配置各跑一遍：

| 配置 | 含义 |
|---|---|
| baseline | 规则路由 + 字段校验，默认配置 |
| `ROUTE=model` | 跳过关键词规则，每次都由模型判断意图 |
| `GUARD=off` | 跳过字段存在性校验 |

```powershell
python evaluation\ablation.py
```

它会打印每组的准确率、平均 token、平均调用次数、异常数，并算出相对 baseline 的变化，结果写进 `results/ablation.json`。

十二个问题 × 三组配置，大约七十次模型调用，五分钟左右。

## 四、数字怎么用

论文里最有说服力的三句：

规则路由把平均调用次数从 3 降到 2，平均 token 下降三成左右。数据来自 `ROUTE=model` 那一行。

关掉字段校验后，跨表借用字段不再被拦截，执行阶段的报错次数上升。数据来自 `GUARD=off` 那一行。

fast 与 full 两种模式的准确率差距，反映回答环节引入的额外失败。用同一条用例集跑两遍相减。

## 五、注意

跑评测前确认 MySQL 五张汇总表有数据，`python ai-service/check_data.py` 能打出数字。

评测会产生真实模型调用，别在没余额的时候跑 full。

`GUARD=off` 只在评测里用，跑完记得清环境变量，否则会带进正常使用：

```powershell
Remove-Item Env:ROUTE, Env:GUARD, Env:MODE, Env:CASES -ErrorAction SilentlyContinue
```
