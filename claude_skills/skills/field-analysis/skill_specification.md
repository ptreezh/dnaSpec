# Field Analysis场域分析技能规范

## 技能定义
**技能名称**: field-analysis  
**中文名称**: 布迪厄场域分析专家  
**应用场景**: 教育场域、学术场域、文化场域等中国本土场域的布迪厄理论分析

## 核心功能模块

### 1. 场域边界识别模块（程序化规则）
```python
def identify_field_boundaries(social_context, field_indicators):
    """
    程序化的场域边界识别
    返回: {
        "field_type": "educational|academic|cultural|economic|political",
        "boundary_markers": [],
        "key_institutions": [],
        "confidence_level": float
    }
    """
    field_patterns = {
        "educational": {
            "institutions": ["学校", "大学", "研究机构", "教育部"],
            "practices": ["教学", "研究", "评估", "认证"],
            "stakes": ["知识传承", "能力培养", "社会流动"]
        },
        "academic": {
            "institutions": ["期刊", "学会", "评审委员会", "研究机构"],
            "practices": ["发表", "评审", "引用", "合作"],
            "stakes": ["学术声誉", "知识权威", "研究资源"]
        },
        "cultural": {
            "institutions": ["媒体", "艺术机构", "文化组织", "出版商"],
            "practices": ["创作", "评论", "传播", "消费"],
            "stakes": ["文化认可", "审美权威", "市场价值"]
        }
    }
```

### 2. 资本分布分析（渐进式披露）
```python
class CapitalDistributionAnalyzer:
    def __init__(self):
        self.capital_types = {
            "economic_capital": {
                "indicators": ["收入", "资产", "投资", "资助"],
                "measurement": "quantitative"
            },
            "cultural_capital": {
                "indicators": ["学历", "知识", "技能", "品味"],
                "measurement": "mixed_methods"
            },
            "social_capital": {
                "indicators": ["人脉", "网络", "声望", "影响力"],
                "measurement": "qualitative_weighted"
            },
            "symbolic_capital": {
                "indicators": ["认可", "荣誉", "地位", "权威"],
                "measurement": "qualitative"
            }
        }
    
    def progressive_analysis(self, field_data, analysis_depth):
        """
        渐进式披露：根据分析深度提供不同层次的资本分析
        depth=1: 基础资本识别和量化
        depth=2: 资本转换关系分析
        depth=3: 资本权力动态分析
        """
        if analysis_depth == 1:
            return self.basic_capital_assessment(field_data)
        elif analysis_depth == 2:
            return self.capital_conversion_analysis(field_data)
        else:
            return self.power_dynamics_analysis(field_data)
```

### 3. 习性模式分析（定性定量结合）
```python
class HabitusAnalyzer:
    def __init__(self):
        self.quantitative_patterns = [
            "behavioral_frequency",    # 行为频率
            "choice_consistency",      # 选择一致性
            "social_network_patterns", # 社交网络模式
            "resource_allocation"      # 资源分配模式
        ]
        
        self.qualitative_dimensions = [
            "disposition_patterns",   # 倾向性模式
            "internalized_structures", # 内化结构
            "practical_sense",         # 实践感
            "embodied_history"         # 具身化历史
        ]
    
    def mixed_methods_habitus_analysis(self, individual_data, field_context):
        """
        定性定量有机结合的习性分析
        """
        # 定量部分：行为模式统计
        quant_patterns = self.analyze_behavioral_patterns(individual_data)
        
        # 定性部分：基于AI的深度质性分析
        qual_context = self.prepare_habitus_context(individual_data, field_context)
        qual_insights = self.ai_habitus_interpretation(qual_context)
        
        return self.integrated_habitus_profile(quant_patterns, qual_insights)
```

### 4. 自主性评估（程序化+定性）
```python
class FieldAutonomyAssessment:
    def __init__(self):
        self.autonomy_indicators = {
            "internal": {
                "rules_autonomy": 0.8,      # 内部规则自主性
                "evaluation_autonomy": 0.7, # 评价标准自主性
                "reproduction_mechanism": 0.6 # 再生产机制自主性
            },
            "external": {
                "economic_pressure": 0.3,    # 经济压力影响
                "political_influence": 0.4,  # 政治影响
                "media_dependency": 0.5     # 媒体依赖度
            }
        }
    
    def calculate_autonomy_score(self, field_structure, external_influences):
        """
        计算场域自主性得分
        """
        internal_score = self.internal_autonomy_metrics(field_structure)
        external_score = self.external_dependency_metrics(external_influences)
        
        return {
            "overall_autonomy": internal_score - external_score,
            "dimensional_scores": {...},
            "autonomy_dynamics": self.analyze_autonomy_trends(field_structure)
        }
```

## 渐进式披露设计

### 层次1：基础场域识别
- **必需上下文**：社会现象描述
- **输出**：场域类型和基本边界
- **程序化程度**：85%

### 层次2：资本结构分析
- **必需上下文**：场域参与者信息
- **输出**：四种资本分布图
- **程序化程度**：65%

### 层次3：习性模式识别
- **必需上下文**：个体行为数据和背景
- **输出**：习性结构分析
- **程序化程度**：45%

### 层次4：场域动力机制
- **必需上下文**：完整场域历史和互动
- **输出**：场域运行机制和预测
- **程序化程度**：25%

## 中国本土化适配

### 教育场域中国特征
```python
class ChineseEducationalField(FieldAnalyzer):
    def localized_patterns(self):
        return {
            "specific_capitals": {
                "guanxi_capital": ["关系网络", "人情资源", "背景支持"],
                "policy_capital": ["政策理解", "体制适应", "行政资源"],
                "exam_capital": ["应试能力", "考试技巧", "升学履历"]
            },
            "field_dynamics": {
                "gaokao_influence": 0.9,      # 高考影响
                "educational_hierarchy": 0.8,   # 教育层级性
                "regional_disparity": 0.7      # 地区差异
            }
        }
```

### 学术场域中国特征
```python
class ChineseAcademicField(FieldAnalyzer):
    def localized_patterns(self):
        return {
            "specific_capitals": {
                "administrative_capital": ["行政职务", "管理权限"],
                "project_capital": ["项目获得", "经费申请"],
                "publication_capital": ["SCI论文", "核心期刊"]
            },
            "field_dynamics": {
                "centralization_level": 0.8,   # 集权化程度
                "evaluation_system": 0.9,      # 评价体系
                "international_pressure": 0.6  # 国际化压力
            }
        }
```

## 规则提示词模板

### 场域边界识别提示词
```
你是一位布迪厄场域分析专家，正在分析以下中国社会现象：

**现象描述**: {phenomenon_description}
**社会背景**: {social_context}

请识别：
1. 这属于哪种类型的场域？（教育/学术/文化/经济/政治）
2. 场域边界的关键指标是什么？
3. 核心参与者和制度有哪些？
4. 场域内的利害关系是什么？

基于中国本土特色，考虑：
- 体制性因素
- 文化传统影响
- 政策环境
- 社会关系网络
```

### 资本转换分析提示词
```
基于场域识别结果，分析资本分布和转换：

**场域类型**: {field_type}
**参与者信息**: {participants_data}
**资源分布**: {resource_distribution}

请分析：
1. 四种资本（经济、文化、社会、象征）的具体表现
2. 资本之间的转换关系和效率
3. 资本不平等的具体表现
4. 中国特色资本形式（如关系资本、政策资本）

特别关注：
- 资本积累的策略性
- 资本转换的制度约束
- 资本再生产的社会机制
```

## 应用场景映射

### 高等教育场域分析
```python
class HigherEducationField(ChineseEducationalField):
    def specific_analysis(self):
        return {
            "key_positions": ["教授", "院长", "校长", "学科带头人"],
            "critical_capitals": ["学术声誉", "行政职务", "项目经费", "学生质量"],
            "field_logic": ["学术卓越", "行政效率", "社会服务", "经济效益"],
            "conflict_points": ["学术vs行政", "教学vs研究", "本土vs国际"]
        }
```

### 科研机构场域分析
```python
class ResearchInstitutionField(ChineseAcademicField):
    def specific_analysis(self):
        return {
            "key_positions": ["首席科学家", "课题组长", "研究员", "博士后"],
            "critical_capitals": ["科研成果", "项目经费", "团队规模", "政策支持"],
            "field_logic": ["创新突破", "经费充足", "团队稳定", "社会影响"],
            "conflict_points": ["基础vs应用", "个人vs团队", "自由vs任务"]
        }
```

## 实现规范

### 技能接口
```python
def analyze_bourdieu_field(
    phenomenon_description: str,
    field_context: dict,
    analysis_depth: int = 1,
    localization_focus: str = "china_specific",
    capital_measurement: str = "mixed_methods"
) -> dict:
    """
    布迪厄场域分析主入口
    
    Args:
        phenomenon_description: 待分析现象描述
        field_context: 场域背景信息
        analysis_depth: 分析深度 (1-4)
        localization_focus: 本土化重点
        capital_measurement: 资本测量方式
    
    Returns:
        dict: 结构化场域分析结果
    """
```

### 输出格式
```json
{
    "field_identification": {
        "field_type": "...",
        "boundary_markers": [...],
        "key_institutions": [...],
        "confidence_score": 0.85
    },
    "capital_distribution": {
        "economic_capital": {...},
        "cultural_capital": {...},
        "social_capital": {...},
        "symbolic_capital": {...},
        "local_specific_capitals": {...}
    },
    "habitus_patterns": {
        "behavioral_patterns": {...},
        "disposition_structures": {...},
        "practical_sense_analysis": {...}
    },
    "field_dynamics": {
        "autonomy_score": float,
        "power_relations": {...},
        "conflict_zones": [...],
        "transformation_trends": [...]
    }
}
```

## 质量保证

### 验证清单
- [ ] 场域边界准确性
- [ ] 资本类型完整性
- [ ] 本土化适配性
- [ ] 定性定量平衡
- [ ] 实践指导价值

### 限制条件
- 数据质量：需要足够的实证材料
- 文化敏感性：考虑中国特殊国情
- 时间范围：建议关注当代变化趋势
- 分析层次：从基础到渐进深入

## 工具集成

### 资本量化工具
```python
def quantify_capital_holding(individual_data, field_standards):
    """
    量化个体资本持有量
    """
    return {
        "economic_score": float,
        "cultural_score": float,
        "social_score": float,
        "symbolic_score": float,
        "local_specific_scores": {...}
    }
```

### 场域动力学模拟
```python
def simulate_field_dynamics(field_structure, intervention_scenarios):
    """
    模拟场域动力学变化
    """
    return {
        "baseline_projection": {...},
        "intervention_effects": {...},
        "stability_assessment": {...},
        "critical_tipping_points": [...]
    }
```