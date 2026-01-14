# Simple Architect Skill对齐优化规范

## 1. 技能定义与功能边界

### 1.1 技能定义
基于architect模式的简化架构设计工具，专注于单模块和小型系统的架构设计，提供快速、轻量级的设计方案。

### 1.2 核心功能
- **快速架构设计**：提供简化的架构设计流程
- **模块化设计**：支持单模块和小型系统的模块化
- **模板化应用**：应用预定义的架构模板
- **轻量级文档**：生成精简的架构文档

### 1.3 应用场景
- **小型项目架构**：单模块应用和小型系统设计
- **快速原型**：快速原型验证和概念验证
- **简化重构**：小型系统的重构设计
- **教学示例**：架构设计的教学和演示

## 2. 渐进式披露功能模块

### Level 1: 基础架构快速设计 (95% 程序化)
**目标**: 提供基础的快速架构设计功能
**程序化规则**: 基于预定义模板和规则的设计生成

**确定性规则**:
```python
# 基础架构快速设计规则
def quick_architecture_design(requirements):
    # 1. 解析基础需求
    basic_requirements = extract_basic_requirements(requirements)
    
    # 2. 匹配架构模板
    template = match_architecture_template(basic_requirements)
    
    # 3. 生成基础架构
    architecture = generate_basic_architecture(template)
    
    # 4. 验证基础完整性
    return validate_basic_architecture(architecture)

# 快速设计规则
QUICK_DESIGN_RULES = {
    "single_module": {
        "max_components": 10,
        "complexity": "low",
        "template": "single_module_template"
    },
    "small_system": {
        "max_components": 20,
        "max_modules": 5,
        "complexity": "medium",
        "template": "small_system_template"
    }
}
```

**功能模块**:
- 基础需求解析 (95%)
- 模板匹配引擎 (95%)
- 快速架构生成 (95%)
- 基础验证检查 (90%)

### Level 2: 模板化架构设计 (85% 程序化)
**目标**: 基于模板的架构设计优化
**程序化规则**: 模板选择和参数化配置

**确定性规则**:
```python
# 模板化架构设计规则
def template_based_design(template_type, parameters):
    # 1. 加载模板定义
    template = load_architecture_template(template_type)
    
    # 2. 参数化配置
    configured_template = configure_template(template, parameters)
    
    # 3. 生成架构设计
    design = generate_from_template(configured_template)
    
    # 4. 模板适配检查
    return validate_template_fit(design, template_type)

# 模板库定义
TEMPLATE_LIBRARY = {
    "single_module": {
        "components": ["service", "data", "interface"],
        "patterns": ["mvc", "layered", "service_locator"]
    },
    "small_system": {
        "modules": ["auth", "business", "data", "api"],
        "patterns": ["microservice", "monolith", "hybrid"]
    }
}
```

**AI定性分析提示**:
```
分析当前场景最适合的架构模板类型，考虑：
1. 项目规模和复杂度
2. 技术栈和约束条件
3. 团队经验和偏好
4. 性能和扩展性需求
5. 模板适配度和可定制性
```

**功能模块**:
- 模板选择策略 (85%)
- 参数化配置 (90%)
- 模板适配分析 (80%)
- 定制化建议 (75%)

### Level 3: 小型系统集成设计 (75% 程序化)
**目标**: 小型多模块系统的集成设计
**程序化规则**: 模块间集成模式和接口设计

**确定性规则**:
```python
# 小型系统集成设计规则
def small_system_integration(modules):
    # 1. 分析模块依赖
    dependencies = analyze_module_dependencies(modules)
    
    # 2. 设计集成模式
    integration_pattern = select_integration_pattern(dependencies)
    
    # 3. 定义接口规范
    interfaces = define_module_interfaces(modules, integration_pattern)
    
    # 4. 验证集成可行性
    return validate_integration_design(modules, interfaces)

# 集成模式定义
INTEGRATION_PATTERNS = {
    "tight_coupling": {
        "suitable_for": "small_teams",
        "complexity": "low",
        "performance": "high"
    },
    "loose_coupling": {
        "suitable_for": "growing_teams",
        "complexity": "medium",
        "performance": "medium"
    }
}
```

**AI定性分析提示**:
```
评估小型系统集成策略，分析：
1. 模块间依赖关系的合理性
2. 集成模式的适用性和风险
3. 接口设计的清晰度和一致性
4. 数据流和控制流的优化空间
5. 系统整体的可维护性
```

**功能模块**:
- 模块依赖分析 (80%)
- 集成模式选择 (75%)
- 接口设计规范 (70%)
- 集成风险评估 (70%)

### Level 4: 轻量级架构优化 (65% 程序化)
**目标**: 基于性能和成本约束的轻量级优化
**程序化规则**: 基础性能和资源优化算法

**确定性规则**:
```python
# 轻量级架构优化规则
def lightweight_optimization(architecture, constraints):
    # 1. 分析性能瓶颈
    bottlenecks = identify_bottlenecks(architecture)
    
    # 2. 应用优化模式
    optimizations = apply_optimization_patterns(bottlenecks)
    
    # 3. 评估优化效果
    improvements = measure_optimization_impact(optimizations)
    
    # 4. 生成优化建议
    return generate_optimization_recommendations(improvements)

# 轻量级优化模式
LIGHTWEIGHT_OPTIMIZATIONS = {
    "performance": ["caching", "async_processing", "connection_pooling"],
    "resource": ["lazy_loading", "resource_pooling", "compression"],
    "simplicity": ["remove_redundancy", "simplify_interfaces", "consolidate_modules"]
}
```

**AI定性分析提示**:
```
优化轻量级架构设计，考虑：
1. 性能瓶颈的关键影响因素
2. 资源使用的效率和成本效益
3. 架构简洁性和可维护性平衡
4. 优化措施的实施难度和风险
5. 长期演化和扩展的适应性
```

**功能模块**:
- 性能瓶颈识别 (70%)
- 优化模式匹配 (65%)
- 效果评估测量 (60%)
- 优化建议生成 (60%)

### Level 5: 简化架构文档生成 (55% 程序化)
**目标**: 生成精简实用的架构文档
**程序化规则**: 基于模板的文档生成规则

**确定性规则**:
```python
# 简化文档生成规则
def generate_simple_documentation(architecture):
    # 1. 提取关键信息
    key_info = extract_key_architecture_info(architecture)
    
    # 2. 应用文档模板
    doc_template = select_documentation_template(key_info)
    
    # 3. 生成文档内容
    documentation = generate_documentation_content(key_info, doc_template)
    
    # 4. 简化表达优化
    return simplify_documentation_expression(documentation)

# 简化文档模板
SIMPLE_DOC_TEMPLATES = {
    "overview": ["system_purpose", "key_components", "main_flows"],
    "technical": ["technology_stack", "architecture_patterns", "interfaces"],
    "deployment": ["environment_requirements", "deployment_steps", "configuration"]
}
```

**AI定性分析提示**:
```
生成简化架构文档，注重：
1. 信息的简洁性和完整性平衡
2. 不同受众的理解需求差异
3. 可视化图表的有效运用
4. 实际操作的指导价值
5. 文档维护的便利性
```

**功能模块**:
- 关键信息提取 (60%)
- 文档模板选择 (55%)
- 内容生成优化 (50%)
- 表达简化处理 (50%)

## 3. 定性与定量有机结合

### 3.1 定量分析核心 (90-95% 程序化)
**架构度量指标**:
```python
# 架构复杂度度量
def calculate_architecture_complexity(architecture):
    return {
        "cyclomatic_complexity": calculate_cyclomatic(architecture),
        "coupling_factor": measure_coupling(architecture),
        "cohesion_metric": evaluate_cohesion(architecture),
        "modularity_score": assess_modularity(architecture)
    }

# 简化度评估
def assess_simplicity(architecture):
    return {
        "component_count": count_components(architecture),
        "interface_complexity": measure_interface_complexity(architecture),
        "dependency_depth": calculate_dependency_depth(architecture),
        "documentation_ratio": calculate_doc_ratio(architecture)
    }
```

### 3.2 定性分析辅助 (80-85% AI驱动)
**架构质量评估**:
```python
# AI定性分析提示模板
ARCHITECTURE_QUALITY_PROMPT = """
分析简化架构的设计质量：

**技术维度分析**：
1. 架构模式的适用性和简洁性
2. 技术选择的合理性和一致性
3. 接口设计的清晰度和易用性
4. 数据结构的效率和可扩展性

**业务维度分析**：
1. 业务需求的满足程度
2. 用户体验的优化空间
3. 业务流程的支持度
4. 未来扩展的适应性

**实施维度分析**：
1. 开发复杂度的合理性
2. 测试覆盖的可行性
3. 部署运维的简便性
4. 团队技能的匹配度

**维护维度分析**：
1. 代码结构的可读性
2. 文档信息的完整性
3. 问题诊断的便利性
4. 修改实施的安全性
"""
```

## 4. 应用场景对齐

### 4.1 小型项目架构场景
**场景特征**: 1-3个开发者，3-6个月周期，单模块或少模块
**优化重点**:
- 快速设计和实现
- 简洁清晰的架构
- 最小化技术债务
- 易于理解维护

### 4.2 快速原型场景
**场景特征**: 概念验证，快速迭代，技术探索
**优化重点**:
- 快速搭建和修改
- 核心功能优先
- 技术风险最小
- 演示效果导向

### 4.3 教学示例场景
**场景特征**: 教学演示，概念说明，学习实践
**优化重点**:
- 概念表达清晰
- 代码结构简洁
- 文档说明详细
- 易于理解复现

## 5. 最小上下文加载

### 5.1 上下文分层策略
**L1上下文** (必需，~200 tokens): 基础需求描述
**L2上下文** (按需，~400 tokens): 模板类型和参数
**L3上下文** (可选，~600 tokens): 约束条件和偏好
**L4上下文** (扩展，~800 tokens): 技术栈和环境信息
**L5上下文** (完整，~1000 tokens): 业务场景和团队背景

### 5.2 智能上下文加载
```python
# 上下文需求评估
def evaluate_context_needs(requirements):
    complexity = assess_architecture_complexity(requirements)
    
    if complexity == "very_low":
        return ["L1", "L2"]
    elif complexity == "low":
        return ["L1", "L2", "L3"]
    elif complexity == "medium":
        return ["L1", "L2", "L3", "L4"]
    else:
        return ["L1", "L2", "L3", "L4", "L5"]

# 动态上下文加载
def load_context_dynamically(level, requirements):
    context_loaders = {
        "L1": load_basic_requirements,
        "L2": load_template_parameters,
        "L3": load_constraints_preferences,
        "L4": load_technical_environment,
        "L5": load_business_context
    }
    return context_loaders[level](requirements)
```

## 6. 实施规范

### 6.1 技术实施规范
- **规则编码化**: 所有设计规则转换为可执行代码
- **模板库管理**: 版本化的架构模板库
- **验证自动化**: 自动化的架构验证检查
- **文档生成**: 自动化的简明文档生成

### 6.2 质量保证规范
- **设计审查**: 分层级的架构设计审查
- **一致性检查**: 模板应用的一致性验证
- **性能验证**: 轻量级性能测试验证
- **可读性评估**: 文档和代码的可读性评估

## 7. 质量评估机制

### 7.1 定量评估指标 (90-95% 程序化)
```python
# 简化架构质量指标
def evaluate_simple_architecture_quality(architecture):
    return {
        "simplicity_score": measure_simplicity(architecture),
        "clarity_score": assess_clarity(architecture),
        "consistency_score": check_consistency(architecture),
        "maintainability_score": evaluate_maintainability(architecture)
    }

# 快速设计效率指标
def measure_design_efficiency(design_process):
    return {
        "design_time": measure_elapsed_time(design_process),
        "template_usage": calculate_template_utilization(design_process),
        "automation_ratio": assess_automation_level(design_process),
        "satisfaction_score": evaluate_user_satisfaction(design_process)
    }
```

### 7.2 定性评估维度 (80-85% AI驱动)
```python
# AI定性评估框架
QUALITY_EVALUATION_FRAMEWORK = """
评估简化架构的综合质量：

**设计质量维度**：
1. 架构的简洁性和清晰度
2. 模块划分的合理性
3. 接口设计的直观性
4. 技术选择的适宜性

**实施质量维度**：
1. 开发实现的简便性
2. 测试验证的可行性
3. 部署运维的便捷性
4. 学习理解的容易性

**业务价值维度**：
1. 需求满足的充分性
2. 快速交付的及时性
3. 成本控制的有效性
4. 未来演化的适应性
"""
```

通过这套完整的优化规范，simple-architect技能能够在保持简洁性的同时，提供高效、实用的架构设计能力，满足小型项目和快速原型场景的需求。