#!/usr/bin/env python3
"""
DSGS Context Engineering Skills - 最终安装验证脚本
验证在各种环境下能否正确执行配置脚本
"""

def verify_package_structure():
    """
    验证npm包的结构是否正确
    """
    import os
    import sys
    import platform
    
    print("DSGS Context Engineering Skills - 环境验证脚本")
    print("=" * 60)
    
    # 检查当前工作目录
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 检查系统中的AI CLI工具路径
    print("\n系统中AI CLI工具路径:")
    import shutil
    for tool in ['claude', 'qwen', 'gemini', 'cursor']:
        path = shutil.which(tool)
        print(f"  {tool}: {path}")
    
    # 检查Python模块路径
    print("\nPython模块路径检查:")
    import subprocess
    
    try:
        # 检查项目中的run_auto_config.py是否存在
        project_config_script = os.path.join(current_dir, 'run_auto_config.py')
        exists = os.path.exists(project_config_script)
        print(f"  run_auto_config.py (当前目录): {'✅' if exists else '❌'}")
        
        if exists:
            print(f"    路径: {project_config_script}")
        
        # 检查src目录下的配置脚本
        src_config_script = os.path.join(current_dir, 'src', 'dsgs_spec_kit_integration', 'cli.py')
        exists = os.path.exists(src_config_script)
        print(f"  cli.py (src目录): {'✅' if exists else '❌'}")
        
        if exists:
            print(f"    路径: {src_config_script}")
        
    except Exception as e:
        print(f"检查时发生错误: {e}")
    
    # 模拟index.js中的逻辑来验证路径
    print("\n模拟index.js中的路径解析逻辑:")
    print("1. 检测当前目录是否为项目目录...")
    
    is_project_dir = os.path.exists('src') and os.path.exists('pyproject.toml') and os.path.exists('package.json')
    print(f"   是否为项目目录: {'✅' if is_project_dir else '❌'}")
    
    if is_project_dir:
        print("   → 使用当前目录作为projectDir")
    else:
        print("   → 需要克隆项目到临时目录")
        
    # 检测全局安装时的环境
    print(f"\n模拟全局npm安装后的环境:")
    print(f"操作系统: {platform.system()}")
    print(f"Python版本: {sys.version}")
    
    # 尝试模拟npm全局安装后执行的路径
    print("\n全局npm安装后，index.js可能的执行逻辑:")
    npm_global_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'npm', 'node_modules', 'dnaspec')
    print(f"  NPM全局包路径 (Windows): {npm_global_path if os.path.exists(npm_global_path) else '[实际路径未知]'}")
    
    print("\n修复建议:")
    print("1. 确保全局npm包中包含所有必需的Python脚本")
    print("2. 修复index.js中的配置脚本路径逻辑")
    print("3. 确保run_auto_config.py在npm包中正确发布")
    
    return {
        'is_project_dir': is_project_dir,
        'current_directory': current_dir,
        'system_info': {
            'platform': platform.system(),
            'python_version': sys.version
        }
    }


def check_module_imports():
    """
    检查模块导入是否正常
    """
    print("\n" + "=" * 60)
    print("模块导入测试:")
    
    modules_to_test = [
        'src.dna_spec_kit_integration.core.cli_detector',
        'src.dna_spec_kit_integration.core.auto_configurator',
        'src.dna_context_engineering.skills_system_final',
        'src.dna_context_engineering.skills.context_analysis'
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")


def main():
    """主函数"""
    env_info = verify_package_structure()
    check_module_imports()
    
    print(f"\n验证完成!")
    print(f"当前环境: {env_info['system_info']['platform']}")
    print(f"是否为项目目录: {env_info['is_project_dir']}")


if __name__ == "__main__":
    main()