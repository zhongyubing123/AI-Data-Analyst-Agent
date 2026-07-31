# Sprint11：Vue3前端展示

# Sprint Goal

本 Sprint 在 Sprint10 数据可视化能力基础上，增加 Vue3 前端展示层。

通过 FastAPI 接口连接 AI Agent，实现聊天交互、AI回答展示和 ECharts 图表动态渲染，形成完整的数据分析可视化流程。

# Background

前期 Sprint 已完成 AI Agent 后端能力建设，能够完成数据查询和 ECharts 配置生成，但结果仍需要通过接口查看。

本 Sprint 增加 Vue3 前端展示层，实现用户通过页面进行 AI 对话，并直观展示分析结果和业务图表。


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


# Development Summary

本 Sprint 完成 Vue3 前端接入，实现 AI Agent 与用户界面的连接。

通过 Axios 调用 FastAPI 接口，并结合 ECharts 组件完成分析结果和业务图表展示。


# Development Flow

用户通过 Vue3 页面输入问题，前端通过 Axios 调用 FastAPI。

后端 Agent Service 负责任务分析、SQL生成、安全检查和数据查询，最后结合 DeepSeek 返回分析结果或 ECharts 配置，并由 Vue3 展示。


# Development Problems

## Problem 1：跨域问题

问题：

Vue3 与 FastAPI 运行端口不同，导致接口请求被浏览器拦截。

解决：

FastAPI 增加 CORS 配置，允许前端访问后端接口。


## Problem 2：JSON解析失败

问题：

DeepSeek 返回 Markdown 格式 JSON，导致解析失败。

解决：

优化 Prompt，要求模型只返回标准 JSON。


## Problem 3：Decimal类型转换

问题：

MySQL Decimal 类型无法直接进行 JSON 序列化。

解决：

返回前转换为 float 类型。

Decimal

↓

float

↓

JSON