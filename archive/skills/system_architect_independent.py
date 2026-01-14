"""
系统架构师技能 - 独立执行版本
支持跨CLI工具部署的独立执行函数
"""
from typing import Dict, Any, List
from enum import Enum
import json


class SystemArchitectureType(Enum):
    LAYERED = "layered"
    MICROSERVICES = "microservices"
    EVENT_DRIVEN = "event-driven"
    CLIENT_SERVER = "client-server"
    PEER_TO_PEER = "peer-to-peer"
    SERVICE_ORIENTED = "service-oriented"
    SERVERLESS = "serverless"
    PIPE_FILTER = "pipe-filter"


class TechnologyStack(Enum):
    FULL_STACK = "full-stack"
    JAMSTACK = "jamstack"
    LAMP = "lamp"
    MEAN = "mean"
    MERN = "mern"
    PYTHON_WEB = "python-web"
    JAVA_ENTERPRISE = "java-enterprise"
    CLOUD_NATIVE = "cloud-native"


class ModuleType(Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    INFRASTRUCTURE = "infrastructure"
    SECURITY = "security"
    MONITORING = "monitoring"


class SystemComponent:
    def __init__(self, name: str, module_type: ModuleType, 
                 technologies: List[str], responsibilities: List[str]):
        self.name = name
        self.module_type = module_type
        self.technologies = technologies
        self.responsibilities = responsibilities
        self.interfaces = []

    def add_interface(self, name: str, interface_type: str, 
                     input_format: str, output_format: str):
        interface = {
            "name": name,
            "type": interface_type,
            "input_format": input_format,
            "output_format": output_format
        }
        self.interfaces.append(interface)

    def to_dict(self):
        return {
            "name": self.name,
            "module_type": self.module_type.value,
            "technologies": self.technologies,
            "responsibilities": self.responsibilities,
            "interfaces": self.interfaces
        }


def execute_system_architect(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    独立执行的系统架构师技能函数
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
        result_data = _execute_architecture_design(input_text, options, context)
        
        # 根据详细程度格式化输出
        formatted_result = _format_output(result_data, detail_level)
        
        return {
            "status": "success",
            "data": formatted_result,
            "metadata": {
                "skill_name": "system-architect",
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


def _execute_architecture_design(input_text: str, options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """执行系统架构设计逻辑"""
    # 架构指示器
    microservice_indicators = [
        'microservice', '服务拆分', '独立部署', '服务治理', '分布式',
        'service mesh', 'kubernetes', 'docker', '容器化'
    ]
    
    event_driven_indicators = [
        'event', '事件驱动', '消息队列', '异步处理', '实时处理',
        'kafka', 'rabbitmq', 'pub/sub', '发布订阅'
    ]
    
    high_availability_indicators = [
        'high availability', '高可用', '容错', '故障转移', '冗余',
        '99.9%', '负载均衡', '灾备', 'failover'
    ]
    
    cloud_native_indicators = [
        'cloud native', 'container', 'kubernetes', 'saas', 'multi-tenant',
        'elastic', 'scalable'
    ]
    
    data_indicators = [
        'big data', 'analytics', 'pb', 'processing', 'data lake', 
        'data warehouse', 'hadoop', 'spark'
    ]
    
    mobile_indicators = [
        'mobile', 'app', 'offline', 'push', 'native', 'hybrid'
    ]
    
    # 技术推荐
    tech_stacks = {
        TechnologyStack.FULL_STACK: {
            "frontend": ["React", "Vue.js", "Angular"],
            "backend": ["Node.js", "Django", "Spring Boot"],
            "database": ["PostgreSQL", "MongoDB", "Redis"],
            "infrastructure": ["AWS", "Docker", "Kubernetes"]
        },
        TechnologyStack.JAMSTACK: {
            "frontend": ["Next.js", "Gatsby", "Nuxt.js"],
            "backend": ["Serverless Functions", "API Gateway"],
            "database": ["Firebase", "GraphQL", "CDN"],
            "infrastructure": ["Netlify", "Vercel", "Cloudflare"]
        },
        TechnologyStack.MERN: {
            "frontend": ["React"],
            "backend": ["Node.js", "Express.js"],
            "database": ["MongoDB"],
            "infrastructure": ["Docker", "Kubernetes", "AWS"]
        },
        TechnologyStack.JAVA_ENTERPRISE: {
            "frontend": ["Angular", "React", "Vue.js"],
            "backend": ["Spring Boot", "Spring Cloud", "Java EE"],
            "database": ["PostgreSQL", "Oracle", "Redis"],
            "infrastructure": ["Docker", "Kubernetes", "Jenkins"]
        },
        TechnologyStack.CLOUD_NATIVE: {
            "frontend": ["React", "Vue.js"],
            "backend": ["Node.js", "Go", "Python"],
            "database": ["DynamoDB", "Firestore", "Redis"],
            "infrastructure": ["Kubernetes", "Lambda", "Istio"]
        }
    }
    
    def identify_architecture_type(requirements: str) -> SystemArchitectureType:
        """根据需求识别合适的架构类型"""
        req_lower = requirements.lower()
        
        if any(indicator in req_lower for indicator in microservice_indicators):
            return SystemArchitectureType.MICROSERVICES
        elif any(indicator in req_lower for indicator in event_driven_indicators):
            return SystemArchitectureType.EVENT_DRIVEN
        elif any(indicator in req_lower for indicator in high_availability_indicators):
            return SystemArchitectureType.CLIENT_SERVER
        elif any(indicator in req_lower for indicator in cloud_native_indicators):
            return SystemArchitectureType.SERVERLESS
        else:
            return SystemArchitectureType.LAYERED
    
    def recommend_tech_stack(requirements: str, arch_type: SystemArchitectureType) -> TechnologyStack:
        """根据需求和架构类型推荐合适的技术栈"""
        req_lower = requirements.lower()
        
        if any(indicator in req_lower for indicator in data_indicators):
            return TechnologyStack.PYTHON_WEB
        elif any(indicator in req_lower for indicator in mobile_indicators):
            return TechnologyStack.JAMSTACK
        elif any(indicator in req_lower for indicator in cloud_native_indicators):
            return TechnologyStack.CLOUD_NATIVE
        elif 'java' in req_lower or 'enterprise' in req_lower:
            return TechnologyStack.JAVA_ENTERPRISE
        elif 'react' in req_lower or 'javascript' in req_lower:
            return TechnologyStack.MERN
        else:
            return TechnologyStack.FULL_STACK
    
    def identify_modules(requirements: str, arch_type: SystemArchitectureType) -> List[SystemComponent]:
        """根据需求识别系统模块"""
        modules = []
        
        # Identify core modules based on requirements
        req_lower = requirements.lower()
        
        # Frontend module
        frontend_tech = tech_stacks[recommend_tech_stack(requirements, arch_type)].get("frontend", ["React"])[0]
        frontend_responsibilities = ["User interface", "User interaction", "Data presentation"]
        
        if any(indicator in req_lower for indicator in mobile_indicators):
            frontend_responsibilities.append("Mobile compatibility")
            frontend_responsibilities.append("Offline support")
        
        frontend_module = SystemComponent(
            name="Frontend Module",
            module_type=ModuleType.FRONTEND,
            technologies=[frontend_tech],
            responsibilities=frontend_responsibilities
        )
        
        # Backend module
        backend_tech = tech_stacks[recommend_tech_stack(requirements, arch_type)].get("backend", ["Node.js"])[0]
        backend_responsibilities = ["Business logic", "Data processing", "API management"]
        
        backend_module = SystemComponent(
            name="Backend Module",
            module_type=ModuleType.BACKEND,
            technologies=[backend_tech],
            responsibilities=backend_responsibilities
        )
        
        # Database module
        db_tech = tech_stacks[recommend_tech_stack(requirements, arch_type)].get("database", ["PostgreSQL"])[0]
        db_responsibilities = ["Data storage", "Data retrieval", "Data consistency"]
        
        database_module = SystemComponent(
            name="Database Module",
            module_type=ModuleType.DATABASE,
            technologies=[db_tech],
            responsibilities=db_responsibilities
        )
        
        modules.extend([frontend_module, backend_module, database_module])
        
        # Add additional modules based on requirements
        if any(indicator in req_lower for indicator in high_availability_indicators):
            infra_module = SystemComponent(
                name="Infrastructure Module",
                module_type=ModuleType.INFRASTRUCTURE,
                technologies=["Kubernetes", "Docker"],
                responsibilities=["Deployment", "Scaling", "Load balancing"]
            )
            modules.append(infra_module)
        
        if 'security' in req_lower or 'auth' in req_lower:
            security_module = SystemComponent(
                name="Security Module",
                module_type=ModuleType.SECURITY,
                technologies=["OAuth2", "JWT", "TLS"],
                responsibilities=["Authentication", "Authorization", "Data encryption"]
            )
            modules.append(security_module)
        
        return modules
    
    def define_interfaces(modules: List[SystemComponent], arch_type: SystemArchitectureType) -> List[Dict[str, Any]]:
        """定义模块间接口"""
        interfaces = []
        
        # Define REST API interfaces
        rest_api = {
            "name": "REST API",
            "type": "REST",
            "description": "Main API for frontend-backend communication",
            "endpoints": [
                {"method": "GET", "path": "/api/data", "description": "Retrieve data"},
                {"method": "POST", "path": "/api/data", "description": "Create new data"}
            ]
        }
        interfaces.append(rest_api)
        
        # Define database interfaces
        db_interface = {
            "name": "Database Interface",
            "type": "SQL/NoSQL",
            "description": "Interface for database operations",
            "operations": ["SELECT", "INSERT", "UPDATE", "DELETE"]
        }
        interfaces.append(db_interface)
        
        return interfaces
    
    def generate_architecture_recommendations(requirements: str, arch_type: SystemArchitectureType) -> List[str]:
        """生成架构建议"""
        recommendations = [
            f"采用 {arch_type.value} 架构模式",
            "实施微服务治理策略",
            "建立自动化CI/CD流水线",
            "配置监控和日志系统"
        ]
        
        if arch_type == SystemArchitectureType.MICROSERVICES:
            recommendations.append("使用服务网格进行服务间通信管理")
            recommendations.append("实施分布式追踪系统")
        
        return recommendations
    
    def identify_potential_issues(requirements: str, arch_type: SystemArchitectureType) -> List[str]:
        """识别潜在问题"""
        issues = [
            "需要考虑数据一致性问题",
            "系统复杂性可能增加运维成本",
            "需要制定详细的测试策略"
        ]
        
        if arch_type == SystemArchitectureType.MICROSERVICES:
            issues.append("服务间通信延迟可能影响性能")
            issues.append("需要实现服务发现和负载均衡")
        
        return issues
    
    def generate_implementation_guidance(arch_type: SystemArchitectureType) -> List[str]:
        """生成实施指导"""
        guidance = [
            "1. 进行详细的需求分析和技术选型",
            "2. 设计系统架构图和数据流图",
            "3. 制定开发规范和代码审查流程",
            "4. 建立持续集成和持续部署环境"
        ]
        
        if arch_type == SystemArchitectureType.MICROSERVICES:
            guidance.append("5. 实施服务注册与发现机制")
            guidance.append("6. 配置API网关和负载均衡器")
        
        return guidance
    
    # 执行架构设计逻辑
    arch_type = identify_architecture_type(input_text)
    tech_stack = recommend_tech_stack(input_text, arch_type)
    modules = identify_modules(input_text, arch_type)
    interfaces = define_interfaces(modules, arch_type)
    architecture_recommendations = generate_architecture_recommendations(input_text, arch_type)
    potential_issues = identify_potential_issues(input_text, arch_type)
    
    design = {
        "input_requirements": input_text[:100] + "..." if len(input_text) > 100 else input_text,
        "architecture_type": arch_type.value,
        "recommended_tech_stack": tech_stack.value,
        "identified_modules": [module.to_dict() for module in modules],
        "defined_interfaces": interfaces,
        "architecture_recommendations": architecture_recommendations,
        "potential_issues": potential_issues,
        "implementation_guidance": generate_implementation_guidance(arch_type),
        "module_division_rationale": f"Using {arch_type.value} architecture based on system requirements"
    }
    
    return design


def _format_output(result_data: Dict[str, Any], detail_level: str) -> Dict[str, Any]:
    """根据详细程度格式化输出结果"""
    if detail_level == "basic":
        # 基础级别只返回核心信息
        return {
            "architecture_type": result_data["architecture_type"],
            "recommended_tech_stack": result_data["recommended_tech_stack"],
            "main_modules_count": len(result_data["identified_modules"]),
            "main_recommendations": result_data["architecture_recommendations"][:3]
        }
    elif detail_level == "standard":
        # 标准级别返回标准信息
        return {
            "architecture_type": result_data["architecture_type"],
            "recommended_tech_stack": result_data["recommended_tech_stack"],
            "identified_modules": result_data["identified_modules"],
            "defined_interfaces": result_data["defined_interfaces"][:5],  # 只返回前5个接口
            "architecture_recommendations": result_data["architecture_recommendations"][:5],
            "potential_issues": result_data["potential_issues"][:3]
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
        print("Usage: python system_architect_independent.py '<requirements>' [detail_level]")
        sys.exit(1)
    
    requirements = sys.argv[1]
    detail_level = sys.argv[2] if len(sys.argv) > 2 else "standard"
    
    args = {
        "input": requirements,
        "detail_level": detail_level,
        "options": {},
        "context": {}
    }
    
    result = execute_system_architect(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()