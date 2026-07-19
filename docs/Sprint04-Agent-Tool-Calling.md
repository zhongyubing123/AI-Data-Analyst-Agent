# Sprint 04：Agent Tool Calling V1

> Date：2026-07-17  
> Author：zhongyubing


---

# Sprint Goal


引入 Agent Service 作为 AI Data Analyst Agent 的核心流程控制层，实现用户问题、数据库工具和大模型之间的协同工作。


本 Sprint 主要完成：

- Agent Service 创建
- MySQL Tool 接入 Agent 流程
- 数据库查询结果传递给 DeepSeek
- 基于真实业务数据生成 AI 分析结果


本阶段实现的是 Agent 工具调用流程 V1，并非大模型原生 Function Calling。


---

# Background


前三个 Sprint 已完成：


## Sprint01

完成：

- FastAPI 服务搭建
- DeepSeek API 接入


基础流程：

```
User

↓

FastAPI

↓

DeepSeek
```



---


## Sprint02


完成：

- Prompt Engineering
- System Prompt
- Schema Prompt


提升模型对业务数据结构的理解能力。


---


## Sprint03


完成：

- MySQL Tool
- 数据库连接封装
- SQL 查询能力


流程：

```
Python

↓

MySQL Tool

↓

MySQL

```


---


但是目前：

```
FastAPI

↓

DeepSeek
```


和：

```
MySQL Tool

↓

MySQL
```


仍然是独立模块。


因此需要增加 Agent Service，对用户请求、数据库查询和 AI 分析流程进行统一管理。


---

# Project Architecture


加入 Agent 后：


```
                 User

                  │

                  ▼

              FastAPI

                  │

                  ▼

            Agent Service

          ┌────────┴────────┐

          ▼                 ▼

   MySQL Tool        DeepSeek Service

          │                 ▲

          ▼                 │

        MySQL        Query Result

```


Agent Service 负责：

- 接收用户问题
- 判断业务处理流程
- 调用数据库工具
- 获取真实数据
- 调用 DeepSeek 生成分析结果


---

# Project Structure


当前结构：


```
ai-service

│

├── app.py

│

├── prompts

│

├── services

│     ├── llm_client.py

│     ├── agent_service.py

│

├── tools

│     └── mysql_tool.py

│

├── security

│

└── .env

```


新增：

```
services/agent_service.py
```


---

# Agent Design


新增：

```
services/agent_service.py
```


主要职责：

- 组织 AI 分析流程
- 调用 MySQL Tool
- 调用 DeepSeek Service
- 返回最终结果


Agent 作为业务协调层，将：

```
FastAPI

数据库

LLM

```

进行连接。


---

# Data Flow


当前执行流程：


```
用户输入

↓

FastAPI

↓

Agent Service

↓

MySQL Tool

↓

MySQL

↓

Database Result

↓

DeepSeek Service

↓

自然语言回答

↓

用户

```


---

# Development


## 1. 创建 Agent Service


新增：

```
services/agent_service.py
```


用于封装 Agent 核心逻辑。


避免将所有业务代码直接写入：

```
app.py
```


提高代码可维护性。


---

## 2. 调用 MySQL Tool


Agent 调用：


```python
execute_query(sql)
```


获取数据库真实查询结果。


例如：

数据库返回：

```
brand      sales

Nike       23500

Apple      22000
```


---

## 3. 调用 DeepSeek


查询结果作为上下文传递给 DeepSeek。


模型根据：

- 用户问题
- 数据库结果


生成自然语言分析。


---

# Development Summary


本 Sprint 完成：


- [x] 创建 Agent Service
- [x] 整合 MySQL Tool
- [x] 实现数据库查询结果传递
- [x] 实现 AI 基于真实数据分析
- [x] 完成 Agent 基础流程


---

# Technical Stack


- Python 3.11
- FastAPI
- DeepSeek API
- PyMySQL
- python-dotenv


---

# Architecture Evolution


## Sprint01


```
User

↓

FastAPI

↓

DeepSeek

```



---


## Sprint03


```
Python

↓

MySQL Tool

↓

MySQL

```



---


## Sprint04


```
User

↓

FastAPI

↓

Agent Service

        │

        ├──── MySQL Tool

        │          │

        │          ▼

        │        MySQL

        │

        ▼

   DeepSeek Service

        │

        ▼

      Answer

```


---

# Key Learning


本 Sprint 学习内容：


## 1. Agent 工作模式


理解 Agent 在 AI 应用中的作用：


```
User Request

↓

Agent

↓

Tool / LLM

↓

Result

```


---

## 2. Tool 集成思想


理解：

LLM 不直接访问外部系统，而通过 Tool 获取数据。


---

## 3. 服务模块化设计


将：

- HTTP 接口
- Agent逻辑
- 数据访问


进行拆分，提高项目可维护性。


---

# Next Sprint


## Sprint05：Planner + NL2SQL


目标：


让 Agent 根据用户问题自动判断业务意图，并生成对应 SQL 查询。


流程：


```
User Question

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

DeepSeek Analysis

↓

Answer

```


实现：

- 意图识别
- SQL 自动生成
- SQL 安全校验
- 自动数据查询


---

# Git Commit


```bash
git add .

git commit -m "feat: add agent service workflow"

git push
```


---

# Sprint Status


✅ Sprint 04 Completed

```
Agent Service

MySQL Tool Integration

DeepSeek Analysis

Completed
```
