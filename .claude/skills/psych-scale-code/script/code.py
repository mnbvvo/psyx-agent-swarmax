"""
Psych Scale Code Skill
心理量表编码查询 Skill（自包含，无需依赖tools）
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


async def psych_scale_code(scale_name: str) -> Dict[str, Any]:
    """
    查询心理筛查量表编码（ICD-11），如 PHQ-9、GAD-7

    Args:
        scale_name: 量表或议题名称

    Returns:
        {
            "answer": "格式化的量表编码信息",
            "icd11_code": "ICD-11 编码",
            "category": "量表分类"
        }
    """
    logger.info(f"Searching ICD-11 code for: {scale_name}")

    # 使用知识库单例
    kb = get_knowledge_base()

    # 使用 Milvus 检索心理筛查量表编码
    results = kb.search(
        query=f"{scale_name} 量表 编码 筛查 标准",
        top_k=1,
        filter_type="disease_classification"
    )

    if results and results[0]["score"] > 0.1:
        doc = results[0]
        metadata = doc["metadata"]

        # 从内容中提取编码（简单解析）
        content = doc["content"]
        icd11_code = metadata.get("icd11_code", "")
        if not icd11_code and ("编码：" in content or "ICD-11编码：" in content):
            # 从内容中提取
            lines = content.split("\n")
            for line in lines:
                if "编码：" in line:
                    icd11_code = line.split("：", 1)[1].strip()
                    break

        return {
            "answer": format_code_info(scale_name, content),
            "icd11_code": icd11_code,
            "category": metadata.get("category", ""),
            "source": "向量数据库"
        }
    else:
        # 未找到相关内容
        logger.warning(f"No scale/code found in vector DB for {scale_name}")
        return {
            "answer": f"未找到'{scale_name}'的量表或编码信息，建议使用更标准的名称或联系专业人员。",
            "icd11_code": "",
            "category": "",
            "source": "未找到"
        }


def format_code_info(scale_name: str, content: str) -> str:
    """格式化心理量表/编码信息"""
    output = [
        f"【心理量表 / 编码信息】\n",
        content
    ]

    return "\n".join(output)


def psych_scale_code_sync(scale_name: str) -> Dict[str, Any]:
    import asyncio
    return asyncio.run(psych_scale_code(scale_name))
