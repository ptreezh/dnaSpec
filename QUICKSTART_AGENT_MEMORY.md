# Agent-Creator + 记忆系统 - 快速入门

## 5分钟快速开始

### 基础用法（不启用记忆）

```python
from skills.agent_creator.skill import agent_creator_skill
from dna_context_engineering.memory import create_agent_from_creator

# Step 1: 使用 agent-creator 创建智能体
result = agent_creator_skill.execute_skill({
    'agent_description': '数据分析专家'
})

# Step 2: 创建智能体实例（默认不启用记忆）
agent = create_agent_from_creator(result)

# Step 3: 执行任务
result = agent.execute_task('分析销售数据')
print(result['result'])  # ✅ 任务 '分析销售数据' 已由 数据分析专家 完成
```

### 启用记忆

```python
# 只需要一步：启用记忆
agent = create_agent_from_creator(result, enable_memory=True)

# 现在智能体会记住所有任务
agent.execute_task('分析Q1销售数据')
agent.execute_task('分析Q2销售数据')
agent.execute_task('分析Q3销售数据')

# 回顾相关历史
history = agent.recall_relevant_history('Q1')
for memory in history:
    print(memory)
# 输出:
# 执行任务: 分析Q1销售数据 ✅
# 结果: 任务 '分析Q1销售数据' 已完成
```

## 常见用例

### 用例1: 创建学习型助手

```python
# 创建一个从经验中学习的助手
agent = create_agent_from_creator(
    agent_creator_skill.execute_skill({
        'agent_description': 'Bug修复专家'
    }),
    enable_memory=True
)

# 执行一系列修复任务
bugs = ['登录bug', '数据库连接bug', 'API超时bug']
for bug in bugs:
    agent.execute_task(f'修复{bug}')

# 后续遇到类似bug时，可以回顾经验
similar = agent.recall_relevant_history('数据库')
print(f"找到 {len(similar)} 条相关经验")
```

### 用例2: 批量创建智能体

```python
from dna_context_engineering.memory import AgentMemoryIntegrator

integrator = AgentMemoryIntegrator()

# 创建多个智能体
configs = [
    {'id': 'analyst', 'role': '分析师', 'capabilities': ['分析']},
    {'id': 'writer', 'role': '写手', 'capabilities': ['写作']},
    {'id': 'reviewer', 'role': '审查员', 'capabilities': ['审查']}
]

for config in configs:
    integrator.create_agent_with_memory(config, enable_memory=False)

# 列出所有智能体
for agent_info in integrator.list_agents():
    print(f"{agent_info['agent_config']['role']}")
```

### 用例3: 导出和分析记忆

```python
# 执行任务后导出记忆
from pathlib import Path

agent = create_agent_from_creator(result, enable_memory=True)

# 执行多个任务
tasks = ['任务1', '任务2', '任务3']
for task in tasks:
    agent.execute_task(task)

# 导出记忆
integrator = AgentMemoryIntegrator()
integrator.agents[agent.agent_id] = agent
memory_data = integrator.export_agent_memory(
    agent.agent_id,
    output_path='agent_memory.json'
)

print(f"导出 {memory_data['stats']['total_memories']} 条记忆")
```

## 关键特性对比

| 特性 | 不启用记忆 | 启用记忆 |
|-----|----------|---------|
| **代码** | `AgentWithMemory(config)` | `AgentWithMemory(config, enable_memory=True)` |
| **基础功能** | ✅ 正常工作 | ✅ 正常工作 |
| **历史记录** | ❌ 无 | ✅ 有 |
| **学习能力** | ❌ 无 | ✅ 有 |
| **向后兼容** | ✅ 完全兼容 | ✅ 完全兼容 |
| **推荐场景** | 简单任务 | 学习/追踪 |

## 配置选项

### 记忆容量限制

```python
from dna_context_engineering.memory import MemoryConfig

# 默认配置
config = MemoryConfig(
    enabled=True,
    max_short_term=50,    # 短期记忆最大数量
    max_long_term=200,    # 长期记忆最大数量
    auto_cleanup=True     # 自动清理低价值记忆
)

agent = AgentWithMemory(agent_config, enable_memory=True, memory_config=config)
```

### 选择性记忆

```python
# 只记忆重要任务
important_tasks = ['关键修复', '安全更新']
normal_tasks = ['日常检查']

for task in important_tasks:
    agent.execute_task(task, remember_task=True)  # 记住

for task in normal_tasks:
    agent.execute_task(task, remember_task=False)  # 不记住
```

## 常用API

### 检查记忆状态

```python
if agent.has_memory:
    print("记忆已启用")
else:
    print("记忆未启用")
```

### 获取记忆统计

```python
stats = agent.memory_manager.get_stats(agent.agent_id)
print(f"总记忆数: {stats['total_memories']}")
print(f"短期记忆: {stats['short_term_count']}")
print(f"长期记忆: {stats['long_term_count']}")
```

### 清理记忆

```python
# 自动清理（保留重要记忆）
remaining = agent.cleanup_memory()
print(f"清理后剩余 {remaining} 条记忆")
```

## 注意事项

### ✅ DO (推荐做法)

1. **默认禁用记忆**
   ```python
   agent = AgentWithMemory(config)  # 默认安全
   ```

2. **按需启用**
   ```python
   agent = AgentWithMemory(config, enable_memory=True)  # 明确需要时
   ```

3. **定期清理**
   ```python
   agent.cleanup_memory()  # 防止记忆膨胀
   ```

4. **检查状态**
   ```python
   if agent.has_memory:  # 始终检查
       # 使用记忆功能
   ```

### ❌ DON'T (避免做法)

1. ❌ 不检查就使用记忆
   ```python
   # 错误：可能导致空列表
   history = agent.recall_relevant_history('查询')
   ```

2. ❌ 无限制地记忆
   ```python
   # 错误：可能导致记忆爆炸
   for i in range(10000):
       agent.execute_task(f'任务{i}', remember_task=True)
   ```

3. ❌ 依赖记忆存在
   ```python
   # 错误：记忆可能未启用
   stats = agent.memory_manager.get_stats(id)  # 可能返回None
   ```

## 完整示例

```python
from skills.agent_creator.skill import agent_creator_skill
from dna_context_engineering.memory import (
    create_agent_from_creator,
    run_agent_with_memory_tracking
)

# 1. 创建智能体
result = agent_creator_skill.execute_skill({
    'agent_description': '性能优化专家'
})

# 2. 启用记忆
agent = create_agent_from_creator(result, enable_memory=True)

# 3. 执行任务并自动追踪
tasks = [
    '优化数据库查询',
    '缓存热点数据',
    '重构API层',
    '压缩前端资源'
]

results = run_agent_with_memory_tracking(
    agent,
    tasks,
    export_memory_path='performance_agent_memory.json'
)

# 4. 回顾经验
optimization_history = agent.recall_relevant_history('优化')
print(f"\n性能优化经验 ({len(optimization_history)} 条):")
for memory in optimization_history:
    print(f"  📝 {memory}")

# 5. 查看统计
stats = agent.memory_manager.get_stats(agent.agent_id)
print(f"\n记忆统计: {stats['total_memories']} 条")
```

## 下一步

- 📖 阅读完整文档: `AGENT_CREATOR_MEMORY_INTEGRATION.md`
- 📖 记忆系统详情: `MEMORY_SYSTEM_IMPLEMENTATION.md`
- 🧪 运行测试: `python test_agent_creator_memory_integration.py`

---

**提示**: 记忆功能默认禁用，只有显式设置 `enable_memory=True` 才会激活。这确保了向后兼容性和非侵入式设计。
