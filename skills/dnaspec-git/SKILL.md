---
name: dnaspec-git
description: Assist with version management using Git for AI-assisted development. Provides intelligent commit suggestions, branch management guidance, conflict resolution assistance, and workflow optimization. When you need help with Git operations, version control guidance, commit message generation, or merge conflict resolution, use this skill.
---

# DNASPEC Git

## 使用时机

当用户提到以下需求时，使用此技能：
- "版本管理" 或 "version management"
- "Git操作" 或 "git operations"
- "提交建议" 或 "commit suggestion"
- "分支管理" 或 "branch management"
- "冲突解决" 或 "conflict resolution"
- "Git工作流" 或 "git workflow"
- "提交信息生成" 或 "commit message generation"
- 需要Git版本管理指导
- 需要智能提交建议
- 需要合并冲突解决辅助
- 需要分支策略建议

**不要在以下情况使用**：
- ❌ 强制执行Git规则（这是用户的责任）
- ❌ 替代Git命令（使用Git本身）
- ❌ 强制代码质量检查（使用专门的测试工具）

## 核心理念

### 🎯 版本管理辅助（Version Management Assistance）

**什么是版本管理辅助？**

dnaspec-git 是一个辅助工具，帮助用户更有效地使用Git进行版本管理。它不强制规则，而是提供建议和辅助。

```
❌ 强制式Git管理的问题：

Git Hooks强制执行：
├─ 提交前检查：代码必须通过测试
│   └─ 问题：阻止用户提交，即使有合理理由
├─ 提交信息格式：必须符合规范
│   └─ 问题：格式僵化，不适应所有场景
└─ 分支保护：禁止直接推送
    └─ 问题：缺乏灵活性，影响开发效率

→ 问题：强制执行可能导致用户绕过机制
→ 问题：一刀切规则不适应所有项目
→ 问题：过度限制降低开发效率
```

```
✅ 辅助式Git管理的优势：

智能辅助建议：
├─ 提交前建议：建议测试代码，但不阻止提交
│   └─ 优势：用户可以选择是否遵循
├─ 提交信息生成：智能生成规范的提交信息
│   └─ 优势：节省时间，提高质量
└─ 分支策略建议：推荐合理的分支策略
    └─ 优势：适应项目特点，灵活调整

→ 优势：辅助而非强制
→ 优势：用户保留最终决策权
→ 优势：提高版本管理效率
→ 优势：学习和最佳实践
```

**版本管理辅助的关键原则**：

**1. 建议而非强制**
```yaml
suggestion_over_enforcement:
  principle: 提供建议，由用户决策

  commit_message:
    generation: 智能生成规范的提交信息
    suggestion: "feat: Add user authentication"
    user_override: 允许用户修改
    enforcement: false

  pre_commit_checks:
    suggestion: "建议运行测试 before commit"
    action: 显示测试命令
    user_choice: 用户可以选择跳过
    blocking: false

  branch_strategy:
    recommendation: 推荐Git Flow或Github Flow
    adaptation: 根据团队规模和项目调整
    enforcement: false
```

**2. 智能辅助**
```yaml
intelligent_assistance:
  commit_message_generation:
    input: git diff 输出
    analysis: 分析变更内容
    output: 规范的提交信息
    example:
      changes: ["Add login", "Add register", "Add password reset"]
      suggestion: "feat: Implement user authentication system"

  conflict_resolution:
    detection: 检测合并冲突
    analysis: 分析冲突原因
    suggestion: 提供解决建议
    example:
      conflict: "Both modified user.service.ts"
      suggestion: "检查两处修改，合并逻辑或选择版本"

  branch_management:
    workflow_suggestion: 根据项目特点推荐工作流
    example:
      small_team: "建议使用 simplified Git Flow"
      large_team: "建议使用 full Git Flow with release branches"
      solo_dev: "建议使用 simple feature branch workflow"
```

**3. 上下文感知**
```yaml
context_awareness:
  project_context:
    - 检测项目类型（前端/后端/全栈）
    - 检测团队规模（单人/小团队/大团队）
    - 检测开发阶段（原型/开发/维护）

  git_history_analysis:
    - 分析提交历史模式
    - 学习项目特定的提交信息风格
    - 适应项目分支策略

  customized_suggestions:
    - 根据项目特点定制建议
    - 尊重现有工作模式
    - 渐进式改进建议
```

### 🎯 Git工作流优化（Git Workflow Optimization）

**什么是Git工作流优化？**

根据项目特点和团队情况，优化Git工作流程，提高版本管理效率。

```
常见Git工作流：

1. Centralized Workflow（集中式工作流）
   适用于：单人项目或小团队
   特点：所有人都向main分支提交
   优势：简单
   劣势：容易冲突

2. Feature Branch Workflow（功能分支工作流）
   适用于：小到中型团队
   特点：每个功能一个分支，通过PR合并
   优势：隔离开发，代码审查
   劣势：分支管理复杂

3. Git Flow Workflow（Git Flow工作流）
   适用于：有明确发布计划的项目
   特点：main + develop + feature + release + hotfix
   优势：结构清晰，发布管理
   劣势：复杂性高

4. GitHub Flow / GitLab Flow（简化工作流）
   适用于：持续部署项目
   特点：main + feature，通过PR部署
   优势：简单，适合CI/CD
   劣势：需要良好的自动化
```

**工作流选择建议**：

```yaml
workflow_selection:
  solo_developer:
    recommended: Centralized Workflow
    reason: 最简单，无协作开销
    alternative: Feature Branch（如果需要隔离功能）

  small_team_2-5:
    recommended: Feature Branch Workflow
    reason: 平衡简单和协作
    alternative: GitHub Flow（如果使用PR）

  medium_team_5-20:
    recommended: Git Flow
    reason: 结构清晰，适合有发布计划的项目
    alternative: GitHub Flow（如果持续部署）

  large_team_20+:
    recommended: Git Flow with modifications
    reason: 需要严格的发布管理
    modifications:
      - 使用release branches
      - 严格的code review
      - 自动化测试和部署
```

### 🎯 格式塔认知原则在Git管理中的应用

**整体性原则（Whole > Sum of Parts）**：

```
❌ 孤立的Git操作：

操作1：git add .
操作2：git commit -m "fix bug"
操作3：git push

问题：看不到整体意图，提交信息不明确

✅ 整体化的Git工作流：

完整的提交周期：
1. 分析变更：查看git diff
2. 理解意图：这是一个bug修复还是新功能？
3. 生成提交信息："fix: Resolve login issue with expired tokens"
4. 执行提交：git add + git commit + git push

→ 整体性：理解变更的意图和影响
→ 提交信息：准确反映变更内容
→ 工作流：连贯的版本管理过程
```

**从简单到复杂演化**：

```
Git工作流演化路径：

阶段1：单人项目（简单）
├─ 工作流：直接提交到main
├─ 分支：无
└─ 提交：自由格式
→ 最简单的版本管理

↓ 逐步演化

阶段2：小团队协作（稍复杂）
├─ 工作流：Feature Branch
├─ 分支：feature/*
├─ 提交：规范化格式
└─ 合并：Pull Request + Code Review
→ 引入分支和审查

↓ 继续演化

阶段3：正式发布管理（复杂）
├─ 工作流：Git Flow
├─ 分支：main + develop + feature/* + release/* + hotfix/*
├─ 提交：严格规范
├─ 合并：PR + CI + Review
└─ 发布：版本标签 + 发布说明
→ 完整的版本管理体系

关键：从简单到复杂逐步演化，而不是一开始就使用最复杂的
```

---

## 全生命周期应用

### 📋 Idea阶段：为项目初始化版本管理

**场景**：用户有一个新项目想法，需要初始化Git

**示例**：
```
用户想法："我想做一个AI代码助手"

版本管理初始化：
📋 Git仓库初始化
步骤1：创建Git仓库
$ git init
$ git add .
$ git commit -m "Initial commit: AI Code Assistant project"

步骤2：创建README.md
包含：
- 项目描述
- 安装说明
- 使用指南

步骤3：创建.gitignore
忽略：
- node_modules/
- .dnaspec/cache/
- *.log
- dist/

步骤4：初始提交
$ git add README.md .gitignore
$ git commit -m "docs: Add README and .gitignore"

✅ 格式塔原则：简单但完整的初始化
- Git仓库建立
- 基础文档完善
- 忽略规则配置
- 准备好协作
```

### 📋 需求阶段：为功能开发创建分支

**场景**：有功能需求，需要创建feature分支

**示例**：
```
需求：实现用户认证功能

分支管理：
📋 Feature Branch工作流

步骤1：创建feature分支
$ git checkout -b feature/user-authentication

分支命名建议：
├─ feature/user-authentication  ✅ 清晰
├─ feature/add-login           ✅ 清晰
└─ feature/auth                ⚠️ 稍模糊（什么认证？）

步骤2：开发功能
在feature分支上进行开发
├─ 实现登录
├─ 实现注册
└─ 实现密码重置

步骤3：阶段性提交
$ git add auth/login.js
$ git commit -m "feat: Add login functionality"

$ git add auth/register.js
$ git commit -m "feat: Add user registration"

$ git add auth/reset.js
$ git commit -m "feat: Add password reset"

提交信息生成建议：
- 自动分析git diff
- 生成规范的提交信息
- 用户可以修改

步骤4：合并到main
$ git checkout main
$ git merge feature/user-authentication
$ git branch -d feature/user-authentication

✅ 分支隔离：
- 功能开发不影响主分支
- 清晰的提交历史
- 易于回滚和审查
```

### 📋 细化阶段：处理复杂提交场景

**场景**：复杂功能需要细粒度提交

**示例**：
```
细化需求：重构用户认证模块

细化提交策略：
📋 原子化提交

原计划：一次性提交所有更改
❌ 问题：提交过大，难以审查

细化后：拆分为多个原子提交

提交1：重构准备
$ git commit -m "refactor: Prepare for authentication module refactoring"
更改：
- 添加新的目录结构
- 移动文件到新位置
- 不改变功能

提交2：提取认证逻辑
$ git commit -m "refactor: Extract authentication logic into separate module"
更改：
- 创建AuthService类
- 迁移认证相关代码
- 不改变功能

提交3：改进错误处理
$ git commit -m "refactor: Improve error handling in authentication"
更改：
- 添加详细的错误信息
- 改进错误恢复
- 功能改进

提交4：添加单元测试
$ git commit -m "test: Add unit tests for authentication module"
更改：
- 添加测试用例
- 不改变功能

提交5：更新文档
$ git commit -m "docs: Update authentication documentation"
更改：
- 更新API文档
- 添加使用示例
- 不改变功能

✅ 原子化提交：
- 每个提交只做一件事
- 易于理解和审查
- 易于回滚
- 清晰的提交历史
```

### 📋 智能阶段：管理AI辅助开发的版本

**场景**：AI生成代码，需要智能版本管理

**示例**：
```
AI辅助：AI生成用户认证代码

智能版本管理：
📋 AI生成代码的版本管理

步骤1：创建AI工作分支
$ git checkout -b ai-assist/user-auth-ai-gen

步骤2：AI生成代码
AI生成文件：
- auth/login.js
- auth/register.js
- auth/reset.js

步骤3：代码审查和测试
人工审查AI生成的代码：
├─ 代码质量检查
├─ 安全性检查
└─ 功能测试

步骤4：智能提交
提交信息生成建议：
输入：git diff --staged
分析：
- 添加了三个认证功能文件
- 实现了登录、注册、密码重置
- 使用JWT认证

生成提交信息：
"feat: Implement user authentication with JWT (AI-assisted)

- Add login functionality with JWT token generation
- Add user registration with password encryption
- Add password reset with email verification
- AI-generated code, reviewed and tested by [username]"

步骤5：创建审查PR
PR标题："feat: User authentication (AI-assisted, reviewed)"
PR描述：
- AI生成了认证模块代码
- 人工审查通过
- 测试覆盖率85%
- 建议合并

步骤6：合并后打标签
$ git tag -a v1.0.0 -m "Release: User authentication feature"
$ git push origin v1.0.0

✅ AI辅助版本管理：
- 记录AI参与
- 标记人工审查
- 透明的历史记录
- 版本标签管理
```

---

## 核心功能

### 1. 智能提交信息生成

**分析Git变更**
```yaml
diff_analysis:
  input: git diff --staged

  analysis:
    - 检测变更类型（feat/fix/docs/refactor/test/chore）
    - 识别变更范围（模块/功能）
    - 提取关键变更点
    - 评估影响范围

  example:
    changes:
      - added: ["src/auth/login.js", "src/auth/register.js"]
      - modified: ["src/app.js"]
      - deleted: []

    detection:
      type: "feat"  # 新功能
      scope: "authentication"
      impact: "medium"

    suggestion: "feat: Add user authentication (login, registration)"
```

**生成提交信息**
```yaml
commit_message_generation:
  format: "Conventional Commits"

  template: "<type>(<scope>): <subject>"

  type_detection:
    feat: 新功能
    fix: Bug修复
    docs: 文档更新
    style: 代码格式（不影响功能）
    refactor: 重构（不是新功能也不是修复）
    test: 添加测试
    chore: 构建/工具/辅助功能

  examples:
    "feat: Add user authentication"
    "fix(auth): Resolve token expiration issue"
    "docs: Update API documentation"
    "refactor(auth): Simplify login logic"
    "test(auth): Add unit tests for login"
```

### 2. 分支管理辅助

**分支命名建议**
```yaml
branch_naming:
  conventions:
    feature/:  新功能
    fix/:       Bug修复
    hotfix/:    紧急修复
    release/:   发布准备
    refactor/:  重构
    test/:      实验性功能
    ai-assist/: AI辅助开发

  examples:
    feature/user-authentication  ✅
    fix/login-bug               ✅
    hotfix/security-patch       ✅
    release/v1.0.0              ✅
    refactor/auth-module        ✅
    test/new-approach           ✅
    ai-assist/code-generation   ✅
```

**分支策略建议**
```yaml
branch_strategy:
  recommendation_engine:
    input:
      - 项目规模（团队人数）
      - 发布频率
      - CI/CD成熟度
      - 团队经验

    output:
      workflow: "Git Flow / GitHub Flow / Simplified"
      reasoning: "为什么推荐这个工作流"
      adaptation: "如何适应项目特点"

  example:
    input:
      team_size: 3
      release_frequency: "weekly"
      cicd: "basic"
      experience: "intermediate"

    output:
      workflow: "Simplified Git Flow"
      reasoning: "小团队，不需要复杂的多分支管理"
      adaptation: "使用 main + develop + feature/* 分支"
```

### 3. 合并冲突解决辅助

**冲突检测**
```yaml
conflict_detection:
  analysis:
    - 识别冲突文件
    - 分析冲突类型
    - 评估冲突复杂度
    - 提供解决建议

  conflict_types:
    same_line_changes: 同一行被不同方式修改
    adjacent_changes: 相邻行被修改
    file_deleted: 一方删除，一方修改
    rename_conflict: 文件被重命名

  complexity:
    low: 1-2个冲突文件
    medium: 3-5个冲突文件
    high: 6+个冲突文件
```

**解决建议**
```yaml
resolution_suggestions:
  strategy:
    manual_review: "建议手动审查每个冲突"
    tool_assisted: "使用合并工具辅助"
    communication: "与团队成员协调"

  example:
    conflict: "src/auth/service.ts"
    situation: "Both modified login function"

    suggestions:
      - option1: "保留两个版本的逻辑"
      - option2: "合并两处修改"
      - option3: "选择一个版本，手动添加另一个版本的修改"

    guidance: "建议理解两处修改的意图，然后合并或选择"
```

### 4. 版本标签管理

**语义化版本**
```yaml
semantic_versioning:
  format: "MAJOR.MINOR.PATCH"

  rules:
    MAJOR: 不兼容的API变更
    MINOR: 向后兼容的新功能
    PATCH: 向后兼容的Bug修复

  examples:
    1.0.0 → 1.0.1: Bug修复
    1.0.0 → 1.1.0: 新功能（向后兼容）
    1.0.0 → 2.0.0: API变更（不兼容）

  recommendation:
    based_on: 分析提交历史
    factors:
      - 破坏性变更数量
      - 新功能数量
      - Bug修复数量

    example:
      breaking_changes: 2
      new_features: 5
      bug_fixes: 3
      suggestion: "2.0.0（有破坏性变更）"
```

**标签创建建议**
```yaml
tag_creation:
  when:
    - 发布新版本
    - 重要里程碑
    - 完成主要功能

  annotation:
    format: "Release <version>: <description>"
    example: "Release 1.0.0: User authentication feature"

  best_practices:
    - 使用语义化版本
    - 添加有意义的描述
    - 推送到远程仓库
    - 在GitHub上创建Release
```

---

## 输出格式

### 提交信息建议输出

```json
{
  "analysis": {
    "files_changed": 3,
    "insertions": 120,
    "deletions": 15,
    "change_type": "feature"
  },
  "suggested_commit_message": {
    "type": "feat",
    "scope": "authentication",
    "subject": "Implement user authentication with JWT",
    "body": "- Add login functionality with JWT token generation\n- Add user registration with password encryption\n- Add password reset with email verification",
    "full_message": "feat(auth): Implement user authentication with JWT\n\n- Add login functionality with JWT token generation\n- Add user registration with password encryption\n- Add password reset with email verification"
  },
  "alternative_messages": [
    "feat: Add user authentication system",
    "feat(auth): Add login, registration, and password reset"
  ]
}
```

### 分支策略建议输出

```json
{
  "project_analysis": {
    "team_size": 3,
    "release_frequency": "weekly",
    "cicd_maturity": "intermediate"
  },
  "recommended_workflow": {
    "name": "Simplified Git Flow",
    "branches": ["main", "develop", "feature/*"],
    "description": "简化的Git Flow，适合小团队"
  },
  "branch_structure": {
    "main": "生产环境，稳定版本",
    "develop": "开发集成分支",
    "feature/*": "功能开发分支，从develop创建，合并回develop"
  },
  "workflow_description": "1. 从develop创建feature分支\n2. 在feature分支开发\n3. 通过PR合并回develop\n4. 定期从develop合并到main进行发布"
}
```

---

## 质量检查清单

### 提交信息检查
- [ ] 符合Conventional Commits规范
- [ ] 准确描述变更内容
- [ ] 提供足够的上下文
- [ ] 不包含敏感信息

### 分支管理检查
- [ ] 分支命名清晰
- [ ] 分支目的明确
- [ ] 合并策略合理
- [ ] 工作流适合项目

### 版本标签检查
- [ ] 使用语义化版本
- [ ] 标签描述准确
- [ ] 推送到远程
- [ ] 创建Release

---

## 协作技能

- **dnaspec-workspace**: 工作区管理，配合Git进行文件版本管理
- **dnaspec-context-optimization**: 优化提交信息，使其简洁清晰
- **dnaspec-task-decomposer**: 任务分解，将大任务分解为可独立提交的原子任务

---

## 关键成就

1. ✅ **智能提交信息生成** - 自动分析变更，生成规范的提交信息
2. ✅ **分支管理辅助** - 推荐适合项目的分支策略和工作流
3. ✅ **合并冲突解决** - 提供冲突分析和解决建议
4. ✅ **版本标签管理** - 智能推荐版本号和创建标签
5. ✅ **全生命周期应用** - Idea→需求→细化→智能四阶段支持
6. ✅ **格式塔原则体现** - 整体性设计、从简单到复杂演化

---

*此技能提供Git版本管理的智能辅助，帮助用户更有效地使用Git进行版本控制，通过建议而非强制的方式，提高版本管理效率。*
