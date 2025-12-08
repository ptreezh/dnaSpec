# DNASPEC Skills 集成部署包

## 项目概述
DNASPEC (Dynamic Specification Growth System) Skills 是一套智能架构师技能系统，包含7个核心技能：

- **dnaspec-agent-creator**: 智能体创建器 - 创建和配置智能体
- **dnaspec-architect**: 智能架构师 - 主协调技能
- **dnaspec-system-architect**: 系统架构师 - 系统架构设计
- **dnaspec-task-decomposer**: 任务分解器 - 任务分解和原子化
- **dnaspec-constraint-generator**: 约束生成器 - 生成系统约束
- **dnaspec-dapi-checker**: DAPI检查器 - 接口一致性检查
- **dnaspec-modulizer**: 模块化器 - 模块成熟化核验

## Claude Code 集成

### 安装步骤
1. 确保已安装 Claude Code CLI
2. 启用 Skills 功能 (Settings > Capabilities > Enable Skills)
3. 将 `claude_code_skills` 目录中的所有技能复制到 Claude 配置目录：
   - Windows: `~/.config/claude/skills/`
   - Unix/Linux/Mac: `~/.config/claude/skills/`

### 验证安装
运行以下命令验证安装：
```bash
python test_claude_integration.py
```

### 使用示例
在 Claude Code 中尝试以下请求：
- "创建一个智能体" - 自动调用 dnaspec-agent-creator
- "分解复杂任务" - 自动调用 dnaspec-task-decomposer  
- "生成系统约束" - 自动调用 dnaspec-constraint-generator
- "检查接口一致性" - 自动调用 dnaspec-dapi-checker
- "模块化重构" - 自动调用 dnaspec-modulizer

## Gemini CLI 集成

### 安装步骤
1. 确保已安装 Gemini CLI
2. 将 `gemini_extensions` 目录中的扩展安装到 Gemini CLI
3. 配置 MCP 服务器（如需要）

### 配置文件
- `extensions.json` - 扩展配置文件
- 每个扩展目录包含 `GEMINI.md` 上下文文件

## Qwen CLI 集成

### 安装步骤
1. 确保已安装 Qwen CLI
2. 将 `qwen_plugins` 目录中的插件安装到 Qwen CLI
3. 配置工具执行权限

### 配置文件
- `plugins.json` - 插件配置文件
- 每个插件目录包含 `plugin.json` 配置和 `README.md` 说明

## 关键特性

### 智能发现机制
- 基于关键词匹配的意图识别
- 多维度置信度计算
- 自动技能选择和调用

### 高级功能
- **模块智能化**: 支持模块自主智能和具身认知
- **接口一致性**: 检查接口、参数、定义的一致性
- **隔离测试**: 支持模块化隔离测试
- **系统重构**: 支持自动模块重构

### 性能优化
- 低延迟技能调用
- 高效关键词匹配算法
- 优化的置信度计算

## 故障排除

### Claude Code
- 确保 Skills 功能已启用
- 检查技能目录权限
- 验证 SKILL.md 文件格式

### Gemini CLI
- 确保 MCP 服务器正常运行
- 检查扩展配置文件
- 验证 Playbook 触发规则

### Qwen CLI
- 确保插件权限正确
- 检查工具执行配置
- 验证 API 连接

## 更新日志
- v1.0.0: 初始版本，包含7个核心技能
- 支持 Claude Code、Gemini CLI、Qwen CLI 三平台集成
- 实现智能发现和自动调用机制

## 许可证
MIT License