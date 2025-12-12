# DNASPEC 精简命令参考

## 🎯 命令格式标准

**所有DNASPEC斜杠命令使用统一格式：`/dnaspec.*`**

### 基本语法
```bash
/dnaspec.<command> [arguments...]
```

---

## 🔍 上下文工程技能

### 上下文分析
```bash
/dnaspec.context-analysis "分析这个用户认证系统需求文档"

# 增强模式
/dnaspec.context-analysis "API设计文档" --mode enhanced
```

### 上下文优化
```bash
/dnaspec.context-optimization "帮我写代码" --goals clarity,completeness

# 多目标优化
/dnaspec.context-optimization "系统需求" --goals clarity,relevance
```

### 认知模板
```bash
# 思维链推理
/dnaspec.cognitive-template "如何提高性能" --template chain_of_thought

# 验证检查
/dnaspec.cognitive-template "审查设计方案" --template verification
```

---

## 🏗️ 系统设计技能

### 系统架构
```bash
/dnaspec.architect "电商平台，支持用户、商品、订单管理" --style microservices

# 带约束条件
/dnaspec.architect "实时数据处理系统" --constraints high_performance
```

### 任务分解
```bash
/dnaspec.task-decomposer "开发一个完整的电商平台"

# 带时间约束
/dnaspec.task-decomposer "AI辅助开发工具" --constraints 2_months
```

### 智能体创建
```bash
/dnaspec.agent-creator "代码审查助手" capabilities=analysis,coding

# 多技能智能体
/dnaspec.agent-creator "全栈开发助手" capabilities=frontend,backend
```

### 约束生成
```bash
/dnaspec.constraint-generator "金融交易系统" type=security

# 性能约束
/dnaspec.constraint-generator "实时数据处理" type=performance
```

### API检查
```bash
/dnaspec.dapi-checker "RESTful API设计文档"

# 验证一致性
/dnaspec.dapi-checker "微服务API接口" --check consistency
```

### 模块化
```bash
/dnaspec.modulizer "大型电商系统单体应用"

# 设计接口
/dnaspec.modulizer "用户管理系统" --design interfaces
```

---

## 🔧 开发辅助技能（精简格式）

### Git操作
```bash
# 查看状态
/dnaspec.git status

# 添加文件
/dnaspec.git add "src/auth.py"

# 提交
/dnaspec.git commit "feat: 添加用户认证模块"

# 推送
/dnaspec.git push

# 拉取
/dnaspec.git pull

# 创建分支
/dnaspec.git branch "user-authentication"

# 查看历史
/dnaspec.git log --limit 10
```

### 工作区管理
```bash
# 创建工作区
/dnaspec.workspace create

# 添加文件
/dnaspec.workspace add "auth.py" "代码内容"

# 列出文件
/dnaspec.workspace list

# 清理工作区
/dnaspec.workspace clean

# 移动文件到暂存区
/dnaspec.workspace stage "auth.py"

# 验证文件
/dnaspec.workspace verify "auth.py"

# 提升到工作区
/dnaspec.workspace promote "auth.py"
```

---

## 🛠️ 工具命令

### 使用示例
```bash
# 显示所有技能
/dnaspec.examples

# 显示特定技能示例
/dnaspec.examples context-analysis
/dnaspec.examples architect
```

### 系统状态
```bash
# 检查健康状态
/dnaspec.liveness

# 详细状态
/dnaspec.liveness --verbose
```

### 版本信息
```bash
# 显示版本
/dnaspec.version

# 详细信息
/dnaspec.version --detailed
```

---

## 💻 命令行工具

### 主命令
```bash
dnaspec init                    # 项目初始化
dnaspec deploy                   # 部署到AI CLI平台
dnaspec validate                 # 验证集成状态
dnaspec list                     # 显示可用技能
dnaspec status                   # 检查系统状态
dnaspec clean                    # 清理临时文件
dnaspec --version                # 显示版本
```

### 部署选项
```bash
dnaspec deploy --list            # 列出检测到的平台
dnaspec deploy --platform claude # 部署到特定平台
dnaspec deploy --force            # 强制重新部署
```

---

## 🎨 实际使用场景

### 场景1：需求分析
```bash
# 分析需求文档
/dnaspec.context-analysis "用户要求开发在线教育平台，支持视频课程、直播、作业提交"

# 优化需求描述
/dnaspec.context-optimization "做个网站" --goals clarity,completeness

# 结构化分析
/dnaspec.cognitive-template "教育平台需求" --template chain_of_thought
```

### 场景2：系统设计
```bash
# 设计架构
/dnaspec.architect "在线教育平台架构" --style microservices

# 分解任务
/dnaspec.task-decomposer "教育平台开发" --constraints 3_months,5_devs

# 生成约束
/dnaspec.constraint-generator "教育平台" type=performance,security
```

### 场景3：AI辅助开发
```bash
# 创建工作区
/dnaspec.workspace create

# 添加AI生成的文件（保存在temp_workspace）
# [AI CLI生成用户认证代码]

# 移动到暂存区
/dnaspec.workspace stage "user_auth.py"

# 验证文件
/dnaspec.workspace verify "user_auth.py"

# 提升到工作区
/dnaspec.workspace promote "user_auth.py"

# 安全提交
/dnaspec.git commit "feat: 添加验证后的用户认证模块"
```

### 场景4：代码审查
```bash
# 应用验证模板
/dnaspec.cognitive-template "审查支付模块" --template verification

# 检查API设计
/dnaspec.dapi-checker "支付API设计文档"

# 模块化改进
/dnaspec.modulizer "大型单体应用代码库"
```

### 场景5：项目管理
```bash
# 查看项目状态
/dnaspec.liveness

# Git状态检查
/dnaspec.git status

# 提交所有已验证的工作
/dnaspec.git commit "完成用户认证模块开发"
```

---

## ⚙️ 参数选项

### 认知模板类型
- `chain_of_thought` - 思维链推理
- `few_shot` - 少示例学习
- `verification` - 验证检查
- `role_playing` - 角色扮演

### 架构风格
- `microservices` - 微服务架构
- `monolithic` - 单体架构
- `event_driven` - 事件驱动架构
- `serverless` - 无服务器架构

### 约束类型
- `performance` - 性能约束
- `security` - 安全约束
- `reliability` - 可靠性约束
- `scalability` - 可扩展性约束

### 优化目标
- `clarity` - 清晰度
- `completeness` - 完整性
- `relevance` - 相关性
- `consistency` - 一致性

---

## 💡 使用技巧

### 快速开始
```bash
# 1. 检查系统状态
/dnaspec.liveness

# 2. 查看可用命令
/dnaspec.examples

# 3. 开始第一个任务
/dnaspec.context-analysis "你的需求描述"
```

### 组合使用
```bash
# 先分析后优化
/dnaspec.context-analysis "原始需求"
/dnaspec.context-optimization "改进后的需求" --goals clarity,completeness

# 先设计后验证
/dnaspec.architect "系统架构"
/dnaspec.cognitive-template "验证架构" --template verification
```

### 安全工作流
```bash
# 创建工作区
/dnaspec.workspace create

# AI生成文件后
/dnaspec.workspace stage "generated_file.py"
/dnaspec.workspace verify "generated_file.py"
/dnaspec.workspace promote "generated_file.py"

# 安全提交
/dnaspec.git commit "Add verified AI-generated content"
```

---

## 🔧 命令别名对比

| 功能 | 复杂格式（已废弃） | 精简格式（推荐） |
|------|------------------|----------------|
| Git状态检查 | `/dnaspec.git-operations operation=status` | `/dnaspec.git status` |
| Git提交 | `/dnaspec.git-operations operation=commit message="..."` | `/dnaspec.git commit "..."` |
| 工作区创建 | `/dnaspec.temp-workspace operation=create` | `/dnaspec.workspace create` |
| 添加文件 | `/dnaspec.temp-workspace operation=add-file file_path=...` | `/dnaspec.workspace add "..."` |

---

🎯 **记住**：使用精简的命令格式，享受更直观的开发体验！

📚 **更多信息**：
- [安全工作流指南](./DNASPEC_SECURE_WORKFLOW_GUIDE.md)
- [统一命令使用指南](./DNASPEC_UNIFIED_COMMANDS.md)