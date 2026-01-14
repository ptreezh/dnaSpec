# DNASPEC 记忆系统 - 生产环境部署指南

## 目录

1. [环境准备](#环境准备)
2. [配置管理](#配置管理)
3. [部署脚本](#部署脚本)
4. [实际使用场景](#实际使用场景)
5. [性能优化](#性能优化)
6. [监控和运维](#监控和运维)
7. [故障排除](#故障排除)

---

## 环境准备

### 1. 系统要求

- Python 3.8+
- 至少 100MB 可用磁盘空间（用于记忆存储）
- 建议内存：2GB+（取决于记忆数量）

### 2. 安装依赖

```bash
# 确认已安装 dnaspec
pip install -e .

# 验证安装
python -c "from dna_context_engineering.memory import MemoryManager; print('✅ 记忆系统已安装')"
```

### 3. 创建目录结构

```bash
# 项目根目录
your_project/
├── config/
│   └── memory_config.json       # 记忆配置
├── memory_storage/              # 记忆存储目录（自动创建）
├── logs/                        # 日志目录
├── scripts/
│   ├── setup_memory.py          # 初始化脚本
│   ├── backup_memory.py         # 备份脚本
│   └── cleanup_memory.py        # 清理脚本
└── your_app.py                  # 您的应用
```

---

## 配置管理

### 1. 配置文件

创建 `config/memory_config.json`:

```json
{
  "global_settings": {
    "memory_enabled": true,
    "auto_cleanup": true,
    "backup_enabled": true,
    "backup_interval_hours": 24
  },
  "skills": {
    "task-decomposer": {
      "enabled": true,
      "max_short_term": 50,
      "max_long_term": 200,
      "auto_cleanup": true
    },
    "architect": {
      "enabled": true,
      "max_short_term": 100,
      "max_long_term": 300,
      "auto_cleanup": true
    },
    "modulizer": {
      "enabled": false,
      "note": "根据需要启用"
    },
    "constraint-generator": {
      "enabled": false,
      "note": "根据需要启用"
    }
  },
  "storage": {
    "path": "./memory_storage",
    "backup_path": "./memory_backups"
  },
  "performance": {
    "cleanup_threshold": 0.8,
    "max_memory_size_mb": 500
  }
}
```

### 2. 配置加载器

创建 `scripts/memory_config_loader.py`:

```python
"""
记忆配置加载器
"""
import json
from pathlib import Path
from typing import Dict, Any
from dna_context_engineering.memory import MemoryConfig


class MemoryConfigLoader:
    """加载和管理记忆配置"""

    def __init__(self, config_path: str = "config/memory_config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_skill_config(self, skill_name: str) -> MemoryConfig:
        """
        获取技能的配置

        Args:
            skill_name: 技能名称 (如 'task-decomposer')

        Returns:
            MemoryConfig 对象
        """
        skill_settings = self.config.get('skills', {}).get(skill_name, {})

        return MemoryConfig(
            enabled=skill_settings.get('enabled', False),
            max_short_term=skill_settings.get('max_short_term', 50),
            max_long_term=skill_settings.get('max_long_term', 200),
            auto_cleanup=skill_settings.get('auto_cleanup', True),
            persistence_path=Path(self.config['storage']['path'])
        )

    def get_storage_path(self) -> Path:
        """获取存储路径"""
        return Path(self.config['storage']['path'])

    def get_backup_path(self) -> Path:
        """获取备份路径"""
        return Path(self.config['storage']['backup_path'])

    def is_skill_enabled(self, skill_name: str) -> bool:
        """检查技能是否启用记忆"""
        return self.config.get('skills', {}).get(skill_name, {}).get('enabled', False)

    def list_enabled_skills(self) -> list:
        """列出启用记忆的技能"""
        enabled = []
        for skill_name, settings in self.config.get('skills', {}).items():
            if settings.get('enabled', False):
                enabled.append(skill_name)
        return enabled
```

---

## 部署脚本

### 1. 初始化脚本

创建 `scripts/setup_memory.py`:

```python
"""
记忆系统初始化脚本
"""
import sys
from pathlib import Path

def setup_memory_system():
    """初始化记忆系统"""

    print("=" * 60)
    print("DNASPEC 记忆系统初始化")
    print("=" * 60)

    # 1. 创建必要的目录
    print("\n[1/4] 创建目录结构...")
    directories = [
        'memory_storage',
        'memory_backups',
        'logs',
        'config'
    ]

    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(exist_ok=True)
        print(f"  ✅ {directory}/")

    # 2. 创建默认配置
    print("\n[2/4] 创建默认配置...")
    config_path = Path('config/memory_config.json')

    if not config_path.exists():
        default_config = {
            "global_settings": {
                "memory_enabled": True,
                "auto_cleanup": True,
                "backup_enabled": True,
                "backup_interval_hours": 24
            },
            "skills": {
                "task-decomposer": {
                    "enabled": True,
                    "max_short_term": 50,
                    "max_long_term": 200,
                    "auto_cleanup": True
                },
                "architect": {
                    "enabled": True,
                    "max_short_term": 100,
                    "max_long_term": 300,
                    "auto_cleanup": True
                }
            },
            "storage": {
                "path": "./memory_storage",
                "backup_path": "./memory_backups"
            }
        }

        import json
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)

        print(f"  ✅ 创建配置文件: {config_path}")
    else:
        print(f"  ⚠️  配置文件已存在: {config_path}")

    # 3. 验证安装
    print("\n[3/4] 验证安装...")
    try:
        from dna_context_engineering.memory import (
            MemoryManager,
            SkillsMemoryManager,
            create_task_decomposer_with_memory,
            create_architect_with_memory
        )
        print("  ✅ 记忆系统导入成功")
    except ImportError as e:
        print(f"  ❌ 导入失败: {e}")
        sys.exit(1)

    # 4. 测试配置
    print("\n[4/4] 测试配置...")
    try:
        from scripts.memory_config_loader import MemoryConfigLoader
        loader = MemoryConfigLoader()
        enabled_skills = loader.list_enabled_skills()
        print(f"  ✅ 配置加载成功")
        print(f"  📋 启用记忆的技能: {', '.join(enabled_skills)}")
    except Exception as e:
        print(f"  ⚠️  配置测试失败: {e}")

    print("\n" + "=" * 60)
    print("✅ 初始化完成！")
    print("=" * 60)
    print("\n下一步:")
    print("  1. 根据需要编辑 config/memory_config.json")
    print("  2. 运行您的应用程序")
    print("  3. 使用 scripts/backup_memory.py 定期备份")


if __name__ == '__main__':
    setup_memory_system()
```

### 2. 备份脚本

创建 `scripts/backup_memory.py`:

```python
"""
记忆备份脚本
"""
import json
import shutil
from pathlib import Path
from datetime import datetime
from dna_context_engineering.memory import SkillsMemoryManager


def backup_all_memories(
    memory_storage_path: str = "memory_storage",
    backup_base_path: str = "memory_backups"
):
    """
    备份所有记忆

    Args:
        memory_storage_path: 记忆存储路径
        backup_base_path: 备份基础路径
    """
    print("=" * 60)
    print("DNASPEC 记忆系统备份")
    print("=" * 60)

    # 创建备份目录（带时间戳）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = Path(backup_base_path) / f"backup_{timestamp}"
    backup_path.mkdir(parents=True, exist_ok=True)

    print(f"\n创建备份目录: {backup_path}")

    # 复制记忆存储
    storage_path = Path(memory_storage_path)
    if storage_path.exists():
        backup_storage_path = backup_path / "memory_storage"
        shutil.copytree(storage_path, backup_storage_path)
        print(f"✅ 已备份记忆存储")

        # 统计文件
        file_count = sum(1 for _ in backup_storage_path.rglob('*.json'))
        print(f"   文件数: {file_count}")
    else:
        print("⚠️  记忆存储目录不存在")

    # 创建备份元数据
    metadata = {
        'backup_time': datetime.now().isoformat(),
        'backup_path': str(backup_path),
        'source_path': str(storage_path),
        'backup_type': 'full'
    }

    metadata_path = backup_path / 'metadata.json'
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"✅ 已创建备份元数据")

    # 清理旧备份（保留最近10个）
    print("\n清理旧备份...")
    backup_base = Path(backup_base_path)
    if backup_base.exists():
        backups = sorted(backup_base.glob('backup_*'), reverse=True)
        old_backups = backups[10:]  # 保留最新的10个

        for old_backup in old_backups:
            shutil.rmtree(old_backup)
            print(f"  🗑️  删除: {old_backup.name}")

    print("\n" + "=" * 60)
    print("✅ 备份完成！")
    print("=" * 60)
    print(f"备份位置: {backup_path}")


if __name__ == '__main__':
    import sys

    storage_path = sys.argv[1] if len(sys.argv) > 1 else 'memory_storage'
    backup_path = sys.argv[2] if len(sys.argv) > 2 else 'memory_backups'

    backup_all_memories(storage_path, backup_path)
```

### 3. 清理脚本

创建 `scripts/cleanup_memory.py`:

```python
"""
记忆清理脚本
"""
import sys
from pathlib import Path
from dna_context_engineering.memory import SkillsMemoryManager


def cleanup_all_skills(
    config_path: str = "config/memory_config.json"
):
    """
    清理所有技能的记忆

    Args:
        config_path: 配置文件路径
    """
    print("=" * 60)
    print("DNASPEC 记忆系统清理")
    print("=" * 60)

    # 加载配置
    from scripts.memory_config_loader import MemoryConfigLoader
    loader = MemoryConfigLoader(config_path)

    enabled_skills = loader.list_enabled_skills()
    print(f"\n启用记忆的技能: {', '.join(enabled_skills) if enabled_skills else '无'}")

    if not enabled_skills:
        print("\n⚠️  没有启用记忆的技能，无需清理")
        return

    # 创建管理器（模拟）
    manager = SkillsMemoryManager()

    # 清理统计
    print("\n清理记忆:")
    print("-" * 60)

    # 注意：这里需要实际的技能实例才能清理
    # 以下为示例代码
    for skill_name in enabled_skills:
        print(f"  {skill_name}:")
        print(f"    ⚠️  需要实际技能实例来执行清理")
        print(f"    💡 在应用中调用: manager.cleanup_all_skills()")

    print("\n" + "=" * 60)
    print("💡 提示:")
    print("  在应用代码中使用:")
    print("  ```python")
    print("  from dna_context_engineering.memory import SkillsMemoryManager")
    print("  manager = SkillsMemoryManager()")
    print("  results = manager.cleanup_all_skills()")
    print("  ```")
    print("=" * 60)


if __name__ == '__main__':
    config_path = sys.argv[1] if len(sys.argv) > 1 else 'config/memory_config.json'
    cleanup_all_skills(config_path)
```

---

## 实际使用场景

### 场景1: 持续集成项目助手

创建 `examples/ci_project_helper.py`:

```python
"""
CI/CD 项目助手 - 使用记忆系统学习项目历史
"""
from pathlib import Path
from skills.task_decomposer.skill import task_decomposer_skill
from skills.architect.skill import architect_skill
from dna_context_engineering.memory import (
    create_task_decomposer_with_memory,
    create_architect_with_memory,
    SkillsMemoryManager,
    MemoryConfig
)
from scripts.memory_config_loader import MemoryConfigLoader


class CIProjectHelper:
    """CI/CD 项目助手"""

    def __init__(self, config_path: str = "config/memory_config.json"):
        # 加载配置
        self.config_loader = MemoryConfigLoader(config_path)

        # 创建带记忆的技能
        self.task_decomposer = self._create_skill(
            'task-decomposer',
            task_decomposer_skill,
            create_task_decomposer_with_memory
        )

        self.architect = self._create_skill(
            'architect',
            architect_skill,
            create_architect_with_memory
        )

        # 统一管理
        self.manager = SkillsMemoryManager()
        if self.task_decomposer.has_memory:
            self.manager.register_skill(self.task_decomposer)
        if self.architect.has_memory:
            self.manager.register_skill(self.architect)

    def _create_skill(self, skill_name: str, skill_instance, creator_func):
        """创建带记忆的技能"""
        if self.config_loader.is_skill_enabled(skill_name):
            config = self.config_loader.get_skill_config(skill_name)
            return creator_func(skill_instance, enable_memory=True)
        else:
            return creator_func(skill_instance, enable_memory=False)

    def plan_project(self, project_description: str) -> dict:
        """
        规划新项目（利用历史经验）

        Args:
            project_description: 项目描述

        Returns:
            项目规划
        """
        print(f"\n📋 规划项目: {project_description}")

        # 1. 回顾类似项目
        if self.task_decomposer.has_memory:
            similar = self.task_decomposer.recall_similar_decompositions(project_description[:20])
            if similar:
                print(f"\n💡 找到 {len(similar)} 条类似项目经验:")
                for memory in similar[:3]:
                    print(f"  - {memory}")

        # 2. 分解任务
        print("\n🔨 分解项目任务...")
        tasks = self.task_decomposer.execute({
            'input': project_description,
            'decomposition_method': 'hierarchical'
        })

        print(f"  生成 {len(tasks.get('subtasks', []))} 个子任务")

        # 3. 设计架构
        print("\n🏗️  设计项目架构...")
        architecture = self.architect.execute({
            'input': project_description,
            'architecture_style': 'auto'
        })

        style = architecture.get('architecture_style', 'unknown')
        components = architecture.get('architecture_design', {}).get('components', [])
        print(f"  架构风格: {style}")
        print(f"  核心组件: {len(components)} 个")

        return {
            'tasks': tasks,
            'architecture': architecture
        }

    def show_memory_stats(self):
        """显示记忆统计"""
        print("\n📊 记忆统计:")
        print("-" * 60)

        skills = self.manager.list_skills()
        for skill_info in skills:
            skill_name = skill_info['skill_name']
            has_memory = "✅" if skill_info['has_memory'] else "❌"
            stats = skill_info.get('memory_stats', {})
            total = stats.get('total_memories', 0)

            print(f"  {has_memory} {skill_name}: {total} 条记忆")

            if total > 0:
                short = stats.get('short_term_count', 0)
                long = stats.get('long_term_count', 0)
                print(f"      短期: {short}, 长期: {long}")


# 使用示例
if __name__ == '__main__':
    # 初始化助手
    helper = CIProjectHelper()

    # 规划多个项目（第二个项目会利用第一个的经验）
    projects = [
        "构建微服务架构的电商平台",
        "开发内容管理系统",
        "创建实时数据分析平台"
    ]

    for i, project in enumerate(projects, 1):
        print(f"\n{'=' * 60}")
        print(f"项目 {i}: {project}")
        print('=' * 60)

        result = helper.plan_project(project)

        # 显示记忆增长
        if i > 0:
            helper.show_memory_stats()

    # 最终统计
    print(f"\n{'=' * 60}")
    print("最终记忆统计")
    print('=' * 60)
    helper.show_memory_stats()
```

### 场景2: 智能代码审查助手

创建 `examples/code_review_assistant.py`:

```python
"""
代码审查助手 - 记住审查历史和常见问题
"""
from skills.task_decomposer.skill import task_decomposer_skill
from dna_context_engineering.memory import (
    create_task_decomposer_with_memory,
    MemoryConfig
)


class CodeReviewAssistant:
    """代码审查助手"""

    def __init__(self):
        # 创建带记忆的任务分解器
        config = MemoryConfig(
            enabled=True,
            max_short_term=100,
            max_long_term=500,
            auto_cleanup=True
        )

        self.decomposer = create_task_decomposer_with_memory(
            task_decomposer_skill,
            enable_memory=True
        )

    def review_codebase(self, codebase_description: str):
        """审查代码库"""
        print(f"\n🔍 审查代码库: {codebase_description}")

        # 分解审查任务
        result = self.decomposer.execute({
            'input': f'代码审查: {codebase_description}',
            'decomposition_method': 'hierarchical'
        })

        subtasks = result.get('subtasks', [])
        print(f"\n生成 {len(subtasks)} 个审查任务:")
        for task in subtasks:
            print(f"  - {task.get('name', 'Unknown')}")

        # 记忆常见问题
        common_issues = self.decomposer.recall_similar_decompositions('问题')
        if common_issues:
            print(f"\n⚠️  历史常见问题 ({len(common_issues)}):")
            for issue in common_issues[:5]:
                print(f"  - {issue}")

    def learn_from_review(self, review_summary: str):
        """从审查中学习"""
        print(f"\n📚 记录审查经验: {review_summary}")
        # 记忆会自动记录
```

---

## 性能优化

### 1. 记忆容量优化

```python
# 根据使用场景调整容量
from dna_context_engineering.memory import MemoryConfig

# 轻量级 - 临时任务
light_config = MemoryConfig(
    enabled=True,
    max_short_term=20,
    max_long_term=50,
    auto_cleanup=True
)

# 标准级 - 常规项目
standard_config = MemoryConfig(
    enabled=True,
    max_short_term=50,
    max_long_term=200,
    auto_cleanup=True
)

# 重量级 - 长期项目
heavy_config = MemoryConfig(
    enabled=True,
    max_short_term=100,
    max_long_term=500,
    auto_cleanup=True
)
```

### 2. 选择性记忆

```python
# 只记忆重要内容
important_tasks = [
    {'task': '系统架构设计', 'remember': True},
    {'task': '临时调试', 'remember': False},
    {'task': '核心功能开发', 'remember': True}
]

for item in important_tasks:
    result = decomposer.execute(
        {'input': item['task']},
        remember_decomposition=item['remember']
    )
```

### 3. 批量操作优化

```python
# 批量执行后统一清理
tasks = [f'任务{i}' for i in range(100)]

# 执行
for task in tasks:
    decomposer.execute({'input': task})

# 统一清理（而非每次执行后清理）
decomposer.memory_manager.cleanup(decomposer.skill_id)
```

---

## 监控和运维

### 1. 监控脚本

创建 `scripts/monitor_memory.py`:

```python
"""
记忆系统监控脚本
"""
import json
from pathlib import Path
from datetime import datetime


def monitor_memory_system(storage_path: str = "memory_storage"):
    """
    监控记忆系统状态

    Args:
        storage_path: 记忆存储路径
    """
    print("=" * 60)
    print("DNASPEC 记忆系统监控")
    print("=" * 60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    storage = Path(storage_path_path)

    if not storage.exists():
        print("\n⚠️  记忆存储目录不存在")
        return

    # 统计总体情况
    total_files = 0
    total_size = 0
    agent_count = 0

    agents_dir = storage / 'agents'
    if agents_dir.exists():
        for agent_dir in agents_dir.iterdir():
            if agent_dir.is_dir():
                agent_count += 1
                agent_files = list(agent_dir.glob('*.json'))
                agent_file_count = len(agent_files)
                agent_size = sum(f.stat().st_size for f in agent_files)

                total_files += agent_file_count
                total_size += agent_size

                print(f"\n📁 {agent_dir.name}:")
                print(f"   记忆文件: {agent_file_count}")
                print(f"   大小: {agent_size / 1024:.2f} KB")

    print("\n" + "=" * 60)
    print("总体统计:")
    print(f"  智能体数量: {agent_count}")
    print(f"  总记忆文件: {total_files}")
    print(f"  总大小: {total_size / (1024 * 1024):.2f} MB")
    print(f"  平均每智能体: {total_files / agent_count:.1f} 个文件" if agent_count > 0 else "")
    print("=" * 60)

    # 健康检查
    print("\n健康检查:")
    if total_size > 500 * 1024 * 1024:  # 500MB
        print("  ⚠️  总大小超过 500MB，建议清理")
    else:
        print("  ✅ 大小正常")

    if total_files > 10000:
        print("  ⚠️  文件数超过 10000，建议清理")
    else:
        print("  ✅ 文件数正常")


if __name__ == '__main__':
    import sys
    storage_path = sys.argv[1] if len(sys.argv) > 1 else 'memory_storage'
    monitor_memory_system(storage_path)
```

### 2. 定期维护任务

创建 `scripts/maintenance_scheduler.py`:

```python
"""
定期维护任务调度器
"""
import schedule
import time
from scripts.backup_memory import backup_all_memories
from scripts.monitor_memory import monitor_memory_system


def run_maintenance():
    """运行维护任务"""

    # 每天凌晨2点备份
    schedule.every().day.at("02:00").do(
        backup_all_memories
    )

    # 每6小时监控
    schedule.every(6).hours.do(
        monitor_memory_system
    )

    print("维护任务调度器启动...")
    print("备份: 每天 02:00")
    print("监控: 每 6 小时")

    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次


if __name__ == '__main__':
    run_maintenance()
```

---

## 故障排除

### 问题1: 记忆未保存

**症状**: 执行任务后无法检索到记忆

**诊断**:
```python
# 1. 检查记忆是否启用
if not skill.has_memory:
    print("❌ 记忆未启用")

# 2. 检查存储路径
storage_path = Path("memory_storage")
if not storage_path.exists():
    print("❌ 存储目录不存在")

# 3. 检查权限
import os
if not os.access(storage_path, os.W_OK):
    print("❌ 没有写入权限")
```

**解决方案**:
```bash
# 创建存储目录
mkdir -p memory_storage/agents

# 检查权限
chmod 755 memory_storage
```

### 问题2: 记忆数量过多

**症状**: 记忆数量快速增长，影响性能

**解决方案**:
```python
# 1. 调整配置
config = MemoryConfig(
    enabled=True,
    max_short_term=30,  # 降低限制
    auto_cleanup=True
)

# 2. 手动清理
skill.memory_manager.cleanup(skill.skill_id)

# 3. 导出并清理
manager.export_all_memories(Path('backup'))
manager.cleanup_all_skills()
```

### 问题3: 配置文件错误

**症状**: 无法加载配置

**解决方案**:
```bash
# 1. 验证JSON格式
python -m json.tool config/memory_config.json

# 2. 重新生成配置
python scripts/setup_memory.py

# 3. 检查路径
ls -la config/memory_config.json
```

---

## 部署清单

### 初次部署

- [ ] 运行初始化脚本: `python scripts/setup_memory.py`
- [ ] 编辑配置文件: `config/memory_config.json`
- [ ] 设置定期备份: 配置 cron 任务
- [ ] 配置监控: 设置监控脚本
- [ ] 测试功能: 运行示例代码

### 日常维护

- [ ] 每日自动备份
- [ ] 每周检查监控报告
- [ ] 每月清理旧记忆
- [ ] 每季度审查配置

### 应急准备

- [ ] 备份恢复流程
- [ ] 故障诊断文档
- [ ] 联系支持信息

---

## 快速参考

### 常用命令

```bash
# 初始化
python scripts/setup_memory.py

# 备份记忆
python scripts/backup_memory.py

# 监控状态
python scripts/monitor_memory.py

# 清理记忆（在应用中）
python -c "from your_app import helper; helper.manager.cleanup_all_skills()"
```

### 配置模板

```json
{
  "skills": {
    "task-decomposer": {
      "enabled": true,
      "max_short_term": 50,
      "max_long_term": 200,
      "auto_cleanup": true
    }
  }
}
```

---

**文档版本**: 1.0
**最后更新**: 2025-12-26
**维护者**: DNASPEC Team
