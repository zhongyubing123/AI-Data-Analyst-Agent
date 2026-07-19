# Sprint 08：RAG Knowledge Enhancement

> Date：2026-07-18  
> Author：zhongyubing


---

# Sprint Goal


在 AI Data Analyst Agent 基础上，引入 RAG（Retrieval Augmented Generation）能力，使 Agent 除了查询数据库外，还能够检索项目知识和业务文档。


本 Sprint 实现：

- Markdown 知识库构建
- 文档向量化
- FAISS 相似度搜索
- 检索结果增强 Prompt
- Agent 集成知识问答


提升 Agent 对非结构化信息的理解能力。


---

# Background


前几个 Sprint 已完成：


## Sprint06

完成：

- NL2SQL
- Schema Prompt
- SQL 查询流程


实现：
