# DNASPEC Init 命令使用指南

## 概述

`dnaspec init` 是项目级别的初始化命令，用于检测系统中已安装的AI CLI工具，并让用户选择部署目标平台，完成DNASPEC技能的配置。

## 安装前提

### 1. 安装DNASPEC
```bash
# npm方式安装（推荐）
npm install -g dnaspec

# 或从GitHub仓库安装
npm install -g ptreezh/dnaSpec
```

### 2. 安装AI CLI工具（至少一个）

#### Claude CLI
```bash
# 安装Claude CLI
npm install -g @anthropic-ai/claude-cli

# 验证安装
claude --version
```

#### Gemini CLI
```bash
# 安装Gemini CLI
npm install -g @google-ai/gemini-cli

# 验证安装
gemini --version
```

#### Qwen CLI
```bash
# 安装Qwen CLI
pip install qwen-cli

# 验证安装
qwen --version
```

#### IFlow CLI
```bash
# 安装IFlow CLI
npm install -g iflow-cli

# 验证安装
iflow --version
```

#### QoderCLI
```bash
# 安装QoderCLI
npm install -g qodercli

# 验证安装
qodercli --version
```

#### CodeBuddy
```bash
# 安装CodeBuddy
npm install -g codebuddy-cli

# 验证安装
codebuddy --version
```

#### GitHub Copilot CLI
```bash
# 安装GitHub CLI
npm install -g gh

# 安装Copilot扩展
gh extension install github/gh-copilot

# 验证安装
gh copilot --version
```

## 使用方法

### 1. 基本初始化

在您的项目目录中运行：

```bash
cd /path/to/your/project
dnaspec init
```

### 2. 初始化流程示例

#### 场景1：检测到多个AI CLI工具

```bash
$ dnaspec init

🚀 DNASPEC Project Initialization
==================================================
Welcome to DNA SPEC Context System!
This wizard will help you configure DNASPEC skills for your AI CLI tools.

🔍 Scanning for AI CLI tools...

✅ Found 4 AI CLI tool(s):
  1. Claude
     Version: 1.2.0
     Path: /usr/local/bin/claude

  2. Qwen
     Version: 2.1.3
     Path: /usr/local/bin/qwen

  3. IFlow
     Version: 0.9.5
     Path: /usr/local/bin/iflow

  4. CodeBuddy
     Version: 1.0.2
     Path: /usr/local/bin/codebuddy

Select deployment target:
  0. Deploy to all detected platforms
  1-4. Deploy to specific platform
  s. Skip deployment (generate configs only)
  q. Quit

Enter your choice: 1

🚀 Deploying DNASPEC skills to 1 platform(s)...

📦 Deploying to Claude...
⚙️  Generating configuration files...
✅ Claude deployment completed

✅ Successfully deployed to 1/1 platforms

==================================================
🎉 DNASPEC Initialization Complete!
==================================================

✅ Successfully configured 1 platform(s):
  • Claude

📖 Usage Examples:
You can now use DNASPEC skills in your configured AI CLI tools:

  Context Analysis:
    /speckit.dnaspec.context-analysis "Analyze this requirement"

  Context Optimization:
    /speckit.dnaspec.context-optimization "Optimize this prompt"

  System Architecture:
    /speckit.dnaspec.architect "Design a user authentication system"

  Cognitive Template:
    /speckit.dnaspec.cognitive-template "Apply verification template" template=verification

  Git Operations:
    /speckit.dnaspec.git-skill operation=status

  Temp Workspace:
    /speckit.dnaspec.temp-workspace operation=create

📁 Configuration saved to: /path/to/project/.dnaspec/
🔧 To reconfigure, run: dnaspec init
📋 To check status, run: dnaspec status

Happy coding with DNASPEC! 🚀
```

#### 场景2：选择多个平台

```bash
Select deployment target:
  0. Deploy to all detected platforms
  1-4. Deploy to specific platform
  s. Skip deployment (generate configs only)
  q. Quit

Enter your choice: s

Select platforms (comma-separated numbers, e.g., 1,3,5):
Enter numbers: 1,3,4

🚀 Deploying DNASPEC skills to 3 platform(s)...

📦 Deploying to Claude...
✅ Claude deployment completed

📦 Deploying to IFlow...
✅ IFlow deployment completed

📦 Deploying to CodeBuddy...
✅ CodeBuddy deployment completed

✅ Successfully deployed to 3/3 platforms
```

#### 场景3：未检测到任何AI CLI工具

```bash
$ dnaspec init

🚀 DNASPEC Project Initialization
==================================================

🔍 Scanning for AI CLI tools...

❌ No supported AI CLI tools detected.

Please install at least one of the following AI CLI tools:

🛠️  Recommended AI CLI Tools:
  • Claude CLI
    Install: https://claude.ai/cli
    Verify: claude --version

  • Gemini CLI
    Install: https://ai.google.dev/cli
    Verify: gemini --version

  • Qwen CLI
    Install: https://qwen.readthedocs.io/
    Verify: qwen --version

  • IFlow CLI
    Install: https://iflow.dev/docs/cli
    Verify: iflow --version

  • QoderCLI
    Install: https://qodercli.dev/
    Verify: qodercli --version

  • CodeBuddy
    Install: https://codebuddy.dev/
    Verify: codebuddy --version

  • GitHub Copilot CLI
    Install: https://github.com/cli/cli#installation
    Verify: gh copilot --version

After installing, run 'dnaspec init' again to continue setup.
```

## 初始化后生成的文件结构

初始化完成后，项目目录中会创建以下结构：

```
your-project/
├── .dnaspec/
│   ├── deployment.json          # 部署配置信息
│   ├── cli_extensions/          # CLI扩展文件
│   │   ├── claude/
│   │   ├── qwen/
│   │   └── iflow/
│   └── config.yaml              # 主配置文件
├── .iflow/
│   └── commands/                # IFlow命令文件
├── .qwen/
│   └── commands/                # Qwen命令文件
└── .codebuddy/
    └── commands/                # CodeBuddy命令文件
```

## 技能使用示例

### 在Claude CLI中使用

```bash
# 启动Claude CLI
claude

# 在Claude中使用DNASPEC技能
/speckit.dnaspec.context-analysis "分析这个用户需求文档的质量和完整性"
/speckit.dnaspec.architect "设计一个支持用户注册、登录、产品浏览的电商系统"
/speckit.dnaspec.git-skill operation=status
/speckit.dnaspec.temp-workspace operation=create
```

### 在Qwen CLI中使用

```bash
# 启动Qwen CLI
qwen

# 在Qwen中使用DNASPEC技能
/speckit.dnaspec.context-optimization "优化这个提示词，提升清晰度和完整性"
/speckit.dnaspec.cognitive-template "应用验证检查模板" template=verification
/speckit.dnaspec.git-skill operation=commit message="feat: 添加新功能"
```

### 在IFlow CLI中使用

```bash
# 启动IFlow CLI
iflow

# 在IFlow中使用DNASPEC技能
/speckit.dnaspec.context-analysis "Analyze this system requirement"
/speckit.dnaspec.architect "Design microservices architecture for e-commerce"
/speckit.dnaspec.constraint-generator "Generate constraints for payment system"
```

### 在CodeBuddy中使用

```bash
# 启动CodeBuddy
codebuddy

# 在CodeBuddy中使用DNASPEC技能
/speckit.dnaspec.context-analysis "Review this code documentation"
/speckit.dnaspec.modulizer "Break down this monolithic code into modules"
/speckit.dnaspec.dapi-checker "Check API design consistency"
```

## 高级功能

### 1. 重新配置

如果需要重新配置或添加新的AI CLI工具：

```bash
# 在项目目录中重新运行初始化
dnaspec init
```

### 2. 检查状态

查看当前部署状态：

```bash
dnaspec status
```

### 3. 验证集成

验证所有平台集成是否正常：

```bash
dnaspec validate
```

### 4. 查看可用技能

列出所有可用的DNASPEC技能：

```bash
dnaspec list
```

## 故障排除

### 常见问题

1. **未检测到AI CLI工具**
   - 确保AI CLI工具已正确安装
   - 检查工具是否在系统PATH中
   - 运行 `--version` 命令验证安装

2. **部署失败**
   - 检查项目目录的写权限
   - 确保没有其他进程占用配置文件
   - 重新运行 `dnaspec init`

3. **技能命令不工作**
   - 检查AI CLI工具版本兼容性
   - 重新运行 `dnaspec validate` 检查集成
   - 查看AI CLI工具的错误日志

### 调试模式

启用详细日志输出：

```bash
# 设置环境变量启用调试
export DNASPEC_DEBUG=1
dnaspec init
```

## 支持的平台

| 平台 | 支持状态 | 配置目录 | 命令前缀 |
|------|----------|----------|----------|
| Claude CLI | ✅ 完全支持 | ~/.config/claude/skills | `/` |
| Gemini CLI | ✅ 完全支持 | ~/.gemini/commands | `/` |
| Qwen CLI | ✅ 完全支持 | ~/.qwen/commands | `/` |
| IFlow CLI | ✅ 完全支持 | ~/.iflow/commands | `/` |
| QoderCLI | ✅ 完全支持 | ~/.qodercli/commands | `/` |
| CodeBuddy | ✅ 完全支持 | ~/.codebuddy/commands | `/` |
| GitHub Copilot | ✅ 完全支持 | ~/.config/gh-copilot | `/` |
| Cursor | ✅ 完全支持 | ~/.cursor | `/` |

## 更新和卸载

### 更新DNASPEC

```bash
# 更新到最新版本
npm update -g dnaspec

# 重新配置项目
dnaspec init
```

### 清理配置

如果需要完全清理DNASPEC配置：

```bash
# 删除项目配置
rm -rf .dnaspec
rm -rf .iflow
rm -rf .qwen
rm -rf .codebuddy
rm -rf .qodercli

# 或使用清理命令
dnaspec clean
```

---

📚 **更多信息**: [GitHub项目地址](https://github.com/ptreezh/dnaSpec)
🐛 **问题反馈**: [Issues页面](https://github.com/ptreezh/dnaSpec/issues)
💬 **讨论交流**: [Discussions页面](https://github.com/ptreezh/dnaSpec/discussions)