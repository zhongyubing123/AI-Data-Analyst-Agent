# Sprint 05：Planner + NL2SQL + SQL Guard

# Sprint Goal

实现自然语言查询数据库能力。

本阶段增加 Planner、SQL Generator 和 SQL Guard，使 Agent 能够根据用户问题生成 SQL，并查询 MySQL 数据。

# Background

前几个 Sprint 已完成：

- Agent Service 流程搭建；
- MySQL Tool 数据查询能力。

但是当前查询仍依赖固定 SQL，无法根据用户需求动态生成。

因此本阶段增加 Planner 和 NL2SQL 流程，让用户可以通过自然语言进行数据查询。

# Project Structure

新增 Planner、SQL 生成和 SQL 校验相关文件：

```text
ai-service/
│
├── services/
│   ├── planner_service.py
│   └── sql_generator.py
│
├── security/
│   └── sql_guard.py
│
└── prompts/
    └── planner_prompt.txt
```

文件说明：

**planner_service.py**

负责分析用户问题，判断当前任务类型。

**sql_generator.py**

负责结合用户问题和 Schema 信息生成 SQL。

**sql_guard.py**

负责检查生成 SQL，限制危险数据库操作。

# Planner

用户问题类型不同，需要先判断当前任务类型。

因此增加 Planner，对用户输入进行意图识别。

输出：

```json
{
 "intent":"sql",
 "table":"dws_brand_sales",
 "reason":"查询品牌销售排名"
}
```

当前支持：

```text
sql
chart
rag
chat
```

Planner 根据判断结果，将请求分发到对应处理流程。

# SQL Generator

由于 LLM 不了解数据库结构，因此需要提供 Schema 信息辅助生成 SQL。

SQL Generator 根据：

- 用户问题；
- 数据库 Schema；

生成查询语句。

流程：

```text
用户问题
↓
SQL Generator
↓
SQL
↓
MySQL Tool
↓
查询结果
```

例如：

用户输入：

```text
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

# SQL Guard

由于 AI 生成 SQL 存在安全问题，因此增加 SQL Guard 对 SQL 进行校验。

当前限制：

禁止：

```text
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

避免 Agent 执行修改数据库操作。

# Agent Flow

当前 Agent 查询流程：

```text
User
↓
FastAPI
↓
Agent Service
↓
Planner
↓
SQL Generator
↓
SQL Guard
↓
MySQL Tool
↓
Database Result
↓
DeepSeek
↓
Answer
```


# Development Summary

本阶段完成 Planner、SQL Generator 和 SQL Guard 开发，实现自然语言查询数据库流程。

通过增加意图判断和 SQL 自动生成能力，为后续 RAG、Function Calling 等 Agent 功能开发提供基础。

# Next Sprint

## Sprint 06：RAG Knowledge Enhancement

下一阶段增加业务知识检索能力。

通过构建知识库和向量检索，使模型能够理解业务指标和字段含义。