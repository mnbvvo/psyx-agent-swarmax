---
name: disease-code
description: Look up psychological screening scales and diagnostic coding references (PHQ-9, GAD-7, ICD-11/DSM-5 mental disorder categories). Provides educational info only; this skill does NOT diagnose.
---

# Disease Code (心理量表 / 诊断编码)

查询心理筛查量表与诊断编码参考（PHQ-9、GAD-7、ICD-11/DSM-5 精神行为障碍分类）。

## When to Use

- 需要量表或诊断标准的科普/编码参考
- 解释筛查工具与结果边界
- 为专业转介提供标准化依据

## 底层实现

- 技术: 量表/编码检索 + Milvus 向量数据库（RAG）
- 数据源: 心理量表/诊断编码文档（disease_classification 类型）
- 注意: 仅作科普与转介参考，不替代专业诊断

## 调用方式

```bash
/disease-code PHQ-9
```
