# DSGS智能架构师项目目录结构

## 项目概述
基于Claude Skills框架实现DSGS智能架构师系统，支持复杂项目的分层架构设计、任务分解、智能体化和约束生成。

## 根目录结构
```
DNASPEC-Project/
├── README.md                           # 项目说明文档
├── PROJECT_PLAN.md                     # 项目实施计划
├── docs/                              # 文档目录
├── src/                               # 源代码目录
├── skills/                            # Claude Skills根目录
├── workspace/                         # 工作目录（中间过程文档）
├── output/                            # 输出目录（最终结果）
└── tests/                             # 测试目录
```

## docs/ - 文档目录结构
```
docs/
├── architecture/                      # 架构设计文档
│   ├── DSGS_CLAUDE_SKILLS_ARCHITECTURE.md  # 主架构设计
│   ├── BIOLOGICAL_ARCHITECTURE_DESIGN.md   # 生物学架构设计
│   ├── TECHNICAL_IMPLEMENTATION_ROADMAP.md # 技术实现路线图
│   └── CORE_REQUIREMENTS_AND_GOALS.md      # 核心需求与目标
│
├── design/                            # 设计文档
│   ├── CLAUDE_SKILLS_STYLE_DESIGN.md       # Skills风格设计
│   ├── CLI_COLLABORATION_WORKFLOW.md       # CLI协作工作流
│   └── CORE_SKILLS_DEFINITION.md           # 核心技能定义
│
├── research/                          # 研究文档
│   ├── CLAUDE_SKILLS_LEARNING_SUMMARY.md   # Skills学习总结
│   └── CONTEXT_ENGINEERING_RESEARCH.md     # 上下文工程研究
│
├── specifications/                    # 规范文档
│   ├── HIERARCHICAL_AGENT_SPECIFICATION.md # 层次智能体规范
│   ├── COLLABORATION_WORKFLOW_STANDARD.md  # 协作流程标准
│   └── SYSTEM_PROMPTS/                     # 系统提示词
│       ├── SYSTEM_ARCHITECT_PROMPT.md
│       ├── TASK_DECOMPOSER_PROMPT.md
│       ├── ATOMIC_VALIDATOR_PROMPT.md
│       ├── COMPLEXITY_EVALUATOR_PROMPT.md
│       ├── QUALITY_ASSURANCE_REVIEWER_PROMPT.md
│       ├── CORE_ALIGNMENT_AUDITOR_PROMPT.md
│       ├── TDD_DEVELOPER_PROMPT.md
│       ├── TEST_ENGINEER_PROMPT.md
│       └── DISPUTE_RESOLUTION_ARBITRATOR_PROMPT.md
│
└── reports/                           # 报告文档
    ├── PROGRESS_REPORTS/                   # 进度报告
    ├── TEST_REPORTS/                       # 测试报告
    ├── VALIDATION_REPORTS/                 # 验证报告
    └── FINAL_DELIVERY/                     # 最终交付报告
```

## skills/ - Claude Skills根目录结构
```
skills/
├── dnaspec-architect/                    # 主技能目录
│   ├── SKILL.md                           # 主技能定义
│   ├── scripts/                           # 主技能脚本
│   ├── references/                        # 主技能参考文档
│   └── assets/                            # 主技能资源文件
│
├── sub-skills/                        # 子技能目录
│   ├── system-architect/                  # 系统架构师技能
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── assets/
│   │
│   ├── task-decomposer/                   # 任务分解技能
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── assets/
│   │
│   ├── atomic-verifier/                   # 原子验证技能
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── assets/
│   │
│   ├── agent-creator/                     # 智能体创建技能
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── assets/
│   │
│   ├── constraint-generator/              # 约束生成技能
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── assets/
│   │
│   └── ... (其他核心技能)
│
├── workflows/                         # 工作流定义
│   ├── architecture.workflow
│   ├── decomposition.workflow
│   ├── agent.workflow
│   └── constraint.workflow
│
└── templates/                         # 技能模板
    ├── skill_template.md
    └── script_template.py
```

## workspace/ - 工作目录结构（中间过程文档）
```
workspace/
├── analysis/                          # 分析过程文档
│   ├── project_analysis/
│   ├── task_decomposition/
│   └── constraint_analysis/
│
├── design/                            # 设计过程文档
│   ├── architecture_design/
│   ├── agent_design/
│   └── workflow_design/
│
├── implementation/                    # 实现阶段文档
│   ├── skill_development/
│   ├── script_development/
│   └── integration/
│
├── testing/                           # 测试过程文档
│   ├── unit_tests/
│   ├── integration_tests/
│   └── end_to_end_tests/
│
└── validation/                        # 验证过程文档
    ├── functional_validation/
    ├── performance_validation/
    └── quality_assurance/
```

## output/ - 输出目录结构（最终结果）
```
output/
├── final_skills/                      # 最终测试通过的Skills
│   ├── dnaspec-architect/
│   ├── sub-skills/
│   └── packaged_skills/               # 打包的技能文件
│
├── generated_artifacts/               # 生成的工件
│   ├── architecture_documents/
│   ├── task_decompositions/
│   ├── agent_specifications/
│   └── constraint_definitions/
│
├── test_results/                      # 测试结果
│   ├── final_test_reports/
│   ├── validation_certificates/
│   └── performance_benchmarks/
│
└── delivery_packages/                 # 交付包
    ├── version_releases/
    ├── documentation_packages/
    └── deployment_packages/
```

## tests/ - 测试目录结构
```
tests/
├── unit_tests/                        # 单元测试
│   ├── skill_tests/
│   ├── script_tests/
│   └── component_tests/
│
├── integration_tests/                 # 集成测试
│   ├── workflow_tests/
│   ├── skill_integration_tests/
│   └── tool_integration_tests/
│
├── end_to_end_tests/                  # 端到端测试
│   ├── scenario_tests/
│   ├── use_case_tests/
│   └── acceptance_tests/
│
└── validation_tests/                  # 验证测试
    ├── functional_validation/
    ├── performance_validation/
    └── security_validation/
```

## 目录管理原则

### 1. 文档分类管理
- **架构文档**: 系统设计和架构相关文档
- **设计文档**: 具体功能和实现设计文档
- **研究文档**: 技术研究和学习总结文档
- **规范文档**: 系统规范和标准文档
- **报告文档**: 项目进展和测试报告文档

### 2. 技能目录管理
- **主技能**: 核心协调技能
- **子技能**: 功能性子技能
- **工作流**: 技能协作工作流
- **模板**: 技能开发模板

### 3. 工作目录管理
- **分析阶段**: 需求和分析文档
- **设计阶段**: 设计和规划文档
- **实现阶段**: 开发和集成文档
- **测试阶段**: 测试和验证文档

### 4. 输出目录管理
- **最终技能**: 通过测试的技能文件
- **生成工件**: 系统生成的文档和规范
- **测试结果**: 完整的测试报告和验证结果
- **交付包**: 可交付的版本和部署包

这种目录结构确保了项目的清晰组织，便于团队协作、版本控制和项目管理。