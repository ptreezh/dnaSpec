#!/usr/bin/env python3
"""
精确术语替换器 - 将DNASPEC相关术语统一替换为dnaspec
"""
import os
import re
from pathlib import Path


def replace_terms_in_specific_file(file_path: str, term_mapping: dict):
    """
    在特定文件中进行术语替换
    
    Args:
        file_path: 文件路径
        term_mapping: 术语映射字典
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original_content = content
    
    # 执行术语替换
    for old_term, new_term in term_mapping.items():
        # 使用单词边界确保精确替换
        pattern = r'\b' + re.escape(old_term) + r'\b'
        content = re.sub(pattern, new_term, content)
        
        # 同时处理大小写变体
        pattern_upper = r'\b' + old_term.upper() + r'\b'
        content = re.sub(pattern_upper, new_term.upper(), content)
        
        pattern_capital = r'\b' + old_term.capitalize() + r'\b'
        content = re.sub(pattern_capital, new_term.capitalize(), content)
    
    # 如果内容发生变化，写回文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ 已更新: {file_path}")
        return True
    else:
        print(f"  → 无需更新: {file_path}")
        return False


def batch_replace_terms(directory_path: str, file_patterns: list = None):
    """
    批量替换术语
    
    Args:
        directory_path: 目录路径
        file_patterns: 文件模式列表
    """
    if file_patterns is None:
        file_patterns = ['*.py', '*.js', '*.md', '*.json', '*.toml']
    
    # 术语替换映射
    term_mapping = {
        # 包和项目名
        'DNASPEC': 'DNASPEC',
        'dnaspec': 'dnaspec',
        'dnaspec-': 'dnaspec-',
        'DNASPEC-': 'DNASPEC-',
        
        # 技能命令前缀
        '/speckit.dnaspec.': '/speckit.dnaspec.',
        
        # 模块路径
        'dnaspec_spec_kit_integration': 'dnaspec_spec_kit_integration',
        'dnaspec_context_engineering': 'dnaspec_context_engineering',
        'dnaspec_context_engineering_skills': 'dnaspec_context_engineering_skills',
        
        # 类名和技能名
        'DNASpecSkill': 'DNASpecSkill',
        'Dnaspec': 'Dnaspec',
        'dnaspec_skill': 'dnaspec_skill',
        
        # 产品描述相关
        'DNASPEC Context Engineering Skills': 'DNASPEC Context Engineering Skills',
        'DNASPEC context engineering': 'DNASPEC context engineering',
        'Dynamic Specification Growth System': 'Dynamic Specification Growth System',
    }
    
    updated_count = 0
    dir_path = Path(directory_path)
    
    # 找到符合条件的文件
    files_to_process = []
    for pattern in file_patterns:
        files_to_process.extend(list(dir_path.rglob(pattern)))
    
    print(f"发现 {len(files_to_process)} 个文件需要处理")
    
    for file_path in files_to_process:
        # 跳过缓存目录和隐藏文件
        if any(skip_dir in str(file_path) for skip_dir in ['__pycache__', '.git', '.vscode', 'node_modules', '.dnaspec']):
            continue
        
        try:
            if str(file_path).endswith(('.py', '.js', '.md', '.json', '.toml')):
                if replace_terms_in_specific_file(str(file_path), term_mapping):
                    updated_count += 1
        except Exception as e:
            print(f"  ❌ 处理失败 {file_path}: {e}")
    
    print(f"\n术语替换完成: 共更新了 {updated_count} 个文件")
    return updated_count


def main():
    """主函数"""
    print("🚀 DNASPEC 术语统一替换工具")
    print("="*50)
    print("将项目中所有DNASPEC相关术语统一替换为dnaspec")
    print()
    
    project_path = r"D:\DAIP\dnaSpec"
    print(f"处理项目路径: {project_path}")
    
    updated_files = batch_replace_terms(
        project_path, 
        ['*.py', '*.js', '*.md', '*.json', '*.toml', '*.yaml', '*.yml']
    )
    
    print(f"\n✅ 术语替换任务完成！")
    print(f"已更新 {updated_files} 个文件中的DNASPEC术语为dnaspec")
    
    # 创建更新说明
    print("\n主要替换内容:")
    print("  - DNASPEC → DNASPEC")
    print("  - dnaspec → dnaspec")
    print("  - /speckit.dnaspec. → /speckit.dnaspec.") 
    print("  - 模块路径和类名统一更新")


if __name__ == "__main__":
    main()