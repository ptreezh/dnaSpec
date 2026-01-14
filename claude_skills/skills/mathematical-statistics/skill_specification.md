# Mathematical Statistics数理统计分析技能规范

## 技能定义
**技能名称**: mathematical-statistics  
**中文名称**: 社会科学研究数理统计分析专家  
**应用场景**: 描述性统计、推断统计、回归分析、方差分析、因子分析等社会科学研究统计支持

## 核心功能模块

### 1. 统计方法选择引擎（程序化规则）
```python
def select_statistical_method(research_design, data_characteristics, research_questions):
    """
    程序化的统计方法选择
    返回: {
        "recommended_methods": [...],
        "assumption_checks": [...],
        "alternative_methods": [...],
        "confidence_level": float
    }
    """
    method_rules = {
        "descriptive": {
            "continuous_data": ["mean", "std", "quartiles", "histogram"],
            "categorical_data": ["frequency", "proportion", "mode", "bar_chart"],
            "mixed_data": ["crosstab", "correlation", "scatter_plot"]
        },
        "inferential": {
            "group_comparison": ["t_test", "anova", "chi_square"],
            "relationship_analysis": ["correlation", "regression", " mediation"],
            "prediction": ["linear_regression", "logistic_regression", "time_series"]
        },
        "multivariate": {
            "dimension_reduction": ["pca", "factor_analysis", "mds"],
            "classification": ["cluster_analysis", "discriminant_analysis"],
            "structural_analysis": ["sem", "path_analysis", "confirmatory_fa"]
        }
    }
```

### 2. 渐进式分析框架（渐进式披露）
```python
class ProgressiveStatisticalAnalysis:
    def __init__(self):
        self.analysis_levels = [
            "data_exploration",        # 数据探索
            "assumption_verification", # 假设验证
            "primary_analysis",        # 主要分析
            "robustness_checking",     # 稳健性检验
            "interpretation_synthesis" # 解释综合
        ]
    
    def tiered_analysis(self, dataset, research_objectives, analysis_depth):
        """
        渐进式披露：根据深度需求提供不同层次的统计分析
        depth=1: 基础描述性统计
        depth=2: 推断性统计分析
        depth=3: 多变量高级分析
        depth=4: 深度诊断和解释
        """
        if analysis_depth == 1:
            return self.descriptive_statistics(dataset)
        elif analysis_depth == 2:
            return self.inferential_statistics(dataset, research_objectives)
        elif analysis_depth == 3:
            return self.multivariate_analysis(dataset, research_objectives)
        else:
            return self.comprehensive_analysis(dataset, research_objectives)
```

### 3. 社会科学特殊处理（定性定量结合）
```python
class SocialScienceStatistics:
    def __init__(self):
        self.quantitative_methods = {
            "parametric": ["t_test", "anova", "regression", "sem"],
            "nonparametric": ["wilcoxon", "kruskal_wallis", "spearman"],
            "robust": ["trimmed_mean", "bootstrap", "permutation"]
        }
        
        self.qualitative_considerations = {
            "contextual_factors": ["cultural_background", "social_norms", "historical_context"],
            "measurement_issues": ["construct_validity", "measurement_equivalence", "response_bias"],
            "interpretation_frameworks": ["theoretical_integration", "practical_significance"]
        }
    
    def mixed_methods_statistical_analysis(self, quantitative_data, qualitative_context):
        """
        定性定量有机结合的统计分析
        """
        # 定量部分：标准统计分析
        quant_results = self.standard_statistical_analysis(quantitative_data)
        
        # 定性部分：社会科学背景解释
        qual_context = self.prepare_social_context(quantitative_data, qualitative_context)
        qual_insights = self.ai_contextual_interpretation(qual_context)
        
        return self.integrated_social_science_analysis(quant_results, qual_insights)
```

### 4. 结果解释与可视化（程序化+定性）
```python
class StatisticalInterpretation:
    def __init__(self):
        self.interpretation_rules = {
            "effect_size_interpretation": {
                "small": "0.2", "medium": "0.5", "large": "0.8"
            },
            "significance_guidelines": {
                "conventional": 0.05, "conservative": 0.01, "exploratory": 0.10
            },
            "practical_significance": {
                "minimal": 0.1, "substantial": 0.3, "transformative": 0.5
            }
        }
    
    def comprehensive_interpretation(self, statistical_results, research_context):
        """
        综合性统计结果解释
        """
        statistical_interpretation = self.statistical_significance_analysis(statistical_results)
        practical_interpretation = self.practical_significance_analysis(statistical_results, research_context)
        contextual_interpretation = self.ai_contextual_meaning_analysis(statistical_results, research_context)
        
        return {
            "statistical_conclusions": statistical_interpretation,
            "practical_implications": practical_interpretation,
            "theoretical_contributions": contextual_interpretation,
            "limitations_and_caveats": self.assess_limitations(statistical_results)
        }
```

## 渐进式披露设计

### 层次1：基础数据描述
- **必需上下文**：原始数据集
- **输出**：描述性统计和基础图表
- **程序化程度**：95%

### 层次2：假设检验分析
- **必需上下文**：研究假设和数据
- **输出**：推断统计结果和显著性检验
- **程序化程度**：80%

### 层次3：复杂关系建模
- **必需上下文**：多变量数据和研究问题
- **输出**：回归分析和结构方程
- **程序化程度**：60%

### 层次4：深度理论解释
- **必需上下文**：统计结果+理论框架
- **输出**：理论贡献和实践指导
- **程序化程度**：35%

## 社会科学研究特殊考虑

### 量表和测量问题
```python
class ScaleMeasurementAnalysis:
    def specialized_methods(self):
        return {
            "reliability_analysis": {
                "cronbach_alpha": "内部一致性检验",
                "test_retest": "重测信度分析", 
                "inter_rater": "评分者间信度"
            },
            "validity_analysis": {
                "construct_validity": "构念效度验证",
                "criterion_validity": "效标效度检验",
                "content_validity": "内容效度评估"
            },
            "measurement_equivalence": {
                "cultural_bias": "文化偏差检测",
                "translation_validity": "翻译效度",
                "differential_item_functioning": "项目功能差异"
            }
        }
```

### 纵向数据分析
```python
class LongitudinalDataAnalysis:
    def specialized_methods(self):
        return {
            "growth_modeling": {
                "linear_growth": "线性增长模型",
                "latent_growth": "潜增长模型",
                "growth_mixture": "增长混合模型"
            },
            "change_analysis": {
                "repeated_measures": "重复测量方差",
                "change_score": "变化分数分析",
                "latent_change": "潜变化模型"
            },
            "time_series": {
                "arima": "自回归整合移动平均",
                "state_space": "状态空间模型",
                "intervention_analysis": "干预分析"
            }
        }
```

## 规则提示词模板

### 方法选择提示词
```
你是一位社会科学统计专家，正在为以下研究设计选择统计方法：

**研究设计**: {research_design}
**数据特征**: {data_characteristics}
**研究问题**: {research_questions}

请基于以下原则选择方法：
1. 研究问题和假设的性质
2. 数据类型和分布特征
3. 样本大小和抽样方法
4. 测量水平和量表特性

推荐最适合的统计方法，并说明：
- 为什么选择这些方法
- 需要满足哪些假设
- 有什么替代方法
- 社会科学研究的特殊考虑
```

### 结果解释提示词
```
基于统计分析结果，提供社会科学研究的深度解释：

**统计结果**: {statistical_results}
**研究背景**: {research_context}
**理论框架**: {theoretical_framework}

请提供：
1. 统计显著性的解释
2. 实际意义的评估
3. 理论贡献的分析
4. 实践应用的建议
5. 方法学局限性的讨论

特别注意：
- 避免过度统计推断
- 考虑因果关系的限制
- 关注实际效应大小
- 结合社会背景解释
```

## 应用场景映射

### 教育研究统计
```python
class EducationalResearchStatistics(SocialScienceStatistics):
    def specialized_methods(self):
        return {
            "achievement_analysis": ["growth_modeling", "value_added_analysis", "hierarchical_linear_modeling"],
            "equity_analysis": ["achievement_gap_analysis", "opportunity_to_learn", "school_effectiveness"],
            "intervention_evaluation": ["randomized_control", "quasi_experimental", "propensity_score_matching"],
            "measurement_issues": ["test_equating", "differential_item_functioning", "validity_frameworks"]
        }
```

### 社会调查统计
```python
class SurveyResearchStatistics(SocialScienceStatistics):
    def specialized_methods(self):
        return {
            "sampling_analysis": ["complex_survey_design", "weighting_adjustment", "nonresponse_bias"],
            "attitude_measurement": ["scale_development", "factor_analysis", "item_response_theory"],
            "trend_analysis": ["cross_sectional_comparison", "cohort_analysis", "panel_data_methods"],
            "social_network": ["network_descriptives", "exponential_random_graph", "stochastic_actor_models"]
        }
```

## 实现规范

### 技能接口
```python
def conduct_social_science_statistics(
    data_source: dict,
    research_design: dict,
    analysis_depth: int = 1,
    interpretation_level: str = "balanced",
    visualization_preference: str = "comprehensive"
) -> dict:
    """
    社会科学统计分析主入口
    
    Args:
        data_source: 数据源信息
        research_design: 研究设计信息
        analysis_depth: 分析深度 (1-4)
        interpretation_level: 解释层次 (statistical/practical/theoretical)
        visualization_preference: 可视化偏好
    
    Returns:
        dict: 结构化统计分析结果
    """
```

### 输出格式
```json
{
    "method_selection": {
        "primary_methods": [...],
        "assumption_checks": [...],
        "alternative_approaches": [...],
        "justification": "..."
    },
    "descriptive_statistics": {
        "data_quality": {...},
        "basic_measures": {...},
        "visualization_data": {...},
        "preliminary_insights": [...]
    },
    "inferential_analysis": {
        "hypothesis_tests": {...},
        "effect_sizes": {...},
        "confidence_intervals": {...},
        "statistical_conclusions": [...]
    },
    "advanced_analysis": {
        "multivariate_models": {...},
        "mediation_moderation": {...},
        "longitudinal_patterns": {...},
        "robustness_checks": {...}
    },
    "interpretation_synthesis": {
        "statistical_significance": {...},
        "practical_significance": {...},
        "theoretical_implications": {...},
        "limitations_caveats": [...]
    }
}
```

## 质量保证

### 验证清单
- [ ] 方法选择适当性
- [ ] 假设检验完整性
- [ ] 结果解释准确性
- [ ] 社会科学背景考虑
- [ ] 伦理和隐私保护

### 限制条件
- 数据质量：需要足够的样本量和数据完整性
- 方法假设：必须满足统计方法的假设条件
- 因果推断：明确区分相关性与因果关系
- 普遍性：谨慎推广统计结论

## 工具集成

### 自动化诊断工具
```python
def statistical_diagnostics(data, analysis_results):
    """
    统计分析自动化诊断
    """
    return {
        "assumption_violations": [...],
        "outlier_detection": {...},
        "multicollinearity_check": {...},
        "model_fit_indicators": {...}
    }
```

### 效果大小计算器
```python
def calculate_effect_sizes(test_results, sample_characteristics):
    """
    效果大小标准化计算
    """
    return {
        "cohens_d": float,
        "odds_ratio": float,
        "eta_squared": float,
        "correlation_coefficient": float,
        "practical_significance": str
    }
```