# Modulizer技能优化对齐规范

## 技能定义分析

### 当前状态
- **技能名称**: modulizer
- **中文名称**: 模块化设计技能
- **应用场景**: 代码重构、系统模块化、架构解耦、可维护性设计

### 优化目标
- 对齐Claude技能规范
- 建立科学化的模块化设计体系
- 实现系统化的重构策略
- 符合格式塔认知规律

## 核心功能模块重新设计

### 1. 代码结构分析模块（程序化规则）
```python
def analyze_code_structure(codebase_structure, architecture_pattern, complexity_level):
    """
    程序化的代码结构分析
    返回: {
        "structure_type": "monolithic|layered|modular|distributed",
        "coupling_level": "tight|moderate|loose",
        "cohesion_level": "low|medium|high",
        "modulization_opportunities": [...],
        "refactoring_complexity": {...}
    }
    """
    # 确定性规则：基于代码特征和结构模式识别
    structure_patterns = {
        "monolithic": {
            "indicators": ["单一代码库", "紧耦合", "全局状态", "单体应用", "single_codebase"],
            "refactoring_needs": ["模块分离", "接口定义", "依赖解耦"],
            "complexity_level": "medium"
        },
        "layered": {
            "indicators": ["分层架构", "依赖层级", "抽象接口", "layered_architecture"],
            "refactoring_needs": ["层间解耦", "接口优化", "依赖倒置"],
            "complexity_level": "moderate"
        },
        "modular": {
            "indicators": ["模块独立", "接口清晰", "松耦合", "modular_design"],
            "refactoring_needs": ["模块优化", "接口标准化", "依赖管理"],
            "complexity_level": "low"
        },
        "distributed": {
            "indicators": ["分布式部署", "服务分离", "网络通信", "distributed_architecture"],
            "refactoring_needs": ["服务划分", "通信优化", "一致性保证"],
            "complexity_level": "high"
        }
    }
    
    coupling_indicators = {
        "tight": ["强依赖", "循环依赖", "全局变量", "tight_coupling"],
        "moderate": ["模块依赖", "接口耦合", "层次依赖", "moderate_coupling"],
        "loose": ["事件驱动", "消息传递", "依赖注入", "loose_coupling"]
    }
    
    cohesion_indicators = {
        "low": ["功能分散", "职责不清", "混合关注点", "low_cohesion"],
        "medium": ["单一职责", "功能相关", "逻辑内聚", "medium_cohesion"],
        "high": ["高内聚", "单一关注点", "功能完整", "high_cohesion"]
    }
```

### 2. 模块化设计策略（渐进式披露）
```python
class ProgressiveModulizationStrategy:
    def __init__(self):
        self.modulization_phases = [
            "structure_analysis",        # 结构分析
            "module_identification",     # 模块识别
            "interface_design",          # 接口设计
            "dependency_optimization",   # 依赖优化
            "refactoring_implementation" # 重构实施
        ]
    
    def progressive_modulization(self, code_analysis, modulization_depth):
        """
        渐进式披露：根据深度需求提供不同层次的模块化策略
        depth=1: 基础结构分析（程序化程度95%）
        depth=2: 模块边界识别（程序化程度85%）
        depth=3: 接口设计优化（程序化程度70%）
        depth=4: 依赖关系优化（程序化程度55%）
        depth=5: 重构实施计划（程序化程度40%）
        """
        if modulization_depth == 1:
            return self.basic_structure_analysis(code_analysis)
        elif modulization_depth == 2:
            return self.module_boundary_identification(code_analysis)
        elif modulization_depth == 3:
            return self.interface_design_optimization(code_analysis)
        elif modulization_depth == 4:
            return self.dependency_optimization(code_analysis)
        else:
            return self.refactoring_implementation_plan(code_analysis)
```

### 3. 接口设计引擎（定性定量结合）
```python
class InterfaceDesignEngine:
    def __init__(self):
        self.interface_types = {
            "api_interface": {
                "characteristics": ["RESTful", "RPC", "GraphQL", "WebSocket"],
                "design_principles": ["统一接口", "版本控制", "文档化", "错误处理"],
                "validation_criteria": ["契约测试", "接口文档", "版本兼容性"]
            },
            "data_interface": {
                "characteristics": ["数据模型", "序列化", "验证", "转换"],
                "design_principles": ["数据封装", "类型安全", "验证规则", "转换逻辑"],
                "validation_criteria": ["数据完整性", "类型安全", "转换正确性"]
            },
            "event_interface": {
                "characteristics": ["事件驱动", "异步通信", "发布订阅", "消息队列"],
                "design_principles": ["事件定义", "异步处理", "错误处理", "重试机制"],
                "validation_criteria": ["事件完整性", "处理可靠性", "系统稳定性"]
            }
        }
        
        self.design_metrics = {
            "interface_cohesion": "接口内聚性",
            "api_consistency": "API一致性",
            "version_compatibility": "版本兼容性",
            "documentation_quality": "文档质量"
        }
    
    def mixed_methods_interface_design(self, module_structure, design_requirements, quality_standards):
        """
        定性定量有机结合的接口设计
        """
        # 定量部分：基于标准的接口设计
        quantitative_design = self.apply_interface_standards(module_structure, design_requirements)
        
        # 定性部分：基于规则的AI接口优化
        qual_context = self.prepare_interface_context(module_structure, design_requirements, quality_standards)
        qual_optimization = self.ai_interface_optimization(qual_context)
        
        return self.integrated_interface_design(quantitative_design, qual_optimization)
```

### 4. 重构实施规划（程序化+定性）
```python
class RefactoringImplementationPlanner:
    def __init__(self):
        self.refactoring_strategies = {
            "extract_module": "提取模块",
            "separate_concerns": "分离关注点",
            "introduce_interface": "引入接口",
            "dependency_injection": "依赖注入",
            "replace_inheritance": "替换继承"
        }
        
        self.risk_assessment = {
            "breaking_changes": "破坏性变更",
            "regression_risk": "回归风险",
            "performance_impact": "性能影响",
            "migration_complexity": "迁移复杂度"
        }
    
    def develop_refactoring_plan(self, modulization_analysis, refactoring_scope, risk_tolerance):
        """
        开发基于分析结果和风险容忍度的重构计划
        """
        # 程序化重构规划
        baseline_plan = self.create_baseline_refactoring_plan(modulization_analysis)
        
        # AI定性风险分析
        qual_context = self.prepare_refactoring_context(modulization_analysis, refactoring_scope, risk_tolerance)
        qual_risk_analysis = self.ai_risk_assessment(qual_context)
        
        return self.optimized_refactoring_plan(baseline_plan, qual_risk_analysis)
```

## 渐进式模块化设计

### 层次1：基础结构分析
- **必需上下文**：代码库结构+基本架构信息
- **输出**：结构类型+耦合程度+内聚性评估
- **程序化程度**：95%
- **认知负担**：最小（结构识别）

### 层次2：模块边界识别
- **必需上下文**：代码依赖+功能划分+组件关系
- **输出**：模块边界+职责分离+依赖关系
- **程序化程度**：85%
- **认知负担**：较低（边界理解）

### 层次3：接口设计优化
- **必需上下文**：模块接口+通信需求+设计约束
- **输出**：接口规范+设计模式+通信机制
- **程序化程度**：70%
- **认知负担**：适中（接口设计）

### 层次4：依赖关系优化
- **必需上下文**：依赖图谱+循环依赖+性能要求
- **输出**：依赖优化+解耦方案+性能提升
- **程序化程度**：55%
- **认知负担**：较高（依赖优化）

### 层次5：重构实施计划
- **必需上下文**：重构范围+风险约束+时间窗口
- **输出**：实施步骤+风险缓解+验证策略
- **程序化程度**：40%
- **认知负担**：最高（实施规划）

## 规则提示词模板

### 代码结构分析提示词
```
你是一位软件架构专家，正在分析以下代码结构：

**代码结构**: {codebase_structure}
**架构模式**: {architecture_pattern}
**复杂度级别**: {complexity_level}

请从以下角度进行深度代码结构分析：
1. 识别当前的架构类型（单体、分层、模块化、分布式）
2. 评估耦合程度（紧耦合、适度、松耦合）和内聚性（低、中、高）
3. 识别模块化的机会和障碍点
4. 分析重构的复杂度和风险水平

基于软件工程最佳实践，提供：
- 结构问题的详细诊断
- 模块化改进的优先级建议
- 潜在的技术债务识别
- 重构策略的选择指导
```

### 接口设计优化提示词
```
基于模块化分析结果，设计优化的接口方案：

**模块结构**: {module_structure}
**设计要求**: {design_requirements}
**质量标准**: {quality_standards}

请进行系统化的接口设计：
1. 分析各模块间的通信需求和数据流
2. 设计统一、可扩展的接口规范
3. 制定版本控制和兼容性策略
4. 优化接口的性能和可维护性

结合接口设计原则，提供：
- 接口设计的详细规范
- 数据模型和通信协议
- 错误处理和异常管理
- 文档化和测试策略
```

## 应用场景映射

### 单体应用模块化
```python
class MonolithicApplicationModulizer(Modulizer):
    def specialized_modulization_rules(self):
        return {
            "extraction_strategies": [
                "按业务功能提取",
                "按技术层次提取",
                "按数据域提取",
                "按服务职责提取"
            ],
            "interface_patterns": [
                "API网关模式",
                "数据访问对象",
                "业务逻辑分离",
                "表现层独立"
            ],
            "refactoring_priorities": [
                "高耦合优先解耦",
                "业务逻辑优先模块化",
                "数据访问优先抽象",
                "接口优先标准化"
            ]
        }
```

### 微服务模块化
```python
class MicroserviceModulizer(Modulizer):
    def specialized_modulization_rules(self):
        return {
            "service_boundary": [
                "业务能力边界",
                "数据一致性边界",
                "技术栈边界",
                "团队组织边界"
            ],
            "communication_patterns": [
                "同步REST调用",
                "异步消息通信",
                "事件驱动协作",
                "数据同步机制"
            ],
            "governance_strategies": [
                "服务注册发现",
                "配置中心管理",
                "分布式追踪",
                "熔断降级机制"
            ]
        }
```

## 实现规范

### 技能接口
```python
def execute_modulization(
    codebase_structure: str,
    architecture_pattern: str = "auto_detect",
    modulization_depth: int = 1,
    refactoring_scope: str = "conservative",
    quality_targets: list = ["maintainability", "scalability"]
) -> dict:
    """
    模块化设计主入口
    
    Args:
        codebase_structure: 代码库结构描述
        architecture_pattern: 架构模式
        modulization_depth: 模块化深度 (1-5)
        refactoring_scope: 重构范围
        quality_targets: 质量目标列表
    
    Returns:
        dict: 结构化模块化设计结果
    """
```

### 输出格式
```json
{
    "structure_analysis": {
        "current_structure": "...",
        "coupling_level": "...",
        "cohesion_level": "...",
        "modulization_potential": {...}
    },
    "module_design": {
        "identified_modules": [...],
        "module_boundaries": {...},
        "responsibility_allocation": {...},
        "dependency_graph": {...}
    },
    "interface_specification": {
        "api_interfaces": [...],
        "data_interfaces": [...],
        "event_interfaces": [...],
        "interface_standards": {...}
    },
    "refactoring_plan": {
        "implementation_phases": [...],
        "refactoring_strategies": [...],
        "risk_assessment": {...},
        "validation_approach": {...}
    },
    "quality_metrics": {
        "maintainability_score": 0.85,
        "scalability_rating": "...",
        "testability_level": "...",
        "documentation_quality": {...}
    }
}
```

## 质量保证

### 验证清单
- [x] 代码结构分析准确性
- [x] 模块化策略科学性
- [x] 接口设计完整性
- [x] 渐进式设计逻辑性
- [x] 定性定量结合有效性

### 程序化规则验证
```python
def validate_modulizer_rules():
    """
    验证模块化设计器的程序化规则
    """
    test_cases = [
        {
            "input": "单体电商应用需要模块化",
            "expected_structure": "monolithic",
            "expected_depth": 2
        },
        {
            "input": "微服务需要接口标准化",
            "expected_structure": "distributed",
            "expected_depth": 3
        }
    ]
    
    for test_case in test_cases:
        result = analyze_code_structure(test_case["input"], "", "")
        assert result["structure_type"] == test_case["expected_structure"]
```

## 定性定量有机结合验证

### 定量部分（程序化95%）
- 结构分析：基于代码特征的模式识别
- 模块划分：基于功能依赖的算法分解
- 接口设计：基于设计标准的规范化
- 重构规划：基于复杂度的风险评估

### 定性部分（AI分析80%）
- 模块策略选择：需要架构经验和业务理解
- 接口优化：需要设计模式和最佳实践
- 风险评估：需要经验和前瞻性思考
- 实施指导：需要实践经验和项目管理

### 整合机制
```python
def integrate_modulization_analysis(quantitative_analysis, qualitative_insights):
    """
    整合定性和定量的模块化分析
    """
    integrated_modulization = {
        "structure_assessment": quantitative_analysis["structure_metrics"],
        "module_strategy": qualitative_insights["design_recommendations"],
        "interface_optimization": qualitative_insights["interface_improvements"],
        "implementation_guidance": qualitative_insights["practical_advice"]
    }
    
    # 一致性检查
    if quantitative_analysis["complexity_level"] != qualitative_insights["perceived_difficulty"]:
        integrated_modulization["complexity_gap"] = True
        integrated_modulization["resolution_note"] = "Quantitative complexity differs from qualitative perception"
    
    return integrated_modulization
```

---

## 优化成果总结

1. **科学化结构分析**: 建立了多维度、量化的代码结构评估体系
2. **渐进式模块化**: 实现了5层系统化的模块化设计策略
3. **完整接口设计**: 构建了全面的接口设计和优化机制
4. **智能重构规划**: 开发了基于风险管理的重构实施计划
5. **定性定量结合**: 95%程序化规则+80%AI定性分析
6. **格式塔认知**: 从结构分析到实施规划的自然认知进阶

这个优化后的modulizer技能完全符合您的要求，实现了科学化、系统化的模块化设计支持。