# Task Decomposer - 中级场景

## 核心能力

将复杂需求分解为原子任务，每个任务有独立工作区，防止上下文爆炸。

## 复杂分解场景

### 场景1：AI辅助开发任务分解

**背景**：AI生成的代码需要独立的工作区和上下文管理。

**示例**：AI生成用户认证系统

```json
{
  "decomposition": {
    "root_task": "AI生成用户认证系统",
    "tasks": [
      {
        "id": "001",
        "name": "ai-generate-auth-code",
        "description": "AI生成用户认证代码",
        "type": "ai-assisted",
        "workspace": "task-001-ai-generate-auth-code/",
        "context": {
          "role": "AI代码生成助手",
          "capability": "生成登录、注册、密码重置代码",
          "local_context": "只包含认证规范和API设计（2000 tokens）",
          "input": ["认证需求.md"],
          "output": ["login.py", "register.py", "reset.py"]
        },
        "ai_config": {
          "model": "claude-3.5-sonnet",
          "max_tokens": 4000,
          "temperature": 0.3
        }
      },
      {
        "id": "002",
        "name": "review-ai-code",
        "description": "人工审查AI生成的代码",
        "type": "human-review",
        "workspace": "task-002-review-ai-code/",
        "dependencies": ["001"],
        "context": {
          "checklist": [
            "代码质量：符合编码规范",
            "安全性：无SQL注入、XSS漏洞",
            "功能完整性：覆盖所有需求",
            "测试覆盖率：> 80%"
          ]
        }
      }
    ]
  }
}
```

**关键点**：
- AI任务：限制上下文大小（< 2000 tokens）
- 审查任务：独立工作区，人工检查
- 失败隔离：AI失败不影响审查任务

### 场景2：微服务架构任务分解

**背景**：微服务需要独立部署和扩展。

**示例**：电商平台微服务化

```json
{
  "decomposition": {
    "architecture": "microservices",
    "tasks": [
      {
        "id": "001",
        "name": "user-service",
        "description": "用户服务微服务",
        "type": "microservice",
        "workspace": "task-001-user-service/",
        "context": {
          "responsibility": "用户管理、认证授权",
          "api_boundary": "POST /api/users/*",
          "database": "独立的PostgreSQL数据库",
          "deployment": "独立Docker容器"
        },
        "isolation": {
          "context_isolated": true,
          "database_isolated": true,
          "deployment_isolated": true
        }
      },
      {
        "id": "002",
        "name": "product-service",
        "description": "商品服务微服务",
        "type": "microservice",
        "workspace": "task-002-product-service/",
        "context": {
          "responsibility": "商品管理、库存管理",
          "api_boundary": "POST /api/products/*",
          "database": "独立的PostgreSQL数据库",
          "deployment": "独立Docker容器"
        }
      },
      {
        "id": "003",
        "name": "order-service",
        "description": "订单服务微服务",
        "type": "microservice",
        "workspace": "task-003-order-service/",
        "dependencies": ["001", "002"],
        "context": {
          "responsibility": "订单创建、支付处理",
          "api_boundary": "POST /api/orders/*",
          "integration": "调用user-service和product-service",
          "deployment": "独立Docker容器"
        }
      }
    ],
    "communication_protocol": {
      "format": "REST/JSON",
      "error_handling": "统一错误格式",
      "timeout": "30s",
      "retry": "最多3次"
    }
  }
}
```

**关键点**：
- 服务边界清晰：每个服务有明确职责
- 上下文隔离：每个服务独立数据库和部署
- 接口对齐：统一的通信协议
- 依赖管理：order-service依赖user和product服务

### 场景3：多阶段项目任务分解

**背景**：项目有明确的阶段划分。

**示例**：软件开发全流程

```json
{
  "decomposition": {
    "phases": [
      {
        "phase": "Idea阶段",
        "tasks": [
          {
            "id": "001",
            "name": "concept-validation",
            "description": "验证概念可行性",
            "type": "validation",
            "workspace": "task-001-concept-validation/",
            "context": {
              "input": ["用户想法"],
              "output": ["可行性报告"],
              "criteria": ["技术可行性", "市场需求", "资源评估"]
            },
            "is_atomic": true,
            "estimated_hours": 2
          }
        ]
      },
      {
        "phase": "需求阶段",
        "tasks": [
          {
            "id": "002",
            "name": "requirements-gathering",
            "description": "收集完整需求",
            "type": "analysis",
            "workspace": "task-002-requirements-gathering/",
            "dependencies": ["001"],
            "context": {
              "input": ["可行性报告", "用户访谈"],
              "output": ["需求规格说明书"],
              "techniques": ["用例分析", "用户故事", "验收标准"]
            }
          }
        ]
      },
      {
        "phase": "细化阶段",
        "tasks": [
          {
            "id": "003",
            "name": "technical-design",
            "description": "技术设计细化",
            "type": "design",
            "workspace": "task-003-technical-design/",
            "dependencies": ["002"],
            "subtasks": [
              {
                "id": "003-1",
                "name": "database-design",
                "description": "数据库设计",
                "workspace": "task-003-1-database-design/"
              },
              {
                "id": "003-2",
                "name": "api-design",
                "description": "API设计",
                "workspace": "task-003-2-api-design/"
              }
            ]
          }
        ]
      },
      {
        "phase": "智能阶段",
        "tasks": [
          {
            "id": "004",
            "name": "ai-agent-creation",
            "description": "创建局部智能体",
            "type": "ai-agent",
            "workspace": "task-004-ai-agent-creation/",
            "context": {
              "agent_type": "code-review-agent",
              "local_context": "代码审查规则（1500 tokens）",
              "capabilities": ["代码质量检查", "安全扫描"],
              "interface": "POST /api/agents/code-review/check"
            }
          }
        ]
      }
    ]
  }
}
```

**关键点**：
- 阶段明确：Idea→需求→细化→智能
- 依赖清晰：后阶段依赖前阶段
- 子任务支持：任务可以继续分解
- 全生命周期支持

## 上下文管理策略

### 策略1：上下文大小限制

```yaml
context_size_limits:
  atomic_task:
    soft_limit: 2000 tokens
    hard_limit: 5000 tokens
    action: "超过hard_limit时压缩上下文"

  ai_agent_task:
    recommended: 1500 tokens
    maximum: 3000 tokens
    reason: "AI智能体需要更小上下文以保持性能"

  compound_task:
    soft_limit: 3000 tokens
    hard_limit: 8000 tokens
    action: "分解为多个原子任务"
```

### 策略2：上下文分层

```
上下文分层结构：

context.md
├── # 核心信息（必需）
│   ├── 任务ID
│   ├── 任务名称
│   ├── 目标（1-2句话）
│   ├── 输入文件列表
│   └── 输出文件列表
│
├── ## 约束条件（必需）
│   ├── 技术约束
│   ├── 时间约束
│   └── 资源约束
│
├── ## 详细说明（可选）
│   ├── 实现细节
│   ├── 参考资料
│   └── 示例代码
│
└── ## 历史记录（可选）
    ├── 之前执行的结果
    ├── 遇到的问题
    └── 解决方案

分层读取策略：
- 快速执行：只读核心信息
- 正常执行：读取核心+约束
- 深度分析：读取全部
```

### 策略3：动态上下文加载

```python
# 伪代码：智能上下文加载
def load_context(task, mode):
    """
    根据执行模式加载适当的上下文

    mode:
    - minimal: 只加载核心信息（< 500 tokens）
    - standard: 加载核心+约束（< 2000 tokens）
    - full: 加载全部信息（< 5000 tokens）
    """

    if mode == "minimal":
        return {
            "task_id": task.id,
            "name": task.name,
            "goal": task.goal,
            "input": task.input_files,
            "output": task.output_files
        }
    elif mode == "standard":
        return {
            **load_context(task, "minimal"),
            "constraints": task.constraints,
            "dependencies": task.dependencies
        }
    else:  # full
        return {
            **load_context(task, "standard"),
            "details": task.details,
            "examples": task.examples,
            "history": task.history
        }
```

## 任务依赖管理

### 依赖类型

```yaml
dependency_types:
  sequential:
    description: "顺序依赖"
    example: "任务001必须在任务002之前完成"
    check: "task001.status == completed"

  parallel:
    description: "并行执行"
    example: "任务001和任务002可以同时进行"
    condition: "无共享资源"

  conditional:
    description: "条件依赖"
    example: "如果任务001成功，执行任务002；否则执行任务003"
    check: "if task001.success: task002 else: task003"

  data_dependency:
    description: "数据依赖"
    example: "任务002需要任务001的输出文件"
    check: "exists(task001.output/result.json)"
```

### 依赖验证

```python
# 伪代码：依赖验证
def validate_dependencies(task, all_tasks):
    """
    验证任务依赖是否满足
    """
    for dep_id in task.dependencies:
        dep_task = all_tasks[dep_id]

        # 检查依赖任务是否完成
        if dep_task.status != "completed":
            return False, f"依赖任务 {dep_id} 未完成"

        # 检查依赖任务的输出是否存在
        for output_file in dep_task.context.output:
            if not file_exists(output_file):
                return False, f"依赖输出文件 {output_file} 不存在"

    return True, "依赖检查通过"
```

## 执行计划生成

### 关键路径计算

```python
# 伪代码：关键路径分析
def calculate_critical_path(tasks):
    """
    计算任务执行的关键路径
    """
    # 构建依赖图
    graph = build_dependency_graph(tasks)

    # 使用拓扑排序找出最长路径
    longest_path = find_longest_path(graph)

    return {
        "critical_path": longest_path,
        "total_duration": sum(task.duration for task in longest_path),
        "parallelizable_tasks": count_parallelizable(tasks),
        "bottleneck_tasks": identify_bottlenecks(graph)
    }
```

### 资源分配建议

```json
{
  "resource_allocation": {
    "parallel_tasks": [
      {
        "tasks": ["001", "002", "003"],
        "reason": "无依赖关系",
        "assigned_to": ["开发者A", "开发者B", "开发者C"]
      }
    ],
    "sequential_tasks": [
      {
        "path": ["004", "005", "006"],
        "reason": "有数据依赖",
        "assigned_to": "开发者D",
        "estimated_duration": "3天"
      }
    ]
  }
}
```

## 质量保证检查

### 分解质量检查

```yaml
quality_checks:
  atomicity:
    - 每个任务能否独立完成？
    - 任务职责是否单一？

  isolation:
    - 每个任务是否有独立工作区？
    - 上下文是否隔离？

  completeness:
    - 是否覆盖所有需求？
    - 输入输出是否明确？

  feasibility:
    - 估算的工时是否合理？
    - 技术是否可行？

  optimality:
    - 是否有可以并行执行的任务？
    - 关键路径是否最短？
```

### 自动化验证

```python
# 伪代码：自动化质量检查
def validate_decomposition(decomposition):
    """
    验证任务分解的质量
    """
    results = []

    # 检查原子性
    for task in decomposition.tasks:
        if task.estimated_hours > 8:
            results.append({
                "level": "warning",
                "task": task.id,
                "message": "任务估算超过8小时，建议进一步分解"
            })

    # 检查工作区隔离
    workspaces = [task.workspace for task in decomposition.tasks]
    if len(workspaces) != len(set(workspaces)):
        results.append({
            "level": "error",
            "message": "存在重复的工作区名称"
        })

    # 检查依赖闭环
    if has_circular_dependency(decomposition.tasks):
        results.append({
            "level": "error",
            "message": "存在循环依赖"
        })

    return {
        "valid": all(r["level"] != "error" for r in results),
        "warnings": [r for r in results if r["level"] == "warning"],
        "errors": [r for r in results if r["level"] == "error"]
    }
```
