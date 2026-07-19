# Sprint11：Vue3 Chat UI & ECharts Visualization Integration

> Date：2026-07-19  
> Author：zhongyubing

---

# Sprint Goal

本 Sprint 的目标是在 Sprint10（AI 数据可视化 Agent）的基础上，将 AI Agent 后端能力接入 Vue3 前端，实现完整的人机交互界面。

Sprint10 已完成：

- AI识别图表需求
- NL2SQL
- SQL安全检查
- MySQL数据查询
- DeepSeek生成ECharts配置

但是目前系统仍存在以下问题：

- 用户只能通过接口测试 AI
- 查询结果无法直观展示
- ECharts 配置无法在页面渲染

因此，本 Sprint 目标：

- 搭建 Vue3 AI 聊天界面
- 调用 FastAPI `/chat` 接口
- 展示 AI 返回结果
- 接收 ECharts Option
- 动态渲染业务图表

最终实现：

```
用户
 ↓
AI Agent
 ↓
数据库分析
 ↓
可视化展示
```

---

# Background

在前面的 Sprint 中，系统已经具备：

```
FastAPI

↓

AI Agent

↓

DeepSeek

↓

MySQL

↓

ECharts Option
```

但是后端生成的数据分析结果仍然需要通过接口测试查看。

为了让系统更加接近真实应用，本 Sprint 增加 Vue3 前端展示层。

升级后架构：

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

               │

       ┌───────┴────────┐

       ▼                ▼

   Text Answer      ECharts JSON

       │                │

       ▼                ▼

   Chat展示        图表展示

```

---

# Project Structure

新增前端目录：

```
project

│

├── ai-service

│
├── frontend

│
├── src

│   ├── App.vue

│   ├── api

│   │   └── chat.js

│   │

│   ├── components

│   │   ├── ChatBox.vue

│   │   └── ChartView.vue

│   │

│   └── main.js

│

└── package.json

```

---

# Technical Stack

## Frontend

- Vue3
- Axios
- ECharts


## Backend

- FastAPI
- DeepSeek API
- MySQL
- AI Agent

---

# Development Summary


## 1. Vue3 项目搭建

创建 Vue3 项目：

```bash
npm create vue@latest frontend
```

安装依赖：

```bash
npm install

npm install axios

npm install echarts
```

完成前端基础环境搭建。

---

# 2. Axios接口封装


新增：

```
src/api/chat.js
```


功能：

调用后端接口：

```
POST /chat
```


发送用户问题：

```javascript
axios.post(
    "/chat",
    {
        message:userInput
    }
)
```


实现：

```
Vue

↓

FastAPI

↓

Agent
```

数据通信。

---

# 3. AI聊天窗口


实现聊天流程：

```
用户输入问题

↓

Vue发送请求

↓

FastAPI

↓

Agent处理

↓

DeepSeek分析

↓

返回结果

↓

页面展示
```


示例：

用户输入：

```
销量最高品牌有哪些？
```


AI返回：

```
销量最高品牌为XXX，
销售额为XXX。
```


---

# ECharts Visualization


新增组件：

```
ChartView.vue
```


功能：

- 接收后端返回的 ECharts Option
- 初始化 ECharts
- 渲染业务图表


数据流程：

```
MySQL数据

↓

Chart Service

↓

ECharts Option JSON

↓

FastAPI

↓

Vue

↓

ECharts渲染
```


示例返回：

```json
{
"title":{
"text":"品牌销售排行"
},

"xAxis":{
"data":[
"戴尔",
"小米",
"VIVO"
]
},

"series":[
{
"type":"bar",
"data":[
26230041,
16215386,
16013851
]
}
]
}
```


前端根据配置自动生成：

```
品牌销售排行榜柱状图
```

---

# Development Flow


完整系统流程：

```
用户输入自然语言

↓

Vue3 Chat页面

↓

Axios请求

↓

FastAPI /chat

↓

Agent Service

↓

Planner判断任务

↓

SQL Generator生成SQL

↓

SQL Guard检查

↓

MySQL查询

↓

DeepSeek分析

↓

生成回答/ECharts配置

↓

Vue展示

```

---

# Test Results


## Test 1：AI聊天功能


输入：

```
销量最高品牌？
```


执行流程：

```
Vue

↓

FastAPI

↓

Agent

↓

SQL

↓

MySQL

↓

DeepSeek
```


返回：

```
销量最高品牌为戴尔。
```


测试成功。

---

## Test 2：AI生成图表


输入：

```
生成品牌销售图表
```


系统流程：

```
用户需求

↓

Agent识别可视化任务

↓

查询 dws_brand_sales

↓

生成ECharts JSON

↓

Vue渲染
```


页面展示：

```
品牌销售排行榜柱状图
```


测试成功。

---

# Problems and Solutions


## Problem 1：跨域问题


错误：

```
CORS policy blocked
```


原因：

Vue运行：

```
localhost:5173
```


FastAPI运行：

```
localhost:8000
```


两个服务属于不同源。


解决：

FastAPI增加 CORS 配置：

```python
from fastapi.middleware.cors import CORSMiddleware


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```


解决前后端通信问题。


---

## Problem 2：ECharts JSON解析失败


问题：

DeepSeek返回：

```json
```json
{}
```
```


导致：

```javascript
JSON.parse()
```

失败。


解决：

Prompt增加：

```
只返回JSON格式。

禁止Markdown代码块。
```


---

## Problem 3：Decimal类型无法JSON传输


问题：

MySQL金额字段：

```
Decimal
```


无法直接返回前端。


解决：

转换：

```
Decimal

↓

float

↓

JSON
```


保证接口正常返回。

---

# Architecture Evolution


## Sprint10

```
AI Agent

↓

Database

↓

ECharts JSON
```


## Sprint11


```
User

↓

Vue3

↓

FastAPI

↓

AI Agent

↓

Database

↓

ECharts

↓

Visualization
```


系统从接口测试工具升级为完整 Web 应用。

---

# Key Learning


本 Sprint 学习内容：

- Vue3 前后端交互
- Axios调用接口
- FastAPI跨域配置
- ECharts动态渲染
- AI分析结果可视化
- 前后端系统集成


---

# Sprint Achievement


Sprint11完成 AI Agent 前端展示能力。


新增：

- Vue3聊天界面
- Axios接口通信
- AI回答展示
- ECharts动态渲染
- 数据分析可视化


系统升级：

之前：

```
API测试AI Agent
```


现在：

```
Vue3

↓

AI Chat

↓

数据分析

↓

图表展示
```


实现完整用户交互闭环。


---

# Next Sprint


Sprint12：Project Engineering Optimization


目标：

- 完善 README
- GitHub 项目整理
- 添加运行说明
- 项目截图整理
- 日志优化
- 配置文件整理
- 部署说明


最终形成：

```
AI Data Analyst Agent v1.0
```


用于简历项目展示。

---

# Git Commit


建议提交：

```bash
git add .

git commit -m "feat: integrate vue3 chat ui with echarts visualization"

git push
```

---

# Sprint Status


✅ Sprint11 Completed