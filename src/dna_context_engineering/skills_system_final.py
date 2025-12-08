"""
DNASPEC Context Engineering Skills - 英文版实现
所有输出使用英文和ANSI字符
"""
import json
import re
from typing import Dict, Any
from src.dna_spec_kit_integration.core.skill import DNASpecSkill, SkillResult, SkillStatus


def simulate_ai_completion(instruction: str) -> str:
    """
    模拟AI模型完成度函数（真实实现中会调用AI API）
    """
    import re
    
    if "分析" in instruction or "评估" in instruction or "quality" in instruction.lower():
        # 提取上下文内容 (English version)
        context_match = re.search(r'"([^"]+)"', instruction)
        if context_match:
            context_text = context_match.group(1)
        else:
            context_text = "Test context content"

        # 计算指标 (English version)
        clarity = min(1.0, max(0.0, 0.5 + len(context_text) * 0.0001))
        relevance = min(1.0, max(0.0, 0.7 + (0.1 if any(kw in context_text.lower() for kw in ['system', 'function', 'task', 'requirement', '需求', 'system', 'function', 'task']) else 0)))
        completeness = min(1.0, max(0.0, 0.3 + (0.3 if any(kw in context_text.lower() for kw in ['constraint', 'requirement', 'goal', 'requirement', 'constraint', 'requirement', 'goal']) else 0)))
        consistency = min(1.0, max(0.0, 0.8 - (0.2 if any(kw in context_text.lower() for kw in ['but', 'however', '但是', '然而']) else 0)))
        efficiency = min(1.0, max(0.0, 1.0 - len(context_text) * 0.00005))

        result_data = {
            "context_length": len(context_text),
            "token_count_estimate": max(1, len(context_text) // 4),
            "metrics": {
                "clarity": round(clarity, 2),
                "relevance": round(relevance, 2),
                "completeness": round(completeness, 2),
                "consistency": round(consistency, 2),
                "efficiency": round(efficiency, 2)
            },
            "suggestions": [
                "Add more specific goal descriptions",
                "Supplement constraint conditions and specific requirements",
                "Improve expression clarity"
            ],
            "issues": [i for i in [
                "Lack of explicit constraint conditions" if completeness < 0.6 else "",
                "Some expressions can be more precise" if clarity < 0.7 else ""
            ] if i],  # Filter out empty issues
            "confidence": 0.85
        }

        return json.dumps(result_data, ensure_ascii=False)

    elif "优化" in instruction or "改进" in instruction or "提升" in instruction or "optimize" in instruction.lower():
        # 提取原始上下文 (English version)
        context_extracted = instruction.split('"')[1] if '"' in instruction else "Content to optimize"
        original_context = context_extracted

        # 提取优化目标 (English version)
        goals_text = "clarity,completeness"
        for line in instruction.split('\n'):
            if '目标:' in line or '优化目标:' in line or 'goal:' in line.lower() or 'optimize' in line.lower():
                goals_match = re.search(r'[:：]\s*(.+)', line)
                if goals_match:
                    goals_text = goals_match.group(1).strip()
                break

        goals = [g.strip() for g in goals_text.split(',') if g.strip()]

        optimized_context = original_context
        applied_optimizations = []

        if any(goal in goals_text.lower() for goal in ['clarity', '清晰度', 'clarity']):
            optimized_context += "\n\nPlease clearly specify goals and constraints."
            applied_optimizations.append("Improve expression clarity")

        if any(goal in goals_text.lower() for goal in ['completeness', '完整性', 'completeness']):
            optimized_context += "\n\nConstraint: Need to complete within specified time\nClear goal: Implement expected functionality\nPrerequisite: Have necessary resource support"
            applied_optimizations.append("Supplement completeness elements")

        result_data = {
            "original_context": original_context,
            "optimized_context": optimized_context,
            "applied_optimizations": applied_optimizations,
            "improvement_metrics": {
                "clarity": 0.2 if any(goal in goals_text.lower() for goal in ['clarity', 'clear', '清晰度']) else 0.0,
                "relevance": 0.15 if any(goal in goals_text.lower() for goal in ['relevance', 'relevant', '相关性']) else 0.0,
                "completeness": 0.3 if any(goal in goals_text.lower() for goal in ['completeness', 'complete', '完整性']) else 0.0,
                "conciseness": -0.1 if any(goal in goals_text.lower() for goal in ['conciseness', 'concise', '简洁性']) else 0.0
            },
            "optimization_summary": f"Optimized according to goals: {', '.join(goals)}"
        }

        return json.dumps(result_data, ensure_ascii=False)

    else:
        # Default return
        result_data = {
            "enhanced_content": f"AI processed instruction: {instruction[:50]}...",
            "success": True
        }
        return json.dumps(result_data, ensure_ascii=False)


class ContextAnalysisSkill(DNASpecSkill):
    """Context Analysis Skill - Use AI model native intelligence for analysis"""

    def __init__(self):
        super().__init__(
            name="dnaspec-context-analysis",
            description="Context Analysis Skill - Use AI model native intelligence for professional context quality analysis"
        )

    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """Execute context analysis - through AI model native intelligence"""
        if not request.strip():
            return {
                'success': False,
                'error': 'Context cannot be empty',
                'result': {}
            }

        analysis_instruction = f"""
As a professional context quality analyst, please evaluate the following context across five dimensions:

Context: "{request}"

Metrics (0.0-1.0 scoring):
1. Clarity: Expression clarity
2. Relevance: Task relevance
3. Completeness: Information completeness
4. Consistency: Logical consistency
5. Efficiency: Information density

Return analysis result in JSON format.
"""

        try:
            # Use simulated AI completion function
            simulation_result = simulate_ai_completion(analysis_instruction)
            parsed_result = json.loads(simulation_result)

            return {
                'success': True,
                'result': parsed_result
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'AI analysis failed: {str(e)}',
                'result': {}
            }

    def _calculate_confidence(self, request: str) -> float:
        """Calculate confidence"""
        if len(request) < 5:
            return 0.3  # Low confidence for too short input
        else:
            return 0.8


class ContextOptimizationSkill(DNASpecSkill):
    """Context Optimization Skill - Use AI model native intelligence for optimization"""

    def __init__(self):
        super().__init__(
            name="dnaspec-context-optimization",
            description="Context Optimization Skill - Use AI model native intelligence to optimize context quality"
        )

    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """Execute context optimization - through AI model native intelligence"""
        if not request.strip():
            return {
                'success': False,
                'error': 'Context cannot be empty',
                'result': {}
            }

        # Get optimization goals
        params = context or {}
        goals = params.get('optimization_goals', ['clarity', 'completeness'])
        if isinstance(goals, str):
            goals = [g.strip() for g in goals.split(',') if g.strip()]

        optimization_instruction = f"""
Optimize the context based on the following goals:

Optimization goals: {', '.join(goals)}

Original context: "{request}"

Please return optimized content and applied optimization measures in JSON format.
"""

        try:
            # Use simulated AI completion function
            simulation_result = simulate_ai_completion(optimization_instruction)
            parsed_result = json.loads(simulation_result)

            return {
                'success': True,
                'result': parsed_result
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'AI optimization failed: {str(e)}',
                'result': {}
            }

    def _calculate_confidence(self, request: str) -> float:
        """Calculate confidence"""
        if len(request) < 5:
            return 0.4  # Low confidence for short input
        else:
            return 0.75


class CognitiveTemplateSkill(DNASpecSkill):
    """Cognitive Template Skill - Use AI model native intelligence to apply cognitive templates"""

    def __init__(self):
        super().__init__(
            name="dnaspec-cognitive-template",
            description="Cognitive Template Skill - Use AI model native intelligence to apply cognitive templates to structure complex tasks"
        )

        self.templates = {
            'chain_of_thought': 'Chain-of-Thought Reasoning Template',
            'few_shot': 'Few-Shot Learning Template',
            'verification': 'Verification Check Template',
            'role_playing': 'Role-Playing Template',
            'understanding': 'Deep Understanding Template'
        }

    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """Execute cognitive template application - through AI model native intelligence"""
        if not request.strip():
            return {
                'success': False,
                'error': 'Context cannot be empty',
                'result': {'success': False}
            }

        params = context or {}
        template_type = params.get('template', 'chain_of_thought')

        if template_type not in self.templates:
            return {
                'success': False,
                'error': f'Unknown template: {template_type}',
                'available_templates': list(self.templates.keys()),
                'result': {'success': False}
            }

        template_desc = self.templates[template_type]

        if template_type == 'chain_of_thought':
            template_instruction = f"""
Using chain-of-thought method to analyze the following task:

Task: {request}

Analyze in following steps:
1. Problem Understanding
2. Step Decomposition
3. Intermediate Reasoning
4. Verification Check
5. Final Answer

Return structured analysis.
"""
        elif template_type == 'verification':
            template_instruction = f"""
Using verification framework to analyze the following content:

Original content: {request}

Perform verification:
1. Preliminary Answer
2. Logical Consistency Check
3. Fact Accuracy Check
4. Completeness Check
5. Final Confirmation

Return verification result.
"""
        else:
            # Default use chain-of-thought
            template_instruction = f"""
Using {template_desc} to analyze task: {request}

Return structured result.
"""

        try:
            # Construct template application result
            enhanced_content = f"""
### {template_type} Cognitive Template Application

**Original Task**: {request}

**Structured Analysis**:
[AI model will apply {template_desc} for professional analysis...]

**Professional Result**:
[Return results based on {template_desc} professional framework]

**Confidence Level**: 0.85
"""

            return {
                'success': True,
                'result': {
                    'success': True,
                    'template_type': template_type,
                    'template_description': template_desc,
                    'original_context': request,
                    'enhanced_context': enhanced_content,
                    'template_structure': ['Apply Cognitive Framework', 'Structure Output', 'Verify Results'],
                    'confidence': 0.85
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Template application failed: {str(e)}',
                'result': {'success': False}
            }

    def _calculate_confidence(self, request: str) -> float:
        """Calculate confidence"""
        if len(request) < 5:
            return 0.35
        else:
            return 0.85


def execute(args: Dict[str, Any]) -> str:
    """
    Execute function - Interface integrated with AI CLI platforms
    """
    import json
    from src.dna_spec_kit_integration.core.skill import SkillResult, SkillStatus
    
    skill_name = args.get('skill', 'context-analysis')
    context_input = args.get('context', '') or args.get('request', '')
    params = args.get('params', {})

    if not context_input:
        return "Error: Context to process was not provided"

    try:
        if skill_name == 'context-analysis':
            skill = ContextAnalysisSkill()
            result = skill.process_request(context_input, params)

            if result.status.name == 'COMPLETED':
                analysis = result.result
                if 'result' in analysis:
                    analysis_data = analysis['result']
                else:
                    analysis_data = analysis

                output_lines = []
                output_lines.append("Context Quality Analysis Results:")
                output_lines.append(f"Length: {analysis_data['context_length']} characters")
                output_lines.append(f"Token Estimate: {analysis_data['token_count_estimate']}")
                output_lines.append("")

                output_lines.append("Five-Dimensional Quality Metrics (0.0-1.0):")
                metric_names = {
                    'clarity': 'Clarity', 'relevance': 'Relevance', 'completeness': 'Completeness',
                    'consistency': 'Consistency', 'efficiency': 'Efficiency'
                }

                for metric, score in analysis_data['metrics'].items():
                    indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
                    output_lines.append(f"  {indicator} {metric_names.get(metric, metric)}: {score:.2f}")

                if analysis_data.get('suggestions'):
                    output_lines.append("\nOptimization Suggestions:")
                    for s in analysis_data['suggestions'][:3]:  # Show top 3 suggestions
                        output_lines.append(f"  • {s}")

                if analysis_data.get('issues'):
                    output_lines.append("\nIdentified Issues:")
                    for i in analysis_data['issues']:
                        output_lines.append(f"  • {i}")

                return "\n".join(output_lines)
            else:
                return f"Error: {result.error_message}"

        elif skill_name == 'context-optimization':
            skill = ContextOptimizationSkill()
            result = skill.process_request(context_input, params)

            if result.status.name == 'COMPLETED':
                optimization = result.result
                if 'result' in optimization:
                    optimization_data = optimization['result']
                else:
                    optimization_data = optimization

                output_lines = []
                output_lines.append("Context Optimization Results:")
                output_lines.append(f"Original Length: {len(optimization_data['original_context'])} characters")
                output_lines.append(f"Optimized Length: {len(optimization_data['optimized_context'])} characters")
                output_lines.append("")

                output_lines.append("Applied Optimizations:")
                for opt in optimization_data['applied_optimizations']:
                    output_lines.append(f"  • {opt}")

                output_lines.append("\nImprovement Metrics:")
                for metric, change in optimization_data['improvement_metrics'].items():
                    if change != 0:  # Only show metrics with changes
                        direction = "↗️" if change > 0 else "↘️" if change < 0 else "➡️"
                        output_lines.append(f"  {direction} {metric}: {change:+.2f}")

                output_lines.append("\nOptimized Context:")
                output_lines.append(optimization_data['optimized_context'])

                return "\n".join(output_lines)
            else:
                return f"Error: {result.error_message}"

        elif skill_name == 'cognitive-template':
            skill = CognitiveTemplateSkill()
            result = skill.process_request(context_input, params)

            if result.status.name == 'COMPLETED' and result.result['result']['success']:
                template_result = result.result['result']
                output_lines = []
                output_lines.append(f"Cognitive Template Application: {template_result['template_type']} ({template_result['template_description']})")
                output_lines.append("="*60)
                output_lines.append("")
                output_lines.append("Structured Output:")
                output_lines.append(template_result['enhanced_context'])

                return "\n".join(output_lines)
            else:
                error_msg = result.result['result'].get('error', 'Template application failed') if result.status.name == 'COMPLETED' else result.error_message
                return f"Error: {error_msg}"

        else:
            available_skills = ['context-analysis', 'context-optimization', 'cognitive-template']
            return f"Error: Unknown skill '{skill_name}'. Available skills: {', '.join(available_skills)}"

    except Exception as e:
        return f"Error: Execution exception occurred - {str(e)}"


def get_available_skills() -> Dict[str, str]:
    """Get available skills list"""
    return {
        'context-analysis': 'Context Quality Five-Dimensional Professional Analysis',
        'context-optimization': 'AI-Driven Context Quality Enhancement',
        'cognitive-template': 'Cognitive Template for Structuring Complex Tasks'
    }


# Additional advanced functionality

def create_agent_for_context_analysis(goals: str, constraints: str) -> str:
    """
    Create intelligent agent with context analysis capabilities
    """
    agent_specification = f"""
Intelligent Agent Creation Specification:

Goals: {goals}
Constraints: {constraints}

Capability Requirements:
- Context Quality Analysis
- Task Decomposition Capability
- Solution Optimization Capability
- Risk Identification Capability
- Execution Monitoring Capability

Behavior Guidelines:
- Maintain context consistency
- Follow constraint conditions
- Optimize execution efficiency
- Report execution status
- Ensure goal achievement
    """
    return agent_specification


def decompose_complex_task(task_description: str) -> dict:
    """
    Decompose complex task into executable subtasks
    """
    import re
    
    # Extract key elements from task description
    entities = re.findall(r'([A-Za-z0-9_\u4e00-\u9fff]+)([包含|包括|需要|require|need|包含|包括|需要])', task_description)
    dependencies = []
    
    # Simple decomposition logic (actual would be more complex)
    if 'system' in task_description.lower() or '系统' in task_description:
        subtasks = [
            f'Analyze {task_description} requirements',
            f'Design {task_description} architecture',
            f'Implement {task_description} functionality',
            f'Test {task_description} results'
        ]
    else:
        subtasks = [f'Decompose task: {task_description}']

    return {
        'original_task': task_description,
        'subtasks': subtasks,
        'dependencies': dependencies,
        'estimated_duration': f"{len(subtasks) * 2} hours",
        'required_skills': ['Analysis', 'Design', 'Development', 'Testing']
    }


def design_project_structure(requirements: str) -> dict:
    """
    Project structure design
    """
    structure = {
        'recommended': {
            'src': {
                'main.py': 'Main application entry point',
                'models/': 'Data models',
                'services/': 'Business services',
                'utils/': 'Utility functions',
                'tests/': 'Test code'
            },
            'docs/': 'Documentation',
            'config/': 'Configuration files',
            'data/': 'Data files'
        },
        'patterns': ['MVC', 'Layered Architecture', 'Dependency Injection'],
        'best_practices': [
            'Single Responsibility Principle',
            'Open/Closed Principle',
            'Dependency Inversion Principle'
        ]
    }
    return structure


def generate_constraints_from_requirements(requirements: str) -> dict:
    """
    Generate system constraints from requirements
    """
    constraints = {
        'functional': [],
        'non_functional': {
            'performance': 'Response time < 2 seconds',
            'security': 'Data encryption in transit',
            'scalability': 'Support 1000 concurrent users',
            'reliability': 'System availability > 99.9%'
        },
        'architectural': [
            'No direct database access',
            'Layered architecture constraints',
            'API version control'
        ],
        'business': []
    }
    
    # Dynamically generate specific constraints based on requirements
    if 'real-time' in requirements.lower():
        constraints['non_functional']['performance'] = 'Response time < 100 milliseconds'
    
    return constraints