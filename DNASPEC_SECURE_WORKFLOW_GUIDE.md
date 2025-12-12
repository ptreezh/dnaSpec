# DNASPEC 安全工作流使用指南

## 概述

DNASPEC采用**三阶段安全工作流**确保AI生成内容的安全管理：
- **临时工作区** (temp_workspace) - AI生成内容安全隔离
- **缓冲区** (staging_area) - 待核验内容缓冲
- **工作区** (workspace) - 已核验内容，可提交到Git

## 完整初始化流程

### 1. 项目初始化

```bash
# 在项目目录中运行
cd /path/to/your/project
dnaspec init
```

#### 初始化输出示例

```
🚀 DNASPEC Complete Project Initialization
============================================================
🧬 DNA SPEC Context System - 安全工作流 + 渐进式披露
============================================================

This will create a secure AI-assisted development environment with:
  • Progressive disclosure directory structure
  • Secure workflow: Temp → Staging → Workspace → Git
  • AI CLI tool integration
  • Safety buffers and verification system

🏗️  Creating DNASPEC secure directory structure...
📁 Creating secure directory structure...
  ✅ Created: .dnaspec
  ✅ Created: .dnaspec/temp_workspace
  ✅ Created: .dnaspec/staging_area
  ✅ Created: .dnaspec/workspace
  ✅ Created: .dnaspec/docs
  ✅ Created: .dnaspec/logs
  ✅ Created: .dnaspec/config
  ✅ Created .gitignore for security isolation

📋 Setting up progressive disclosure system...
  ✅ Progressive disclosure system configured

🔒 Configuring secure workflow...
  ✅ Secure workflow system configured
  ✅ Workflow management scripts created

🔍 Scanning for AI CLI tools...

✅ Found 3 AI CLI tool(s):
  1. Claude
     Version: 1.2.0
  2. Qwen
     Version: 2.1.3
  3. IFlow
     Version: 0.9.5

Select deployment target:
  0. Deploy to all detected platforms
  1-3. Deploy to specific platform
  s. Skip AI CLI integration (directories only)
  q. Quit

Enter your choice: 0

🚀 Deploying DNASPEC skills to 3 platform(s)...

============================================================
🎉 DNASPEC Complete Initialization Successful!
============================================================
```

### 2. 创建的目录结构

初始化后，项目将包含以下安全目录结构：

```
your-project/
├── .dnaspec/                    # DNASPEC配置和管理目录
│   ├── temp_workspace/          # AI生成内容暂存区（Git忽略）
│   │   ├── ai_generated/        # AI生成的文件
│   │   └── experiments/         # 实验性内容
│   ├── staging_area/            # 待核验内容缓冲区（Git忽略）
│   │   ├── pending_review/      # 待审查文件
│   │   └── verified/           # 已验证待提升文件
│   ├── workspace/               # 已核验工作区（Git跟踪）
│   │   ├── src/                # 源代码
│   │   ├── docs/               # 文档
│   │   └── tests/              # 测试
│   ├── docs/                    # 渐进式披露文档
│   │   ├── basic_README.md     # 基础级别文档
│   │   ├── intermediate_README.md # 中级文档
│   │   └── advanced_README.md  # 高级文档
│   ├── config/                  # 配置文件
│   │   ├── progressive_disclosure.json
│   │   └── secure_workflow.json
│   ├── logs/                    # 系统日志
│   └── scripts/                 # 工作流管理脚本
│       ├── verify_and_stage.py   # 验证和暂存脚本
│       └── promote_to_workspace.py # 提升脚本
├── .iflow/                     # IFlow CLI命令（如果安装）
├── .qwen/                      # Qwen CLI命令（如果安装）
└── ...                         # 其他项目文件
```

## 安全工作流使用

### 第一阶段：AI生成内容进入临时工作区

使用AI CLI工具生成内容，内容自动保存到临时工作区：

```bash
# 在Claude CLI中
/speckit.dnaspec.temp-workspace operation=create

# 生成代码文件
/speckit.dnaspec.temp-workspace operation=add-file file_path=user_auth.py content="
import hashlib
import bcrypt

class UserAuth:
    def __init__(self):
        self.users = {}

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify_password(self, password, hashed):
        return bcrypt.checkpw(password.encode(), hashed)
"
```

生成的文件保存在：
```
.dnaspec/temp_workspace/ai_generated/user_auth.py
```

### 第二阶段：验证和暂存

验证AI生成的内容后移至缓冲区：

```bash
# 使用验证脚本
python .dnaspec/scripts/verify_and_stage.py .dnaspec/temp_workspace/ai_generated/user_auth.py

# 输出示例
📋 Verifying: user_auth.py
✅ Valid: True
⚠️  Issues:
  - File contains TODO or FIXME markers
💡 Suggestions:
  - Consider completing todos before staging

Stage this file? (y/n): y
✅ Staged to: .dnaspec/staging_area/pending_review/user_auth.py
Remove original from temp_workspace? (y/n): y
🗑️  Removed from temp_workspace
```

### 第三阶段：提升到工作区

将已验证的文件提升到工作区（可提交到Git）：

```bash
# 提升已验证文件到工作区
python .dnaspec/scripts/promote_to_workspace.py .dnaspec/staging_area/verified/user_auth.py

# 输出示例
📋 Promoting: user_auth.py
Promote to workspace (Git-tracked)? (y/n): y
✅ Promoted to: .dnaspec/workspace/src/user_auth.py

💡 File is now ready for Git commit
   Run: git add workspace/ && git commit -m 'Add verified AI-generated content'
```

### 第四阶段：Git提交

仅将工作区内容提交到Git仓库：

```bash
# 添加工作区内容到Git
git add .dnaspec/workspace/

# 提交
git commit -m "feat: Add verified AI-generated user authentication module"

# 推送到远程仓库
git push
```

## 渐进式披露系统

### 披露级别

1. **基础级别 (Basic)**
   - 访问权限：公开 (Public)
   - 包含：README.md、docs/overview/
   - 适用：客户、外部用户

2. **中级 (Intermediate)**
   - 访问权限：团队 (Team)
   - 包含：docs/api/、docs/guides/、tests/、config/
   - 适用：开发团队成员

3. **高级 (Advanced)**
   - 访问权限：内部 (Internal)
   - 包含：docs/internal/、ops/、scripts/、.dnaspec/internal/
   - 适用：核心开发、运维人员

### 使用示例

```bash
# 查看当前披露级别配置
cat .dnaspec/config/progressive_disclosure.json

# 创建各披露级别的文档
mkdir -p .dnaspec/workspace/docs/overview
mkdir -p .dnaspec/workspace/docs/api
mkdir -p .dnaspec/workspace/docs/internal
```

## AI CLI技能使用

### 上下文分析

```bash
# 在Claude CLI中
/dnaspec.context-analysis "分析这个用户认证系统需求文档的质量和完整性"

# 在Qwen CLI中
/dnaspec.context-analysis "分析这个系统设计文档的清晰度和一致性"
```

### 系统架构设计

```bash
# 使用架构师技能
/dnaspec.architect "设计一个支持用户注册、登录、密码重置的认证系统"
```

### Git操作

```bash
# 安全的Git操作（通过工作区）
/dnaspec.git-operations operation=status
/dnaspec.git-operations operation=commit message="feat: 添加验证后的AI生成代码"
```

### 认知模板

```bash
# 应用验证检查模板
/dnaspec.cognitive-template "审查这个系统设计方案" template=verification

# 应用思维链模板
/dnaspec.cognitive-template "分析这个复杂的业务逻辑" template=chain_of_thought
```

## 管理命令

### 系统状态检查

```bash
# 检查DNASPEC系统状态
dnaspec status

# 输出示例
🔍 DNASPEC System Status
========================
✅ Secure Workflow: Active
✅ Progressive Disclosure: Configured
✅ AI CLI Integration: 3 platforms
📁 Workspace: .dnaspec/workspace/
🔒 Temp Files: 0
⏳ Staged Files: 2
```

### 验证集成

```bash
# 验证所有AI CLI工具集成
dnaspec validate

# 输出示例
🧪 Validating DNASPEC Integrations
==================================
✅ Claude CLI: OK
✅ Qwen CLI: OK
✅ IFlow CLI: OK
```

### 清理临时文件

```bash
# 清理过期的临时文件
dnaspec clean

# 输出示例
🧹 Cleaning up temporary files...
🗑️  Removed 3 expired files from temp_workspace
✅ Cleanup completed
```

## 安全最佳实践

### 1. 严格遵循工作流

```bash
# ❌ 错误：直接提交AI生成内容
git add temp_workspace/  # 不要这样做！

# ✅ 正确：遵循三阶段工作流
AI生成 → temp_workspace → staging_area → workspace → Git
```

### 2. 定期验证

```bash
# 定期验证待暂存文件
python .dnaspec/scripts/verify_and_stage.py .dnaspec/temp_workspace/ai_generated/*

# 批量提升验证文件
python .dnaspec/scripts/promote_to_workspace.py .dnaspec/staging_area/verified/*
```

### 3. 访问控制

```bash
# 根据团队角色设置文档访问权限
# 基础文档 → 公开
# 技术文档 → 团队
# 内部文档 → 核心团队
```

### 4. 定期清理

```bash
# 设置定时任务清理临时文件
# 建议每周运行一次
dnaspec clean
```

## 故障排除

### 常见问题

1. **文件验证失败**
   ```bash
   # 检查验证规则
   cat .dnaspec/config/secure_workflow.json

   # 手动验证文件
   python .dnaspec/scripts/verify_and_stage.py path/to/file
   ```

2. **AI CLI技能不工作**
   ```bash
   # 检查集成状态
   dnaspec validate

   # 重新部署技能
   dnaspec deploy
   ```

3. **工作区文件未Git跟踪**
   ```bash
   # 检查.gitignore设置
   cat .dnaspec/.gitignore

   # 手动添加工作区到Git
   git add .dnaspec/workspace/
   git commit -m "Add workspace directory to Git tracking"
   ```

### 调试模式

```bash
# 启用详细日志
export DNASPEC_DEBUG=1
dnaspec init

# 查看系统日志
tail -f .dnaspec/logs/system.log
```

## 进阶功能

### 1. 自定义验证规则

编辑 `.dnaspec/config/secure_workflow.json` 添加自定义验证规则：

```json
{
  "custom_validation_rules": [
    {
      "name": "security_check",
      "pattern": "password|secret|key|token",
      "action": "flag"
    },
    {
      "name": "todo_check",
      "pattern": "TODO|FIXME",
      "action": "warn"
    }
  ]
}
```

### 2. 自动化工作流

创建自动化脚本：

```bash
#!/bin/bash
# auto_verify_and_promote.sh

# 验证所有临时文件
for file in .dnaspec/temp_workspace/ai_generated/*; do
    if [ -f "$file" ]; then
        python .dnaspec/scripts/verify_and_stage.py "$file"
    fi
done

# 提升所有已验证文件
for file in .dnaspec/staging_area/verified/*; do
    if [ -f "$file" ]; then
        python .dnaspec/scripts/promote_to_workspace.py "$file"
    fi
done

echo "✅ Automated workflow completed"
```

### 3. 集成CI/CD

在CI/CD管道中集成安全检查：

```yaml
# .github/workflows/dnaspec-security.yml
name: DNASPEC Security Check

on: [push, pull_request]

jobs:
  security-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Check for forbidden files
      run: |
        if git ls-files | grep -E "temp_workspace|staging_area"; then
          echo "❌ Forbidden files found in commit"
          exit 1
        fi

    - name: Validate workspace structure
      run: |
        python .dnaspec/scripts/validate_workspace.py
```

---

📚 **更多信息**：
- [项目地址](https://github.com/ptreezh/dnaSpec)
- [问题反馈](https://github.com/ptreezh/dnaSpec/issues)
- [社区讨论](https://github.com/ptreezh/dnaSpec/discussions)

🔒 **记住**：安全工作流是DNASPEC的核心特性，请始终遵循三阶段安全流程！