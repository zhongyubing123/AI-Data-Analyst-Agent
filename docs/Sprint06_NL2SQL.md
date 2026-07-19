# Sprint 06：NL2SQL Enhancement

> Date：2026-07-18  
> Author：zhongyubing


---

# Sprint Goal


提升 AI Data Analyst Agent 的自然语言数据查询能力。


本 Sprint 引入数据库 Schema 信息，使大语言模型能够理解：

- 数据库名称
- 数据表结构
- 字段含义


并根据用户业务问题自动生成 SQL 查询。


实现：

```
Natural Language

↓

SQL

↓

Database Query

↓

AI Analysis

```


---

# Background


前几个 Sprint 已完成：


## Sprint03

完成：

- MySQL Tool
- 数据库访问封装


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

- 用户请求
- LLM
- 数据库工具


---


## Sprint05


完成：

- Planner
- SQL Generator
- SQL Guard


实现：

```
User Question

↓

Intent Recognition

↓

SQL Generation

↓

SQL Validation

```


---


但是模型生成 SQL 时需要知道真实数据库结构。


如果缺少 Schema 信息：

模型可能生成不存在的：

```
dws_hot_items

item_sales

goods_sales

```


导致 SQL 执行失败。


因此 Sprint06 增加 Schema 注入。


---

# Project Architecture


升级后的流程：


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

          Database Schema

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


当前结构：


```
ai-service

│

├── app.py

│

├── prompts

│   ├── system_prompt.txt

│   ├── schema.txt

│   └── planner_prompt.txt

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

└── .env

```


---

# Core Implementation


## 1. Database Schema


新增：


```
prompts/schema.txt
```


用于描述数据库结构。


例如：


```
Database:

ecommerce


Tables:


dws_brand_sales

Columns:

brand

sales_amount

buy_count


dws_category_sales

Columns:

category

sales_amount


dws_item_hot

Columns:

item_name

buy_count


dws_user_active

Columns:

user_id

active_days

buy_count

```


作用：


让模型了解：

- 哪些表存在
- 哪些字段可以查询
- 字段业务含义


减少 SQL 幻觉。


---

# 2. Schema 注入 Prompt


系统 Prompt 中加入 Schema：


```
System Prompt

+

Database Schema

```


发送给 DeepSeek。


模型能够根据真实数据库结构生成 SQL。


---

# 3. SQL Generation


用户输入：


```
查询销量最高的品牌
```


模型生成：


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

# 4. SQL Validation


生成 SQL 后进入：

```
sql_guard.py
```


检查危险操作。


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


保证数据库安全。


---

# 5. Execute SQL


通过：

```python
execute_query(sql)
```


调用 MySQL Tool。


获取真实业务数据。


---

# 6. Result Analysis


数据库返回结果：


```
Apple 853000

Huawei 801234

Xiaomi 650000

```


发送给 DeepSeek。


生成自然语言分析。


---

# Development Problems


## 问题一：Schema 表名错误


错误：

```
dws_hot_items
```


实际：

```
dws_item_hot
```


导致：

```
Table doesn't exist
```


解决：

同步：

```
schema.txt

数据库真实表结构
```



---

## 问题二：模型生成不存在字段


原因：

Schema 信息不足。


例如：

模型生成：

```sql
item_sales
```


但数据库不存在。


解决：

完善：

- Table
- Column
- Description


---

## 问题三：SQL 执行异常


问题：

SQL 错误导致 FastAPI 返回：

```
500 Internal Server Error
```


解决：

增加异常处理：


```python
try:

except Exception as e:
```


将错误返回 Agent。


---

# Testing


## Test 1


输入：

```
销量最高品牌有哪些？
```


生成：

```sql
SELECT
brand,
sales_amount
FROM dws_brand_sales
ORDER BY sales_amount DESC
LIMIT 10;
```


成功执行。


---

## Test 2


输入：

```
销量最高商品类别？
```


生成：


```sql
SELECT *
FROM dws_category_sales
ORDER BY sales_amount DESC
LIMIT 1;
```


成功执行。


---

## Test 3


输入：

```
购买次数最多的用户？
```


生成：

```sql
SELECT
user_id,
buy_count
FROM dws_user_active
ORDER BY buy_count DESC
LIMIT 1;
```


成功执行。


---

# Development Summary


本 Sprint 完成：


- [x] 增加数据库 Schema 描述
- [x] Schema 注入 Prompt
- [x] 提升 SQL 自动生成准确率
- [x] 完善 NL2SQL 流程
- [x] 增加 SQL 异常处理
- [x] 完成自然语言查询数据库闭环


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


## 1. NL2SQL


理解：

```
自然语言

↓

SQL

↓

数据查询

```


---

## 2. Schema Prompt Engineering


通过数据库结构约束模型输出。


降低：

- 表名错误
- 字段错误
- SQL 幻觉


---

## 3. AI 数据分析流程


理解完整链路：


```
User

↓

LLM

↓

SQL

↓

Database

↓

Result

↓

Analysis

```


---

# Problems


当前限制：

- Schema 需要人工维护
- SQL 复杂 JOIN 能力有限
- 缺少查询历史记录
- 缺少结果缓存


后续继续优化。


---

# Next Sprint


## Sprint07：RAG Knowledge Enhancement


目标：

使用 RAG 增强 Agent 对业务知识和数据库结构的理解。


实现：

- Knowledge Markdown
- Embedding
- FAISS Search
- Context Retrieval


流程：


```
User

↓

RAG Retrieval

↓

Agent

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

git commit -m "feat: enhance nl2sql with schema prompt"

git push
```


---

# Sprint Status


✅ Sprint 06 Completed


Completed:

```
Schema Prompt

NL2SQL

SQL Validation

Database Query

AI Analysis

```
