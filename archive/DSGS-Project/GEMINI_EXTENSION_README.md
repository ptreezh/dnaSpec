# DNASPEC Gemini CLI Extensions

DNASPEC (Dynamic Specification Growth System) 智能架构师系统的Gemini CLI扩展，为Gemini CLI提供专业技能支持。

## 功能特性

- **智能技能匹配**: 基于多维度算法自动匹配最合适的技能
- **自动技能调用**: 无需手动指定，系统自动调用相应技能
- **专业架构建议**: 提供专业的系统架构和设计建议
- **多技能协同**: 支持多个技能协同工作

## 支持的技能

1. **dnaspec-agent-creator** - 智能体创建器
   - 创建和配置智能体
   - 定义智能体角色和行为
   - 生成智能体规范文档

2. **dnaspec-task-decomposer** - 任务分解器
   - 复杂任务分解和原子化
   - 任务依赖分析
   - 任务计划生成

3. **dnaspec-dapi-checker** - 分布式接口检查器
   - 接口一致性和完整性检查
   - API文档验证
   - 参数匹配检查

4. **dnaspec-modulizer** - 模块化器
   - 模块成熟度检查
   - 组件封装
   - 自底向上分析

5. **dnaspec-architect** - 架构师
   - 系统架构设计
   - 技术栈选择
   - 模块划分

## 安装使用

### 安装扩展

```bash
python install_gemini_extension.py install
```

### 使用示例

在Gemini CLI中直接输入自然语言请求：

```
创建一个项目管理智能体
分解复杂的软件开发任务
检查API接口一致性
对系统进行模块化重构
设计系统架构
生成智能体角色定义
验证接口参数不一致问题
执行模块成熟度检查
```

## 技术架构

### 智能匹配算法

采用多维度匹配算法：
- **精确匹配** (权重0.5) - 关键词和技能名称匹配
- **语义匹配** (权重0.3) - 描述语义相似度分析
- **上下文匹配** (权重0.2) - 请求类型和领域上下文分析

### Hook机制

通过Hook拦截用户请求，智能匹配并执行相应技能，无缝集成到Gemini CLI中。

## 开发说明

### 目录结构

```
dnaspec-gemini-extensions/
├── gemini_skills_core.py         # 技能核心框架
├── gemini_intelligent_matcher.py # 智能匹配器
├── gemini_hook_handler.py        # Hook处理器
├── dnaspec_gemini_cli.py            # 主入口
├── install_gemini_extension.py   # 安装脚本
├── GEMINI_EXTENSION_CONFIG.json  # 配置文件
├── skills/                       # 技能定义文件
└── src/                          # 技能实现代码
```

### 扩展开发

1. 创建新的技能类继承DNASPECSkill基类
2. 在SkillManager中注册技能信息
3. 更新智能匹配器的关键词映射
4. 在Hook处理器中添加技能执行逻辑

## 许可证

MIT License