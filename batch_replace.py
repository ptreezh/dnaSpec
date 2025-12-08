#!/usr/bin/env python3
"""
批量替换工具 - 将所有dna_替换为dna_
"""
import os
import re
import shutil
from pathlib import Path

def replace_dna_with_dna_in_file(filepath):
    """在单个文件中将dna_替换为dna_"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 执行替换
        content = content.replace('dna_', 'dna_')
        content = content.replace('DNA_', 'DNA_')
        content = content.replace('dna-', 'dna-')
        content = content.replace('DNA-', 'DNA-')
        
        # 如果内容发生变化，写回文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ 已更新: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"   ❌ 无法处理文件 {filepath}: {e}")
        return False

def replace_dna_with_dna_in_directory(directory_path):
    """批量替换目录中所有文件中的dna_为dna_"""
    dir_path = Path(directory_path)
    extensions = ['.py', '.js', '.md', '.txt', '.json', '.yaml', '.yml', '.cfg', '.ini', '.toml']

    total_updated = 0
    total_processed = 0

    for root, dirs, files in os.walk(dir_path):
        # 跳过缓存和隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__']]

        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                total_processed += 1
                file_path = Path(root) / file
                try:
                    updated = replace_dna_with_dna_in_file(str(file_path))
                    if updated:
                        total_updated += 1
                except Exception as e:
                    print(f"   ❌ 处理文件 {file_path} 时出错: {e}")

    print(f"\n✅ 完成了替换: {total_updated}/{total_processed} 个文件中包含dna_被更新")
    return total_updated

def rename_dna_directories(directory_path):
    """重命名所有包含dna-的目录为dna-"""
    print("\n🔍 重命名包含dna-的目录...")
    
    dir_path = Path(directory_path)
    renamed_count = 0
    
    for root, dirs, files in os.walk(dir_path, topdown=False):  # topdown=False 确保从最深处开始重命名
        for dir_name in dirs:
            if 'dna-' in dir_name or 'dna_' in dir_name or 'DSGS' in dir_name:
                old_path = Path(root) / dir_name
                new_name = dir_name.replace('dna-', 'dna-').replace('DNA-', 'DNA-').replace('dna_', 'dna_').replace('DNA_', 'DNA_')
                new_path = Path(root) / new_name
                
                if old_path != new_path:
                    try:
                        old_path.rename(new_path)
                        print(f"   ✅ 重命名目录: {dir_name} → {new_name}")
                        renamed_count += 1
                    except Exception as e:
                        print(f"   ❌ 无法重命名目录 {old_path}: {e}")
    
    print(f"\n✅ 目录重命名完成: {renamed_count} 个目录已重命名")
    return renamed_count

def main():
    print("🚀 批量替换工具 - DSGS → DNA")
    print("="*50)
    
    project_path = r"D:\DAIP\dnaSpec"
    
    print(f"处理项目路径: {project_path}")
    print("\n1. 重命名目录...")
    dir_renamed = rename_dna_directories(project_path)
    
    print("\n2. 替换文件内容...")
    files_updated = replace_dna_with_dna_in_directory(project_path)
    
    print("\n" + "="*50)
    print("🎉 批量替换完成！")
    print(f"目录重命名: {dir_renamed} 个")
    print(f"文件内容更新: {files_updated} 个")
    print("DSGS → DNA 替换全部完成！")

if __name__ == "__main__":
    main()