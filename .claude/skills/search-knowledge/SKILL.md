---
name: search-knowledge
description: Search psychology knowledge base. Use when user asks about psychology information, concern details, or general psychological knowledge. Fast semantic search powered by Milvus vector database.
---

# Search Psychology Knowledge (搜索心理知识库)

快速搜索心理知识库，获取困扰、表现、调适等相关信息。

## When to Use

- 用户问"焦虑是什么""抑郁的表现有哪些"
- 需要查询通用心理知识
- 简单、单步查询（不需要多步推理）

## 底层实现

- 技术: Milvus 向量数据库 + 语义检索
- 速度: 快速（<1秒）

## 调用方式

```bash
/search-knowledge 高血压的治疗方法
```

## 返回格式

```json
{
  "answer": "格式化的知识库检索结果",
  "total_found": 3,
  "query": "焦虑的调适方法"
}
```
