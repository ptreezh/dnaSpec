"""
架构设计技能 - Claude & DNASPEC 双重兼容实现
"""
from typing import Dict, Any, Union
import json


def execute(args: Dict[str, Any]) -> str:
    """
    DNASPEC 标准执行接口
    """
    description = args.get("description", "").lower()
    
    # 使用字典映射关键字和架构，更易于扩展
    architecture_map = {
        "电商": "[WebApp] -> [API Server] -> [Database]",
        "博客": "[WebApp] -> [Database]",
        "用户管理": "[Frontend] -> [API Gateway] -> [Auth Service] -> [User DB]",
        "认证": "[Auth Service] -> [User DB] -> [Session Store]",
        "api": "[API Gateway] -> [Microservices] -> [Data Layer]"
    }

    for keyword, architecture in architecture_map.items():
        if keyword in description:
            return architecture

    # 默认返回
    return "根据需求设计系统架构: " + description


def handle_claude_request(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Claude Skills 标准接口
    """
    try:
        # 从 Claude 事件中提取输入
        input_text = (
            event.get('input') or 
            event.get('query') or 
            event.get('prompt', '')
        )
        
        # 准备 DNASPEC 格式的参数
        dnaspec_args = {
            'description': input_text
        }
        
        # 调用标准 DNASPEC 接口
        result = execute(dnaspec_args)
        
        # 格式化为 Claude 响应
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'result': result,
                'success': True,
                'input': input_text
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': str(e),
                'success': False
            })
        }


# Claude Skills 兼容的处理函数
def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    AWS Lambda 兼容的 Claude Skills 处理器
    """
    return handle_claude_request(event)


# 保持向后兼容性
__all__ = ['execute', 'handle_claude_request', 'lambda_handler']