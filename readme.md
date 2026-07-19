# AI Data Analyst Agent

基于电商数据仓库与大语言模型的智能数据分析 Agent


## 1. 项目介绍

本项目基于阿里天池 UserBehavior 用户行为数据，构建电商数据仓库，并结合 DeepSeek 大语言模型开发 AI Data Analyst Agent。

系统实现从数据采集、ETL、数仓建模到 AI 自然语言分析的完整流程，使用户可以通过自然语言查询业务数据，并自动生成分析结果。

项目主要包含：

- 电商数据仓库平台
- AI 数据分析 Agent
- 数据可视化分析系统


核心目标：

> 用户提出业务问题，AI 自动理解需求，查询真实业务数据，并生成分析结果。


---

# 2. 系统架构


```
                User

                 ↓

          Vue3 Chat / Dashboard

                 ↓

              FastAPI

                 ↓

        AI Data Analyst Agent

        ┌────────┼────────┐

        ↓        ↓        ↓

     NL2SQL     RAG    Chart Agent

        ↓        ↓        ↓

      MySQL    FAISS   ECharts

                 ↓

          Hive / MySQL 数仓

```


---

# 3. 技术栈


## 数据开发

- Python
- Pandas
- MySQL
- Hive
- SQL
- SparkSQL（优化方向）


## AI Agent

- DeepSeek API
- FastAPI
- Prompt Engineering
- Function Calling
- NL2SQL
- Multi-Step Agent
- RAG
- FAISS
- Sentence Transformer


## 前端

- Vue3
- Axios
- ECharts


---

# 4. 数据仓库建设


数据来源：

阿里天池 UserBehavior 用户行为数据


数据规模：

```
6万+ 用户行为数据
```


数据流程：

```
Raw Data

↓

Python ETL

↓

ODS

↓

DWD

↓

DWS

↓

AI分析

```


采用星型模型设计：


```
              dim_goods


                  |

dim_brand -- fact_behavior -- dim_users


                  |

            dim_category

```


## 数据分层


### ODS层

保存原始用户行为数据：

```
ods_user_behavior
```


### DWD层

明细数据：

- dim_goods
- dim_users
- dim_brand
- dim_category
- fact_behavior


### DWS层

业务指标汇总：

| 表 | 功能 |
|-|-|
| dws_brand_sales | 品牌销售分析 |
| dws_item_hot | 热门商品分析 |
| dws_user_active | 用户活跃分析 |
| dws_category_sales | 品类销售分析 |



---

# 5. Hive 数仓迁移


为了提升数据处理能力，将 MySQL 数仓迁移至 Hive。


完成：

- Hadoop环境搭建
- Hive部署
- ODS/DWD/DWS迁移


架构：

```
MySQL

↓

Hive

↓

ODS/DWD/DWS

↓

分析服务

```


---

# 6. AI Data Analyst Agent


## Agent流程


```
用户问题

↓

DeepSeek理解需求

↓

Agent任务规划

↓

NL2SQL生成SQL

↓

SQL安全检查

↓

MySQL查询

↓

AI分析回答

```


---

## 核心能力


### 1. NL2SQL

通过数据库 Schema 注入，让模型理解数据库结构。


例如：

用户：

```
销量最高的品牌有哪些？
```


AI自动生成SQL并查询：

```sql
SELECT 
brand,
SUM(sales_amount)
FROM dws_brand_sales
GROUP BY brand
ORDER BY sales_amount DESC;
```


---

### 2. Function Calling


实现：

```
DeepSeek

↓

Tool Calling

↓

MySQL Tool

↓

Database

↓

Result

↓

AI Answer

```


AI能够根据问题自动调用数据库工具。


---

### 3. Multi-Step Agent


支持：

- Agent任务规划
- 多轮Tool Calling
- ReAct推理流程
- Conversation Memory


流程：

```
Reason

↓

Tool

↓

Observation

↓

Final Answer

```


---

### 4. RAG知识库


构建企业知识库：

```
knowledge

├── business.md

└── project.md

```


流程：

```
Document

↓

Embedding

↓

FAISS

↓

Vector Search

↓

DeepSeek

```


支持企业业务知识问答。


---

### 5. SQL安全控制


增加 SQL Guard，对 AI 生成SQL进行安全检测。


允许：

```
SELECT
```


禁止：

```
DELETE
UPDATE
INSERT
DROP
ALTER
TRUNCATE
```


执行流程：

```
AI生成SQL

↓

SQL Guard

↓

MySQL

```


保证数据库只读分析。


---

### 6. AI可视化分析


AI自动生成 ECharts 配置。


流程：

```
用户需求

↓

SQL查询

↓

数据分析

↓

生成ECharts Option

↓

Vue展示

```


支持：

- 柱状图
- 饼图
- 折线图


---

# 7. 项目目录


```
AI-Data-Analyst-Agent

├── ai-service
│
│   ├── services
│   ├── tools
│   ├── security
│   ├── prompts
│   ├── knowledge
│   └── app.py
│
├── vue-dashboard
│
├── sql
│
├── docs
│   ├── Sprint01.md
│   ├── Sprint02.md
│   └── ...
│
└── README.md

```


---

# 8. 项目运行


## 后端


安装依赖：

```bash
pip install -r requirements.txt
```


配置：

```
.env
```


启动：

```bash
uvicorn app:app --reload
```


## 前端


```bash
npm install

npm run dev
```


---

# 9. 项目成果


目前系统具备：


## 数据工程能力

✅ Python ETL

✅ 数据仓库建模

✅ ODS/DWD/DWS分层

✅ Hive离线分析


## AI Agent能力

✅ Prompt Engineering

✅ Function Calling

✅ NL2SQL

✅ Multi-Step Agent

✅ RAG知识库

✅ SQL安全控制


## 数据分析能力

✅ Vue3可视化

✅ ECharts图表生成

✅ AI业务分析


---

# 10. 后续优化


- SparkSQL替代部分ETL任务
- SQL执行日志
- 查询历史记录
- 更复杂业务分析
- Multi-Agent协作


---

# 11. 总结


本项目将传统数据仓库与大语言模型结合，构建了一个企业级 AI 数据分析 Agent。

系统不仅具备数据清洗、数仓建模和业务分析能力，同时支持自然语言查询、智能SQL生成、知识库增强和自动化可视化分析。

项目体现了：

- 数据工程能力
- 数据仓库设计能力
- AI Agent开发能力
- 大模型应用能力

## 项目目前存在的不足

1. **数据仓库指标体系不够完善**
   当前 DWS 层主要支持品牌销售、商品热度、用户活跃、品类销售等基础分析，但缺少商品销售额、平均价格、转化率、用户价值等更丰富的业务指标，导致 AI Agent 在部分业务问题查询时无法获取对应数据。

2. **Hive 与 SparkSQL 应用深度不足**
   目前已完成 MySQL 到 Hive 的数仓迁移，但 Hive 主要用于数据存储和查询，缺少分区表、分桶、ORC 等优化；SparkSQL 仍处于规划阶段，尚未完全替代 ETL 流程。

3. **AI Agent 上下文能力仍需优化**
   当前 Agent 已实现多轮对话和简单上下文记忆，但记忆主要依赖程序内存，系统重启后数据会丢失，后续可引入 Redis 等长期记忆方案提升连续对话能力。

4. **SQL 安全控制能力较基础**
   当前通过 Prompt 约束和关键词检测实现 SQL Guard，可以拦截危险 SQL，但安全规则仍较简单，后续可结合 SQL Parser 实现更精确的 SQL 权限控制。

5. **RAG 知识库规模较小**
   当前知识库主要包含项目介绍和业务指标定义，文档数量有限，后续可以增加数据库说明、业务规则、指标口径等企业文档，并优化文档切片和检索策略。

6. **系统工程化能力仍需提升**
   当前系统已完成 AI Agent、数据仓库和可视化功能集成，但日志管理、Docker 部署、异常监控、权限管理等企业级能力仍需要进一步完善。
