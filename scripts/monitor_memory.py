"""
记忆系统监控脚本
"""
import sys
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

    storage = Path(storage_path)

    if not storage.exists():
        print("\n⚠️  记忆存储目录不存在")
        print(f"   路径: {storage.absolute()}")
        print("\n💡 运行初始化脚本:")
        print("   python scripts/setup_memory.py")
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
    else:
        print("\n⚠️  没有找到 agents 目录")

    print("\n" + "=" * 60)
    print("总体统计:")
    print(f"  智能体/技能数量: {agent_count}")
    print(f"  总记忆文件: {total_files}")
    print(f"  总大小: {total_size / (1024 * 1024):.2f} MB")
    if agent_count > 0:
        print(f"  平均每技能: {total_files / agent_count:.1f} 个文件")
    print("=" * 60)

    # 健康检查
    print("\n健康检查:")

    # 检查大小
    if total_size > 500 * 1024 * 1024:  # 500MB
        print("  ⚠️  总大小超过 500MB")
        print("     建议: 运行清理或备份")
        print("     命令: python scripts/backup_memory.py")
    elif total_size > 100 * 1024 * 1024:  # 100MB
        print("  ⚡ 总大小较大 (100-500MB)")
        print("     建议: 考虑清理")
    else:
        print("  ✅ 大小正常")

    # 检查文件数
    if total_files > 10000:
        print("  ⚠️  文件数超过 10000")
        print("     建议: 运行清理")
    elif total_files > 5000:
        print("  ⚡ 文件数较多 (5000-10000)")
        print("     建议: 监控增长")
    else:
        print("  ✅ 文件数正常")

    # 检查备份
    backup_path = Path('memory_backups')
    if backup_path.exists():
        backups = list(backup_path.glob('backup_*'))
        if backups:
            latest_backup = max(backups, key=lambda p: p.stat().st_mtime)
            print(f"  ✅ 最新备份: {latest_backup.name}")
        else:
            print("  ⚠️  备份目录为空")
    else:
        print("  ⚠️  备份目录不存在")

    # 推荐操作
    print("\n推荐操作:")
    if total_size > 100 * 1024 * 1024 or total_files > 5000:
        print("  1. 备份记忆: python scripts/backup_memory.py")
        print("  2. 清理旧记忆: 在应用中调用 manager.cleanup_all_skills()")

    if not backup_path.exists():
        print("  1. 创建备份目录: mkdir -p memory_backups")
        print("  2. 设置定期备份")

    print("\n" + "=" * 60)


def show_quick_stats(storage_path: str = "memory_storage"):
    """显示快速统计"""
    storage = Path(storage_path)

    if not storage.exists():
        print("❌ 记忆存储目录不存在")
        return

    total_files = 0
    total_size = 0
    agent_count = 0

    agents_dir = storage / 'agents'
    if agents_dir.exists():
        for agent_dir in agents_dir.iterdir():
            if agent_dir.is_dir():
                agent_count += 1
                agent_files = list(agent_dir.glob('*.json'))
                total_files += len(agent_files)
                total_size += sum(f.stat().st_size for f in agent_files)

    print(f"技能数: {agent_count}, 记忆数: {total_files}, 大小: {total_size / (1024 * 1024):.2f} MB")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        storage_path = sys.argv[2] if len(sys.argv) > 2 else 'memory_storage'
        show_quick_stats(storage_path)
    else:
        storage_path = sys.argv[1] if len(sys.argv) > 1 else 'memory_storage'
        monitor_memory_system(storage_path)
