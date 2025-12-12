# DNASPEC 统一斜杠命令使用指南

## 🎯 命令格式标准

**所有DNASPEC斜杠命令使用统一格式：`/dnaspec.*`**

### 基本语法
```bash
/dnaspec.<skill-name> [arguments] [options]
```

## 📋 完整命令列表

### 🔍 上下文分析
```bash
# 分析上下文质量
/dnaspec.context-analysis "设计一个用户认证系统，支持注册、登录、密码重置功能"

# 检查特定维度的质量
/dnaspec.context-analysis "API接口设计文档" --mode enhanced
```

### ⚡ 上下文优化
```bash
# 优化清晰度和完整性
/dnaspec.context-optimization "帮我写代码" --goals clarity,completeness

# 多目标优化
/dnaspec.context-optimization "系统需求文档" --goals clarity,relevance,consistency
```

### 🧠 认知模板
```bash
# 应用思维链模板
/dnaspec.cognitive-template "如何提高系统性能？" --template chain_of_thought

# 应用验证检查模板
/dnaspec.cognitive-template "审查这个架构设计" --template verification

# 应用少示例学习模板
/dnaspec.cognitive-template "实现支付功能" --template few_shot
```

### 🏗️ 系统架构
```bash
# 设计微服务架构
/dnaspec.architect "电商平台，支持用户管理、商品管理、订单处理" --style microservices

# 带约束条件的架构设计
/dnaspec.architect "实时数据处理系统" --constraints high_performance,scalable
```

### 📋 任务分解
```bash
# 分解复杂任务
/dnaspec.task-decomposer "开发一个完整的电商平台"

# 带特定约束的分解
/dnaspec.task-decomposer "AI辅助开发工具" --constraints 2_months,3_devs
```

### 🤖 智能体创建
```bash
# 创建特定能力的智能体
/dnaspec.agent-creator "代码审查助手" capabilities=analysis,coding,security

# 创建多技能智能体
/dnaspec.agent-creator "全栈开发助手" capabilities=frontend,backend,devops,testing
```

### 🔧 Git操作
```bash
# 查看Git状态
/dnaspec.git-operations operation=status

# 安全提交
/dnaspec.git-operations operation=commit message="feat: 添加用户认证模块"

# 创建功能分支
/dnaspec.git-operations operation=branch name=user-authentication

# 查看提交历史
/dnaspec.git-operations operation=log limit=10
```

### 📁 临时工作区
```bash
# 创建临时工作区
/dnaspec.temp-workspace operation=create

# 添加AI生成的文件
/dnaspec.temp-workspace operation=add-file file_path=auth.py content="import hashlib..."

# 列出临时文件
/dnaspec.temp-workspace operation=list-files

# 清理临时工作区
/dnaspec.temp-workspace operation=clean
```

### ⚖️ 约束生成
```bash
# 生成系统约束
/dnaspec.constraint-generator "金融交易系统" type=security

# 生成性能约束
/dnaspec.constraint-generator "实时数据处理" type=performance

# 生成可用性约束
/dnaspec.constraint-generator "电商网站" type=reliability
```

### 🔌 API检查
```bash
# 检查API设计
/dnaspec.dapi-checker "RESTful API设计文档"

# 验证API一致性
/dnaspec.dapi-checker "微服务API接口规范" --check consistency
```

### 🧩 模块化
```bash
# 模块化单体应用
/dnaspec.modulizer "大型电商系统单体应用"

# 设计模块接口
/dnaspec.modulizer "用户管理系统" --design interfaces
```

### 📖 使用示例
```bash
# 显示所有可用技能
/dnaspec.examples

# 显示特定技能示例
/dnaspec.examples context-analysis
/dnaspec.examples architect
```

### 💡 系统状态
```bash
# 检查系统健康状态
/dnaspec.liveness

# 显示详细状态信息
/dnaspec.liveness --verbose
```

### ℹ️ 版本信息
```bash
# 显示版本信息
/dnaspec.version

# 显示详细配置信息
/dnaspec.version --detailed
```

## 🎨 实际使用场景

### 场景1：需求分析
```bash
# 分析需求文档质量
/dnaspec.context-analysis "用户要求开发一个在线教育平台，需要支持视频课程、直播、作业提交功能"

# 优化需求描述
/dnaspec.context-optimization "做个网站" --goals clarity,completeness

# 应用认知模板结构化分析
/dnaspec.cognitive-template "教育平台需求分析" --template chain_of_thought
```

### 场景2：系统设计
```bash
# 设计系统架构
/dnaspec.architect "在线教育平台架构设计" --style microservices

# 分解开发任务
/dnaspec.task-decomposer "教育平台开发项目" --constraints 3_months,5_devs

# 生成系统约束
/dnaspec.constraint-generator "教育平台" type=performance,security
```

### 场景3：AI辅助开发
```bash
# 创建临时工作区
/dnaspec.temp-workspace operation=create

# 让AI生成代码（保存在temp_workspace）
# [在AI CLI中让AI生成用户认证代码]

# 验证并暂存文件
python .dnaspec/scripts/verify_and_stage.py .dnaspec/temp_workspace/ai_generated/user_auth.py

# 提升到工作区
python .dnaspec/scripts/promote_to_workspace.py .dnaspec/staging_area/verified/user_auth.py

# 安全提交
/dnaspec.git-operations operation=commit message="feat: 添加验证后的用户认证模块"
```

### 场景4：代码审查
```bash
# 应用验证模板审查代码
/dnaspec.cognitive-template "审查这个支付模块的代码实现" --template verification

# 检查API设计
/dnaspec.dapi-checker "支付API接口设计文档"

# 模块化改进建议
/dnaspec.modulizer "大型单体应用代码库"
```

## ⚙️ 高级选项

### 通用选项
- `--verbose` - 显示详细输出
- `--quiet` - 静默模式
- `--help` - 显示帮助信息

### 认知模板类型
- `chain_of_thought` - 思维链推理
- `few_shot` - 少示例学习
- `verification` - 验证检查
- `role_playing` - 角色扮演
- `understanding` - 深度理解

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
- `maintainability` - 可维护性约束

## 🔧 命令别名

为了方便使用，部分命令支持别名：

| 主命令 | 别名 | 说明 |
|--------|------|------|
| `/dnaspec.context-analysis` | `/dnaspec.analyze` | 上下文分析 |
| `/dnaspec.context-optimization` | `/dnaspec.optimize` | 上下文优化 |
| `/dnaspec.cognitive-template` | `/dnaspec.template` | 认知模板 |
| `/dnaspec.architect` | `/dnaspec.design` | 系统架构 |
| `/dnaspec.git-operations` | `/dnaspec.git` | Git操作 |
| `/dnaspec.temp-workspace` | `/dnaspec.temp` | 临时工作区 |
| `/dnaspec.examples` | `/dnaspec.help` | 使用示例 |
| `/dnaspec.liveness` | `/dnaspec.status` | 系统状态 |

## 💡 使用技巧

### 1. 组合使用技能
```bash
# 先分析再优化
/dnaspec.context-analysis "原始需求"
/dnaspec.context-optimization "改进后的需求" --goals clarity,completeness

# 先设计后验证
/dnaspec.architect "系统架构"
/dnaspec.cognitive-template "验证架构设计" --template verification
```

### 2. 参数化使用
```bash
# 使用变量和参数
/dnaspec.architect "系统: ${SYSTEM_NAME}, 用户数: ${USER_COUNT}, 性能要求: ${PERF_REQUIREMENTS}"

# 多目标优化
/dnaspec.context-optimization "${DOCUMENT}" --goals ${GOALS_LIST}
```

### 3. 流水线操作
```bash
# 需求分析流水线
/dnaspec.context-analysis "${REQUIREMENT}" \
&& dnaspec.context-optimization "${REQUIREMENT}" --goals clarity,completeness \
&& dnaspec.architect "${OPTIMIZED_REQUIREMENT}"
```

## 🚀 快速开始

1. **检查系统状态**
   ```bash
   /dnaspec.liveness
   ```

2. **查看可用技能**
   ```bash
   /dnaspec.examples
   ```

3. **开始第一个任务**
   ```bash
   /dnaspec.context-analysis "你的第一个需求描述"
   ```

---

📚 **更多信息**：
- [安全工作流指南](./DNASPEC_SECURE_WORKFLOW_GUIDE.md)
- [项目地址](https://github.com/ptreezh/dnaSpec)
- [问题反馈](https://github.com/ptreezh/dnaSpec/issues)

🎯 **记住**：统一使用 `/dnaspec.*` 格式，享受一致的AI辅助开发体验！