# Sprint10：AI生成ECharts
# Sprint Goal

在已有数据查询能力基础上，引入 AI 数据可视化能力，使 Agent 能够根据查询结果自动生成 ECharts 配置，实现业务数据图表展示。


# Background

当前 Agent 已具备数据查询能力，但查询结果主要以文本形式返回。

因此本阶段增加 Chart Service，将 SQL 查询结果转换为 ECharts 配置，为后续 Vue3 前端展示提供数据支持。

# Project Structure
ai-service/

├── services/
│   ├── agent_service.py
│   ├── chart_service.py
│   └── sql_generator.py
│
├── tools/
│   └── mysql_tool.py
│
├── security/
│   └── sql_guard.py
│
└── app.py


chart_service.py
负责根据数据库查询结果生成 ECharts 配置。
包括：
接收查询数据；
调用 LLM 生成图表配置；

返回 ECharts Option JSON。




# Chart Service

新增：
services/chart_service.py

功能：
- 接收查询结果
- 根据数据生成 ECharts option
- 返回前端可解析 JSON

输入：
```json
[
{
"brand":"戴尔",
"sales":26230041
}
]
```


输出：
```json
{
"title":{
"text":"品牌销售排行"
},

"xAxis":{
"type":"category"
},

"series":[
{
"type":"bar",
"data":[26230041]
}
]
}
```


# Development Problems


## Problem 1：SQL Guard误判 DESC


问题：

SQL Guard 使用关键词匹配时，会将 `ORDER BY DESC` 误认为危险操作。

解决：

优化 SQL 检测规则，使用正则匹配避免误判。


## Problem 2：Decimal 类型无法返回 JSON

问题：

MySQL 金额字段使用 Decimal 类型，无法直接进行 JSON 序列化。

解决：

查询结果返回前转换为 float 类型。


## Problem 3：DeepSeek 返回格式异常

问题：

模型可能返回 Markdown 包裹的 JSON，导致程序解析失败。

解决：

通过 Prompt 限制模型只返回标准 JSON 格式。

# Development Summary

本 Sprint 完成 Agent 数据可视化能力建设，实现从用户图表需求识别、SQL 数据查询到 ECharts 配置生成的完整流程。

通过 Chart Service 将查询结果转换为可视化数据，使 Agent 不仅能够分析业务数据，还能够生成直观的图表展示。

# Next Sprint


## Sprint11：Vue3 AI Chat Visualization


本 Sprint 完成 AI Agent 前端展示能力建设，将后端数据分析结果接入 Vue3 页面。

通过聊天窗口、接口通信和 ECharts 动态渲染，实现 AI 对话与数据可视化结合，形成完整的 AI Chat + Visualization 交互体验。


