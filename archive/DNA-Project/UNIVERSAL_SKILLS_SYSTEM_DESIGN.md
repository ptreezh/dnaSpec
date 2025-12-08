# 通用化跨平台AI技能系统方案

## 1. 核心设计理念

### 1.1 平台无关性
- 核心技能逻辑与具体AI平台解耦
- 通过适配器模式支持不同平台集成
- 统一的技能接口和数据结构定义

### 1.2 可扩展性
- 插件化架构支持新平台快速接入
- 模块化设计便于功能扩展
- 标准化接口降低集成复杂度

### 1.3 兼容性
- 向后兼容现有Claude Code Skills
- 支持各平台原生集成方式
- 保持各平台最佳用户体验

## 2. 架构设计

### 2.1 分层架构
```
DNASPEC Skills System
├── Core Layer (平台无关核心)
│   ├── Skill Interface (技能接口定义)
│   ├── Skill Manager (技能管理器)
│   ├── Matcher Engine (匹配引擎)
│   └── Data Models (数据模型)
├── Adapter Layer (平台适配器)
│   ├── Claude CLI Adapter (SKILL.md生成)
│   ├── Gemini CLI Adapter (MCP服务器)
│   ├── Qwen CLI Adapter (MCP服务器)
│   └── Other Platform Adapters
└── Integration Layer (集成层)
    ├── Configuration Manager (配置管理)
    ├── Plugin System (插件系统)
    └── Deployment Tools (部署工具)
```

### 2.2 核心组件设计

#### 2.2.1 抽象技能接口
```python
# dnaspec_core/skill.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class SkillResult:
    """平台无关的技能执行结果"""
    skill_name: str
    success: bool
    result: Any
    confidence: float
    metadata: Dict[str, Any]

class DNASpecSkill(ABC):
    """抽象技能基类"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def process_request(self, request: str, context: Dict[str, Any] = None) -> SkillResult:
        """处理请求 - 子类必须实现"""
        pass
    
    @abstractmethod
    def get_skill_info(self) -> Dict[str, Any]:
        """获取技能信息 - 子类必须实现"""
        pass
```

#### 2.2.2 统一技能管理器
```python
# dnaspec_core/manager.py
from typing import Dict, List, Optional
from .skill import DNASpecSkill, SkillResult
from .models import SkillInfo

class SkillManager:
    """平台无关的技能管理器"""
    def __init__(self):
        self.skills: Dict[str, DNASpecSkill] = {}
        self.skill_registry: Dict[str, SkillInfo] = {}
    
    def register_skill(self, skill: DNASpecSkill):
        """注册技能"""
        self.skills[skill.name] = skill
        # 更新技能注册表
    
    def match_skill(self, request: str) -> Optional[SkillInfo]:
        """平台无关的技能匹配"""
        # 统一的匹配逻辑
        pass
    
    def execute_skill(self, skill_name: str, request: str, context: Dict[str, Any] = None) -> SkillResult:
        """执行技能"""
        if skill_name in self.skills:
            return self.skills[skill_name].process_request(request, context)
        # 返回错误结果
```

### 2.3 平台适配器设计

#### 2.3.1 Claude CLI适配器
```python
# adapters/claude/adapter.py
import os
from typing import Dict, Any
from dnaspec_core.manager import SkillManager

class ClaudeCLIAdapter:
    """Claude CLI适配器"""
    def __init__(self, skill_manager: SkillManager):
        self.skill_manager = skill_manager
    
    def generate_skill_md(self, skill_name: str, output_dir: str):
        """生成SKILL.md文件"""
        skill_info = self.skill_manager.get_skill_info(skill_name)
        if skill_info:
            # 生成符合Claude规范的SKILL.md文件
            pass
    
    def create_claude_skill_structure(self, output_dir: str):
        """创建Claude技能目录结构"""
        # 创建目录结构和相关文件
```

#### 2.3.2 Gemini CLI适配器
```python
# adapters/gemini/adapter.py
from typing import Dict, Any
from dnaspec_core.manager import SkillManager
# Gemini MCP相关导入

class GeminiCLIAdapter:
    """Gemini CLI适配器"""
    def __init__(self, skill_manager: SkillManager):
        self.skill_manager = skill_manager
    
    def create_mcp_server(self):
        """创建MCP服务器"""
        # 实现Gemini兼容的MCP服务器
        pass
    
    def handle_mcp_request(self, request: Dict[str, Any]):
        """处理MCP请求"""
        # 处理来自Gemini CLI的MCP请求
```

#### 2.3.3 Qwen CLI适配器
```python
# adapters/qwen/adapter.py
from typing import Dict, Any
from dnaspec_core.manager import SkillManager
# Qwen MCP相关导入

class QwenCLIAdapter:
    """Qwen CLI适配器"""
    def __init__(self, skill_manager: SkillManager):
        self.skill_manager = skill_manager
    
    def create_qwen_mcp_server(self):
        """创建Qwen兼容的MCP服务器"""
        # 实现Qwen Code兼容的MCP服务器
        pass
```

## 3. 配置管理

### 3.1 统一配置文件
```yaml
# dnaspec_config.yaml
skills:
  - name: dnaspec-agent-creator
    description: "DNASPEC智能体创建器"
    keywords:
      - "创建智能体"
      - "智能体设计"
      - "agent creator"
    version: "1.0.0"

platforms:
  claude:
    enabled: true
    skills_dir: "~/.claude/skills/dnaspec"
  
  gemini:
    enabled: true
    mcp_port: 8080
    transport: "stdio"
  
  qwen:
    enabled: true
    mcp_port: 8081
    transport: "stdio"
```

### 3.2 配置管理器
```python
# config/manager.py
import yaml
from typing import Dict, Any

class ConfigManager:
    """统一配置管理器"""
    def __init__(self, config_file: str):
        self.config = self._load_config(config_file)
    
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """加载配置文件"""
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get_platform_config(self, platform: str) -> Dict[str, Any]:
        """获取平台配置"""
        return self.config.get('platforms', {}).get(platform, {})
    
    def get_skill_config(self, skill_name: str) -> Dict[str, Any]:
        """获取技能配置"""
        skills = self.config.get('skills', [])
        for skill in skills:
            if skill.get('name') == skill_name:
                return skill
        return {}
```

## 4. 部署和使用

### 4.1 统一部署脚本
```bash
#!/bin/bash
# deploy_all.sh
echo "部署DNASPEC技能到所有支持的平台..."

# 部署到Claude CLI
python deploy.py --platform claude

# 部署到Gemini CLI
python deploy.py --platform gemini

# 部署到Qwen CLI
python deploy.py --platform qwen

echo "部署完成！"
```

### 4.2 平台特定部署
```python
# deploy.py
import argparse
from config.manager import ConfigManager
from adapters.claude.adapter import ClaudeCLIAdapter
from adapters.gemini.adapter import GeminiCLIAdapter
from adapters.qwen.adapter import QwenCLIAdapter

def deploy_to_platform(platform: str, config_manager: ConfigManager):
    """部署到指定平台"""
    if platform == "claude":
        adapter = ClaudeCLIAdapter(skill_manager)
        # 生成SKILL.md文件
    elif platform == "gemini":
        adapter = GeminiCLIAdapter(skill_manager)
        # 启动MCP服务器
    elif platform == "qwen":
        adapter = QwenCLIAdapter(skill_manager)
        # 启动Qwen兼容的MCP服务器

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", required=True, help="目标平台")
    args = parser.parse_args()
    
    config_manager = ConfigManager("dnaspec_config.yaml")
    deploy_to_platform(args.platform, config_manager)
```

## 5. 优势对比

### 5.1 与当前Gemini CLI方案对比

| 特性 | 当前Gemini CLI方案 | 通用化方案 |
|------|-------------------|------------|
| 平台兼容性 | 仅支持Gemini CLI | 支持所有主流AI CLI |
| 代码复用 | 无法复用 | 核心逻辑100%复用 |
| 维护成本 | 高 | 低 |
| 扩展性 | 差 | 好 |
| 部署复杂度 | 中等 | 低 |

### 5.2 与Claude Skills方案对比

| 特性 | Claude Skills | 通用化方案 |
|------|---------------|------------|
| 集成方式 | SKILL.md文件 | 多种适配器支持 |
| 发现机制 | 文件系统扫描 | 统一管理 |
| 执行环境 | Claude沙箱 | 平台原生环境 |
| 可移植性 | 低 | 高 |

## 6. 实施步骤

### 6.1 第一阶段：核心抽象
1. 提取平台无关的核心逻辑
2. 定义统一的接口和数据模型
3. 实现基本的技能管理和匹配功能

### 6.2 第二阶段：适配器开发
1. 开发Claude CLI适配器
2. 开发Gemini CLI适配器
3. 开发Qwen CLI适配器

### 6.3 第三阶段：集成测试
1. 在各平台测试技能功能
2. 验证跨平台兼容性
3. 优化性能和用户体验

### 6.4 第四阶段：文档和部署
1. 编写跨平台使用文档
2. 创建自动化部署工具
3. 提供示例和最佳实践