# DNASPEC Git - 基础应用

## 智能提交信息生成

### Conventional Commits规范

```
格式：<type>(<scope>): <subject>

类型（type）：
- feat: 新功能
- fix: Bug修复
- docs: 文档更新
- style: 代码格式（不影响功能）
- refactor: 重构（不是新功能也不是修复）
- test: 添加测试
- chore: 构建/工具/辅助功能

示例：
feat: Add user authentication
fix(auth): Resolve token expiration issue
docs: Update API documentation
refactor(auth): Simplify login logic
```

### 分支命名规范

```
feature/  - 新功能
fix/      - Bug修复
hotfix/   - 紧急修复
release/  - 发布准备
refactor/ - 重构
test/     - 实验性功能

示例：
feature/user-authentication
fix/login-bug
hotfix/security-patch
```

### 基础工作流

```
1. 创建功能分支
   git checkout -b feature/user-auth

2. 开发并提交
   git add .
   git commit -m "feat: Add user authentication"

3. 合并到主分支
   git checkout main
   git merge feature/user-auth
   git branch -d feature/user-auth
```

## 版本标签基础

### 语义化版本

```
格式：MAJOR.MINOR.PATCH

- MAJOR: 不兼容的API变更
- MINOR: 向后兼容的新功能
- PATCH: 向后兼容的Bug修复

示例：
1.0.0 → 1.0.1: Bug修复
1.0.0 → 1.1.0: 新功能（向后兼容）
1.0.0 → 2.0.0: API变更（不兼容）
```

创建标签：
```bash
git tag -a v1.0.0 -m "Release: User authentication"
git push origin v1.0.0
```
