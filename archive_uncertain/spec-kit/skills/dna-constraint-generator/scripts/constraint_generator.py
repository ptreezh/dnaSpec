"""
DNASPEC Constraint Generator Script
Implements the core functionality for generating system constraints based on project requirements
"""

import re
from typing import Dict, Any, List, Tuple
from enum import Enum


class ConstraintType(Enum):
    PERFORMANCE = "performance"
    SECURITY = "security"
    DATA = "data"
    QUALITY = "quality"
    OPERATIONAL = "operational"


class Constraint:
    def __init__(self, id: str, type: ConstraintType, description: str, severity: str, 
                 applies_to: List[str] = None, verification_method: str = ""):
        self.id = id
        self.type = type
        self.description = description
        self.severity = severity  # critical, high, medium, low
        self.applies_to = applies_to or []
        self.verification_method = verification_method
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "description": self.description,
            "severity": self.severity,
            "applies_to": self.applies_to,
            "verification_method": self.verification_method
        }


class ConstraintGenerator:
    def __init__(self):
        self.performance_indicators = [
            r'time', r'performance', r'speed', r'fast', r'slow', r'response', 
            r'latency', r'throughput', r'concurrency', r'scal(e|ability)', 
            r'load', r'bandwidth', r'efficiency'
        ]
        
        self.security_indicators = [
            r'secure', r'security', r'privacy', r'authentication', r'authorization', 
            r'permission', r'access', r'protect', r'vulnerability', r'encryption', 
            r'compliance', r'regulation', r'policy', r'audit', r'log', r'cryptography'
        ]
        
        self.data_indicators = [
            r'data', r'database', r'storage', r'format', r'structure', r'schema', 
            r'validation', r'integrity', r'consistency', r'reliability', r'transaction', 
            r'replication', r'backup', r'recovery', r'privacy', r'consent'
        ]
        
        self.quality_indicators = [
            r'quality', r'reliability', r'robust', r'fault', r'error', r'failure', 
            r'uptime', r'availability', r'maintain', r'test', r'verification', 
            r'validation', r'monitor', r'debug', r'observability'
        ]
        
        # Severity keywords
        self.severity_keywords = {
            'critical': [r'critical', r'vital', r'essential', r'must', r'require', r'mandatory'],
            'high': [r'important', r'needed', r'necessary', r'high', r'significant'],
            'medium': [r'medium', r'moderate', r'normal', r'standard'],
            'low': [r'low', r'optional', r'nice to have', r'preferred', r'desirable']
        }
    
    def identify_constraint_type(self, requirement: str) -> List[ConstraintType]:
        """Identify the type(s) of constraints based on the requirement text"""
        types = set()
        req_lower = requirement.lower()
        
        # Check for performance indicators
        for pattern in self.performance_indicators:
            if re.search(r'\b' + pattern + r'\b', req_lower):
                types.add(ConstraintType.PERFORMANCE)
        
        # Check for security indicators
        for pattern in self.security_indicators:
            if re.search(r'\b' + pattern + r'\b', req_lower):
                types.add(ConstraintType.SECURITY)
        
        # Check for data indicators
        for pattern in self.data_indicators:
            if re.search(r'\b' + pattern + r'\b', req_lower):
                types.add(ConstraintType.DATA)
        
        # Check for quality indicators
        for pattern in self.quality_indicators:
            if re.search(r'\b' + pattern + r'\b', req_lower):
                types.add(ConstraintType.QUALITY)
        
        # If no specific type identified, default to operational
        if not types:
            types.add(ConstraintType.OPERATIONAL)
        
        return list(types)
    
    def determine_severity(self, requirement: str) -> str:
        """Determine the severity of constraints based on keywords in requirement"""
        req_lower = requirement.lower()
        
        for severity, keywords in self.severity_keywords.items():
            for keyword in keywords:
                if re.search(r'\b' + keyword + r'\b', req_lower):
                    return severity
        
        # Default to medium if no keywords match
        return 'medium'
    
    def generate_performance_constraints(self, requirement: str) -> List[Constraint]:
        """Generate performance-related constraints"""
        constraints = []
        req_lower = requirement.lower()
        
        # Identify specific performance requirements
        if re.search(r'response time|latency|speed', req_lower):
            constraints.append(Constraint(
                id=f"PERF-{len(constraints)+1:03d}",
                type=ConstraintType.PERFORMANCE,
                description="System response time must be under 2 seconds for 95% of requests",
                severity=self.determine_severity(requirement),
                verification_method="Load testing with performance monitoring"
            ))
        
        if re.search(r'throughput|concurrency|simultaneous', req_lower):
            constraints.append(Constraint(
                id=f"PERF-{len(constraints)+1:03d}",
                type=ConstraintType.PERFORMANCE,
                description="System must support at least 1000 concurrent users",
                severity=self.determine_severity(requirement),
                verification_method="Stress testing with concurrent user simulation"
            ))
        
        if re.search(r'scale|scalability|growth', req_lower):
            constraints.append(Constraint(
                id=f"PERF-{len(constraints)+1:03d}",
                type=ConstraintType.PERFORMANCE,
                description="System must scale horizontally to handle traffic increases",
                severity=self.determine_severity(requirement),
                verification_method="Performance testing with increasing load"
            ))
        
        # If no specific requirements found, add general performance constraint
        if not constraints:
            constraints.append(Constraint(
                id=f"PERF-{len(constraints)+1:03d}",
                type=ConstraintType.PERFORMANCE,
                description="System must meet standard performance benchmarks for similar applications",
                severity=self.determine_severity(requirement),
                verification_method="Performance testing against industry benchmarks"
            ))
        
        return constraints
    
    def generate_security_constraints(self, requirement: str) -> List[Constraint]:
        """Generate security-related constraints"""
        constraints = []
        req_lower = requirement.lower()
        
        if re.search(r'authentication|login|access control', req_lower):
            constraints.append(Constraint(
                id=f"SEC-{len(constraints)+1:03d}",
                type=ConstraintType.SECURITY,
                description="All users must authenticate before accessing the system using strong authentication methods",
                severity=self.determine_severity(requirement),
                verification_method="Security testing and vulnerability scanning"
            ))
        
        if re.search(r'authorization|permission|privilege|role', req_lower):
            constraints.append(Constraint(
                id=f"SEC-{len(constraints)+1:03d}",
                type=ConstraintType.SECURITY,
                description="Access control must follow the principle of least privilege",
                severity=self.determine_severity(requirement),
                verification_method="Access control testing and role validation"
            ))
        
        if re.search(r'encrypt|privacy|secure transmission', req_lower):
            constraints.append(Constraint(
                id=f"SEC-{len(constraints)+1:03d}",
                type=ConstraintType.SECURITY,
                description="All sensitive data must be encrypted both in transit and at rest",
                severity=self.determine_severity(requirement),
                verification_method="Encryption validation and penetration testing"
            ))
        
        if re.search(r'compliance|regulation|law', req_lower):
            constraints.append(Constraint(
                id=f"SEC-{len(constraints)+1:03d}",
                type=ConstraintType.SECURITY,
                description="System must comply with applicable regulations (e.g., GDPR, HIPAA)",
                severity=self.determine_severity(requirement),
                verification_method="Compliance auditing and legal review"
            ))
        
        # If no specific requirements found, add general security constraint
        if not constraints:
            constraints.append(Constraint(
                id=f"SEC-{len(constraints)+1:03d}",
                type=ConstraintType.SECURITY,
                description="System must implement standard security best practices",
                severity=self.determine_severity(requirement),
                verification_method="Security assessment and best practices review"
            ))
        
        return constraints
    
    def generate_data_constraints(self, requirement: str) -> List[Constraint]:
        """Generate data-related constraints"""
        constraints = []
        req_lower = requirement.lower()
        
        if re.search(r'data format|schema|validation|structure', req_lower):
            constraints.append(Constraint(
                id=f"DATA-{len(constraints)+1:03d}",
                type=ConstraintType.DATA,
                description="All data must conform to defined schemas with proper validation",
                severity=self.determine_severity(requirement),
                verification_method="Schema validation and data testing"
            ))
        
        if re.search(r'integrity|consistency|reliability', req_lower):
            constraints.append(Constraint(
                id=f"DATA-{len(constraints)+1:03d}",
                type=ConstraintType.DATA,
                description="Data integrity must be maintained through ACID transactions",
                severity=self.determine_severity(requirement),
                verification_method="Transaction testing and data consistency checks"
            ))
        
        if re.search(r'backup|recovery|availability', req_lower):
            constraints.append(Constraint(
                id=f"DATA-{len(constraints)+1:03d}",
                type=ConstraintType.DATA,
                description="Data must be backed up regularly with recovery time objectives defined",
                severity=self.determine_severity(requirement),
                verification_method="Backup and recovery testing"
            ))
        
        if re.search(r'privacy|consent|personal', req_lower):
            constraints.append(Constraint(
                id=f"DATA-{len(constraints)+1:03d}",
                type=ConstraintType.DATA,
                description="Personal data must be processed according to privacy regulations",
                severity=self.determine_severity(requirement),
                verification_method="Privacy compliance audit"
            ))
        
        # If no specific requirements found, add general data constraint
        if not constraints:
            constraints.append(Constraint(
                id=f"DATA-{len(constraints)+1:03d}",
                type=ConstraintType.DATA,
                description="Data must be stored and processed according to standard practices",
                severity=self.determine_severity(requirement),
                verification_method="Data handling review"
            ))
        
        return constraints
    
    def generate_quality_constraints(self, requirement: str) -> List[Constraint]:
        """Generate quality-related constraints"""
        constraints = []
        req_lower = requirement.lower()
        
        if re.search(r'reliable|robust|fault|error|failure', req_lower):
            constraints.append(Constraint(
                id=f"QUAL-{len(constraints)+1:03d}",
                type=ConstraintType.QUALITY,
                description="System must have fault tolerance and error recovery mechanisms",
                severity=self.determine_severity(requirement),
                verification_method="Fault injection testing and error handling validation"
            ))
        
        if re.search(r'uptime|availability|downtime', req_lower):
            constraints.append(Constraint(
                id=f"QUAL-{len(constraints)+1:03d}",
                type=ConstraintType.QUALITY,
                description="System must maintain 99.9% availability during operational hours",
                severity=self.determine_severity(requirement),
                verification_method="Availability monitoring and tracking"
            ))
        
        if re.search(r'test|verify|validation', req_lower):
            constraints.append(Constraint(
                id=f"QUAL-{len(constraints)+1:03d}",
                type=ConstraintType.QUALITY,
                description="Code must have at least 80% test coverage with automated tests",
                severity=self.determine_severity(requirement),
                verification_method="Test coverage analysis and CI/CD validation"
            ))
        
        if re.search(r'monitor|debug|log|observability', req_lower):
            constraints.append(Constraint(
                id=f"QUAL-{len(constraints)+1:03d}",
                type=ConstraintType.QUALITY,
                description="System must provide comprehensive monitoring and logging",
                severity=self.determine_severity(requirement),
                verification_method="Monitoring and logging validation"
            ))
        
        # If no specific requirements found, add general quality constraint
        if not constraints:
            constraints.append(Constraint(
                id=f"QUAL-{len(constraints)+1:03d}",
                type=ConstraintType.QUALITY,
                description="System must meet standard quality and reliability expectations",
                severity=self.determine_severity(requirement),
                verification_method="Quality assessment and testing"
            ))
        
        return constraints
    
    def generate_operational_constraints(self, requirement: str) -> List[Constraint]:
        """Generate operational constraints when no specific type is identified"""
        constraints = []
        
        constraints.append(Constraint(
            id=f"OP-{len(constraints)+1:03d}",
            type=ConstraintType.OPERATIONAL,
            description="System must follow standard operational procedures and practices",
            severity=self.determine_severity(requirement),
            verification_method="Operational review and procedure validation"
        ))
        
        return constraints
    
    def generate_constraints(self, requirements: str) -> List[Constraint]:
        """Generate constraints based on the provided requirements"""
        # Identify constraint types based on requirements
        types = self.identify_constraint_type(requirements)
        
        all_constraints = []
        
        for constraint_type in types:
            if constraint_type == ConstraintType.PERFORMANCE:
                all_constraints.extend(self.generate_performance_constraints(requirements))
            elif constraint_type == ConstraintType.SECURITY:
                all_constraints.extend(self.generate_security_constraints(requirements))
            elif constraint_type == ConstraintType.DATA:
                all_constraints.extend(self.generate_data_constraints(requirements))
            elif constraint_type == ConstraintType.QUALITY:
                all_constraints.extend(self.generate_quality_constraints(requirements))
            else:  # OPERATIONAL
                all_constraints.extend(self.generate_operational_constraints(requirements))
        
        # Ensure unique IDs
        for i, constraint in enumerate(all_constraints):
            if constraint.id.startswith("OP-"):
                constraint.id = f"OP-{i+1:03d}"
            elif constraint.id.startswith("PERF-"):
                constraint.id = f"PERF-{i+1:03d}"
            elif constraint.id.startswith("SEC-"):
                constraint.id = f"SEC-{i+1:03d}"
            elif constraint.id.startswith("DATA-"):
                constraint.id = f"DATA-{i+1:03d}"
            elif constraint.id.startswith("QUAL-"):
                constraint.id = f"QUAL-{i+1:03d}"
        
        return all_constraints
    
    def generate_constraint_documentation(self, requirements: str) -> Dict[str, Any]:
        """Generate complete constraint documentation from requirements"""
        constraints = self.generate_constraints(requirements)
        
        # Group constraints by type
        constraints_by_type = {}
        for constraint in constraints:
            constraint_type = constraint.type.value
            if constraint_type not in constraints_by_type:
                constraints_by_type[constraint_type] = []
            constraints_by_type[constraint_type].append(constraint.to_dict())
        
        return {
            "input_requirements": requirements[:100] + "..." if len(requirements) > 100 else requirements,
            "total_constraints": len(constraints),
            "constraints_by_type": constraints_by_type,
            "all_constraints": [c.to_dict() for c in constraints],
            "constraint_summary": {
                "performance": len([c for c in constraints if c.type == ConstraintType.PERFORMANCE]),
                "security": len([c for c in constraints if c.type == ConstraintType.SECURITY]),
                "data": len([c for c in constraints if c.type == ConstraintType.DATA]),
                "quality": len([c for c in constraints if c.type == ConstraintType.QUALITY]),
                "operational": len([c for c in constraints if c.type == ConstraintType.OPERATIONAL])
            }
        }


def main():
    """
    Example usage of the ConstraintGenerator
    """
    requirements = """
    The system needs to support thousands of concurrent users with low latency.
    User data must be protected with strong encryption and proper access controls.
    The application should be reliable with high uptime and proper error handling.
    All personal information must be stored securely following privacy regulations.
    """
    
    generator = ConstraintGenerator()
    documentation = generator.generate_constraint_documentation(requirements)
    
    print("## Constraint Documentation Report")
    print(f"Input Requirements Preview: {documentation['input_requirements']}")
    print(f"Total Constraints Generated: {documentation['total_constraints']}")
    print("\n### Constraints Summary:")
    for category, count in documentation['constraint_summary'].items():
        print(f"- {category.title()}: {count} constraints")
    
    print("\n### All Constraints:")
    for constraint in documentation['all_constraints']:
        print(f"\n- **{constraint['id']}** ({constraint['type']}, {constraint['severity']}):")
        print(f"  {constraint['description']}")
        print(f"  Verification: {constraint['verification_method']}")


if __name__ == "__main__":
    main()