"""
Claude Skills 规范的约束生成技能实现
符合 Claude 官方 Skills 规范
"""
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List


def execute_skill(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Claude Skills 标准执行函数
    """
    try:
        # 从事件中提取参数
        requirements = event.get('requirements') or event.get('input') or event.get('query', '')
        change_request = event.get('change_request', '')
        
        if not requirements.strip():
            error_result = {
                "success": False,
                "error": "Requirements input is required for constraint generation",
                "input": requirements
            }
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(error_result)
            }

        # 生成约束（简化版本）
        req_lower = requirements.lower()
        constraints = []
        
        # 安全约束
        if any(term in req_lower for term in ['security', 'secure', 'auth', 'encrypt', 'privacy', 'protect']):
            constraints.append({
                "id": f"constraint_{uuid.uuid4().hex[:8]}",
                "type": "security",
                "description": "系统必须实现标准安全措施",
                "severity": "high",
                "created_at": datetime.now().isoformat()
            })

        # 性能约束
        if any(term in req_lower for term in ['performance', 'fast', 'response', 'throughput', 'latency']):
            constraints.append({
                "id": f"constraint_{uuid.uuid4().hex[:8]}",
                "type": "performance", 
                "description": "系统必须满足定义的性能要求",
                "severity": "medium",
                "created_at": datetime.now().isoformat()
            })

        # 数据约束
        if any(term in req_lower for term in ['data', 'database', 'storage', 'retrieve', 'persist']):
            constraints.append({
                "id": f"constraint_{uuid.uuid4().hex[:8]}",
                "type": "data_integrity",
                "description": "系统必须保持数据完整性和备份能力",
                "severity": "high", 
                "created_at": datetime.now().isoformat()
            })

        # 对齐检查
        alignment_check = {
            "is_aligned": not (change_request and 
                             any(contradiction in change_request.lower() 
                                 for contradiction in ['no security', 'negligible performance', 'unreliable'])),
            "conflicts": [],
            "suggestions": ["No change request provided, requirements are baseline"] if not change_request else ["Change request appears aligned with base requirements"]
        }
        
        result_data = {
            "constraints": constraints,
            "alignment_check": alignment_check,
            "version_info": {
                "current_version": f"version_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}",
                "tracked": True
            },
            "timestamp": datetime.now().timestamp()
        }

        success_result = {
            "success": True,
            "result": result_data,
            "input": {
                "requirements": requirements,
                "change_request": change_request
            }
        }
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(success_result, ensure_ascii=False)
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
            'body': json.dumps(error_result, ensure_ascii=False)
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
    requirements = args.get("requirements", args.get("description", args.get("input", "")))
    change_request = args.get("change_request", "")
    
    if not requirements.strip():
        return "错误: 需要提供系统需求描述以生成约束"

    # 生成约束
    req_lower = requirements.lower()
    constraints = []
    
    # 安全约束
    if any(term in req_lower for term in ['security', 'secure', 'auth', 'encrypt', 'privacy', 'protect']):
        constraints.append("安全约束: 系统必须实现标准安全措施")
    
    # 性能约束  
    if any(term in req_lower for term in ['performance', 'fast', 'response', 'throughput', 'latency']):
        constraints.append("性能约束: 系统必须满足定义的性能要求")
    
    # 数据约束
    if any(term in req_lower for term in ['data', 'database', 'storage', 'retrieve', 'persist']):
        constraints.append("数据约束: 系统必须保持数据完整性和备份能力")

    # 格式化输出
    output_lines = []
    output_lines.append("约束生成结果:")
    output_lines.append(f"需求: {requirements}")
    output_lines.append("")
    
    if constraints:
        output_lines.append("生成的约束:")
        for i, constraint in enumerate(constraints, 1):
            output_lines.append(f"  {i}. {constraint}")
    else:
        output_lines.append("未识别到特定约束类型，可能需要更具体的需求描述")
    
    if change_request:
        output_lines.append("")
        output_lines.append(f"变更请求: {change_request}")
        # 简单对齐检查
        if 'no security' in change_request.lower() and 'security' in req_lower:
            output_lines.append("⚠️  警告: 变更请求与基础需求冲突")
        else:
            output_lines.append("✅ 变更请求与基础需求对齐")
    
    return "\n".join(output_lines)