---
name: analyze-symptoms
description: Analyze psychological distress patterns (emotional/behavioral/cognitive/physical). Maps presenting concerns to possible issue areas for further assessment. Use when a user describes emotional, behavioral, cognitive, or somatic distress and needs pattern analysis (not a diagnosis).
---

# Analyze Symptoms (心理困扰模式分析)

将情绪/行为/认知/生理信号归类为困扰模式，提示可能关联的议题（非诊断）。

## When to Use

- 用户描述情绪、行为、认知或生理层面的困扰
- 需要梳理困扰的维度与关联
- 为风险评估或求助提供线索

## 底层实现

- 技术: 困扰四维分类（情绪/行为/认知/生理）+ Milvus 向量数据库
- 数据源: 困扰模式规则库 + 心理知识库（RAG）

## 调用方式

```bash
/analyze-symptoms 睡不着,不想上学,觉得自己没用
```
