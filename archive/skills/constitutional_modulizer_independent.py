"""
Constitutional Module Formation Skill - Execution Interface
Implements the constitutional requirement of bottom-up module formation from mature components
"""
from typing import Dict, Any
from .constitutional_modulizer import ConstitutionalModuleSkill


# Global instance to maintain state across calls
_constitutional_skill = ConstitutionalModuleSkill()


def execute_constitutional_module_formation(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute constitutional module formation skill
    
    Args:
        args: Dictionary containing:
            - operation: String specifying the operation to perform
            - component_name: Component name (for register_component)
            - component_description: Component description (for register_component)
            - component_category: Component category (for register_component)
            - component_id: Component ID (for other operations)
            - status: Component status (for update_component_status)
            - maturity_boost: Maturity boost amount (for update_component_status)
            - from_component_id: Source component ID (for add_dependency)
            - to_component_id: Target component ID (for add_dependency)
    
    Returns:
        Dictionary with execution result
    """
    operation = args.get('operation', '').lower()
    
    try:
        if operation == 'register_component':
            name = args.get('component_name', '')
            description = args.get('component_description', '')
            category = args.get('component_category', 'utility')
            
            if not name:
                return {
                    'success': False,
                    'error': 'Component name is required for registration'
                }
                
            return _constitutional_skill.register_component(name, description, category)
        
        elif operation == 'update_component_status':
            component_id = args.get('component_id', '')
            status = args.get('status', 'PROPOSED')
            maturity_boost = float(args.get('maturity_boost', 0.0))
            
            if not component_id:
                return {
                    'success': False,
                    'error': 'Component ID is required to update status'
                }
                
            return _constitutional_skill.update_component_status(component_id, status, maturity_boost)
        
        elif operation == 'add_component_dependency':
            from_comp_id = args.get('from_component_id', '')
            to_comp_id = args.get('to_component_id', '')
            
            if not from_comp_id or not to_comp_id:
                return {
                    'success': False,
                    'error': 'Both from_component_id and to_component_id are required'
                }
                
            return _constitutional_skill.add_component_dependency(from_comp_id, to_comp_id)
        
        elif operation == 'get_ready_modules':
            return _constitutional_skill.get_ready_modules()
        
        elif operation == 'evaluate_module_formation':
            return _constitutional_skill.evaluate_module_formation_opportunities()
        
        elif operation == 'get_formulation_insights':
            return _constitutional_skill.get_formulation_insights()
        
        else:
            return {
                'success': False,
                'error': f'Unknown operation: {operation}',
                'supported_operations': [
                    'register_component',
                    'update_component_status', 
                    'add_component_dependency',
                    'get_ready_modules',
                    'evaluate_module_formation',
                    'get_formulation_insights'
                ]
            }
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Execution error: {str(e)}'
        }


def get_constitutional_module_formation_info() -> Dict[str, str]:
    """Get information about the constitutional module formation skill"""
    return {
        'name': 'constitutional-module-formation',
        'description': 'Constitutional skill for bottom-up module formation based on mature component aggregation',
        'purpose': 'Implements constitutional requirement of gradual encapsulation of mature components into modules as complexity grows',
        'operations': [
            'register_component: Register new component for tracking',
            'update_component_status: Update component maturity status',
            'add_component_dependency: Establish component relationships',
            'get_ready_modules: Retrieve formed modules',
            'evaluate_module_formation: Trigger module formation evaluation',
            'get_formulation_insights: Get process metrics'
        ]
    }