"""
认知模板技能 - 重构版本
符合DNASPEC标准化技能接口规范
"""
from typing import Dict, Any
from ..skill_base import BaseSkill, DetailLevel


class CognitiveTemplateSkill(BaseSkill):
    """认知模板技能 - 使用AI模型原生智能应用认知模板"""
    
    def __init__(self):
        super().__init__(
            name="cognitive-template",
            description="使用AI模型原生智能应用认知模板来结构化复杂任务"
        )
        
        self.templates = {
            'chain_of_thought': '思维链推理模板',
            'few_shot': '少样本学习模板',
            'verification': '验证检查模板',
            'role_playing': '角色扮演模板',
            'understanding': '深度理解模板'
        }
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """执行认知模板应用逻辑"""
        if not input_text.strip():
            return {
                'success': False,
                'error': '上下文不能为空',
                'original_context': input_text
            }
        
        template_type = options.get('template', 'chain_of_thought')
        role = options.get('role', '专家')
        
        if template_type not in self.templates:
            return {
                'success': False,
                'error': f'未知模板: {template_type}',
                'available_templates': list(self.templates.keys()),
                'original_context': input_text
            }
        
        template_desc = self.templates[template_type]
        
        if template_type == 'chain_of_thought':
            # 构造思维链模板应用结果
            enhanced_content = f"""
### 思维链认知模板应用

**原始任务**: {input_text}

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
            template_structure = [
                "应用认知框架",
                "结构化输出",
                "验证结果"
            ]
        
        elif template_type == 'few_shot':
            enhanced_content = f"""
### 少样本学习模板应用

**任务**: {input_text}

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

请参考以上示例模式，处理您的任务：{input_text}

请详细说明分析过程、决策依据和最终方案。
"""
            template_structure = [
                "提供示例对",
                "模式识别",
                "应用示例"
            ]
        
        elif template_type == 'verification':
            enhanced_content = f"""
### 验证检查模板应用

**待验证内容**: {input_text}

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
            template_structure = [
                "初步验证",
                "多维度检查",
                "最终确认"
            ]
        
        elif template_type == 'role_playing':
            enhanced_content = f"""
### {role}角色扮演分析

**任务**: {input_text}

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
            template_structure = [
                "角色能力识别",
                "专业视角分析",
                "建议制定",
                "决策推荐"
            ]
        
        elif template_type == 'understanding':
            enhanced_content = f"""
### 深度理解框架

**待理解内容**: {input_text}

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
            template_structure = [
                "目标理解",
                "要素分析",
                "约束识别",
                "标准定义",
                "风险评估"
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
        """根据详细程度格式化输出结果"""
        if detail_level == DetailLevel.BASIC:
            # 基础级别只返回核心信息
            if result_data.get('success', False):
                return {
                    'template_type': result_data['template_type'],
                    'enhanced_context': result_data['enhanced_context'][:200] + "..." if len(result_data['enhanced_context']) > 200 else result_data['enhanced_context']
                }
            else:
                return result_data
        elif detail_level == DetailLevel.STANDARD:
            # 标准级别返回标准信息
            return result_data
        else:  # DETAILED
            # 详细级别返回完整信息
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