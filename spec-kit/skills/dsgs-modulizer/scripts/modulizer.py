"""
DNASPEC Modulizer Script
Implements the core functionality for module maturation verification 
and modular encapsulation following the principle of maximum modularity.
"""

import re
from typing import Dict, Any, List, Tuple
from enum import Enum
import json


class MaturityLevel(Enum):
    UNDEFINED = "undefined"  # No maturity assessment
    INITIAL = "initial"      # Basic concept, no implementation
    DEVELOPING = "developing"  # In development, partial implementation
    STABLE = "stable"       # Implemented and stable
    MATURE = "mature"       # Fully mature, well-tested, documented
    OPTIMIZED = "optimized"  # Optimized for performance and usability


class ModuleQuality(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


class Module:
    def __init__(self, name: str, description: str = "", 
                 dependencies: List[str] = None, interfaces: List[str] = None):
        self.name = name
        self.description = description
        self.dependencies = dependencies or []
        self.interfaces = interfaces or []
        self.maturity = MaturityLevel.UNDEFINED
        self.cohesion_score = 0.0  # 0.0-1.0
        self.coupling_score = 0.0  # 0.0-1.0, lower is better
        self.interface_stability = 0.0  # 0.0-1.0
        self.documentation_completeness = 0.0  # 0.0-1.0
        self.test_coverage = 0.0  # 0.0-1.0
        self.quality = ModuleQuality.CRITICAL

    def calculate_overall_maturity(self) -> MaturityLevel:
        """Calculate maturity level based on various factors"""
        factors = [
            self.cohesion_score,
            (1 - self.coupling_score),  # Inverse since lower coupling is better
            self.interface_stability,
            self.documentation_completeness,
            self.test_coverage
        ]
        
        avg_score = sum(factors) / len(factors)
        
        if avg_score >= 0.9:
            return MaturityLevel.OPTIMIZED
        elif avg_score >= 0.75:
            return MaturityLevel.MATURE
        elif avg_score >= 0.6:
            return MaturityLevel.STABLE
        elif avg_score >= 0.4:
            return MaturityLevel.DEVELOPING
        else:
            return MaturityLevel.INITIAL

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "dependencies": self.dependencies,
            "interfaces": self.interfaces,
            "maturity": self.maturity.value,
            "cohesion_score": self.cohesion_score,
            "coupling_score": self.coupling_score,
            "interface_stability": self.interface_stability,
            "documentation_completeness": self.documentation_completeness,
            "test_coverage": self.test_coverage,
            "quality": self.quality.value,
            "calculated_maturity": self.calculate_overall_maturity().value
        }


class DSGSModulizer:
    def __init__(self):
        # Thresholds for different quality levels
        self.quality_thresholds = {
            ModuleQuality.EXCELLENT: 0.9,
            ModuleQuality.GOOD: 0.75,
            ModuleQuality.FAIR: 0.6,
            ModuleQuality.POOR: 0.4,
            ModuleQuality.CRITICAL: 0.0
        }

    def assess_cohesion(self, module_description: str) -> Tuple[float, List[str]]:
        """Assess the cohesion of a module based on its description"""
        issues = []
        
        # Look for signs of low cohesion (multiple unrelated responsibilities)
        responsibility_keywords = [
            r'and\b',  # Indicates multiple responsibilities
            r'or\b',   # Indicates choice between responsibilities
            r'as well as\b',
            r'also\b'
        ]
        
        issue_count = 0
        for keyword in responsibility_keywords:
            matches = re.findall(keyword, module_description, re.IGNORECASE)
            issue_count += len(matches)
        
        # Look for specific functionality keywords that might indicate scattering
        scattered_functionality = [
            'user', 'database', 'payment', 'notification', 'logging', 
            'security', 'cache', 'email', 'file', 'validation'
        ]
        
        found_functionalities = []
        for func in scattered_functionality:
            if re.search(r'\b' + func + r'\b', module_description, re.IGNORECASE):
                found_functionalities.append(func)
        
        if len(found_functionalities) > 3:
            issues.append(f"Module appears to handle multiple unrelated concerns: {', '.join(found_functionalities[:5])}")
        
        # Calculate cohesion score (lower number of issues = higher cohesion)
        max_issues = 10  # Assume 10+ issues = 0% cohesion
        cohesion_score = max(0.0, 1.0 - (min(issue_count, max_issues) / max_issues))
        
        # Further reduce cohesion for too many unrelated functionalities
        if len(found_functionalities) > 3:
            cohesion_score *= (3.0 / len(found_functionalities))
        
        return round(cohesion_score, 2), issues

    def assess_coupling(self, dependencies: List[str]) -> Tuple[float, List[str]]:
        """Assess the coupling of a module based on its dependencies"""
        issues = []
        
        coupling_score = 0.0
        if len(dependencies) == 0:
            # Highly independent module
            coupling_score = 0.1  # Not 0 to allow for some necessary dependencies
        elif len(dependencies) <= 3:
            # Reasonable number of dependencies
            coupling_score = 0.3
        elif len(dependencies) <= 6:
            # Moderate number of dependencies
            coupling_score = 0.6
            issues.append("Module has many dependencies, consider reducing coupling")
        else:
            # Too many dependencies
            coupling_score = 0.9
            issues.append(f"Module has too many dependencies ({len(dependencies)}), high coupling")
        
        return round(coupling_score, 2), issues

    def assess_interface_stability(self, interfaces: List[str]) -> Tuple[float, List[str]]:
        """Assess the stability of module interfaces"""
        issues = []
        
        if not interfaces:
            return 0.2, ["Module has no defined interfaces"]
        
        # Look for interface patterns that indicate stability
        stable_indicators = 0
        unstable_indicators = 0
        
        for interface in interfaces:
            interface_lower = interface.lower()
            
            # Stable interface indicators
            if re.search(r'get|find|retrieve|search', interface_lower):
                stable_indicators += 1
            elif re.search(r'create|add|insert', interface_lower):
                stable_indicators += 1
            elif re.search(r'update|modify|change', interface_lower):
                stable_indicators += 1
            elif re.search(r'delete|remove|destroy', interface_lower):
                stable_indicators += 1
            
            # Unstable/complex interface indicators
            if re.search(r'and|or|with|using', interface_lower):
                unstable_indicators += 1
            if len(interface) > 50:  # Very long interface names may indicate complexity
                unstable_indicators += 1
        
        # Calculate stability score
        if len(interfaces) == 0:
            stability_score = 0.0
        else:
            stability_score = max(0.0, min(1.0, stable_indicators / len(interfaces)))
            # Reduce score based on unstable indicators
            stability_score = max(0.0, stability_score - (unstable_indicators / len(interfaces)))
        
        if unstable_indicators > stable_indicators:
            issues.append(f"Module interfaces appear complex with {unstable_indicators} potentially unstable patterns")
        
        return round(stability_score, 2), issues

    def assess_documentation_quality(self, description: str) -> Tuple[float, List[str]]:
        """Assess the quality of module documentation"""
        issues = []
        
        if not description or len(description.strip()) < 10:
            return 0.1, ["Module has insufficient documentation"]
        
        # Check for key documentation elements
        has_purpose = bool(re.search(r'purpose|function|role', description, re.IGNORECASE))
        has_inputs = bool(re.search(r'input|parameter|argument|accept', description, re.IGNORECASE))
        has_outputs = bool(re.search(r'output|return|result|provide', description, re.IGNORECASE))
        has_dependencies = bool(re.search(r'use|depend|require|need', description, re.IGNORECASE))
        
        doc_score = sum([has_purpose, has_inputs, has_outputs, has_dependencies]) / 4.0
        
        if not has_purpose:
            issues.append("Documentation does not clearly state the module's purpose")
        if not has_inputs:
            issues.append("Documentation does not describe inputs/parameters")
        if not has_outputs:
            issues.append("Documentation does not describe outputs/results")
        if not has_dependencies:
            issues.append("Documentation does not mention dependencies or requirements")
        
        return round(doc_score, 2), issues

    def assess_module(self, name: str, description: str = "", 
                     dependencies: List[str] = None, 
                     interfaces: List[str] = None) -> Module:
        """Assess a module's maturity and quality"""
        if dependencies is None:
            dependencies = []
        if interfaces is None:
            interfaces = []
        
        module = Module(name, description, dependencies, interfaces)
        
        # Assess various quality factors
        module.cohesion_score, cohesion_issues = self.assess_cohesion(description)
        module.coupling_score, coupling_issues = self.assess_coupling(dependencies)
        module.interface_stability, interface_issues = self.assess_interface_stability(interfaces)
        module.documentation_completeness, doc_issues = self.assess_documentation_quality(description)
        
        # Test coverage is not assessable from description alone, set to default
        module.test_coverage = 0.5  # Default medium coverage
        
        # Determine overall quality based on the lowest score
        scores = [
            module.cohesion_score,
            (1 - module.coupling_score),  # Inverse since lower coupling is better
            module.interface_stability,
            module.documentation_completeness,
            module.test_coverage
        ]
        
        min_score = min(scores)
        
        # Assign quality level based on minimum score
        for quality_level, threshold in self.quality_thresholds.items():
            if min_score >= threshold:
                module.quality = quality_level
                break
        
        # Calculate maturity
        module.maturity = module.calculate_overall_maturity()
        
        return module

    def identify_circular_dependencies(self, modules: List[Module]) -> List[Tuple[str, str]]:
        """Identify circular dependencies between modules"""
        circular_deps = []
        
        # Simple detection: if module A depends on B and B depends on A
        for i, module_a in enumerate(modules):
            for j, module_b in enumerate(modules):
                if i != j:
                    if module_a.name in module_b.dependencies and module_b.name in module_a.dependencies:
                        circular_deps.append((module_a.name, module_b.name))
        
        return circular_deps

    def generate_modulization_report(self, modules_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a complete modulization report"""
        modules = []
        
        # Assess each module
        for module_data in modules_data:
            module = self.assess_module(
                module_data.get('name', ''),
                module_data.get('description', ''),
                module_data.get('dependencies', []),
                module_data.get('interfaces', [])
            )
            modules.append(module)
        
        # Identify circular dependencies
        circular_deps = self.identify_circular_dependencies(modules)
        
        # Generate encapsulation recommendations
        encapsulation_recommendations = self.generate_encapsulation_recommendations(modules)
        
        # Generate maturity assessment
        maturity_assessment = self.generate_maturity_assessment(modules)
        
        report = {
            "total_modules": len(modules),
            "assessed_modules": [module.to_dict() for module in modules],
            "circular_dependencies": [{"module_a": dep[0], "module_b": dep[1]} for dep in circular_deps],
            "encapsulation_recommendations": encapsulation_recommendations,
            "maturity_assessment": maturity_assessment,
            "overall_quality_metrics": self.calculate_overall_metrics(modules),
            "refactoring_priorities": self.determine_refactoring_priorities(modules)
        }
        
        return report

    def generate_encapsulation_recommendations(self, modules: List[Module]) -> List[str]:
        """Generate recommendations for module encapsulation"""
        recommendations = []
        
        for module in modules:
            if module.quality in [ModuleQuality.CRITICAL, ModuleQuality.POOR]:
                recommendations.append(f"Module '{module.name}' requires encapsulation - quality: {module.quality.value}")
            if module.coupling_score > 0.6:
                recommendations.append(f"Module '{module.name}' has high coupling, needs encapsulation")
            if module.cohesion_score < 0.5:
                recommendations.append(f"Module '{module.name}' has low cohesion, consider refactoring for better encapsulation")
        
        if not recommendations:
            recommendations.append("All modules show appropriate encapsulation")
        
        return recommendations

    def generate_maturity_assessment(self, modules: List[Module]) -> Dict[str, Any]:
        """Generate maturity assessment summary"""
        maturity_counts = {}
        for module in modules:
            maturity_level = module.calculate_overall_maturity().value
            maturity_counts[maturity_level] = maturity_counts.get(maturity_level, 0) + 1
        
        avg_cohesion = sum(m.cohesion_score for m in modules) / len(modules) if modules else 0
        avg_coupling = sum(m.coupling_score for m in modules) / len(modules) if modules else 0
        avg_stability = sum(m.interface_stability for m in modules) / len(modules) if modules else 0
        
        return {
            "maturity_distribution": maturity_counts,
            "average_cohesion": round(avg_cohesion, 2),
            "average_coupling": round(avg_coupling, 2),
            "average_interface_stability": round(avg_stability, 2),
            "summary": f"System has {maturity_counts.get('mature', 0) + maturity_counts.get('optimized', 0)}/{len(modules)} mature modules"
        }

    def calculate_overall_metrics(self, modules: List[Module]) -> Dict[str, float]:
        """Calculate overall system metrics"""
        if not modules:
            return {}
        
        return {
            "average_cohesion": round(sum(m.cohesion_score for m in modules) / len(modules), 2),
            "average_coupling": round(sum(m.coupling_score for m in modules) / len(modules), 2),
            "average_interface_stability": round(sum(m.interface_stability for m in modules) / len(modules), 2),
            "average_documentation": round(sum(m.documentation_completeness for m in modules) / len(modules), 2),
            "average_test_coverage": round(sum(m.test_coverage for m in modules) / len(modules), 2)
        }

    def determine_refactoring_priorities(self, modules: List[Module]) -> List[Dict[str, Any]]:
        """Determine refactoring priorities based on module quality"""
        priorities = []
        
        for module in modules:
            # Calculate a priority score based on low scores in critical areas
            priority_score = 0
            if module.cohesion_score < 0.5:
                priority_score += (0.5 - module.cohesion_score) * 10
            if module.coupling_score > 0.6:
                priority_score += (module.coupling_score - 0.6) * 10
            if module.interface_stability < 0.5:
                priority_score += (0.5 - module.interface_stability) * 5
            if module.documentation_completeness < 0.5:
                priority_score += (0.5 - module.documentation_completeness) * 3
            
            if priority_score > 0:
                priorities.append({
                    "module": module.name,
                    "priority_score": round(priority_score, 2),
                    "primary_issues": [
                        f"Low cohesion ({module.cohesion_score})" if module.cohesion_score < 0.5 else None,
                        f"High coupling ({module.coupling_score})" if module.coupling_score > 0.6 else None,
                        f"Unstable interfaces ({module.interface_stability})" if module.interface_stability < 0.5 else None,
                        f"Poor documentation ({module.documentation_completeness})" if module.documentation_completeness < 0.5 else None
                    ],
                    "suggested_actions": self.generate_suggested_actions(module)
                })
        
        # Sort by priority score (highest first)
        priorities.sort(key=lambda x: x['priority_score'], reverse=True)
        return priorities

    def generate_suggested_actions(self, module: Module) -> List[str]:
        """Generate specific suggested actions for a module"""
        actions = []
        
        if module.cohesion_score < 0.5:
            actions.append("Split module into smaller, more focused components")
        if module.coupling_score > 0.6:
            actions.append("Reduce dependencies, implement dependency injection")
        if module.interface_stability < 0.5:
            actions.append("Standardize and stabilize interfaces")
        if module.documentation_completeness < 0.5:
            actions.append("Improve module documentation")
        if module.test_coverage < 0.5:
            actions.append("Increase test coverage")
        
        return actions if actions else ["Module is in good shape, no immediate actions needed"]


def main():
    """Example usage of the DSGSModulizer"""
    # Example module data from test case
    modules_data = [
        {
            "name": "User Authentication Module",
            "description": "Handles user authentication including login, logout, and session management",
            "dependencies": ["Database Module", "Logging Module"],
            "interfaces": ["login", "logout", "validate_session", "create_user"]
        },
        {
            "name": "Data Access Layer",
            "description": "Provides database access functionality for all system components including users, products, and orders",
            "dependencies": ["Database Module", "Configuration Module", "Logging Module", "Cache Module", "Security Module"],
            "interfaces": ["get_user", "save_user", "get_product", "save_product", "get_order", "save_order"]
        },
        {
            "name": "Business Logic Component",
            "description": "Implements core business rules for order processing, inventory management, and customer relations",
            "dependencies": ["Data Access Layer", "User Authentication Module", "Notification Module", "Payment Module"],
            "interfaces": ["process_order", "update_inventory", "manage_customer"]
        }
    ]
    
    modulizer = DSGSModulizer()
    report = modulizer.generate_modulization_report(modules_data)
    
    print("## DNASPEC Modulization Report")
    print(f"Total Modules: {report['total_modules']}")
    
    print("\n### Module Assessments:")
    for module in report['assessed_modules']:
        print(f"\n- {module['name']} (Quality: {module['quality']})")
        print(f"  Maturity: {module['calculated_maturity']}")
        print(f"  Cohesion: {module['cohesion_score']}, Coupling: {module['coupling_score']}")
        print(f"  Dependencies: {len(module['dependencies'])}")
        print(f"  Interfaces: {len(module['interfaces'])}")
    
    print("\n### Circular Dependencies:")
    for dep in report['circular_dependencies']:
        print(f"- {dep['module_a']} ↔ {dep['module_b']}")
    
    print("\n### Encapsulation Recommendations:")
    for rec in report['encapsulation_recommendations'][:3]:  # Show first 3
        print(f"- {rec}")
    
    print(f"\n### Maturity Assessment:")
    print(f"- Distribution: {report['maturity_assessment']['maturity_distribution']}")
    print(f"- Average Cohesion: {report['maturity_assessment']['average_cohesion']}")
    print(f"- Average Coupling: {report['maturity_assessment']['average_coupling']}")
    
    print("\n### Refactoring Priorities:")
    for priority in report['refactoring_priorities'][:3]:  # Show first 3
        print(f"- {priority['module']} (Score: {priority['priority_score']})")
        for action in priority['suggested_actions'][:2]:  # Show first 2 actions
            print(f"  * {action}")


if __name__ == "__main__":
    # Run tests for each test case scenario
    test_scenarios = [
        {
            "name": "Simple Modules",
            "modules": [
                {
                    "name": "User Authentication",
                    "description": "Handles user authentication including login, logout, and session management",
                    "dependencies": ["Database Module"],
                    "interfaces": ["login", "logout", "validate_session"]
                }
            ]
        },
        {
            "name": "Complex System",
            "modules": [
                {
                    "name": "Order Processing",
                    "description": "Processes orders, manages inventory, handles customer relations, and manages payments",
                    "dependencies": ["Inventory", "Customer", "Payment", "Notification", "Database", "Logging", "Security", "Cache"],
                    "interfaces": ["create_order", "update_order", "cancel_order", "process_refund"]
                },
                {
                    "name": "Inventory Management", 
                    "description": "Manages product inventory, stock levels, and warehouse operations",
                    "dependencies": ["Order Processing", "Database"],
                    "interfaces": ["add_product", "remove_product", "update_stock", "check_availability"]
                }
            ]
        }
    ]
    
    modulizer = DSGSModulizer()
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'='*60}")
        print(f"Running Test Scenario {i}: {scenario['name']}")
        print(f"{'='*60}")
        
        report = modulizer.generate_modulization_report(scenario['modules'])
        
        print(f"Modules Assessed: {report['total_modules']}")
        print(f"Average Cohesion: {report['overall_quality_metrics'].get('average_cohesion', 0)}")
        print(f"Circular Dependencies Found: {len(report['circular_dependencies'])}")
        print(f"Refactoring Priorities: {len(report['refactoring_priorities'])}")