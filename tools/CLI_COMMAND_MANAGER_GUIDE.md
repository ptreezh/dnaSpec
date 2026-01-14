# DNASPEC CLI Command Manager 使用指南

## 概述

CLI Command Manager 是一个为 DNASPEC 项目设计的原子性命令部署管理工具，确保在多平台 AI CLI 环境中安全地部署和删除命令。

## 核心特性

### ✅ 原子性操作 (Atomic Operations)
- **全部成功或全部失败**：部署/删除操作要么完全成功，要么完全回滚
- **事务性保证**：每个操作都有唯一的事务 ID，支持完整的状态追踪

### 🔄 自动回滚机制
- 操作失败时自动恢复到之前的状态
- 支持手动回滚任何历史事务
- 备份文件自动管理

### 📊 事务追踪
- 所有操作都有详细的事务记录
- 支持事务状态查询
- 错误日志和备份路径记录

## 支持的平台

- **iflow**: iflow-cli
- **claude**: Claude Code CLI
- **copilot**: GitHub Copilot CLI
- **gemini**: Gemini CLI
- **qwen**: Qwen CLI
- **qodercli**: Qoder CLI
- **codebuddy**: CodeBuddy CLI

## 命令列表

1. `dnaspec-agent-creator`
2. `dnaspec-architect`
3. `dnaspec-cache-manager`
4. `dnaspec-constraint-generator`
5. `dnaspec-dapi-checker`
6. `dnaspec-git-operations`
7. `dnaspec-modulizer`
8. `dnaspec-task-decomposer`

## 使用方法

### 1. 部署命令到指定平台

```bash
# 部署到单个平台
python tools/cli_command_manager.py deploy --platforms iflow

# 部署到多个平台
python tools/cli_command_manager.py deploy --platforms iflow,claude,copilot

# 指定源目录
python tools/cli_command_manager.py deploy --platforms iflow --source ./archive_uncertain
```

**操作流程：**
1. 📦 创建备份（自动备份现有命令）
2. 📝 部署新命令
3. 🔍 验证部署
4. ✅ 标记事务完成

**如果任何步骤失败，自动回滚到备份状态。**

### 2. 从指定平台删除命令

```bash
# 删除命令（保留备份）
python tools/cli_command_manager.py remove --platforms iflow

# 删除命令（不保留备份）
python tools/cli_command_manager.py remove --platforms iflow,claude --no-backup
```

**操作流程：**
1. 📦 创建备份
2. 🗑️ 删除命令文件
3. 🔍 验证删除
4. 💾 保留或清理备份

### 3. 回滚事务

```bash
# 回滚指定的事务
python tools/cli_command_manager.py rollback --transaction-id abc123def456
```

### 4. 查看事务状态

```bash
# 查看所有事务状态
python tools/cli_command_manager.py status
```

**输出示例：**
```
📊 Transaction Status

✅ abc123def456
   Operation: deploy
   Platforms: iflow, claude
   Status: completed
   Time: 2025-12-25T10:30:45
   Backup: D:\DAIP\dnaSpec\.dnaspec\backups\backup_20251225_103045

❌ xyz789uvw012
   Operation: remove
   Platforms: iflow
   Status: failed
   Time: 2025-12-25T11:15:20
   Error: Validation failed: iflow command dnaspec-architect not found
   Backup: D:\DAIP\dnaSpec\.dnaspec\backups\backup_20251225_111520
```

## 原子性操作的重要性

### 问题场景

**之前的问题：**
```bash
# 手动删除命令
rm -rf .iflow/commands/*.md

# iflow-cli 启动失败！
# 因为配置中仍然期望这些命令存在
```

**为什么失败？**
- CLI 工具在启动时扫描 `.{platform}/commands/` 目录
- 删除文件后，CLI 可能因为找不到预期命令而崩溃
- 没有备份，无法恢复

### 解决方案

**使用 CLI Command Manager：**
```bash
python tools/cli_command_manager.py remove --platforms iflow
```

**原子性保证：**
1. ✅ 操作前自动备份
2. ✅ 验证删除结果
3. ✅ 失败时自动回滚
4. ✅ 完整的事务日志

## 事务生命周期

```
pending → completed
     ↓
  failed → rolled_back
```

### 状态说明

- **pending**: 操作正在执行
- **completed**: 操作成功完成
- **failed**: 操作失败（已自动回滚）
- **rolled_back**: 手动回滚完成

## 数据存储结构

```
.dnaspec/
├── transactions/           # 事务记录
│   ├── abc123def456.json  # 事务详情
│   └── xyz789uvw012.json
└── backups/               # 备份文件
    ├── backup_20251225_103045/
    │   ├── iflow/
    │   └── claude/
    └── backup_20251225_111520/
```

## 事务文件格式

```json
{
  "id": "abc123def456",
  "operation": "deploy",
  "platforms": ["iflow", "claude"],
  "timestamp": "2025-12-25T10:30:45.123456",
  "status": "completed",
  "backup_path": "D:\\DAIP\\dnaSpec\\.dnaspec\\backups\\backup_20251225_103045",
  "error": null
}
```

## 最佳实践

### 1. 始终使用工具进行操作

❌ **不推荐：**
```bash
# 手动复制/删除命令
cp archive_uncertain/.iflow/commands/* .iflow/commands/
rm .iflow/commands/*.md
```

✅ **推荐：**
```bash
# 使用 CLI Command Manager
python tools/cli_command_manager.py deploy --platforms iflow
python tools/cli_command_manager.py remove --platforms iflow
```

### 2. 批量操作前先测试

```bash
# 先在单个平台测试
python tools/cli_command_manager.py deploy --platforms iflow

# 验证成功后再批量部署
python tools/cli_command_manager.py deploy --platforms iflow,claude,copilot
```

### 3. 定期检查事务状态

```bash
# 定期查看历史事务
python tools/cli_command_manager.py status
```

### 4. 保留重要备份

```bash
# 删除时保留备份（默认行为）
python tools/cli_command_manager.py remove --platforms iflow

# 如需清理备份，手动删除过期备份
```

## 错误处理

### 部署失败示例

```bash
$ python tools/cli_command_manager.py deploy --platforms iflow

🚀 Starting atomic deployment to platforms: iflow
📦 Step 1: Creating backup...
✅ Backup created: .dnaspec/backups/backup_20251225_120000
📝 Step 2: Deploying commands...
  ✓ iflow/dnaspec-architect.md
  ✓ iflow/dnaspec-agent-creator.md
🔍 Step 3: Validating deployment...

❌ Deployment failed: Validation failed: iflow command dnaspec-constraint-generator not found
🔄 Rolling back...
✅ Rollback completed

Transaction ID: abc123def456
Status: failed
```

### 恢复步骤

1. 查看失败的事务
2. 检查错误原因
3. 修复问题（如补充缺失的命令文件）
4. 重新执行部署

## 集成到开发流程

### pre-commit 钩子

创建 `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# 验证命令部署状态
python tools/cli_command_manager.py status | grep -q "failed" && {
    echo "❌ 有失败的部署事务，请先处理"
    exit 1
}
```

### CI/CD 集成

```yaml
# .github/workflows/deploy-cli.yml
name: Deploy CLI Commands

on: [push, pull_request]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to iflow
        run: |
          python tools/cli_command_manager.py deploy --platforms iflow
          python tools/cli_command_manager.py status
```

## 故障排除

### Q: iflow-cli 仍然启动失败？

**A:**
1. 检查 `.iflow/commands/` 目录是否存在
2. 使用 `status` 命令检查最近的事务
3. 如果有失败的事务，执行回滚
4. 重新部署命令

### Q: 如何恢复到之前的版本？

**A:**
```bash
# 1. 查看历史事务，找到备份路径
python tools/cli_command_manager.py status

# 2. 手动恢复备份
cp -r .dnaspec/backups/backup_20251225_103045/iflow/.iflow/commands .iflow/
```

### Q: 备份占用太多空间？

**A:**
```bash
# 清理旧的备份（保留最近 10 个）
cd .dnaspec/backups
ls -t | tail -n +11 | xargs rm -rf
```

## 总结

CLI Command Manager 提供了：

✅ **原子性操作** - 全部成功或全部失败
✅ **自动回滚** - 失败时自动恢复
✅ **事务追踪** - 完整的操作历史
✅ **多平台支持** - 统一管理所有 AI CLI 平台
✅ **安全可靠** - 备份、验证、回滚三重保障

使用这个工具可以避免手动操作导致的配置不一致问题，确保 DNASPEC 技能在多个 AI CLI 平台上的稳定运行。
