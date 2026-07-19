# Sprint 05：Planner + NL2SQL + SQL Guard

> Date：2026-07-18  
> Author：zhongyubing


---

# Sprint Goal


实现 AI Data Analyst Agent 的自动数据查询流程。


本 Sprint 引入：

- Planner 意图识别
- SQL Generator
- SQL Guard


使用户能够通过自然语言描述业务需求，Agent 自动生成 SQL，并通过 MySQL Tool 查询真实业务数据。


---

# Background


前几个 Sprint 已完成：


## Sprint01

完成：

- FastAPI 服务
- DeepSeek API 接入


流程：

```
User

↓

FastAPI

↓

DeepSeek
```



---


## Sprint03

完成：

- MySQL Tool
- Python 数据库访问能力


流程：

```
Python

↓

MySQL Tool

↓

MySQL

```



---


## Sprint04

完成：

- Agent Service

负责协调：

- LLM
- Database Tool


但是之前的数据查询流程仍然需要固定 SQL。


例如：

```python
sql = """
SELECT *
FROM dws_brand_sales
LIMIT 10;
"""
```


无法根据用户问题动态生成查询。


因此 Sprint05 目标：

实现自然语言到 SQL 的转换。


---

# Project Architecture


升级后的 Agent 流程：


```
                 User

                  │

                  ▼

              FastAPI

                  │

                  ▼

            Agent Service

                  │

                  ▼

              Planner

                  │

                  ▼

          SQL Generator

                  │

                  ▼

             SQL Guard

                  │

                  ▼

            MySQL Tool

                  │

                  ▼

              MySQL

                  │

                  ▼

           Query Result

                  │

                  ▼

          DeepSeek Analysis

                  │

                  ▼

              Answer

```


---

# Project Structure


新增：


```
ai-service

│

├── app.py

│

├── services

│   ├── agent_service.py

│   ├── planner_service.py

│   └── sql_generator.py

│

├── tools

│   └── mysql_tool.py

│

├── security

│   └── sql_guard.py

│

├── prompts

│   ├── system_prompt.txt

│   ├── schema.txt

│   └── planner_prompt.txt

│

└── .env

```


---

# Core Implementation


## 1. Planner


新增：

```
services/planner_service.py
```


功能：

分析用户问题。


输出：

```json
{
 "intent":"sql",
 "table":"dws_brand_sales",
 "reason":"查询品牌销售排名"
}
```


支持意图：


```
sql

chart

rag

chat
```


---

# 2. SQL Generator


新增：

```
services/sql_generator.py
```


功能：

根据：

- 用户问题
- 数据库 Schema


生成 SQL。


例如：

用户：

```
查询销量最高的品牌
```


生成：

```sql
SELECT
brand,
SUM(sales_amount) AS total_sales
FROM dws_brand_sales
GROUP BY brand
ORDER BY total_sales DESC
LIMIT 10;
```


---

# 3. SQL Guard


新增：

```
security/sql_guard.py
```


功能：

限制 AI 生成危险 SQL。


禁止：

```
DELETE

UPDATE

DROP

ALTER

INSERT

CREATE

TRUNCATE
```


只允许：

```sql
SELECT
```


提高数据库安全性。


---

# 4. MySQL Tool


调用：

```python
execute_query(sql)
```


执行 AI 生成 SQL。


返回真实数据库结果。


---

# Development Summary


本 Sprint 完成：


- [x] 实现 Planner 意图识别
- [x] 实现 SQL 自动生成
- [x] 增加 SQL 安全校验
- [x] Agent 接入 MySQL Tool
- [x] 完成自然语言查询数据库流程


---

# Example


用户输入：


```
查询销量最高的品牌
```


Agent 流程：


```
用户问题

↓

Planner

↓

intent=sql

↓

SQL Generator

↓

SELECT SQL

↓

SQL Guard

↓

MySQL Tool

↓

查询结果

↓

DeepSeek总结

↓

回答用户

```


---

# Technical Stack


- Python 3.11
- FastAPI
- DeepSeek API
- Prompt Engineering
- PyMySQL
- MySQL


---

# Key Learning


本 Sprint 学习内容：


## 1. NL2SQL 基础


理解：

自然语言

↓

SQL

↓

数据库结果


的转换过程。


---

## 2. Prompt Engineering


通过：

- schema prompt
- planner prompt


提高模型生成 SQL 的准确性。


---

## 3. SQL 安全控制


理解 AI 生成 SQL 存在风险，需要增加安全校验层。


---

# Problems


当前版本仍存在：

- SQL 生成依赖 Prompt
- Schema 信息需要维护
- 多表复杂查询能力有限


后续继续优化：

- RAG Schema 检索
- 动态 Schema 获取
- 查询结果可视化


---

# Next Sprint


## Sprint06：RAG Knowledge Enhancement


目标：


利用向量数据库增强 Agent 对业务知识的理解。


实现：

- Markdown Knowledge 文档
- Embedding
- FAISS 向量搜索
- Schema 检索增强


流程：


```
User

↓

Agent

↓

RAG Knowledge

↓

SQL Generator

↓

MySQL

↓

Answer

```


---

# Git Commit


```bash
git add .

git commit -m "feat: implement planner and nl2sql workflow"

git push
```


---

# Sprint Status


✅ Sprint 05 Completed


Completed:

```
Planner

SQL Generator

SQL Guard

NL2SQL V1

```
