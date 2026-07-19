# Sprint12：Project Engineering Optimization

> Date：2026-07-19  
> Author：zhongyubing

---

# Sprint Goal


本 Sprint 的目标是在 Sprint11（Vue3 Chat UI & ECharts Visualization Integration）的基础上，对 AI Data Analyst Agent 项目进行工程化整理与优化。

Sprint11 已完成：

- Vue3 AI聊天界面
- Axios接口通信
- FastAPI接口调用
- AI回答展示
- ECharts动态渲染
- 数据分析可视化


目前系统已经具备完整功能：

```
用户输入

↓

Vue3

↓

FastAPI

↓

AI Agent

↓

DeepSeek

↓

MySQL

↓

ECharts

↓

结果展示
```


但是作为一个完整项目，还需要进一步优化：

- 项目结构整理
- GitHub展示优化
- README完善
- 环境部署说明
- 配置文件规范化
- 日志记录完善


因此，本 Sprint 目标：

将项目从"功能开发阶段"提升为"可展示、可维护的完整项目版本"。

---

# Background


前面的 Sprint 已经完成 AI Data Analyst Agent 核心功能：


## AI能力

- Prompt Engineering
- Function Calling
- NL2SQL
- Multi-Step Agent
- Conversation Memory
- RAG


## 数据能力

- MySQL数据查询
- SQL自动生成
- SQL Guard安全检查


## 可视化能力

- ECharts配置生成
- Vue3图表展示


当前项目已经具备：

```
AI Agent

+

数据分析

+

知识库

+

可视化

```


本 Sprint 重点不再增加新的 AI 功能，而是提升项目工程质量。

---

# Project Structure Optimization


最终项目结构整理：

```
AI-Data-Analyst-Agent

│
├── ai-service
│
│   ├── app.py
│   │
│   ├── services
│   │   ├── agent_service.py
│   │   ├── deepseek_service.py
│   │   ├── sql_generator.py
│   │   ├── chart_service.py
│   │   └── vector_search.py
│   │
│   ├── tools
│   │   └── mysql_tool.py
│   │
│   ├── security
│   │   └── sql_guard.py
│   │
│   ├── prompts
│   │   ├── system_prompt.txt
│   │   ├── schema.txt
│   │   └── planner_prompt.txt
│   │
│   ├── knowledge
│   │   ├── business.md
│   │   └── project.md
│   │
│   ├── vector_store
│   │   ├── index.faiss
│   │   └── docs.pkl
│   │
│   ├── requirements.txt
│   │
│   └── .env
│
│
├── frontend
│
│   ├── src
│   │
│   ├── components
│   │
│   ├── api
│   │
│   └── package.json
│
│
├── docs
│
│   ├── Sprint01.md
│   ├── Sprint02.md
│   ├── ...
│   └── Sprint12.md
│
│
└── README.md

```

---

# README Documentation


新增：

```
README.md
```


主要内容：


## 1. 项目介绍


示例：


```
AI Data Analyst Agent

基于 DeepSeek + FastAPI + MySQL + Vue3 构建的智能数据分析 Agent。

用户通过自然语言提出业务问题，
AI 自动完成：

- 意图识别
- SQL生成
- 数据查询
- 结果分析
- 图表展示

```


---

## 2. System Architecture


项目架构：

```
Vue3

↓

FastAPI

↓

AI Agent

↓

DeepSeek

↓

MySQL

↓

ECharts

```


---

## 3. Features


实现功能：


### AI Agent

- Function Calling
- Multi-Step Tool Calling
- NL2SQL
- Conversation Memory


### Knowledge Enhancement

- RAG
- FAISS
- Vector Search


### Database

- MySQL
- SQL Guard
- Read Only Query


### Visualization

- Vue3
- ECharts


---

# Environment Configuration


## Backend


Python环境：

```
Python 3.11
```


安装依赖：

```bash
pip install -r requirements.txt
```


---


## Frontend


进入：

```bash
cd frontend
```


安装：

```bash
npm install
```


启动：

```bash
npm run dev
```


---

# Configuration Management


整理环境变量：


```
.env
```


保存：

```
DEEPSEEK_API_KEY

MYSQL_HOST

MYSQL_PORT

MYSQL_USER

MYSQL_PASSWORD

MYSQL_DATABASE
```


避免：

- API Key泄露
- 数据库密码泄露


同时加入：

```
.gitignore
```


忽略：

```
.env

__pycache__

node_modules

vector_store

```


---

# Requirements Management


新增：

```
requirements.txt
```


保存 Python依赖：

```
fastapi

uvicorn

openai

python-dotenv

pymysql

sentence-transformers

faiss-cpu

numpy
```


方便其他环境快速部署。

---

# Logging Optimization


增加 Agent运行日志。


记录：

- 用户问题
- Agent规划
- SQL语句
- 查询结果
- 执行时间


日志示例：

```
========== Agent ==========

User:

销量最高品牌？

Plan:

查询品牌销售数据


SQL:

SELECT brand,
SUM(sales_amount)
FROM dws_brand_sales;


Result:

Success

```


方便：

- Debug
- 项目展示
- 问题定位


---

# Deployment Documentation


整理运行流程。


## Step 1

启动 MySQL


确保：

```
ecommerce database
```


存在。


---

## Step 2

启动 AI Service


进入：

```
ai-service
```


运行：

```bash
uvicorn app:app --reload
```


启动：

```
localhost:8000
```


---

## Step 3

启动 Vue3


进入：

```
frontend
```


运行：

```bash
npm run dev
```


访问：

```
localhost:5173
```


---

# GitHub Optimization


项目上传 GitHub：

目录：

```
AI-Data-Analyst-Agent
```


包含：

```
README.md

docs/

ai-service/

frontend/

requirements.txt

.gitignore

```


提交：

```bash
git add .

git commit -m "docs: optimize project structure and documentation"

git push
```


---

# Final Architecture


最终版本：


```
                 User

                  │

                  ▼

                Vue3

                  │

                  ▼

              FastAPI

                  │

                  ▼

             AI Agent

        ┌─────────┼─────────┐

        ▼         ▼         ▼

   Planner    RAG      Tool Calling

        │         │         │

        ▼         ▼         ▼

    DeepSeek   FAISS    MySQL

                  │

                  ▼

              ECharts

                  │

                  ▼

             Visualization

```


---

# Sprint Achievement


Sprint12完成项目工程化优化。


新增：

- README文档
- 项目结构整理
- 环境配置说明
- requirements管理
- GitHub展示优化
- 部署流程说明
- 日志规范


项目从：

```
功能Demo
```


升级为：

```
完整AI数据分析项目
```


---

# Key Learning


本 Sprint 学习内容：

- 软件项目结构设计
- GitHub项目管理
- README编写
- 环境依赖管理
- 项目部署流程
- 工程化开发规范


---

# Project Final Status


AI Data Analyst Agent v1.0


已完成：

✅ FastAPI后端

✅ DeepSeek接入

✅ Prompt Engineering

✅ MySQL Tool

✅ Function Calling

✅ NL2SQL

✅ Multi-Step Agent

✅ Conversation Memory

✅ RAG知识库

✅ SQL Guard

✅ ECharts可视化

✅ Vue3前端展示

✅ 项目工程化整理


---

# Sprint Status


✅ Sprint12 Completed