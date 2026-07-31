# Sprint 07：Agent Workflow统一调度

# Sprint Goal

优化 Agent 执行流程，将 SQL 查询、RAG 查询和普通对话统一到 Agent Service 中管理。

解决任务流程分散、上下文关联不足和调试困难等问题。

# Background

前几个 Sprint 已完成：

- Planner 意图识别；
- SQL 查询流程；
- MySQL Tool 数据访问；
- RAG 知识检索。

但是之前不同功能模块独立运行，缺少统一执行入口。

因此本阶段增加 Agent Workflow，通过 Agent Service 统一管理用户请求、任务分发和结果处理。


# Project Structure

优化 Agent 服务调用结构：

```text
ai-service/

├── services/
│   ├── agent_service.py
│   ├── planner_service.py
│   ├── deepseek_service.py
│   └── memory.py
│
└── tools/
    └── mysql_tool.py

文件说明：

agent_service.py
负责统一 Agent 流程入口，协调 Planner、Tool 和 LLM 调用。

Agent Workflow
本阶段将多个功能整合到统一 Agent 流程。

执行流程：
User
↓
Agent Service
↓
Planner
↓
Task Routing
↓
SQL / Chat / Chart / RAG
↓
Answer


# Business Context
在 Conversation Memory 基础上新增 last_entity 和 last_result 字段，记录上一轮的业务实体与查询结果，解决连续数据分析中的上下文衔接问题。

# Agent Logging
增加执行日志，记录用户输入、Intent、SQL 及查询结果，便于流程追踪与调试。

# Problems
当前为单 Agent 架构，Memory 采用本地存储，服务重启后上下文数据全部丢失。

## Next Sprint
Sprint08：RAG Knowledge Enhancement

优化知识库能力：

文档切片；
向量化存储；
FAISS 检索；
Prompt 增强。
