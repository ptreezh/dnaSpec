# DNASPEC Git - 中级应用

## Git工作流选择

### 根据项目特点选择工作流

**单人项目**：
- 推荐：Centralized Workflow
- 特点：直接提交到main
- 优势：最简单，无协作开销

**小团队（2-5人）**：
- 推荐：Feature Branch Workflow
- 特点：每个功能一个分支，通过PR合并
- 优势：平衡简单和协作

**中大型团队（5-20人）**：
- 推荐：Git Flow
- 特点：main + develop + feature + release + hotfix
- 优势：结构清晰，发布管理

**持续部署项目**：
- 推荐：GitHub Flow
- 特点：main + feature，通过PR部署
- 优势：简单，适合CI/CD

## 智能提交信息生成

### 分析Git变更

```yaml
输入：git diff --staged

分析维度：
- 变更类型检测（feat/fix/docs/refactor/test/chore）
- 变更范围识别（模块/功能）
- 影响范围评估
- 关键变更点提取

示例：
变更：
- added: ["src/auth/login.js", "src/auth/register.js"]
- modified: ["src/app.js"]

检测结果：
  type: "feat"  # 新功能
  scope: "authentication"
  impact: "medium"

建议提交信息：
"feat: Add user authentication (login, registration)"
```

## 分支管理策略

### Feature Branch工作流

```
1. 从develop创建feature分支
   git checkout develop
   git checkout -b feature/user-auth

2. 在feature分支开发
   - 阶段性提交
   - 保持更新：git pull origin develop

3. 通过PR合并
   - 创建Pull Request
   - 代码审查
   - 合并到develop

4. 清理分支
   git branch -d feature/user-auth
```

### 原子化提交

```
原则：每个提交只做一件事

❌ 一次性提交所有更改
✅ 拆分为多个原子提交

示例：
提交1：重构准备（不改变功能）
提交2：提取认证逻辑（不改变功能）
提交3：改进错误处理（功能改进）
提交4：添加单元测试（不改变功能）
提交5：更新文档（不改变功能）
```

## 合并冲突解决

### 冲突类型

```
1. same_line_changes - 同一行被不同方式修改
2. adjacent_changes - 相邻行被修改
3. file_deleted - 一方删除，一方修改
4. rename_conflict - 文件被重命名
```

### 解决策略

```
1. 识别冲突文件
   git status

2. 分析冲突类型和复杂度
   - 低：1-2个冲突文件
   - 中：3-5个冲突文件
   - 高：6+个冲突文件

3. 解决建议
   - 理解两处修改的意图
   - 选择：合并/选择版本/手动编写

4. 验证解决
   git add .
   git commit
```

## AI辅助开发的版本管理

```
1. 创建AI工作分支
   git checkout -b ai-assist/user-auth-ai-gen

2. AI生成代码并人工审查
   - 代码质量检查
   - 安全性检查
   - 功能测试

3. 标记AI参与
   提交信息包含：
   - AI生成了认证模块代码
   - 人工审查通过
   - 测试覆盖率85%

4. 创建审查PR
   PR标题："feat: User authentication (AI-assisted, reviewed)"
```
