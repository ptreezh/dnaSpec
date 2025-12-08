"""
Cognitive Template Skill - 符合DNASPEC原始规范的实现
为AI CLI平台提供认知模板应用能力
"""
from typing import Dict, Any


def execute(args: Dict[str, Any]) -> str:
    """
    执行认知模板应用 - 与DNASPEC原始技能接口保持一致
    """
    context = args.get("context", "") or args.get("request", "") or args.get("description", "")
    template_type = args.get("template", "chain_of_thought")
    role = args.get("role", "专家")
    
    if not context.strip():
        return "错误: 未提供要应用模板的上下文"
    
    # 执行认知模板应用
    template_result = _apply_cognitive_template_with_ai(context, template_type, role)
    
    # 格式化输出结果
    if template_result['success']:
        output_lines = []
        output_lines.append(f"认知模板应用结果 - {template_result['template_type']} ({template_result['template_description']})")
        output_lines.append("=" * 60)
        output_lines.append("")
        output_lines.append("结构化后的内容:")
        output_lines.append(template_result['enhanced_context'])
        
        return "\n".join(output_lines)
    else:
        return f"错误: {template_result['error']}"


def _apply_cognitive_template_with_ai(context: str, template_type: str, role: str = "专家") -> Dict[str, Any]:
    """
    使用AI模型应用认知模板（模拟实现）
    """
    if template_type not in ['chain_of_thought', 'few_shot', 'verification', 'role_playing', 'understanding']:
        return {
            'success': False,
            'error': f"未知模板类型: {template_type}. 支持: chain_of_thought, few_shot, verification, role_playing, understanding",
            'available_templates': ['chain_of_thought', 'few_shot', 'verification', 'role_playing', 'understanding']
        }
    
    # 根据模板类型构造相应的认知结构
    template_results = {
        'chain_of_thought': _apply_chain_of_thought_template(context),
        'few_shot': _apply_few_shot_template(context),
        'verification': _apply_verification_template(context),
        'role_playing': _apply_role_playing_template(context, role),
        'understanding': _apply_understanding_template(context)
    }
    
    result = template_results[template_type]
    result['success'] = True
    result['template_type'] = template_type
    result['template_description'] = {
        'chain_of_thought': '思维链推理模板 - 通过逐步推理分析复杂问题',
        'few_shot': '少样本学习模板 - 通过示例引导AI行为',
        'verification': '验证检查模板 - 通过多步验证确保结果质量',
        'role_playing': '角色扮演模板 - 从特定角色视角分析问题',
        'understanding': '深度理解模板 - 从多维度深入理解任务'
    }[template_type]
    
    return result


def _apply_chain_of_thought_template(context: str) -> Dict[str, Any]:
    """
    应用思维链模板
    """
    enhanced_context = f"""
### 思维链分析框架

**原始任务**: {context}

请按以下思维链步骤详细分析此任务：

1. **问题理解**: 
   - 明确任务的核心需求
   - 识别关键约束和限制
   - 确定成功标准

2. **步骤分解**: 
   - 将任务分解为可执行的子步骤
   - 确定步骤间的依赖关系
   - 评估每步的时间和资源需求

3. **中间推理**: 
   - 针对每个子步骤进行详细推理
   - 考虑不同的实现方案
   - 评估各方案的优劣

4. **验证检查**: 
   - 检查推理过程的逻辑一致性
   - 验证方案的可行性
   - 识别潜在风险和挑战

5. **最终答案**: 
   - 综合所有分析给出最终解决方案
   - 提供明确的执行建议
   - 确定优先级和里程碑

请返回完整的分析过程和最终结论。
"""
    
    return {
        'enhanced_context': enhanced_context,
        'context_length': len(enhanced_context),
        'applied_template': 'chain_of_thought'
    }


def _apply_few_shot_template(context: str) -> Dict[str, Any]:
    """
    应用少样本学习模板
    """
    enhanced_context = f"""
### 少样本学习框架

**任务**: {context}

以下是处理类似任务的示例对，用于指导模型行为：

**示例1**:
输入: 分析电商平台架构需求
输出: 
- 识别核心组件: 用户管理、商品管理、订单管理、支付系统
- 分析技术栈: 前端、后端、数据库、缓存
- 确定交互模式: REST API、消息队列、事件驱动
- 验证安全要求: 认证、授权、数据加密

**示例2**:
输入: 设计API接口规范
输出:
- 定义数据模型: 实体结构、关系、约束
- 规范接口定义: 端点、参数、响应格式
- 配置错误处理: 错误代码、消息、恢复策略
- 优化性能考虑: 分页、缓存、限流

请参考以上示例模式，处理您的任务：{context}

请详细说明分析过程、决策依据和最终方案。
"""
    
    return {
        'enhanced_context': enhanced_context,
        'context_length': len(enhanced_context),
        'applied_template': 'few_shot'
    }


def _apply_verification_template(context: str) -> Dict[str, Any]:
    """
    应用验证检查模板
    """
    enhanced_context = f"""
### 验证检查框架

**待验证内容**: {context}

请执行以下验证步骤以确保质量：

1. **初步答案**:
   基于待验证内容，给出初步判断或方案：[暂空]

2. **逻辑一致性检查**:
   - 验证内容内部的逻辑一致性和连贯性
   - 检查是否存在矛盾或冲突信息
   - 确认因果关系的合理性

3. **事实准确性检查**:
   - 核实陈述的事实准确性
   - 验证技术要求的可行性
   - 检查约束条件的合理性

4. **完整性检查**:
   - 评估是否包含所有必要信息
   - 确认关键要素是否齐全
   - 检查边缘案例的覆盖

5. **最终确认**:
   基于以上检查，给出最终验证结论：[暂空]

请返回每个验证步骤的详细结果和最终确认。
"""
    
    return {
        'enhanced_context': enhanced_context,
        'context_length': len(enhanced_context),
        'applied_template': 'verification'
    }


def _apply_role_playing_template(context: str, role: str) -> Dict[str, Any]:
    """
    应用角色扮演模板
    """
    enhanced_context = f"""
### {role}角色扮演分析

**任务**: {context}

请以{role}的专业身份和视角分析此任务：

1. **角色专业能力识别**:
   作为{role}，我具备以下专业能力：
   - [专业技能1]
   - [专业技能2]
   - [专业技能3]

2. **专业视角分析**:
   从{role}的专业角度分析任务的关键要素：
   - 核心关注点
   - 潜在挑战
   - 最佳实践方法

3. **专业建议制定**:
   基于{role}的专业知识，提供具体可行的建议：
   - [建议1: 具体操作]
   - [建议2: 注意事项]
   - [建议3: 成功要点]

4. **专业决策推荐**:
   从{role}的专业视角做出最优决策推荐，并说明理由。

请返回{role}视角的专业分析、建议和决策。
"""
    
    return {
        'enhanced_context': enhanced_context,
        'context_length': len(enhanced_context),
        'applied_template': 'role_playing'
    }


def _apply_understanding_template(context: str) -> Dict[str, Any]:
    """
    应用深度理解模板
    """
    enhanced_context = f"""
### 深度理解框架

**待理解内容**: {context}

请从以下维度进行深入理解：

1. **核心目标**:
   - 此内容的首要目标是什么？
   - 预期达成什么成果？
   - 成功的标准如何定义？

2. **关键要素**:
   - 包含哪些重要组成部分？
   - 涉及哪些关键技术/概念？
   - 有哪些主要参与者？

3. **约束条件**:
   - 有哪些限制和约束？
   - 前提假设是什么？
   - 资源和时间限制？

4. **成功标准**:
   - 如何判断任务完成得好？
   - 质量衡量指标是什么？
   - 用户满意度标准？

5. **潜在风险**:
   - 可能面临哪些挑战？
   - 存在什么风险因素？
   - 如何预防和缓解？

请返回深度理解结果和相关建议。
"""
    
    return {
        'enhanced_context': enhanced_context,
        'context_length': len(enhanced_context),
        'applied_template': 'understanding'
    }