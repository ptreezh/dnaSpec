#!/usr/bin/env python3
"""
重命名工具 - 将所有dna-前缀的目录重命名为dna-
根据第一性原理分析，确保所有组件都使用正确的包名
"""
import os
import shutil
from pathlib import Path

def rename_dnaspec_directories(base_path: str):
    """
    递归重命名所有dna-开头的目录为dna-开头
    """
    print("🔍 扫描并重命名DNASPEC相关目录...")
    
    renamed_dirs = []
    
    # 遍历所有目录
    for root, dirs, files in os.walk(base_path):
        # 避免处理缓存和隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.') and '__pycache__' not in root]
        
        for dir_name in dirs:
            if dir_name.startswith('dna-'):
                old_path = Path(root) / dir_name
                new_name = dir_name.replace('dna-', 'dna-', 1)  # 只替换第一个匹配
                new_path = Path(root) / new_name
                
                # 重命名目录
                if str(old_path).lower() != str(new_path).lower():  # 避免Windows大小写问题
                    try:
                        old_path.rename(new_path)
                        renamed_dirs.append((str(old_path), str(new_path)))
                        print(f"✅ 重命名: {dir_name} → {new_name}")
                    except OSError as e:
                        print(f"⚠️  无法重命名 {old_path}: {e}")
    
    print(f"\n🎉 重命名完成！总共重命名了 {len(renamed_dirs)} 个目录")
    for old, new in renamed_dirs:
        print(f"  {old} → {new}")
    
    return renamed_dirs

def update_content_references(base_path: str):
    """
    更新所有文件中对dna-的引用为dna-
    """
    print("\n📝 更新所有文件中的引用...")
    
    # 更新文件中内容的引用
    updated_files = []
    extensions = ['.py', '.js', '.md', '.json', '.yaml', '.yml', '.toml']
    
    for root, dirs, files in os.walk(base_path):
        # 跳过__pycache__和.git目录
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git']]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = Path(root) / file
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # 替换路径引用
                    content = content.replace('dna-', 'dna-')
                    content = content.replace('DNA-', 'DNA-')
                    content = content.replace('DNASPEC', 'DNASPEC')
                    content = content.replace('dnaspec', 'dnaspec')
                    
                    # 如果内容有变化，写回文件
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        updated_files.append(str(file_path))
                        print(f"✅ 更新文件: {file}")
                        
                except UnicodeDecodeError:
                    # 跳过二进制文件或编码问题
                    continue
                except Exception as e:
                    print(f"⚠️  处理文件 {file_path} 时出错: {e}")
    
    print(f"\n🎉 文件更新完成！总共更新了 {len(updated_files)} 个文件")
    return updated_files

def main():
    """主函数"""
    base_path = "D:\\DAIP\\dnaSpec"
    
    print("DNASPEC → DNA- 重命名工具")
    print("=" * 50)
    print(f"处理路径: {base_path}")
    print()
    
    # 1. 重命名目录
    renamed_directories = rename_dnaspec_directories(base_path)
    
    # 2. 更新内容引用
    updated_files = update_content_references(base_path)
    
    # 3. 总结
    print("\n" + "=" * 50)
    print("总览:")
    print(f"- 重命名的目录: {len(renamed_directories)}")
    print(f"- 更新的文件: {len(updated_files)}")
    
    print("\n注意: 重命名后需要相应地更新引用路径")
    print("如果您要发布到npm，请确保所有引用都已更新为新的名称")
    
    return True

if __name__ == "__main__":
    main()