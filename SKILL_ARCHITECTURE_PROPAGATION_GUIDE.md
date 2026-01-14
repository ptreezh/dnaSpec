# DNASPEC技能4层架构推广指南

## 📋 推广概述

基于task-decomposer（试点）和context-fundamentals（第13个技能）的成功经验，将4层渐进式架构推广到所有DNASPEC技能。

### 成功经验总结

**task-decomposer试点成果**：
- ✅ 4层提示词系统（00→01→02→03）
- ✅ 生产级脚本（validator、calculator、analyzer、executor）
- ✅ 智能自动选择层次
- ✅ 端到端测试通过率83%
- ✅ 总代码量：1271行Python + 29,222字符提示词

**context-fundamentals验证成果**：
- ✅ 验证了架构可复制性
- ✅ 核心功能100%可用
- ✅ 成功融合Agent-Skills优秀实践
- ✅ 建立了标准化模板

---

## 🎯 推广目标

### 需要重构的技能（11个）

**核心分解技能**（2个）：
1. ✅ task-decomposer（已完成）
2. ⏳ **modulizer** - 待重构

**质量保证技能**（2个）：
3. ⏳ **constraint-generator** - 待重构
4. ⏳ **dapi-checker** - 待重构

**优化技能**（3个）：
5. ⏳ **context-analysis** - 整合context-degradation
6. ⏳ **context-optimization** - 待重构
7. ⏳ **cognitive-template** - 待重构

**协调技能**（2个）：
8. ⏳ **architect** - 待重构
9. ⏳ **system-architect** - 待重构

**智能体技能**（1个）：
10. ⏳ **agent-creator** - 整合memory-systems

**基础设施技能**（2个）：
11. ⏳ **workspace** - 待重构
12. ⏳ **git** - 待重构

---

## 📐 标准架构模板

### 目录结构（每个技能必备）

```
dnaspec-{skill-name}/
├── SKILL.md                     # 技能描述（<500行）
├── prompts/                     # 4层渐进式提示词
│   ├── 00_context.md           # 核心概念层（<500字符）
│   ├── 01_basic.md             # 基础应用层（<1000字符）
│   ├── 02_intermediate.md      # 中级场景层（<2000字符）
│   └── 03_advanced.md          # 高级应用层（<3000字符）
├── scripts/                     # 生产级脚本
│   ├── validator.py            # 输入验证器
│   ├── calculator.py           # 指标计算器
│   ├── analyzer.py             # 深度分析器
│   ├── executor.py             # 智能协调器
│   └── __init__.py
├── config/                      # 配置文件
│   ├── parameters.yaml         # 技能参数
│   └── constraints.json        # 约束定义
├── references/                  # 参考资料（可选）
│   └── detailed_docs.md
└── tests/                       # 测试文件
    └── test_{skill}_e2e.py     # 端到端测试
```

### SKILL.md标准模板

```markdown
# DNASPEC {Skill Name} Skill

## When to Activate
（激活时机）

## Core Concepts
（核心概念）

## Practical Guidance
（实践指导）

## Examples
（使用示例）

## Guidelines
（质量检查清单）

## Integration
（与其他技能的协作）

## Key Achievements
（学习成果）

## References
（参考文档）
```

### 4层提示词标准模板

#### Level 00 - 核心概念层（<500字符）

```markdown
# {Skill Name} - 核心概念

## 你是谁
你是**{技能角色}**，负责{核心职责}。

## 核心原则

### 1. {核心概念1}
{简短定义}

### 2. {核心概念2}
{简短定义}

### 3. {核心概念3}
{简短定义}

---

## 快速指导
{3-5条关键要点}
```

#### Level 01 - 基础应用层（<1000字符）

```markdown
# {Skill Name} - 基础应用

## 在00_context基础上扩展
已理解：{列出核心概念}
本层目标：掌握{基础应用场景}

---

## 常见场景

### 场景1：{场景名称}
**上下文**：{需要什么信息}
**方法**：{如何处理}
**最佳实践**：{推荐做法}

### 场景2：{场景名称}
...

---

## 实践指导
{具体操作步骤}
```

#### Level 02 - 中级场景层（<2000字符）

```markdown
# {Skill Name} - 中级场景

## 复杂场景处理

### 场景1：{复杂场景1}
详细说明、工具使用、代码示例

### 场景2：{复杂场景2}
...

---

## 高级技术
{中级场景所需的技术}
```

#### Level 03 - 高级应用层（<3000字符）

```markdown
# {Skill Name} - 高级应用

## 大规模系统

### 架构模式
### 企业级实践
### 性能优化
...

---

## 前沿趋势
{最新发展和未来方向}
```

### 生产级脚本模板

#### validator.py模板

```python
"""
{Skill Name} Validator
负责验证{请求类型}
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class ValidationSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ValidationIssue:
    severity: ValidationSeverity
    category: str
    message: str
    suggestion: Optional[str] = None

@dataclass
class ValidationResult:
    is_valid: bool
    issues: List[ValidationIssue]

class {Skill}Validator:
    """验证器"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}

    def validate(self, request: str, context: Optional[Dict] = None) -> ValidationResult:
        """验证请求"""
        issues = []

        # 1. 验证不为空
        # 2. 验证长度
        # 3. 验证格式
        # 4. 验证内容

        is_valid = not any(
            issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]
            for issue in issues
        )

        return ValidationResult(is_valid=is_valid, issues=issues)
```

#### calculator.py模板

```python
"""
{Skill Name} Calculator
负责计算{指标类型}
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class {Skill}Metrics:
    """指标"""
    # 基础指标
    metric1: float
    metric2: int

    # 复杂度指标
    complexity_score: float

    # 推荐指标
    recommended_level: str
    recommendations: List[str]

class {Skill}Calculator:
    """计算器"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}

    def calculate(self, request: str, context: Optional[Dict] = None) -> {Skill}Metrics:
        """计算指标"""
        # 1. 计算基础指标
        # 2. 计算复杂度
        # 3. 生成推荐

        return {Skill}Metrics(...)
```

#### analyzer.py模板

```python
"""
{Skill Name} Analyzer
负责分析{分析对象}
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

class AnalysisPattern(Enum):
    PATTERN1 = "pattern1"
    PATTERN2 = "pattern2"

@dataclass
class AnalysisResult:
    detected_patterns: List[AnalysisPattern]
    quality_scores: Dict[str, float]
    optimization_suggestions: List[str]

class {Skill}Analyzer:
    """分析器"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}

    def analyze(self, request: str, context: Optional[Dict] = None) -> AnalysisResult:
        """分析"""
        # 1. 检测模式
        # 2. 计算质量分数
        # 3. 生成建议

        return AnalysisResult(...)
```

#### executor.py模板

```python
"""
{Skill Name} Executor
智能协调器：整合定性和定量
"""

from typing import Dict, Any, Optional
from pathlib import Path

from .validator import {Skill}Validator
from .calculator import {Skill}Calculator, {Skill}Metrics
from .analyzer import {Skill}Analyzer, AnalysisResult

class {Skill}Executor:
    """执行器"""

    def __init__(self, skill_dir: Optional[Path] = None):
        if skill_dir is None:
            skill_dir = Path(__file__).parent.parent

        self.skill_dir = Path(skill_dir)
        self.prompts_dir = self.skill_dir / "prompts"

        self.validator = {Skill}Validator()
        self.calculator = {Skill}Calculator()
        self.analyzer = {Skill}Analyzer()

    def execute(
        self,
        request: str,
        context: Optional[Dict] = None,
        force_level: Optional[str] = None
    ) -> Dict[str, Any]:
        """执行"""
        # 1. 验证
        validation = self.validator.validate(request, context)

        # 2. 计算
        metrics = self.calculator.calculate(request, context)

        # 3. 分析
        analysis = self.analyzer.analyze(request, context)

        # 4. 选择层次
        level = force_level or self._select_level(metrics, analysis)

        # 5. 加载提示词
        prompt = self._load_prompt(level)

        # 6. 返回结果
        return {
            "validation": validation,
            "metrics": metrics,
            "analysis": analysis,
            "level": level,
            "prompt": prompt
        }

    def _select_level(self, metrics, analysis) -> str:
        """智能选择层次"""
        if metrics.complexity_score < 0.3:
            return "00"
        elif metrics.complexity_score < 0.5:
            return "01"
        elif metrics.complexity_score < 0.7:
            return "02"
        else:
            return "03"

    def _load_prompt(self, level: str) -> str:
        """加载提示词"""
        filename_map = {
            "00": "00_context.md",
            "01": "01_basic.md",
            "02": "02_intermediate.md",
            "03": "03_advanced.md"
        }

        prompt_file = self.prompts_dir / filename_map[level]
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
```

### 端到端测试模板

```python
"""
{Skill Name} - End-to-End Test
"""

import sys
from pathlib import Path

# 添加技能目录
skills_dir = Path(__file__).parent / "skills" / "dnaspec-{skill}"
sys.path.insert(0, str(skills_dir))

from scripts.executor import {Skill}Executor

def test_1_prompt_loading():
    """测试提示词加载"""
    executor = {Skill}Executor(skills_dir)

    levels = ["00", "01", "02", "03"]
    for level in levels:
        prompt = executor._load_prompt(level)
        assert len(prompt) > 0, f"Level {level} prompt is empty"

    print("✅ Prompt loading test passed")

def test_2_validation():
    """测试输入验证"""
    executor = {Skill}Executor(skills_dir)

    # 测试用例
    test_cases = [
        ("正常请求", True),
        ("", False),
    ]

    for request, should_pass in test_cases:
        result = executor.validator.validate(request, None)
        assert result.is_valid == should_pass

    print("✅ Validation test passed")

def test_3_calculation():
    """测试指标计算"""
    executor = {Skill}Executor(skills_dir)

    metrics = executor.calculator.calculate("测试请求", None)
    assert metrics.complexity_score >= 0.0
    assert metrics.complexity_score <= 1.0

    print("✅ Calculation test passed")

def test_4_full_execution():
    """测试完整执行"""
    executor = {Skill}Executor(skills_dir)

    result = executor.execute("测试请求", None)

    assert "validation" in result
    assert "metrics" in result
    assert "analysis" in result
    assert "level" in result
    assert "prompt" in result

    print("✅ Full execution test passed")

if __name__ == "__main__":
    test_1_prompt_loading()
    test_2_validation()
    test_3_calculation()
    test_4_full_execution()

    print("\n🎉 All tests passed!")
```

---

## 🚀 推广实施计划

### Phase 1: 优先级1 - 核心技能（本周）

**技能1：modulizer**
- **优先级**：高（核心分解技能）
- **复杂度**：中等
- **预计时间**：2天
- **参考**：task-decomposer架构

**技能2：constraint-generator**
- **优先级**：高（质量保证）
- **复杂度**：中等
- **预计时间**：2天
- **参考**：task-decomposer + context-fundamentals

### Phase 2: 优先级2 - 优化技能（下周）

**技能3：context-analysis**
- **优先级**：高（整合context-degradation）
- **复杂度**：高
- **预计时间**：3天
- **特殊**：需要整合外部项目内容

**技能4：context-optimization**
- **优先级**：中
- **复杂度**：中等
- **预计时间**：2天
- **参考**：context-analysis

**技能5：cognitive-template**
- **优先级**：中
- **复杂度**：中等
- **预计时间**：2天
- **参考**：context-fundamentals

### Phase 3: 优先级3 - 协调和智能体（第3周）

**技能6：architect**
- **优先级**：中（协调技能）
- **复杂度**：高
- **预计时间**：3天

**技能7：system-architect**
- **优先级**：中
- **复杂度**：高
- **预计时间**：3天
- **参考**：architect

**技能8：agent-creator**
- **优先级**：高（整合memory-systems）
- **复杂度**：高
- **预计时间**：3天
- **特殊**：需要添加记忆系统设计

### Phase 4: 优先级4 - 质量保证和基础（第4周）

**技能9：dapi-checker**
- **优先级**：中
- **复杂度**：低
- **预计时间**：1-2天

**技能10：workspace**
- **优先级**：低
- **复杂度**：低
- **预计时间**：1天

**技能11：git**
- **优先级**：低
- **复杂度**：低
- **预计时间**：1天

---

## 📋 技能重构检查清单

### ✅ 必需组件

- [ ] SKILL.md (<500行，包含所有必需章节)
- [ ] prompts/目录（4层提示词文件）
- [ ] scripts/目录（4个生产级脚本）
- [ ] config/目录（parameters.yaml, constraints.json）
- [ ] 端到端测试文件

### ✅ SKILL.md检查

- [ ] When to Activate章节
- [ ] Core Concepts章节
- [ ] Practical Guidance章节
- [ ] Examples章节
- [ ] Guidelines章节
- [ ] Integration章节
- [ ] Key Achievements章节
- [ ] References章节（可选）

### ✅ 提示词检查

- [ ] 00_context.md (<500字符)
- [ ] 01_basic.md (<1000字符)
- [ ] 02_intermediate.md (<2000字符)
- [ ] 03_advanced.md (<3000字符)
- [ ] 每层自包含且完整
- [ ] 层次间渐进式披露

### ✅ 脚本检查

**validator.py**：
- [ ] 继承基础验证模式
- [ ] 检测空输入
- [ ] 检测长度限制
- [ ] 检测格式错误
- [ ] 提供有用的错误消息

**calculator.py**：
- [ ] 计算基础指标
- [ ] 计算复杂度分数（0-1）
- [ ] 智能推荐提示词层次
- [ ] 生成可操作的建议

**analyzer.py**：
- [ ] 检测关键模式
- [ ] 计算质量分数
- [ ] 生成优化建议
- [ ] 识别潜在问题

**executor.py**：
- [ ] 整合所有组件
- [ ] 智能选择层次
- [ ] 加载正确的提示词
- [ ] 返回完整的结果

### ✅ 配置检查

- [ ] parameters.yaml包含所有参数
- [ ] constraints.json定义所有约束
- [ ] 配置与脚本一致

### ✅ 测试检查

- [ ] 提示词加载测试
- [ ] 输入验证测试
- [ ] 指标计算测试
- [ ] 完整执行测试
- [ ] 至少3个测试用例
- [ ] 测试通过率>80%

---

## 🎯 质量标准

### 代码质量

- **代码行数**：每个脚本约200-400行
- **类型注解**：所有公共函数都有类型注解
- **文档字符串**：所有类和方法都有docstring
- **错误处理**：适当的异常处理和验证
- **可测试性**：代码易于单元测试

### 提示词质量

- **长度控制**：严格遵守字符限制
- **自包含**：每层都是独立完整的
- **渐进式**：信息逐步深入
- **清晰性**：结构清晰，易于理解
- **实用性**：提供可操作的指导

### 测试质量

- **覆盖率**：核心功能100%覆盖
- **通过率**：至少80%测试通过
- **边界情况**：包含边界测试
- **错误情况**：包含异常输入测试

---

## 📊 进度追踪

### 技能重构进度表

| 技能 | 状态 | 进度 | 开始日期 | 完成日期 | 负责人 |
|-----|------|------|---------|---------|--------|
| task-decomposer | ✅ 完成 | 100% | 2025-12-25 | 2025-12-25 | Claude |
| context-fundamentals | ✅ 完成 | 100% | 2025-12-26 | 2025-12-26 | Claude |
| modulizer | ⏳ 待开始 | 0% | - | - | - |
| constraint-generator | ⏳ 待开始 | 0% | - | - | - |
| context-analysis | ⏳ 待开始 | 0% | - | - | - |
| context-optimization | ⏳ 待开始 | 0% | - | - | - |
| cognitive-template | ⏳ 待开始 | 0% | - | - | - |
| architect | ⏳ 待开始 | 0% | - | - | - |
| system-architect | ⏳ 待开始 | 0% | - | - | - |
| agent-creator | ⏳ 待开始 | 0% | - | - | - |
| dapi-checker | ⏳ 待开始 | 0% | - | - | - |
| workspace | ⏳ 待开始 | 0% | - | - | - |
| git | ⏳ 待开始 | 0% | - | - | - |

### 里程碑

- **Milestone 1**：完成核心技能（task-decomposer, modulizer, constraint-generator）
- **Milestone 2**：完成优化技能（context-analysis, context-optimization, cognitive-template）
- **Milestone 3**：完成协调和智能体技能（architect, system-architect, agent-creator）
- **Milestone 4**：完成质量保证和基础技能（dapi-checker, workspace, git）
- **Milestone 5**：所有技能完成，建立评估体系

---

## 🔄 持续改进

### 反馈循环

1. **测试驱动**：每个技能重构后立即测试
2. **问题追踪**：记录遇到的问题和解决方案
3. **经验总结**：提炼可复用的模式和最佳实践
4. **模板更新**：根据经验持续改进模板

### 知识管理

- **文档化**：记录每个决策的理由
- **示例库**：收集好的示例和反模式
- **FAQ**：整理常见问题和解答
- **培训材料**：创建新手上手指南

---

## 📞 支持和资源

### 参考资料

- **成功案例**：task-decomposer, context-fundamentals
- **架构文档**：CONTRACT.yaml v3.0
- **整合方案**：SKILLS_INTEGRATION_PLAN.md
- **Agent-Skills分析**：AGENT_SKILLS_ANALYSIS_REPORT.md

### 获取帮助

- **查看示例**：参考已完成的技能
- **阅读文档**：CONTRACT.yaml定义了所有标准
- **运行测试**：使用测试模板验证实现
- **迭代改进**：第一次实现不必完美，持续优化

---

*推广指南版本：v1.0*
*创建日期：2025-12-26*
*基于：task-decomposer + context-fundamentals成功经验*
