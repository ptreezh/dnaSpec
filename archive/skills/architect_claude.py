"""
Claude Skills 规范的架构设计技能实现
符合 Claude 官方 Skills 规范
"""
import json
from typing import Dict, Any, Union


def execute_skill(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Claude Skills 标准执行函数
    """
    try:
        # 从事件中提取参数
        requirements = event.get('requirements') or event.get('input') or event.get('query', '')
        
        # 使用架构映射
        architecture_map = {
            "电商": "[WebApp] -> [API Server] -> [Database]",
            "博客": "[WebApp] -> [Database]",
            "用户管理": "[Frontend] -> [API Gateway] -> [Auth Service] -> [User DB]",
            "认证": "[Auth Service] -> [User DB] -> [Session Store]",
            "api": "[API Gateway] -> [Microservices] -> [Data Layer]"
        }

        # 查找匹配的架构
        for keyword, architecture in architecture_map.items():
            if keyword in requirements.lower():
                result = {
                    "success": True,
                    "result": architecture,
                    "architecture_type": keyword,
                    "input": requirements
                }
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(result)
                }

        # 默认返回
        result = {
            "success": True,
            "result": f"根据需求设计系统架构: {requirements}",
            "architecture_type": "custom",
            "input": requirements
        }
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result)
        }
        
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'input': event
        }
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(error_result)
        }


def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    AWS Lambda 兼容的处理函数
    """
    return execute_skill(event, context)


# 同时保留 DNASPEC 格式的 execute 函数以保持兼容性
def execute(args: Dict[str, Any]) -> str:
    """
    DNASPEC 格式的执行函数
    """
    description = args.get("description", args.get("requirements", "")).lower()
    
    # 使用架构映射
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
    return f"根据需求设计系统架构: {description}"