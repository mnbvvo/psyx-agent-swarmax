---
name: recommend-lifestyle
description: Provide psychological self-care and coping suggestions (sleep, exercise, relaxation, social support) for a stated concern. Use when a user needs everyday regulation strategies, not clinical treatment.
---

# Recommend Lifestyle (心理调适建议)

提供生活作息与心理调适建议（放松训练、运动、睡眠、社会支持）。

## When to Use

- 用户需要日常情绪调节方法
- 学习压力、人际、睡眠等一般困扰的应对
- 作为专业帮助之外的自助补充

## 底层实现

- 技术: 心理调适建议库 + Milvus 向量数据库（RAG）
- 数据源: 心理调适建议文档（lifestyle 类型）

## 调用方式

```bash
/recommend-lifestyle 考试焦虑
```
