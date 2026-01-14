# DNASPEC Workspace - 中级应用

## 上下文隔离机制

### 物理隔离

```yaml
directory_isolation:
  - 每个任务独立的目录
  - 独立的上下文文件
  - 独立的输入输出目录
  - 独立的临时工作空间

enforcement:
  - 禁止跨工作区文件引用
  - 禁止共享上下文文件
  - 禁止共享临时文件
```

### 逻辑隔离

```yaml
context_boundary:
  - 每个context.md只包含本任务信息
  - 通过输入文件传递外部信息
  - 通过输出文件返回结果
  - 任务间只通过明确定义的接口通信
```

## 上下文大小管理

### 大小限制

```
soft_limit: 3000 tokens   # 警告阈值
hard_limit: 5000 tokens   # 阻止阈值
```

### 监控和警告

```yaml
actions:
  warning (超过soft_limit):
    - 记录日志
    - 通知用户
    - 建议清理

  blocking (超过hard_limit):
    - 阻止执行
    - 强制清理
    - 上下文压缩
```

## 工作区生命周期

### 创建阶段

```yaml
creation:
  - 任务创建时生成工作区
  - 初始化context.md
  - 创建必要目录结构
  - 生成metadata.json
```

### 执行阶段

```yaml
execution:
  - 任务在工作区内执行
  - 所有操作限定在工作区内
  - 监控工作区大小
  - 更新状态为 in_progress
```

### 完成阶段

```yaml
completion:
  - 验证输出
  - 更新状态为 completed
  - 清理临时文件
  - 归档工作区
```

## 自动清理策略

### 成功任务清理

```yaml
on_success:
  - 清理 workspace/ 目录
  - 保留 output/ 关键文件
  - 压缩 context.md
  - 归档到 archives/
```

### 失败任务处理

```yaml
on_failure:
  - 保留所有文件用于调试
  - 标记工作区状态为 failed
  - 生成失败报告
  - 通知用户检查
```

### 定时清理

```yaml
scheduled:
  - 清理30天前完成的工作区
  - 压缩归档60天前的工作区
  - 删除90天前的归档
```

## 工作区嵌套

### 子任务工作区

```
task-001-user-module/
├─ context.md           # 原始任务上下文
├─ subtask-001-auth-api/
│   ├─ context.md       # 认证API子任务上下文
│   ├─ input/
│   ├─ output/
│   └─ workspace/
├─ subtask-002-session-management/
│   ├─ context.md       # 会话管理子任务上下文
│   └─ ...
└─ subtask-003-user-profile/
    ├─ context.md       # 用户档案子任务上下文
    └─ ...
```

### 分层隔离

```yaml
layered_isolation:
  - 主任务工作区
  - 子任务工作区
  - 每层上下文独立
  - 支持任务分解
```

## 隔离检查

### 目录隔离检查

```bash
workspace check --isolation --id 001
```

检查项：
- 工作区目录独立性
- 无跨工作区文件引用
- 无共享上下文文件

### 上下文隔离检查

检查项：
- context.md 只包含本任务信息
- 无外部上下文引用
- 上下文大小合理（< 5000 tokens）

### 运行时隔离检查

检查项：
- 任务在工作区内执行
- 无跨工作区文件操作
- 临时文件在工作区内
