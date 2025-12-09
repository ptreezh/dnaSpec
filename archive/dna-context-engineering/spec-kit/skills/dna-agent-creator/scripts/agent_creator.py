"""
DNASPEC Agent Creator Script
Implements the core functionality for creating and configuring intelligent agents
"""

import re
from typing import Dict, Any, List, Tuple
from enum import Enum
import json


class AgentType(Enum):
    REACTIVE = "reactive"
    DELIBERATIVE = "deliberative" 
    LEARNING = "learning"
    HYBRID = "hybrid"


class AgentRole(Enum):
    TASK_EXECUTOR = "task-executor"
    COMMUNICATION = "communication"
    MONITORING = "monitoring"
    DECISION_MAKER = "decision-maker"
    LEARNING = "learning"


class Agent:
    def __init__(self, name: str, agent_type: AgentType, role: AgentRole,
                 capabilities: List[str] = None, constraints: List[str] = None):
        self.name = name
        self.type = agent_type
        self.role = role
        self.capabilities = capabilities or []
        self.constraints = constraints or []
        self.communication_protocols = []
        self.configuration = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type.value,
            "role": self.role.value,
            "capabilities": self.capabilities,
            "constraints": self.constraints,
            "communication_protocols": self.communication_protocols,
            "configuration": self.configuration
        }


class AgentCreator:
    def __init__(self):
        self.task_keywords = [
            'execute', 'perform', 'do', 'implement', 'carry out', 'complete', 
            'fulfill', 'conduct', 'accomplish', 'achieve'
        ]
        
        self.communication_keywords = [
            'communicate', 'coordinate', 'interact', 'message', 'notify', 
            'report', 'update', 'sync', 'share', 'transfer'
        ]
        
        self.monitoring_keywords = [
            'monitor', 'track', 'watch', 'observe', 'check', 'verify', 
            'validate', 'audit', 'log', 'analyze'
        ]
        
        self.decision_keywords = [
            'decide', 'choose', 'select', 'evaluate', 'assess', 'judge', 
            'determine', 'recommend', 'suggest', 'plan'
        ]
        
        self.learning_keywords = [
            'learn', 'adapt', 'improve', 'evolve', 'update', 'optimize',
            'train', 'predict', 'recognize', 'classify'
        ]
    
    def identify_agent_role(self, requirements: str) -> AgentRole:
        """Identify the most appropriate agent role based on requirements"""
        req_lower = requirements.lower()
        
        # Count occurrences of keywords for each role
        task_count = sum(1 for keyword in self.task_keywords if keyword in req_lower)
        comm_count = sum(1 for keyword in self.communication_keywords if keyword in req_lower)
        mon_count = sum(1 for keyword in self.monitoring_keywords if keyword in req_lower)
        dec_count = sum(1 for keyword in self.decision_keywords if keyword in req_lower)
        learn_count = sum(1 for keyword in self.learning_keywords if keyword in req_lower)
        
        # Determine the role with the most matching keywords
        counts = [
            (AgentRole.TASK_EXECUTOR, task_count),
            (AgentRole.COMMUNICATION, comm_count),
            (AgentRole.MONITORING, mon_count),
            (AgentRole.DECISION_MAKER, dec_count),
            (AgentRole.LEARNING, learn_count)
        ]
        
        # Sort by count and pick the highest
        most_appropriate = max(counts, key=lambda x: x[1])
        
        # If no keywords match, default to task executor
        if most_appropriate[1] == 0:
            return AgentRole.TASK_EXECUTOR
        
        return most_appropriate[0]
    
    def identify_agent_type(self, requirements: str, role: AgentRole) -> AgentType:
        """Identify the most appropriate agent type based on requirements and role"""
        req_lower = requirements.lower()
        
        # Determine type based on keywords and context
        if 'reactive' in req_lower or 'response' in req_lower or 'immediate' in req_lower:
            return AgentType.REACTIVE
        elif 'plan' in req_lower or 'think' in req_lower or 'analyze' in req_lower or 'consider' in req_lower:
            return AgentType.DELIBERATIVE
        elif 'learn' in req_lower or 'adapt' in req_lower or 'evolve' in req_lower:
            return AgentType.LEARNING
        elif 'reactive' in req_lower and ('plan' in req_lower or 'analyze' in req_lower):
            return AgentType.HYBRID
        elif role == AgentRole.LEARNING:
            return AgentType.LEARNING
        else:
            # Default based on role
            if role in [AgentRole.DECISION_MAKER, AgentRole.MONITORING]:
                return AgentType.DELIBERATIVE
            else:
                return AgentType.REACTIVE
    
    def extract_capabilities(self, requirements: str) -> List[str]:
        """Extract potential capabilities from requirements"""
        capabilities = set()
        
        # Look for specific capabilities in the requirements
        capability_patterns = [
            r'ability to (\w+)',
            r'can (\w+)',
            r'should be able to (\w+)',
            r'capability for (\w+)',
            r'function to (\w+)',
            r'needs to (\w+)',
            r'must (\w+)'
        ]
        
        for pattern in capability_patterns:
            matches = re.findall(pattern, requirements, re.IGNORECASE)
            for match in matches:
                capabilities.add(match.lower())
        
        # Add common capabilities based on role
        if 'data' in requirements.lower():
            capabilities.add('handle data')
        if 'security' in requirements.lower():
            capabilities.add('ensure security')
        if 'user' in requirements.lower():
            capabilities.add('interact with users')
        if 'api' in requirements.lower():
            capabilities.add('interface with APIs')
        if 'database' in requirements.lower():
            capabilities.add('access databases')
        if 'real-time' in requirements.lower() or 'immediate' in requirements.lower():
            capabilities.add('real-time processing')
        
        return list(capabilities)
    
    def identify_constraints(self, requirements: str) -> List[str]:
        """Identify constraints and limitations from requirements"""
        constraints = set()
        
        # Look for constraint indicators
        constraint_patterns = [
            r'should not (\w+)',
            r'cannot (\w+)',
            r'must not (\w+)',
            r'prohibited from (\w+)',
            r'restricted to (\w+)',
            r'limited by (\w+)',
            r'only allowed to (\w+)',
            r'no (\w+)',
        ]
        
        for pattern in constraint_patterns:
            matches = re.findall(pattern, requirements, re.IGNORECASE)
            for match in matches:
                constraints.add(f"Must not {match}")
        
        # Add specific constraints based on keywords
        req_lower = requirements.lower()
        if 'secure' in req_lower or 'security' in req_lower:
            constraints.add("Must follow security protocols")
        if 'private' in req_lower or 'privacy' in req_lower:
            constraints.add("Must protect private data")
        if 'performance' in req_lower or 'efficiency' in req_lower:
            constraints.add("Must optimize for performance")
        if 'reliable' in req_lower:
            constraints.add("Must ensure reliability")
        
        return list(constraints)
    
    def determine_communication_protocols(self, requirements: str) -> List[str]:
        """Determine appropriate communication protocols based on requirements"""
        protocols = []
        
        req_lower = requirements.lower()
        
        if 'api' in req_lower or 'rest' in req_lower:
            protocols.append('REST API')
        if 'message' in req_lower or 'queue' in req_lower:
            protocols.append('Message Queue')
        if 'real-time' in req_lower or 'websocket' in req_lower:
            protocols.append('WebSocket')
        if 'secure' in req_lower or 'authentication' in req_lower:
            protocols.append('Secure Communication with Authentication')
        if 'broadcast' in req_lower:
            protocols.append('Broadcast/Multicast')
        
        # Default protocol if none specified
        if not protocols:
            protocols.append('Standard API Communication')
        
        return protocols
    
    def create_agent(self, name: str, requirements: str) -> Agent:
        """Create an agent based on requirements"""
        role = self.identify_agent_role(requirements)
        agent_type = self.identify_agent_type(requirements, role)
        capabilities = self.extract_capabilities(requirements)
        constraints = self.identify_constraints(requirements)
        protocols = self.determine_communication_protocols(requirements)
        
        agent = Agent(name, agent_type, role, capabilities, constraints)
        agent.communication_protocols = protocols
        
        # Generate basic configuration based on type
        if agent_type == AgentType.REACTIVE:
            agent.configuration = {
                "response_time": "immediate",
                "decision_making": "rule_based",
                "memory": "minimal",
                "planning": "none"
            }
        elif agent_type == AgentType.DELIBERATIVE:
            agent.configuration = {
                "response_time": "considered",
                "decision_making": "analytical",
                "memory": "extensive", 
                "planning": "strategic"
            }
        elif agent_type == AgentType.LEARNING:
            agent.configuration = {
                "response_time": "adaptive",
                "decision_making": "learning_based",
                "memory": "evolving",
                "planning": "predictive"
            }
        elif agent_type == AgentType.HYBRID:
            agent.configuration = {
                "response_time": "adaptive",
                "decision_making": "hybrid",
                "memory": "extensive",
                "planning": "both_immediate_strategic"
            }
        
        return agent
    
    def generate_agent_specification(self, name: str, requirements: str) -> Dict[str, Any]:
        """Generate a complete agent specification"""
        agent = self.create_agent(name, requirements)
        
        specification = {
            "agent_name": agent.name,
            "agent_type": agent.type.value,
            "agent_role": agent.role.value,
            "capabilities": agent.capabilities,
            "constraints": agent.constraints,
            "communication_protocols": agent.communication_protocols,
            "configuration": agent.configuration,
            "design_recommendations": self.generate_design_recommendations(agent),
            "implementation_notes": self.generate_implementation_notes(agent, requirements)
        }
        
        return specification
    
    def generate_design_recommendations(self, agent: Agent) -> List[str]:
        """Generate design recommendations based on agent type and role"""
        recommendations = []
        
        if agent.type == AgentType.REACTIVE:
            recommendations.append("Implement event-driven architecture")
            recommendations.append("Use rule-based decision making")
            recommendations.append("Focus on fast response times")
        
        if agent.type == AgentType.DELIBERATIVE:
            recommendations.append("Implement planning and reasoning modules")
            recommendations.append("Include extensive state tracking")
            recommendations.append("Use analytical decision making")
        
        if agent.type == AgentType.LEARNING:
            recommendations.append("Include machine learning components")
            recommendations.append("Implement feedback mechanisms")
            recommendations.append("Plan for model training and updating")
        
        if agent.role == AgentRole.COMMUNICATION:
            recommendations.append("Implement robust message handling")
            recommendations.append("Ensure reliable communication protocols")
            recommendations.append("Plan for message queuing if needed")
        
        if agent.role == AgentRole.MONITORING:
            recommendations.append("Implement logging and tracking")
            recommendations.append("Include alerting mechanisms")
            recommendations.append("Plan for metric collection")
        
        return recommendations
    
    def generate_implementation_notes(self, agent: Agent, requirements: str) -> List[str]:
        """Generate implementation notes based on agent and requirements"""
        notes = []
        
        if 'performance' in requirements.lower():
            notes.append("Optimize for performance with efficient algorithms")
        if 'security' in requirements.lower():
            notes.append("Implement security measures throughout the agent")
        if 'scalability' in requirements.lower():
            notes.append("Design with scalability in mind")
        
        # Add notes based on type
        if agent.type == AgentType.LEARNING:
            notes.append("Include model versioning and management")
        
        # Add notes based on role
        if agent.role == AgentRole.DECISION_MAKER:
            notes.append("Implement decision validation and audit trails")
        
        return notes


def main():
    """
    Example usage of the AgentCreator
    """
    requirements = """
    Create an agent that can monitor system performance and alert administrators 
    when certain thresholds are exceeded. The agent should collect metrics, 
    analyze them in real-time, and send notifications to appropriate channels. 
    It must be secure and reliable, with minimal impact on system performance.
    """
    
    creator = AgentCreator()
    specification = creator.generate_agent_specification("SystemMonitorAgent", requirements)
    
    print("## Agent Specification Report")
    print(f"Agent Name: {specification['agent_name']}")
    print(f"Type: {specification['agent_type']}")
    print(f"Role: {specification['agent_role']}")
    
    print(f"\n### Capabilities:")
    for capability in specification['capabilities']:
        print(f"- {capability}")
    
    print(f"\n### Constraints:")
    for constraint in specification['constraints']:
        print(f"- {constraint}")
    
    print(f"\n### Communication Protocols:")
    for protocol in specification['communication_protocols']:
        print(f"- {protocol}")
    
    print(f"\n### Configuration:")
    for key, value in specification['configuration'].items():
        print(f"- {key}: {value}")
    
    print(f"\n### Design Recommendations:")
    for recommendation in specification['design_recommendations']:
        print(f"- {recommendation}")
    
    print(f"\n### Implementation Notes:")
    for note in specification['implementation_notes']:
        print(f"- {note}")


if __name__ == "__main__":
    main()