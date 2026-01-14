"""
记忆备份脚本
"""
import sys
from pathlib import Path
import json
import shutil
from datetime import datetime


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
        total_size = sum(
            f.stat().st_size
            for f in backup_storage_path.rglob('*.json')
        )
        print(f"   文件数: {file_count}")
        print(f"   大小: {total_size / (1024 * 1024):.2f} MB")
    else:
        print("⚠️  记忆存储目录不存在")

    # 创建备份元数据
    metadata = {
        'backup_time': datetime.now().isoformat(),
        'backup_path': str(backup_path),
        'source_path': str(storage_path.absolute()),
        'backup_type': 'full',
        'file_count': file_count if storage_path.exists() else 0,
        'total_size_bytes': total_size if storage_path.exists() else 0
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

        if old_backups:
            print(f"找到 {len(old_backups)} 个旧备份:")
            for old_backup in old_backups:
                shutil.rmtree(old_backup)
                print(f"  🗑️  删除: {old_backup.name}")
        else:
            print("  无需清理")

    print("\n" + "=" * 60)
    print("✅ 备份完成！")
    print("=" * 60)
    print(f"备份位置: {backup_path.absolute()}")
    print(f"备份文件: {file_count} 个")
    print(f"备份大小: {total_size / (1024 * 1024):.2f} MB")


if __name__ == '__main__':
    storage_path = sys.argv[1] if len(sys.argv) > 1 else 'memory_storage'
    backup_path = sys.argv[2] if len(sys.argv) > 2 else 'memory_backups'

    backup_all_memories(storage_path, backup_path)
