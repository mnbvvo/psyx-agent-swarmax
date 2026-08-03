"""
DiagnosticAgent：心理风险评估 / 危机检测 Agent

这是第一个 WorkerAgent 实现，展示如何：
1. 参与 Swarm 协作
2. 自主认领任务
3. 调用心理工具
4. 将结果写入 SharedContext
"""
from typing import Dict, Any, Optional
from loguru import logger

from .base_agent import BaseAgent
from .skill_registry_mixin import SkillRegistryMixin
from core import LLMClient


class DiagnosticAgent(BaseAgent, SkillRegistryMixin):
    """
    心理风险评估 Agent（不诊断，只分级与转介）

    职责：
    - 青少年心理困扰的风险分级
    - 危机信号检测（自伤/自杀/受虐/伤人）
    - 困扰模式的关联分析
    - 给出就医/求助的转介建议

    能力标签：
    - risk_assessment
    - crisis_detection
    - differential_reasoning
    - distress_pattern_analysis
    """

    def __init__(
        self,
        agent_id: str = "diagnostic_agent",
        config: Optional[Dict[str, Any]] = None,
        llm_client: Optional[LLMClient] = None
    ):
        config = config or {}
        config.setdefault('max_iterations', 5)

        super().__init__(agent_id, config, llm_client)

        # 设置能力标签（Swarm 协作用）
        self.set_capabilities([
            "risk_assessment",
            "crisis_detection",
            "differential_reasoning",
            "distress_pattern_analysis"
        ])

    def register_tools(self):
        """注册所有 9 个 Skills（共享实现，来自 SkillRegistryMixin）"""
        self.register_all_skills()

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """你是专业的心理风险评估 Agent（DiagnosticAgent）。你的职责是：
1. 分析情绪/行为/认知困扰的模式与关联性
2. 进行风险分级（低/中/高/危机）
3. 检测危机信号（自伤、自杀、受虐、伤人）
4. 给出就医与求助的转介建议（不做诊断）

**评估原则**：
- 使用循证心理评估框架（如哥伦比亚自杀严重程度评定量表 C-SSRS 的思路）
- 优先考虑安全：任何危机信号都优先升级干预
- 区分"正常的发展性困扰"与"需要专业介入的状况"
- 永远不做明确诊断，只提供风险研判与转介思路

**可用 Skills（9个）**：
1. search_knowledge: 搜索心理知识库
2. recommend_lifestyle: 生活作息与调适建议
3. assess_risk: 评估风险等级（低/中/高/危机）
4. analyze_symptoms: 分析困扰模式（情绪/行为/认知/生理）
5. psych_scale_code: 查询心理筛查量表编码（ICD-11、PHQ-9、GAD-7 等）
6. clinical_guideline: 检索心理干预指南与循证实践
7. deep_research: 深度研究
8. search_history: 搜索当前会话历史（短期记忆）
9. search_similar_cases: 搜索相似历史案例（长期记忆）

**Skills 使用策略**：
- 首先使用 assess_risk 评估风险
- 然后使用 analyze_symptoms 分析模式
- 如需量表/编码，使用 psych_scale_code
- 如需权威指南，使用 clinical_guideline
- 基于 Skill 结果进行风险研判
- 最多2-3次 Skill 调用，然后给出研判

**Swarm 协作模式**：
- 你可能从 SharedContext 读取其他 Agent 的评估结果
- 你的风险评估会被其他 Agent（如 ConsultationAgent）用于回应
- 专注于你的专长：风险分级与危机检测

**输出格式**：
【风险评估】
风险等级：...（低/中/高/危机）
紧急程度：...

【困扰模式分析】
主要困扰类别：...
模式关联性：...

【风险研判】
1. 关注点A（可能性/严重度）
   - 支持依据：...
   - 需排除/警惕：...
2. 关注点B（可能性/严重度）
   ...

【建议转介】
- 建议寻求的专业帮助（心理老师/心理咨询师/精神科）
- 如有危机：立即提供心理援助热线与紧急联系方式

【推理过程】
简述风险研判逻辑...
"""

    async def post_process_result(
        self,
        result: Dict[str, Any],
        final_response: str
    ) -> Dict[str, Any]:
        """
        结果后处理：提取结构化风险信息
        """
        # 尝试提取风险等级
        risk_level = "unknown"
        if "危机" in final_response or "CRISIS" in final_response:
            risk_level = "crisis"
        elif "风险等级" in final_response:
            if "高" in final_response or "HIGH" in final_response:
                risk_level = "high"
            elif "中" in final_response or "MEDIUM" in final_response:
                risk_level = "medium"
            elif "低" in final_response or "LOW" in final_response:
                risk_level = "low"

        result.update({
            "risk_level": risk_level,
            "assessment_provided": True
        })

        return result


# 便捷函数
async def diagnose(question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    便捷函数：快速使用 DiagnosticAgent 进行心理风险评估

    Args:
        question: 困扰描述
        context: 额外上下文（年龄、既往史等）

    Returns:
        风险评估结果
    """
    agent = DiagnosticAgent()
    input_data = {'question': question}
    if context:
        input_data['context'] = context

    return await agent.process(input_data)
