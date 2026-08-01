"""
Analyze Symptoms Skill
心理困扰模式分析 Skill（依赖 RAG 知识库）
将情绪/行为/认知/生理信号归类为困扰模式，提示可能关联的议题（非诊断）
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


async def analyze_symptoms(symptoms: str) -> Dict[str, Any]:
    """
    分析心理困扰模式

    Args:
        symptoms: 困扰描述（字符串）

    Returns:
        {
            "answer": "格式化的困扰模式分析",
            "patterns": ["模式1", "模式2"],
            "possible_concerns": ["可能议题1", "可能议题2"]
        }
    """
    logger.info(f"Analyzing distress: {symptoms}")

    symptom_list = [s.strip() for s in symptoms.split(",") if s.strip()]
    if not symptom_list:
        symptom_list = [symptoms]

    # 心理困扰分类（四维模型）
    distress_categories = {
        "emotional": {
            "keywords": ["难过", "悲伤", "焦虑", "恐惧", "愤怒", "空虚", "无助", "无望", "内疚", "烦躁"],
            "name": "情绪维度"
        },
        "behavioral": {
            "keywords": ["厌学", "退避", "失眠", "暴食", "厌食", "自伤", "攻击", "成瘾", "拖延", "孤僻"],
            "name": "行为维度"
        },
        "cognitive": {
            "keywords": ["注意力不集中", "记忆力下降", "消极想法", "自我否定", "灾难化", "钻牛角尖", "犹豫"],
            "name": "认知维度"
        },
        "physical": {
            "keywords": ["头痛", "胃痛", "心悸", "胸闷", "乏力", "食欲", "心慌", "手抖", "睡眠"],
            "name": "生理维度"
        },
    }

    detected_categories = []
    for cat_id, cat_data in distress_categories.items():
        for symptom in symptom_list:
            if any(kw in symptom for kw in cat_data["keywords"]):
                if cat_id not in [c["id"] for c in detected_categories]:
                    detected_categories.append({"id": cat_id, "name": cat_data["name"]})
                break

    patterns = []
    if detected_categories:
        names = [c["name"] for c in detected_categories]
        patterns.append(f"困扰涉及：{', '.join(names)}")

    if len(detected_categories) > 1:
        patterns.append("多维度困扰，建议综合评估而非单一归因")

    # 可能的议题关联（基于维度，非诊断）
    possible_concerns = []
    for cat in detected_categories:
        if cat["id"] == "emotional":
            possible_concerns.extend(["情绪调节困难", "焦虑/抑郁倾向待评估"])
        elif cat["id"] == "behavioral":
            possible_concerns.extend(["适应/行为问题", "回避或退缩"])
        elif cat["id"] == "cognitive":
            possible_concerns.extend(["负性认知偏向", "注意力/学业影响"])
        elif cat["id"] == "physical":
            possible_concerns.extend(["心身反应", "睡眠/躯体化"])

    possible_concerns = list(set(possible_concerns))[:5]

    # 从 RAG 知识库补充
    kb_insights = []
    if possible_concerns:
        try:
            kb = get_knowledge_base()
            for concern in possible_concerns[:3]:
                results = kb.search(query=f"{concern} 调适 干预", top_k=1, filter_type=None)
                if results and results[0]["score"] > 0.5:
                    kb_insights.append({"concern": concern, "info": results[0]["content"][:200]})
        except Exception as e:
            logger.warning(f"Failed to get KB insights: {e}")

    return {
        "answer": format_analysis(symptoms, patterns, possible_concerns, kb_insights),
        "patterns": patterns,
        "possible_concerns": possible_concerns,
        "kb_insights": kb_insights,
    }


def format_analysis(symptoms: str, patterns: list, concerns: list, kb_insights: list = None) -> str:
    """格式化困扰模式分析"""
    output = [
        f"【心理困扰模式分析】",
        f"\n困扰描述：{symptoms}",
    ]

    if patterns:
        output.append("\n识别到的困扰模式：")
        for pattern in patterns:
            output.append(f"  • {pattern}")

    if concerns:
        output.append("\n可能关联的议题（非诊断）：")
        for concern in concerns:
            output.append(f"  • {concern}")

    if kb_insights:
        output.append("\n【知识库补充信息】")
        for insight in kb_insights:
            output.append(f"\n关于 {insight['concern']}：")
            output.append(f"{insight['info']}")

    output.append("\n⚠️ 以上仅为模式分析，不能替代专业心理评估。如困扰持续或加重，请寻求专业帮助。")
    output.append("💡 数据来源：困扰模式分析 + 心理知识库（Milvus RAG）")

    return "\n".join(output)


def analyze_symptoms_sync(symptoms: str) -> Dict[str, Any]:
    import asyncio
    return asyncio.run(analyze_symptoms(symptoms))
