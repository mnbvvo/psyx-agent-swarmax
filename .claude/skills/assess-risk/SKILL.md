---
name: assess-risk
description: Assess psychological risk level (low/medium/high/crisis). Detects crisis signals such as self-harm, suicidal ideation, abuse, or harm to others, and recommends professional help or hotlines. Use when a user describes distress, hopelessness, or any risk of harm.
---

# Assess Risk (心理风险评估)

评估心理风险等级，检测自伤/自杀/受虐/伤人等危机信号，给出转介与求助建议。

## When to Use

- 用户表达情绪低落、无助、无望
- 出现自伤、自杀、受虐、伤人等危机信号
- 需要判断困扰的严重程度与求助优先级
- 风险分级（低/中/高/危机）

## 底层实现

- 技术: 危机规则引擎 + Milvus 向量数据库
- 数据源: 危机信号规则库 + 心理知识库（RAG）
- 增强: 从知识库检索调适与求助资源

## 调用方式

```bash
/assess-risk 最近总想消失，觉得活着没意思
```
