#!/usr/bin/env python3
"""
完整的DNASPEC功能验证脚本
测试所有核心功能是否正常工作
"""
import os
import sys
import subprocess
from typing import Dict, Any


def test_module_imports():
    """测试模块导入"""
    print("1. 测试模块导入...")
    modules_to_test = [
        ("src.dna_context_engineering.skills_system_final", "execute, get_available_skills"),
        ("src.dna_spec_kit_integration.core.cli_detector", "CliDetector"),
        ("src.dna_spec_kit_integration.core.skill", "DNASpecSkill"),
        ("src.dna_spec_kit_integration.adapters.spec_kit_adapter", "SpecKitAdapter"),
        ("src.dna_spec_kit_integration.adapters.concrete_spec_kit_adapter", "ConcreteSpecKitAdapter"),
        ("src.dna_spec_kit_integration.core.auto_configurator", "AutoConfigurator"),
        ("src.dna_spec_kit_integration.core.integration_validator", "IntegrationValidator")
    ]
    
    for module_path, objects in modules_to_test:
        try:
            result = subprocess.run([
                sys.executable, '-c', f'from {module_path} import {objects}; print(f"✅ {module_path} - 导入成功")'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(result.stdout.strip())
            else:
                print(f"❌ {module_path} - 导入失败: {result.stderr.strip()[:100]}")
        except Exception as e:
            print(f"❌ {module_path} - 测试错误: {e}")


def test_skill_execution():
    """测试技能执行"""
    print("\n2. 测试技能执行...")
    try:
        result = subprocess.run([
            sys.executable, '-c', '''
from src.dna_context_engineering.skills_system_final import execute
r = execute({"skill": "context-analysis", "context": "Test context for functionality verification"})
print("✅ Context Analysis Skill - 执行成功")
print(f"结果预览: {r[:100]}...")
            '''
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print(f"❌ Context Analysis Skill - 执行失败: {result.stderr.strip()[:100]}")
    except Exception as e:
        print(f"❌ Context Analysis Skill - 测试错误: {e}")


def test_available_skills():
    """测试可用技能列表"""
    print("\n3. 测试可用技能列表...")
    try:
        result = subprocess.run([
            sys.executable, '-c', '''
from src.dna_context_engineering.skills_system_final import get_available_skills
skills = get_available_skills()
print(f"✅ 可用技能: {list(skills.keys())}")
for skill, desc in skills.items():
    print(f"  • {skill}: {desc}")
            '''
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print(f"❌ 获取可用技能失败: {result.stderr.strip()[:100]}")
    except Exception as e:
        print(f"❌ 获取可用技能错误: {e}")


def test_cli_detection():
    """测试CLI检测器"""
    print("\n4. 测试CLI工具检测...")
    try:
        result = subprocess.run([
            sys.executable, '-c', '''
from src.dna_spec_kit_integration.core.cli_detector import CliDetector
detector = CliDetector()
results = detector.detect_all()
print(f"✅ CLI检测器运行成功，检测到{len(results)}个工具:")
for tool, info in results.items():
    status = "✅" if info.get("installed", False) else "❌"
    version = info.get("version", "Not installed")
    print(f"  {status} {tool}: {version}")
            '''
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print(f"❌ CLI检测器失败: {result.stderr.strip()[:100]}")
    except Exception as e:
        print(f"❌ CLI检测器错误: {e}")


def test_adapter_integration():
    """测试适配器集成"""
    print("\n5. 测试适配器集成...")
    try:
        result = subprocess.run([
            sys.executable, '-c', '''
from src.dna_spec_kit_integration.adapters.concrete_spec_kit_adapter import ConcreteSpecKitAdapter
adapter = ConcreteSpecKitAdapter()
registered_skills = adapter.get_registered_skills()
print(f"✅ 适配器集成成功，注册了{len(registered_skills)}个技能:")
for skill in registered_skills[:5]:  # 只显示前5个
    print(f"  • {skill}")
            '''
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            print(f"❌ 适配器集成失败: {result.stderr.strip()[:100]}")
    except Exception as e:
        print(f"❌ 适配器集成错误: {e}")


def main():
    """主函数"""
    print("="*60)
    print("🚀 DNASPEC Context Engineering Skills - 完整功能验证")
    print("="*60)
    
    test_module_imports()
    test_available_skills()
    test_skill_execution()
    test_cli_detection()
    test_adapter_integration()
    
    print("\n" + "="*60)
    print("✅ 所有功能测试完成！")
    print("如果所有测试都显示✅，则DNASPEC系统正常工作。")
    print("="*60)


if __name__ == "__main__":
    main()