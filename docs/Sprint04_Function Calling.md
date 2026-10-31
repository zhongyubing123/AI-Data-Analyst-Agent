> 状态：未采用。原计划用大模型原生 Function Calling，实际实现为自定义 Tool 调用流程，见 services/router.py 与 services/sql_service.py。

# Sprint 04：Function Calling
# Sprint Goal

引入 Agent Service 作为流程控制层，将用户问题、数据库工具和大模型连接起来，实现基础 Agent 数据分析流程。

本阶段完成 MySQL Tool 接入 Agent，并将查询结果传递给 DeepSeek 生成分析结果。

当前版本为 Tool 调用流程 V1，暂未使用大模型原生 Function Calling。


# Background

前几个 Sprint 已完成：

- FastAPI 与 DeepSeek API 连接；
- Prompt 和 Schema 管理；
- MySQL Tool 数据查询能力。

但是模型调用和数据库查询仍然是独立模块。

因此增加 Agent Service 作为中间层，负责协调用户请求、数据库查询和 AI 分析流程。


# Project Structure

新增：

```text
ai-service/
│
├── services/
│   ├── llm_client.py
│   ├── deepseek_service.py
│   └── agent_service.py
│
├── tools/
│   └── mysql_tool.py
│
└── app.py
```

文件说明：

**agent_service.py**

负责组织 Agent 执行流程，包括调用 MySQL Tool、处理查询结果以及调用 DeepSeek。


# Agent Service

新增：

```text
services/agent_service.py
```

主要负责：

- 接收用户问题；
- 调用 MySQL Tool 查询数据；
- 将查询结果传递给 DeepSeek；
- 返回最终分析结果。


通过 Agent Service 将接口层、数据访问层和模型调用流程连接起来。


# Agent Flow

当前执行流程：

```text
User

↓

FastAPI

↓

Agent Service

↓

MySQL Tool

↓

MySQL

↓

DeepSeek

↓

Answer
```

Agent Service 负责协调：

- 用户请求；
- 数据库查询；
- AI 分析。


# Architecture

```text
User
 │
FastAPI
 │
Agent Service
 │
 ├── MySQL Tool
 │       │
 │       ▼
 │     MySQL
 │
 └── DeepSeek Service
          │
          ▼
       Answer
```


# Development Summary

本阶段完成 Agent Service 开发，实现基础 Tool 调用流程，将数据库查询能力接入 AI 分析流程。

为后续 Planner、Function Calling 和 NL2SQL 功能开发提供基础。


# Technical Stack

- Python
- FastAPI
- DeepSeek API
- PyMySQL
- MySQL


# Next Sprint

## Sprint 05：Planner + NL2SQL

下一阶段增加用户意图判断和 SQL 自动生成能力。

通过 Planner 分析用户问题，并结合 SQL Generator 和 MySQL Tool 完成自动查询。