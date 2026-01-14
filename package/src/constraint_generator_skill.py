"""
Constraint Generator Skill Implementation
Following the TDD plan with KISS, SOLID, and YAGNI principles
"""
from typing import Dict, Any, List
from src.dna_spec_kit_integration.core.skill import DNASpecSkill, SkillResult, SkillStatus
import uuid
from datetime import datetime


class ConstraintGeneratorSkill(DNASpecSkill):
    """
    Constraint Generator Skill - Generates and manages system constraints
    Adheres strictly to KISS, SOLID, and YAGNI principles
    """
    
    def __init__(self):
        super().__init__(
            name="dnaspec-constraint-generator-simple",
            description="Simple Constraint Generator - Manages constraints following KISS principles"
        )
        # Keep state simple, avoid complex data structures (KISS)
        self.active_constraints = []
        self.versions = {}
        self.current_version = None

    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """
        Execute constraint generation logic
        Single method with clear responsibility
        """
        # Parse inputs - keep simple
        requirements = request
        change_request = context.get('change_request', '')
        track_version = context.get('track_version', False)
        
        # Generate constraints from requirements - single responsibility
        new_constraints = self._generate_constraints_from_requirements(requirements)
        
        # Perform alignment check if change request provided
        alignment_check = self._perform_alignment_check(requirements, change_request)
        
        # Track version if requested
        version_info = self._handle_version_tracking(requirements, track_version)
        
        # Update active constraints
        self.active_constraints.extend(new_constraints)
        
        return {
            "constraints": new_constraints,
            "alignment_check": alignment_check,
            "version_info": version_info,
            "success": True,
            "timestamp": datetime.now().timestamp()
        }

    def _generate_constraints_from_requirements(self, requirements: str) -> List[Dict[str, Any]]:
        """
        Generate constraints based on requirements
        Simple keyword-based approach (KISS)
        """
        constraints = []
        req_lower = requirements.lower()
        
        # Security constraints
        if any(term in req_lower for term in ['security', 'secure', 'auth', 'encrypt', 'privacy', 'protect']):
            constraints.append({
                "id": f"constraint_{uuid.uuid4().hex[:8]}",
                "type": "security",
                "description": "System must implement standard security measures",
                "severity": "high",
                "created_at": datetime.now().isoformat()
            })

        # Performance constraints
        if any(term in req_lower for term in ['performance', 'fast', 'response', 'throughput', 'latency']):
            constraints.append({
                "id": f"constraint_{uuid.uuid4().hex[:8]}",
                "type": "performance",
                "description": "System must meet defined performance requirements",
                "severity": "medium",
                "created_at": datetime.now().isoformat()
            })

        # Data constraints
        if any(term in req_lower for term in ['data', 'database', 'storage', 'retrieve', 'persist']):
            constraints.append({
                "id": f"constraint_{uuid.uuid4().hex[:8]}",
                "type": "data_integrity",
                "description": "System must maintain data integrity and backup capabilities",
                "severity": "high",
                "created_at": datetime.now().isoformat()
            })

        # Keep it simple - return basic constraints based on keywords
        return constraints

    def _perform_alignment_check(self, base_requirements: str, change_request: str) -> Dict[str, Any]:
        """
        Check alignment between base requirements and change request
        Simple comparison approach (KISS)
        """
        if not change_request:
            # If no change request, consider aligned
            return {
                "is_aligned": True,
                "conflicts": [],
                "suggestions": ["No change request provided, requirements are baseline"]
            }
        
        # Simple alignment check - if change contradicts base requirements
        conflicts = []
        suggestions = []
        
        # Check for obvious conflicts
        base_req_lower = base_requirements.lower()
        change_req_lower = change_request.lower()
        
        # Look for contradictory terms
        contradiction_pairs = [
            ('security', 'no security'),
            ('performance', 'negligible performance'),
            ('reliability', 'unreliable')
        ]
        
        for positive, negative in contradiction_pairs:
            if positive in base_req_lower and negative in change_req_lower:
                conflicts.append({
                    "type": "RequirementsConflict",
                    "description": f"Change request '{change_request}' conflicts with base requirement '{positive}'",
                    "severity": "high"
                })
        
        # Determine alignment
        is_aligned = len(conflicts) == 0
        
        if is_aligned:
            suggestions.append("Change request appears aligned with base requirements")
        else:
            suggestions.append("Address conflicts before proceeding with change request")
        
        return {
            "is_aligned": is_aligned,
            "conflicts": conflicts,
            "suggestions": suggestions
        }

    def _handle_version_tracking(self, requirements: str, track_version: bool) -> Dict[str, Any]:
        """
        Handle version tracking if requested
        Simple version management (KISS)
        """
        if track_version:
            version_id = f"version_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
            self.versions[version_id] = {
                "requirements": requirements,
                "timestamp": datetime.now().isoformat(),
                "constraints": [c["id"] for c in self._generate_constraints_from_requirements(requirements)]
            }
            self.current_version = version_id
            
            return {
                "current_version": version_id,
                "tracked": True
            }
        else:
            return {
                "current_version": self.current_version,
                "tracked": False
            }