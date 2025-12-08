#!/usr/bin/env python3
"""
项目目录环境检测脚本
用于诊断在项目目录下CLI工具检测失败的问题
"""
import subprocess
import platform
import os
import sys
import shutil

def test_path_accessibility():
    """测试命令在PATH中的可访问性"""
    print("=== PATH环境测试 ===")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python版本: {sys.version}")
    print(f"操作系统: {platform.system()}")
    
    # 检查PATH中的路径
    path_dirs = os.environ.get('PATH', '').split(os.pathsep)
    print(f"PATH数量: {len(path_dirs)}")
    
    # 检查npm全局路径
    npm_global_path = r"C:\npm_global"
    print(f"npm全局路径存在: {os.path.exists(npm_global_path)}")
    
    # 检查npm_global下是否有AI工具
    if os.path.exists(npm_global_path):
        ai_tools = []
        for file in os.listdir(npm_global_path):
            if file in ['claude', 'qwen', 'gemini', 'copilot']:
                ai_tools.append(file)
        print(f"npm_global中的AI工具: {ai_tools}")
    
    return npm_global_path

def test_command_availability():
    """测试命令是否可用"""
    print("\n=== 命令可用性测试 ===")
    
    ai_tools = ['claude', 'gemini', 'qwen', 'copilot', 'cursor']
    
    for tool in ai_tools:
        # 方法1: 使用shutil.which
        tool_path = shutil.which(tool)
        print(f"{tool}: {tool_path}")
        
        # 方法2: 尝试运行
        try:
            result = subprocess.run(
                [tool, '--version'], 
                capture_output=True, 
                text=True,
                timeout=10,
                shell=(platform.system() == 'Windows')
            )
            status = "✅" if result.returncode == 0 else "❌"
            print(f"  {status} 运行测试: 退出码={result.returncode}, 输出={result.stdout.strip()[:50]}")
            if result.stderr.strip():
                print(f"     错误: {result.stderr.strip()[:50]}")
        except Exception as e:
            print(f"  ❌ 异常: {e}")

def test_subprocess_with_different_methods():
    """测试不同的subprocess调用方法"""
    print("\n=== subprocess方法对比测试 ===")
    
    # 方法1: 直接运行（当前实现）
    print("方法1 - 直接运行:")
    try:
        result = subprocess.run(
            ['claude', '--version'],
            capture_output=True,
            text=True,
            timeout=10,
            shell=(platform.system() == 'Windows')
        )
        print(f"  返回码: {result.returncode}")
        print(f"  输出: {result.stdout.strip()[:100]}")
        if result.stderr.strip():
            print(f"  错误: {result.stderr.strip()[:100]}")
    except Exception as e:
        print(f"  异常: {e}")
    
    # 方法2: 使用where/call命令
    print("\n方法2 - 使用where命令:")
    try:
        if platform.system() == 'Windows':
            result = subprocess.run(
                ['where', 'claude'],
                capture_output=True,
                text=True,
                shell=True
            )
            if result.returncode == 0:
                tool_path = result.stdout.strip().split('\n')[0]
                print(f"  工具路径: {tool_path}")
                
                # 尝试直接运行获取的路径
                path_result = subprocess.run(
                    [tool_path, '--version'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                print(f"  路径测试结果: 退出码={path_result.returncode}, 输出={path_result.stdout.strip()[:100]}")
    except Exception as e:
        print(f"  异常: {e}")

def test_environment_isolation():
    """测试环境隔离问题"""
    print("\n=== 环境隔离测试 ===")
    
    # 检查当前目录的Python包环境
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'list'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        has_dnaspec = 'dnaspec' in result.stdout.lower()
        print(f"当前目录Python环境是否有dnaspec包: {has_dnaspec}")
    except Exception as e:
        print(f"检查包环境时出错: {e}")

def main():
    print("DNASPEC CLI工具检测问题诊断工具")
    print("=" * 50)
    
    npm_path = test_path_accessibility()
    test_command_availability()
    test_subprocess_with_different_methods()
    test_environment_isolation()
    
    print("\n=== 问题诊断总结 ===")
    print("如果在项目目录中检测失败，但其他目录中正常，可能的原因：")
    print("1. 项目目录的Python环境与全局环境不一致")
    print("2. 项目目录中存在优先级更高的本地代码")
    print("3. 项目目录的环境变量被修改")
    print("4. editable安装模式导致的路径混淆")

if __name__ == "__main__":
    main()