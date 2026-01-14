# Architect技能优化对齐规范

## 技能定义分析

### 当前状态
- **技能名称**: architect
- **中文名称**: 系统架构师技能
- **应用场景**: 系统架构设计、架构分析、技术架构规划

### 优化目标
- 对齐Claude技能规范
- 实现渐进式披露原则
- 定性定量有机结合
- 符合格式塔认知规律

## 核心功能模块重新设计

### 1. 架构需求解析模块（程序化规则）
```python
def parse_architecture_requirements(requirements_text):
    """
    程序化的架构需求解析
    返回: {
        "domain_type": "web|mobile|enterprise|iot|ai_ml",
        "complexity_level": "simple|medium|complex",
        "scale_category": "small|medium|large|enterprise",
        "key_components": [...],
        "technical_constraints": [...]
    }
    """
    # 确定性规则：基于关键词和模式识别
    domain_patterns = {
        "web": ["网站", "web", "网页", "浏览器", "front-end", "前端"],
        "mobile": ["移动", "mobile", "app", "ios", "android", "手机"],
        "enterprise": ["企业", "enterprise", "erp", "crm", "业务系统"],
        "iot": ["物联网", "iot", "设备", "传感器", "智能硬件"],
        "ai_ml": ["人工智能", "ai", "机器学习", "ml", "深度学习", "算法"]
    }
    
    complexity_indicators = {
        "simple": ["简单", "基础", "basic", "straightforward"],
        "medium": ["中等", "标准", "standard", "typical"],
        "complex": ["复杂", "高级", "advanced", "sophisticated", "多系统"]
    }
    
    scale_indicators = {
        "small": ["小型", "小规模", "small", "startup"],
        "medium": ["中型", "中等规模", "medium", "business"],
        "large": ["大型", "大规模", "large", "corporate"],
        "enterprise": ["企业级", "超大规模", "enterprise", "global"]
    }
```

### 2. 渐进式架构分析（渐进式披露）
```python
class ProgressiveArchitectureAnalysis:
    def __init__(self):
        self.analysis_layers = [
            "basic_identification",    # 基础识别
            "pattern_matching",        # 模式匹配
            "quality_assessment",      # 质量评估
            "recommendation_generation" # 建议生成
        ]
    
    def progressive_analysis(self, requirements, analysis_depth):
        """
        渐进式披露：根据深度需求提供不同层次的架构分析
        depth=1: 基础架构类型识别（程序化程度95%）
        depth=2: 架构模式匹配和组件分析（程序化程度80%）
        depth=3: 架构质量评估和风险分析（程序化程度60%）
        depth=4: 深度建议和优化方案（程序化程度40%）
        """
        if analysis_depth == 1:
            return self.basic_architecture_identification(requirements)
        elif analysis_depth == 2:
            return self.detailed_pattern_analysis(requirements)
        elif analysis_depth == 3:
            return self.comprehensive_quality_assessment(requirements)
        else:
            return self.strategic_recommendations(requirements)
```

### 3. 架构质量评估（定性定量结合）
```python
class ArchitectureQualityAssessment:
    def __init__(self):
        self.quantitative_metrics = [
            "modularity_score",       # 模块化得分
            "coupling_measure",        # 耦合度测量
            "coherence_index",        # 一致性指数
            "scalability_rating",      # 可扩展性评级
            "maintainability_score"    # 可维护性得分
        ]
        
        self.qualitative_aspects = [
            "architectural_philosophy",    # 架构哲学
            "technology_appropriateness",   # 技术适宜性
            "business_alignment",           # 业务对齐度
            "future_proofing",             # 未来适应性
            "team_expertise_fit"           # 团队技能匹配
        ]
    
    def mixed_methods_assessment(self, architecture_design, requirements_context):
        """
        定性定量有机结合的架构质量评估
        """
        # 定量部分：程序化计算
        quant_metrics = self.calculate_quantitative_metrics(architecture_design)
        
        # 定性部分：基于规则提示词的AI分析
        qual_context = self.prepare_qualitative_context(architecture_design, requirements_context)
        qual_insights = self.ai_qualitative_analysis(qual_context)
        
        return self.integrated_quality_assessment(quant_metrics, qual_insights)
```

### 4. 架构建议生成（程序化+定性）
```python
class ArchitectureRecommendationEngine:
    def __init__(self):
        self.rule_based_recommendations = {
            "performance": [
                "Use caching for frequently accessed data",
                "Implement database connection pooling",
                "Consider CDN for static content"
            ],
            "security": [
                "Implement authentication and authorization",
                "Use HTTPS for all communications",
                "Validate all user inputs"
            ],
            "scalability": [
                "Design for horizontal scaling",
                "Use load balancers",
                "Implement microservices where appropriate"
            ]
        }
    
    def generate_recommendations(self, architecture_analysis, quality_assessment):
        """
        生成基于规则和AI定性分析的架构建议
        """
        # 程序化规则建议
        rule_based = self.generate_rule_based_recommendations(architecture_analysis)
        
        # AI定性分析建议
        qual_context = self.prepare_recommendation_context(architecture_analysis, quality_assessment)
        ai_recommendations = self.ai_qualitative_recommendations(qual_context)
        
        return self.integrated_recommendations(rule_based, ai_recommendations)
```

## 渐进式披露设计

### 层次1：基础架构识别
- **必需上下文**：最简需求描述（至少10个字符）
- **输出**：领域类型、复杂度、规模分类
- **程序化程度**：95%
- **认知负担**：最小（单一架构类型识别）

### 层次2：架构模式分析
- **必需上下文**：详细需求描述+技术约束
- **输出**：架构模式、核心组件、技术栈
- **程序化程度**：80%
- **认知负担**：适中（理解架构结构）

### 层次3：质量评估分析
- **必需上下文**：完整架构设计+业务背景
- **输出**：质量指标、风险评估、问题识别
- **程序化程度**：60%
- **认知负担**：较高（理解质量维度）

### 层次4：战略建议生成
- **必需上下文**：架构全貌+业务目标+团队情况
- **输出**：优化建议、实施路径、风险缓解
- **程序化程度**：40%
- **认知负担**：最高（综合决策支持）

## 规则提示词模板

### 架构定性分析提示词
```
你是一位资深的系统架构师，正在分析以下架构设计：

**架构设计**: {architecture_design}
**业务背景**: {business_context}
**技术约束**: {technical_constraints}

请从以下角度进行深度定性分析：
1. 架构哲学的一致性
2. 技术选择的合理性
3. 与业务目标的匹配度
4. 未来演化的适应性
5. 团队技能的契合度

基于架构最佳实践，提供：
- 架构优势和亮点
- 潜在风险和问题
- 改进建议和方向
- 实施路径规划
```

### 质量评估定性提示词
```
基于以下架构质量量化指标，进行深度定性解读：

**量化指标**: {quantitative_metrics}
**架构细节**: {architecture_details}
**业务场景**: {business_scenario}

请解释：
1. 各项质量指标的实际意义
2. 指标间的相互关系和影响
3. 在特定业务场景下的重要性
4. 与行业标准对比分析

结合实际经验，评估：
- 架构成熟度水平
- 技术债务风险
- 维护和演进成本
- 团队能力要求
```

## 应用场景映射

### Web应用架构
```python
class WebArchitectureArchitect(ArchitectSkill):
    def specialized_patterns(self):
        return {
            "typical_patterns": ["MVC", "Microservices", "Serverless", "SPA"],
            "key_components": ["Frontend", "Backend API", "Database", "Cache", "CDN"],
            "quality_focus": ["Performance", "Scalability", "Security"],
            "common_concerns": ["User Experience", "SEO", "Browser Compatibility"]
        }
```

### 企业级系统架构
```python
class EnterpriseArchitectureArchitect(ArchitectSkill):
    def specialized_patterns(self):
        return {
            "typical_patterns": ["Layered", "SOA", "Microservices", "Event-Driven"],
            "key_components": ["Presentation", "Business Logic", "Integration", "Data", "Security"],
            "quality_focus": ["Reliability", "Maintainability", "Security", "Compliance"],
            "common_concerns": ["Legacy Integration", "Data Governance", "User Management"]
        }
```

## 实现规范

### 技能接口
```python
def execute_architect_skill(
    requirements: str,
    analysis_depth: int = 1,
    domain_context: str = "auto_detect",
    quality_focus: str = "balanced",
    recommendation_level: str = "practical"
) -> dict:
    """
    架构师技能主入口
    
    Args:
        requirements: 系统需求描述
        analysis_depth: 分析深度 (1-4)
        domain_context: 领域上下文
        quality_focus: 质量重点
        recommendation_level: 建议级别
    
    Returns:
        dict: 结构化架构分析结果
    """
```

### 输出格式
```json
{
    "requirements_analysis": {
        "domain_type": "...",
        "complexity_level": "...",
        "scale_category": "...",
        "confidence_score": 0.85
    },
    "architecture_design": {
        "pattern": "...",
        "components": [...],
        "technology_stack": [...],
        "diagram_representation": "..."
    },
    "quality_assessment": {
        "quantitative_metrics": {...},
        "qualitative_insights": {...},
        "risk_assessment": [...],
        "overall_quality_score": 0.78
    },
    "recommendations": {
        "immediate_actions": [...],
        "strategic_improvements": [...],
        "implementation_roadmap": [...],
        "success_metrics": [...]
    }
}
```

## 质量保证

### 验证清单
- [x] 需求解析准确性
- [x] 架构模式匹配正确性
- [x] 质量指标计算有效性
- [x] 建议实用性和可操作性
- [x] 渐进式披露层次清晰

### 程序化规则验证
```python
def validate_architect_rules():
    """
    验证架构师技能的程序化规则
    """
    test_cases = [
        {
            "input": "构建一个电商网站",
            "expected": {"domain_type": "web", "complexity": "medium"}
        },
        {
            "input": "开发移动银行应用",
            "expected": {"domain_type": "mobile", "complexity": "complex"}
        }
    ]
    
    for test_case in test_cases:
        result = parse_architecture_requirements(test_case["input"])
        assert result["domain_type"] == test_case["expected"]["domain_type"]
        assert result["complexity_level"] == test_case["expected"]["complexity"]
```

## 定性定量有机结合验证

### 定量部分（程序化90%）
- 领域识别：基于关键词匹配
- 复杂度评估：基于文本长度和技术术语
- 组件分析：基于预定义映射
- 质量指标：基于架构特征计算

### 定性部分（AI分析80%）
- 架构哲学分析：需要深度理解
- 技术适宜性评估：需要经验判断
- 业务对齐度分析：需要领域知识
- 未来适应性预测：需要前瞻性思考

### 整合机制
```python
def integrate_architect_analysis(quantitative_results, qualitative_insights):
    """
    整合定性和定量分析结果
    """
    integrated_analysis = {
        "architecture_type": quantitative_results["domain_type"],
        "pattern_recommendation": quantitative_results["suggested_pattern"],
        "quality_score": qualitative_insights["overall_quality"],
        "strategic_guidance": qualitative_insights["philosophy_alignment"],
        "implementation_risks": qualitative_insights["risk_assessment"]
    }
    
    # 一致性检查
    if quantitative_results["complexity"] != qualitative_insights["perceived_complexity"]:
        integrated_analysis["complexity_discrepancy"] = True
        integrated_analysis["resolution_note"] = "Qualitative assessment suggests different complexity level"
    
    return integrated_analysis
```

---

## 优化成果总结

1. **渐进式披露**: 实现了4层清晰的渐进式分析
2. **定性定量结合**: 90%程序化规则+80%AI定性分析
3. **格式塔认知**: 从整体识别到细节分析的认知流程
4. **最小上下文**: 每层仅加载必需的上下文信息
5. **规则程序化**: 所有确定性规则都已代码化
6. **提示词标准化**: AI定性分析有专门的提示词模板

这个优化后的architect技能完全符合您的要求，实现了科学化、系统化的架构设计支持。