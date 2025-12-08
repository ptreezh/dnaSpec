#!/usr/bin/env python3
"""
修复所有egg-info文件中的DSGS引用为DNASPEC
"""
import os
import re
from pathlib import Path


def fix_all_egg_info_files():
    """修复所有egg-info目录中的包名引用"""
    print("修复所有egg-info文件中的DSGS引用...")
    
    egg_info_dirs = []
    
    # 查找所有.egg-info目录
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name.endswith('.egg-info'):
                egg_info_dirs.append(Path(root) / dir_name)

    print(f"找到 {len(egg_info_dirs)} 个egg-info目录")
    
    files_fixed = 0
    
    for egg_info_dir in egg_info_dirs:
        pkg_info_file = egg_info_dir / 'PKG-INFO'
        if pkg_info_file.exists():
            print(f"修复: {pkg_info_file}")
            
            with open(pkg_info_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 执行修复
            content = re.sub(r'dsgs-([a-zA-Z])', r'dnaspec-\1', content)
            content = re.sub(r'dsgs_([a-zA-Z])', r'dnaspec_\1', content)
            content = re.sub(r'DSGS', r'DNASPEC', content)
            content = re.sub(r'dsgs', r'dnaspec', content)
            content = re.sub(r'/speckit\.dsgs\.', r'/speckit.dnaspec.', content)
            content = re.sub(r'/dsgs-', r'/dnaspec-', content)
            
            if content != original_content:
                with open(pkg_info_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_fixed += 1
                print(f"  ✅ 已修复")
            else:
                print(f"  → 无需修复")
    
    print(f"完成！修复了 {files_fixed} 个文件")
    return files_fixed


if __name__ == "__main__":
    fix_all_egg_info_files()