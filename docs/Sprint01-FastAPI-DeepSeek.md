# Sprint 01：FastAPI + DeepSeek

> Date：2026-07-16
> Author：zhongyubing

---

# Sprint Goal

搭建 AI 服务基础框架，实现 FastAPI 与 DeepSeek API 的连接，提供统一的聊天接口，为后续 AI Agent 开发打下基础。

---

# Background

项目目标是开发一个 AI Data Analysis Agent，能够通过自然语言完成电商数据分析。

本阶段首先完成 AI 服务框架搭建，实现客户端与 DeepSeek 大模型之间的通信。

---

# Project Structure

创建项目目录：

```text
ecommerce/
│
├── ai-service/
│   ├── app.py
│   ├── .env
│   ├── requirements.txt
│   └── services/
│       └── llm_client.py
│
├── backend/
└── vue/
```

---

# Environment

创建 Conda 环境：

```bash
conda create -n ai-agent python=3.11

conda activate ai-agent
```

安装依赖：

```bash
pip install fastapi uvicorn openai python-dotenv
```

---

# Environment Variables

创建：

```text
ai-service/.env
```

配置：

```env
DEEPSEEK_API_KEY=**************
```

`.env` 已加入 `.gitignore`，避免 API Key 上传至 GitHub。

---

# LLM Client

创建：

```text
services/llm_client.py
```

统一创建 DeepSeek Client：

```python
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
```

后续所有模型调用均复用该 Client。

---

# FastAPI

创建：

```text
app.py
```

实现：

- 创建 FastAPI 服务
- 创建 `/chat` 接口
- 接收用户消息
- 调用 AI 服务
- 返回模型回复

接口：

```http
POST /chat
```

请求：

```json
{
  "message": "你好"
}
```

返回：

```json
{
  "answer": "你好，我是 AI 数据分析助手。"
}
```

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

测试：

```
POST /chat
```

成功返回 DeepSeek 回复。

---

# Architecture

```
User
   │
HTTP
   │
FastAPI
   │
LLM Client
   │
DeepSeek API
   │
AI Response
```

---

# Development Summary

完成内容：

- [x] 创建 AI Service
- [x] 创建 FastAPI
- [x] 创建 Chat API
- [x] 封装 LLM Client
- [x] 配置 .env
- [x] Swagger 测试成功

---

# Technical Stack

- Python 3.11
- FastAPI
- Uvicorn
- OpenAI SDK
- DeepSeek API
- python-dotenv

---

# Key Learning

本阶段学习内容：

- FastAPI 基础开发
- RESTful API
- OpenAI SDK 使用
- DeepSeek API 调用
- 环境变量管理（.env）
- Swagger 接口测试

---

# Next Sprint

Sprint 02：Prompt Engineering

目标：

- 外置 System Prompt
- 加载数据库 Schema
- 封装 DeepSeek Service
- 增加基础上下文记忆

---

# Git Commit

```bash
git add .

git commit -m "feat: initialize FastAPI and DeepSeek service"

git push
```

---

# Sprint Status

✅ Sprint 01 Completed