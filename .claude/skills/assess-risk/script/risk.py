"""
Assess Risk Skill
心理风险评估 Skill（依赖 RAG 知识库）
检测自伤/自杀/受虐/伤人等危机信号，输出风险等级与转介建议
"""
from typing import Dict, Any, List
from loguru import logger

# 全局知识库实例（避免重复加载模型）
_kb_instance = None


def get_knowledge_base():
    """获取知识库单例"""
    global _kb_instance
    if _kb_instance is None:
        from knowledge.milvus_kb import PsychologyKnowledgeBase
        _kb_instance = PsychologyKnowledgeBase()
    return _kb_instance


# 危机信号（最高优先级，触发强制升级干预）
CRISIS_SIGNALS = [
    "自伤", "自杀", "轻生", "不想活", "结束生命", "伤害自己", "割腕", "跳楼",
    "服药自杀", "想死", "活不下去", "受虐", "家暴", "被虐待", "伤害他人",
    "失踪", "离家出走", "消失",
]

# 高风险心理困扰关键词
HIGH_RISK_KEYWORDS = ["持续低落", "重度", "功能受损", "拒学", "自贬", "幻觉", "妄想", "冲动", "攻击"]

# 中风险特征关键词
MEDIUM_RISK_KEYWORDS = ["持续", "加重", "反复", "严重", "剧烈", "两周以上", "失眠", "食欲骤变"]


async def assess_risk(symptoms: str) -> Dict[str, Any]:
    """
    评估心理风险等级（含危机检测）

    Args:
        symptoms: 困扰/情绪描述（字符串）

    Returns:
        {
            "answer": "格式化的风险评估结果",
            "risk_level": "low/medium/high/crisis",
            "recommendation": "转介/求助建议"
        }
    """
    logger.info(f"Assessing psychological risk: symptoms={symptoms}")

    # 将描述字符串转换为列表
    symptom_list = [s.strip() for s in symptoms.split(",") if s.strip()]
    if not symptom_list:
        symptom_list = [symptoms]

    risk_level = "low"
    reasons = []
    is_crisis = False

    # 1) 危机信号检测（最高优先级）
    for symptom in symptom_list:
        for crisis in CRISIS_SIGNALS:
            if crisis in symptom:
                is_crisis = True
                risk_level = "crisis"
                reasons.append(f"检测到危机信号：{symptom}")
                break
        if is_crisis:
            break

    # 2) 高风险困扰
    if not is_crisis:
        for symptom in symptom_list:
            if any(kw in symptom for kw in HIGH_RISK_KEYWORDS):
                risk_level = "high"
                reasons.append(f"高风险困扰特征：{symptom}")
                break

    # 3) 中风险特征
    if risk_level == "low":
        for symptom in symptom_list:
            if any(kw in symptom for kw in MEDIUM_RISK_KEYWORDS):
                risk_level = "medium"
                reasons.append(f"困扰特征提示需要关注：{symptom}")
                break

    # 生成建议
    if risk_level == "crisis":
        recommendation = ("⚠️ 立即干预：请马上联系信任的成人/学校心理老师，拨打心理援助热线 "
                         "400-161-9995 或 010-82951332；如有即时危险请拨打 120/110。")
    elif risk_level == "high":
        recommendation = "建议尽快寻求专业帮助：学校心理老师、心理咨询师或精神科评估，勿拖延。"
    elif risk_level == "medium":
        recommendation = "建议关注并观察变化，必要时联系心理老师或咨询师；学习基础调适方法。"
    else:
        recommendation = "建议保持自我观察，运用健康作息与社交支持；如困扰加重及时寻求帮助。"

    # 从 RAG 知识库获取相关心理建议
    kb_advice = None
    try:
        kb = get_knowledge_base()
        risk_query = f"{symptoms} 风险评估 调适建议 求助资源"
        results = kb.search(query=risk_query, top_k=1, filter_type=None)
        if results and results[0]["score"] > 0.5:
            kb_advice = results[0]["content"][:300]
    except Exception as e:
        logger.warning(f"Failed to get KB advice: {e}")

    return {
        "answer": format_assessment(symptoms, risk_level, reasons, recommendation, kb_advice),
        "risk_level": risk_level,
        "recommendation": recommendation,
        "kb_advice": kb_advice,
    }


def format_assessment(symptoms: str, level: str, reasons: list, recommendation: str, kb_advice: str = None) -> str:
    """格式化心理风险评估结果"""
    level_map = {
        "low": "低危 🟢",
        "medium": "中危 🟡",
        "high": "高危 🔴",
        "crisis": "危机 🚨",
    }

    output = [
        f"【心理风险评估】",
        f"\n困扰描述：{symptoms}",
        f"\n风险等级：{level_map.get(level, level)}",
    ]

    if reasons:
        output.append("\n风险提示：")
        for reason in reasons:
            output.append(f"  • {reason}")

    output.append(f"\n求助建议：{recommendation}")

    if kb_advice:
        output.append("\n【心理知识库补充】")
        output.append(kb_advice)

    if level == "crisis":
        output.append("\n🚨 请立即寻求专业支持，你并不孤单：")
        output.append("· 全国24小时心理援助热线：400-161-9995")
        output.append("· 北京心理危机研究与干预中心：010-82951332")
        output.append("· 青少年服务热线：12355")
    elif level == "high":
        output.append("\n🔴 建议尽快联系专业帮助，不要独自承受。")

    output.append("\n💡 数据来源：风险规则引擎 + 心理知识库（Milvus RAG）")

    return "\n".join(output)


def assess_risk_sync(symptoms: str) -> Dict[str, Any]:
    import asyncio
    return asyncio.run(assess_risk(symptoms))
