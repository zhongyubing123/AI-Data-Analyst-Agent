# Sprint 08：RAG知识增强


# Sprint Goal


在 AI Data Analyst Agent 基础上，引入 RAG 能力，使 Agent 支持业务文档和项目知识检索。

本阶段通过知识库构建、向量检索和 Prompt 增强，提升 Agent 对非结构化信息的理解能力。

# Background

前几个 Sprint 已完成：

- NL2SQL 查询流程；
- SQL 数据分析能力；
- Agent Workflow。

但是 Agent 主要面向结构化数据查询，缺少业务文档和知识理解能力。

因此本阶段引入 RAG，通过知识库检索增强模型回答能力。

# Project Structure

新增 RAG 知识检索相关模块：

```text
ai-service/

├── knowledge/
│   └── *.md
│
├── services/
│   ├── build_vector.py
│   └── vector_search.py
│
└── vector_store/
    ├── index.faiss
    └── docs.pkl

文件说明：

build_vector.py
负责读取 Markdown 知识文档，并通过 Embedding 模型生成 FAISS 向量索引。

vector_search.py
负责加载向量库，根据用户问题检索相关知识内容。

## Knowledge Base

构建 Markdown 业务知识库，包含项目介绍、技术架构和电商业务指标定义，为 Agent 提供知识检索来源。


## Vector Retrieval

通过 Embedding 将知识文档向量化，并利用 FAISS 检索相关知识内容，为 Agent 提供回答上下文。

## RAG Workflow

Agent 增加知识检索流程，通过 Vector Search 获取相关知识内容，并结合 Prompt 提供给 DeepSeek 生成回答。

流程：

User

↓

Agent Service

↓

Planner

↓

Vector Search

↓

Knowledge Context

↓

DeepSeek

↓

Answer

## Development Summary

本阶段完成 Markdown 知识库、文档向量化、FAISS 检索以及 RAG 集成。
通过 RAG 能力扩展，Agent 支持业务知识检索和非结构化信息理解。


## Technical Stack
Python 3.11
FastAPI
DeepSeek API
SentenceTransformer
FAISS

## Problems

当前知识库规模较小。
检索效果依赖文档质量和 Embedding 模型。

## Next Sprint
Sprint09：Conversation Memory Enhancement

优化 Agent 上下文管理，实现历史记录持久化和多轮对话能力增强。