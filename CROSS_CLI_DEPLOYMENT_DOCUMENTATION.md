# DNASPEC跨CLI技能部署文档

## 1. 概述

DNASPEC技能系统支持跨多种CLI工具部署，包括Claude CLI、Qwen CLI、Gemini CLI等。本文档详细说明了如何将DNASPEC技能部署到不同的CLI工具中，并提供了相应的适配器和独立执行函数。

## 2. 架构设计

### 2.1 核心组件

1. **BaseSkill类** (`src/dna_spec_kit_integration/core/skill_base.py`)
   - 提供标准化的技能接口
   - 支持渐进式信息披露（BASIC/STANDARD/DETAILED）
   - 统一的输入验证和错误处理机制

2. **重构后的技能实现** (`src/dna_spec_kit_integration/skills/*_refactored.py`)
   - 继承BaseSkill类
   - 实现_execute_skill_logic和_format_output方法
   - 支持不同详细级别的输出格式

3. **独立执行函数** (`src/dna_spec_kit_integration/skills/*_independent.py`)
   - 为每个技能提供独立的执行函数
   - 支持命令行接口和JSON输入输出
   - 可直接被CLI工具调用

4. **CLI适配器** (`src/dna_spec_kit_integration/core/*_cli_adapter.py`)
   - 为不同CLI工具提供专门的适配器
   - 生成符合CLI规范的配置文件
   - 管理技能的部署和验证

### 2.2 接口规范

#### 标准化输入参数
```json
{
  "input": "主要输入内容",
  "detail_level": "basic|standard|detailed",
  "options": {},  // 可选配置参数
  "context": {}   // 上下文信息
}
```

#### 标准化输出格式
```json
{
  "status": "success|error",
  "data": {},  // 技能执行结果
  "metadata": {
    "skill_name": "技能名称",
    "detail_level": "standard"
  }
}
```

## 3. 部署流程

### 3.1 Qwen CLI部署

#### 自动部署
使用Qwen CLI适配器自动部署所有技能：

```bash
python src/dna_spec_kit_integration/core/qwen_cli_adapter.py --action deploy-all
```

#### 验证部署
验证技能是否成功部署：

```bash
python src/dna_spec_kit_integration/core/qwen_cli_adapter.py --action verify
```

#### 手动部署单个技能
部署特定技能：

```bash
python src/dna_spec_kit_integration/core/qwen_cli_adapter.py --action deploy --skill context-analysis --description "上下文分析技能"
```

### 3.2 支持的技能

1. **context-analysis** - 上下文分析技能
   - 分析上下文质量的五个维度：清晰度、相关性、完整性、一致性和效率
   - 提供改进建议和问题识别

2. **context-optimization** - 上下文优化技能
   - 根据特定目标优化上下文内容
   - 提高上下文的质量和有效性

3. **cognitive-template** - 认知模板技能
   - 应用认知模板如链式思维、验证、少样本学习等
   - 结构化思考和问题解决

4. **system-architect** - 系统架构师技能
   - 复杂项目的系统架构设计
   - 技术栈选择、模块划分和接口定义

5. **simple-architect** - 简易架构师技能
   - 通用应用程序的简单架构设计
   - 快速技术选型和部署策略

## 4. 独立执行函数

每个技能都提供了独立的执行函数，可以直接调用：

### 4.1 命令行调用

```bash
# 上下文分析技能
python src/dna_spec_kit_integration/skills/context_analysis_independent.py "请分析这个需求文档的质量" standard

# 系统架构师技能
python src/dna_spec_kit_integration/skills/system_architect_independent.py "设计一个电商平台" detailed

# 简易架构师技能
python src/dna_spec_kit_integration/skills/simple_architect_independent.py "创建一个博客网站" basic
```

### 4.2 Python函数调用

```python
from src.dna_spec_kit_integration.skills.context_analysis_independent import execute_context_analysis

args = {
    "input": "请分析这个需求文档的质量",
    "detail_level": "standard",
    "options": {},
    "context": {}
}

result = execute_context_analysis(args)
print(result)
```

## 5. CLI适配器

### 5.1 Qwen CLI适配器

Qwen CLI适配器(`src/dna_spec_kit_integration/core/qwen_cli_adapter.py`)提供了完整的部署和管理功能：

1. **generate_qwen_plugin_manifest** - 生成Qwen插件清单
2. **deploy_skill_to_qwen** - 部署单个技能到Qwen CLI
3. **deploy_all_skills** - 批量部署所有技能
4. **verify_deployment** - 验证部署状态
5. **remove_skill_from_qwen** - 从Qwen CLI移除技能

### 5.2 其他CLI适配器

可以根据需要为其他CLI工具创建类似的适配器：
- Claude CLI适配器
- Gemini CLI适配器
- Copilot CLI适配器

## 6. 渐进式信息披露

所有技能都支持三种详细级别：

1. **Basic** - 基础级别，只返回核心信息
2. **Standard** - 标准级别，返回标准信息集
3. **Detailed** - 详细级别，返回完整信息

## 7. 测试和验证

### 7.1 单元测试
每个技能都有相应的单元测试，确保功能正确性。

### 7.2 集成测试
验证技能在不同CLI工具中的集成和执行。

### 7.3 端到端测试
测试完整的技能调用流程，从CLI命令到技能执行结果。

## 8. 故障排除

### 8.1 部署失败
- 检查CLI工具是否正确安装
- 验证插件目录权限
- 确认技能文件是否存在

### 8.2 技能执行错误
- 检查输入参数格式
- 验证技能依赖是否满足
- 查看错误日志获取详细信息

### 8.3 性能问题
- 监控技能执行时间
- 优化技能实现逻辑
- 考虑缓存机制

## 9. 最佳实践

1. **版本管理** - 确保技能和CLI工具版本兼容
2. **配置管理** - 使用配置文件管理不同环境的设置
3. **日志记录** - 实现详细的日志记录以便调试
4. **安全性** - 验证输入参数，防止恶意代码注入
5. **性能优化** - 优化技能执行逻辑，减少响应时间

## 10. 扩展支持

要为新的CLI工具添加支持：
1. 创建对应的CLI适配器
2. 实现该CLI工具的插件格式生成
3. 验证技能在新CLI工具中的执行
4. 更新文档和测试用例