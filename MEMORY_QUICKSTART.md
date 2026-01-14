# DNASPEC 记忆系统 - 快速启动

## 3分钟快速开始

### 1. 初始化系统

```bash
# 运行初始化脚本
python scripts/setup_memory.py
```

这将创建：
- `memory_storage/` - 记忆存储目录
- `memory_backups/` - 备份目录
- `config/memory_config.json` - 配置文件

### 2. 配置记忆启用

编辑 `config/memory_config.json`:

```json
{
  "skills": {
    "task-decomposer": {
      "enabled": true,   // 改为 true 启用
      "max_short_term": 50,
      "max_long_term": 200
    },
    "architect": {
      "enabled": true    // 改为 true 启用
    }
  }
}
```

### 3. 运行示例

```bash
# 运行CI项目助手示例
python examples/ci_project_helper.py
```

您将看到技能如何记住并利用项目经验！

## 常用命令

```bash
# 初始化
python scripts/setup_memory.py

# 备份记忆
python scripts/backup_memory.py

# 监控状态
python scripts/monitor_memory.py

# 快速查看统计
python scripts/monitor_memory.py --quick
```

## 代码示例

### 基础使用

```python
from skills.task_decomposer.skill import task_decomposer_skill
from dna_context_engineering.memory import create_task_decomposer_with_memory

# 创建带记忆的技能
decomposer = create_task_decomposer_with_memory(
    task_decomposer_skill,
    enable_memory=True
)

# 执行任务（自动记忆）
result = decomposer.execute({
    'input': '实现用户认证系统'
})

# 回顾历史
history = decomposer.recall_similar_decompositions('认证')
for memory in history:
    print(memory)
```

### 统一管理

```python
from dna_context_engineering.memory import SkillsMemoryManager

manager = SkillsMemoryManager()
manager.register_skill(decomposer)
manager.register_skill(architect)

# 清理所有
manager.cleanup_all_skills()

# 导出所有
from pathlib import Path
manager.export_all_memories(Path('backup'))
```

## 目录结构

```
your_project/
├── config/
│   └── memory_config.json       # 配置文件
├── memory_storage/              # 记忆存储（自动创建）
│   └── agents/
│       ├── task-decomposer_*/
│       └── architect_*/
├── memory_backups/              # 备份目录
├── scripts/
│   ├── setup_memory.py          # 初始化
│   ├── backup_memory.py         # 备份
│   ├── monitor_memory.py        # 监控
│   └── memory_config_loader.py  # 配置加载
├── examples/
│   └── ci_project_helper.py     # 示例
└── docs/
    └── PRODUCTION_MEMORY_GUIDE.md  # 完整指南
```

## 配置选项

### 全局设置

```json
{
  "global_settings": {
    "memory_enabled": true,        // 总开关
    "auto_cleanup": true,           // 自动清理
    "backup_enabled": true,         // 启用备份
    "backup_interval_hours": 24     // 备份间隔
  }
}
```

### 技能配置

```json
{
  "skills": {
    "task-decomposer": {
      "enabled": true,              // 启用记忆
      "max_short_term": 50,         // 短期记忆上限
      "max_long_term": 200,         // 长期记忆上限
      "auto_cleanup": true          // 自动清理
    }
  }
}
```

## 性能调优

### 轻量级配置

```json
{
  "max_short_term": 20,
  "max_long_term": 50
}
```

### 标准配置

```json
{
  "max_short_term": 50,
  "max_long_term": 200
}
```

### 重量级配置

```json
{
  "max_short_term": 100,
  "max_long_term": 500
}
```

## 监控和维护

### 日常监控

```bash
# 查看状态
python scripts/monitor_memory.py

# 输出示例:
# 技能数: 2, 记忆数: 150, 大小: 2.5 MB
# ✅ 大小正常
```

### 定期备份

```bash
# 手动备份
python scripts/backup_memory.py

# 或设置 cron 任务
0 2 * * * cd /path/to/project && python scripts/backup_memory.py
```

### 清理记忆

```python
# 在应用代码中
manager.cleanup_all_skills()
```

## 故障排除

### 记忆未保存

1. 检查是否启用: `"enabled": true`
2. 检查目录权限: `ls -la memory_storage/`
3. 查看存储路径: `"path": "./memory_storage"`

### 性能问题

1. 降低记忆上限
2. 启用自动清理: `"auto_cleanup": true`
3. 定期清理旧记忆

### 配置错误

```bash
# 验证JSON格式
python -m json.tool config/memory_config.json

# 重新初始化
python scripts/setup_memory.py
```

## 最佳实践

✅ **DO**
- 默认禁用，按需启用
- 设置合理的记忆上限
- 定期备份记忆
- 监控存储大小
- 启用自动清理

❌ **DON'T**
- 不检查就使用记忆
- 无限制记忆增长
- 忽略备份
- 混淆生产/开发配置

## 完整文档

📖 **生产环境部署指南**: `docs/PRODUCTION_MEMORY_GUIDE.md`

包含：
- 详细配置说明
- 部署脚本使用
- 性能优化建议
- 监控和运维
- 故障排除

## 支持

- 文档: `docs/PRODUCTION_MEMORY_GUIDE.md`
- 示例: `examples/ci_project_helper.py`
- 测试: `test_*.py`

---

**版本**: 1.0
**更新**: 2025-12-26
**状态**: ✅ 生产就绪
