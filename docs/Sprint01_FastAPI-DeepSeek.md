# Sprint 01：FastAPI + DeepSeek

# Sprint Goal

搭建基础 AI 服务环境，实现 FastAPI 与 DeepSeek API 的连接，提供统一的聊天接口。

# Background

项目目标是开发一个 AI Data Analysis Agent，通过自然语言完成电商数据分析。

由于 Agent 需要调用大语言模型完成问题理解和任务处理，因此首先搭建 FastAPI 服务并连接 DeepSeek API，为后续功能开发提供基础。

# Project Structure

创建项目目录：

```text
AI-Data-Analyst-Agent/
│
└── ai-service/
    ├── app.py
    ├── .env
    ├── requirements.txt
    └── services/
        └── llm_client.py
```

# Environment

开发环境：

- Python 3.11
- FastAPI
- Uvicorn
- OpenAI SDK
- python-dotenv

# LLM Client

为了避免在接口代码中重复编写大模型调用逻辑，将 DeepSeek API 调用进行独立封装。

创建：

```text
services/llm_client.py
```

通过 OpenAI SDK 创建 DeepSeek Client：

```python
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
```

后续模型调用统一通过该 Client 管理。

# FastAPI 服务

创建：

```text
app.py
```

使用 FastAPI 搭建 AI 服务接口，提供 `/chat` 接收用户输入。

接口接收到请求后，通过 LLM Client 调用 DeepSeek API，并返回模型生成结果，完成客户端与大模型之间的基础通信。

通过 Swagger 文档测试接口，验证 DeepSeek 调用链路正常。

# Architecture

```text
User
 │
FastAPI
 │
LLM Client
 │
DeepSeek API
 │
Response
```

# Development Summary

本阶段完成 AI Service 基础框架搭建，实现 FastAPI 与 DeepSeek API 的连接，并完成 Chat 接口测试验证，为后续 Agent 功能开发提供基础。

# Technical Stack

- Python 3.11
- FastAPI
- OpenAI SDK
- DeepSeek API
- python-dotenv

# Next Sprint

## Sprint 02：Prompt Engineering

下一阶段优化模型调用方式，通过设计 System Prompt 和引入数据库 Schema 信息，提高模型对业务数据的理解能力。