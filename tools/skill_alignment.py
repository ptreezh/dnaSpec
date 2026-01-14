"""
技能对齐实现工具集
用于将现有DNASPEC技能对齐到Claude标准格式
"""

import json
import yaml
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List
import re

class SkillAlignmentTool:
    """技能对齐工具"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.config_path = self.project_root / ".dnaspec" / "cli_extensions" / "claude" / "dnaspec_skills.json"
        self.skills_dir = self.project_root / "skills"
        
    def create_skill_directory_structure(self):
        """创建标准技能目录结构"""
        print("创建技能目录结构...")
        
        if not self.skills_dir.exists():
            self.skills_dir.mkdir(parents=True, exist_ok=True)
            
        # 读取现有配置
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            for skill in config.get('skills', []):
                skill_name = skill.get('name', '').replace('dnaspec-', '')
                skill_dir = self.skills_dir / skill_name
                
                # 创建技能目录
                skill_dir.mkdir(exist_ok=True)
                
                # 创建子目录结构
                subdirs = ['examples', 'tools', 'resources', 'reference']
                for subdir in subdirs:
                    (skill_dir / subdir).mkdir(exist_ok=True)
                    
                print(f"✓ 创建技能目录: {skill_name}")
    
    def convert_skill_to_standard_format(self, skill_data: Dict[str, Any]) -> Dict[str, Any]:
        """将技能转换为标准格式"""
        skill_name = skill_data.get('name', '').replace('dnaspec-', '')
        
        # 创建标准YAML frontmatter
        frontmatter = {
            'name': skill_name,
            'description': self._enhance_description(skill_data.get('description', ''))
        }
        
        # 创建主SKILL.md内容
        skill_content = self._generate_skill_content(skill_data)
        
        return {
            'frontmatter': frontmatter,
            'content': skill_content,
            'original_data': skill_data
        }
    
    def _enhance_description(self, original_desc: str) -> str:
        """增强描述以符合标准"""
        # 添加使用时机说明
        if 'when' not in original_desc.lower() and '用于' not in original_desc:
            return f"{original_desc} Use when you need to design system architecture and create technical specifications."
        return original_desc
    
    def _generate_skill_content(self, skill_data: Dict[str, Any]) -> str:
        """生成技能内容"""
        skill_name = skill_data.get('name', '').replace('dnaspec-', '')
        category = skill_data.get('category', 'general')
        
        # 根据技能类型生成专门内容
        content_templates = {
            'architect': self._architect_content(),
            'agent-creator': self._agent_creator_content(),
            'task-decomposer': self._task_decomposer_content(),
            'constraint-generator': self._constraint_generator_content(),
            'dapi-checker': self._dapi_checker_content(),
            'modulizer': self._modulizer_content(),
            'cache-manager': self._cache_manager_content(),
            'git-operations': self._git_operations_content()
        }
        
        return content_templates.get(skill_name, self._default_skill_content(skill_name, category))
    
    def _architect_content(self) -> str:
        """架构师技能内容"""
        return '''# 系统架构设计技能

## 工作流程

1. **需求分析**: 分析项目需求和技术约束
2. **架构设计**: 设计系统整体架构和组件关系
3. **技术选型**: 选择合适的技术栈和框架
4. **文档生成**: 生成架构文档和技术规范

## 关键决策点

- 系统复杂度评估
- 技术栈兼容性分析
- 性能和扩展性考虑
- 安全性要求评估

## 基本使用方法

直接描述需要设计的系统需求，我将为您提供：
- 系统架构图
- 组件设计说明
- 技术选型建议
- 实施路线图

## 常见模式

- 微服务架构设计
- 分层架构设计
- 事件驱动架构
- 领域驱动设计
'''
    
    def _agent_creator_content(self) -> str:
        """智能体创建技能内容"""
        return '''# 智能体创建技能

## 工作流程

1. **需求理解**: 分析目标场景和任务需求
2. **角色定义**: 确定智能体的专业领域和职责
3. **能力设计**: 设计智能体的技能集和工具
4. **验证测试**: 验证智能体设计的有效性

## 关键决策点

- 任务复杂度评估
- 专业领域选择
- 工具集成需求
- 性能要求定义

## 基本使用方法

描述需要创建的智能体类型和应用场景，我将为您提供：
- 智能体角色定义
- 核心能力设计
- 工具配置建议
- 使用指南

## 常见模式

- 领域专家智能体
- 任务自动化智能体
- 分析决策智能体
- 协作助手智能体
'''
    
    def _task_decomposer_content(self) -> str:
        """任务分解技能内容"""
        return '''# 任务分解技能

## 工作流程

1. **任务分析**: 理解任务目标和约束条件
2. **依赖识别**: 识别任务间的依赖关系
3. **分解规划**: 制定合理的分解策略
4. **优先级排序**: 确定子任务的执行顺序

## 关键决策点

- 任务粒度控制
- 依赖关系处理
- 资源分配优化
- 风险评估管理

## 基本使用方法

提供需要分解的复杂任务描述，我将为您提供：
- 任务分解树
- 子任务定义
- 执行计划
- 依赖关系图

## 常见模式

- 项目管理任务分解
- 开发任务拆分
- 业务流程分解
- 学习计划制定
'''
    
    def _constraint_generator_content(self) -> str:
        """约束生成技能内容"""
        return '''# 约束生成技能

## 工作流程

1. **环境分析**: 分析系统环境和业务规则
2. **约束识别**: 识别各种约束条件
3. **规则制定**: 生成具体的约束规则
4. **验证机制**: 设计约束验证方法

## 关键决策点

- 约束类型确定
- 约束强度定义
- 验证策略选择
- 异常处理设计

## 基本使用方法

描述系统或项目需要满足的约束需求，我将为您提供：
- 约束规则定义
- 验证机制设计
- 实施建议
- 测试用例

## 常见模式

- 数据约束生成
- 业务规则约束
- 性能约束定义
- 安全约束设计
'''
    
    def _dapi_checker_content(self) -> str:
        """API检查技能内容"""
        return '''# API接口检查技能

## 工作流程

1. **接口分析**: 分析API接口设计和实现
2. **规范验证**: 检查是否符合API设计规范
3. **功能测试**: 验证接口功能完整性
4. **文档评估**: 评估API文档质量

## 关键决策点

- 接口设计规范
- 数据格式标准
- 错误处理机制
- 安全性检查

## 基本使用方法

提供API接口代码或文档，我将为您提供：
- 接口设计分析
- 规范符合性检查
- 改进建议
- 测试用例设计

## 常见模式

- REST API检查
- GraphQL接口验证
- 微服务接口分析
- API文档评估
'''
    
    def _modulizer_content(self) -> str:
        """模块化技能内容"""
        return '''# 模块化设计技能

## 工作流程

1. **代码分析**: 分析现有代码结构和依赖关系
2. **模块识别**: 识别可模块化的功能单元
3. **接口设计**: 设计模块间接口和数据流
4. **重构实施**: 制定模块化重构方案

## 关键决策点

- 模块边界划分
- 接口设计原则
- 依赖关系管理
- 可测试性考虑

## 基本使用方法

提供需要模块化的代码或系统描述，我将为您提供：
- 模块化设计方案
- 接口定义
- 重构步骤
- 测试策略

## 常见模式

- 单一职责模块化
- 分层架构模块化
- 组件化设计
- 服务化改造
'''
    
    def _cache_manager_content(self) -> str:
        """缓存管理技能内容"""
        return '''# 缓存管理技能

## 工作流程

1. **缓存需求分析**: 分析缓存使用场景和需求
2. **策略设计**: 设计缓存策略和生命周期管理
3. **实施部署**: 实施缓存解决方案
4. **监控优化**: 监控缓存效果并优化

## 关键决策点

- 缓存类型选择
- 过期策略设计
- 一致性保证
- 性能优化

## 基本使用方法

描述缓存管理需求，我将为您提供：
- 缓存策略设计
- 实施方案
- 监控指标
- 优化建议

## 常见模式

- 应用缓存管理
- 数据库缓存优化
- 分布式缓存设计
- CDN配置管理
'''
    
    def _git_operations_content(self) -> str:
        """Git操作技能内容"""
        return '''# Git操作管理技能

## 工作流程

1. **规则制定**: 制定Git工作流和提交规范
2. **自动化配置**: 配置自动化Git操作
3. **质量检查**: 实施代码质量检查
4. **协作优化**: 优化团队协作流程

## 关键决策点

- 工作流选择
- 分支策略制定
- 提交规范设计
- 代码审查流程

## 基本使用方法

描述Git管理需求，我将为您提供：
- 工作流设计
- 规范制定
- 自动化配置
- 最佳实践建议

## 常见模式

- Git Flow工作流
- GitHub Flow策略
- 提交规范制定
- 分支保护设置
'''
    
    def _default_skill_content(self, skill_name: str, category: str) -> str:
        """默认技能内容模板"""
        return f'''# {skill_name.title()} 技能

## 工作流程

1. **需求理解**: 理解任务需求和目标
2. **方案设计**: 设计解决方案和实施计划
3. **执行实施**: 执行具体任务和操作
4. **结果验证**: 验证结果质量和效果

## 关键决策点

- 需求分析准确性
- 方案可行性评估
- 资源配置优化
- 质量标准制定

## 基本使用方法

描述相关任务需求，我将为您提供：
- 需求分析结果
- 解决方案设计
- 实施指导
- 质量保证建议

## 常见模式

- 标准任务处理
- 特殊需求适配
- 质量优化方案
- 效率提升建议
'''
    
    def create_skill_files(self):
        """创建标准格式的技能文件"""
        print("创建技能文件...")
        
        if not self.config_path.exists():
            print("❌ 配置文件不存在")
            return
            
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        for skill in config.get('skills', []):
            skill_name = skill.get('name', '').replace('dnaspec-', '')
            skill_dir = self.skills_dir / skill_name
            
            # 转换技能格式
            standard_skill = self.convert_skill_to_standard_format(skill)
            
            # 创建SKILL.md文件
            skill_md_path = skill_dir / "SKILL.md"
            with open(skill_md_path, 'w', encoding='utf-8') as f:
                # 写入YAML frontmatter
                f.write('---\n')
                yaml.dump(standard_skill['frontmatter'], f, default_flow_style=False, allow_unicode=True)
                f.write('---\n\n')
                # 写入内容
                f.write(standard_skill['content'])
                
            print(f"✓ 创建技能文件: {skill_name}/SKILL.md")
            
            # 创建示例文件
            self._create_example_files(skill_dir, skill_name)
    
    def _create_example_files(self, skill_dir: Path, skill_name: str):
        """创建示例文件"""
        examples_dir = skill_dir / "examples"
        
        # 创建基本使用示例
        basic_example = examples_dir / "basic-usage.md"
        with open(basic_example, 'w', encoding='utf-8') as f:
            f.write(f'''# {skill_name.title()} 基本使用示例

## 示例场景

描述一个典型的使用场景和操作步骤。

## 操作步骤

1. 步骤描述
2. 具体操作
3. 预期结果

## 注意事项

- 注意事项1
- 注意事项2
''')
        
        # 创建高级模式示例
        advanced_example = examples_dir / "advanced-patterns.md"
        with open(advanced_example, 'w', encoding='utf-8') as f:
            f.write(f'''# {skill_name.title()} 高级模式

## 复杂场景处理

描述如何在复杂场景中使用此技能。

## 最佳实践

- 最佳实践1
- 最佳实践2
- 常见问题解决
''')
    
    def create_migration_guide(self):
        """创建迁移指南"""
        guide_path = self.project_root / "MIGRATION_GUIDE.md"
        
        guide_content = '''# DNASPEC 技能迁移指南

## 概述

本指南说明如何将DNASPEC技能从现有格式迁移到Claude标准格式。

## 迁移步骤

### 1. 目录结构迁移

```
旧格式:
.dnaspec/cli_extensions/claude/dnaspec_skills.json

新格式:
skills/
├── architect/
│   ├── SKILL.md
│   ├── examples/
│   ├── tools/
│   └── resources/
├── agent-creator/
│   ├── SKILL.md
│   └── ...
└── ...
```

### 2. 文件格式变更

#### 技能定义格式

**旧格式 (JSON):**
```json
{
  "name": "dnaspec-architect",
  "description": "Design system architecture",
  "category": "design",
  "command": "/dnaspec.architect",
  "handler": {...}
}
```

**新格式 (SKILL.md + YAML):**
```yaml
---
name: architect
description: "Design system architecture and technical specifications. Use when you need to create system designs."
---

# 系统架构设计技能

[技能内容...]
```

### 3. 执行机制变更

- **旧方式**: 通过Python模块调用
- **新方式**: Claude自然语言理解 + 工具调用

### 4. 向后兼容性

- 保持原有JSON配置文件
- 新增标准技能目录
- 支持渐进式迁移

## 验证方法

运行测试套件验证迁移效果:

```bash
python tests/test_skill_alignment.py
```

## 注意事项

1. 保持技能名称一致性
2. 确保描述包含使用时机
3. 遵循渐进式披露原则
4. 维护向后兼容性
'''
        
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
            
        print(f"✓ 创建迁移指南: {guide_path}")
    
    def run_alignment_process(self):
        """执行完整的对齐流程"""
        print("开始DNASPEC技能对齐流程...")
        
        try:
            # 1. 创建目录结构
            self.create_skill_directory_structure()
            
            # 2. 创建技能文件
            self.create_skill_files()
            
            # 3. 创建迁移指南
            self.create_migration_guide()
            
            print("\n✅ 技能对齐完成!")
            print("\n下一步:")
            print("1. 运行测试验证: python tests/test_skill_alignment.py")
            print("2. 查看迁移指南: MIGRATION_GUIDE.md")
            print("3. 测试技能功能")
            
        except Exception as e:
            print(f"❌ 对齐过程中出现错误: {e}")
            raise


if __name__ == "__main__":
    # 使用示例
    project_root = "."  # 当前目录
    aligner = SkillAlignmentTool(project_root)
    aligner.run_alignment_process()