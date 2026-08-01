"""
集中加载 PsyX 项目配置（来自项目根目录的 .env 文件）。

原先分散在 config.py 的 LLM_CONFIG / MEM0_CONFIG 改为从环境变量读取，
便于用 .env 文件配置密钥，避免把敏感信息写进代码库。

用法：
    from core.config_loader import LLM_CONFIG, MEM0_CONFIG

优先级：.env 文件中的值 > 系统环境变量（load_dotenv 默认不覆盖已存在的环境变量）。
"""
from pathlib import Path
import os
from dotenv import load_dotenv

# 项目根目录（psyx-agent-swarm/）；本文件位于 core/ 下
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

# 加载 .env（文件不存在时静默忽略，仍可依赖系统环境变量）
load_dotenv(ENV_PATH, override=False)


def _to_float(value, default):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# LLM API 配置（OpenAI 兼容端点，如字节豆包 / OpenAI / DeepSeek）
LLM_CONFIG = {
    "api_key": os.getenv("LLM_API_KEY", ""),
    "model_name": os.getenv("LLM_MODEL_NAME", "doubao-seed-1-6-flash-250828"),
    "base_url": os.getenv("LLM_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"),
    "temperature": _to_float(os.getenv("LLM_TEMPERATURE"), 0.7),
    "max_tokens": _to_int(os.getenv("LLM_MAX_TOKENS"), 8192),
}

# Mem0 长期记忆配置（可选，留空则关闭长期记忆）
MEM0_CONFIG = {
    "api_key": os.getenv("MEM0_API_KEY", ""),
}
