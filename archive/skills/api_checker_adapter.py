"""
API检查技能适配器 - 为CLI提供标准execute接口
"""
import json
from typing import Dict, Any

# 直接从api_checker模块导入所需函数
from dna_spec_kit_integration.skills.api_checker import execute_api_checker

def execute(args: Dict[str, Any]) -> str:
    """
    标准执行接口 - 适配API检查技能
    """
    return execute_api_checker(args)