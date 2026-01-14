"""
模块化技能适配器 - 为CLI提供标准execute接口
"""
import json
from typing import Dict, Any

# 直接从modulizer_independent模块导入所需函数
from dna_spec_kit_integration.skills.modulizer_independent import execute_modulizer

def execute(args: Dict[str, Any]) -> str:
    """
    标准执行接口 - 适配模块化技能
    """
    return execute_modulizer(args)