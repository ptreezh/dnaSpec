"""
约束生成技能适配器 - 为CLI提供标准execute接口
"""
import json
from typing import Dict, Any

# 直接从constraint_generator模块导入所需函数
from dna_spec_kit_integration.skills.constraint_generator import execute_constraint_generator

def execute(args: Dict[str, Any]) -> str:
    """
    标准执行接口 - 适配约束生成技能
    """
    return execute_constraint_generator(args)