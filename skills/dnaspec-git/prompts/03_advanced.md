# DNASPEC Git - 高级应用

## 企业级Git工作流

### 大型团队Git Flow

```
分支结构：
main        - 生产环境，稳定版本
develop     -开发集成分支
feature/*   - 功能开发分支
release/*   - 发布准备分支
hotfix/*    - 紧急修复分支

工作流程：
1. feature从develop创建，合并回develop
2. release从develop创建，合并回main和develop
3. hotfix从main创建，合并回main和develop
4. main始终可部署
5. 定期从develop合并到main进行发布
```

### 严格Code Review

```yaml
PR检查清单：
  - [ ] 通过所有自动化测试
  - [ ] 代码覆盖率不降低
  - [ ] 符合代码规范
  - [ ] 至少一人审查通过
  - [ ] 文档已更新
  - [ ] 没有敏感信息泄露

自动化：
  - CI测试自动运行
  - 代码质量检查（SonarQube）
  - 安全扫描
  - 性能测试
```

## 智能版本管理

### 基于提交历史的版本推荐

```yaml
分析：
  breaking_changes: 2    # 破坏性变更数量
  new_features: 5        # 新功能数量
  bug_fixes: 3           # Bug修复数量

推荐版本号：2.0.0

推理：
  - 有2个破坏性变更 → MAJOR版本升级
  - 5个新功能值得发布
  - 3个Bug修复包含在内

发布说明生成：
  自动生成release notes
  - 列出新特性
  - 列出Bug修复
  - 标记破坏性变更
  - 提供迁移指南
```

### 持续部署版本策略

```yaml
策略：
  - 使用语义化版本
  - 自动生成版本号
  - 自动创建git标签
  - 自动生成release notes
  - 自动部署到环境

自动化流程：
  1. 代码合并到main
  2. CI/CD自动运行
  3. 自动生成版本号（如：1.2.3）
  4. 自动创建git标签
  5. 自动生成release notes
  6. 自动部署到生产环境
```

## Git工作流优化

### 从简单到复杂演化

```
阶段1：单人项目（简单）
├─ 工作流：直接提交到main
├─ 分支：无
└─ 提交：自由格式

↓ 逐步演化

阶段2：小团队协作（稍复杂）
├─ 工作流：Feature Branch
├─ 分支：feature/*
├─ 提交：规范化格式
└─ 合并：Pull Request + Code Review

↓ 继续演化

阶段3：正式发布管理（复杂）
├─ 工作流：Git Flow
├─ 分支：main + develop + feature/* + release/* + hotfix/*
├─ 提交：严格规范
├─ 合并：PR + CI + Review
└─ 发布：版本标签 + 发布说明

关键：从简单到复杂逐步演化，而不是一开始就使用最复杂的
```

### 上下文感知的建议

```yaml
项目上下文分析：
  - 检测项目类型（前端/后端/全栈）
  - 检测团队规模（单人/小团队/大团队）
  - 检测开发阶段（原型/开发/维护）

Git历史分析：
  - 分析提交历史模式
  - 学习项目特定的提交信息风格
  - 适应项目分支策略

定制化建议：
  - 根据项目特点定制建议
  - 尊重现有工作模式
  - 渐进式改进建议
```

## 版本管理最佳实践

### 提交信息质量

```yaml
高质量提交信息：
  - 符合Conventional Commits规范
  - 准确描述变更内容
  - 提供足够的上下文
  - 不包含敏感信息
  - 使用祈使句语气
  - 限制首行长度（50字符内）

示例：
❌ "fixed bug"
✅ "fix(auth): Resolve token expiration issue"

❌ "update"
✅ "docs: Update API documentation for v2.0"
```

### 分支管理最佳实践

```yaml
分支命名：
  - 清晰描述目的
  - 使用一致的约定
  - 包含相关issue/PR编号
  - 避免过长或过短

示例：
✅ feature/user-authentication
✅ fix/123-login-bug
✅ release/v2.0.0

❌ auth
❌ stuff
❌ feature/very-long-branch-name-that-is-hard-to-read
```

### 发布管理

```yaml
发布准备：
  1. 创建release分支
     git checkout -b release/v2.0.0

  2. 完成发布准备
     - 更新版本号
     - 更新CHANGELOG
     - 更新文档

  3. 测试发布版本
     - 完整回归测试
     - 性能测试
     - 安全扫描

  4. 合并到main和develop
     git checkout main
     git merge release/v2.0.0

  5. 创建发布标签
     git tag -a v2.0.0 -m "Release 2.0.0"

  6. 推送和发布
     git push origin main v2.0.0
     在GitHub创建Release
```

## 协作技能整合

```yaml
与workspace技能协作：
  - Git管理代码版本
  - Workspace管理临时文件
  - 配合实现完整的版本管理

与context-optimization协作：
  - 优化提交信息
  - 使其简洁清晰
  - 符合上下文预算原则

与task-decomposer协作：
  - 任务分解
  - 将大任务分解为原子提交
  - 每个提交独立可测试
```
