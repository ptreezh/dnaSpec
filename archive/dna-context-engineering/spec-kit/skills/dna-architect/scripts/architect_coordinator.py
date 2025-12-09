"""
DNASPEC Architect Script
Implements the core functionality for complex project architecture design, 
technology stack selection, task decomposition coordination, and constraint generation.
"""

import re
from typing import Dict, Any, List, Tuple
from enum import Enum
import json


class ArchitecturePattern(Enum):
    MICROSERVICES = "microservices"
    MONOLITHIC = "monolithic"
    EVENT_DRIVEN = "event-driven"
    LAYERED = "layered"
    CLIENT_SERVER = "client-server"
    PIPE_FILTER = "pipe-filter"


class TechnologyCategory(Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    INFRASTRUCTURE = "infrastructure"
    SECURITY = "security"
    MONITORING = "monitoring"


class ArchitectRecommendation:
    def __init__(self, component: str, technology: str, 
                 pattern: ArchitecturePattern, category: TechnologyCategory,
                 rationale: str = ""):
        self.component = component
        self.technology = technology
        self.pattern = pattern
        self.category = category
        self.rationale = rationale

    def to_dict(self) -> Dict[str, Any]:
        return {
            "component": self.component,
            "technology": self.technology,
            "pattern": self.pattern.value,
            "category": self.category.value,
            "rationale": self.rationale
        }


class DNASPECArchitect:
    def __init__(self):
        # Define patterns and technologies for different requirements
        self.scalability_indicators = [
            'million', 'thousand', 'concurrent', 'high traffic', 
            'scalable', 'scale', 'performance', 'load'
        ]
        
        self.security_indicators = [
            'secure', 'security', 'private', 'sensitive', 'financial', 
            'health', 'medical', 'authentication', 'authorization', 'compliance'
        ]
        
        self.realtime_indicators = [
            'real-time', 'realtime', 'immediate', 'instant', 'live', 
            'stream', 'push', 'message', 'notification'
        ]
        
        self.data_indicators = [
            'data processing', 'analysis', 'analytic', 'big data', 
            'processing', 'pipeline', 'visualization', 'storage'
        ]
        
        # Technology recommendations
        self.tech_recommendations = {
            TechnologyCategory.FRONTEND: {
                "standard": ["React", "Vue.js", "Angular"],
                "mobile": ["React Native", "Flutter", "Ionic"],
                "performance": ["Svelte", "Preact", "Alpine.js"]
            },
            TechnologyCategory.BACKEND: {
                "general": ["Node.js", "Python (Django/Flask)", "Java (Spring)", "Go"],
                "high_performance": ["Rust", "Go", "C++", "Java"],
                "microservices": ["Node.js", "Go", "Java", "Python"]
            },
            TechnologyCategory.DATABASE: {
                "relational": ["PostgreSQL", "MySQL", "Oracle"],
                "nosql": ["MongoDB", "Cassandra", "Couchbase"],
                "cache": ["Redis", "Memcached"],
                "search": ["Elasticsearch", "Solr"]
            },
            TechnologyCategory.INFRASTRUCTURE: {
                "cloud": ["AWS", "Azure", "GCP"],
                "container": ["Docker", "Kubernetes"],
                "messaging": ["Kafka", "RabbitMQ", "AWS SQS"]
            },
            TechnologyCategory.SECURITY: {
                "auth": ["OAuth 2.0", "JWT", "OpenID Connect"],
                "encryption": ["AES", "RSA", "TLS 1.3"],
                "monitoring": ["OWASP", "SAST", "DAST"]
            }
        }
        
        # Architecture patterns for different scenarios
        self.pattern_recommendations = {
            ArchitecturePattern.MICROSERVICES: {
                "use_cases": ["scalability", "independence", "multiple teams"],
                "rationale": "Enables independent development and scaling of components"
            },
            ArchitecturePattern.EVENT_DRIVEN: {
                "use_cases": ["real-time", "asynchronous", "loose coupling"],
                "rationale": "Enables real-time processing and loose coupling"
            },
            ArchitecturePattern.LAYERED: {
                "use_cases": ["enterprise", "complex business logic", "standardization"],
                "rationale": "Provides clear separation of concerns"
            }
        }

    def identify_requirements(self, requirements: str) -> Dict[str, bool]:
        """Identify key requirements patterns from the input"""
        req_lower = requirements.lower()
        
        identified = {
            'scalability': any(indicator in req_lower for indicator in self.scalability_indicators),
            'security': any(indicator in req_lower for indicator in self.security_indicators),
            'realtime': any(indicator in req_lower for indicator in self.realtime_indicators),
            'data_processing': any(indicator in req_lower for indicator in self.data_indicators)
        }
        
        return identified

    def recommend_architecture_pattern(self, requirements: str) -> ArchitecturePattern:
        """Recommend architecture pattern based on requirements"""
        req_lower = requirements.lower()
        
        # Check for specific indicators
        if any(indicator in req_lower for indicator in self.scalability_indicators):
            return ArchitecturePattern.MICROSERVICES
        
        if any(indicator in req_lower for indicator in self.realtime_indicators):
            return ArchitecturePattern.EVENT_DRIVEN
        
        if 'monolith' in req_lower or 'single' in req_lower:
            return ArchitecturePattern.MONOLITHIC
        
        # Default to layered for general enterprise applications
        return ArchitecturePattern.LAYERED

    def recommend_technologies(self, requirements: str, req_features: Dict[str, bool]) -> List[ArchitectRecommendation]:
        """Recommend technologies based on requirements"""
        recommendations = []
        
        # Frontend recommendations
        frontend_tech = self.tech_recommendations[TechnologyCategory.FRONTEND]["standard"][0]
        if any(word in requirements.lower() for word in ['mobile', 'app']):
            frontend_tech = self.tech_recommendations[TechnologyCategory.FRONTEND]["mobile"][0]
        
        recommendations.append(ArchitectRecommendation(
            component="Frontend",
            technology=frontend_tech,
            pattern=self.recommend_architecture_pattern(requirements),
            category=TechnologyCategory.FRONTEND,
            rationale=f"Standard frontend framework for web applications"
        ))
        
        # Backend recommendations
        if req_features['scalability']:
            backend_tech = self.tech_recommendations[TechnologyCategory.BACKEND]["microservices"][0]
        elif req_features['realtime']:
            backend_tech = self.tech_recommendations[TechnologyCategory.BACKEND]["high_performance"][1]  # Go
        else:
            backend_tech = self.tech_recommendations[TechnologyCategory.BACKEND]["general"][0]
        
        recommendations.append(ArchitectRecommendation(
            component="Backend",
            technology=backend_tech,
            pattern=self.recommend_architecture_pattern(requirements),
            category=TechnologyCategory.BACKEND,
            rationale=f"Backend technology suitable for {'scalable' if req_features['scalability'] else 'general'} applications"
        ))
        
        # Database recommendations
        if req_features['data_processing']:
            db_tech = self.tech_recommendations[TechnologyCategory.DATABASE]["nosql"][0]
        elif req_features['security']:
            db_tech = self.tech_recommendations[TechnologyCategory.DATABASE]["relational"][0]
        else:
            db_tech = self.tech_recommendations[TechnologyCategory.DATABASE]["relational"][0]
        
        recommendations.append(ArchitectRecommendation(
            component="Database",
            technology=db_tech,
            pattern=self.recommend_architecture_pattern(requirements),
            category=TechnologyCategory.DATABASE,
            rationale=f"Database solution suitable for {'analytical' if req_features['data_processing'] else 'transactional'} workloads"
        ))
        
        # Infrastructure recommendations
        if req_features['scalability']:
            infra_tech = self.tech_recommendations[TechnologyCategory.INFRASTRUCTURE]["container"][1]  # Kubernetes
        else:
            infra_tech = self.tech_recommendations[TechnologyCategory.INFRASTRUCTURE]["cloud"][0]  # AWS
        
        recommendations.append(ArchitectRecommendation(
            component="Infrastructure",
            technology=infra_tech,
            pattern=self.recommend_architecture_pattern(requirements),
            category=TechnologyCategory.INFRASTRUCTURE,
            rationale=f"Infrastructure solution suitable for {'containerized scalable' if req_features['scalability'] else 'standard'} deployments"
        ))
        
        # Security recommendations
        if req_features['security']:
            sec_tech = self.tech_recommendations[TechnologyCategory.SECURITY]["auth"][0]  # OAuth
            recommendations.append(ArchitectRecommendation(
                component="Security",
                technology=sec_tech,
                pattern=self.recommend_architecture_pattern(requirements),
                category=TechnologyCategory.SECURITY,
                rationale="Industry standard authentication protocol"
            ))
        
        return recommendations

    def identify_components(self, requirements: str) -> List[str]:
        """Identify system components from requirements"""
        components = set()
        
        # Look for common component patterns in requirements
        component_patterns = [
            r'user management|user service|authentication',
            r'product catalog|product management|inventory',
            r'order processing|order management|checkout',
            r'payment|billing|transaction',
            r'message|notification|communication',
            r'data analysis|analytics|reporting',
            r'content management|cms|editor',
            r'search|discovery|lookup'
        ]
        
        req_lower = requirements.lower()
        for pattern in component_patterns:
            if re.search(pattern, req_lower):
                # Extract the main component name
                match = re.search(pattern, req_lower)
                if match:
                    text_match = match.group(0)
                    if 'user' in text_match:
                        components.add('User Service')
                    elif 'product' in text_match or 'inventory' in text_match:
                        components.add('Product Service')
                    elif 'order' in text_match or 'checkout' in text_match:
                        components.add('Order Service')
                    elif 'payment' in text_match or 'billing' in text_match or 'transaction' in text_match:
                        components.add('Payment Service')
                    elif 'message' in text_match or 'notification' in text_match:
                        components.add('Notification Service')
                    elif 'data' in text_match or 'analytic' in text_match or 'report' in text_match:
                        components.add('Analytics Service')
                    elif 'content' in text_match or 'cms' in text_match:
                        components.add('Content Management Service')
                    elif 'search' in text_match:
                        components.add('Search Service')
        
        # If no specific components found, provide general ones
        if not components:
            general_components = [
                'Authentication Service', 
                'Main Business Logic Service',
                'Data Storage Service',
                'API Gateway'
            ]
            components.update(general_components)
        
        return list(components)

    def generate_architecture_documentation(self, requirements: str) -> Dict[str, Any]:
        """Generate comprehensive architecture documentation"""
        # Analyze requirements
        req_features = self.identify_requirements(requirements)
        pattern = self.recommend_architecture_pattern(requirements)
        technologies = self.recommend_technologies(requirements, req_features)
        components = self.identify_components(requirements)
        
        # Generate recommendations for coordination with other DNASPEC skills
        coordination_recommendations = self.generate_coordination_recommendations(requirements)
        
        documentation = {
            "input_requirements": requirements[:100] + "..." if len(requirements) > 100 else requirements,
            "identified_features": req_features,
            "recommended_pattern": pattern.value,
            "technology_recommendations": [tech.to_dict() for tech in technologies],
            "identified_components": components,
            "pattern_rationale": self.pattern_recommendations[pattern]["rationale"],
            "coordination_with": coordination_recommendations,
            "architecture_summary": f"This architecture follows {pattern.value} pattern with recommended technologies for each component",
            "implementation_considerations": self.generate_implementation_considerations(req_features)
        }
        
        return documentation

    def generate_coordination_recommendations(self, requirements: str) -> Dict[str, str]:
        """Generate recommendations for coordinating with other DNASPEC skills"""
        coordination = {}
        
        req_lower = requirements.lower()
        
        # Recommend task decomposition coordination
        coordination["dnaspec-task-decomposer"] = "Coordinate for breaking architecture components into implementation tasks"
        
        # Recommend constraint generation coordination
        if any(indicator in req_lower for indicator in self.security_indicators):
            coordination["dnaspec-constraint-generator"] = "Generate security and compliance constraints"
        elif any(indicator in req_lower for indicator in self.scalability_indicators):
            coordination["dnaspec-constraint-generator"] = "Generate performance and scalability constraints"
        else:
            coordination["dnaspec-constraint-generator"] = "Generate general system constraints"
        
        # Recommend agent creation coordination
        if any(indicator in req_lower for indicator in self.realtime_indicators):
            coordination["dnaspec-agent-creator"] = "Create monitoring and message handling agents"
        else:
            coordination["dnaspec-agent-creator"] = "Create appropriate system agents based on architecture"
        
        return coordination

    def generate_implementation_considerations(self, req_features: Dict[str, bool]) -> List[str]:
        """Generate implementation considerations based on requirements"""
        considerations = []
        
        if req_features['scalability']:
            considerations.append("Design for horizontal scaling from the start")
            considerations.append("Consider stateless service design")
            considerations.append("Plan for distributed data management")
        
        if req_features['security']:
            considerations.append("Implement security at every layer")
            considerations.append("Plan for regular security audits")
            considerations.append("Include compliance monitoring")
        
        if req_features['realtime']:
            considerations.append("Optimize for low latency communication")
            considerations.append("Consider eventual consistency models")
            considerations.append("Plan for high availability")
        
        if req_features['data_processing']:
            considerations.append("Consider data pipeline architecture")
            considerations.append("Plan for batch vs. real-time processing")
            considerations.append("Include data quality and validation")
        
        if not considerations:
            considerations.append("Follow standard software architecture principles")
            considerations.append("Plan for testing and monitoring")
            considerations.append("Document the architecture decisions")
        
        return considerations


def main():
    """Example usage of the DNASPECArchitect"""
    # Example requirement from test case
    requirements = "创建一个简单的电商系统，需要用户管理、产品管理、订单处理功能"
    
    architect = DNASPECArchitect()
    documentation = architect.generate_architecture_documentation(requirements)
    
    print("## DNASPEC Architecture Documentation")
    print(f"Input Requirements: {documentation['input_requirements']}")
    print(f"Recommended Pattern: {documentation['recommended_pattern']}")
    print(f"Pattern Rationale: {documentation['pattern_rationale']}")
    
    print("\n### Identified Components:")
    for component in documentation['identified_components']:
        print(f"- {component}")
    
    print("\n### Technology Recommendations:")
    for tech in documentation['technology_recommendations']:
        print(f"- {tech['component']}: {tech['technology']} ({tech['category']})")
        print(f"  Rationale: {tech['rationale']}")
    
    print("\n### Coordination Recommendations:")
    for skill, recommendation in documentation['coordination_with'].items():
        print(f"- {skill}: {recommendation}")
    
    print("\n### Implementation Considerations:")
    for consideration in documentation['implementation_considerations']:
        print(f"- {consideration}")


if __name__ == "__main__":
    # Run tests for each test case
    test_cases = [
        "创建一个简单的电商系统，需要用户管理、产品管理、订单处理功能",
        "设计一个高并发的社交媒体平台，需要支持千万级用户，实时消息推送，内容推荐算法",
        "为一个金融交易系统设计架构，需要高安全性、高可用性、低延迟"
    ]
    
    architect = DNASPECArchitect()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"Running Test Case {i}")
        print(f"{'='*50}")
        documentation = architect.generate_architecture_documentation(test_case)
        print(f"Recommended Pattern: {documentation['recommended_pattern']}")
        print(f"Components Identified: {len(documentation['identified_components'])}")
        print(f"Technologies Recommended: {len(documentation['technology_recommendations'])}")