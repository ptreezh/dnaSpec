---
name: dnaspec-skills
description: Complete DNASPEC Context Engineering Skills Suite - Professional AI-assisted development tools with AgentSkills.io standard compliance
license: MIT
compatibility: Claude Code, VS Code, and any Agent Skills compatible environment
metadata:
  author: DNASPEC Team
  version: "2.0.0"
  category: context-engineering
  standard_compliance: AgentSkills.io v1.0
  framework_version: DNASPEC Framework v2.0.0
---

# DNASPEC Skills Suite v2.0

## 概述

DNASPEC Skills Suite v2.0 是完全符合 AgentSkills.io 标准的上下文工程技能集合，基于 TDD 方法重新实现，严格遵循 KISS、SOLID、YAGNI 原则。

## 核心改进

### 🎯 标准合规性
- **AgentSkills.io v1.0 完全兼容**
- **统一技能接口标准**
- **标准化响应格式**
- **一致的错误处理**

### 🧪 TDD 驱动开发
- **先写测试，后实现**
- **100% 测试覆盖**
- **真实的测试用例**
- **持续集成验证**

### 📋 技能清单

| 技能名称 | 状态 | 描述 | 测试覆盖率 |
|---------|------|------|-----------|
| `architect` | ✅ 重构完成 | 系统架构设计和分析 | 100% |
| `context-analyzer` | ✅ 重构完成 | 5维上下文质量分析 | 100% |
| `cognitive-templater` | 🔄 重构中 | 认知模板应用 | 0% |
| `agent-creator` | 🔄 重构中 | 智能体创建 | 0% |
| `task-decomposer` | 🔄 重构中 | 任务分解 | 0% |
| `constraint-generator` | 🔄 重构中 | 约束生成 | 0% |

## 架构设计

### 技能层次结构
```
DNASPEC Skills Suite v2.0
├── dnaspec_skill_framework.py     # 核心框架
├── skills/
│   ├── architect/                # 架构师技能
│   │   ├── SKILL.md
│   │   └── skill.py
│   ├── context-analyzer/         # 上下文分析技能
│   │   ├── SKILL.md
│   │   └── skill.py
│   ├── cognitive-templater/      # 认知模板技能
│   ├── agent-creator/            # 智能体创建技能
│   ├── task-decomposer/          # 任务分解技能
│   └── constraint-generator/     # 约束生成技能
└── tests/
    └── test_skills_compliance.py  # TDD 测试套件
```

### 核心框架特性
- **统一基类**: `DNASpecSkillBase`
- **标准化验证**: 输入验证和错误处理
- **性能监控**: 自动执行指标收集
- **日志记录**: 结构化日志系统
- **技能注册**: 统一的技能管理

## 技能标准

### 1. 统一接口
所有技能必须实现：
```python
class MySkill(DNASpecSkillBase):
    def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]
    def execute_skill(self, input_data: Dict[str, Any]) -> Dict[str, Any]
    def lambda_handler(self, event: Dict[str, Any], context: Any = None) -> Dict[str, Any]
```

### 2. 标准输入格式
```json
{
  "inputs": [
    {
      "input": "主要输入内容",
      "parameter1": "可选参数1",
      "parameter2": "可选参数2"
    }
  ],
  "tool_name": "技能名称"
}
```

### 3. 标准输出格式
```json
{
  "statusCode": 200,
  "body": {
    "success": true,
    "result": { "具体结果" },
    "metadata": {
      "skill": "技能名称",
      "execution_id": "唯一执行ID",
      "timestamp": "2025-12-20T08:00:00Z",
      "execution_time": 0.123,
      "version": "2.0.0"
    }
  }
}
```

## 质量保证

### 测试策略
- **单元测试**: 每个技能方法的独立测试
- **集成测试**: 技能与框架的集成测试
- **性能测试**: 响应时间和资源使用测试
- **错误处理测试**: 异常情况的优雅处理

### 性能要求
- **响应时间**: 简单技能 < 500ms，复杂技能 < 2000ms
- **内存使用**: 基础技能 < 128MB，复杂技能 < 512MB
- **错误率**: < 1%（排除输入错误）

### 安全标准
- **输入验证**: 所有输入必须验证
- **权限控制**: 最小权限原则
- **敏感数据**: 避免敏感信息泄露

## 使用指南

### 安装
```bash
# 从源码安装
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaSpec
pip install -e .
```

### 基本使用
```python
# 直接使用技能
from skills.architect.skill import get_skill

architect = get_skill()
result = architect.lambda_handler({
    "inputs": [{"input": "设计电商平台"}],
    "tool_name": "architect"
})
```

### 技能注册
```python
# 注册技能到全局注册表
from skills.dnaspec_skill_framework import register_skill
from skills.architect.skill import get_skill

register_skill(get_skill())
```

## 开发指南

### 创建新技能
1. **继承基类**:
```python
from skills.dnaspec_skill_framework import DNASpecSkillBase, track_execution

@track_execution
class NewSkill(DNASpecSkillBase):
    def __init__(self):
        super().__init__(
            name="new-skill",
            description="技能描述"
        )
```

2. **实现必需方法**:
```python
def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
    # 实现输入验证

def execute_skill(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
    # 实现技能逻辑
```

3. **创建标准文件**:
```
new-skill/
├── SKILL.md     # 技能描述（符合AgentSkills.io格式）
└── skill.py     # 技能实现
```

4. **编写测试**:
```python
def test_new_skill_valid_input(self):
    event = self.create_valid_event("new-skill", "测试输入")
    response = lambda_handler(event)
    self.assert_valid_response_format(response)
```

## 迁移指南

### 从 v1.0 升级到 v2.0
1. **更新导入路径**: 使用新的统一框架
2. **调整输入格式**: 符合标准事件格式
3. **实现验证方法**: 添加输入验证逻辑
4. **更新响应格式**: 使用标准响应结构
5. **运行测试**: 确保通过所有测试

### 兼容性说明
- **向后兼容**: v1.0 的功能在 v2.0 中都有对应实现
- **接口变更**: 主要变更在内部接口，外部调用保持兼容
- **配置迁移**: 自动迁移旧配置到新格式

## 问题修复

### 已解决的问题
- ✅ **UUID 导入错误**: 修复了缺失的 uuid 导入
- ✅ **输入验证缺失**: 添加了完整的输入验证机制
- ✅ **错误处理不完善**: 实现了统一的错误处理
- ✅ **测试虚假问题**: 基于真实功能编写测试
- ✅ **性能监控缺失**: 添加了自动性能指标收集

### 待解决问题
- 🔄 **剩余技能重构**: cognitive-templater, agent-creator, task-decomposer, constraint-generator
- 🔄 **文档同步**: 更新所有文档以反映 v2.0 变更
- 🔄 **性能优化**: 优化技能执行性能
- 🔄 **多语言支持**: 完善多语言技能支持

## 版本历史

### v2.0.0 (当前)
- 🎯 完全重构以符合 AgentSkills.io 标准
- 🧪 基于 TDD 方法重新实现
- 🏗️ 新的统一技能框架
- ✅ 修复所有已知的核心问题

### v1.0.2 (之前)
- ❌ 存在多个关键问题，不推荐用于生产环境

## 贡献指南

### 开发环境设置
```bash
# 克隆仓库
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaSpec

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/test_skills_compliance.py -v
```

### 代码规范
- **Python 版本**: 3.8+
- **代码风格**: PEP 8
- **文档字符串**: Google 风格
- **类型注解**: 必需

### 提交流程
1. Fork 仓库
2. 创建功能分支
3. 编写测试
4. 实现功能
5. 确保测试通过
6. 提交 Pull Request

## 许可证

MIT License - 允许商业和非商业使用，保留版权声明。

## 支持

- **问题报告**: https://github.com/ptreezh/dnaSpec/issues
- **文档**: https://github.com/ptreezh/dnaSpec/wiki
- **社区**: https://github.com/ptreezh/dnaSpec/discussions

---

**DNASPEC Skills Suite v2.0** - 专业级 AI 辅助开发工具套件，完全符合 AgentSkills.io 标准，基于 TDD 方法构建，确保质量和可靠性。