# Validity & Reliability信度效度分析技能规范

## 技能定义
**技能名称**: validity-reliability  
**中文名称**: 研究信度效度分析专家  
**应用场景**: 内部一致性、重测信度、评分者信度、构念效度、内容效度、效标效度等全面分析

## 核心功能模块

### 1. 信度效度类型识别（程序化规则）
```python
def identify_validity_reliability_types(measurement_design, research_context):
    """
    程序化的信度效度类型识别
    返回: {
        "required_reliability": [...],
        "required_validity": [...],
        "priority_levels": {...},
        "assessment_methods": [...]
    }
    """
    validity_reliability_matrix = {
        "quantitative_research": {
            "reliability": ["internal_consistency", "test_retest", "parallel_forms", "inter_rater"],
            "validity": ["construct_validity", "content_validity", "criterion_validity", "convergent_discriminant"],
            "priority": ["reliability_first", "construct_central", "criterion_validation"]
        },
        "qualitative_research": {
            "reliability": ["inter_rater", "intra_rater", "stability", "transferability"],
            "validity": ["credibility", "transferability", "dependability", "confirmability"],
            "priority": ["credibility_central", "triangulation", "reflexivity"]
        },
        "mixed_methods": {
            "reliability": ["quantitative_reliability", "qualitative_consistency", "integration_reliability"],
            "validity": ["convergence_validity", "complementarity_validity", "expansion_validity"],
            "priority": ["integration_focus", "method_compatibility", "holistic_assessment"]
        }
    }
```

### 2. 渐进式评估流程（渐进式披露）
```python
class ProgressiveValidityReliabilityAssessment:
    def __init__(self):
        self.assessment_stages = [
            "preliminary_review",       # 初步审查
            "reliability_assessment",   # 信度评估
            "validity_assessment",      # 效度评估
            "integration_analysis",     # 整合分析
            "improvement_recommendations" # 改进建议
        ]
    
    def tiered_assessment(self, measurement_data, assessment_objectives, assessment_depth):
        """
        渐进式披露：根据深度需求提供不同层次的信效度评估
        depth=1: 基础信度指标计算
        depth=2: 核心效度分析
        depth=3: 综合信效度评估
        depth=4: 深度诊断和改进
        depth=5: 方法学优化建议
        """
        if assessment_depth == 1:
            return self.basic_reliability_assessment(measurement_data)
        elif assessment_depth == 2:
            return self.core_validity_analysis(measurement_data, assessment_objectives)
        elif assessment_depth == 3:
            return self.comprehensive_validity_reliability_assessment(measurement_data)
        elif assessment_depth == 4:
            return self.deep_diagnostic_analysis(measurement_data, assessment_objectives)
        else:
            return self.methodological_optimization_recommendations(measurement_data, assessment_objectives)
```

### 3. 量化分析引擎（定性定量结合）
```python
class QuantitativeValidityReliabilityAnalysis:
    def __init__(self):
        self.reliability_indicators = {
            "internal_consistency": {
                "cronbach_alpha": "内部一致性系数",
                "split_half": "分半信度",
                "kuder_richardson": "KR-20/KR-21系数",
                "omega": "组合信度"
            },
            "stability": {
                "test_retest": "重测信度",
                "parallel_forms": "复本信度",
                "alternate_forms": "替代形式信度"
            },
            "inter_rater": {
                "inter_rater_reliability": "评分者间信度",
                "intra_rater_reliability": "评分者内信度",
                "icc": "组内相关系数",
                "kappa": "科恩卡帕系数"
            }
        }
        
        self.validity_indicators = {
            "construct_validity": {
                "convergent_validity": "收敛效度",
                "discriminant_validity": "区分效度",
                "factor_structure": "因子结构效度",
                "nomological_network": "法则网络效度"
            },
            "criterion_validity": {
                "predictive_validity": "预测效度",
                "concurrent_validity": "同时效度",
                "postdictive_validity": "回顾效度",
                "incremental_validity": "增量效度"
            }
        }
    
    def mixed_methods_assessment(self, quantitative_data, qualitative_evidence, theoretical_framework):
        """
        定性定量有机结合的信效度评估
        """
        # 定量部分：标准信效度指标计算
        quant_results = self.calculate_standard_indicators(quantitative_data)
        
        # 定性部分：基于规则的深度效度分析
        qual_context = self.prepare_validity_context(qualitative_evidence, theoretical_framework)
        qual_insights = self.ai_validity_interpretation(qual_context)
        
        return self.integrated_validity_reliability_assessment(quant_results, qual_insights)
```

### 4. 质性研究信效度（特殊化处理）
```python
class QualitativeValidityReliability:
    def __init__(self):
        self.qualitative_criteria = {
            "credibility": {
                "techniques": ["prolonged_engagement", "persistent_observation", "triangulation", "member_checking"],
                "indicators": ["participant_validation", "peer_debriefing", "negative_case_analysis"],
                "assessment": "participant_reality_alignment"
            },
            "transferability": {
                "techniques": ["thick_description", "contextual_detail", "comparative_analysis"],
                "indicators": ["contextual_richness", "comparative_insight"],
                "assessment": "contextual_similarity_judgment"
            },
            "dependability": {
                "techniques": ["audit_trail", "stepwise_replication", "inquiry_audit"],
                "indicators": ["process_transparency", "method_consistency"],
                "assessment": "process_replicability"
            },
            "confirmability": {
                "techniques": ["reflexivity", "audit_trail", "triangulation"],
                "indicators": ["researcher_bias_control", "data_source_triangulation"],
                "assessment": "research_neutrality"
            }
        }
    
    def qualitative_rigor_assessment(self, qualitative_data, research_process, researcher_reflexivity):
        """
        质性研究严谨性评估
        """
        credibility_assessment = self.assess_credibility(qualitative_data, research_process)
        transferability_assessment = self.assess_transferability(qualitative_data)
        dependability_assessment = self.assess_dependability(research_process)
        confirmability_assessment = self.assess_confirmability(researcher_reflexivity)
        
        return {
            "overall_rigor_score": self.calculate_rigor_score(...),
            "dimensional_assessments": {...},
            "improvement_recommendations": self.qualitative_improvement_recommendations(...)
        }
```

## 渐进式披露设计

### 层次1：基础信度检查
- **必需上下文**：测量数据和基本设计
- **输出**：核心信度指标和基础建议
- **程序化程度**：95%

### 层次2：核心效度验证
- **必需上下文**：测量数据+理论框架
- **输出**：主要效度指标和理论检验
- **程序化程度**：80%

### 层次3：综合信效度评估
- **必需上下文**：完整测量体系
- **输出**：系统性信效度报告
- **程序化程度**：65%

### 层次4：深度诊断分析
- **必需上下文**：多次测量+对比数据
- **输出**：问题诊断和改进方案
- **程序化程度**：45%

### 层次5：方法学优化
- **必需上下文**：完整研究设计和实施
- **输出**：方法学改进和最佳实践
- **程序化程度**：25%

## 改进策略框架

### 量表优化策略
```python
class ScaleOptimizationStrategies:
    def optimization_methods(self):
        return {
            "item_analysis": {
                "difficulty_analysis": "项目难度分析",
                "discrimination_analysis": "项目区分度分析",
                "item_total_correlation": "项目-总分相关",
                "factor_loading": "因子载荷评估"
            },
            "scale_modification": {
                "item_removal": "问题项目删除",
                "item_rewording": "项目表述优化",
                "scale_restructuring": "量表结构重组",
                "response_format_improvement": "反应格式改进"
            },
            "pilot_testing": {
                "cognitive interviewing": "认知访谈",
                "think_aloud_protocol": "思维过程记录",
                "expert_review": "专家评审",
                "field_testing": "现场测试"
            }
        }
```

### 实施质量保障
```python
class ImplementationQualityAssurance:
    def quality_control_methods(self):
        return {
            "data_collection": {
                "standardization": "标准化培训",
                "supervision": "现场监督",
                "quality_monitoring": "质量监控",
                "contingency_planning": "应急预案"
            },
            "data_processing": {
                "data_cleaning": "数据清洗",
                "outlier_detection": "异常值检测",
                "missing_data_handling": "缺失数据处理",
                "consistency_checks": "一致性检查"
            },
            "interpretation_guidelines": {
                "score_interpretation": "分数解释指南",
                "error_margins": "误差边界说明",
                "contextual_factors": "情境因素考虑",
                "reporting_standards": "报告标准"
            }
        }
```

## 规则提示词模板

### 信度评估提示词
```
你是一位测量学专家，正在评估以下测量工具的信度：

**测量数据**: {measurement_data}
**工具描述**: {instrument_description}
**使用情境**: {use_context}

请评估：
1. 内部一致性是否达到可接受水平？
2. 重测信度是否满足稳定性要求？
3. 评分者间一致性是否足够？
4. 各种信度指标之间是否一致？

基于信度理论，提供：
- 具体信度系数和解释
- 潜在的可靠性问题
- 改进信度的具体建议
- 信度报告的标准格式
```

### 效度验证提示词
```
基于测量工具和理论框架，进行效度验证：

**测量工具**: {measurement_instrument}
**理论框架**: {theoretical_framework}
**效标数据**: {criterion_data}

请验证：
1. 构念效度是否充分体现理论概念？
2. 内容效度是否覆盖重要内容领域？
3. 效标效度是否有充分证据支持？
4. 各种效度证据是否相互支持？

结合现代效度理论，分析：
- 效度证据的整体性
- 测量解释的合理性
- 使用后果的考虑
- 效度论证的完整性
```

## 应用场景映射

### 教育评估工具
```python
class EducationalAssessmentValidityReliability(ValidityReliabilityAnalysis):
    def specialized_considerations(self):
        return {
            "test_construction": {
                "content_alignment": "内容与课程对应",
                "difficulty_appropriateness": "难度适当性",
                "bias_evaluation": "偏差评估",
                "accessibility": "可及性考虑"
            },
            "score_interpretation": {
                "norm_referenced": "常模参照解释",
                "criterion_referenced": "标准参照解释",
                "growth_monitoring": "成长监测",
                "diagnostic_use": "诊断性使用"
            },
            "educational_decisions": {
                "placement_decisions": "安置决策",
                "instructional_planning": "教学规划",
                "accountability": "问责制",
                "improvement_planning": "改进规划"
            }
        }
```

### 心理健康量表
```python
class MentalHealthScaleValidityReliability(ValidityReliabilityAnalysis):
    def specialized_considerations(self):
        return {
            "clinical_relevance": {
                "symptom_coverage": "症状覆盖度",
                "severity_differentiation": "严重程度区分",
                "change_sensitivity": "变化敏感性",
                "cultural_appropriateness": "文化适宜性"
            },
            "ethical_considerations": {
                "stigma_minimization": "污名化最小化",
                "confidentiality_protection": "保密保护",
                "informed_consent": "知情同意",
                "harm_prevention": "伤害预防"
            },
            "diagnostic_utility": {
                "screening_accuracy": "筛查准确性",
                "diagnostic_consistency": "诊断一致性",
                "treatment_monitoring": "治疗监测",
                "outcome_evaluation": "结果评估"
            }
        }
```

## 实现规范

### 技能接口
```python
def conduct_validity_reliability_analysis(
    measurement_data: dict,
    theoretical_framework: dict,
    research_context: dict,
    assessment_depth: int = 1,
    analysis_focus: str = "comprehensive"
) -> dict:
    """
    信度效度分析主入口
    
    Args:
        measurement_data: 测量数据
        theoretical_framework: 理论框架
        research_context: 研究情境
        assessment_depth: 评估深度 (1-5)
        analysis_focus: 分析重点 (reliability/validity/comprehensive)
    
    Returns:
        dict: 结构化信效度分析结果
    """
```

### 输出格式
```json
{
    "assessment_overview": {
        "measurement_type": "...",
        "research_context": "...",
        "assessment_scope": {...},
        "methodological_approach": "..."
    },
    "reliability_analysis": {
        "internal_consistency": {...},
        "stability_measures": {...},
        "inter_rater_agreement": {...},
        "overall_reliability_score": float
    },
    "validity_analysis": {
        "construct_validity": {...},
        "content_validity": {...},
        "criterion_validity": {...},
        "overall_validity_assessment": {...}
    },
    "qualitative_rigor": {
        "credibility_assessment": {...},
        "transferability_evaluation": {...},
        "dependability_verification": {...},
        "confirmability_review": {...}
    },
    "diagnostic_findings": {
        "identified_issues": [...],
        "problem_severity": {...},
        "root_causes": [...],
        "impact_assessment": {...}
    },
    "improvement_recommendations": {
        "short_term_actions": [...],
        "long_term_strategies": [...],
        "resource_requirements": {...},
        "implementation_timeline": {...}
    },
    "quality_assurance": {
        "monitoring_indicators": [...],
        "reporting_standards": {...},
        "documentation_requirements": [...],
        "ethical_considerations": [...]
    }
}
```

## 质量保证

### 验证清单
- [ ] 信效度指标完整性
- [ ] 理论框架一致性
- [ ] 方法学适当性
- [ ] 实践指导价值
- [ ] 伦理和公平性

### 限制条件
- 数据质量：需要足够样本和数据完整性
- 测量复杂度：考虑构念复杂性影响
- 情境依赖性：信效度具有情境特异性
- 改进约束：考虑实际可行性

## 工具集成

### 自动化诊断系统
```python
def automated_validity_reliability_diagnosis(measurement_data, benchmark_standards):
    """
    自动化信效度诊断
    """
    return {
        "compliance_check": {...},
        "risk_identification": {...},
        "performance_benchmarks": {...},
        "improvement_prioritization": {...}
    }
```

### 持续质量监测
```python
def continuous_quality_monitoring(longitudinal_data, quality_indicators):
    """
    持续质量监测系统
    """
    return {
        "trend_analysis": {...},
        "quality_alerts": [...],
        "maintenance_recommendations": [...],
        "performance_optimization": {...}
    }
```