"""
系统架构师技能 - 重构版本
符合DNASPEC标准化技能接口规范
"""
import re
from typing import Dict, Any, List
from enum import Enum
from src.dna_spec_kit_integration.core.skill_base import BaseSkill, DetailLevel


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


class SystemArchitectSkill(BaseSkill):
    """系统架构师技能 - 用于系统架构设计、技术栈选择、模块划分和接口定义"""
    
    def __init__(self):
        super().__init__(
            name="system-architect",
            description="用于复杂项目的系统架构设计、技术栈选择、模块划分和接口定义"
        )
        
        # 架构指示器
        self.microservice_indicators = [
            'microservice', '服务拆分', '独立部署', '服务治理', '分布式',
            'service mesh', 'kubernetes', 'docker', '容器化'
        ]
        
        self.event_driven_indicators = [
            'event', '事件驱动', '消息队列', '异步处理', '实时处理',
            'kafka', 'rabbitmq', 'pub/sub', '发布订阅'
        ]
        
        self.high_availability_indicators = [
            'high availability', '高可用', '容错', '故障转移', '冗余',
            '99.9%', '负载均衡', '灾备', 'failover'
        ]
        
        self.performance_indicators = [
            'low latency', 'high throughput', 'performance', 'fast', 'optimized',
            'real-time', 'millisecond', 'speed'
        ]
        
        self.data_indicators = [
            'big data', 'analytics', 'pb', 'processing', 'data lake', 
            'data warehouse', 'hadoop', 'spark'
        ]
        
        self.mobile_indicators = [
            'mobile', 'app', 'offline', 'push', 'native', 'hybrid'
        ]
        
        self.cloud_native_indicators = [
            'cloud native', 'container', 'kubernetes', 'saas', 'multi-tenant',
            'elastic', 'scalable'
        ]
        
        # 技术推荐
        self.tech_stacks = {
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

    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """执行系统架构师技能逻辑"""
        arch_type = self.identify_architecture_type(input_text)
        tech_stack = self.recommend_tech_stack(input_text, arch_type)
        modules = self.identify_modules(input_text, arch_type)
        interfaces = self.define_interfaces(modules, arch_type)
        
        # 生成架构建议
        architecture_recommendations = self.generate_architecture_recommendations(input_text, arch_type)
        
        # 识别潜在问题
        potential_issues = self.identify_potential_issues(input_text, arch_type)
        
        design = {
            "input_requirements": input_text[:100] + "..." if len(input_text) > 100 else input_text,
            "architecture_type": arch_type.value,
            "recommended_tech_stack": tech_stack.value,
            "identified_modules": [module.to_dict() for module in modules],
            "defined_interfaces": interfaces,
            "architecture_recommendations": architecture_recommendations,
            "potential_issues": potential_issues,
            "implementation_guidance": self.generate_implementation_guidance(arch_type),
            "module_division_rationale": f"Using {arch_type.value} architecture based on system requirements"
        }
        
        return design

    def _format_output(self, result_data: Dict[str, Any], detail_level: DetailLevel) -> Dict[str, Any]:
        """根据详细程度格式化输出结果"""
        if detail_level == DetailLevel.BASIC:
            # 基础级别只返回核心信息
            return {
                "architecture_type": result_data["architecture_type"],
                "recommended_tech_stack": result_data["recommended_tech_stack"],
                "main_modules_count": len(result_data["identified_modules"]),
                "main_recommendations": result_data["architecture_recommendations"][:3]
            }
        elif detail_level == DetailLevel.STANDARD:
            # 标准级别返回标准信息
            return {
                "architecture_type": result_data["architecture_type"],
                "recommended_tech_stack": result_data["recommended_tech_stack"],
                "identified_modules": result_data["identified_modules"],
                "defined_interfaces": result_data["defined_interfaces"][:5],  # 只返回前5个接口
                "architecture_recommendations": result_data["architecture_recommendations"][:5],
                "potential_issues": result_data["potential_issues"][:3]
            }
        else:  # DETAILED
            # 详细级别返回完整信息
            return result_data

    def identify_architecture_type(self, requirements: str) -> SystemArchitectureType:
        """根据需求识别合适的架构类型"""
        req_lower = requirements.lower()
        
        if any(indicator in req_lower for indicator in self.microservice_indicators):
            return SystemArchitectureType.MICROSERVICES
        elif any(indicator in req_lower for indicator in self.event_driven_indicators):
            return SystemArchitectureType.EVENT_DRIVEN
        elif any(indicator in req_lower for indicator in self.high_availability_indicators):
            return SystemArchitectureType.CLIENT_SERVER
        elif any(indicator in req_lower for indicator in self.cloud_native_indicators):
            return SystemArchitectureType.SERVERLESS
        else:
            return SystemArchitectureType.LAYERED

    def recommend_tech_stack(self, requirements: str, arch_type: SystemArchitectureType) -> TechnologyStack:
        """根据需求和架构类型推荐合适的技术栈"""
        req_lower = requirements.lower()
        
        if any(indicator in req_lower for indicator in self.data_indicators):
            return TechnologyStack.PYTHON_WEB
        elif any(indicator in req_lower for indicator in self.mobile_indicators):
            return TechnologyStack.JAMSTACK
        elif any(indicator in req_lower for indicator in self.cloud_native_indicators):
            return TechnologyStack.CLOUD_NATIVE
        elif 'java' in req_lower or 'enterprise' in req_lower:
            return TechnologyStack.JAVA_ENTERPRISE
        elif 'react' in req_lower or 'javascript' in req_lower:
            return TechnologyStack.MERN
        else:
            return TechnologyStack.FULL_STACK

    def identify_modules(self, requirements: str, arch_type: SystemArchitectureType) -> List[SystemComponent]:
        """根据需求识别系统模块"""
        modules = []
        
        # Identify core modules based on requirements
        req_lower = requirements.lower()
        
        # Frontend module
        frontend_tech = self.tech_stacks[self.recommend_tech_stack(requirements, arch_type)].get("frontend", ["React"])[0]
        frontend_responsibilities = ["User interface", "User interaction", "Data presentation"]
        
        if any(indicator in req_lower for indicator in self.mobile_indicators):
            frontend_responsibilities.append("Mobile compatibility")
            frontend_responsibilities.append("Offline support")
        
        frontend_module = SystemComponent(
            name="Frontend Module",
            module_type=ModuleType.FRONTEND,
            technologies=[frontend_tech],
            responsibilities=frontend_responsibilities
        )
        
        # Add interfaces for frontend
        frontend_module.add_interface(
            name="API Interface",
            interface_type="REST API",
            input_format="JSON",
            output_format="JSON"
        )
        
        modules.append(frontend_module)
        
        # Backend module
        backend_tech = self.tech_stacks[self.recommend_tech_stack(requirements, arch_type)].get("backend", ["Node.js"])[0]
        backend_responsibilities = ["Business logic", "API endpoints", "Data processing"]
        
        if arch_type == SystemArchitectureType.MICROSERVICES:
            backend_responsibilities = ["Service orchestration", "API gateway", "Service communication"]
        
        backend_module = SystemComponent(
            name="Backend Module",
            module_type=ModuleType.BACKEND,
            technologies=[backend_tech],
            responsibilities=backend_responsibilities
        )
        
        # Add interfaces for backend
        backend_module.add_interface(
            name="Database Interface",
            interface_type="SQL/NoSQL",
            input_format="Query/Command",
            output_format="Data/Result"
        )
        
        if arch_type == SystemArchitectureType.EVENT_DRIVEN:
            backend_module.add_interface(
                name="Message Interface",
                interface_type="Message Queue",
                input_format="Message",
                output_format="Acknowledgment"
            )
        
        modules.append(backend_module)
        
        # Database module
        db_tech = self.tech_stacks[self.recommend_tech_stack(requirements, arch_type)].get("database", ["PostgreSQL"])[0]
        
        if any(indicator in req_lower for indicator in self.data_indicators):
            db_tech = "Apache Kafka, Hadoop, Spark"  # For big data
        
        db_responsibilities = ["Data storage", "Data retrieval", "Data consistency"]
        
        if arch_type == SystemArchitectureType.MICROSERVICES:
            db_responsibilities = ["Per-service data storage", "Data synchronization", "Distributed data management"]
        
        db_module = SystemComponent(
            name="Database Module",
            module_type=ModuleType.DATABASE,
            technologies=[db_tech],
            responsibilities=db_responsibilities
        )
        
        modules.append(db_module)
        
        # Add infrastructure module if needed
        if arch_type in [SystemArchitectureType.MICROSERVICES, SystemArchitectureType.SERVERLESS]:
            infra_tech = self.tech_stacks[self.recommend_tech_stack(requirements, arch_type)].get("infrastructure", ["AWS"])[0]
            
            infra_responsibilities = ["Deployment", "Scaling", "Monitoring"]
            if arch_type == SystemArchitectureType.MICROSERVICES:
                infra_responsibilities.append("Service discovery")
                infra_responsibilities.append("Load balancing")
            
            infra_module = SystemComponent(
                name="Infrastructure Module",
                module_type=ModuleType.INFRASTRUCTURE,
                technologies=[infra_tech],
                responsibilities=infra_responsibilities
            )
            
            modules.append(infra_module)
        
        return modules

    def define_interfaces(self, modules: List[SystemComponent], arch_type: SystemArchitectureType) -> List[Dict[str, Any]]:
        """定义模块间接口"""
        interfaces = []
        
        # Define standard interfaces based on architecture type
        if arch_type == SystemArchitectureType.MICROSERVICES:
            for i, module in enumerate(modules):
                if module.module_type == ModuleType.BACKEND:
                    # Add service-to-service communication
                    for j, other_module in enumerate(modules):
                        if i != j and other_module.module_type == ModuleType.BACKEND:
                            interface = {
                                "source": module.name,
                                "target": other_module.name,
                                "protocol": "REST API / gRPC",
                                "data_format": "JSON / Protocol Buffers",
                                "description": "Inter-service communication"
                            }
                            interfaces.append(interface)
        else:
            # Standard layered architecture interfaces
            for module in modules:
                if module.name == "Frontend Module":
                    interface = {
                        "source": module.name,
                        "target": "Backend Module",
                        "protocol": "HTTP/HTTPS",
                        "data_format": "JSON",
                        "description": "Client-server communication"
                    }
                    interfaces.append(interface)
                elif module.name == "Backend Module":
                    interface = {
                        "source": module.name,
                        "target": "Database Module",
                        "protocol": "Database Protocol",
                        "data_format": "Query Result",
                        "description": "Data access layer"
                    }
                    interfaces.append(interface)
        
        return interfaces

    def generate_architecture_recommendations(self, requirements: str, arch_type: SystemArchitectureType) -> List[str]:
        """生成具体的架构建议"""
        recommendations = []
        
        if arch_type == SystemArchitectureType.MICROSERVICES:
            recommendations.extend([
                "Implement API gateway for service routing",
                "Use circuit breaker pattern for fault tolerance",
                "Implement distributed logging and monitoring",
                "Consider data consistency challenges in distributed system"
            ])
        elif arch_type == SystemArchitectureType.EVENT_DRIVEN:
            recommendations.extend([
                "Implement event sourcing pattern",
                "Use message brokers for decoupling",
                "Design idempotent event processors",
                "Implement retry and dead-letter queue mechanisms"
            ])
        elif arch_type == SystemArchitectureType.SERVERLESS:
            recommendations.extend([
                "Optimize function cold start times",
                "Implement proper state management",
                "Use managed services where possible",
                "Consider vendor lock-in implications"
            ])
        else:  # LAYERED architecture
            recommendations.extend([
                "Maintain clear separation of concerns",
                "Implement proper error handling layers",
                "Use dependency injection for loose coupling",
                "Consider caching strategies for performance"
            ])
        
        req_lower = requirements.lower()
        if any(indicator in req_lower for indicator in self.high_availability_indicators):
            recommendations.extend([
                "Implement redundancy for critical components",
                "Design for graceful degradation",
                "Plan for disaster recovery",
                "Implement health checks and monitoring"
            ])
        
        if any(indicator in req_lower for indicator in self.performance_indicators):
            recommendations.extend([
                "Optimize database queries and indexing",
                "Implement caching at multiple levels",
                "Use CDNs for static content delivery",
                "Monitor and optimize response times"
            ])
        
        return recommendations

    def identify_potential_issues(self, requirements: str, arch_type: SystemArchitectureType) -> List[str]:
        """识别潜在的架构问题"""
        issues = []
        
        if arch_type == SystemArchitectureType.MICROSERVICES:
            issues.extend([
                "Increased complexity in development and deployment",
                "Network latency between services",
                "Distributed data consistency challenges",
                "Debugging and monitoring complexity"
            ])
        elif arch_type == SystemArchitectureType.EVENT_DRIVEN:
            issues.extend([
                "Event ordering and sequencing challenges",
                "Complexity in maintaining event consistency",
                "Difficulty in debugging event flows",
                "Potential for event loops"
            ])
        elif arch_type == SystemArchitectureType.SERVERLESS:
            issues.extend([
                "Cold start latency issues",
                "Limited execution time constraints",
                "Vendor dependency concerns",
                "Debugging and testing challenges"
            ])
        
        return issues

    def generate_implementation_guidance(self, arch_type: SystemArchitectureType) -> List[str]:
        """生成实施指导"""
        guidance = []
        
        if arch_type == SystemArchitectureType.MICROSERVICES:
            guidance.extend([
                "Start with a monolith and gradually decompose",
                "Design services around business capabilities",
                "Use contract testing between services",
                "Implement centralized logging and monitoring"
            ])
        elif arch_type == SystemArchitectureType.EVENT_DRIVEN:
            guidance.extend([
                "Design events with schema evolution in mind",
                "Use event versioning for backward compatibility",
                "Implement event validation and sanitization",
                "Plan for event replay capabilities"
            ])
        else:
            guidance.extend([
                "Follow established architecture patterns",
                "Implement proper testing at each layer",
                "Use continuous integration and deployment",
                "Document interfaces and dependencies clearly"
            ])
        
        return guidance