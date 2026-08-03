"""
Recommend Lifestyle Skill
生活方式建议 Skill（自包含，无需依赖tools）
"""
from typing import Dict, Any
from loguru import logger

# 全局知识库实例
_kb_instance = None

def get_knowledge_base():
    global _kb_instance
    if _kb_instance is None:
        from knowledge.milvus_kb import PsychologyKnowledgeBase
        _kb_instance = PsychologyKnowledgeBase()
    return _kb_instance


async def recommend_lifestyle(concern: str) -> Dict[str, Any]:
    """
    提供心理调适与生活方式建议

    Args:
        concern: 困扰或情绪议题描述

    Returns:
        {
            "answer": "格式化的心理调适建议",
            "concern": "困扰议题",
            "categories": ["relaxation", "exercise", "sleep", "social_support"]
        }
    """
    logger.info(f"Recommending lifestyle for: {concern}")

    # 使用知识库单例
    kb = get_knowledge_base()

    # 从 Milvus 检索心理调适建议
    results = kb.search(
        query=f"{concern} 心理调适 放松训练 作息 运动 社会支持",
        top_k=1,
        filter_type="lifestyle"
    )

    if results and results[0]["score"] > 0.1:
        doc = results[0]
        content = doc["content"]

        return {
            "answer": format_advice(concern, content),
            "concern": concern,
            "categories": ["relaxation", "exercise", "sleep", "social_support"],
            "source": "向量数据库"
        }
    else:
        # 未找到相关内容
        logger.warning(f"No coping advice found in vector DB for {concern}")
        return {
            "answer": f"未找到关于'{concern}'的调适建议，可尝试更具体的困扰描述或联系学校心理老师。",
            "concern": concern,
            "categories": [],
            "source": "未找到"
        }


def format_advice(concern: str, content: str) -> str:
    """格式化心理调适建议"""
    output = [
        f"【{concern} 心理调适建议】\n",
        content,
        "\n【免责声明】",
        "以上建议仅供参考，不能替代专业心理咨询师的指导。"
    ]

    return "\n".join(output)


def recommend_lifestyle_sync(concern: str) -> Dict[str, Any]:
    import asyncio
    return asyncio.run(recommend_lifestyle(concern))
