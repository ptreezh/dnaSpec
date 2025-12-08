#!/usr/bin/env python3
"""
术语统一替换工具
将项目中所有"DNASPEC"相关术语替换为"dnaspec"
"""
import os
import re
from pathlib import Path


def replace_terms_in_file(file_path: str):
    """替换文件中的术语"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 执行替换
        replacements = [
            # 包名和产品名替换
            (r'\bDNASPEC\b', 'DNASPEC'),
            (r'\bdnaspec\b', 'dnaspec'),
            (r'\bDNASPEC\b', 'DNASPEC'), 
            (r'\bDNA-Project\b', 'DNA-SPEC-Project'),
            (r'\bDNASPEC_CONTEXT_ENGINEERING\b', 'DNASPEC_CONTEXT_ENGINEERING'),
            (r'\bDNASPEC_Context_Engineering\b', 'DNASPEC_Context_Engineering'),
            (r'\bdsks\b', 'dnaspec'),
            
            # 中英文混合替换 - 大写
            (r'Context Engineering Skills', 'Context Engineering Skills'),
            
            # 命令和路径替换
            (r'/speckit\.dnaspec\.', '/speckit.dnaspec.'),
            (r'dnaspec-', 'dnaspec-'),
            (r'DNASPEC_', 'DNASPEC_'),
            (r'\bdnaspec_', 'dnaspec_'),
            
            # 保留"dnaspec"相关，但移除其他DNASPEC术语
            (r'DNASPEC Context Engineering Skills', 'DNASPEC Context Engineering Skills'),
            (r'dnaspec-context-engineering', 'dnaspec-context-engineering'),
            (r'dnaspec_spec_kit', 'dnaspec_spec_kit'),
            (r'dnaspec_context_engineering', 'dnaspec_context_engineering'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
    
        # 如果内容发生变化，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   已更新: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"   无法处理文件 {file_path}: {e}")
        return False


def replace_terms_in_directory(directory: str):
    """批量替换目录中的术语"""
    dir_path = Path(directory)
    extensions = ['.py', '.js', '.md', '.txt', '.json', '.yaml', '.yml', '.toml']
    
    updated_count = 0
    total_count = 0
    
    for root, dirs, files in os.walk(dir_path):
        # 跳过__pycache__和临时目录
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.vscode', 'node_modules', '.dnaspec']]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                total_count += 1
                file_path = Path(root) / file
                if replace_terms_in_file(str(file_path)):
                    updated_count += 1
    
    print(f"\n术语替换完成: {updated_count}/{total_count} 个文件已更新")
    return updated_count, total_count


def verify_replacements():
    """验证替换结果"""
    print("\n验证替换结果...")
    
    # 查找可能遗漏的DNASPEC术语
    import subprocess
    try:
        result = subprocess.run(
            ['grep', '-r', 'DNASPEC', '.', '--include=*.py', '--include=*.js', '--include=*.md', '--exclude-dir=.git'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        if result.stdout:
            print("可能还有遗漏的DNASPEC术语:")
            print(result.stdout[:500])  # 只显示前500字符
        else:
            print("✅ 所有DNASPEC术语已成功替换为dnaspec")
    except:
        print("无法使用grep检查，跳过验证")


def main():
    """主函数"""
    print("术语统一替换工具")
    print("="*50)
    print("将所有DNASPEC相关术语替换为dnaspec")
    print()
    
    directory = r"D:\DAIP\dnaSpec"
    print(f"处理目录: {directory}")
    
    updated, total = replace_terms_in_directory(directory)
    
    print(f"\n处理完成: {updated}个文件被更新，共检查{total}个文件")
    
    verify_replacements()
    
    print("\n术语替换任务完成！")
    print("主要替换:")
    print("- DNASPEC → DNASPEC")
    print("- dnaspec → dnaspec") 
    print("- /speckit.dnaspec. → /speckit.dnaspec.")
    print("- 各种模块和类名中的DNASPEC术语")


if __name__ == "__main__":
    main()