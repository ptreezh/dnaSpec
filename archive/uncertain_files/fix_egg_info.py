# 批量替换所有DSGS相关术语为DNASPEC
import os
import re

# 修复 PKG-INFO 文件中的所有DSGS引用
pkg_info_path = r"D:\DAIP\dnaSpec\src\dna_context_engineering_skills.egg-info\PKG-INFO"

with open(pkg_info_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换所有引用
replacements = [
    # 包名和项目名替换
    (r'dsgs-(\w+)', r'dnaspec-\1'),
    (r'dsgs_(\w+)', r'dnaspec_\1'),
    (r'DSGS', 'DNASPEC'),
    (r'dsgs', 'dnaspec'),
    
    # 特定命令替换
    (r'/speckit\.dsgs\.', '/speckit.dnaspec.'),
    (r'`dsgs-(\w+)`', r'`dnaspec-\1`'),
    (r'`dsgs`', '`dnaspec`'),
]

for old_pattern, new_pattern in replacements:
    content = re.sub(old_pattern, new_pattern, content)

with open(pkg_info_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"已修复 PKG-INFO 文件: {pkg_info_path}")