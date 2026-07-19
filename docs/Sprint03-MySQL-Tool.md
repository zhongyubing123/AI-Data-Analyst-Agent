# Sprint 03：MySQL Tool

> Date：2026-07-17  
> Author：zhongyubing


---

# Sprint Goal

封装 MySQL 数据库访问能力，为 AI Data Analyst Agent 提供统一的数据查询工具（Tool）。

本 Sprint 主要完成：

- Python 服务连接 MySQL 数据库
- 封装数据库查询方法
- 使用环境变量管理数据库配置
- 为后续 Agent 数据查询流程和 NL2SQL 能力提供基础支持


---

# Background

当前 AI 服务已经能够完成基础的大模型调用：

```
User

↓

FastAPI

↓

DeepSeek Service
```


但是，LLM 本身无法直接访问业务数据库。

因此需要增加数据库工具层，通过 Python 后端安全访问 MySQL，并将查询能力封装成 Agent 可调用的 Tool。


当前升级后的服务结构：

```
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


本 Sprint 完成 MySQL Tool 基础能力建设，暂不涉及自动化 Agent 调用流程。


---

# Project Structure


新增目录：


```
ai-service
│
├── app.py
│
├── services
│
├── prompts
│
├── tools
│   └── mysql_tool.py
│
├── security
│
├── .env
│
└── requirements.txt

```


新增文件：

```
tools/mysql_tool.py
```


用于统一管理 MySQL 数据库访问。


---

# Environment Configuration


为了避免数据库账号信息直接写入代码，使用 `.env` 文件管理配置。


新增环境变量：


```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=******
MYSQL_DATABASE=ecommerce
```


通过：

```python
python-dotenv
```

加载环境变量。


注意：

```
.env
```

文件已经加入：

```
.gitignore
```


避免：

- 数据库密码泄露
- API Key 泄露


---

# Dependency Installation


安装 MySQL Python 驱动：


```bash
python -m pip install pymysql
```


验证安装：


```bash
python -c "import pymysql; print(pymysql.__version__)"
```


输出版本号表示安装成功。


---

# MySQL Tool Design


新增：

```
tools/mysql_tool.py
```


该模块负责封装数据库访问能力。


主要包含两个核心方法。


---

## 1. get_connection()


功能：

创建 MySQL 数据库连接。


职责：

- 读取 `.env` 配置
- 创建数据库连接
- 返回 Connection 对象


示例：


```python
connection = get_connection()
```


---

## 2. execute_query(sql)


功能：

执行 SQL 查询并返回结果。


职责：


- 接收 SQL 查询语句
- 执行数据库查询
- 获取查询结果
- 自动关闭数据库连接


统一封装数据库访问逻辑，减少重复连接代码。


后续结合 SQL Guard 对 SQL 进行安全限制。


---

# Database Connection Test


测试代码：


```python
if __name__ == "__main__":

    sql = """
    SELECT *
    FROM dws_item_hot
    LIMIT 5;
    """

    result = execute_query(sql)

    print(result)
```


运行：


```bash
python tools/mysql_tool.py
```


运行结果：


```text
(
('商品A', 1200),
('商品B', 980),
...
)
```


说明：

- Python 成功连接 MySQL
- SQL 查询正常执行
- MySQL Tool 基础功能完成


---

# Development Summary


本 Sprint 完成内容：


- [x] 创建 tools 目录
- [x] 创建 mysql_tool.py
- [x] 配置 MySQL 环境变量
- [x] 使用 python-dotenv 管理配置
- [x] 使用 PyMySQL 连接数据库
- [x] 封装数据库查询函数
- [x] 完成 MySQL Tool 测试


---

# Technical Stack


- Python 3.11
- PyMySQL
- python-dotenv
- MySQL
- FastAPI


---

# Architecture


当前 AI 服务架构：


```
                 User

                  │

                  ▼

              FastAPI

                  │

                  ▼

          Agent Service

                  │

                  ▼

            MySQL Tool

                  │

                  ▼

              MySQL

```


MySQL Tool 作为 AI Agent 与数据库之间的数据访问层。


---

# Key Learning


本阶段主要学习：


## 1. Python 数据库连接


学习使用：

```
PyMySQL
```


完成 Python 与 MySQL 的通信。


---

## 2. 环境变量管理


使用：

```
python-dotenv
```


管理：

- 数据库连接信息
- 敏感配置


提升项目安全性。


---

## 3. Tool 设计思想


理解 AI Agent 中 Tool 的作用：

```
LLM

↓

Tool

↓

External System

```


Agent 通过工具访问外部数据，而不是直接操作数据库。


---

## 4. 数据访问封装


将数据库操作统一封装，提高代码复用性，为后续 Agent 流程整合提供基础。


---

# Next Sprint


## Sprint 04：Agent 数据查询流程


目标：

实现用户自然语言问题到数据库查询的完整流程。


计划流程：


```
User Question

↓

Planner

↓

SQL Generator

↓

SQL Guard

↓

MySQL Tool

↓

Database Result

↓

DeepSeek Analysis

↓

User

```


实现：

- 用户问题理解
- 自动生成查询 SQL
- 执行数据库查询
- 基于真实数据生成分析结果


---

# Git Commit


提交代码：


```bash
git add .

git commit -m "feat: add mysql tool for ai agent"

git push
```


---

# Sprint Status


✅ Sprint 03 Completed

```
MySQL Tool
Database Connection
Query Execution

Completed
```
