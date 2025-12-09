#!/usr/bin/env python3
"""
项目整理脚本 - 将重复目录归档，而不是删除
保留有价值内容，清理冗余结构
"""
import os
import shutil
from pathlib import Path
import datetime


def archive_redundant_directories():
    """将重复目录归档处理"""
    print("🔍 检查和整理重复目录...")
    
    project_root = Path("D:\\DAIP\\dnaSpec")
    
    # 要归档的目录列表
    redundant_dirs = ['dnaSpec', 'dna-context-engineering']
    
    for dir_name in redundant_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists() and dir_path.is_dir():
            # 创建归档目录名
            archive_dir = project_root / 'archive' / dir_name
            archive_dir.parent.mkdir(exist_ok=True)
            
            # 检查是否已经有同名归档，若有则加时间戳
            if archive_dir.exists():
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_dir = project_root / 'archive' / f"{dir_name}_{timestamp}"
            
            # 移动到归档目录
            print(f"📦 归档目录: {dir_name}")
            try:
                shutil.move(str(dir_path), str(archive_dir))
                print(f"   → 已归档到: {archive_dir}")
            except Exception as e:
                print(f"   ❌ 归档失败: {e}")
                import traceback
                traceback.print_exc()

    print("\n✅ 项目整理完成！")
    print("重复目录已归档到 archive/ 子目录中")


def verify_cleanup():
    """验证清理操作"""
    project_root = Path("D:\\DAIP\\dnaSpec")
    
    print("\n📋 验证项目结构...")
    redundant_exists = []
    
    for dir_name in ['dnaSpec', 'dna-context-engineering']:
        dir_path = project_root / dir_name
        if dir_path.exists():
            redundant_exists.append(dir_name)
    
    if not redundant_exists:
        print("✅ 所有重复目录已归档")
    else:
        print(f"⚠️ 仍有未归档的重复目录: {redundant_exists}")


if __name__ == "__main__":
    archive_redundant_directories()
    verify_cleanup()