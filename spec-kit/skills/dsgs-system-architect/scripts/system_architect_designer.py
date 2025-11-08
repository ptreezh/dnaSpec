"""
DSGS System Architect Script
Implements the core functionality for system architecture design, 
technology stack selection, module division, and interface definition.
"""

import re
from typing import Dict, Any, List, Tuple
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
        self.dependencies = []

    def add_interface(self, interface_name: str, interface_type: str, 
                      input_format: str, output_format: str):
        interface = {
            "name": interface_name,
            "type": interface_type,
            "input_format": input_format,
            "output_format": output_format
        }
        self.interfaces.append(interface)

    def add_dependency(self, dependency_name: str, dependency_type: str):
        dependency = {
            "name": dependency_name,
            "type": dependency_type
        }
        self.dependencies.append(dependency)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "module_type": self.module_type.value,
            "technologies": self.technologies,
            "responsibilities": self.responsibilities,
            "interfaces": self.interfaces,
            "dependencies": self.dependencies
        }


class DSGSSystemArchitect:
    def __init__(self):
        # Architecture pattern indicators
        self.microservice_indicators = [
            'microservice', 'distributed', 'scalable', 'independent', 
            'multiple services', 'service oriented', 'modular'
        ]
        
        self.event_driven_indicators = [
            'real-time', 'asynchronous', 'event', 'message', 'notification', 
            'stream', 'reactive', 'publish', 'subscribe'
        ]
        
        self.high_availability_indicators = [
            '99.99%', 'availability', 'redundancy', 'failover', 'fault tolerance',
            'reliable', 'no downtime', 'backup'
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
        
        # Technology recommendations
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

    def identify_architecture_type(self, requirements: str) -> SystemArchitectureType:
        """Identify the appropriate architecture type based on requirements"""
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
        """Recommend appropriate technology stack based on requirements and architecture type"""
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
        """Identify system modules based on requirements"""
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
        """Define interfaces between modules"""
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

    def generate_architecture_design(self, requirements: str) -> Dict[str, Any]:
        """Generate complete system architecture design"""
        arch_type = self.identify_architecture_type(requirements)
        tech_stack = self.recommend_tech_stack(requirements, arch_type)
        modules = self.identify_modules(requirements, arch_type)
        interfaces = self.define_interfaces(modules, arch_type)
        
        # Generate architecture recommendations
        architecture_recommendations = self.generate_architecture_recommendations(requirements, arch_type)
        
        # Identify potential issues
        potential_issues = self.identify_potential_issues(requirements, arch_type)
        
        design = {
            "input_requirements": requirements[:100] + "..." if len(requirements) > 100 else requirements,
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

    def generate_architecture_recommendations(self, requirements: str, arch_type: SystemArchitectureType) -> List[str]:
        """Generate specific architecture recommendations"""
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
        """Identify potential architecture issues"""
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
        """Generate implementation guidance based on architecture type"""
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


def main():
    """Example usage of the DSGSSystemArchitect"""
    # Example requirement from test case
    requirements = "为一个博客系统设计系统架构，需要前端展示、后端管理、数据库存储"
    
    system_architect = DSGSSystemArchitect()
    design = system_architect.generate_architecture_design(requirements)
    
    print("## DSGS System Architecture Design")
    print(f"Input Requirements: {design['input_requirements']}")
    print(f"Architecture Type: {design['architecture_type']}")
    print(f"Recommended Tech Stack: {design['recommended_tech_stack']}")
    
    print("\n### Identified Modules:")
    for module in design['identified_modules']:
        print(f"- {module['name']} ({module['module_type']})")
        print(f"  Technologies: {', '.join(module['technologies'])}")
        print(f"  Responsibilities: {', '.join(module['responsibilities'])}")
    
    print("\n### Defined Interfaces:")
    for interface in design['defined_interfaces']:
        print(f"- {interface['source']} → {interface['target']}")
        print(f"  Protocol: {interface['protocol']}, Format: {interface['data_format']}")
    
    print("\n### Architecture Recommendations:")
    for rec in design['architecture_recommendations']:
        print(f"- {rec}")
    
    print("\n### Potential Issues:")
    for issue in design['potential_issues']:
        print(f"- {issue}")


if __name__ == "__main__":
    # Run tests for each test case
    test_cases = [
        "为一个博客系统设计系统架构，需要前端展示、后端管理、数据库存储",
        "为一个大型电商平台设计微服务架构，包含用户服务、产品服务、订单服务",
        "设计一个金融交易系统，要求99.99%可用性，高安全性"
    ]
    
    system_architect = DSGSSystemArchitect()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"Running Test Case {i}")
        print(f"{'='*50}")
        design = system_architect.generate_architecture_design(test_case)
        print(f"Architecture Type: {design['architecture_type']}")
        print(f"Tech Stack: {design['recommended_tech_stack']}")
        print(f"Modules Identified: {len(design['identified_modules'])}")
        print(f"Recommendations: {len(design['architecture_recommendations'])}")