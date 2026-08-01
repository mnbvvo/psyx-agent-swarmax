---
name: clinical-guideline
description: Retrieve evidence-based psychological intervention guidelines and expert consensus (CBT, DBT, crisis intervention, teen depression). Use when a user or another agent needs authoritative, cited guidance.
---

# Clinical Guideline (心理干预指南)

检索心理干预指南与循证实践（CBT、DBT、危机干预、青少年抑郁等）。

## When to Use

- 需要权威、可引用的心理干预指引
- 验证其他 Agent 的干预建议
- 提供证据等级与来源

## 底层实现

- 技术: 指南检索 + Milvus 向量数据库（RAG）
- 数据源: 心理干预指南文档（clinical_guideline 类型）

## 调用方式

```bash
/clinical-guideline 青少年抑郁 干预
```
