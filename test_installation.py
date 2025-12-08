#!/usr/bin/env python3
"""
测试安装脚本 - 模拟 Node.js 脚本的执行过程
"""
import os
import sys
import subprocess
from pathlib import Path


def test_installation():
    """测试安装和配置过程"""
    print("🔍 测试 DNASPEC Context Engineering Skills 安装配置...")
    
    # 检查依赖
    print("\n📋 检查系统依赖...")
    try:
        # 检查Python
        print(f"✅ Python版本: {sys.version}")
        
        # 检查Git
        result = subprocess.run(['git', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Git版本: {result.stdout.strip()}")
        else:
            print("❌ 未找到Git")
            return False
    except Exception as e:
        print(f"❌ 依赖检查失败: {e}")
        return False

    # 测试Python包安装
    print("\n📦 测试Python包功能...")
    try:
        from src.dnaspec_context_engineering.skills_system_clean import ContextAnalysisSkill
        from src.dnaspec_spec_kit_integration.core.auto_configurator import AutoConfigurator
        
        print("✅ 成功导入DSGS模块")
        
        # 测试核心功能
        skill = ContextAnalysisSkill()
        result = skill.execute_with_ai('测试功能', {})
        print(f"✅ 核心功能测试: {'成功' if result['success'] else '失败'}")
        
        # 测试自动配置
        auto_config = AutoConfigurator()
        config_result = auto_config.quick_configure()
        print(f"✅ 自动配置测试: {'成功' if config_result['success'] else '失败'}")
        
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")
        return False


def test_encoding():
    """测试中文编码支持"""
    print("\n🌐 测试中文编码支持...")
    try:
        from src.dnaspec_context_engineering.skills_system_clean import ContextAnalysisSkill
        
        # 测试包含中文的输入
        skill = ContextAnalysisSkill()
        result = skill.execute_with_ai('测试中文编码支持和功能', {})
        
        if result['success']:
            print("✅ 中文编码支持正常")
            analysis = result['result']
            if 'metrics' in analysis:
                print(f"✅ 分析功能正常 - 清晰度: {analysis['metrics']['clarity']}")
                return True
            else:
                print("⚠️  分析结果格式异常")
                return False
        else:
            print(f"❌ 中文编码测试失败: {result.get('error', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 中文编码测试异常: {e}")
        return False


def main():
    """主测试函数"""
    print("="*60)
    print("DNASPEC Context Engineering Skills - 安装配置测试")
    print("="*60)
    
    # 设置环境变量以确保UTF-8编码
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
    os.environ.setdefault('LANG', 'en_US.UTF-8')
    
    print(f"编码设置: PYTHONIOENCODING={os.environ.get('PYTHONIOENCODING')}")
    
    # 执行测试
    install_success = test_installation()
    encoding_success = test_encoding()
    
    print("\n" + "="*60)
    print("测试结果总结:")
    print(f"  安装配置测试: {'✅ 通过' if install_success else '❌ 失败'}")
    print(f"  中文编码测试: {'✅ 通过' if encoding_success else '❌ 失败'}")
    
    overall_success = install_success and encoding_success
    print(f"  总体结果: {'✅ 成功' if overall_success else '❌ 失败'}")
    print("="*60)
    
    return overall_success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)