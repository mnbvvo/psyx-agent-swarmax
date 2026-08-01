# PsyX 多智能体青少年心理助手

基于 Skills-Agent 两层架构的多智能体协作心理辅助系统，融合 Agent Loop、Agent Swarm、记忆管理和 Milvus 知识库。面向 **6-18 岁青少年及其家长**，提供倾听陪伴、心理科普、风险评估与资源转介。

> ⚠️ 本项目仅用于学习/研究与原型验证，**不能替代精神科医生或专业心理咨询师的诊断与治疗**。涉及自伤、自杀、受虐、伤人等危机信号时，系统会强制升级干预并提供心理援助热线。

## 🎯 核心特性

- **🔧 Skills 直达架构**: 9 个原子 Skills 自包含，直接转换为 OpenAI function calling 格式 ✅
- **🤖 Agent Loop**: LLM 驱动的 Skill 调用循环，Agent 自主规划、调用 Skills 并完成任务 ✅
- **🐝 Agent Swarm**: 去中心化群体协作，危机信号自动触发风险评估 Agent 介入 ✅
- **🧠 记忆系统**: 短期记忆（会话级）+ 长期记忆（Mem0 跨会话）✅
- **💾 Milvus 知识库**: 心理调适建议、筛查量表、干预指南的统一语义检索 ✅
- **🛡️ 危机拦截（Harness）**: 约束驱动的越界检测 + 自动修复（补免责声明、补危机热线）✅

## 🛡️ 安全与危机干预（本项目的重点）

心理辅助与医疗辅助最大的不同在于**危机红线**：

- `constraints/agent_constraints.yaml` 定义每个 Agent 的能力边界与禁止行为，红线包括：
  - `encourage_self_harm`（绝不鼓励自伤/自杀）
  - `diagnose_mental_disorder` / `prescribe_medication`（不诊断、不开药）
  - `must_screen_for_crisis`（必须完成危机筛查）
  - `protect_minor`（未成年人保护优先于保密）
- `constraints/validator.py` + `validation/auto_fixer_*.py`：运行时检测危机关键词（自伤/自杀/受虐/伤人），自动追加心理援助热线（400-161-9995、010-82951332、12355）。
- `assess-risk` Skill：内置危机信号规则引擎，输出风险等级（低/中/高/危机）。
- `swarm_constraints.yaml`：用户表述含危机关键词时，强制引入 `diagnostic_agent` 进行风险评估。

> 热线（中国大陆）：全国24小时心理援助热线 400-161-9995 ｜ 北京心理危机研究与干预中心 010-82951332 ｜ 青少年服务热线 12355 ｜ 即时危险拨打 120/110。

## 📋 Skills 与 Agent 清单

### 9 个原子 Skills（所有 Agent 共享）

| Skill | 功能 | 数据源 |
|-------|------|--------|
| `search_knowledge` | 搜索心理知识库 | Milvus |
| `recommend_lifestyle` | 心理调适/自助建议 | Milvus |
| `assess_risk` | 心理风险/危机评估 | 规则引擎 + RAG |
| `analyze_symptoms` | 困扰模式分析（情绪/行为/认知/生理） | 规则引擎 + RAG |
| `disease_code` | 心理量表/诊断编码参考（PHQ-9、GAD-7、ICD-11） | Milvus |
| `clinical_guideline` | 心理干预指南检索（CBT、危机干预等） | Milvus |
| `deep_research` | 深度研究（网络搜索+证据综合） | 网络搜索 |
| `search_history` | 搜索当前会话历史（短期记忆） | 内存 |
| `search_similar_cases` | 搜索相似历史案例（长期记忆） | Mem0 |

### 3 个专业 Agent

- **ConsultationAgent（心理陪伴/倾听/科普）**：共情倾听、情绪支持、心理调适建议。
- **DiagnosticAgent（心理风险评估/危机检测）**：困扰风险分级、危机信号检测、求助转介（不做诊断）。
- **ResearchAgent（循证心理研究）**：指南、文献、量表、最新进展检索与证据综合。

### 2 个协调 Agent

- **LeadAgent**: 任务分解与结果汇总。
- **SwarmCoordinator**: 智能路由（简单问题→单Agent，危机/复杂问题→Swarm）。

## 🚀 从零开始运行

```bash
conda create -n psyx-swarm python=3.12 -y
conda activate psyx-swarm
cd psyx-agent-swarm
pip install -r requirements.txt
```

### 配置 API（项目根目录的 `.env` 文件）

复制模板并填写密钥：

```bash
cp .env.example .env
```

`.env` 内容示例：

```bash
# LLM API 配置（OpenAI 兼容端点，如字节豆包 / OpenAI / DeepSeek）
LLM_API_KEY=your-llm-api-key
LLM_MODEL_NAME=doubao-seed-1-6-flash-250828
LLM_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=8192

# Mem0 长期记忆（可选，留空则关闭）
MEM0_API_KEY=
```

> 配置读取逻辑见 `core/config_loader.py`，优先级为：`.env` 文件 > 系统环境变量。`python-dotenv` 已在 `requirements.txt` 中声明。

### 初始化知识库

```bash
python knowledge/scripts/import_hardcoded_data.py
```

### 运行

```bash
python main.py                 # 交互式
python examples/test_all.py    # 测试套件（含约束与危机检测）
```

## 📦 知识库

- 向量数据库: Milvus Lite（本地文件）
- Embedding: BAAI/bge-small-zh-v1.5（中文，512 维）
- 文档: `knowledge/data/documents/*.txt`
  - `01-09`: 心理调适建议（coping）
  - `10-19`: 心理筛查量表 / 诊断编码（psych_scale）
  - `20-29`: 心理干预指南（clinical_guideline）

## ⚠️ 免责声明

本系统仅供学习和研究使用，不能替代专业心理/精神科服务。所有建议仅供参考，如遇心理危机请立即拨打心理援助热线或紧急电话。

## 📄 许可证

MIT License
