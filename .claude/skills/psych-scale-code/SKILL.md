---
name: psych-scale-code
description: Look up psychological screening scales and coding references (PHQ-9, GAD-7, ICD-11/DSM-5 mental disorder categories). Provides educational info only; this skill does NOT diagnose.
---

# Psych Scale Code (心理量表 / 编码参考)

查询心理筛查量表与编码参考（PHQ-9、GAD-7、ICD-11/DSM-5 精神行为障碍分类）。

## When to Use

- 需要量表或编码标准的科普/参考
- 解释筛查工具与结果边界
- 为专业转介提供标准化依据

## 底层实现

- 技术: 量表/编码检索 + Milvus 向量数据库（RAG）
- 数据源: 心理量表/编码文档（disease_classification 类型）
- 注意: 仅作科普与转介参考，不替代专业诊断

## 调用方式

```bash
/psych-scale-code PHQ-9
```
