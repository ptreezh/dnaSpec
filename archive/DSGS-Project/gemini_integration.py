#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNASPEC Gemini CLI Extensions 集成脚本
用于将DSGS扩展集成到Gemini CLI中
"""

import os
import sys
import json
import shutil
from pathlib import Path

def find_gemini_config():
    """查找Gemini CLI配置文件"""
    # 常见的配置文件位置
    possible_paths = [
        os.path.expanduser("~/.gemini/config.json"),
        os.path.expanduser("~/gemini/config.json"),
        "/usr/local/gemini/config.json",
        "/opt/gemini/config.json"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # 检查环境变量
    gemini_home = os.environ.get("GEMINI_HOME")
    if gemini_home:
        config_path = os.path.join(gemini_home, "config.json")
        if os.path.exists(config_path):
            return config_path
    
    return None

def integrate_dsgs_extension():
    """集成DSGS扩展到Gemini CLI"""
    print("=== DNASPEC Gemini CLI Extensions 集成工具 ===")
    print()
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"DSGS扩展目录: {current_dir}")
    
    # 查找Gemini CLI配置文件
    config_path = find_gemini_config()
    if not config_path:
        print("未找到Gemini CLI配置文件")
        config_path = input("请输入Gemini CLI配置文件路径: ").strip()
    
    if not os.path.exists(config_path):
        print(f"错误: 配置文件 {config_path} 不存在")
        return False
    
    print(f"找到Gemini CLI配置文件: {config_path}")
    
    # 读取现有配置
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return False
    
    # 创建扩展目录
    gemini_dir = os.path.dirname(config_path)
    extensions_dir = os.path.join(gemini_dir, "extensions")
    dsgs_dir = os.path.join(extensions_dir, "dnaspec")
    
    os.makedirs(extensions_dir, exist_ok=True)
    print(f"创建扩展目录: {extensions_dir}")
    
    # 复制DSGS扩展文件
    print("复制DSGS扩展文件...")
    
    # 需要复制的文件和目录
    items_to_copy = [
        "gemini_skills_core.py",
        "gemini_intelligent_matcher.py", 
        "gemini_hook_handler.py",
        "gemini_skill_executor.py",
        "GEMINI_EXTENSION_CONFIG.json",
        "skills",
        "src"
    ]
    
    for item in items_to_copy:
        src_path = os.path.join(current_dir, item)
        dst_path = os.path.join(dsgs_dir, item)
        
        if os.path.exists(src_path):
            if os.path.isdir(src_path):
                if os.path.exists(dst_path):
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)
                print(f"  复制目录: {item}")
            else:
                shutil.copy2(src_path, dst_path)
                print(f"  复制文件: {item}")
        else:
            print(f"  警告: {item} 不存在")
    
    # 更新配置文件
    print("更新Gemini CLI配置...")
    
    # 确保extensions字段存在
    if "extensions" not in config:
        config["extensions"] = []
    
    # 检查是否已存在DSGS扩展
    dsgs_extension_exists = False
    for ext in config["extensions"]:
        if ext.get("name") == "dnaspec-gemini-extensions":
            ext["path"] = dsgs_dir
            ext["enabled"] = True
            ext["version"] = "1.0.0"
            dsgs_extension_exists = True
            break
    
    # 如果不存在，添加新的扩展配置
    if not dsgs_extension_exists:
        dsgs_extension = {
            "name": "dnaspec-gemini-extensions",
            "path": dsgs_dir,
            "enabled": True,
            "version": "1.0.0"
        }
        config["extensions"].append(dsgs_extension)
        print("  添加新的DSGS扩展配置")
    else:
        print("  更新现有DSGS扩展配置")
    
    # 保存配置文件
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"  配置文件已保存: {config_path}")
    except Exception as e:
        print(f"  保存配置文件失败: {e}")
        return False
    
    print("\n=== 集成完成 ===")
    print("DSGS扩展已成功集成到Gemini CLI中!")
    print()
    print("使用方法:")
    print("1. 在Gemini CLI中直接输入自然语言请求")
    print("2. 系统将自动匹配并执行相应的DSGS技能")
    print()
    print("支持的技能:")
    print("  • 智能体创建 (dnaspec-agent-creator)")
    print("  • 任务分解 (dnaspec-task-decomposer)")
    print("  • 接口检查 (dnaspec-dapi-checker)")
    print("  • 模块化 (dnaspec-modulizer)")
    print("  • 架构设计 (dnaspec-architect)")
    print()
    print("示例请求:")
    print("  • '设计微服务系统架构'")
    print("  • '创建项目管理智能体'")
    print("  • '检查API接口一致性'")
    print("  • '对订单处理模块进行成熟度评估'")
    
    return True

def remove_dsgs_extension():
    """移除DSGS扩展"""
    print("=== DNASPEC Gemini CLI Extensions 移除工具 ===")
    print()
    
    # 查找Gemini CLI配置文件
    config_path = find_gemini_config()
    if not config_path:
        print("未找到Gemini CLI配置文件")
        config_path = input("请输入Gemini CLI配置文件路径: ").strip()
    
    if not os.path.exists(config_path):
        print(f"错误: 配置文件 {config_path} 不存在")
        return False
    
    print(f"找到Gemini CLI配置文件: {config_path}")
    
    # 读取现有配置
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return False
    
    # 移除DSGS扩展配置
    if "extensions" in config:
        config["extensions"] = [
            ext for ext in config["extensions"] 
            if ext.get("name") != "dnaspec-gemini-extensions"
        ]
        print("移除DSGS扩展配置")
    
    # 保存配置文件
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"配置文件已更新: {config_path}")
    except Exception as e:
        print(f"保存配置文件失败: {e}")
        return False
    
    # 移除扩展目录
    gemini_dir = os.path.dirname(config_path)
    dsgs_dir = os.path.join(gemini_dir, "extensions", "dnaspec")
    
    if os.path.exists(dsgs_dir):
        try:
            shutil.rmtree(dsgs_dir)
            print(f"移除扩展目录: {dsgs_dir}")
        except Exception as e:
            print(f"移除扩展目录失败: {e}")
    
    print("\n=== 移除完成 ===")
    print("DSGS扩展已从Gemini CLI中移除!")
    
    return True

def main():
    """主函数"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ["install", "integrate"]:
            integrate_dsgs_extension()
        elif sys.argv[1] in ["uninstall", "remove"]:
            remove_dsgs_extension()
        else:
            print("用法:")
            print("  python gemini_integration.py install    - 安装并集成DSGS扩展")
            print("  python gemini_integration.py uninstall  - 移除DSGS扩展")
    else:
        print("DNASPEC Gemini CLI Extensions 集成工具")
        print()
        print("用法:")
        print("  python gemini_integration.py install    - 安装并集成DSGS扩展")
        print("  python gemini_integration.py uninstall  - 移除DSGS扩展")

if __name__ == "__main__":
    main()