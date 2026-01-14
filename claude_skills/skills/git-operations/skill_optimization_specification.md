# Git Operations Skill对齐优化规范

## 1. 技能定义与功能边界

### 1.1 技能定义
专业的Git操作管理工具，专注于配置Git工作流规则、防止AI文件污染、优化团队协作流程和实施自动化代码质量管理。

### 1.2 核心功能
- **Git工作流配置**: 设置和管理Git工作流程
- **提交规范制定**: 建立统一的提交信息规范
- **分支策略设计**: 设计适合项目的分支管理策略
- **自动化检查**: 配置代码质量检查和CI/CD流程
- **团队协作优化**: 优化团队Git使用效率

### 1.3 应用场景
- **新项目初始化**: 建立项目的Git工作流规范
- **团队协作改进**: 优化现有团队的Git使用流程
- **AI项目治理**: 防止AI生成文件对仓库的污染
- **质量保障体系**: 建立代码质量检查和保障机制

## 2. 渐进式披露功能模块

### Level 1: 基础Git规则配置 (95% 程序化)
**目标**: 提供基础的Git配置和规则设定
**程序化规则**: 标准化的Git配置模板和规则

**确定性规则**:
```python
# 基础Git配置规则
def configure_basic_git_rules(project_type, team_size):
    # 1. 选择基础配置模板
    config_template = select_git_config_template(project_type, team_size)
    
    # 2. 设置.gitignore规则
    gitignore_rules = generate_gitignore_rules(project_type)
    
    # 3. 配置基础钩子
    basic_hooks = setup_basic_git_hooks()
    
    # 4. 生成配置文件
    return generate_git_configuration(config_template, gitignore_rules, basic_hooks)

# 基础配置模板
BASIC_GIT_TEMPLATES = {
    "solo_developer": {
        "branch_strategy": "main_only",
        "commit_format": "conventional_simple",
        "hooks": ["pre-commit_basic"]
    },
    "small_team": {
        "branch_strategy": "feature_branch",
        "commit_format": "conventional_full",
        "hooks": ["pre-commit", "commit_msg"]
    }
}
```

**功能模块**:
- Git配置模板选择 (95%)
- .gitignore规则生成 (90%)
- 基础钩子设置 (90%)
- 配置文件生成 (95%)

### Level 2: 分支策略设计 (85% 程序化)
**目标**: 设计适合项目的分支管理策略
**程序化规则**: 分支策略模式和最佳实践

**确定性规则**:
```python
# 分支策略设计规则
def design_branch_strategy(project_complexity, team_workflow):
    # 1. 分析项目特征
    project_characteristics = analyze_project_characteristics(project_complexity)
    
    # 2. 匹配分支策略
    branch_strategy = match_branch_strategy(project_characteristics, team_workflow)
    
    # 3. 定义分支规则
    branch_rules = define_branch_rules(branch_strategy)
    
    # 4. 生成保护配置
    return generate_branch_protection(branch_rules)

# 分支策略模式
BRANCH_STRATEGIES = {
    "git_flow": {
        "suitable_for": "complex_releases",
        "branches": ["main", "develop", "feature", "release", "hotfix"],
        "complexity": "high"
    },
    "github_flow": {
        "suitable_for": "continuous_deployment",
        "branches": ["main", "feature"],
        "complexity": "low"
    },
    "gitlab_flow": {
        "suitable_for": "environment_based",
        "branches": ["main", "feature", "environment"],
        "complexity": "medium"
    }
}
```

**AI定性分析提示**:
```
分析最适合项目的分支策略，考虑：
1. 项目发布节奏和复杂性
2. 团队规模和协作模式
3. 代码审查和集成需求
4. 发布频率和风险管理
5. 工具链和CI/CD集成能力
```

**功能模块**:
- 项目特征分析 (85%)
- 策略匹配引擎 (80%)
- 分支规则定义 (75%)
- 保护配置生成 (75%)

### Level 3: 提交规范制定 (75% 程序化)
**目标**: 建立统一和规范的提交信息格式
**程序化规则**: 提交信息模板和验证规则

**确定性规则**:
```python
# 提交规范制定规则
def define_commit_standards(project_type, team_preferences):
    # 1. 选择提交规范类型
    commit_type = select_commit_type(project_type)
    
    # 2. 定义提交格式
    commit_format = define_commit_format(commit_type)
    
    # 3. 设置验证规则
    validation_rules = setup_commit_validation(commit_format)
    
    # 4. 生成模板和示例
    return generate_commit_templates(commit_format, validation_rules)

# 提交规范类型
COMMIT_STANDARDS = {
    "conventional": {
        "format": "<type>(<scope>): <subject>",
        "types": ["feat", "fix", "docs", "style", "refactor", "test", "chore"],
        "validation": "regex_based"
    },
    "semantic": {
        "format": "<type>[(<scope>)]: <subject>",
        "types": ["feat", "fix", "perf", "revert"],
        "validation": "semantic_release"
    },
    "custom": {
        "format": "project_specific",
        "types": "custom_defined",
        "validation": "custom_rules"
    }
}
```

**AI定性分析提示**:
```
制定合适的提交规范，分析：
1. 项目类型和文档需求
2. 自动化工具集成要求
3. 团队成员接受程度
4. 变更日志生成需求
5. 版本发布管理策略
```

**功能模块**:
- 规范类型选择 (80%)
- 提交格式定义 (75%)
- 验证规则设置 (70%)
- 模板示例生成 (70%)

### Level 4: AI文件污染防护 (65% 程序化)
**目标**: 防止AI生成文件对Git仓库的负面影响
**程序化规则**: AI文件识别和处理策略

**确定性规则**:
```python
# AI文件污染防护规则
def prevent_ai_file_pollution(ai_config, project_settings):
    # 1. 识别AI生成文件模式
    ai_patterns = identify_ai_file_patterns(ai_config)
    
    # 2. 设置过滤规则
    filtering_rules = setup_ai_filtering_rules(ai_patterns)
    
    # 3. 配置处理策略
    handling_strategy = configure_ai_handling_strategy(filtering_rules)
    
    # 4. 生成防护配置
    return generate_ai_protection_config(handling_strategy)

# AI文件模式识别
AI_FILE_PATTERNS = {
    "llm_generated": {
        "extensions": [".md", ".txt", ".py", ".js"],
        "markers": ["ai_generated", "llm_created"],
        "patterns": ["temp_*", "auto_*", "generated_*"]
    },
    "auto_tools": {
        "extensions": [".log", ".tmp", ".cache", ".bak"],
        "markers": ["auto_generated", "tool_created"],
        "patterns": ["*.log", "*.tmp", "__pycache__"]
    }
}
```

**AI定性分析提示**:
```
评估AI文件污染风险，制定策略：
1. AI工具使用模式分析
2. 临时文件识别和处理
3. 代码质量和版本控制影响
4. 团队协作和文件共享
5. 自动化检测和处理机制
```

**功能模块**:
- AI文件模式识别 (70%)
- 过滤规则设置 (65%)
- 处理策略配置 (60%)
- 防护配置生成 (60%)

### Level 5: 协作流程优化 (55% 程序化)
**目标**: 优化团队Git协作效率和质量
**程序化规则**: 协作流程模板和自动化配置

**确定性规则**:
```python
# 协作流程优化规则
def optimize_collaboration_workflow(team_structure, workflow_analysis):
    # 1. 分析团队协作模式
    collaboration_pattern = analyze_collaboration_pattern(team_structure)
    
    # 2. 选择工作流模板
    workflow_template = select_workflow_template(collaboration_pattern)
    
    # 3. 配置自动化流程
    automation_config = configure_automation(workflow_template)
    
    # 4. 生成协作指南
    return generate_collaboration_guide(automation_config)

# 协作工作流模板
COLLABORATION_WORKFLOWS = {
    "distributed_team": {
        "timezone_handling": "async_first",
        "review_process": "pull_request_based",
        "communication": "document_driven"
    },
    "co_located_team": {
        "timezone_handling": "sync_optimized",
        "review_process": "pair_programming",
        "communication": "face_to_face"
    },
    "hybrid_team": {
        "timezone_handling": "flexible",
        "review_process": "mixed_approach",
        "communication": "multi_channel"
    }
}
```

**AI定性分析提示**:
```
优化团队协作流程，考虑：
1. 团队地理分布和时区差异
2. 开发经验和技能水平差异
3. 项目紧急性和发布节奏
4. 沟通偏好和工具使用习惯
5. 质量标准和代码审查要求
```

**功能模块**:
- 协作模式分析 (60%)
- 工作流模板选择 (55%)
- 自动化配置 (50%)
- 协作指南生成 (50%)

## 3. 定性与定量有机结合

### 3.1 定量分析核心 (90-95% 程序化)
**Git效率度量**:
```python
# Git操作效率指标
def calculate_git_efficiency(git_logs, team_metrics):
    return {
        "commit_frequency": analyze_commit_frequency(git_logs),
        "merge_conflict_rate": calculate_conflict_rate(git_logs),
        "review_turnaround": measure_review_time(git_logs),
        "deployment_frequency": count_deployments(git_logs)
    }

# 代码质量指标
def assess_code_quality(git_data):
    return {
        "test_coverage": analyze_test_coverage(git_data),
        "code_complexity": measure_complexity(git_data),
        "bug_density": calculate_bug_density(git_data),
        "technical_debt": assess_technical_debt(git_data)
    }
```

### 3.2 定性分析辅助 (80-85% AI驱动)
**流程质量评估**:
```python
# AI定性分析提示模板
WORKFLOW_QUALITY_PROMPT = """
分析Git工作流的设计质量：

**效率维度分析**：
1. 开发流程的顺畅性和阻塞点
2. 团队协作的效率瓶颈
3. 代码审查的有效性和及时性
4. 发布部署的自动化程度

**质量维度分析**：
1. 代码质量的稳定性和一致性
2. 问题发现和解决的及时性
3. 知识传承和文档完整性
4. 团队技能提升和最佳实践

**适应性维度分析**：
1. 项目规模变化的适应性
2. 团队结构调整的灵活性
3. 技术栈演化的支持度
4. 业务需求变化的响应速度
"""
```

## 4. 应用场景对齐

### 4.1 新项目初始化场景
**场景特征**: 项目启动，团队组建，工具链建立
**优化重点**:
- 快速建立Git工作流
- 适合团队的分支策略
- 清晰的提交规范
- 基础质量检查

### 4.2 团队协作改进场景
**场景特征**: 现有团队，效率问题，质量改进需求
**优化重点**:
- 痛点分析和解决
- 流程优化和自动化
- 团队培训和规范
- 工具集成和配置

### 4.3 AI项目治理场景
**场景特征**: AI工具使用，文件管理混乱，版本控制问题
**优化重点**:
- AI文件识别和过滤
- 自动化处理机制
- 团队使用规范
- 质量保障体系

## 5. 最小上下文加载

### 5.1 上下文分层策略
**L1上下文** (必需，~200 tokens): 基础项目信息和Git现状
**L2上下文** (按需，~400 tokens): 团队结构和协作模式
**L3上下文** (可选，~600 tokens): 工具链和CI/CD配置
**L4上下文** (扩展，~800 tokens): 质量要求和发布策略
**L5上下文** (完整，~1000 tokens): 业务背景和团队能力

### 5.2 智能上下文加载
```python
# 上下文需求评估
def evaluate_git_context_needs(project_info):
    complexity = assess_git_complexity(project_info)
    
    if complexity == "simple":
        return ["L1", "L2"]
    elif complexity == "medium":
        return ["L1", "L2", "L3"]
    elif complexity == "complex":
        return ["L1", "L2", "L3", "L4"]
    else:
        return ["L1", "L2", "L3", "L4", "L5"]

# 动态上下文加载
def load_git_context_dynamically(level, project_info):
    context_loaders = {
        "L1": load_basic_project_info,
        "L2": load_team_structure,
        "L3": load_toolchain_config,
        "L4": load_quality_requirements,
        "L5": load_business_context
    }
    return context_loaders[level](project_info)
```

## 6. 实施规范

### 6.1 技术实施规范
- **配置模板化**: 所有Git配置基于可重用模板
- **规则自动化**: 自动化的规则检查和执行
- **监控可视化**: Git使用情况的可视化监控
- **文档同步**: 配置变更的自动文档更新

### 6.2 质量保证规范
- **配置验证**: Git配置的自动化验证
- **流程监控**: 工作流执行情况的持续监控
- **效果评估**: 配置效果的定期评估
- **持续改进**: 基于数据的配置优化

## 7. 质量评估机制

### 7.1 定量评估指标 (90-95% 程序化)
```python
# Git工作流质量指标
def evaluate_git_workflow_quality(git_metrics):
    return {
        "efficiency_score": calculate_efficiency_score(git_metrics),
        "quality_score": assess_code_quality_score(git_metrics),
        "collaboration_score": measure_collaboration_score(git_metrics),
        "automation_score": evaluate_automation_score(git_metrics)
    }

# 团队协作效率指标
def measure_team_efficiency(team_data, git_data):
    return {
        "commit_productivity": calculate_commit_productivity(git_data),
        "review_efficiency": measure_review_efficiency(team_data),
        "merge_success_rate": calculate_merge_success_rate(git_data),
        "deployment_frequency": assess_deployment_frequency(git_data)
    }
```

### 7.2 定性评估维度 (80-85% AI驱动)
```python
# AI定性评估框架
GIT_WORKFLOW_EVALUATION = """
评估Git工作流的综合质量：

**流程效率维度**：
1. 开发流程的顺畅性和自动化程度
2. 代码审查的及时性和有效性
3. 问题发现和解决的效率
4. 发布部署的稳定性和频率

**协作质量维度**：
1. 团队沟通的效率和清晰度
2. 知识共享和传承的完整性
3. 冲突解决和决策的及时性
4. 新成员融入和学习曲线

**技术质量维度**：
1. 代码质量的稳定性和一致性
2. 架构演化的合理性和可控性
3. 技术债务的管理和清理
4. 安全性和合规性的保障

**业务价值维度**：
1. 需求响应的及时性和准确性
2. 功能交付的可靠性和质量
3. 用户反馈的处理和改进
4. 业务目标的达成和超越
"""
```

通过这套完整的优化规范，git-operations技能能够提供专业、高效的Git工作流管理能力，确保团队协作效率最大化，同时有效防止AI文件污染，保障代码质量和项目健康。