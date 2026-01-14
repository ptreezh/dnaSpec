"""
任务分解技能适配器 - 为CLI提供标准execute接口
"""
import json
from typing import Dict, Any

# 直接从task_decomposer模块导入所需函数
from dna_spec_kit_integration.skills.task_decomposer import execute_task_decomposer

def execute(args: Dict[str, Any]) -> str:
    """
    标准执行接口 - 适配任务分解技能
    """
    return execute_task_decomposer(args)