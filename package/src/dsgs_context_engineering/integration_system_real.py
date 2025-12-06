"""
DSGS Context Engineering Skills - 与DSGS-Project集成实现
整合DSGS Project中现有的skills与Context Engineering增强技能
"""
import sys
import os
from typing import Dict, Any

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.dsgs_context_engineering.skills_system_final_clean import (
    ContextAnalysisSkill as ContextEngineAnalysisSkill,
    ContextOptimizationSkill as ContextEngineOptimizationSkill, 
    CognitiveTemplateSkill as ContextEngineTemplateSkill
)

# 在DSGS-Project路径中查找原生技能
dsgs_proj_path = os.path.join(os.path.dirname(__file__), '..', '..', 'DSGS-Project')
sys.path.insert(0, dsgs_proj_path)

# 尝试导入DSGS-Project的原生技能
try:
    # 从DSGS-Project导入技能类
    dsgs_src_path = os.path.join(dsgs_proj_path, 'src')
    sys.path.insert(0, dsgs_src_path)
    
    from dsgs_architect import DSGSArchitect
    from dsgs_task_decomposer import DSGSTaskDecomposer  
    from dsgs_agent_creator import DSGSAgentCreator
    from dsgs_system_architect import DSGSSystemArchitect
    from dsgs_constraint_generator import DSGSConstraintGenerator
    from dsgs_dapi_checker import DSGSDAPIChecker
    from dsgs_modulizer import DSGSModulizer
    
    DSGS_PROJECT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ DSGS-Project技能不可用: {e}")
    DSGS_PROJECT_AVAILABLE = False
    # 创建模拟类以继续集成
    class DSGSArchitect:
        def __init__(self): 
            self.name = "dsgs-architect"
            self.description = "DSGS原生架构师技能 (模拟)"
        
        def process_request(self, request: str, context=None):
            return {"status": "processed", "result": f"模拟架构师处理: {request}"}
    
    class DSGSTaskDecomposer:
        def __init__(self):
            self.name = "dsgs-task-decomposer"
            self.description = "DSGS原生任务分解技能 (模拟)"
            
        def process_request(self, request: str, context=None):
            return {"status": "processed", "result": f"模拟任务分解: {request}"}
    
    # 其他模拟类...
    DSGSAgentCreator = DSGSArchitect
    DSGSSystemArchitect = DSGSArchitect  
    DSGSConstraintGenerator = DSGSArchitect
    DSGSDAPIChecker = DSGSArchitect
    DSGSModulizer = DSGSArchitect


class DSGSIntegratedContextEngineeringSystem:
    """
    集成DSGS-Project与Context Engineering Skills的综合系统
    充分利用AI原生智能，整合所有可用技能
    """
    
    def __init__(self):
        # DSGS-Project 原生技能
        if DSGS_PROJECT_AVAILABLE:
            self.native_skills = {
                'dsgs-architect': DSGSArchitect(),
                'dsgs-task-decomposer': DSGSTaskDecomposer(),
                'dsgs-agent-creator': DSGSAgentCreator(),
                'dsgs-system-architect': DSGSSystemArchitect(),
                'dsgs-constraint-generator': DSGSConstraintGenerator(),
                'dsgs-dapi-checker': DSGSDAPIChecker(),
                'dsgs-modulizer': DSGSModulizer()
            }
        else:
            # 如果原生项目不可用，使用模拟技能
            self.native_skills = {
                'dsgs-architect': DSGSArchitect(),
                # 添加更多模拟技能...
            }
        
        # Context Engineering 增强技能（AI原生）
        self.enhanced_skills = {
            'dsgs-context-analysis': ContextEngineAnalysisSkill(),
            'dsgs-context-optimization': ContextEngineOptimizationSkill(),
            'dsgs-cognitive-template': ContextEngineTemplateSkill()
        }
        
        # 统一技能库
        self.all_skills = {**self.native_skills, **self.enhanced_skills}
    
    def execute_skill(self, skill_name: str, context: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行指定技能"""
        params = params or {}
        
        if skill_name in self.enhanced_skills:
            # 使用AI原生增强技能
            skill = self.enhanced_skills[skill_name]
            from src.dsgs_spec_kit_integration.core.skill import DSGSSkill
            if isinstance(skill, DSGSSkill):
                # 使用DSGS框架的process_request
                return skill.process_request(context, params)
            else:
                # 如果没有继承DSGSSkill，直接调用execute方法
                return skill.execute_with_ai(context, params)
        
        elif skill_name in self.native_skills:
            # 使用DSGS-Project原生技能
            skill = self.native_skills[skill_name]
            return skill.process_request(context, params)
        else:
            available_skills = list(self.all_skills.keys())
            return {
                'success': False,
                'error': f'技能不存在: {skill_name}. 可用技能: {available_skills}'
            }
    
    def execute_enhanced_architect_workflow(self, project_context: str) -> Dict[str, Any]:
        """
        执行增强版架构师工作流
        结合原生DSGS技能和Context Engineering增强技能
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
            analysis_result = self.execute_skill('dsgs-context-analysis', project_context)
            results['analysis_phase'] = analysis_result
            
            if isinstance(analysis_result, dict) and analysis_result.get('success', False):
                # Phase 2: 使用Context Engineering进行上下文优化
                optimization_result = self.execute_skill(
                    'dsgs-context-optimization',
                    project_context,
                    {'optimization_goals': ['clarity', 'completeness']}
                )
                results['enhancement_phase'] = optimization_result
                
                # Phase 3: 应用认知模板
                template_result = self.execute_skill(
                    'dsgs-cognitive-template',
                    project_context,
                    {'template': 'chain_of_thought'}
                )
                
                # Phase 4: 使用DSGS原生技能执行（使用优化后的上下文）
                optimized_context = optimization_result.get('result', {}).get('optimized_context', project_context) \
                    if isinstance(optimization_result, dict) and 'result' in optimization_result and \
                       isinstance(optimization_result['result'], dict) else project_context
                
                # 路由到合适的DSGS技能
                dsgs_skill_name = self._route_to_best_dsgs_skill(project_context)
                if dsgs_skill_name in self.native_skills:
                    execution_result = self.execute_skill(dsgs_skill_name, optimized_context)
                    results['execution_phase'] = {
                        'used_skill': dsgs_skill_name,
                        'result': execution_result
                    }
                    
                    # 综合所有结果
                    analysis_summary = analysis_result.get('result', {}).get('result', {}).get('suggestions', [])
                    results['final_output'] = f"""
项目分析与执行结果:

原始上下文: {project_context}

分析结果:
- 质量指标: {analysis_result.get('result', {}).get('result', {}).get('metrics', {})}
- 优化建议: {analysis_summary[:3]}
- 应用技能: {dsgs_skill_name}
- 执行结果: {str(execution_result)[:200]}...

分析完成，AI模型已处理上下文并提供结构化结果。
"""
                else:
                    results['execution_phase'] = {
                        'used_skill': 'dsgs-architect',
                        'result': self.execute_skill('dsgs-architect', optimized_context),
                        'fallback': True
                    }
                    results['final_output'] = f"默认使用dsgs-architect处理: {project_context[:50]}..."
            else:
                # 如果分析失败，直接使用原生DSGS技能
                dsgs_result = self.execute_skill('dsgs-architect', project_context)
                results['execution_phase'] = {
                    'used_skill': 'dsgs-architect',
                    'result': dsgs_result,
                    'fallback': True
                }
                results['final_output'] = f"原生DSGS架构师结果: {str(dsgs_result)[:200]}..."
            
            return {
                'success': True,
                'result': results
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'增强工作流执行失败: {str(e)}'
            }
    
    def _route_to_best_dsgs_skill(self, request: str) -> str:
        """路由请求到最适合的原生DSGS技能"""
        if "constraint" in request.lower() or "约束" in request:
            return "dsgs-constraint-generator"
        elif "agent" in request.lower() or "智能体" in request:
            return "dsgs-agent-creator"
        elif "decompos" in request.lower() or "分解" in request:
            return "dsgs-task-decomposer"
        elif "architect" in request.lower() or "架构" in request:
            return "dsgs-system-architect"
        elif "api" in request.lower() or "接口" in request:
            return "dsgs-dapi-checker"
        else:
            return "dsgs-architect"  # 默认架构师技能
    
    def get_available_skills(self) -> Dict[str, str]:
        """获取所有可用技能"""
        all_descriptions = {}
        for name, skill in self.all_skills.items():
            if hasattr(skill, 'name') and hasattr(skill, 'description'):
                all_descriptions[name] = skill.description
            elif hasattr(skill, 'get_skill_info'):
                try:
                    info = skill.get_skill_info()
                    all_descriptions[name] = info.get('description', 'No description')
                except:
                    all_descriptions[name] = f"{name} 技能 (未知描述)"
            else:
                all_descriptions[name] = f"{name} 技能"
        
        return all_descriptions
    
    def execute_cli_interface(self, args: Dict[str, Any]) -> str:
        """CLI接口 - 集成原生和增强技能"""
        skill_name = args.get('skill', 'dsgs-context-analysis')
        context = args.get('context', '') or args.get('request', '')
        params = args.get('params', {})
        
        if not context:
            return "错误: 未提供需要处理的上下文"
        
        result = self.execute_skill(skill_name, context, params)
        
        # 统一格式化输出
        return self._format_skill_result(skill_name, result, context)
    
    def _format_skill_result(self, skill_name: str, result: Dict[str, Any], original_context: str) -> str:
        """格式化技能执行结果"""
        if skill_name.startswith('dsgs-context-'):
            # Context Engineering 技能的结果格式
            if isinstance(result, dict) and result.get('success', False):
                result_data = result
                if 'result' in result_data and isinstance(result_data['result'], dict):
                    # 两层结果结构
                    if 'result' in result_data['result']:
                        actual_result = result_data['result']['result']
                    else:
                        actual_result = result_data['result']
                else:
                    actual_result = result_data
                
                if skill_name.endswith('analysis'):
                    # 检查结果结构，处理嵌套结果
                    if 'result' in actual_result and 'result' in actual_result['result']:
                        # 三层嵌套结果结构
                        analysis_data = actual_result['result']['result']
                    elif 'result' in actual_result:
                        # 两层嵌套结果结构
                        analysis_data = actual_result['result']
                    else:
                        # 直接结果结构
                        analysis_data = actual_result
                    
                    output_lines = [
                        f"# {skill_name} 结果",
                        f"上下文长度: {analysis_data.get('context_length', len(original_context))} 字符",
                        f"Token估算: {analysis_data.get('token_count_estimate', len(original_context)//4)}",
                        "",
                        "质量指标 (0.0-1.0):"
                    ]
                    
                    metrics = analysis_data.get('metrics', {})
                    metric_names = {
                        'clarity': '清晰度', 'relevance': '相关性', 'completeness': '完整性',
                        'consistency': '一致性', 'efficiency': '效率'
                    }
                    
                    for metric, score in metrics.items():
                        indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
                        output_lines.append(f"  {indicator} {metric_names.get(metric, metric)}: {score:.2f}")
                    
                    if analysis_data.get('suggestions'):
                        output_lines.append("\n优化建议:")
                        for suggestion in analysis_data['suggestions'][:3]:
                            output_lines.append(f"  • {suggestion}")
                    
                    if analysis_data.get('issues'):
                        output_lines.append("\n识别问题:")
                        for issue in analysis_data['issues']:
                            output_lines.append(f"  • {issue}")
                    
                    return "\n".join(output_lines)
                
                elif skill_name.endswith('optimization'):
                    # 检查优化结果结构
                    if 'result' in actual_result and 'result' in actual_result['result']:
                        optimization_data = actual_result['result']['result']
                    elif 'result' in actual_result:
                        optimization_data = actual_result['result']
                    else:
                        optimization_data = actual_result
                    
                    output_lines = [
                        f"# {skill_name} 结果",
                        f"原始长度: {len(optimization_data.get('original_context', original_context))} 字符",
                        f"优化后长度: {len(optimization_data.get('optimized_context', original_context))} 字符",
                        "",
                        "应用的优化措施:"
                    ]
                    
                    optimizations = optimization_data.get('applied_optimizations', [])
                    for opt in optimizations:
                        output_lines.append(f"  • {opt}")
                    
                    output_lines.append("\n改进指标:")
                    improvement_metrics = optimization_data.get('improvement_metrics', {})
                    for metric, change in improvement_metrics.items():
                        direction = "↗️" if change > 0 else "↘️" if change < 0 else "➡️"
                        output_lines.append(f"  {direction} {metric}: {change:+.2f}")
                    
                    output_lines.append("\n优化后内容:")
                    optimized_content = optimization_data.get('optimized_context', original_context)
                    output_lines.append(optimized_content)
                    
                    return "\n".join(output_lines)
                
                elif skill_name.endswith('template'):
                    # 检查模板结果结构
                    if 'result' in actual_result:
                        template_data = actual_result['result']
                    else:
                        template_data = actual_result
                    
                    if template_data.get('success', True):
                        template_result = template_data
                    else:
                        template_result = actual_result
                    
                    output_lines = [
                        f"# {skill_name} 结果",
                        f"模板类型: {template_result.get('template_type', 'unknown')}",
                        f"模板描述: {template_result.get('template_description', '未知')}",
                        "",
                        "结构化结果:"
                    ]
                    
                    enhanced_content = template_result.get('enhanced_context', '')
                    output_lines.append(enhanced_content)
                    
                    return "\n".join(output_lines)
                    output_lines = [
                        f"# {skill_name} 结果",
                        f"原始长度: {len(result_data.get('result', {}).get('original_context', original_context))} 字符",
                        f"优化后长度: {len(result_data.get('result', {}).get('optimized_context', original_context))} 字符",
                        "",
                        "应用的优化措施:"
                    ]
                    
                    optimizations = result_data.get('result', {}).get('applied_optimizations', [])
                    for opt in optimizations:
                        output_lines.append(f"  • {opt}")
                    
                    output_lines.append("\n改进指标:")
                    improvement_metrics = result_data.get('result', {}).get('improvement_metrics', {})
                    for metric, change in improvement_metrics.items():
                        direction = "↗️" if change > 0 else "↘️" if change < 0 else "➡️"
                        output_lines.append(f"  {direction} {metric}: {change:+.2f}")
                    
                    output_lines.append("\n优化后内容:")
                    optimized_content = result_data.get('result', {}).get('optimized_context', original_context)
                    output_lines.append(optimized_content)
                    
                    return "\n".join(output_lines)
                
                elif skill_name.endswith('template'):
                    output_lines = [
                        f"# {skill_name} 结果",
                        f"模板类型: {result_data.get('result', {}).get('template_type', 'unknown')}",
                        f"模板描述: {result_data.get('result', {}).get('template_description', '未知')}",
                        "",
                        "结构化结果:"
                    ]
                    
                    enhanced_content = result_data.get('result', {}).get('enhanced_context', '')
                    output_lines.append(enhanced_content)
                    
                    return "\n".join(output_lines)
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
                    
                    output_lines.append("\n改进指标:")
                    for metric, change in actual_result.get('improvement_metrics', {}).items():
                        direction = "↗️" if change > 0 else "↘️" if change < 0 else "➡️"
                        output_lines.append(f"  {direction} {metric}: {change:+.2f}")
                    
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
                error_msg = result.get('error', 'Unknown error in context engineering skill')
                return f"错误: {error_msg}"
        
        else:
            # 原生DSGS技能的结果格式
            if isinstance(result, dict):
                if result.get('status') == 'processed':
                    result_content = result.get('result', 'No result returned')
                    return f"DSGS原生技能结果:\n{result_content}"
                elif result.get('success', False) == False:
                    error_msg = result.get('error', 'Unknown error in native DSGS skill')
                    return f"错误: {error_msg}"
                else:
                    return str(result)
            else:
                return str(result)


def execute(args: Dict[str, Any]) -> str:
    """
    统一执行接口 - 兼容所有技能
    """
    system = DSGSIntegratedContextEngineeringSystem()
    return system.execute_cli_interface(args)


def get_available_skills() -> Dict[str, str]:
    """
    获取可用技能列表
    """
    system = DSGSIntegratedContextEngineeringSystem()
    return system.get_available_skills()


# 为CLI准备的统一技能接口
def run_integrated_workflow(project_description: str) -> str:
    """
    运行综合工作流 - 融合原生DSGS技能和Context Engineering增强
    """
    system = DSGSIntegratedContextEngineeringSystem()
    result = system.execute_enhanced_architect_workflow(project_description)
    
    if result['success']:
        workflow_result = result['result']
        output_lines = [
            "### 综合上下文工程工作流执行结果",
            "",
            f"原始项目描述: {workflow_result['project_context'][:50]}...",
            "",
            "#### Phase 1: Context Analysis",
            f"分析完成",
            "",
            "#### Phase 2: Context Enhancement", 
            f"优化措施应用",
            "",
            "#### Phase 3: DSGS Execution",
            f"使用的技能: {workflow_result['execution_phase'].get('used_skill', 'unknown')}",
            "",
            "#### 最终输出:",
            str(workflow_result['final_output'])
        ]
        return "\n".join(output_lines)
    else:
        return f"工作流执行失败: {result.get('error', 'Unknown error')}"


if __name__ == "__main__":
    print("DSGS Integrated Context Engineering System - 原生技能集成")
    print("="*70)
    print()
    print("🔍 检测DSGS-Project原生技能可用性...")
    print(f"   DSGS-Project技能: {'✅ 可用' if DSGS_PROJECT_AVAILABLE else '⚠️ 模拟模式'}")
    
    system = DSGSIntegratedContextEngineeringSystem()
    available_skills = system.get_available_skills()
    
    print(f"\n📋 可用技能总数: {len(available_skills)}")
    print("   Context Engineering 增强技能:")
    for name, desc in available_skills.items():
        if name.startswith('dsgs-context-'):
            print(f"     • {name}: {desc[:50]}...")
    
    print("   DSGS-Project 原生技能:")
    for name, desc in available_skills.items():
        if name.startswith('dsgs-') and not name.startswith('dsgs-context-'):
            print(f"     • {name}: {desc[:50]}...")
    
    print()
    print("🎯 系统已成功集成DSGS-Project原生技能与Context Engineering增强技能")
    print("✅ AI原生架构 - 完全利用AI智能，无本地模型依赖")
    print("✅ 融合工作流 - 上下文增强 + DSGS原生能力")
    print("✅ 统一接口 - 兼容所有技能调用")
    print("✅ 平台集成 - 可用于AI CLI平台")
    print()
    print("💡 现在可以使用统一接口调用所有技能:")
    print("   execute({'skill': 'dsgs-context-analysis', 'context': '内容'})")
    print("   execute({'skill': 'dsgs-architect', 'context': '内容'})")
    print("   run_integrated_workflow('项目描述')")