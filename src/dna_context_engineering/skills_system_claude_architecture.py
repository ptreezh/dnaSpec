"""
DNASPEC Context Engineering Skills - Claude Skills Architecture Implementation
遵循Claude Skills架构模式实现，确保与AI CLI平台的兼容性和最佳实践
"""
from typing import Dict, Any, List, Optional
import json
import yaml
from pathlib import Path


def load_skill_config(skill_path: str) -> Dict[str, Any]:
    """
    加载技能配置，遵循Claude Skills的YAML frontmatter模式
    """
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含YAML frontmatter
        if content.startswith('---'):
            lines = content.split('\n')
            frontmatter_end = -1
            for i, line in enumerate(lines[1:], 1):  # 从第二行开始（跳过第一个---）
                if line.strip() == '---':
                    frontmatter_end = i
                    break
            
            if frontmatter_end > 0:
                yaml_content = '\n'.join(lines[1:frontmatter_end])
                config = yaml.safe_load(yaml_content)
                
                # 提取实际内容（去掉frontmatter）
                actual_content = '\n'.join(lines[frontmatter_end + 1:])
                config['content'] = actual_content
                return config
            else:
                # 没有结束的---，整个内容是YAML
                return yaml.safe_load(content)
        else:
            # 没有frontmatter，直接返回内容
            return {'content': content}
    
    except Exception as e:
        return {'error': str(e), 'content': content}


class DNASPECContextEngineeringSystem:
    """
    DNASPEC上下文工程系统 - 遵循Claude Skills架构模式
    作为AI原生工具系统，通过指令驱动而非本地模型实现
    """
    
    def __init__(self):
        self.name = "dnaspec-context-engineering"
        self.description = "DNASPEC Context Engineering Skills System - 专业的上下文工程增强工具集"
        self.version = "1.0.0"
        
        # 定义核心技能
        self.skills = {
            'context-analysis': {
                'name': 'context-analysis',
                'description': '上下文质量五维指标分析',
                'allowed_tools': ['Read', 'Write'],  # 允许的工具
                'model': 'claude-sonnet-4-5-20250929',  # 建议使用的模型
                'activation_contexts': ['analyze', '评估', 'quality', '分析', '质量'],  # 激活上下文
                'implementation': self._run_context_analysis
            },
            'context-optimization': {
                'name': 'context-optimization', 
                'description': '上下文多目标优化',
                'allowed_tools': ['Read', 'Write'],
                'model': 'claude-sonnet-4-5-20250929',
                'activation_contexts': ['optimize', '优化', 'improve', '改进'],
                'implementation': self._run_context_optimization
            },
            'cognitive-template': {
                'name': 'cognitive-template',
                'description': '认知模板应用',
                'allowed_tools': ['Read', 'Write'],
                'model': 'claude-sonnet-4-5-20250929',
                'activation_contexts': ['template', 'framework', '思维链', 'chain', '推理'],
                'implementation': self._run_cognitive_template
            }
        }
        
        self.skill_metadata = self._generate_skill_metadata()
    
    def _generate_skill_metadata(self) -> str:
        """
        生成技能元数据，类似Claude Skills的meta-message模式
        """
        metadata_parts = []
        metadata_parts.append("<available_skills>")
        
        for skill_name, skill_info in self.skills.items():
            metadata_parts.append(f"<skill name='{skill_name}'>")
            metadata_parts.append(f"  <description>{skill_info['description']}</description>")
            metadata_parts.append(f"  <activation_contexts>{', '.join(skill_info['activation_contexts'])}</activation_contexts>")
            metadata_parts.append("</skill>")
        
        metadata_parts.append("</available_skills>")
        return "\n".join(metadata_parts)
    
    def get_available_skills_info(self) -> str:
        """
        获取可用技能信息
        """
        skills_info = []
        skills_info.append(f"Skill: {self.name}")
        skills_info.append(f"Description: {self.description}")
        skills_info.append("Available sub-skills:")
        
        for skill_name, skill_info in self.skills.items():
            skills_info.append(f"  - {skill_name}: {skill_info['description']}")
        
        return "\n".join(skills_info)
    
    def _run_context_analysis(self, context: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行上下文分析，遵循AI原生指令工程模式
        """
        if not context.strip():
            return {
                'success': False,
                'error': '上下文不能为空',
                'skill': 'context-analysis'
            }
        
        # 构造Claude Skills风格的AI指令
        analysis_instruction = f"""
<skill name="context-analysis" type="analysis">
  <input>
    <context><![CDATA[{context}]]></context>
    <parameters>{json.dumps(params)}</parameters>
  </input>
  
  <task>作为专业的上下文质量分析师，对以下上下文进行五维度评估：</task>
  
  <dimensions>
    <dimension name="clarity">清晰度 - 表达明确性，术语准确性 (0.0-1.0)</dimension>
    <dimension name="relevance">相关性 - 与目标相关性，内容针对性 (0.0-1.0)</dimension>
    <dimension name="completeness">完整性 - 关键信息完备性，约束条件完整性 (0.0-1.0)</dimension>
    <dimension name="consistency">一致性 - 内容内部逻辑一致性 (0.0-1.0)</dimension>
    <dimension name="efficiency">效率 - 信息密度与简洁性 (0.0-1.0)</dimension>
  </dimensions>
  
  <output_format>
    必须以JSON格式返回结果:
    {{
      "context_length": 数值,
      "token_count_estimate": 数值, 
      "metrics": {{
        "clarity": 0.0-1.0,
        "relevance": 0.0-1.0,
        "completeness": 0.0-1.0,
        "consistency": 0.0-1.0,
        "efficiency": 0.0-1.0
      }},
      "suggestions": ["建议1", "建议2"],
      "issues": ["问题1", "问题2"]
    }}
  </output_format>
</skill>
"""
        
        # 模拟AI处理（真实实现中会调用AI API）
        import random
        seed = hash(context) % 10000
        random.seed(seed)
        
        clarity = min(1.0, max(0.0, 0.5 + len(context) * 0.0001))
        relevance = min(1.0, max(0.0, 0.7 + (0.2 if '系统' in context or '任务' in context else 0)))
        completeness = min(1.0, max(0.0, 0.3 + (0.3 if '约束' in context or '要求' in context else 0)))
        consistency = min(1.0, max(0.0, 0.8 - (0.2 if '但是' in context or '然而' in context else 0)))
        efficiency = min(1.0, max(0.0, 1.0 - len(context) * 0.00005))
        
        return {
            'success': True,
            'result': {
                'context_length': len(context),
                'token_count_estimate': max(1, len(context) // 4),
                'metrics': {
                    'clarity': round(clarity, 2),
                    'relevance': round(relevance, 2),
                    'completeness': round(completeness, 2),
                    'consistency': round(consistency, 2),
                    'efficiency': round(efficiency, 2)
                },
                'suggestions': [
                    "增加更明确的目标描述",
                    "补充约束条件和具体要求",
                    "提高表述清晰度"
                ],
                'issues': [
                    "缺少明确的约束条件" if completeness < 0.6 else "",
                    "部分表述可以更精确" if clarity < 0.7 else ""
                ],
                'issues': [issue for issue in [
                    "缺少明确的约束条件" if completeness < 0.6 else "",
                    "部分表述可以更精确" if clarity < 0.7 else ""
                ] if issue]
            }
        }
    
    def _run_context_optimization(self, context: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行上下文优化，遵循AI原生指令工程模式
        """
        if not context.strip():
            return {
                'success': False,
                'error': '上下文不能为空',
                'skill': 'context-optimization'
            }
        
        goals = params.get('optimization_goals', ['clarity', 'completeness'])
        if isinstance(goals, str):
            goals = [g.strip() for g in goals.split(',') if g.strip()]
        
        # 构造Claude Skills风格的优化指令
        optimization_instruction = f"""
<skill name="context-optimization" type="optimization">
  <input>
    <context><![CDATA[{context}]]></context>
    <optimization_goals>{', '.join(goals)}</optimization_goals>
  </input>
  
  <task>根据指定目标优化以下上下文内容：</task>
  
  <optimization_targets>
    {', '.join(goals)}
  </optimization_targets>
  
  <requirements>
    - 保持原始核心意图不变
    - 提高指定维度的质量
    - 提供具体的改进措施说明
    - 确保优化后逻辑正确性
  </requirements>
  
  <output_format>
    以JSON格式返回:
    {{
      "original_context": "原始上下文内容",
      "optimized_context": "优化后上下文内容",
      "applied_optimizations": ["优化措施1", "优化措施2"],
      "improvement_metrics": {{
        "clarity_change": +/-0.x,
        "relevance_change": +/-0.x,
        "completeness_change": +/-0.x,
        "conciseness_change": +/-0.x
      }},
      "confidence": 0.8-1.0
    }}
  </output_format>
</skill>
"""
        
        # 模拟优化结果
        optimized_context = context
        applied_optimizations = []
        improvements = {}
        
        if 'clarity' in goals:
            if not any(word in context for word in ['明确', '请', '具体']):
                optimized_context += "\n\n请明确具体的目标和约束条件。"
                applied_optimizations.append("提升表述清晰度")
                improvements['clarity'] = 0.2
        
        if 'completeness' in goals:
            if not any(kw in context for kw in ['约束', '要求', '目标', '条件']):
                optimized_context += "\n\n约束条件: 需在指定时间内完成\n明确目标: 实现预期功能\n前提假设: 有必要的资源支持"
                applied_optimizations.append("补充完整性要素")
                improvements['completeness'] = 0.3
        
        if 'relevance' in goals:
            optimized_context = f"任务目标: {optimized_context}"
            applied_optimizations.append("增强目标相关性")  
            improvements['relevance'] = 0.15
        
        return {
            'success': True,
            'result': {
                'original_context': context,
                'optimized_context': optimized_context,
                'applied_optimizations': applied_optimizations,
                'improvement_metrics': {
                    'clarity': improvements.get('clarity', 0.0),
                    'relevance': improvements.get('relevance', 0.0),
                    'completeness': improvements.get('completeness', 0.0),
                    'conciseness': improvements.get('conciseness', 0.0)
                },
                'optimization_summary': f"根据目标 {', '.join(goals)} 完成优化",
                'confidence': 0.8
            }
        }
    
    def _run_cognitive_template(self, task: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行认知模板应用，遵循AI原生指令工程模式
        """
        if not task.strip():
            return {
                'success': False,
                'error': '任务不能为空',
                'skill': 'cognitive-template'
            }
        
        template_type = params.get('template', 'chain_of_thought')
        
        # 定义认知模板指令
        template_descriptions = {
            'chain_of_thought': '思维链推理模板 - 逐步骤分析复杂问题',
            'few_shot': '少样本学习模板 - 通过示例引导AI行为',
            'verification': '验证检查模板 - 多角度验证结果质量',
            'role_playing': '角色扮演模板 - 从特定角色视角分析',
            'understanding': '深度理解模板 - 多维度理解任务'
        }
        
        if template_type not in template_descriptions:
            return {
                'success': False,
                'error': f'未知模板: {template_type}',
                'available_templates': list(template_descriptions.keys())
            }
        
        template_desc = template_descriptions[template_type]
        
        # 构造Claude Skills风格的模板指令
        template_instruction = f"""
<skill name="cognitive-template" type="framework">
  <input>
    <task><![CDATA[{task}]]></task>
    <template_type>{template_type}</template_type>
    <template_description>{template_desc}</template_description>
  </input>
  
  <task>使用{template_desc}分析以下任务：</task>
  
  <cognitive_process>
    """ + (f"""应用思维链步骤:
1. 问题理解: [理解任务核心]
2. 步骤分解: [分解为子任务]
3. 中间推理: [执行中间步骤]
4. 验证检查: [验证逻辑合理性]
5. 最终答案: [综合所有步骤的答案]
""" if template_type == 'chain_of_thought' else f"""应用{template_type}认知框架:
[在此应用认知框架分析...]
""") + """
  </cognitive_process>
  
  <output_format>
    返回结构化认知处理结果
  </output_format>
</skill>
"""
        
        # 模拟模板应用结果
        template_results = {
            'chain_of_thought': f"""
### 思维链认知框架应用

**原始任务**: {task}

**分析步骤**:
1. **问题理解**: 识别核心需求和约束
2. **步骤分解**: 拆分为可执行子步骤
3. **中间推理**: 详细推理过程
4. **验证检查**: 验证推理合理性
5. **最终答案**: 综合解决方案

**AI模型基于思维链框架完成结构化分析**
""",
            'verification': f"""
### 验证检查认知框架

**原始内容**: {task}

**验证过程**:
1. **初步答案**: 基于内容的初步判断
2. **逻辑一致性检查**: 验证内部逻辑一致性
3. **事实准确性检查**: 核实陈述准确性
4. **完整性检查**: 评估信息完整性
5. **最终确认**: 基于以上检查的确认

**AI模型基于验证框架完成质量评估**
""",
            'few_shot': f"""
### 少样本学习认知框架

**任务**: {task}

**示例对**:
示例1: 输入复杂问题 → 输出结构化解法
示例2: 输入分析任务 → 输出专业框架

**AI模型基于少样本模式完成任务**
"""
        }
        
        enhanced_context = template_results.get(template_type, f"应用{template_type}框架分析: {task}")
        
        return {
            'success': True,
            'result': {
                'success': True,
                'template_type': template_type,
                'template_description': template_desc,
                'original_task': task,
                'enhanced_context': enhanced_context,
                'cognitive_structure': [
                    '应用认知框架', '结构化输出', '验证结果'
                ]
            }
        }
    
    def execute_skill(self, skill_name: str, context: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        执行指定技能，遵循Claude Skills的执行模式
        """
        params = params or {}
        
        if skill_name not in self.skills:
            available_skills = list(self.skills.keys())
            return {
                'success': False,
                'error': f'技能不存在: {skill_name}. 可用技能: {available_skills}'
            }
        
        skill_info = self.skills[skill_name]
        implementation = skill_info['implementation']
        
        try:
            return implementation(context, params)
        except Exception as e:
            return {
                'success': False,
                'error': f'技能执行失败: {str(e)}',
                'skill': skill_name
            }
    
    def get_available_skills_info(self) -> str:
        """
        获取可用技能信息，类似Claude Skills的工具描述
        """
        skills_info = []
        skills_info.append(f"Skill: {self.name}")
        skills_info.append(f"Description: {self.description}")
        skills_info.append("Available sub-skills:")
        
        for skill_name, skill_info in self.skills.items():
            skills_info.append(f"  - {skill_name}: {skill_info['description']}")
        
        return "\n".join(skills_info)
    
    def activate_for_context(self, user_input: str) -> List[str]:
        """
        根据用户输入激活相关的技能
        仿照Claude Skills的上下文感知激活模式
        """
        active_skills = []
        
        input_lower = user_input.lower() + user_input
        
        for skill_name, skill_info in self.skills.items():
            for context_keyword in skill_info['activation_contexts']:
                if context_keyword in input_lower:
                    active_skills.append(skill_name)
                    break  # 一旦匹配就添加技能，继续下一个技能
        
        # 去重但保持顺序
        unique_active = []
        for skill in active_skills:
            if skill not in unique_active:
                unique_active.append(skill)
        
        return unique_active


def execute(args: Dict[str, Any]) -> str:
    """
    统一执行接口 - 与Claude Skills风格兼容
    """
    skill_name = args.get('skill')
    context_input = args.get('context', '') or args.get('request', '')
    params = args.get('params', {})
    
    if not skill_name:
        # 如果没有指定技能，尝试自动识别
        system = DNASPECContextEngineeringSystem()
        active_skills = system.activate_for_context(context_input)
        if active_skills:
            skill_name = active_skills[0]  # 使用第一个匹配的技能
        else:
            skill_name = 'context-analysis'  # 默认分析技能
    
    if not context_input and skill_name != 'help':
        return "错误: 未提供需要处理的上下文或请求内容"
    
    system = DNASPECContextEngineeringSystem()
    
    if skill_name == 'help':
        return system.get_available_skills_info()
    
    result = system.execute_skill(skill_name, context_input, params)
    
    if not result['success']:
        return f"错误: {result.get('error', '技能执行失败')}"
    
    # 格式化输出结果
    output_lines = []
    skill_result = result['result']
    
    if skill_name == 'context-analysis':
        output_lines.append("# 上下文质量分析结果")
        output_lines.append(f"上下文长度: {skill_result['context_length']} 字符")
        output_lines.append(f"Token估算: {skill_result['token_count_estimate']}")
        output_lines.append("")
        
        output_lines.append("五维质量指标 (0.0-1.0):")
        metric_names = {
            'clarity': '清晰度', 'relevance': '相关性', 'completeness': '完整性',
            'consistency': '一致性', 'efficiency': '效率'
        }
        
        for metric, score in skill_result['metrics'].items():
            indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
            output_lines.append(f"  {indicator} {metric_names.get(metric, metric)}: {score:.2f}")
        
        if skill_result.get('suggestions'):
            output_lines.append("\n优化建议:")
            for suggestion in skill_result['suggestions'][:3]:  # 显示前3条
                output_lines.append(f"  • {suggestion}")
        
        if skill_result.get('issues'):
            output_lines.append("\n识别问题:")
            for issue in skill_result['issues']:
                output_lines.append(f"  • {issue}")
    
    elif skill_name == 'context-optimization':
        output_lines.append("# 上下文优化结果")
        output_lines.append(f"原始长度: {len(skill_result['original_context'])} 字符")
        output_lines.append(f"优化后长度: {len(skill_result['optimized_context'])} 字符")
        confidence = skill_result.get('result', {}).get('confidence', 0.8) if 'result' in skill_result else skill_result.get('confidence', 0.8)
        output_lines.append(f"置信度: {confidence:.2f}")
        output_lines.append("")
        
        applied_opts = skill_result.get('result', {}).get('applied_optimizations', []) if 'result' in skill_result else skill_result.get('applied_optimizations', [])
        output_lines.append("应用的优化措施:")
        for opt in applied_opts:
            output_lines.append(f"  • {opt}")
        
        improvement_metrics = skill_result.get('result', {}).get('improvement_metrics', {}) if 'result' in skill_result else skill_result.get('improvement_metrics', {})
        output_lines.append("\n改进指标:")
        for metric, change in improvement_metrics.items():
            if change != 0:  # 只显示有变化的指标
                direction = "↗️" if change > 0 else "↘️" if change < 0 else "➡️"
                output_lines.append(f"  {direction} {metric}: {change:+.2f}")
        
        optimized_context = skill_result.get('result', {}).get('optimized_context', skill_result['original_context']) if 'result' in skill_result else skill_result.get('optimized_context', skill_result['original_context'])
        output_lines.append("\n优化后上下文:")
        output_lines.append(optimized_context)
    
    elif skill_name == 'cognitive-template':
        template_result = skill_result.get('result', {}) if skill_result.get('success', False) else skill_result
        template_type = template_result.get('template_type', 'unknown')
        template_description = template_result.get('template_description', 'Unknown template')
        enhanced_context = template_result.get('enhanced_context', 'No enhanced context returned')
        
        output_lines.append(f"# 认知模板应用: {template_type}")
        output_lines.append(f"描述: {template_description}")
        output_lines.append("=" * 60)
        output_lines.append("")
        output_lines.append("结构化认知输出:")
        output_lines.append(enhanced_context)
    
    return "\n".join(output_lines)


def get_skill_metadata() -> str:
    """
    获取技能元数据，用于Claude Tools的工具描述
    """
    system = DNASPECContextEngineeringSystem()
    return system.skill_metadata