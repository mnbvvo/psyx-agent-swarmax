"""
心理陪伴 / 倾听 / 科普 Agent
支持 Skills 调用
"""
from typing import Dict, Any
from loguru import logger
import re

from .base_agent import BaseAgent
from .skill_registry_mixin import SkillRegistryMixin


class ConsultationAgent(BaseAgent, SkillRegistryMixin):
    """
    心理陪伴 / 倾听 / 科普 Agent
    通过 Skills 调用底层工具
    """

    def __init__(self, config: Dict[str, Any] = None):
        default_config = {
            "model": "openai_compatible",
            "max_iterations": 5,
            "temperature": 0.8,
            "description": "心理陪伴与科普Agent，提供倾听、情绪支持与心理调适建议"
        }

        config = config or default_config
        super().__init__(
            agent_id="consultation_agent",
            config=config
        )

        # 设置能力标签（Swarm 协作用）
        self.set_capabilities([
            "general_psychological_support",
            "emotional_listening",
            "risk_screening",
            "psychoeducation"
        ])

    def get_system_prompt(self) -> str:
        """获取系统提示词"""
        return """你是一位温暖、专业的青少年心理陪伴顾问。你的职责是倾听、共情，并提供安全、适龄的心理支持与科普。

可用 Skills（9个）：
1. search_knowledge: 搜索心理知识库（调适方法、发展心理学、常见困扰）
2. recommend_lifestyle: 提供生活作息与心理调适建议（睡眠、运动、放松、社交支持）
3. assess_risk: 评估当前困扰的风险等级（低/中/高/危机）
4. analyze_symptoms: 分析情绪/行为/认知困扰的模式与可能关联
5. psych_scale_code: 查询心理筛查量表编码（ICD-11 精神行为障碍、PHQ-9、GAD-7 等）
6. clinical_guideline: 检索心理干预指南与循证实践（CBT、DBT、正念等）
7. deep_research: 深度研究（网络搜索+知识库+证据综合）
8. search_history: 搜索当前会话的历史对话（短期记忆）
9. search_similar_cases: 搜索相似历史案例（长期记忆）

**Skills 使用原则**：
- Skills 是可选的，不是必须的
- 对于简单的倾诉与陪伴，优先倾听与共情，无需调用 Skills
- 只在确实需要专业心理信息时调用 Skills
- 调用 Skill 后，基于结果给出最终回应
- **最多使用2-3个 Skills，然后必须给出最终回应**

工作流程建议：
1. 先共情、确认对方的感受（反映式倾听）
2. 判断是否需要调用 Skills（简单陪伴直接回应）
3. 如需调用，选择最合适的 Skills（通常1-2个即可）
4. 基于 Skill 结果生成最终回应

回答要求：
- 使用青少年能理解的语言，避免生硬的专业术语（必要时解释）
- 保持共情、不评判、尊重的语气
- 提供具体、可操作的小步骤建议
- 主动完成危机筛查：若对方流露出无助、无望或伤害自己的念头，温和询问并链接帮助
- 不替代专业诊断与治疗

**重要提醒**：
- 你不能做出明确的心理/精神诊断
- 你不能替代精神科医生或心理咨询师的专业意见
- 对于自伤、自杀、受虐等危机信号，必须立即提供心理援助热线并建议寻求专业帮助
- 保护未成年人：当存在即时危险时，保密让位于安全

在最终回答时，请按以下格式输出：

【回答】
[你的共情与具体回应]

【核心建议】
1. 第一条建议
2. 第二条建议
...

【免责声明】
以上信息仅供参考，不能替代精神科医生或专业心理咨询师的评估与诊断。如有需要，请及时寻求专业帮助。
"""

    def register_tools(self):
        """注册所有 9 个 Skills（共享实现，来自 SkillRegistryMixin）"""
        self.register_all_skills()

    def format_user_input(self, input_data: Dict[str, Any]) -> str:
        """格式化用户输入"""
        question = input_data.get('question', '')
        session_id = input_data.get('session_id', '')

        # 构建消息
        parts = []

        # 添加session_id信息（如果有）
        if session_id:
            parts.append(f"[系统信息] 当前会话ID: {session_id}")

        # 添加上下文信息（如果有）
        context = input_data.get('context', {})
        if context:
            context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
            parts.append(f"背景信息：\n{context_str}\n")

        # 添加用户问题
        parts.append(f"用户问题：{question}")

        return "\n".join(parts)

    async def post_process_result(
        self,
        result: Dict[str, Any],
        final_response: str
    ) -> Dict[str, Any]:
        """
        后处理：从最终响应中提取结构化信息
        """
        # 提取核心建议
        suggestions = []
        suggestion_pattern = r'【核心建议】\s*\n((?:\d+\.\s*.+\n?)+)'
        match = re.search(suggestion_pattern, final_response)

        if match:
            suggestion_text = match.group(1)
            suggestion_lines = re.findall(r'\d+\.\s*(.+)', suggestion_text)
            suggestions = [s.strip() for s in suggestion_lines if s.strip()]

        # 提取免责声明
        disclaimer_pattern = r'【免责声明】\s*\n(.+)'
        disclaimer_match = re.search(disclaimer_pattern, final_response)
        disclaimer = disclaimer_match.group(1) if disclaimer_match else \
            "⚠️ 以上信息仅供参考，不能替代精神科医生或专业心理咨询师的评估与诊断。如有需要，请及时寻求专业帮助。"

        result.update({
            'suggestions': suggestions[:5],  # 最多5条
            'disclaimer': disclaimer
        })

        return result


# 便捷函数
async def consult(question: str, **kwargs) -> Dict[str, Any]:
    """快捷咨询函数"""
    agent = ConsultationAgent()
    return await agent.process({'question': question, **kwargs})
