# DNASPEC Workspace - 基础应用

## 工作区结构

### 标准工作区结构

```
task-{id}-{name}/
├─ context.md          # 独立上下文（核心）
├─ input/              # 输入文件
├─ output/             # 输出文件
├─ workspace/          # 临时工作空间
└─ metadata.json       # 任务元数据
```

### context.md 模板

```markdown
## 任务信息
- 任务ID: 001
- 任务名称: 用户认证设计
- 状态: pending

## 约束条件
- 技术栈: Node.js + JWT
- 安全要求: 加密存储
- 性能要求: 响应时间 < 100ms

## 输入
- [ ] 需求文档
- [ ] 技术规范

## 输出
- [ ] 认证API设计
- [ ] 数据库设计
- [ ] 安全方案

## 执行历史
（记录每次执行的输入输出）
```

## 工作区创建

### 创建命令

```bash
workspace create --task "用户认证设计" --id 001
```

### 自动创建

- 创建工作区目录
- 生成 context.md
- 创建 input/, output/, workspace/ 目录
- 生成 metadata.json

## 工作区状态

### 状态类型

```
pending      - 工作区已创建，任务未开始
in_progress  - 任务正在执行
completed    - 任务成功完成
failed       - 任务失败
archived     - 工作区已归档
```

### 状态查询

```bash
# 查看所有工作区状态
workspace status --all

# 查看特定工作区状态
workspace status --id 001
```

## 基础清理

### 清理已完成任务

```bash
workspace cleanup --status completed
```

### 清理临时文件

```bash
workspace cleanup --temp-only
```
