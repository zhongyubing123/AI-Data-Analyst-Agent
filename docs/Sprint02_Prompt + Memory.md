# Sprint 02：Prompt + Memory

# Sprint Goal

引入 Prompt Engineering，将系统 Prompt 从代码中分离管理，并优化 DeepSeek 调用流程，为后续 Agent 功能开发提供基础。

# Background

Sprint01 已完成 FastAPI 与 DeepSeek API 的连接，实现了基础对话功能。

随着项目功能增加，需要让模型了解更多业务信息，因此本阶段增加 Prompt 管理和简单上下文记录，提高模型回答效果。

# Project Structure

新增 Prompt 和模型服务相关文件：

```text
ai-service/
│
├── prompts/
│   ├── system_prompt.txt
│   └── schema.txt
│
└── services/
    └── deepseek_service.py
```

文件说明：

**system_prompt.txt**

用于保存 AI 角色和回答规则，避免 Prompt 直接写在代码中。

**schema.txt**

用于保存数据库表结构信息，为后续数据查询提供上下文。

**deepseek_service.py**

负责处理 DeepSeek 调用逻辑，包括加载 Prompt 和管理历史消息。

# Prompt Management

由于大语言模型不了解项目业务，需要通过 Prompt 告诉模型角色和回答规则。

本阶段将 System Prompt 独立到文件中，方便后续修改和维护。

流程：

```text
system_prompt.txt
        ↓
deepseek_service.py
        ↓
DeepSeek API
```

# Schema 加载

新增 `schema.txt` 保存数据库结构信息。

内容包括：

- 表名
- 字段名
- 字段含义

在后续数据查询场景中，将 Schema 信息提供给模型，帮助模型理解数据库结构。

# DeepSeek Service 封装

在 Sprint01 的 LLM Client 基础上，对 DeepSeek 调用逻辑进行进一步封装。

调用流程：

```text
用户输入
   ↓
FastAPI
   ↓
DeepSeek Service
   ↓
LLM Client
   ↓
DeepSeek API
   ↓
返回结果
```

其中：

- LLM Client 负责创建 DeepSeek 客户端；
- DeepSeek Service 负责组织 Prompt 和历史消息。

# Conversation Memory

为了支持连续对话，本阶段增加简单上下文记录。

实现方式：

```python
conversation_history = []
```

每次请求后保存聊天记录，并在下一次调用模型时携带历史消息。

当前 Memory 使用 Python 内存保存，主要用于验证连续对话效果。

# Architecture

```text
User
 │
FastAPI
 │
DeepSeek Service
 │
Prompt + Conversation History
 │
LLM Client
 │
DeepSeek API
 │
Response
```

# Development Summary

本阶段完成 Prompt 管理、Schema 加载、DeepSeek Service 封装以及简单上下文记录。

通过优化模型调用流程，为后续 Planner、NL2SQL 等 Agent 功能开发提供基础。

# Next Sprint

## Sprint 03：Intent Planner

下一阶段增加用户意图识别能力。

通过 Planner 判断用户问题类型，区分聊天、数据查询和知识库查询，为后续 Agent 流程提供任务分流。