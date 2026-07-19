# Sprint 07：Agent Workflow Optimization

> Date：2026-07-18  
> Author：zhongyubing


---

# Sprint Goal


在 Sprint06 NL2SQL 基础上，进一步优化 AI Data Analyst Agent 的任务处理流程。


本 Sprint 重点实现：

- Agent 流程统一管理
- Planner 任务判断
- Conversation Memory
- Agent 日志输出
- 多模块协同工作


提升系统从：

```
Question → SQL → Result
```

升级为：

```
Question

↓

Agent

↓

Planning

↓

Data Query

↓

Analysis

↓

Answer

```


---

# Background


前几个 Sprint 已完成：


## Sprint05

完成：

- Planner
- SQL Generator
- SQL Guard


实现：

```
用户问题

↓

SQL生成

↓

数据库查询

```



---


## Sprint06


完成：

- Schema Prompt
- NL2SQL
- 数据查询分析


但是仍存在：

- 用户上下文无法保存
- Agent 流程分散
- 缺少统一任务控制


因此 Sprint07 增加 Agent Workflow。


---

# Project Architecture


当前架构：


```
                 User

                  │

                  ▼

              FastAPI

                  │

                  ▼

            Agent Service

                  │

        ┌─────────┼─────────┐

        ▼         ▼         ▼

    Planner   SQL Agent   RAG

        │         │

        ▼         ▼

   Intent     MySQL Tool

                  │

                  ▼

               MySQL

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

├── services

│   ├── agent_service.py

│   ├── planner_service.py

│   ├── sql_generator.py

│   └── vector_search.py

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

# Agent Service Design


核心文件：


```
services/agent_service.py
```


负责：

- 接收用户请求
- 调度不同服务
- 管理分析流程
- 返回最终结果


处理流程：


```
User Message

↓

Agent Service

↓

Planner

↓

SQL / RAG / Chat

↓

Result

↓

LLM Response

```


---

# Planning


Agent 根据用户问题判断处理方向。


支持：


```
sql

chart

rag

chat

```


例如：


用户：

```
查询销量最高品牌
```


Planner：


```json
{
 "intent":"sql",
 "table":"dws_brand_sales"
}
```


然后进入 SQL 查询流程。


---

# Conversation Memory


为了支持连续对话，引入：

```python
conversation_history=[]

MAX_HISTORY=10
```


保存：

用户消息：

```python
{
"role":"user",
"content":message
}
```


AI 回复：

```python
{
"role":"assistant",
"content":answer
}
```


限制历史长度：

```python
conversation_history[-MAX_HISTORY:]
```


作用：

让 Agent 能够理解上下文。


例如：


用户：

```
销量最高品牌？
```


AI：

```
Apple
```


用户：

```
它销售额是多少？
```


Agent 可以结合历史理解：

```
它 = Apple
```


---

# Agent Log


增加运行日志。


示例：


```
========== Agent ==========

User:
销量最高品牌？


Intent:
sql


Table:
dws_brand_sales


SQL:
SELECT ...


Result:
[(Apple,100000)]

```


方便：

- 调试
- 排查 SQL 错误
- 展示 Agent 工作过程


---

# Development Summary


本 Sprint 完成：


- [x] 优化 Agent Service
- [x] 集成 Planner
- [x] 增加 Conversation Memory
- [x] 增加 Agent 日志
- [x] 完善 SQL / RAG / Chat 路由


---

# Testing


## Test 1


输入：

```
销量最高品牌？
```


流程：


```
Planner

↓

SQL Generator

↓

MySQL Tool

↓

DeepSeek Analysis

```


返回：

```
品牌销售排行分析
```


测试成功。


---

## Test 2


连续对话：


第一轮：

```
销量最高品牌？
```


第二轮：

```
它卖了多少钱？
```


Agent 根据历史消息理解上下文。


测试成功。


---

# Problems


当前限制：


1. Memory 只保存在当前进程

2. Schema 仍需要维护

3. SQL 复杂分析能力有限

4. Agent 规划能力依赖 Prompt


后续继续优化。


---

# Next Sprint


## Sprint08：RAG + Chart Visualization


目标：


增强 Agent 知识检索和可视化能力。


计划：


- Knowledge Base
- Vector Search
- FAISS
- ECharts 自动生成
- Vue 展示


流程：


```
User

↓

Agent

↓

RAG / SQL

↓

Analysis

↓

Chart

↓

Vue

```


---

# Git Commit


```bash
git add .

git commit -m "feat: optimize agent workflow and memory"

git push
```


---

# Sprint Status


✅ Sprint 07 Completed


Completed:

```
Agent Workflow

Planner Integration

Conversation Memory

Agent Logging

```
