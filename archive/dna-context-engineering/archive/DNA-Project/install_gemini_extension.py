#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNASPEC Gemini CLI Extensions 安装脚本
"""

import os
import sys
import json
import shutil
from pathlib import Path

def find_gemini_cli_directory():
    """查找Gemini CLI安装目录"""
    # 常见的安装路径
    possible_paths = [
        os.path.expanduser("~/.gemini"),
        os.path.expanduser("~/gemini"),
        "/usr/local/gemini",
        "/opt/gemini"
    ]
    
    for path in possible_paths:
        if os.path.exists(path) and os.path.isdir(path):
            return path
    
    # 检查PATH环境变量
    for path in os.environ.get("PATH", "").split(os.pathsep):
        if "gemini" in path.lower() and os.path.exists(path):
            return path
    
    return None

def install_dnaspec_extensions():
    """安装DNASPEC扩展"""
    print("=== DNASPEC Gemini CLI Extensions 安装程序 ===")
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"当前目录: {current_dir}")
    
    # 查找Gemini CLI目录
    gemini_dir = find_gemini_cli_directory()
    if not gemini_dir:
        print("警告: 未找到Gemini CLI安装目录")
        gemini_dir = input("请输入Gemini CLI安装目录路径: ").strip()
    
    if not os.path.exists(gemini_dir):
        print(f"错误: 目录 {gemini_dir} 不存在")
        return False
    
    print(f"找到Gemini CLI目录: {gemini_dir}")
    
    # 创建扩展目录
    extensions_dir = os.path.join(gemini_dir, "extensions", "dnaspec")
    os.makedirs(extensions_dir, exist_ok=True)
    print(f"创建扩展目录: {extensions_dir}")
    
    # 复制核心文件
    files_to_copy = [
        "gemini_skills_core.py",
        "gemini_intelligent_matcher.py", 
        "gemini_hook_handler.py",
        "GEMINI_EXTENSION_CONFIG.json"
    ]
    
    for filename in files_to_copy:
        src_path = os.path.join(current_dir, filename)
        dst_path = os.path.join(extensions_dir, filename)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"复制 {filename} -> {dst_path}")
        else:
            print(f"警告: 文件 {filename} 不存在")
    
    # 复制技能目录
    skills_src = os.path.join(current_dir, "skills")
    skills_dst = os.path.join(extensions_dir, "skills")
    if os.path.exists(skills_src):
        if os.path.exists(skills_dst):
            shutil.rmtree(skills_dst)
        shutil.copytree(skills_src, skills_dst)
        print(f"复制技能目录 -> {skills_dst}")
    
    # 复制源代码目录
    src_src = os.path.join(current_dir, "src")
    src_dst = os.path.join(extensions_dir, "src")
    if os.path.exists(src_src):
        if os.path.exists(src_dst):
            shutil.rmtree(src_dst)
        shutil.copytree(src_src, src_dst)
        print(f"复制源代码目录 -> {src_dst}")
    
    # 更新Gemini配置文件
    config_path = os.path.join(gemini_dir, "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            config = {}
        
        # 添加扩展
        if "extensions" not in config:
            config["extensions"] = []
        
        dnaspec_extension = {
            "name": "dnaspec-gemini-extensions",
            "path": extensions_dir,
            "enabled": True,
            "version": "1.0.0"
        }
        
        # 检查是否已存在
        existing = False
        for i, ext in enumerate(config["extensions"]):
            if ext.get("name") == "dnaspec-gemini-extensions":
                config["extensions"][i] = dnaspec_extension
                existing = True
                break
        
        if not existing:
            config["extensions"].append(dnaspec_extension)
        
        # 保存配置
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"更新配置文件: {config_path}")
    
    print("\n=== 安装完成 ===")
    print("DNASPEC扩展已成功安装到Gemini CLI中")
    print("现在可以在Gemini CLI中使用DNASPEC技能了")
    print("\n使用示例:")
    print("  • '创建一个项目管理智能体' -> 自动调用dna-agent-creator")
    print("  • '分解复杂的软件开发任务' -> 自动调用dna-task-decomposer")
    print("  • '检查API接口一致性' -> 自动调用dna-dapi-checker")
    print("  • '对系统进行模块化重构' -> 自动调用dna-modulizer")
    
    return True

def uninstall_dnaspec_extensions():
    """卸载DNASPEC扩展"""
    print("=== DNASPEC Gemini CLI Extensions 卸载程序 ===")
    
    # 查找Gemini CLI目录
    gemini_dir = find_gemini_cli_directory()
    if not gemini_dir:
        print("警告: 未找到Gemini CLI安装目录")
        gemini_dir = input("请输入Gemini CLI安装目录路径: ").strip()
    
    if not os.path.exists(gemini_dir):
        print(f"错误: 目录 {gemini_dir} 不存在")
        return False
    
    # 删除扩展目录
    extensions_dir = os.path.join(gemini_dir, "extensions", "dnaspec")
    if os.path.exists(extensions_dir):
        shutil.rmtree(extensions_dir)
        print(f"删除扩展目录: {extensions_dir}")
    
    # 更新配置文件
    config_path = os.path.join(gemini_dir, "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            config = {}
        
        # 移除扩展
        if "extensions" in config:
            config["extensions"] = [
                ext for ext in config["extensions"] 
                if ext.get("name") != "dnaspec-gemini-extensions"
            ]
        
        # 保存配置
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"更新配置文件: {config_path}")
    
    print("\n=== 卸载完成 ===")
    print("DNASPEC扩展已从Gemini CLI中移除")
    
    return True

def main():
    """主函数"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "install":
            install_dnaspec_extensions()
        elif sys.argv[1] == "uninstall":
            uninstall_dnaspec_extensions()
        else:
            print("用法: python install.py [install|uninstall]")
    else:
        print("DNASPEC Gemini CLI Extensions 安装程序")
        print("用法:")
        print("  python install.py install    - 安装扩展")
        print("  python install.py uninstall  - 卸载扩展")

if __name__ == "__main__":
    main()