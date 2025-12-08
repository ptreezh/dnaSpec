# DNASPEC Gemini CLI Extensions 快速开始指南

## 简介

DNASPEC Gemini CLI Extensions 是一个为Gemini CLI设计的专业技能扩展系统，它提供了多种AI技能来帮助您进行系统架构设计、任务分解、智能体创建等工作。

## 安装

### 方法1: 自动安装
```bash
# 进入项目目录
cd D:\DAIP\dnaSpec\DNASPEC-Project

# 集成到Gemini CLI
python gemini_integration.py install
```

### 方法2: 手动安装
1. 复制扩展文件到Gemini CLI的extensions目录
2. 更新Gemini CLI配置文件
3. 重启Gemini CLI

## 快速使用

### 交互式模式
```bash
# 启动交互式界面
python gemini_interactive_ui.py

# 在交互界面中输入自然语言请求
DNASPEC> 设计微服务系统架构
DNASPEC> 创建项目管理智能体
DNASPEC> 检查API接口一致性
```

### 直接测试
```bash
# 运行演示测试
python dnaspec_gemini_cli.py --test

# 运行交互演示
python gemini_interactive_ui.py --demo
```

## 支持的技能

### 1. dnaspec-agent-creator (智能体创建器)
**功能**: 创建和配置智能体，定义智能体角色和行为

**使用示例**:
- "创建一个项目管理智能体"
- "生成数据处理智能体的角色定义"
- "配置用户认证智能体"

### 2. dnaspec-task-decomposer (任务分解器)
**功能**: 复杂任务分解和原子化，任务依赖分析

**使用示例**:
- "分解用户注册功能的开发任务"
- "分析订单处理流程的任务依赖"
- "细化系统架构设计任务"

### 3. dnaspec-dapi-checker (分布式接口检查器)
**功能**: 接口一致性和完整性检查，API文档验证

**使用示例**:
- "检查用户服务API接口一致性"
- "验证支付接口的参数匹配"
- "检查微服务接口文档完整性"

### 4. dnaspec-modulizer (模块化器)
**功能**: 模块成熟度检查，组件封装，自底向上分析

**使用示例**:
- "对订单处理模块进行成熟度评估"
- "执行用户管理模块的封装操作"
- "分析系统模块化程度"

### 5. dnaspec-architect (架构师)
**功能**: 系统架构设计，技术栈选择，模块划分

**使用示例**:
- "设计微服务系统架构"
- "为电商平台选择技术栈"
- "规划大数据处理系统架构"

### 6. dnaspec-constraint-generator (约束生成器)
**功能**: 系统约束和规范生成，API约束定义

**使用示例**:
- "生成API接口约束规范"
- "定义数据存储约束"
- "创建系统安全规范"

### 7. dnaspec-system-architect (系统架构师)
**功能**: 具体系统架构设计，详细技术方案

**使用示例**:
- "设计用户管理系统架构"
- "规划订单处理系统"
- "构建实时通信系统"

## 交互式界面命令

在交互式界面中，您可以使用以下命令：

- `help` 或 `h` - 显示帮助信息
- `skills` 或 `s` - 查看可用技能列表
- `stats` - 查看执行统计信息
- `debug` - 切换调试模式
- `clear` 或 `cls` - 清屏
- `quit` 或 `q` - 退出程序

## 调试和监控

### 启用调试模式
```bash
# 在交互式界面中
DNASPEC> debug
```

### 查看执行统计
```bash
# 在交互式界面中
DNASPEC> stats
```

## 配置文件

### GEMINI_EXTENSION_CONFIG.json
主要配置文件，包含扩展的基本信息和集成设置。

### 技能配置
每个技能的关键词和描述在`gemini_skills_core.py`中定义。

## 故障排除

### 常见问题

1. **技能无法匹配**
   - 检查输入是否包含足够的关键词
   - 尝试更具体的描述
   - 启用调试模式查看匹配过程

2. **技能执行失败**
   - 检查技能模块是否正确安装
   - 查看错误日志获取详细信息
   - 确认依赖项是否完整

3. **集成失败**
   - 检查Gemini CLI配置文件路径
   - 确认扩展文件是否正确复制
   - 重启Gemini CLI后重试

### 联系支持
如果遇到问题，请查看项目文档或提交Issue。

## 最佳实践

### 1. 请求描述建议
- 使用具体和明确的描述
- 包含相关的关键词
- 避免过于宽泛的请求

### 2. 技能组合使用
- 可以连续使用多个技能
- 前一个技能的结果可以作为后一个技能的输入
- 合理规划技能使用顺序

### 3. 性能优化
- 定期清理执行历史
- 监控技能执行性能
- 及时更新技能关键词库

## 示例工作流

### 系统设计工作流
1. 使用`dnaspec-architect`设计整体架构
2. 使用`dnaspec-task-decomposer`分解开发任务
3. 使用`dnaspec-agent-creator`创建必要的智能体
4. 使用`dnaspec-dapi-checker`验证接口设计
5. 使用`dnaspec-modulizer`进行模块化评估

### 微服务开发工作流
1. 使用`dnaspec-system-architect`设计具体服务
2. 使用`dnaspec-task-decomposer`分解服务开发任务
3. 使用`dnaspec-constraint-generator`生成服务约束
4. 使用`dnaspec-dapi-checker`检查服务接口
5. 使用`dnaspec-modulizer`评估服务成熟度

## 贡献指南

欢迎贡献代码和建议！

1. Fork项目仓库
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 许可证

本项目采用MIT许可证。