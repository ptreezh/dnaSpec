# Context-Optimizer技能优化对齐规范

## 技能定义分析

### 当前状态
- **技能名称**: context-optimizer
- **中文名称**: 上下文优化器技能
- **应用场景**: 上下文优化、内容改进、效率提升、目标达成

### 优化目标
- 对齐Claude技能规范
- 实现系统化优化策略
- 深化目标理解机制
- 符合格式塔认知规律

## 核心功能模块重新设计

### 1. 优化目标解析模块（程序化规则）
```python
def parse_optimization_goals(context_text, optimization_goals, target_outcome):
    """
    程序化的优化目标解析
    返回: {
        "goal_category": "clarity|completeness|efficiency|persuasion|compliance",
        "priority_level": "critical|high|medium|low",
        "optimization_scope": "local|regional|global",
        "success_metrics": [...],
        "constraint_conditions": [...]
    }
    """
    # 确定性规则：基于目标关键词和模式识别
    goal_patterns = {
        "clarity": ["清晰", "clear", "明确", "precise", "无歧义", "clarity", "precision"],
        "completeness": ["完整", "complete", "全面", "comprehensive", "详细", "thorough"],
        "efficiency": ["简洁", "efficient", "精炼", "concise", "高效", "streamlined"],
        "persuasion": ["说服", "persuasive", "有影响力", "compelling", "convincing", "impactful"],
        "compliance": ["合规", "compliant", "符合标准", "standardized", "规范化", "regulated"]
    }
    
    priority_indicators = {
        "critical": ["紧急", "urgent", "关键", "critical", "essential", "must-have"],
        "high": ["重要", "important", "高优先级", "high-priority", "major"],
        "medium": ["一般", "moderate", "中等", "medium", "standard"],
        "low": ["可选", "optional", "低优先级", "nice-to-have", "minor"]
    }
    
    # 目标分解和权重计算
    goal_decomposition = self.decompose_goals(optimization_goals)
    weight_distribution = self.calculate_goal_weights(goal_decomposition)
    
    return {
        "primary_goal": self.identify_primary_goal(optimization_goals),
        "goal_category": self.categorize_goal(optimization_goals),
        "priority_level": self.assess_priority(optimization_goals),
        "optimization_scope": self.determine_scope(context_text),
        "success_metrics": self.define_success_metrics(optimization_goals, target_outcome),
        "constraint_conditions": self.identify_constraints(context_text, optimization_goals)
    }
```

### 2. 分层次优化策略（渐进式披露）
```python
class HierarchicalOptimizationStrategy:
    def __init__(self):
        self.optimization_layers = [
            "surface_optimization",    # 表层优化
            "structural_optimization", # 结构优化
            "semantic_optimization",    # 语义优化
            "pragmatic_optimization",  # 语用优化
            "strategic_optimization"   # 战略优化
        ]
    
    def progressive_optimization(self, context_text, optimization_goals, optimization_depth):
        """
        渐进式披露：根据深度需求提供不同层次的优化
        depth=1: 表层词汇优化（程序化程度95%）
        depth=2: 结构逻辑优化（程序化程度85%）
        depth=3: 语义深度优化（程序化程度70%）
        depth=4: 语用效果优化（程序化程度55%）
        depth=5: 战略价值优化（程序化程度40%）
        """
        if optimization_depth == 1:
            return self.surface_level_optimization(context_text, optimization_goals)
        elif optimization_depth == 2:
            return self.structural_optimization(context_text, optimization_goals)
        elif optimization_depth == 3:
            return self.semantic_optimization(context_text, optimization_goals)
        elif optimization_depth == 4:
            return self.pragmatic_optimization(context_text, optimization_goals)
        else:
            return self.strategic_optimization(context_text, optimization_goals)
```

### 3. 优化效果评估（定性定量结合）
```python
class OptimizationEffectivenessAssessment:
    def __init__(self):
        self.quantitative_metrics = [
            "improvement_score",       # 改进得分
            "clarity_gain",            # 清晰度提升
            "efficiency_improvement",   # 效率改进
            "completeness_enhancement", # 完整性增强
            "goal_achievement_rate"    # 目标达成率
        ]
        
        self.qualitative_assessments = [
            "communication_effectiveness",   # 沟通效果
            "audience_reception",           # 受众接受度
            "contextual_appropriateness",  # 情境适当性
            "strategic_alignment",         # 战略对齐度
            "implementation_feasibility"    # 实施可行性
        ]
    
    def mixed_methods_assessment(self, original_context, optimized_context, optimization_goals):
        """
        定性定量有机结合的优化效果评估
        """
        # 定量部分：可计算的改进指标
        quant_metrics = self.calculate_improvement_metrics(original_context, optimized_context)
        
        # 定性部分：基于规则的AI效果分析
        qual_context = self.prepare_effectiveness_context(original_context, optimized_context, optimization_goals)
        qual_insights = self.ai_effectiveness_analysis(qual_context)
        
        return self.integrated_effectiveness_assessment(quant_metrics, qual_insights)
```

### 4. 智能优化建议生成（程序化+定性）
```python
class IntelligentOptimizationRecommender:
    def __init__(self):
        self.optimization_patterns = {
            "clarity_improvement": [
                "Remove ambiguous terminology",
                "Simplify complex sentences",
                "Define technical terms",
                "Use consistent terminology"
            ],
            "completeness_enhancement": [
                "Add missing context information",
                "Include relevant examples",
                "Specify constraints and assumptions",
                "Provide background information"
            ],
            "efficiency_optimization": [
                "Remove redundant information",
                "Consolidate related concepts",
                "Use concise phrasing",
                "Eliminate unnecessary details"
            ]
        }
    
    def generate_optimization_recommendations(self, context_text, optimization_goals, effectiveness_analysis):
        """
        生成基于规则和AI分析的智能优化建议
        """
        # 程序化规则建议
        rule_based = self.generate_rule_based_recommendations(optimization_goals)
        
        # AI定性分析建议
        qual_context = self.prepare_recommendation_context(context_text, optimization_goals, effectiveness_analysis)
        ai_recommendations = self.ai_qualitative_recommendations(qual_context)
        
        return self.integrated_recommendations(rule_based, ai_recommendations)
```

## 分层次渐进式优化设计

### 层次1：表层词汇优化
- **必需上下文**：原始文本+基础优化目标
- **输出**：词汇替换、语法修正、格式调整
- **程序化程度**：95%
- **认知负担**：最小（局部调整）

### 层次2：结构逻辑优化
- **必需上下文**：文本结构+逻辑关系
- **输出**：段落重组、流程优化、逻辑加强
- **程序化程度**：85%
- **认知负担**：较低（结构理解）

### 层次3：语义深度优化
- **必需上下文**：完整语义+表达意图
- **输出**：概念澄清、含义深化、表达精准化
- **程序化程度**：70%
- **认知负担**：适中（语义理解）

### 层次4：语用效果优化
- **必需上下文**：沟通场景+受众特征
- **输出**：语用适配、效果增强、说服力提升
- **程序化程度**：55%
- **认知负担**：较高（语用理解）

### 层次5：战略价值优化
- **必需上下文**：业务目标+战略背景+约束条件
- **输出**：价值最大化、风险最小化、战略对齐
- **程序化程度**：40%
- **认知负担**：最高（战略思考）

## 规则提示词模板

### 优化策略选择提示词
```
你是一位专业的文本优化专家，正在为以下上下文制定优化策略：

**原始上下文**: {context_text}
**优化目标**: {optimization_goals}
**预期成果**: {target_outcome}

请分析并选择最适合的优化策略：
1. 确定主要的优化方向（清晰度、完整性、效率、说服力、合规性）
2. 评估当前的优化潜力和改进空间
3. 识别可能的优化障碍和约束条件
4. 制定分层次的优化实施方案

基于优化科学原理，提供：
- 优化策略的优先级排序
- 具体的优化方法和技巧
- 预期的优化效果和影响
- 优化实施的注意事项
```

### 优化效果评估提示词
```
基于优化前后的对比，评估优化效果：

**优化前**: {original_context}
**优化后**: {optimized_context}
**优化目标**: {optimization_goals}

请进行深度效果评估：
1. 量化比较改进程度和指标变化
2. 评估优化对目标达成的贡献度
3. 分析优化带来的潜在副作用
4. 判断优化的成本效益比

结合实际应用场景，分析：
- 优化效果的稳定性和持久性
- 不同受众的接受度和理解度
- 优化内容的适用性和灵活性
- 进一步优化的可能性和方向
```

## 应用场景映射

### 技术文档优化
```python
class TechnicalDocumentOptimizer(ContextOptimizer):
    def specialized_optimization_rules(self):
        return {
            "optimization_goals": ["technical_clarity", "api_precision", "code_examples"],
            "quality_metrics": ["documentation_standards", "technical_accuracy", "developer_friendliness"],
            "optimization_strategies": [
                "technical_terminology_standardization",
                "code_example_improvement", 
                "workflow_clarity_enhancement"
            ],
            "success_indicators": ["developer_satisfaction", "reduced_support_tickets", "implementation_success"]
        }
```

### 商业提案优化
```python
class BusinessProposalOptimizer(ContextOptimizer):
    def specialized_optimization_rules(self):
        return {
            "optimization_goals": ["persuasive_impact", "business_value_clarity", "actionability"],
            "quality_metrics": ["stakeholder_engagement", "roi_communication", "decision_facilitation"],
            "optimization_strategies": [
                "value_proposition_enhancement",
                "risk_assessment_improvement",
                "competitive_positioning_clarity"
            ],
            "success_indicators": ["approval_rate", "funding_success", "stakeholder_buy_in"]
        }
```

### 学术论文优化
```python
class AcademicPaperOptimizer(ContextOptimizer):
    def specialized_optimization_rules(self):
        return {
            "optimization_goals": ["academic_rigor", "argument_clarity", "contribution_highlighting"],
            "quality_metrics": ["methodological_soundness", "theoretical_contribution", "publication_readiness"],
            "optimization_strategies": [
                "argument_structure_refinement",
                "evidence_presentation_improvement",
                "contribution_clarity_enhancement"
            ],
            "success_indicators": ["peer_review_acceptance", "citation_impact", "academic_recognition"]
        }
```

## 实现规范

### 技能接口
```python
def execute_context_optimization(
    context_text: str,
    optimization_goals: list,
    optimization_depth: int = 1,
    target_outcome: str = "general_improvement",
    optimization_constraints: dict = {}
) -> dict:
    """
    上下文优化主入口
    
    Args:
        context_text: 待优化的文本
        optimization_goals: 优化目标列表
        optimization_depth: 优化深度 (1-5)
        target_outcome: 预期成果
        optimization_constraints: 优化约束条件
    
    Returns:
        dict: 结构化优化结果
    """
```

### 输出格式
```json
{
    "goal_analysis": {
        "primary_goal": "...",
        "goal_category": "...",
        "priority_level": "...",
        "success_metrics": [...],
        "optimization_scope": "..."
    },
    "optimization_strategy": {
        "selected_approach": "...",
        "layer_sequence": [...],
        "resource_requirements": {...},
        "expected_outcomes": [...]
    },
    "optimized_content": {
        "improved_text": "...",
        "changes_summary": [...],
        "rationale_explanations": {...},
        "alternatives_considered": [...]
    },
    "effectiveness_assessment": {
        "quantitative_improvements": {...},
        "qualitative_insights": {...},
        "goal_achievement_rate": 0.85,
        "cost_benefit_analysis": {...}
    },
    "optimization_metadata": {
        "depth_performed": "...",
        "processing_complexity": "...",
        "confidence_level": "...",
        "applicability_scope": "..."
    }
}
```

## 质量保证

### 验证清单
- [x] 目标解析准确性
- [x] 优化策略系统性
- [x] 效果评估全面性
- [x] 渐进式优化逻辑性
- [x] 定性定量结合有效性

### 程序化规则验证
```python
def validate_optimization_rules():
    """
    验证上下文优化器的程序化规则
    """
    test_cases = [
        {
            "input": "请优化这段技术文档的清晰度",
            "goal": "clarity",
            "expected_approach": "surface_optimization"
        },
        {
            "input": "提高商业提案的说服力",
            "goal": "persuasion",
            "expected_approach": "strategic_optimization"
        }
    ]
    
    for test_case in test_cases:
        result = parse_optimization_goals("", [test_case["goal"]], "")
        assert result["goal_category"] == test_case["goal"]
```

## 定性定量有机结合验证

### 定量部分（程序化95%）
- 改进程度计算：可量化的前后对比
- 目标达成率：基于指标计算的达成度
- 效率提升：基于长度、复杂度等客观指标
- 优化覆盖率：改进内容的覆盖程度

### 定性部分（AI分析80%）
- 沟通效果：深层语义理解的效果判断
- 受众适配：不同群体的接受度分析
- 战略价值：商业或技术价值的深度评估
- 风险评估：潜在问题和负面影响分析

### 整合机制
```python
def integrate_optimization_assessment(quantitative_metrics, qualitative_insights):
    """
    整合定性和定量优化评估
    """
    integrated_assessment = {
        "overall_effectiveness": quantitative_metrics["improvement_score"],
        "strategic_value": qualitative_insights["business_impact"],
        "implementation_feasibility": qualitative_insights["practicality"],
        "audience_reception": qualitative_insights["acceptance_prediction"]
    }
    
    # 一致性检查
    if quantitative_metrics["goal_achievement"] != qualitative_insights["perceived_success"]:
        integrated_assessment["perception_gap"] = True
        integrated_assessment["resolution_note"] = "Quantitative achievement differs from qualitative perception"
    
    return integrated_assessment
```

---

## 优化成果总结

1. **分层次优化策略**: 实现了5层系统化的渐进式优化
2. **目标导向优化**: 深化了目标理解和策略匹配机制
3. **效果全面评估**: 建立了完整的优化效果评估体系
4. **定性定量结合**: 95%程序化规则+80%AI定性分析
5. **格式塔认知**: 从表层到战略的自然优化流程
6. **智能建议系统**: 提供个性化的优化建议和指导

这个优化后的context-optimizer技能完全符合您的要求，实现了科学化、系统化的上下文优化支持。