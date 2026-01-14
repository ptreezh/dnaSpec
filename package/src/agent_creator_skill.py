"""
Agent Creator Skill Implementation
Following the TDD plan with KISS, SOLID, and YAGNI principles
"""
from typing import Dict, Any, List
from src.dna_spec_kit_integration.core.skill import DNASpecSkill, SkillResult, SkillStatus
import uuid
import time


class AgentCreatorSkill(DNASpecSkill):
    """
    Agent Creator Skill - Creates specialized AI agents based on role description
    Adheres strictly to KISS, SOLID, and YAGNI principles
    """
    
    def __init__(self):
        super().__init__(
            name="dnaspec-agent-creator-simple",
            description="Simple Agent Creator - Creates specialized AI agents based on role description"
        )
        # Keep dependencies minimal
        self.default_capabilities = [
            "Task execution", 
            "Information retrieval", 
            "Decision making"
        ]

    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """
        Execute agent creation logic
        Single method with clear responsibility
        """
        # Parse inputs - keep simple
        role = request  # Primary input is the role description
        capabilities = context.get('capabilities', self.default_capabilities)
        domain = context.get('domain', 'general')
        
        # Generate agent configuration - single responsibility
        agent_config = self._generate_agent_config(role, capabilities, domain)
        
        return {
            "agent_config": agent_config,
            "success": True,
            "timestamp": time.time()
        }

    def _generate_agent_config(self, role: str, capabilities: List[str], domain: str) -> Dict[str, Any]:
        """
        Generate agent configuration based on inputs
        Maintains single responsibility
        """
        # Simple config generation - no complex logic
        return {
            "id": f"agent_{uuid.uuid4().hex[:8]}",
            "role": role,
            "domain": domain,
            "capabilities": capabilities,
            "instructions": self._generate_base_instructions(role, domain),
            "personality": "Professional, helpful, focused on assigned tasks"
        }

    def _generate_base_instructions(self, role: str, domain: str) -> str:
        """
        Generate base instructions for agent
        Simple template-based approach
        """
        return f"""
        You are acting as a {role} in the {domain} domain.
        Your primary function is to assist with tasks related to your role.
        Be helpful, professional, and stay within your defined capabilities.
        """