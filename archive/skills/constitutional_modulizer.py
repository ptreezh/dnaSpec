"""
DNASPEC Bottom-up Module Formation Skill
Implements constitutional requirement of gradual encapsulation of mature components
into modules as complexity grows through bottom-up aggregation approach.
"""
import re
import uuid
from datetime import datetime
from typing import Dict, Any, List, Tuple, Callable
from enum import Enum


class ComponentStatus(Enum):
    PROPOSED = "proposed"         # Newly identified component
    IN_PROGRESS = "in_progress"   # Work in progress
    TESTING = "testing"           # Under testing
    MATURE = "mature"             # Ready to be considered for grouping
    STABLE = "stable"             # Stable component


class ModuleFormationCriteria:
    """Criteria for forming modules from mature components"""
    
    def __init__(self):
        self.cohesion_threshold = 0.7  # Minimum cohesion to consider grouping
        self.maturity_score_threshold = 0.8  # Minimum maturity score
        self.dependency_density_threshold = 0.6  # How interconnected components should be
        self.min_components_per_module = 2  # Minimum components to form module
        self.max_components_per_module = 10  # Maximum components per module


class Component:
    """Represents a granular component (could be a task, function, class, etc.)"""
    
    def __init__(self, name: str, description: str = "", category: str = "utility"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.category = category  # group similar components
        self.status = ComponentStatus.PROPOSED
        self.dependencies = []  # other components this depends on
        self.dependents = []    # other components that depend on this
        self.cohesion_score = 0.0  # How cohesive this component is
        self.maturity_score = 0.0  # How mature this component is
        self.creation_date = datetime.now()
        self.last_activity = datetime.now()
        self.code_size = 0  # Lines of code or complexity measure
        self.test_coverage = 0.0  # Test coverage percentage
        self.documentation_complete = False
        self.code_reviewed = False
        
    def add_dependency(self, component_id: str):
        """Add dependency to another component"""
        if component_id not in self.dependencies:
            self.dependencies.append(component_id)
    
    def add_dependent(self, component_id: str):
        """Add dependent component"""
        if component_id not in self.dependents:
            self.dependents.append(component_id)
    
    def update_maturity(self, additional_score: float = 0.1):
        """Update maturity based on completion of work"""
        self.last_activity = datetime.now()
        self.maturity_score = min(1.0, self.maturity_score + additional_score)
        
        # Update status based on maturity
        if self.maturity_score >= 0.9:
            self.status = ComponentStatus.STABLE
        elif self.maturity_score >= 0.8:
            self.status = ComponentStatus.MATURE
        elif self.maturity_score >= 0.5:
            self.status = ComponentStatus.TESTING


class Module:
    """Represents a module that encapsulates related components"""
    
    def __init__(self, name: str, description: str = ""):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.components = []  # List of component IDs
        self.status = ComponentStatus.PROPOSED  # Same enum used for consistency
        self.total_cohesion_score = 0.0
        self.average_cohesion_score = 0.0
        self.coupling_score = 0.0  # How coupled this module is to others
        self.module_size = 0  # Number of components
        self.internal_dependencies = 0  # Dependencies within module
        self.external_dependencies = 0  # Dependencies on other modules
        self.encapsulation_ratio = 0.0  # Ratio of internal to total dependencies
        self.created_date = datetime.now()
        
    def add_component(self, component_id: str):
        """Add component to this module"""
        if component_id not in self.components:
            self.components.append(component_id)
            self.module_size = len(self.components)
    
    def calculate_encapsulation_metrics(self):
        """Calculate how well this module encapsulates its internals"""
        if self.module_size == 0:
            return
            
        # Calculate average cohesion of components in this module
        self.average_cohesion_score = self.total_cohesion_score / self.module_size if self.module_size > 0 else 0
        # Calculate encapsulation ratio
        total_deps = self.internal_dependencies + self.external_dependencies
        self.encapsulation_ratio = self.internal_dependencies / total_deps if total_deps > 0 else 1.0


class BottomUpModuleFormulator:
    """Implements constitutional requirement of gradual bottom-up module formation"""
    
    def __init__(self):
        self.criteria = ModuleFormationCriteria()
        self.components: Dict[str, Component] = {}
        self.modules: Dict[str, Module] = {}
        self.component_categories: Dict[str, List[str]] = {}
        
    def register_component(self, name: str, description: str = "", category: str = "utility") -> str:
        """Register a new component and return its ID"""
        component = Component(name, description, category)
        self.components[component.id] = component
        
        # Add to category index
        if category not in self.component_categories:
            self.component_categories[category] = []
        self.component_categories[category].append(component.id)
        
        return component.id
    
    def update_component_status(self, component_id: str, status: ComponentStatus, 
                              maturity_boost: float = 0.0) -> bool:
        """Update component status and maturity"""
        if component_id not in self.components:
            return False
            
        comp = self.components[component_id]
        comp.status = status
        if maturity_boost > 0:
            comp.update_maturity(maturity_boost)
            
        # If component becomes mature, consider it for module formation
        if comp.status in [ComponentStatus.MATURE, ComponentStatus.STABLE]:
            self._evaluate_module_formation_opportunities()
            
        return True
    
    def add_component_dependency(self, from_comp_id: str, to_comp_id: str) -> bool:
        """Add dependency relationship between components"""
        if from_comp_id in self.components and to_comp_id in self.components:
            from_comp = self.components[from_comp_id]
            to_comp = self.components[to_comp_id]
            
            from_comp.add_dependency(to_comp_id)
            to_comp.add_dependent(from_comp_id)
            return True
        return False
    
    def _find_related_mature_components(self) -> List[List[str]]:
        """Find clusters of related, mature components that could form modules"""
        # Group components by category first
        potential_groups = []
        
        for category, comp_ids in self.component_categories.items():
            # Find mature components in this category
            mature_comps = [
                comp_id for comp_id in comp_ids 
                if comp_id in self.components and 
                self.components[comp_id].status in [ComponentStatus.MATURE, ComponentStatus.STABLE] and
                self.components[comp_id].maturity_score >= self.criteria.maturity_score_threshold
            ]
            
            if len(mature_comps) >= self.criteria.min_components_per_module:
                # Further cluster based on dependencies
                clustered = self._cluster_by_dependencies(mature_comps)
                potential_groups.extend(clustered)
        
        return potential_groups
    
    def _cluster_by_dependencies(self, component_ids: List[str]) -> List[List[str]]:
        """Cluster components based on dependency density"""
        clusters = []
        unprocessed = set(component_ids)
        
        while unprocessed:
            seed = unprocessed.pop()
            cluster = [seed]
            
            # Find components highly connected to this seed
            for comp_id in list(unprocessed):
                connectivity = self._calculate_connectivity(seed, comp_id)
                if connectivity >= self.criteria.dependency_density_threshold:
                    cluster.append(comp_id)
                    unprocessed.remove(comp_id)
            
            # Only keep clusters that meet size requirements
            if len(cluster) >= self.criteria.min_components_per_module:
                clusters.append(cluster)
        
        return clusters
    
    def _calculate_connectivity(self, comp1_id: str, comp2_id: str) -> float:
        """Calculate connectivity between two components based on dependencies"""
        if comp1_id not in self.components or comp2_id not in self.components:
            return 0.0
        
        comp1 = self.components[comp1_id]
        comp2 = self.components[comp2_id]
        
        # Calculate bidirectional dependency score
        direct_connection = 0.0
        if comp2_id in comp1.dependencies or comp1_id in comp2.dependencies:
            direct_connection = 0.5
        
        # Check if they have common dependencies or dependents
        shared_deps = len(set(comp1.dependencies) & set(comp2.dependencies))
        shared_dependents = len(set(comp1.dependents) & set(comp2.dependents))
        
        shared_score = (shared_deps + shared_dependents) / max(len(comp1.dependencies + comp1.dependents), 
                                                              len(comp2.dependencies + comp2.dependents), 1)
        
        return min(1.0, direct_connection + shared_score * 0.5)
    
    def _evaluate_module_formation_opportunities(self):
        """Check if we have enough mature components to form new modules"""
        potential_groups = self._find_related_mature_components()
        
        for group in potential_groups:
            # Calculate collective metrics for the group
            total_maturity = 0
            total_cohesion = 0
            
            for comp_id in group:
                if comp_id in self.components:
                    component = self.components[comp_id]
                    total_maturity += component.maturity_score
                    total_cohesion += component.cohesion_score  # Assuming this is set by client
            
            avg_maturity = total_maturity / len(group) if group else 0
            avg_cohesion = total_cohesion / len(group) if group else 0
            
            # Check if this group meets module formation criteria
            if (avg_maturity >= self.criteria.maturity_score_threshold and 
                avg_cohesion >= self.criteria.cohesion_threshold and
                len(group) >= self.criteria.min_components_per_module and
                len(group) <= self.criteria.max_components_per_module):
                
                # Form a new module from this group
                module_name = self._generate_module_name(group)
                new_module = self._form_module_from_components(module_name, group)
                
                # Add module to system
                self.modules[new_module.id] = new_module
                
                # Update component statuses to reflect they're now in a module
                for comp_id in group:
                    if comp_id in self.components:
                        self.components[comp_id].status = ComponentStatus.STABLE
    
    def _generate_module_name(self, component_ids: List[str]) -> str:
        """Generate a meaningful name for the new module based on its components"""
        if not component_ids:
            return f"Module_{uuid.uuid4().hex[:8]}"
        
        # Take the first component's name as base, add a number if needed
        base_comp = self.components.get(component_ids[0])
        if base_comp:
            # Remove common words that don't add meaning
            base_name = base_comp.name.replace("function", "").replace("component", "").strip()
            base_name = re.sub(r'\s+', '_', base_name)
            if not base_name:
                base_name = "GenericModule"
            return f"{base_name}_Module"
        
        return f"Module_{uuid.uuid4().hex[:8]}"
    
    def _form_module_from_components(self, module_name: str, component_ids: List[str]) -> Module:
        """Form a new module from the given components"""
        # Create module description from component descriptions
        descriptions = [self.components[cid].description for cid in component_ids if cid in self.components]
        combined_description = ". ".join(descriptions[:3])  # First 3 descriptions
        
        module = Module(module_name, combined_description)
        
        # Add components and calculate metrics
        total_cohesion = 0
        for comp_id in component_ids:
            if comp_id in self.components:
                component = self.components[comp_id]
                module.add_component(comp_id)
                total_cohesion += component.cohesion_score
                module.total_cohesion_score = total_cohesion
        
        module.calculate_encapsulation_metrics()
        module.status = ComponentStatus.STABLE  # New modules start as stable
        
        return module
    
    def get_ready_modules(self) -> List[Dict[str, Any]]:
        """Get list of modules that are ready for use"""
        ready_modules = []
        for module_id, module in self.modules.items():
            ready_modules.append({
                'id': module.id,
                'name': module.name,
                'description': module.description,
                'component_count': module.module_size,
                'average_cohesion': module.average_cohesion_score,
                'encapsulation_ratio': module.encapsulation_ratio,
                'created_date': module.created_date.isoformat()
            })
        
        return ready_modules
    
    def get_formulation_insights(self) -> Dict[str, Any]:
        """Get insights about the module formulation process"""
        total_components = len(self.components)
        mature_components = len([c for c in self.components.values() 
                                if c.status in [ComponentStatus.MATURE, ComponentStatus.STABLE]])
        total_modules = len(self.modules)
        
        return {
            'total_components': total_components,
            'mature_components': mature_components,
            'total_modules': total_modules,
            'components_per_module_avg': total_components / total_modules if total_modules > 0 else 0,
            'module_formation_rate': total_modules / total_components if total_components > 0 else 0,
            'categories_identified': list(self.component_categories.keys())
        }


# Main interface for constitutional module formation
class ConstitutionalModuleSkill:
    """Module skill that implements constitutional requirements for bottom-up formation"""
    
    def __init__(self):
        self.formulator = BottomUpModuleFormulator()
        self.skill_name = "constitutnal-module-formulation"
        self.description = "Constitutional skill for bottom-up module formation based on mature component aggregation"
    
    def register_component(self, name: str, description: str = "", category: str = "utility") -> Dict[str, Any]:
        """Register a new component for potential future module inclusion"""
        comp_id = self.formulator.register_component(name, description, category)
        
        return {
            'success': True,
            'component_id': comp_id,
            'message': f'Component "{name}" registered and ready for maturity tracking'
        }
    
    def update_component_status(self, component_id: str, status: str, 
                               maturity_boost: float = 0.0) -> Dict[str, Any]:
        """Update component status and trigger module formation evaluation"""
        # Convert string status to enum
        status_enum = getattr(ComponentStatus, status.upper(), ComponentStatus.PROPOSED)
        
        success = self.formulator.update_component_status(component_id, status_enum, maturity_boost)
        
        return {
            'success': success,
            'message': f'Component {component_id} status updated to {status}',
            'triggered_evaluation': status in ['MATURE', 'STABLE']
        }
    
    def add_component_dependency(self, from_comp_id: str, to_comp_id: str) -> Dict[str, Any]:
        """Add dependency relationship between components"""
        success = self.formulator.add_component_dependency(from_comp_id, to_comp_id)
        
        return {
            'success': success,
            'message': f'Dependency from {from_comp_id} to {to_comp_id} {"added" if success else "failed to add"}'
        }
    
    def get_ready_modules(self) -> Dict[str, Any]:
        """Get modules that have been formed through bottom-up aggregation"""
        modules = self.formulator.get_ready_modules()
        
        return {
            'success': True,
            'modules_count': len(modules),
            'modules': modules
        }
    
    def get_formulation_insights(self) -> Dict[str, Any]:
        """Get insights about the bottom-up module formation process"""
        insights = self.formulator.get_formulation_insights()
        
        return {
            'success': True,
            'insights': insights
        }
    
    def evaluate_module_formation_opportunities(self) -> Dict[str, Any]:
        """Explicitly trigger evaluation of module formation opportunities"""
        self.formulator._evaluate_module_formation_opportunities()
        
        modules_after = len(self.formulator.modules)
        insights = self.formulator.get_formulation_insights()
        
        return {
            'success': True,
            'message': f'Module formation evaluation completed. Total modules: {modules_after}',
            'insights': insights
        }


# Example usage demonstrating constitutional compliance
def demonstrate_constitutional_module_formation():
    """Demonstrate bottom-up module formation according to constitutional principles"""
    
    print("🎯 Demonstrating Constitutional Module Formation...")
    print("   Principle: Gradually mature components are aggregated into modules as complexity grows\n")
    
    skill = ConstitutionalModuleSkill()
    
    # 1. Register individual components (finest granularity)
    print("1. Registering individual components (gradual refinement phase):")
    comp1_id = skill.register_component("user_auth_handler", 
                                       "Handles user authentication requests", 
                                       "security")['component_id']
    comp2_id = skill.register_component("session_manager", 
                                       "Manages user sessions", 
                                       "security")['component_id']
    comp3_id = skill.register_component("jwt_token_generator", 
                                       "Generates JWT tokens", 
                                       "security")['component_id']
    comp4_id = skill.register_component("password_hasher", 
                                       "Hashes user passwords", 
                                       "security")['component_id']
                                       
    comp5_id = skill.register_component("user_profile_service", 
                                       "Manages user profile data", 
                                       "data")['component_id']
    comp6_id = skill.register_component("user_preferences_service", 
                                       "Handles user preferences", 
                                       "data")['component_id']
    comp7_id = skill.register_component("user_data_validator", 
                                       "Validates user data", 
                                       "data")['component_id']
    
    print(f"   - Registered {comp1_id[:8]}...: user_auth_handler")
    print(f"   - Registered {comp2_id[:8]}...: session_manager") 
    print(f"   - Registered {comp3_id[:8]}...: jwt_token_generator")
    print(f"   - Registered {comp4_id[:8]}...: password_hasher")
    print(f"   - Registered {comp5_id[:8]}...: user_profile_service")
    print(f"   - Registered {comp6_id[:8]}...: user_preferences_service")
    print(f"   - Registered {comp7_id[:8]}...: user_data_validator")
    
    # 2. Establish dependencies between components
    print("\n2. Establishing component dependencies:")
    skill.add_component_dependency(comp1_id, comp2_id)  # auth needs session
    skill.add_component_dependency(comp1_id, comp3_id)  # auth needs token gen
    skill.add_component_dependency(comp1_id, comp4_id)  # auth needs password hash
    skill.add_component_dependency(comp5_id, comp7_id)  # profile needs validation
    skill.add_component_dependency(comp6_id, comp7_id)  # preferences need validation
    
    print("   - Set up dependencies between related components")
    
    # 3. Mark components as mature (simulating completion)
    print("\n3. Marking components as mature (complexity now justifies grouping):")
    skill.update_component_status(comp1_id, "MATURE", 0.3)
    skill.update_component_status(comp2_id, "MATURE", 0.3)
    skill.update_component_status(comp3_id, "MATURE", 0.3)
    skill.update_component_status(comp4_id, "MATURE", 0.3)
    
    skill.update_component_status(comp5_id, "MATURE", 0.3)
    skill.update_component_status(comp6_id, "MATURE", 0.3)
    skill.update_component_status(comp7_id, "MATURE", 0.3)
    
    print("   - Marked security components as mature")
    print("   - Marked data components as mature")
    
    # 4. Evaluate and form modules (bottom-up aggregation)
    print("\n4. Evaluating module formation opportunities (bottom-up encapsulation):")
    result = skill.evaluate_module_formation_opportunities()
    print(f"   - {result['insights']['modules_count']} modules formed from mature components")
    
    # 5. Show the resulting modules
    print("\n5. Resulting modules (complexity reduced through encapsulation):")
    modules_result = skill.get_ready_modules()
    
    for module in modules_result['modules']:
        print(f"   - Module: {module['name']}")
        print(f"     Components: {module['component_count']}")
        print(f"     Avg Cohesion: {module['average_cohesion']:.2f}")
        print(f"     Encapsulation: {module['encapsulation_ratio']:.2f}")
    
    print(f"\n✅ Constitutional Module Formation Complete!")
    print(f"   - Started with {result['insights']['total_components']} individual components")
    print(f"   - Ended with {result['insights']['total_modules']} encapsulated modules")
    print(f"   - Reduced complexity through bottom-up aggregation")
    print(f"   - Mature components grouped based on relationships and categories")


if __name__ == "__main__":
    demonstrate_constitutional_module_formation()