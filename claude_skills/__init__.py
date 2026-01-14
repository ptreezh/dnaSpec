"""
Claude Skills 包初始化文件
提供与DNASPEC兼容的Claude Skills标准实现
"""
# 导入主技能实现
from .main import lambda_handler as execute

__all__ = ['execute', 'lambda_handler']


def lambda_handler(event, context):
    """
    Claude Skills标准Lambda处理器
    """
    return execute(event, context)