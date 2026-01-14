#!/usr/bin/env python3
"""
完整的DNASPEC技能对齐工具
包含所有技能的完整对齐工作
"""

import json
import yaml
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List
import re

class CompleteSkillAlignmentTool:
    """完整技能对齐工具"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.config_path = self.project_root / ".dnaspec" / "cli_extensions" / "claude" / "dnaspec_skills.json"
        self.skills_dir = self.project_root / "skills"
        
    def get_complete_skill_list(self) -> List[Dict[str, Any]]:
        """获取完整的技能清单"""
        return [
            {
                "name": "context-analyzer",
                "description": "Analyzes context quality across 5 dimensions (clarity, relevance, completeness, consistency, efficiency)",
                "category": "analysis",
                "command": "/dnaspec.context-analyzer"
            },
            {
                "name": "context-optimizer",
                "description": "Optimizes context quality using AI-driven improvements based on specific goals",
                "category": "optimization",
                "command": "/dnaspec.context-optimizer"
            },
            {
                "name": "cognitive-templater",
                "description": "Applies cognitive templates (chain-of-thought, verification, few-shot, role-playing, understanding)",
                "category": "cognitive",
                "command": "/dnaspec.cognitive-templater"
            },
            {
                "name": "architect",
                "description": "Design system architecture and technical specifications",
                "category": "design",
                "command": "/dnaspec.architect"
            },
            {
                "name": "simple-architect",
                "description": "Provides simple architecture design for basic projects",
                "category": "design",
                "command": "/dnaspec.simple-architect"
            },
            {
                "name": "system-architect",
                "description": "Provides advanced system architecture design and detailed specifications",
                "category": "design",
                "command": "/dnaspec.system-architect"
            },
            {
                "name": "agent-creator",
                "description": "Create intelligent agents for specific tasks and domains",
                "category": "agents",
                "command": "/dnaspec.agent-creator"
            },
            {
                "name": "task-decomposer",
                "description": "Decompose complex tasks into manageable steps",
                "category": "planning",
                "command": "/dnaspec.task-decomposer"
            },
            {
                "name": "constraint-generator",
                "description": "Generate constraints and validation rules for development",
                "category": "validation",
                "command": "/dnaspec.constraint-generator"
            },
            {
                "name": "dapi-checker",
                "description": "Analyze and validate API interfaces and specifications",
                "category": "analysis",
                "command": "/dnaspec.dapi-checker"
            },
            {
                "name": "modulizer",
                "description": "Break down code into reusable and maintainable modules",
                "category": "refactoring",
                "command": "/dnaspec.modulizer"
            },
            {
                "name": "cache-manager",
                "description": "Manage AI-generated files with staging and validation to prevent workspace pollution",
                "category": "maintenance",
                "command": "/dnaspec.cache-manager"
            },
            {
                "name": "git-operations",
                "description": "Setup Git constitution and rules to prevent AI file pollution in projects",
                "category": "maintenance",
                "command": "/dnaspec.git-operations"
            }
        ]
    
    def update_config_file(self):
        """更新配置文件以包含所有技能"""
        print("更新配置文件...")
        
        complete_skills = self.get_complete_skill_list()
        
        # 更新技能数据以匹配标准格式
        for skill in complete_skills:
            skill['handler'] = {
                "type": "python",
                "module": "dna_spec_kit_integration.cli_extension_handler",
                "function": "handle_dnaspec_command",
                "parameters": {
                    "skill_name": skill['name'],
                    "function": f"execute_{skill['name'].replace('-', '_')}"
                }
            }
        
        # 更新配置文件
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {
                "version": "1.0.0",
                "name": "DNASPEC Skills",
                "description": "DNA SPEC Context Engineering Skills for Claude",
                "skills": []
            }
        
        # 添加dnaspec-前缀
        for skill in complete_skills:
            skill['name'] = f"dnaspec-{skill['name']}"
        
        config['skills'] = complete_skills
        config['generated_at'] = "2025-12-20T00:00:00.000000"
        config['project_root'] = str(self.project_root)
        
        # 写入更新后的配置
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
        print(f"✓ 更新配置文件: {self.config_path}")
    
    def create_context_analyzer_skill(self):
        """创建上下文分析技能"""
        skill_dir = self.skills_dir / "context-analyzer"
        skill_dir.mkdir(exist_ok=True)
        
        # 创建子目录
        for subdir in ['examples', 'tools', 'resources', 'reference']:
            (skill_dir / subdir).mkdir(exist_ok=True)
        
        # 创建SKILL.md
        skill_content = '''---
name: context-analyzer
description: Analyzes context quality across 5 dimensions (clarity, relevance, completeness, consistency, efficiency). Use when you need to evaluate document quality, assess requirement completeness, check communication effectiveness, or validate content before processing.
license: MIT
compatibility: Claude Code, VS Code, and any Agent Skills compatible environment
metadata:
  author: DNASPEC Team
  version: "2.0.0"
  category: quality-assessment
  supported_languages: [en, zh-CN, zh-TW, ja, ko]
  analysis_dimensions: [clarity, relevance, completeness, consistency, efficiency]
---

# Context Analyzer Skill

The Context Analyzer skill provides comprehensive quality assessment for text contexts and documents. It evaluates content across five key dimensions to provide actionable insights for improvement.

## Analysis Dimensions

### 1. Clarity (清晰度)

Evaluates how clearly the content expresses its intended meaning.

**Assessment criteria:**
- Language precision and unambiguity
- Logical flow and coherence
- Technical term usage appropriateness
- Structural organization

### 2. Relevance (相关性)

Measures how well the content aligns with its intended purpose and audience.

**Assessment criteria:**
- Topic focus maintenance
- Target audience appropriateness
- Goal alignment
- Information value density

### 3. Completeness (完整性)

Assesses whether all necessary information is present and sufficient.

**Assessment criteria:**
- Information sufficiency
- Coverage of key aspects
- Missing critical elements
- Context completeness

### 4. Consistency (一致性)

Checks for internal consistency and logical coherence.

**Assessment criteria:**
- Terminology consistency
- Logical coherence
- Temporal consistency
- Contradiction detection

### 5. Efficiency (效率)

Evaluates information density and presentation efficiency.

**Assessment criteria:**
- Information-to-noise ratio
- Redundancy elimination
- Conciseness optimization
- Cognitive load management

## 工作流程

1. **Context Input**: Receive the context to be analyzed
2. **Dimension Analysis**: Evaluate each of the 5 dimensions
3. **Score Calculation**: Generate quality scores for each dimension
4. **Improvement Suggestions**: Provide specific recommendations
5. **Report Generation**: Create comprehensive analysis report

## 关键决策点

- **Analysis Depth**: Basic vs. comprehensive evaluation
- **Target Standards**: Academic, business, or technical quality standards
- **Improvement Priority**: Which dimensions to focus on first
- **Format Requirements**: Output format and detail level

## 基本使用方法

Simply provide the context you want to analyze. The skill will:

1. Automatically evaluate all 5 dimensions
2. Provide numerical scores (1-10 scale)
3. Identify specific issues in each dimension
4. Suggest concrete improvements
5. Generate a prioritized action plan

## 常见模式

### Document Quality Assessment
- Requirements documents
- Technical specifications
- User documentation
- Project proposals

### Communication Analysis
- Email effectiveness
- Meeting summaries
- Status reports
- Stakeholder communications

### Content Optimization
- Web content quality
- Training materials
- Knowledge base articles
- API documentation
'''
        
        with open(skill_dir / "SKILL.md", 'w', encoding='utf-8') as f:
            f.write(skill_content)
            
        print("✓ 创建技能: context-analyzer")
    
    def create_context_optimizer_skill(self):
        """创建上下文优化技能"""
        skill_dir = self.skills_dir / "context-optimizer"
        skill_dir.mkdir(exist_ok=True)
        
        # 创建子目录
        for subdir in ['examples', 'tools', 'resources', 'reference']:
            (skill_dir / subdir).mkdir(exist_ok=True)
        
        # 创建SKILL.md
        skill_content = '''---
name: context-optimizer
description: Optimizes context quality using AI-driven improvements based on specific goals. Use when you need to enhance clarity, improve relevance, fill information gaps, resolve inconsistencies, or increase information efficiency.
license: MIT
compatibility: Claude Code, VS Code, and any Agent Skills compatible environment
metadata:
  author: DNASPEC Team
  version: "2.0.0"
  category: optimization
  supported_goals: [clarity, relevance, completeness, consistency, efficiency]
  optimization_methods: [ai_rewrite, information_addition, structure_reorganization, terminology_standardization]
---

# Context Optimizer Skill

The Context Optimizer skill enhances text quality through AI-driven improvements based on specified optimization goals. It combines natural language processing with domain-specific optimization techniques to significantly improve context effectiveness.

## Optimization Goals

### 1. Clarity Enhancement (清晰度增强)

Focuses on making content more understandable and unambiguous.

**Techniques:**
- Simplifying complex sentence structures
- Clarifying ambiguous expressions
- Improving logical flow
- Standardizing terminology

### 2. Relevance Improvement (相关性提升)

Aligns content more closely with its intended purpose and audience.

**Techniques:**
- Refocusing content on key topics
- Adjusting language for target audience
- Emphasizing goal-relevant information
- Removing off-topic content

### 3. Completeness Fulfillment (完整性完善)

Fills information gaps and ensures comprehensive coverage.

**Techniques:**
- Identifying missing information
- Adding necessary context
- Expanding insufficient explanations
- Including relevant examples

### 4. Consistency Resolution (一致性解决)

Eliminates contradictions and ensures internal coherence.

**Techniques:**
- Standardizing terminology usage
- Resolving logical contradictions
- Ensuring temporal consistency
- Harmonizing conflicting statements

### 5. Efficiency Optimization (效率优化)

Improves information density and presentation efficiency.

**Techniques:**
- Eliminating redundancy
- Improving information organization
- Enhancing conciseness
- Optimizing cognitive load

## 工作流程

1. **Goal Specification**: Identify specific optimization objectives
2. **Quality Assessment**: Analyze current context quality
3. **Issue Identification**: Pinpoint areas needing improvement
4. **Optimization Application**: Apply AI-driven improvements
5. **Quality Validation**: Verify optimization effectiveness
6. **Result Delivery**: Provide optimized context with changes

## 关键决策点

- **Goal Prioritization**: Which optimization goals are most critical
- **Change Scope**: Conservative vs. aggressive optimization
- **Style Preservation**: How much to maintain original style
- **Validation Standards**: Criteria for successful optimization

## 基本使用方法

Provide context and specify optimization goals. The skill will:

1. Analyze current quality across all dimensions
2. Identify specific improvement opportunities
3. Apply targeted optimizations based on goals
4. Preserve essential meaning and style
5. Deliver improved context with change tracking

## 常见模式

### Document Enhancement
- Requirements specification optimization
- Technical document improvement
- User manual enhancement
- Business proposal refinement

### Communication Optimization
- Email clarity improvement
- Report summary optimization
- Presentation content enhancement
- Stakeholder communication refinement

### Content Upgrading
- Web content optimization
- Documentation improvement
- Training material enhancement
- Knowledge base refinement
'''
        
        with open(skill_dir / "SKILL.md", 'w', encoding='utf-8') as f:
            f.write(skill_content)
            
        print("✓ 创建技能: context-optimizer")
    
    def update_cognitive_templater_skill(self):
        """更新认知模板技能"""
        skill_dir = self.skills_dir / "cognitive-templater"
        skill_dir.mkdir(exist_ok=True)
        
        # 创建子目录
        for subdir in ['examples', 'tools', 'resources', 'reference']:
            (skill_dir / subdir).mkdir(exist_ok=True)
        
        # SKILL.md已存在，检查是否需要更新
        if (skill_dir / "SKILL.md").exists():
            print("✓ 技能已存在: cognitive-templater")
        else:
            print("❌ 技能缺失: cognitive-templater")
    
    def create_architect_variants(self):
        """创建架构师技能变体"""
        variants = [
            {
                "name": "simple-architect",
                "description": "Provides simple architecture design for basic projects. Use when you need quick, straightforward architecture solutions for small-scale applications.",
                "content": '''# Simple Architect Skill

Provides quick and straightforward architecture design solutions for basic projects and small-scale applications.

## 工作流程

1. **Requirement Analysis**: Understand basic project requirements
2. **Simple Architecture**: Design straightforward architecture
3. **Technology Selection**: Choose appropriate basic technologies
4. **Structure Planning**: Plan basic project structure
5. **Implementation Guide**: Provide simple implementation steps

## 关键决策点

- Project complexity assessment
- Technology stack appropriateness
- Resource availability considerations
- Timeline feasibility

## 基本使用方法

Describe your basic project requirements and I'll provide:
- Simple architecture diagram
- Basic technology recommendations
- Straightforward project structure
- Easy-to-follow implementation guide

## 常见模式

- Personal projects
- Small business applications
- Prototype development
- Learning projects
'''
            },
            {
                "name": "system-architect",
                "description": "Provides advanced system architecture design and detailed specifications. Use when you need comprehensive, scalable, and robust architecture solutions for complex systems.",
                "content": '''# System Architect Skill

Delivers comprehensive and advanced architecture design for complex systems requiring scalability, robustness, and detailed technical specifications.

## 工作流程

1. **Comprehensive Analysis**: Deep analysis of system requirements and constraints
2. **Advanced Architecture**: Design sophisticated multi-tier architecture
3. **Scalability Planning**: Plan for horizontal and vertical scaling
4. **Security Design**: Implement comprehensive security architecture
5. **Performance Optimization**: Design for optimal performance
6. **Detailed Specifications**: Create comprehensive technical documentation

## 关键决策点

- Scalability requirements analysis
- Security architecture design
- Performance optimization strategies
- Integration complexity management
- Technology stack selection

## 基本使用方法

Provide detailed system requirements and I'll deliver:
- Comprehensive architecture design
- Detailed technical specifications
- Scalability and security plans
- Performance optimization strategies
- Implementation roadmap

## 常见模式

- Enterprise systems
- Large-scale web applications
- Distributed systems
- Mission-critical applications
'''
            }
        ]
        
        for variant in variants:
            skill_dir = self.skills_dir / variant["name"]
            skill_dir.mkdir(exist_ok=True)
            
            # 创建子目录
            for subdir in ['examples', 'tools', 'resources', 'reference']:
                (skill_dir / subdir).mkdir(exist_ok=True)
            
            # 创建SKILL.md
            skill_content = f'''---
name: {variant["name"]}
description: {variant["description"]}
license: MIT
compatibility: Claude Code, VS Code, and any Agent Skills compatible environment
metadata:
  author: DNASPEC Team
  version: "2.0.0"
  category: design
  supported_complexities: ["basic", "intermediate", "advanced"]
  architecture_types: ["monolithic", "microservices", "distributed", "hybrid"]
---

{variant["content"]}
'''
            
            with open(skill_dir / "SKILL.md", 'w', encoding='utf-8') as f:
                f.write(skill_content)
                
            print(f"✓ 创建技能: {variant['name']}")
    
    def run_complete_alignment(self):
        """运行完整的对齐流程"""
        print("开始完整的DNASPEC技能对齐...")
        
        try:
            # 1. 更新配置文件
            self.update_config_file()
            
            # 2. 创建缺失的技能
            self.create_context_analyzer_skill()
            self.create_context_optimizer_skill()
            
            # 3. 检查现有技能
            self.update_cognitive_templater_skill()
            
            # 4. 创建架构师技能变体
            self.create_architect_variants()
            
            print("\n✅ 完整技能对齐完成!")
            
            # 验证结果
            self.verify_alignment()
            
        except Exception as e:
            print(f"❌ 对齐过程中出现错误: {e}")
            raise
    
    def verify_alignment(self):
        """验证对齐结果"""
        print("\n🔍 验证对齐结果...")
        
        # 读取配置文件
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        config_skills = [skill['name'].replace('dnaspec-', '') for skill in config['skills']]
        existing_skills = []
        
        # 检查实际技能目录
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                existing_skills.append(skill_dir.name)
        
        print(f"配置文件技能数量: {len(config_skills)}")
        print(f"实际技能目录数量: {len(existing_skills)}")
        
        missing = set(config_skills) - set(existing_skills)
        extra = set(existing_skills) - set(config_skills)
        
        if missing:
            print(f"❌ 仍缺失技能: {sorted(missing)}")
        else:
            print("✅ 所有配置技能都已创建")
            
        if extra:
            print(f"ℹ️  额外技能: {sorted(extra)}")


if __name__ == "__main__":
    project_root = "."
    aligner = CompleteSkillAlignmentTool(project_root)
    aligner.run_complete_alignment()