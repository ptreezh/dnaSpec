# Cognitive Templater Examples

## Example 1: Chain of Thought Template

### Input Problem
```
如何优化数据库查询性能？
```

### Expected Output
```json
{
  "problem": "如何优化数据库查询性能？",
  "selected_template": "chain_of_thought",
  "applied_steps": [
    {
      "step": 1,
      "name": "Problem Understanding",
      "action": "Analyze problem components and requirements",
      "result": "寻求方法或步骤的问题"
    },
    {
      "step": 2,
      "name": "Problem Decomposition", 
      "action": "Break down into logical sub-problems",
      "result": ["数据库查询", "性能优化"]
    },
    {
      "step": 3,
      "name": "Intermediate Reasoning",
      "action": "Reason through each sub-problem step by step", 
      "result": "针对数据库查询、性能优化进行逐步分析和推理"
    },
    {
      "step": 4,
      "name": "Solution Verification",
      "action": "Verify final solution against requirements",
      "result": "解决方案符合问题要求，逻辑一致"
    }
  ],
  "structured_output": "## 思维链分析\n\n**问题**: 如何优化数据库查询性能？\n\n### 1. Problem Understanding\n**操作**: Analyze problem components and requirements\n**结果**: 寻求方法或步骤的问题\n\n### 2. Problem Decomposition\n**操作**: Break down into logical sub-problems\n**结果\": [\"数据库查询\", \"性能优化\"]\n\n### 3. Intermediate Reasoning\n**操作**: Reason through each sub-problem step by step\n**结果**: 针对数据库查询、性能优化进行逐步分析和推理\n\n### 4. Solution Verification\n**操作**: Verify final solution against requirements\n**结果**: 解决方案符合问题要求，逻辑一致",
  "confidence_score": 0.85,
  "reasoning_path": [
    "理解问题: 寻求方法或步骤的问题",
    "分解为: [\"数据库查询\", \"性能优化\"]", 
    "逐步推理...",
    "验证结果: 解决方案符合问题要求，逻辑一致"
  ],
  "validation_results": {
    "completeness": true,
    "logical_flow": true,
    "quality_score": 0.8
  }
}
```

## Example 2: Verification Template

### Input Problem
```
检查这个用户认证系统的安全性
```

### Expected Output
```json
{
  "problem": "检查这个用户认证系统的安全性",
  "selected_template": "verification",
  "applied_steps": [
    {
      "step": 1,
      "name": "Assumption Analysis",
      "action": "Identify underlying assumptions", 
      "result": ["基本假设1", "基本假设2"]
    },
    {
      "step": 2,
      "name": "Logic Validation",
      "action": "Check logical consistency",
      "result": "逻辑一致，无明显矛盾"
    },
    {
      "step": 3,
      "name": "Evidence Evaluation",
      "action": "Assess supporting evidence",
      "result": "证据支持度中等"
    },
    {
      "step": 4,
      "name": "Alternative Consideration",
      "action": "Explore alternative solutions",
      "result": ["方案1", "方案2"]
    }
  ],
  "structured_output": "## 验证分析\n\n**问题**: 检查这个用户认证系统的安全性\n\n验证步骤执行完成...",
  "confidence_score": 0.85,
  "reasoning_path": [
    "识别假设: [\"基本假设1\", \"基本假设2\"]",
    "逻辑验证: 逻辑一致，无明显矛盾",
    "证据评估: 证据支持度中等", 
    "替代方案: [\"方案1\", \"方案2\"]"
  ],
  "validation_results": {
    "completeness": true,
    "quality_score": 0.8
  }
}
```

## Example 3: Role-Playing Template

### Input Problem
```
从不同角度评估这个移动应用的用户体验
```

### Expected Output
```json
{
  "problem": "从不同角度评估这个移动应用的用户体验",
  "selected_template": "role_playing",
  "applied_steps": [
    {
      "step": 1,
      "name": "Role Definition",
      "action": "Define relevant perspectives and roles",
      "result": ["用户", "开发者", "管理者"]
    },
    {
      "step": 2,
      "name": "Perspective Taking",
      "action": "View problem from each role's viewpoint",
      "result": {
        "用户": "从用户角度：从不同角度评估这个移动应用的用户体验",
        "开发者": "从开发者角度：从不同角度评估这个移动应用的用户体验", 
        "管理者": "从管理者角度：从不同角度评估这个移动应用的用户体验"
      }
    },
    {
      "step": 3,
      "name": "Expertise Application",
      "action": "Apply role-specific knowledge and experience",
      "result": {
        "用户": "用户专业分析：从用户角度：从不同角度评估这个移动应用的用户体验",
        "开发者": "开发者专业分析：从开发者角度：从不同角度评估这个移动应用的用户体验",
        "管理者": "管理者专业分析：从管理者角度：从不同角度评估这个移动应用的用户体验"
      }
    },
    {
      "step": 4,
      "name": "Integration",
      "action": "Combine multiple perspectives into comprehensive solution",
      "result": "多角度综合分析结果"
    }
  ],
  "structured_output": "## 角色扮演分析\n\n**问题**: 从不同角度评估这个移动应用的用户体验\n\n多视角分析结果...",
  "confidence_score": 0.85,
  "reasoning_path": [
    "定义角色: [\"用户\", \"开发者\", \"管理者\"]",
    "采纳视角: [\"用户\", \"开发者\", \"管理者\"]",
    "应用专业知识...",
    "综合结果: 多角度综合分析结果"
  ]
}
```

## Example 4: Template Auto-Selection

### Input Problem
```
解释机器学习模型的原理
```

### Expected Output
```json
{
  "problem": "解释机器学习模型的原理",
  "selected_template": "understanding",
  "applied_steps": [
    {
      "step": 1,
      "name": "Concept Identification",
      "action": "Identify key concepts and terminology",
      "result": ["机器学习", "模型", "原理"]
    },
    {
      "step": 2,
      "name": "Relationship Mapping",
      "action": "Map relationships between concepts", 
      "result": {
        "机器学习": [],
        "模型": [],
        "原理": []
      }
    },
    {
      "step": 3,
      "name": "Context Analysis",
      "action": "Understand situational context and factors",
      "result": "上下文环境分析"
    },
    {
      "step": 4,
      "name": "Synthesis",
      "action": "Create comprehensive understanding",
      "result": "对3个概念的深度理解"
    }
  ],
  "confidence_score": 0.85,
  "reasoning_path": [
    "识别概念: [\"机器学习\", \"模型\", \"原理\"]",
    "映射关系: {\"机器学习\": [], \"模型\": [], \"原理\": []}",
    "上下文分析: 上下文环境分析",
    "综合理解: 对3个概念的深度理解"
  ]
}
```

## Usage Patterns

### Complex Problem Solving
使用Chain of Thought模板：
- 算法设计和优化
- 系统架构分析
- 复杂业务逻辑处理

### Quality Assurance
使用Verification模板：
- 代码审查
- 安全性检查
- 设计方案验证

### Pattern-Based Learning
使用Few-Shot模板：
- 类比问题解决
- 经验借鉴应用
- 模式识别任务

### Multi-Perspective Analysis
使用Role-Playing模板：
- 用户体验评估
- 系统设计评审
- 需求分析

### Concept Mastery
使用Understanding模板：
- 技术原理解释
- 知识整合学习
- 概念关系分析

### Template Combination
对于复杂任务，可以组合使用多个模板：
- Chain of Thought + Verification (解决+验证)
- Role-Playing + Understanding (多角度+深度)
- Few-Shot + Chain of Thought (借鉴+推理)