"""
自动修复器
根据约束违规自动修复输出

基于 Harness Engineering 原则：
- 自动检测问题
- 自动修复（在可能的情况下）
- 保持 Agent 输出质量
"""
from typing import Dict, Any, List
from loguru import logger

# 心理援助热线（中国大陆）
CRISIS_HOTLINES = (
    "如果你或你认识的人正处于危险中，请立即寻求帮助：\n"
    "· 全国24小时心理援助热线：400-161-9995\n"
    "· 北京心理危机研究与干预中心：010-82951332\n"
    "· 青少年服务热线：12355\n"
    "· 如有即时危险（自伤/伤人），请立即拨打 120（急救）或 110（报警），"
    "或联系信任的成人、老师、学校心理老师。"
)


class AutoFixer:
    """自动修复器"""

    def fix_output(
        self,
        output: str,
        auto_fixable: List[str]
    ) -> str:
        """
        自动修复输出

        Args:
            output: 原始输出
            auto_fixable: 可修复的违规列表

        Returns:
            修复后的输出
        """
        fixed_output = output

        for fix_type in auto_fixable:
            if fix_type == "add_disclaimer":
                fixed_output = self.fix_missing_disclaimer(fixed_output)
            elif fix_type == "add_emergency_warning":
                fixed_output = self.fix_high_risk_warning(fixed_output)
            elif fix_type == "add_crisis_intervention":
                fixed_output = self.fix_crisis_intervention(fixed_output)

        if fixed_output != output:
            logger.info("🔧 输出已自动修复")

        return fixed_output

    def fix_missing_disclaimer(self, output: str) -> str:
        """
        自动添加免责声明

        Args:
            output: 原始输出

        Returns:
            添加免责声明后的输出
        """
        if "免责" not in output and "仅供参考" not in output:
            disclaimer = "\n\n【免责声明】\n以上信息仅供参考，不能替代精神科医生或专业心理咨询师的评估与诊断。如有需要，请及时寻求专业帮助。"
            logger.debug("+ 自动添加免责声明")
            return output + disclaimer
        return output

    def fix_high_risk_warning(self, output: str) -> str:
        """
        自动添加高危/危机警告

        Args:
            output: 原始输出

        Returns:
            添加警告后的输出
        """
        crisis_keywords = ["自伤", "自杀", "轻生", "不想活", "伤害自己", "受虐", "伤害他人"]
        medical_keywords = ["胸痛", "呼吸困难", "昏厥", "剧烈头痛", "心悸", "突然视力模糊"]

        if any(kw in output for kw in crisis_keywords + medical_keywords):
            if not any(kw in output for kw in ["热线", "医院", "就医", "心理老师", "求助", "120", "110"]):
                warning = "⚠️ **重要提醒**：你提到的情况需要立即获得专业支持，请不要独自承受。\n\n"
                logger.debug("+ 自动添加危机/高危警告")
                return warning + output

        return output

    def fix_crisis_intervention(self, output: str) -> str:
        """
        自动追加危机干预与心理援助热线

        Args:
            output: 原始输出

        Returns:
            追加危机干预信息后的输出
        """
        if not any(kw in output for kw in ["热线", "心理老师", "求助", "120", "110", "医院"]):
            block = "\n\n【危机干预 · 请立即寻求帮助】\n" + CRISIS_HOTLINES + "\n"
            logger.debug("+ 自动追加危机干预热线")
            return output + block
        return output

    def fix_excessive_length(self, output: str, max_length: int) -> str:
        """
        截断过长的输出

        Args:
            output: 原始输出
            max_length: 最大长度

        Returns:
            截断后的输出
        """
        if len(output) > max_length:
            logger.warning(f"输出过长（{len(output)} > {max_length}），自动截断")
            truncated = output[:max_length - 50]  # 保留50字空间添加提示
            truncated += "\n\n[回答内容较长，已截断。如需完整信息，请咨询专业医生]"
            return truncated

        return output

    def remove_diagnosis_statements(self, output: str) -> str:
        """
        移除明确的诊断语句（高级功能，需要 LLM 辅助）

        Args:
            output: 原始输出

        Returns:
            移除诊断语句后的输出
        """
        # 简单替换（实际应该使用 LLM 进行更智能的重写）
        output = output.replace("您患有", "可能存在")
        output = output.replace("确诊为", "建议检查")
        output = output.replace("肯定是", "很可能是")

        return output
