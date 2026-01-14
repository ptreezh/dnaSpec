"""
创建符合OpenSkills/Claude规范的SKILL.md技能文件
"""
import os
import json
from pathlib import Path
from typing import Dict, Any

def create_skill_md_files():
    """创建SKILL.md技能文件"""
    skills_dir = Path(__file__).parent.parent / "skills"
    
    # 定义所有技能的SKILL.md内容
    skill_definitions = {
        "context-analysis-constitutional": """---
name: context-analysis-constitutional
description: Analyze context quality using constitutional principles with progressive disclosure
---

# Context Analysis Constitutional Skill

Analyze context quality using constitutional principles with progressive disclosure implementation and cognitive optimization.

## Purpose

This skill evaluates the quality of input context using five-dimensional metrics while ensuring constitutional compliance and cognitive optimization. It follows progressive disclosure for scalable analysis.

## When to Use

Use this skill when:
- Evaluating context quality before processing
- Applying constitutional validation to content
- Performing cognitive optimization analysis
- Following progressive disclosure principles

## Instructions

To analyze context quality constitutionally:

1. Provide context in input parameter
2. Execute analysis with constitutional validation
3. Review five-dimensional quality metrics
4. Apply cognitive optimization suggestions

Input format:
```
{
    "context": "Context to analyze",
    "detailed": true/false
}
```

## Constitutional Principles Applied

The skill implements:
- Progressive disclosure: Scalable analysis from basic to detailed
- Cognitive convenience: Clear, self-explanatory results
- Information encapsulation: Self-contained analysis
- Cognitive gestalt: Complete analysis units

## Output Metrics

Provides five-dimensional quality metrics:
- Clarity (0.0-1.0): Expression clearness
- Relevance (0.0-1.0): Task relevance
- Completeness (0.0-1.0): Information completeness
- Consistency (0.0-1.0): Logical consistency
- Efficiency (0.0-1.0): Information density

## Quality Thresholds

- High quality: ≥ 0.7
- Medium quality: ≥ 0.4
- Low quality: < 0.4
""",

        "temp-workspace-constitutional": """---
name: temp-workspace-constitutional
description: Constitutional temporary workspace management to prevent Git pollution with progressive disclosure
---

# Constitutional Temporary Workspace Skill

Manage AI-generated temporary files constitutionally to prevent project pollution while ensuring progressive disclosure and cognitive optimization.

## Purpose

This skill provides a constitutional temporary workspace mechanism that prevents temporary files from polluting Git repositories while maintaining cognitive convenience and progressive disclosure principles.

## When to Use

Use this skill when:
- Managing AI-generated temporary files
- Preventing Git repository pollution
- Following constitutional file operations
- Implementing progressive workspace disclosure

## Instructions

To manage constitutional temporary workspace:

1. Create workspace with constitutional rules
2. Add files with constitutional validation
3. Confirm files through constitutional process
4. Clean workspace following constitutional guidelines

Available operations:
- "create-workspace": Initialize constitutional workspace
- "add-file": Add file with constitutional validation
- "confirm-file": Confirm file with constitutional review
- "confirm-all": Confirm all files constitutionally
- "list-files": View workspace with progressive disclosure
- "clean-workspace": Clean following constitutional rules

## Constitutional Protection

The skill enforces:
- Temp file isolation from Git
- Constitutional validation of all operations
- Progressive disclosure of workspace status
- Cognitive convenience in management

## Security Features

- Automatic temporary file detection
- Constitutional commit prevention
- Workspace session management
- File lifecycle tracking
""",

        "git-operations-constitutional": """---
name: git-operations-constitutional
description: Constitutional Git operations with temporary file protection and progressive disclosure
---

# Constitutional Git Operations Skill

Perform Git operations with constitutional validation and automatic protection against temporary file pollution, following progressive disclosure principles.

## Purpose

This skill executes constitutional Git operations while preventing temporary files from being committed and ensuring all operations follow constitutional principles with progressive disclosure.

## When to Use

Use this skill when:
- Performing Git operations with constitutional safety
- Preventing temporary file pollution
- Implementing project constitution enforcement
- Following cognitive convenience principles

## Instructions

To perform constitutional Git operations:

1. Setup project constitution with rules
2. Execute Git operations with validation
3. Review constitutional compliance
4. Apply progressive disclosure as needed

Supported operations:
- "setup-constitution": Initialize project constitution
- "smart-commit": Commit with constitutional validation
- "validate-commit": Check commit constitutionality
- "install-hooks": Install constitutional Git hooks
- "status-report": Get constitutional status
- "auto-manage": Auto-manage constitutional compliance

## Constitutional Rules

Enforced rules include:
- Temporary file detection and blocking
- Constitutionally-valid commit messages
- Progressively-disclosed status reporting
- Cognitive convenience in operations

## Workflow Integration

The skill integrates with development workflows to ensure constitutional compliance throughout the Git process while maintaining progressive disclosure of information.
""",

        "progressive-disclosure-constitutional": """---
name: progressive-disclosure-constitutional
description: Constitutional progressive disclosure directory structure with cognitive optimization
---

# Constitutional Progressive Disclosure Skill

Create directory structures following constitutional principles with progressive disclosure implementation and cognitive optimization.

## Purpose

This skill creates project structures that implement constitutional principles with progressive disclosure, allowing information access at different detail levels while maintaining cognitive convenience.

## When to Use

Use this skill when:
- Creating project directory structures
- Implementing progressive disclosure
- Following constitutional design principles
- Optimizing cognitive convenience

## Instructions

To create constitutional progressive disclosure structure:

1. Define project requirements
2. Choose disclosure level (basic/intermediate/advanced)
3. Execute structure creation
4. Organize content with progressive access

Levels available:
- "basic": Essential structure with minimal disclosure
- "intermediate": Modular structure with moderate disclosure
- "advanced": Complete structure with full disclosure

Parameters:
- "project_name": Name of the project
- "disclosure_level": Level of progressive disclosure
- "requirements": Project requirements for structure

## Constitutional Implementation

The structure follows constitutional principles:
- Progressive disclosure: Hierarchical information access
- Cognitive convenience: Clear, organized structure
- Information encapsulation: Modular, self-contained units
- Cognitive gestalt: Complete structural units

## Benefits

- Graduated information access
- Reduced cognitive load
- Constitutional compliance
- Cognitive optimization
""",

        "cognitive-template-constitutional": """---
name: cognitive-template-constitutional
description: Apply constitutional cognitive templates with progressive disclosure and cognitive optimization
---

# Constitutional Cognitive Template Skill

Apply constitutional cognitive templates to enhance task processing with progressive disclosure and cognitive optimization principles.

## Purpose

This skill applies constitutional cognitive templates to structure complex tasks using proven cognitive frameworks while ensuring progressive disclosure and cognitive convenience.

## When to Use

Use this skill when:
- Processing complex tasks with cognitive templates
- Applying structured thinking patterns
- Following constitutional template principles
- Implementing progressive disclosure templates

## Instructions

To apply cognitive templates constitutionally:

1. Select appropriate template type
2. Provide context for template application
3. Execute template with constitutional validation
4. Review structured results with progressive disclosure

Available templates:
- "chain_of_thought": Sequential reasoning template
- "few_shot": Example-based learning template
- "verification": Quality verification template
- "role_playing": Role-based analysis template
- "understanding": Deep understanding template

## Constitutional Framework

Templates implement constitutional principles:
- Progressive disclosure: Hierarchical information organization
- Cognitive convenience: Clear, unambiguous structure
- Information encapsulation: Self-contained template application
- Cognitive gestalt: Complete reasoning units

## Template Benefits

- Structured approach to complex tasks
- Constitutional compliance
- Cognitive optimization
- Progressive information disclosure
"""
    }
    
    # 创建技能目录和SKILL.md文件
    for skill_name, skill_content in skill_definitions.items():
        skill_dir = skills_dir / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        skill_md_file = skill_dir / "SKILL.md"
        with open(skill_md_file, 'w', encoding='utf-8') as f:
            f.write(skill_content)
        
        print(f"✅ Created: {skill_md_file}")
    
    print(f"✅ 共创建了 {len(skill_definitions)} 个宪法级SKILL.md技能文件")
    
    # 创建参考文档
    create_reference_documents(skills_dir)

def create_reference_documents(base_dir: Path):
    """创建技能参考文档"""
    references_dir = base_dir / "references"
    references_dir.mkdir(exist_ok=True)
    
    # 1. 宪法原则参考
    constitutional_principles = """
# 宪法原则参考

## 四大原则

### 1. 渐进披露 (Progressive Disclosure)
- 信息按层次组织，支持不同详细程度访问
- 重要信息优先展示，详细信息按需展开
- 避免信息过载，减少认知负荷

### 2. 认知便利 (Cognitive Convenience) 
- 内容清晰、自明、完备、无歧义
- 最小化AI认知负荷
- 上下文认知准确，边界清晰

### 3. 信息封装 (Information Encapsulation)
- 子元素信息闭包，自包含
- 边界清晰，外部依赖最小化
- 内容独立，上下文完整

### 4. 认知格式塔 (Cognitive Gestalt)
- 形成完整认知单元
- 结构清晰连贯
- 意义整体性、可识别性
"""
    
    with open(references_dir / "constitutional_principles.md", 'w', encoding='utf-8') as f:
        f.write(constitutional_principles)
    
    # 2. 渐进披露参考
    progressive_disclosure = """
# 渐进披露原则参考

## 基本原则
- 重要信息优先展示
- 详细信息按需展开
- 支持层次化访问
- 减少初始认知负荷

## 实现方式
- 标题层次结构
- 摘要+详情模式
- 可折叠区域
- 状态指示器

## 应用场景
- 目录结构设计
- 文档组织
- 技能输出格式
- 信息展示界面
"""
    
    with open(references_dir / "progressive_disclosure_principles.md", 'w', encoding='utf-8') as f:
        f.write(progressive_disclosure)
    
    print("✅ 创建了技能参考文档")

# 执行创建
if __name__ == "__main__":
    create_skill_md_files()