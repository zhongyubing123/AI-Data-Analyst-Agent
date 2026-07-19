# Sprint10：AI Data Visualization Enhancement


> Date：2026-07-18  
> Author：zhongyubing


---

# Sprint Goal


在 AI Data Analyst Agent 基础上，增加数据可视化能力。


前几个 Sprint 已完成：

- NL2SQL
- MySQL 数据查询
- RAG知识检索
- SQL安全检查


但是当前系统主要返回文本分析结果。


本 Sprint 目标：

让 Agent 根据查询结果自动生成 ECharts 配置，使用户能够通过图表理解业务数据。


---

# Background


当前流程：


```
User

↓

Agent

↓

SQL Query

↓

MySQL

↓

Analysis Result

```


升级后：


```
User

↓

Agent

↓

SQL Query

↓

MySQL

↓

Chart Service

↓

ECharts Option

↓

Vue3 Rendering

```


---

# Project Architecture


```
              User

               │

               ▼

          Agent Service

               │

        ┌──────┴──────┐

        ▼             ▼

    SQL Query     Chart Request

        │             │

        ▼             ▼

      MySQL      Chart Service

        │             │

        └──────┬──────┘

               ▼

          ECharts JSON

               │

               ▼

              Vue3

```


---

# Project Structure


```
ai-service


├── services

│

├── agent_service.py

├── chart_service.py

├── sql_generator.py


├── tools

│

└── mysql_tool.py


├── security

│

└── sql_guard.py


└── app.py

```


---

# Chart Request Detection


在：

```
services/agent_service.py
```


增加图表需求判断。


例如：

用户输入：

```
生成品牌销售图表
```


Agent识别：


```
任务类型：

chart

```


进入可视化流程。


---

# SQL Data Query


根据用户需求查询业务数据。


示例：


```sql
SELECT

brand,

SUM(sales_amount) AS sales

FROM dws_brand_sales

GROUP BY brand

ORDER BY sales DESC

LIMIT 10;
```


获取品牌销售排行。


---

# SQL Security Check


SQL执行前经过：

```
SQL Guard
```


流程：


```
SQL

↓

check_sql()

↓

安全检查

↓

MySQL

```


保证：

- 只执行查询SQL
- 防止危险数据库操作


---

# Result Processing


MySQL返回结果：


```python
[
{
"brand":"戴尔",
"sales":26230041.46
}
]
```


转换：

```
Decimal

↓

float

```


保证：

```
JSON Serializable
```


---

# Chart Service


新增：


```
services/chart_service.py
```


功能：


- 接收查询结果
- 根据数据生成 ECharts option
- 返回前端可解析 JSON


输入：


```json
[
{
"brand":"戴尔",
"sales":26230041
}
]
```


输出：


```json
{
"title":{
"text":"品牌销售排行"
},

"xAxis":{
"type":"category"
},

"series":[
{
"type":"bar",
"data":[26230041]
}
]
}
```


---

# Testing


## Test 1


输入：

```
生成品牌销售图表
```


执行流程：

```
用户请求

↓

Agent识别图表需求

↓

SQL查询

↓

SQL Guard

↓

MySQL

↓

Chart Service

↓

ECharts JSON

```


返回：

```
品牌销售柱状图
```


测试成功。


---

# Development Problems


## Problem 1：SQL Guard误判 DESC


错误：


```
ORDER BY sales DESC
```


被识别为：

```
DESC table
```


原因：

简单关键词匹配。


解决：

使用正则判断：

```
DESC\s+\w+
```


避免影响：

```sql
ORDER BY xxx DESC
```


---

## Problem 2：Decimal JSON解析失败


MySQL金额字段：

```
Decimal
```


无法直接：

```python
json.dumps()
```


解决：


转换：

```python
float(value)
```


---

## Problem 3：DeepSeek返回Markdown


模型返回：

```
```json
{}
```
```


导致：

```
json.loads()
```

失败。


解决：

Prompt增加：

```
Only return JSON.
Do not use Markdown.
```


---

# Development Summary


本 Sprint 完成：


- [x] 图表需求识别
- [x] SQL查询数据
- [x] SQL安全检查
- [x] 查询结果转换
- [x] ECharts配置生成
- [x] AI辅助数据可视化


---

# Technical Stack


- Python
- FastAPI
- DeepSeek API
- MySQL
- ECharts
- Vue3


---

# Key Learning


## 1. 数据分析结果可视化


数据：

```
Database Result
```


转换：

```
Chart Option
```


最终：

```
Visualization
```


---

## 2. AI与BI结合


Agent 不仅能够：

- 查询数据

还能够：

- 生成图表
- 辅助分析


---

# Current Limitations


目前：

- 图表类型较少
- 图表推荐规则简单
- 缺少 Dashboard 管理


后续可继续优化。


---

# Next Sprint


## Sprint11：Vue3 AI Chat Visualization


目标：

完成前端展示。


计划：

- Vue3聊天窗口
- ECharts动态渲染
- AI回答展示
- 图文混合展示


最终形成：

```
AI Chat + Visualization
```


---

# Git Commit


```bash
git add .

git commit -m "feat: add ai chart generation service"

git push
```


---

# Sprint Status


✅ Sprint10 Completed


Completed:

```
Chart Detection

Chart Service

ECharts Option Generation

```

