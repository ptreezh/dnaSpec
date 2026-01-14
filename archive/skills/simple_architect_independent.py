"""
简易架构师技能 - 独立执行版本
支持跨CLI工具部署的独立执行函数
"""
from typing import Dict, Any
import json


def execute_simple_architect(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    独立执行的简易架构师技能函数
    支持跨CLI工具调用
    
    Args:
        args: 包含以下字段的字典
            - input: 系统需求描述
            - detail_level: 详细程度 ("basic", "standard", "detailed")
            - options: 可选配置参数
            - context: 上下文信息
            
    Returns:
        标准化输出响应
    """
    try:
        # 解析输入参数
        input_text = args.get("input", "")
        detail_level_str = args.get("detail_level", "standard")
        options = args.get("options", {})
        context = args.get("context", {})
        
        # 验证输入
        if not input_text or not isinstance(input_text, str):
            return {
                "status": "error",
                "error": {
                    "type": "VALIDATION_ERROR",
                    "message": "Input must be a non-empty string",
                    "code": "INVALID_INPUT"
                }
            }
        
        # 处理详细程度参数
        detail_level = "standard"
        if detail_level_str in ["basic", "standard", "detailed"]:
            detail_level = detail_level_str
        
        # 执行架构设计逻辑
        result_data = _execute_simple_architecture_design(input_text, options, context)
        
        # 根据详细程度格式化输出
        formatted_result = _format_output(result_data, detail_level)
        
        return {
            "status": "success",
            "data": formatted_result,
            "metadata": {
                "skill_name": "simple-architect",
                "detail_level": detail_level
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": {
                "type": type(e).__name__,
                "message": str(e),
                "code": "EXECUTION_ERROR"
            }
        }


def _execute_simple_architecture_design(input_text: str, options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """执行简易架构设计逻辑"""
    
    # 简单的关键字匹配来确定架构类型
    input_lower = input_text.lower()
    
    if 'web' in input_lower or '网站' in input_text:
        architecture = "Web Application"
        tech_stack = ["HTML/CSS/JavaScript", "React/Vue/Angular", "Node.js/Python/Django", "MySQL/PostgreSQL/MongoDB"]
        deployment = "Traditional Web Server"
    elif 'mobile' in input_lower or 'app' in input_lower or '应用' in input_text:
        architecture = "Mobile Application"
        tech_stack = ["React Native/Flutter", "iOS/Android SDK", "Firebase/API", "SQLite/Realm"]
        deployment = "App Store Distribution"
    elif 'api' in input_lower or '服务' in input_text:
        architecture = "API Service"
        tech_stack = ["Node.js/Python/Go", "Express/FastAPI/Gin", "PostgreSQL/Redis", "Docker/Kubernetes"]
        deployment = "Cloud Deployment"
    elif 'data' in input_lower or '分析' in input_text:
        architecture = "Data Processing Pipeline"
        tech_stack = ["Python/R", "Pandas/NumPy", "Apache Spark", "AWS S3/HDFS"]
        deployment = "Big Data Platform"
    else:
        architecture = "General Purpose Application"
        tech_stack = ["Python/Java/C#", "Flask/Spring Boot", "PostgreSQL/MongoDB", "Docker"]
        deployment = "Standard Server Deployment"
    
    # 生成简单的架构建议
    recommendations = [
        f"Recommended Architecture: {architecture}",
        f"Suggested Tech Stack: {', '.join(tech_stack[:3])}",
        f"Deployment Strategy: {deployment}"
    ]
    
    # 识别潜在问题
    potential_issues = []
    if '高并发' in input_text or 'high concurrency' in input_lower:
        potential_issues.append("Need to consider load balancing and horizontal scaling")
    if '安全' in input_text or 'security' in input_lower:
        potential_issues.append("Need to implement proper authentication and authorization")
    if '实时' in input_text or 'real-time' in input_lower:
        potential_issues.append("Consider using WebSocket or message queues for real-time communication")
    
    return {
        "input_summary": input_text[:50] + "..." if len(input_text) > 50 else input_text,
        "recommended_architecture": architecture,
        "technology_stack": tech_stack,
        "deployment_strategy": deployment,
        "key_recommendations": recommendations,
        "potential_issues": potential_issues
    }


def _format_output(result_data: Dict[str, Any], detail_level: str) -> Dict[str, Any]:
    """根据详细程度格式化输出结果"""
    if detail_level == "basic":
        # 基础级别只返回核心信息
        return {
            "recommended_architecture": result_data["recommended_architecture"],
            "main_technology": result_data["technology_stack"][0] if result_data["technology_stack"] else "N/A"
        }
    elif detail_level == "standard":
        # 标准级别返回标准信息
        return {
            "recommended_architecture": result_data["recommended_architecture"],
            "technology_stack": result_data["technology_stack"][:3],  # 只返回前3个技术
            "deployment_strategy": result_data["deployment_strategy"],
            "key_recommendations": result_data["key_recommendations"][:3],  # 只返回前3个建议
            "potential_issues_count": len(result_data["potential_issues"])
        }
    else:  # detailed
        # 详细级别返回完整信息
        return result_data


# 为CLI工具提供命令行接口
def main():
    """命令行接口"""
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python simple_architect_independent.py '<requirements>' [detail_level]")
        sys.exit(1)
    
    requirements = sys.argv[1]
    detail_level = sys.argv[2] if len(sys.argv) > 2 else "standard"
    
    args = {
        "input": requirements,
        "detail_level": detail_level,
        "options": {},
        "context": {}
    }
    
    result = execute_simple_architect(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()