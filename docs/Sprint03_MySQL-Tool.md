# Sprint 03：MySQL Tool

# Sprint Goal

封装 MySQL 数据库访问能力，为 AI Data Analyst Agent 提供统一的数据查询工具。

本阶段完成 Python 连接 MySQL、封装查询方法，为后续 Agent 调用数据库提供基础。

# Background

前两个 Sprint 已完成 AI 服务和模型调用流程：

```text
User
 ↓
FastAPI
 ↓
DeepSeek Service
```

但是 LLM 本身无法直接访问业务数据库，因此需要增加数据库工具层。

通过 MySQL Tool 封装数据库访问逻辑，让 Agent 可以通过工具获取真实业务数据。

整体流程：

```text
User
 ↓
FastAPI
 ↓
Agent Service
 ↓
MySQL Tool
 ↓
MySQL Database
```

# Project Structure

新增数据库工具：

```text
ai-service/
│
├── tools/
│   └── mysql_tool.py
│
├── services/
├── prompts/
├── .env
└── requirements.txt
```

文件说明：

**mysql_tool.py**

负责封装 MySQL 数据库访问逻辑，包括创建连接和执行 SQL 查询。


# Environment Configuration

使用 `.env` 管理数据库连接信息，避免账号密码直接写入代码。

配置：

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=******
MYSQL_DATABASE=ecommerce
```

通过 `python-dotenv` 加载配置。


# MySQL Tool

新增：

```text
tools/mysql_tool.py
```

主要实现两个功能：

## get_connection()

负责创建 MySQL 数据库连接。

流程：

```text
读取环境变量

↓

创建数据库连接

↓

返回 Connection
```


## execute_query(sql)

负责执行 SQL 查询并返回结果。

流程：

```text
SQL

↓

MySQL Tool

↓

Database

↓

Query Result
```

通过统一封装数据库访问逻辑，减少重复连接代码。


# Architecture

```text
User
 │
FastAPI
 │
Agent Service
 │
MySQL Tool
 │
MySQL Database
```

MySQL Tool 作为 Agent 与数据库之间的数据访问层。


# Development Summary

本阶段完成 MySQL Tool 基础能力开发，实现 Python 与 MySQL 的连接，并封装数据库查询方法。

为后续 NL2SQL 和 Agent 自动查询流程提供数据访问基础。


# Technical Stack

- Python
- PyMySQL
- python-dotenv
- MySQL
- FastAPI


# Next Sprint

## Sprint 04：Agent 数据查询流程

下一阶段将实现用户问题到数据库查询的完整流程。

通过 Planner、SQL Generator、MySQL Tool 等模块，实现自然语言查询数据。