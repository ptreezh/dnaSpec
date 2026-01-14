# Task Decomposer - 高级应用

## 核心能力

处理最复杂的任务分解场景，包括大规模项目、跨系统集成、多智能体协作等。

## 高级分解场景

### 场景1：大规模系统重构

**背景**：将单体应用重构为微服务架构，涉及数百个模块。

**策略**：分阶段、渐进式重构

```json
{
  "decomposition_strategy": "phased_refactoring",
  "phases": [
    {
      "phase": "绞杀者模式（Strangler Fig）",
      "description": "逐步替换单体应用模块",
      "tasks": [
        {
          "id": "001",
          "name": "identify-boundaries",
          "description": "识别服务边界",
          "type": "analysis",
          "workspace": "task-001-identify-boundaries/",
          "context": {
            "methodology": "领域驱动设计（DDD）",
            "artifacts": ["领域模型", " bounded上下文图", "服务边界建议"],
            "tools": ["依赖分析工具", "代码分析工具"]
          },
          "output": {
            "service_boundaries": [
              {"service": "user-service", "modules": ["auth", "profile", "permissions"]},
              {"service": "order-service", "modules": ["cart", "checkout", "payment"]},
              {"service": "catalog-service", "modules": ["products", "categories", "search"]}
            ]
          }
        },
        {
          "id": "002",
          "name": "establish-migration-layer",
          "description": "建立迁移层（API Gateway）",
          "type": "infrastructure",
          "workspace": "task-002-migration-layer/",
          "dependencies": ["001"],
          "context": {
            "pattern": "绞杀者模式",
            "components": [
              "API Gateway：路由新老系统",
              "Facade层：统一接口",
              "代理层：转发请求"
            ],
            "migration_strategy": "按功能逐个迁移"
          }
        }
      ]
    },
    {
      "phase": "双写阶段（Dual-Write）",
      "description": "新老系统同时写，逐步读迁移",
      "tasks": [
        {
          "id": "003",
          "name": "implement-dual-write",
          "description": "实现双写逻辑",
          "type": "implementation",
          "workspace": "task-003-dual-write/",
          "context": {
            "pattern": "双写模式",
            "write_flow": [
              "1. 写入老系统",
              "2. 异步写入新系统",
              "3. 记录写入差异",
              "4. 定期对账数据"
            ],
            "rollback_plan": "新系统失败时，只写老系统"
          }
        },
        {
          "id": "004",
          "name": "migrate-read-traffic",
          "description": "逐步迁移读流量",
          "type": "migration",
          "workspace": "task-004-read-migration/",
          "dependencies": ["003"],
          "context": {
            "strategy": "灰度发布",
            "phases": [
              "阶段1：5%流量到新系统",
              "阶段2：20%流量到新系统",
              "阶段3：50%流量到新系统",
              "阶段4：100%流量到新系统"
            ],
            "monitoring": "实时监控错误率、延迟、一致性"
          }
        }
      ]
    },
    {
      "phase": "拆分验证",
      "description": "验证服务独立性",
      "tasks": [
        {
          "id": "005",
          "name": "isolation-verification",
          "description": "验证服务隔离性",
          "type": "testing",
          "workspace": "task-005-isolation-verification/",
          "context": {
            "tests": [
              "数据库隔离测试",
              "API独立性测试",
              "部署隔离测试",
              "故障隔离测试"
            ],
            "success_criteria": {
              "database_isolation": "每个服务有独立数据库",
              "api_independence": "服务间通过API通信",
              "deployment_independence": "可独立部署",
              "failure_isolation": "单个服务故障不影响其他服务"
            }
          }
        }
      ]
    }
  ],
  "risk_mitigation": {
    "rollback_plan": "每阶段都有回滚方案",
    "data_consistency": "双写期间保证数据一致性",
    "performance_impact": "监控性能，及时调整"
  }
}
```

**关键点**：
- 渐进式重构：不是一次性全部重构
- 绞杀者模式：逐步替换老系统
- 双写阶段：保证数据一致性
- 灰度发布：逐步迁移流量
- 风险控制：每阶段可回滚

### 场景2：多智能体系统任务分解

**背景**：需要多个智能体协作完成复杂任务。

**策略**：局部智能体 + 轻量级协调器

```json
{
  "multi_agent_system": {
    "architecture": "orchestrator_pattern",
    "components": [
      {
        "role": "主协调器（Orchestrator）",
        "component": {
          "id": "orchestrator",
          "type": "coordinator",
          "workspace": "coordinators/project-coordinator/",
          "context": {
            "responsibilities": [
              "任务分发",
              "结果聚合",
              "错误处理",
              "进度追踪"
            ],
            "local_context": "只包含协调信息（< 1000 tokens）",
            "communication": {
              "protocol": "REST API",
              "format": "JSON",
              "timeout": "30s per agent"
            }
          },
          "coordination_logic": {
            "task_distribution": "将大任务分解为子任务",
            "agent_selection": "根据能力选择合适的智能体",
            "result_aggregation": "聚合各智能体的结果",
            "error_handling": "智能体失败时的降级策略"
          }
        }
      },
      {
        "role": "局部智能体1：代码审查智能体",
        "component": {
          "id": "code-review-agent",
          "type": "local_agent",
          "workspace": "agents/code-review/",
          "context": {
            "capability": "代码质量分析",
            "local_context": "只包含代码审查规则（2000 tokens）",
            "interface": "POST /api/agents/code-review/check",
            "input": {"code_files": "待审查的代码"},
            "output": {"review_report": "审查报告"}
          },
          "isolation": {
            "context_isolated": true,
            "workspace_isolated": true,
            "failure_isolated": true
          }
        }
      },
      {
        "role": "局部智能体2：测试覆盖率智能体",
        "component": {
          "id": "test-coverage-agent",
          "type": "local_agent",
          "workspace": "agents/test-coverage/",
          "context": {
            "capability": "测试覆盖率分析",
            "local_context": "只包含测试标准（1500 tokens）",
            "interface": "POST /api/agents/test-coverage/check",
            "input": {"project_path": "项目路径"},
            "output": {"coverage_report": "覆盖率报告"}
          }
        }
      },
      {
        "role": "局部智能体3：依赖健康智能体",
        "component": {
          "id": "dependency-health-agent",
          "type": "local_agent",
          "workspace": "agents/dependency-health/",
          "context": {
            "capability": "依赖安全性检查",
            "local_context": "只包含安全策略（1800 tokens）",
            "interface": "POST /api/agents/dependency-health/check",
            "input": {"dependencies": "依赖列表"},
            "output": {"health_report": "健康报告"}
          }
        }
      }
    ],
    "workflow": {
      "step1": "主协调器接收项目健康检查请求",
      "step2": "协调器分解为3个子任务",
      "step3": "并行调用3个局部智能体",
      "step4": "每个智能体在独立上下文中执行",
      "step5": "协调器聚合结果",
      "step6": "生成综合健康报告"
    },
    "multi_layer_alignment": {
      "protocol": "REST/JSON（统一）",
      "error_format": '{"error": "...", "message": "..."}',
      "timeout": "30s (协调器) → 10s (各智能体)",
      "retry": "1次（统一）"
    },
    "performance_metrics": {
      "context_reduction": "98% (从全局100k tokens降到局部2k tokens)",
      "response_time": "10x faster (并行执行)",
      "failure_isolation": "单个智能体失败不影响其他"
    }
  }
}
```

**关键点**：
- 局部智能体：每个智能体有独立的局部上下文
- 轻量级协调器：只负责任务分发和结果聚合
- 上下文隔离：防止上下文膨胀（98%减少）
- 接口对齐：统一的通信协议和错误处理
- 失败隔离：单个智能体失败不影响其他

### 场景3：跨系统集成任务分解

**背景**：需要整合多个外部系统和服务。

**策略**：适配器模式 + 服务网格

```json
{
  "cross_system_integration": {
    "systems": [
      {
        "id": "external-system-A",
        "name": "支付网关系统",
        "type": "external",
        "integration_pattern": "adapter",
        "tasks": [
          {
            "id": "001",
            "name": "payment-gateway-adapter",
            "description": "实现支付网关适配器",
            "workspace": "task-001-payment-adapter/",
            "context": {
              "responsibility": "隔离外部支付网关的复杂性",
              "interface": "统一的支付接口",
              "implements": [
                "协议转换：外部API → 内部API",
                "错误映射：外部错误 → 内部错误",
                "重试逻辑：处理外部系统故障"
              ],
              "external_system": {
                "api": "https://payment-gateway.example.com/api",
                "authentication": "API Key + HMAC",
                "rate_limit": "100 req/min",
                "timeout": "10s"
              }
            },
            "isolation": {
              "context": "只包含适配逻辑",
              "dependencies": ["external SDK", "circuit breaker"]
            }
          }
        ]
      },
      {
        "id": "external-system-B",
        "name": "物流追踪系统",
        "type": "external",
        "integration_pattern": "adapter",
        "tasks": [
          {
            "id": "002",
            "name": "logistics-adapter",
            "description": "实现物流追踪适配器",
            "workspace": "task-002-logistics-adapter/",
            "context": {
              "interface": "统一的物流接口",
              "protocols": ["REST", "SOAP", "FTP"],
              "data_formats": ["JSON", "XML", "CSV"]
            }
          }
        ]
      },
      {
        "id": "external-system-C",
        "name": "CRM系统",
        "type": "external",
        "integration_pattern": "adapter",
        "tasks": [
          {
            "id": "003",
            "name": "crm-adapter",
            "description": "实现CRM适配器",
            "workspace": "task-003-crm-adapter/",
            "context": {
              "interface": "统一的CRM接口",
              "synchronization": "双向数据同步",
              "conflict_resolution": "最后写入优先"
            }
          }
        ]
      }
    ],
    "service_mesh": {
      "orchestration": {
        "component": "integration-coordinator",
        "workspace": "coordinators/integration/",
        "context": {
          "responsibility": "协调多个适配器",
          "patterns": [
            "编排模式：按顺序调用多个适配器",
            "编目模式：并行调用多个适配器"
          ]
        }
      },
      "resilience": {
        "circuit_breaker": {
          "pattern": "熔断器",
          "threshold": "连续失败5次后打开熔断器",
          "recovery": "30秒后半开状态尝试恢复"
        },
        "retry": {
          "strategy": "指数退避",
          "max_attempts": 3,
          "backoff": "2^n 秒"
        },
        "timeout": {
          "external_system_A": "10s",
          "external_system_B": "15s",
          "external_system_C": "8s"
        }
      }
    },
    "data_consistency": {
      "strategy": "最终一致性",
      "mechanisms": [
        "事件溯源（Event Sourcing）",
        "CQRS（命令查询责任分离）",
        "Saga模式（分布式事务）"
      ]
    }
  }
}
```

**关键点**：
- 适配器模式：隔离外部系统复杂性
- 统一接口：内部系统使用统一的API
- 弹性设计：熔断器、重试、超时
- 数据一致性：最终一致性、Saga模式

## 上下文爆炸预防

### 预防机制

```yaml
context_explosion_prevention:
  mechanism_1_size_limits:
    atomic_task: "< 5000 tokens"
    ai_agent: "< 3000 tokens"
    coordinator: "< 1000 tokens"
    action: "超过限制时压缩或分解"

  mechanism_2_information_layering:
    layer_1_core: "必需信息（任务ID、目标、输入输出）"
    layer_2_constraints: "约束条件、依赖关系"
    layer_3_details: "实现细节、参考资料"
    loading_strategy: "按需加载"

  mechanism_3_context_compression:
    technique: "LLM-based compression"
    trigger: "上下文 > 4000 tokens"
    target: "压缩到 < 2000 tokens"
    preservation: "保留关键信息，删除冗余"

  mechanism_4_reference_instead_of_embed:
    principle: "不嵌入大文件，只引用文件路径"
    implementation: "需要时再读取文件内容"
    benefit: "减少上下文大小"
```

### 上下文压缩算法

```python
# 伪代码：智能上下文压缩
def compress_context(context, target_tokens):
    """
    智能压缩上下文到目标token数
    """
    current_tokens = count_tokens(context)

    if current_tokens <= target_tokens:
        return context  # 不需要压缩

    # 压缩策略1：删除冗余信息
    compressed = remove_redundancy(context)
    if count_tokens(compressed) <= target_tokens:
        return compressed

    # 压缩策略2：总结详细信息
    compressed = summarize_details(compressed)
    if count_tokens(compressed) <= target_tokens:
        return compressed

    # 压缩策略3：提取关键要点
    compressed = extract_key_points(compressed)
    if count_tokens(compressed) <= target_tokens:
        return compressed

    # 压缩策略4：使用LLM重写
    compressed = llm_rewrite(compressed, target_tokens)
    return compressed
```

## 复杂依赖管理

### 依赖环检测

```python
# 伪代码：检测循环依赖
def detect_circular_dependencies(tasks):
    """
    使用深度优先搜索检测循环依赖
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {task.id: WHITE for task in tasks}
    cycles = []

    def dfs(task):
        color[task.id] = GRAY
        for dep_id in task.dependencies:
            if color[dep_id] == GRAY:
                # 发现环
                cycles.append(f"环：{dep_id} -> {task.id}")
            elif color[dep_id] == WHITE:
                dfs(tasks[dep_id])
        color[task.id] = BLACK

    for task in tasks:
        if color[task.id] == WHITE:
            dfs(task)

    return {
        "has_cycles": len(cycles) > 0,
        "cycles": cycles
    }
```

### 依赖优化

```yaml
dependency_optimization:
  parallelization:
    strategy: "识别可并行执行的任务"
    algorithm: "拓扑排序 + 关键路径分析"
    benefit: "减少总执行时间"

  breaking_cycles:
    strategy: "引入中间任务打破循环依赖"
    example: "A → B → C → A 变为 A → M ← B → C → A"
    where: "M是中间协调任务"

  leveling:
    strategy: "分层执行，减少跨层依赖"
    layers:
      - layer_1: "无依赖的任务"
      - layer_2: "只依赖layer_1的任务"
      - layer_3: "只依赖layer_2的任务"
```

## 实时任务追踪

### 状态监控

```json
{
  "task_monitoring": {
    "states": [
      "pending：等待执行",
      "in_progress：正在执行",
      "completed：成功完成",
      "failed：执行失败",
      "blocked：被依赖阻塞",
      "cancelled：已取消"
    ],
    "metrics": {
      "total_tasks": 100,
      "completed": 45,
      "in_progress": 10,
      "pending": 35,
      "failed": 5,
      "blocked": 5,
      "completion_rate": "45%",
      "estimated_remaining_time": "8 hours"
    },
    "real_time_updates": {
      "webhook": "POST /api/tasks/{id}/status",
      "websocket": "ws://api/tasks/stream",
      "polling": "GET /api/tasks/status (每10秒)"
    }
  }
}
```

### 动态调整

```python
# 伪代码：动态任务调整
def dynamic_adjustment(current_state):
    """
    根据当前状态动态调整任务执行计划
    """
    # 情况1：任务失败
    if current_state.failed_tasks > threshold:
        # 启动备用任务
        activate_backup_tasks()

    # 情况2：任务耗时超出预期
    if current_state.slow_tasks:
        # 重新分配资源
        rebalance_resources()

    # 情况3：发现可并行执行的任务
    if current_state.new_parallelizable_tasks:
        # 并行执行
        execute_parallel()

    # 情况4：依赖提前完成
    if current_state.dependencies_completed_early:
        # 提前开始阻塞任务
        unblock_tasks()
```

## 质量保证

### 自动化测试

```yaml
testing_strategy:
  unit_tests:
    scope: "测试单个任务逻辑"
    coverage: "> 80%"

  integration_tests:
    scope: "测试任务间交互"
    scenarios: [
      "依赖任务完成检查",
      "数据流验证",
      "错误传播测试"
    ]

  performance_tests:
    metrics: [
      "任务执行时间",
      "内存使用",
      "上下文大小"
    ]
    thresholds: {
      "task_execution": "< 30s",
      "memory_usage": "< 1GB",
      "context_size": "< 5000 tokens"
    }
```

### 持续改进

```python
# 伪代码：持续改进循环
def continuous_improvement():
    """
    持续改进任务分解策略
    """
    # 收集执行数据
    execution_data = collect_task_executions()

    # 分析模式
    patterns = analyze_patterns(execution_data)

    # 识别问题
    issues = identify_issues(patterns)

    # 生成改进建议
    improvements = suggest_improvements(issues)

    # 应用改进
    apply_improvements(improvements)
```
