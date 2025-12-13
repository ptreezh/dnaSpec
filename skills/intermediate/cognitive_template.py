"""
Cognitive Template Skill - Refactored Version
Compliant with DNASPEC Standardized Skill Interface Specification
"""
from typing import Dict, Any
from ..skill_base import BaseSkill, DetailLevel


class CognitiveTemplateSkill(BaseSkill):
    """Cognitive Template Skill - Uses AI model's native intelligence to apply cognitive templates"""

    def __init__(self):
        super().__init__(
            name="cognitive-template",
            description="Uses AI model's native intelligence to apply cognitive templates to structure complex tasks"
        )

        self.templates = {
            'chain_of_thought': 'Chain of Thought Template',
            'few_shot': 'Few-shot Learning Template',
            'verification': 'Verification Check Template',
            'role_playing': 'Role-playing Template',
            'understanding': 'Deep Understanding Template'
        }
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel,
                          options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute cognitive template application logic"""
        if not input_text.strip():
            return {
                'success': False,
                'error': 'Context cannot be empty',
                'original_context': input_text
            }

        template_type = options.get('template', 'chain_of_thought')
        role = options.get('role', 'Expert')

        if template_type not in self.templates:
            return {
                'success': False,
                'error': f'Unknown template: {template_type}',
                'available_templates': list(self.templates.keys()),
                'original_context': input_text
            }

        template_desc = self.templates[template_type]

        if template_type == 'chain_of_thought':
            # Construct chain of thought template application result
            enhanced_content = f"""
### Chain of Thought Cognitive Template Application

**Original Task**: {input_text}

Please analyze this task in detail following these chain of thought steps:

1. **Problem Understanding**:
   - Clarify the core requirements of the task
   - Identify key constraints and limitations
   - Determine success criteria

2. **Step Decomposition**:
   - Break the task into executable sub-steps
   - Determine dependencies between steps
   - Assess time and resource requirements for each step

3. **Intermediate Reasoning**:
   - Perform detailed reasoning for each sub-step
   - Consider different implementation approaches
   - Evaluate pros and cons of each approach

4. **Verification Check**:
   - Check logical consistency of the reasoning process
   - Verify feasibility of the approach
   - Identify potential risks and challenges

5. **Final Answer**:
   - Provide the final solution integrating all analysis
   - Offer clear implementation recommendations
   - Determine priorities and milestones

Please return the complete analysis process and final conclusion.
"""
            template_structure = [
                "Apply cognitive framework",
                "Structured output",
                "Verify results"
            ]
        
        elif template_type == 'few_shot':
            enhanced_content = f"""
### Few-shot Learning Template Application

**Task**: {input_text}

The following are example pairs for handling similar tasks, used to guide model behavior:

**Example 1**:
Input: Analyze e-commerce platform architecture requirements
Output:
- Identify core components: user management, product management, order management, payment system
- Analyze technology stack: frontend, backend, database, cache
- Determine interaction patterns: REST API, message queue, event-driven
- Verify security requirements: authentication, authorization, data encryption

**Example 2**:
Input: Design API interface specification
Output:
- Define data model: entity structure, relationships, constraints
- Standardize interface definition: endpoints, parameters, response format
- Configure error handling: error codes, messages, recovery strategies
- Optimize performance considerations: pagination, caching, throttling

Please refer to the above example patterns to handle your task: {input_text}

Please provide detailed analysis process, decision basis, and final solution.
"""
            template_structure = [
                "Provide example pairs",
                "Pattern recognition",
                "Apply examples"
            ]

        elif template_type == 'verification':
            enhanced_content = f"""
### Verification Check Template Application

**Content to Verify**: {input_text}

Please execute the following verification steps to ensure quality:

1. **Initial Answer**:
   Give an initial judgment or approach based on the content to verify: [Empty]

2. **Logical Consistency Check**:
   - Verify internal logical consistency and coherence of content
   - Check if there are contradictory or conflicting information
   - Confirm reasonableness of causal relationships

3. **Factual Accuracy Check**:
   - Verify accuracy of stated facts
   - Validate feasibility of technical requirements
   - Check reasonableness of constraints

4. **Completeness Check**:
   - Assess if all necessary information is included
   - Confirm if key elements are complete
   - Check coverage of edge cases

5. **Final Confirmation**:
   Based on the above checks, provide final verification conclusion: [Empty]

Please return detailed results for each verification step and final confirmation.
"""
            template_structure = [
                "Initial verification",
                "Multi-dimensional check",
                "Final confirmation"
            ]

        elif template_type == 'role_playing':
            enhanced_content = f"""
### {role} Role-playing Analysis

**Task**: {input_text}

Please analyze this task from the professional identity and perspective of {role}:

1. **Role Professional Capability Identification**:
   As {role}, I possess the following professional capabilities:
   - [Professional skill 1]
   - [Professional skill 2]
   - [Professional skill 3]

2. **Professional Perspective Analysis**:
   Analyze key elements of the task from {role}'s professional perspective:
   - Core focus points
   - Potential challenges
   - Best practice methods

3. **Professional Recommendation Formulation**:
   Provide specific and feasible recommendations based on {role}'s professional knowledge:
   - [Recommendation 1: Specific operation]
   - [Recommendation 2: Considerations]
   - [Recommendation 3: Success points]

4. **Professional Decision Recommendation**:
   Make optimal decision recommendations from {role}'s professional perspective and explain the reasoning.

Please return professional analysis, recommendations, and decisions from {role}'s perspective.
"""
            template_structure = [
                "Role capability identification",
                "Professional perspective analysis",
                "Recommendation formulation",
                "Decision recommendation"
            ]

        elif template_type == 'understanding':
            enhanced_content = f"""
### Deep Understanding Framework

**Content to Understand**: {input_text}

Please perform deep understanding from the following dimensions:

1. **Core Objective**:
   - What is the primary objective of this content?
   - What results are expected to be achieved?
   - How is success defined?

2. **Key Elements**:
   - What important components does it contain?
   - What key technologies/concepts are involved?
   - Who are the main participants?

3. **Constraint Conditions**:
   - What limitations and constraints exist?
   - What are the prerequisites and assumptions?
   - What are the resource and time constraints?

4. **Success Criteria**:
   - How to judge if the task is completed well?
   - What are the quality measurement indicators?
   - What are the user satisfaction standards?

5. **Potential Risks**:
   - What challenges may be faced?
   - What risk factors exist?
   - How to prevent and mitigate?

Please return deep understanding results and related recommendations.
"""
            template_structure = [
                "Objective understanding",
                "Element analysis",
                "Constraint identification",
                "Standard definition",
                "Risk assessment"
            ]

        return {
            'success': True,
            'original_context': input_text,
            'enhanced_context': enhanced_content,
            'template_type': template_type,
            'template_description': template_desc,
            'template_structure': template_structure
        }

    def _format_output(self, result_data: Dict[str, Any], detail_level: DetailLevel) -> Dict[str, Any]:
        """Format output result based on detail level"""
        if detail_level == DetailLevel.BASIC:
            # Basic level returns only core information
            if result_data.get('success', False):
                return {
                    'template_type': result_data['template_type'],
                    'enhanced_context': result_data['enhanced_context'][:200] + "..." if len(result_data['enhanced_context']) > 200 else result_data['enhanced_context']
                }
            else:
                return result_data
        elif detail_level == DetailLevel.STANDARD:
            # Standard level returns standard information
            return result_data
        else:  # DETAILED
            # Detailed level returns complete information
            if result_data.get('success', False):
                detailed_info = {
                    'processing_details': {
                        'template_matched': result_data['template_type'],
                        'template_description': result_data['template_description'],
                        'structure_steps': result_data['template_structure'],
                        'context_length': len(result_data['original_context'])
                    }
                }
                result_data.update(detailed_info)
            return result_data