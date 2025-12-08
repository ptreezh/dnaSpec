# DSGS与spec.kit整合TDD实施规划

## 1. TDD实施原则

### 1.1 核心原则
- 测试先行：先编写测试用例，再实现功能
- 原子化测试：每个测试用例只测试一个功能点
- 自动化测试：所有测试都能自动运行和验证
- 持续集成：测试与开发过程紧密结合

### 1.2 测试分类
- 单元测试：测试单个函数或类的功能
- 集成测试：测试多个组件协同工作
- 系统测试：测试完整功能流程
- 性能测试：测试系统性能指标

## 2. 测试框架选择

### 2.1 Python测试框架
```python
# 推荐使用pytest作为主要测试框架
import pytest
from unittest.mock import Mock, patch

# 测试覆盖率工具
# coverage.py用于测试覆盖率分析

# 持续集成
# GitHub Actions或类似CI工具
```

### 2.2 测试目录结构
```
tests/
├── unit/                 # 单元测试
│   ├── test_adapters/    # 适配器测试
│   ├── test_core/        # 核心功能测试
│   └── test_utils/       # 工具函数测试
├── integration/          # 集成测试
│   ├── test_claude/      # Claude CLI集成测试
│   ├── test_gemini/      # Gemini CLI集成测试
│   └── test_qwen/        # Qwen CLI集成测试
├── system/               # 系统测试
│   └── test_workflows/   # 完整工作流测试
└── performance/          # 性能测试
    └── test_benchmarks/  # 基准测试
```

## 3. 原子化任务TDD实施

### 3.1 第一个原子任务：spec.kit适配器基类

#### 红色阶段（测试先行）
```python
# tests/unit/test_adapters/test_spec_kit_adapter.py
import pytest
from dnaspec.adapters.spec_kit_adapter import SpecKitAdapter

def test_spec_kit_adapter_initialization():
    """测试spec.kit适配器初始化"""
    adapter = SpecKitAdapter()
    assert adapter is not None
    assert hasattr(adapter, 'supported_agents')

def test_spec_kit_adapter_supported_agents():
    """测试支持的AI代理列表"""
    adapter = SpecKitAdapter()
    supported = adapter.get_supported_agents()
    assert isinstance(supported, list)
    assert len(supported) > 0
```

#### 绿色阶段（实现功能）
```python
# dnaspec/adapters/spec_kit_adapter.py
class SpecKitAdapter:
    """spec.kit适配器基类"""
    
    def __init__(self):
        self.supported_agents = [
            'claude', 'gemini', 'qwen', 'copilot',
            'cursor', 'windsurf', 'opencode'
        ]
    
    def get_supported_agents(self):
        """获取支持的AI代理列表"""
        return self.supported_agents
```

#### 重构阶段（优化代码）
```python
# dnaspec/adapters/spec_kit_adapter.py
class SpecKitAdapter:
    """spec.kit适配器基类"""
    
    SUPPORTED_AGENTS = [
        'claude', 'gemini', 'qwen', 'copilot',
        'cursor', 'windsurf', 'opencode'
    ]
    
    def __init__(self):
        self.supported_agents = self.SUPPORTED_AGENTS.copy()
    
    def get_supported_agents(self):
        """获取支持的AI代理列表"""
        return self.supported_agents
    
    def is_agent_supported(self, agent_name: str) -> bool:
        """检查指定代理是否被支持"""
        return agent_name.lower() in [agent.lower() for agent in self.supported_agents]
```

#### 添加新测试
```python
# tests/unit/test_adapters/test_spec_kit_adapter.py
def test_spec_kit_adapter_is_agent_supported():
    """测试代理支持检查功能"""
    adapter = SpecKitAdapter()
    
    # 测试支持的代理
    assert adapter.is_agent_supported('claude') is True
    assert adapter.is_agent_supported('Claude') is True  # 大小写不敏感
    
    # 测试不支持的代理
    assert adapter.is_agent_supported('unsupported') is False
```

### 3.2 第二个原子任务：依赖检查功能

#### 红色阶段
```python
# tests/unit/test_adapters/test_spec_kit_adapter.py
def test_spec_kit_adapter_check_dependencies():
    """测试依赖检查功能"""
    adapter = SpecKitAdapter()
    
    # 模拟系统命令检查
    with patch('shutil.which') as mock_which:
        mock_which.return_value = '/usr/bin/git'
        result = adapter.check_dependencies()
        assert isinstance(result, dict)
        assert 'git' in result
        assert result['git'] is True
```

#### 绿色阶段
```python
# dnaspec/adapters/spec_kit_adapter.py
import shutil
from typing import Dict

class SpecKitAdapter:
    # ... 前面的代码 ...
    
    def check_dependencies(self) -> Dict[str, bool]:
        """检查系统依赖"""
        dependencies = ['git', 'python']
        results = {}
        
        for dep in dependencies:
            results[dep] = shutil.which(dep) is not None
        
        return results
```

#### 重构阶段
```python
# dnaspec/adapters/spec_kit_adapter.py
class SpecKitAdapter:
    # ... 前面的代码 ...
    
    REQUIRED_DEPENDENCIES = ['git', 'python', 'specify']
    
    def check_dependencies(self) -> Dict[str, bool]:
        """检查系统依赖"""
        results = {}
        
        for dep in self.REQUIRED_DEPENDENCIES:
            results[dep] = self._check_dependency(dep)
        
        return results
    
    def _check_dependency(self, dependency: str) -> bool:
        """检查单个依赖"""
        return shutil.which(dependency) is not None
```

## 4. 集成测试实施

### 4.1 命令映射测试
```python
# tests/integration/test_command_mapping.py
import pytest
from dnaspec.adapters.spec_kit_adapter import SpecKitAdapter
from dnaspec.core.skill_manager import SkillManager

def test_command_mapping_integration():
    """测试命令映射集成"""
    adapter = SpecKitAdapter()
    skill_manager = SkillManager()
    
    # 注册测试技能
    skill_manager.register_skill("dnaspec-architect", "系统架构师")
    
    # 测试命令映射
    command = "/speckit.dnaspec.architect"
    mapped_skill = adapter.map_command_to_skill(command)
    
    assert mapped_skill == "dnaspec-architect"
```

### 4.2 跨平台测试
```python
# tests/integration/test_cross_platform.py
import pytest
import platform
from dnaspec.adapters.spec_kit_adapter import SpecKitAdapter

@pytest.mark.skipif(platform.system() != "Windows", reason="仅在Windows上测试")
def test_windows_specific_functionality():
    """测试Windows特定功能"""
    adapter = SpecKitAdapter()
    # Windows特定测试

@pytest.mark.skipif(platform.system() != "Linux", reason="仅在Linux上测试")
def test_linux_specific_functionality():
    """测试Linux特定功能"""
    adapter = SpecKitAdapter()
    # Linux特定测试
```

## 5. TDD实施流程

### 5.1 每日TDD循环
1. **计划**：选择下一个原子任务
2. **红色**：编写失败的测试用例
3. **绿色**：编写最少代码使测试通过
4. **重构**：优化代码结构和性能
5. **验证**：运行所有相关测试确保不破坏现有功能

### 5.2 测试覆盖率目标
- 单元测试覆盖率：≥ 85%
- 集成测试覆盖率：≥ 70%
- 核心功能测试覆盖率：100%

### 5.3 持续集成配置
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          pytest tests/ --cov=dnaspec --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

## 6. 质量保证措施

### 6.1 代码审查检查清单
- [ ] 所有新功能都有对应的测试用例
- [ ] 测试覆盖率符合要求
- [ ] 代码遵循PEP8规范
- [ ] 文档已更新
- [ ] 没有破坏现有功能

### 6.2 性能基准测试
```python
# tests/performance/test_benchmark.py
import time
import pytest
from dnaspec.adapters.spec_kit_adapter import SpecKitAdapter

def test_command_parsing_performance():
    """测试命令解析性能"""
    adapter = SpecKitAdapter()
    command = "/speckit.dnaspec.architect 设计电商系统架构"
    
    # 执行1000次命令解析
    start_time = time.time()
    for _ in range(1000):
        adapter.parse_command(command)
    end_time = time.time()
    
    # 确保平均响应时间小于10ms
    avg_time = (end_time - start_time) / 1000
    assert avg_time < 0.01
```

### 6.3 错误处理测试
```python
# tests/unit/test_adapters/test_error_handling.py
import pytest
from dnaspec.adapters.spec_kit_adapter import SpecKitAdapter

def test_invalid_command_handling():
    """测试无效命令处理"""
    adapter = SpecKitAdapter()
    
    with pytest.raises(ValueError):
        adapter.parse_command("")
    
    with pytest.raises(ValueError):
        adapter.parse_command(None)
```

## 7. 测试驱动开发节奏

### 7.1 每个开发日的TDD节奏
- 上午：2小时新功能TDD开发
- 下午：1小时回归测试 + 1小时代码重构
- 每日结束：运行完整测试套件

### 7.2 每周TDD回顾
- 周一：本周任务规划和测试策略
- 周三：中期测试覆盖率检查
- 周五：完整测试套件运行和质量评估

通过这样的TDD实施规划，我们可以确保DSGS与spec.kit的整合过程质量可控、风险可管理，并且最终交付一个高质量、可维护的系统。