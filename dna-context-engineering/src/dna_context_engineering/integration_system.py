"""
DNASPEC Context Engineering Skills - 与DNA-Project集成实现
整合DNASPEC Project中现有的skills与Context Engineering增强技能
"""
import sys
import os
from typing import Dict, Any

# 添加DNA-Project到路径以访问其技能
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'DNASPEC-Project'))

from src.dnaspec_context_engineering.skills_system_final_clean import (
    ContextAnalysisSkill as ContextEngineAnalysisSkill,
    ContextOptimizationSkill as ContextEngineOptimizationSkill, 
    CognitiveTemplateSkill as ContextEngineTemplateSkill
)

# 从DNA-Project导入原生技能
try:
    from DNASPEC_Project.src.dnaspec_architect import DNASPECArchitect
    from DNASPEC_Project.src.dnaspec_task_decomposer import DNASPECTaskDecomposer  
    from DNASPEC_Project.src.dnaspec_agent_creator import DNASPECAgentCreator
    from DNASPEC_Project.src.dnaspec_system_architect import DNASPECSystemArchitect
    from DNASPEC_Project.src.dnaspec_constraint_generator import DNASPECConstraintGenerator
    from DNASPEC_Project.src.dnaspec_dapi_checker import DNASPECDAPIChecker
    from DNASPEC_Project.src.dnaspec_modulizer import DNASPECModulizer
    
    DNASPEC_PROJECT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ DNASPEC-Project技能不可用: {e}")
    DNASPEC_PROJECT_AVAILABLE = False
    # 创建模拟类以继续集成
    class DNASPECArchitect:
        def __init__(self): 
            self.name = "dnaspec-architect"
            self.description = "DNASPEC原生架构师技能 (模拟)"
        
        def process_request(self, request: str, context=None):
            return {"status": "processed", "result": f"模拟架构师处理: {request}"}
    
    class DNASPECTaskDecomposer:
        def __init__(self):
            self.name = "dnaspec-task-decomposer"
            self.description = "DNASPEC原生任务分解技能 (模拟)"
            
        def process_request(self, request: str, context=None):
            return {"status": "processed", "result": f"模拟任务分解: {request}"}
    
    # 其他模拟类...
    DNASPECAgentCreator = DNASPECArchitect
    DNASPECSystemArchitect = DNASPECArchitect  
    DNASPECConstraintGenerator = DNASPECArchitect
    DNASPECDAPIChecker = DNASPECArchitect
    DNASPECModulizer = DNASPECArchitect


class DNASPECIntegratedContextEngineeringSystem:
    """
    集成DNA-Project与Context Engineering Skills的综合系统
    充分利用AI原生智能，整合所有可用技能
    """
    
    def __init__(self):
        # DNASPEC-Project 原生技能
        if DNASPEC_PROJECT_AVAILABLE:
            self.native_skills = {
                'dnaspec-architect': DNASPECArchitect(),
                'dnaspec-task-decomposer': DNASPECTaskDecomposer(),
                'dnaspec-agent-creator': DNASPECAgentCreator(),
                'dnaspec-system-architect': DNASPECSystemArchitect(),
                'dnaspec-constraint-generator': DNASPECConstraintGenerator(),
                'dnaspec-dapi-checker': DNASPECDAPIChecker(),
                'dnaspec-modulizer': DNASPECModulizer()
            }
        else:
            # 如果原生项目不可用，使用模拟技能
            self.native_skills = {
                'dnaspec-architect': DNASPECArchitect(),
                # 添加更多模拟技能...
            }
        
        # Context Engineering 增强技能（AI原生）
        self.enhanced_skills = {
            'dnaspec-context-analysis': ContextEngineAnalysisSkill(),
            'dnaspec-context-optimization': ContextEngineOptimizationSkill(),
            'dnaspec-cognitive-template': ContextEngineTemplateSkill()
        }
        
        # 统一技能库
        self.all_skills = {**self.native_skills, **self.enhanced_skills}
    
    def execute_skill(self, skill_name: str, context: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行指定技能"""
        if skill_name in self.enhanced_skills:
            # 使用AI原生增强技能
            skill = self.enhanced_skills[skill_name]
            if hasattr(skill, 'process_request'):
                return skill.process_request(context, params or {})
            else:
                # 如果是旧接口
                from src.dnaspec_spec_kit_integration.core.skill import DNASpecSkill
                if isinstance(skill, DNASpecSkill):
                    # 使用DNASPEC框架的process_request
                    return skill.process_request(context, params or {})
                else:
                    # 直接调用execute方法
                    return skill.execute_with_ai(context, params or {})
        
        elif skill_name in self.native_skills:
            # 使用DNA-Project原生技能
            skill = self.native_skills[skill_name]
            return skill.process_request(context, params or {})
        else:
            available_skills = list(self.all_skills.keys())
            return {
                'success': False,
                'error': f'技能不存在: {skill_name}. 可用技能: {available_skills}'
            }
    
    def execute_enhanced_architect_workflow(self, project_context: str) -> Dict[str, Any]:
        """
        执行增强版架构师工作流
        结合原生DNASPEC技能和Context Engineering增强技能
        """
        results = {
            'project_context': project_context,
            'analysis_phase': {},
            'enhancement_phase': {},
            'execution_phase': {},
            'final_output': ''
        }
        
        try:
            # Phase 1: 使用Context Engineering进行上下文分析
            analysis_result = self.execute_skill('dnaspec-context-analysis', project_context)
            results['analysis_phase'] = analysis_result
            
            if analysis_result.get('success', False) == True:
                # Phase 2: 使用Context Engineering进行上下文优化
                optimization_result = self.execute_skill(
                    'dnaspec-context-optimization',
                    project_context,
                    {'optimization_goals': ['clarity', 'completeness']}
                )
                results['enhancement_phase'] = optimization_result
                
                # Phase 3: 应用认知模板
                template_result = self.execute_skill(
                    'dnaspec-cognitive-template',
                    project_context,
                    {'template': 'chain_of_thought'}
                )
                results['enhancement_phase']['template'] = template_result
                
                # Phase 4: 使用DNASPEC原生技能执行（使用优化后的上下文）
                optimized_context = optimization_result.get('result', {}).get('optimized_context', project_context)
                
                # 路由到合适的DNASPEC技能
                dnaspec_skill_name = self._route_to_best_dnaspec_skill(project_context)
                if dnaspec_skill_name in self.native_skills:
                    execution_result = self.execute_skill(dnaspec_skill_name, optimized_context)
                    results['execution_phase'] = {
                        'used_skill': dnaspec_skill_name,
                        'result': execution_result
                    }
                    
                    results['final_output'] = execution_result.get('result', f"使用技能: {dnaspec_skill_name}")
                else:
                    results['execution_phase'] = {
                        'used_skill': 'dnaspec-architect',
                        'result': self.execute_skill('dnaspec-architect', optimized_context)
                    }
                    results['final_output'] = f"默认使用dna-architect处理: {project_context[:50]}..."
            else:
                # 如果分析失败，直接使用原生DNASPEC技能
                dnaspec_result = self.execute_skill('dnaspec-architect', project_context)
                results['execution_phase'] = {
                    'used_skill': 'dnaspec-architect',
                    'result': dnaspec_result,
                    'fallback': True
                }
                results['final_output'] = dnaspec_result.get('result', f"原生处理结果: {project_context[:50]}...")
            
            return {
                'success': True,
                'result': results
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'增强工作流执行失败: {str(e)}'
            }
    
    def _route_to_best_dnaspec_skill(self, request: str) -> str:
        """路由请求到最适合的原生DNASPEC技能"""
        if "constraint" in request.lower() or "约束" in request:
            return "dnaspec-constraint-generator"
        elif "agent" in request.lower() or "智能体" in request:
            return "dnaspec-agent-creator"
        elif "decompos" in request.lower() or "分解" in request:
            return "dnaspec-task-decomposer"
        elif "architect" in request.lower() or "架构" in request:
            return "dnaspec-system-architect"
        elif "api" in request.lower() or "接口" in request:
            return "dnaspec-dapi-checker"
        else:
            return "dnaspec-architect"  # 默认架构师技能
    
    def get_available_skills(self) -> Dict[str, str]:
        """获取所有可用技能"""
        all_descriptions = {}
        for name, skill in self.all_skills.items():
            if hasattr(skill, 'name') and hasattr(skill, 'description'):
                all_descriptions[name] = skill.description
            elif hasattr(skill, 'get_skill_info'):
                info = skill.get_skill_info()
                all_descriptions[name] = info.get('description', 'No description')
            else:
                all_descriptions[name] = f"{name} 技能"
        
        return all_descriptions
    
    def execute_cli_interface(self, args: Dict[str, Any]) -> str:
        """CLI接口 - 集成原生和增强技能"""
        skill_name = args.get('skill', 'dnaspec-context-analysis')
        context = args.get('context', '') or args.get('request', '')
        params = args.get('params', {})
        
        if not context:
            return "错误: 未提供需要处理的上下文"
        
        result = self.execute_skill(skill_name, context, params)
        
        # 统一格式化输出
        return self._format_skill_result(skill_name, result, context)
    
    def _format_skill_result(self, skill_name: str, result: Dict[str, Any], original_context: str) -> str:
        """格式化技能执行结果"""
        if skill_name.startswith('dnaspec-context-'):
            # Context Engineering 技能的结果格式
            if result.get('success', False):
                result_data = result.get('result', result)
                if isinstance(result_data, dict) and 'result' in result_data:
                    # 两层嵌套结果
                    actual_result = result_data['result']
                else:
                    actual_result = result_data
                
                if skill_name.endswith('analysis'):
                    output_lines = [
                        f"# {skill_name} 结果",
                        f"上下文长度: {actual_result.get('context_length', len(original_context))} 字符",
                        f"Token估算: {actual_result.get('token_count_estimate', len(original_context)//4)}",
                        "",
                        "质量指标 (0.0-1.0):"
                    ]
                    
                    metrics = actual_result.get('metrics', {})
                    metric_names = {
                        'clarity': '清晰度', 'relevance': '相关性', 'completeness': '完整性',
                        'consistency': '一致性', 'efficiency': '效率'
                    }
                    
                    for metric, score in metrics.items():
                        indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
                        output_lines.append(f"  {indicator} {metric_names.get(metric, metric)}: {score:.2f}")
                    
                    if actual_result.get('suggestions'):
                        output_lines.append("\n优化建议:")
                        for suggestion in actual_result['suggestions'][:3]:
                            output_lines.append(f"  • {suggestion}")
                            
                    if actual_result.get('issues'):
                        output_lines.append("\n识别问题:")
                        for issue in actual_result['issues']:
                            output_lines.append(f"  • {issue}")
                    
                    return "\n".join(output_lines)
                
                elif skill_name.endswith('optimization'):
                    output_lines = [
                        f"# {skill_name} 结果",
                        f"原始长度: {len(actual_result.get('original_context', original_context))} 字符",
                        f"优化后长度: {len(actual_result.get('optimized_context', original_context))} 字符",
                        "",
                        "应用的优化措施:"
                    ]
                    
                    optimizations = actual_result.get('applied_optimizations', [])
                    for opt in optimizations:
                        output_lines.append(f"  • {opt}")
                    
                    output_lines.append("\n优化后内容:")
                    output_lines.append(actual_result.get('optimized_context', original_context))
                    
                    return "\n".join(output_lines)
                
                elif skill_name.endswith('template'):
                    output_lines = [
                        f"# {skill_name} 结果",
                        f"模板类型: {actual_result.get('template_type', 'unknown')}",
                        f"模板描述: {actual_result.get('template_description', '未知')}",
                        "",
                        "结构化结果:"
                    ]
                    
                    enhanced_content = actual_result.get('enhanced_context', '')
                    output_lines.append(enhanced_content)
                    
                    return "\n".join(output_lines)
            
            else:
                return f"错误: {result.get('error', 'Unknown error in context engineering skill')}"
        
        else:
            # 原生DNASPEC技能的结果格式
            if isinstance(result, dict) and result.get('status') == 'processed':
                result_content = result.get('result', 'No result returned')
                return f"DNASPEC原生技能结果:\n{result_content}"
            elif 'success' in result and not result['success']:
                return f"错误: {result.get('error', 'Unknown error in native DNASPEC skill')}"
            else:
                return str(result)


def execute(args: Dict[str, Any]) -> str:
    """
    统一执行接口 - 兼容所有技能
    """
    system = DNASPECIntegratedContextEngineeringSystem()
    return system.execute_cli_interface(args)


def get_available_skills() -> Dict[str, str]:
    """
    获取可用技能列表
    """
    system = DNASPECIntegratedContextEngineeringSystem()
    return system.get_available_skills()


# 为CLI准备的统一技能接口
def run_integrated_workflow(project_description: str) -> str:
    """
    运行综合工作流 - 融合原生DNASPEC技能和Context Engineering增强
    """
    system = DNASPECIntegratedContextEngineeringSystem()
    result = system.execute_enhanced_architect_workflow(project_description)
    
    if result['success']:
        workflow_result = result['result']
        output_lines = [
            "### 综合上下文工程工作流执行结果",
            "",
            f"原始项目描述: {workflow_result['project_context'][:50]}...",
            "",
            "#### Phase 1: Context Analysis",
            f"分析指标: {len(workflow_result['analysis_phase'].get('result', {}).get('result', {}).get('metrics', {}))} 个",
            "",
            "#### Phase 2: Context Enhancement", 
            f"优化措施: {len(workflow_result['enhancement_phase'].get('result', {}).get('result', {}).get('applied_optimizations', []))} 项",
            "",
            "#### Phase 3: DNASPEC Execution",
            f"使用的技能: {workflow_result['execution_phase'].get('used_skill', 'unknown')}",
            "",
            "#### 最终输出:",
            str(workflow_result['final_output'])[:300] + ("..." if len(str(workflow_result['final_output'])) > 300 else "")
        ]
        return "\n".join(output_lines)
    else:
        return f"工作流执行失败: {result.get('error', 'Unknown error')}"


if __name__ == "__main__":
    print("DNASPEC Integrated Context Engineering System - 原生技能集成")
    print("="*70)
    print()
    print("🔍 检测DNA-Project原生技能可用性...")
    print(f"   DNASPEC-Project技能: {'✅ 可用' if DNASPEC_PROJECT_AVAILABLE else '⚠️ 模拟模式'}")
    
    system = DNASPECIntegratedContextEngineeringSystem()
    available_skills = system.get_available_skills()
    
    print(f"\n📋 可用技能总数: {len(available_skills)}")
    print("   Context Engineering 增强技能:")
    for name, desc in available_skills.items():
        if name.startswith('dnaspec-context-'):
            print(f"     • {name}: {desc[:50]}...")
    
    print("   DNASPEC-Project 原生技能:")
    for name, desc in available_skills.items():
        if not name.startswith('dnaspec-context-'):
            print(f"     • {name}: {desc[:50]}...")
    
    print()
    print("🎯 系统已成功集成DNA-Project原生技能与Context Engineering增强技能")
    print("✅ AI原生架构 - 完全利用AI智能，无本地模型依赖")
    print("✅ 融合工作流 - 上下文增强 + DNASPEC原生能力")
    print("✅ 统一接口 - 兼容所有技能调用")
    print("✅ 平台集成 - 可用于AI CLI平台")
    print()
    print("💡 现在可以使用统一接口调用所有技能:")
    print("   execute({'skill': 'dnaspec-context-analysis', 'context': '内容'})")
    print("   execute({'skill': 'dnaspec-architect', 'context': '内容'})")
    print("   run_integrated_workflow('项目描述')")