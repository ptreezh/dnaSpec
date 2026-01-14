"""
记忆系统初始化脚本
"""
import sys
from pathlib import Path
import json

# 添加src到路径
script_dir = Path(__file__).parent
src_dir = script_dir.parent / 'src'
project_root = script_dir.parent

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


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
        'config',
        'docs',
        'scripts',
        'examples'
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
                },
                "modulizer": {
                    "enabled": False,
                    "note": "根据需要启用"
                },
                "constraint-generator": {
                    "enabled": False,
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
        print("\n💡 请确保已安装 dnaspec:")
        print("   pip install -e .")
        sys.exit(1)

    # 4. 测试配置
    print("\n[4/4] 测试配置...")
    try:
        # 简单测试读取配置
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        enabled_skills = [
            skill for skill, settings in config.get('skills', {}).items()
            if settings.get('enabled', False)
        ]

        print(f"  ✅ 配置加载成功")
        print(f"  📋 启用记忆的技能: {', '.join(enabled_skills) if enabled_skills else '无'}")
    except Exception as e:
        print(f"  ⚠️  配置测试失败: {e}")

    print("\n" + "=" * 60)
    print("✅ 初始化完成！")
    print("=" * 60)
    print("\n目录结构:")
    print("  memory_storage/    - 记忆存储目录")
    print("  memory_backups/    - 记忆备份目录")
    print("  config/            - 配置文件")
    print("  logs/              - 日志目录")
    print("  examples/          - 使用示例")
    print("\n下一步:")
    print("  1. 根据需要编辑 config/memory_config.json")
    print("  2. 运行示例: python examples/ci_project_helper.py")
    print("  3. 设置定期备份: python scripts/backup_memory.py")
    print("\n文档:")
    print("  📖 完整指南: docs/PRODUCTION_MEMORY_GUIDE.md")


if __name__ == '__main__':
    setup_memory_system()
