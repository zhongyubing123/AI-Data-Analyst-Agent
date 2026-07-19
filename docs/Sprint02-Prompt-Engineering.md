# Sprint 02：Prompt Engineering

> Date：2026-07-16
> Author：zhongyubing

---

# Sprint Goal

引入 Prompt Engineering，将系统 Prompt 独立管理，并封装 DeepSeek 对话服务，实现基础上下文记忆，为后续 AI Agent 开发提供统一入口。

---

# Background

Sprint01 已完成 FastAPI 与 DeepSeek API 的连接，实现了基础 AI 对话能力。

本阶段进一步优化模型调用方式，将 Prompt 从代码中分离，并增加简单的对话上下文管理，提高回答的一致性。

---

# Project Structure

新增目录：

```text
ai-service/
│
├── prompts/
│   ├── system_prompt.txt
│   └── schema.txt
│
└── services/
    ├── llm_client.py
    └── deepseek_service.py
```

---

# Prompt Management

新增：

```
prompts/system_prompt.txt
```

用于统一维护 AI 身份和回答规则。

新增：

```
prompts/schema.txt
```

用于保存数据库 Schema，在模型回答过程中一起加载。

---

# LLM Client

新增：

```
services/llm_client.py
```

统一创建 DeepSeek Client。

```python
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
```

后续所有模型调用均复用该 Client。

---

# Conversation Memory

在：

```
deepseek_service.py
```

中增加简单上下文记忆。

```python
conversation_history = []

MAX_HISTORY = 10
```

每次请求都会携带最近的对话记录，提高连续对话效果。

---

# Running

启动：

```bash
uvicorn app:app --reload
```

访问：

```
http://127.0.0.1:8000/docs
```

调用：

```
POST /chat
```

验证 Prompt 加载和上下文记忆是否生效。

---

# Architecture

```
User
   │
HTTP
   │
FastAPI
   │
DeepSeek Service
   │
System Prompt
   │
Schema
   │
DeepSeek API
```

---

# Development Summary

完成内容：

- [x] Prompt 外置管理
- [x] Schema 加载
- [x] LLM Client 封装
- [x] DeepSeek Service 封装
- [x] Conversation Memory

---

# Technical Stack

- Python
- FastAPI
- OpenAI SDK
- DeepSeek API
- pathlib

---

# Key Learning

本阶段学习内容：

- Prompt Engineering
- System Prompt
- Prompt 外置管理
- LLM Client 封装
- Conversation Memory

---

# Next Sprint

Sprint 03：Intent Planner

目标：

- 引入 Planner
- 实现用户意图识别
- 区分聊天、数据库查询和知识库查询

---

# Git Commit

```bash
git add .

git commit -m "feat: add prompt engineering and conversation memory"

git push
```

---

# Sprint Status

✅ Sprint 02 Completed