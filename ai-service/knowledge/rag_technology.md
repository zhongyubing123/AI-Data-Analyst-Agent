# RAG技术说明


RAG全称 Retrieval-Augmented Generation。

中文名称：
检索增强生成。


RAG流程：

1. 文档切片

2. 文本向量化

3. 保存到向量数据库

4. 用户问题向量化

5. 相似度检索

6. 将检索结果提供给大语言模型生成回答


FAISS是Facebook AI Similarity Search。

项目中使用FAISS作为向量检索工具。


FAISS作用：

- 保存文本向量
- 进行相似度搜索
- 快速找到相关知识片段


Sentence Transformers用于文本Embedding。

