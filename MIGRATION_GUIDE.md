# DNASPEC 技能迁移指南

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
