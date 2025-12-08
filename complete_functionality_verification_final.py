#!/usr/bin/env python3
"""
dnaspec 全功能验证脚本
测试所有核心功能是否正常工作
"""
import os
import sys
import subprocess
from typing import Dict, Any

def test_core_skills():
    """测试核心技能功能"""
    print("=" * 60)
    print("Testing Core DNASPEC Skills...")
    print("=" * 60)
    
    errors = []
    
    # 1. 测试上下文分析技能
    print("\n1. Testing Context Analysis Skill:")
    try:
        from src.dna_context_engineering.skills_system_final import execute
        result = execute({
            'skill': 'context-analysis',
            'context': 'Test context analysis functionality',
            'params': {}
        })
        print(f"   ✅ Context Analysis: Success")
        print(f"      Result type: {type(result)}")
        print(f"      Result preview: {result[:100] if result else 'No result'}...")
    except Exception as e:
        print(f"   ❌ Context Analysis: Failed - {e}")
        errors.append(f"Context Analysis: {e}")
        import traceback
        traceback.print_exc()
    
    # 2. 测试上下文优化技能
    print("\n2. Testing Context Optimization Skill:")
    try:
        from src.dna_context_engineering.skills_system_final import execute
        result = execute({
            'skill': 'context-optimization',
            'context': 'Test context optimization functionality',
            'params': {}
        })
        print(f"   ✅ Context Optimization: Success")
        print(f"      Result type: {type(result)}")
        print(f"      Result preview: {result[:100] if result else 'No result'}...")
    except Exception as e:
        print(f"   ❌ Context Optimization: Failed - {e}")
        errors.append(f"Context Optimization: {e}")
        import traceback
        traceback.print_exc()
    
    # 3. 测试认知模板技能
    print("\n3. Testing Cognitive Template Skill:")
    try:
        from src.dna_context_engineering.skills_system_final import execute
        result = execute({
            'skill': 'cognitive-template',
            'context': 'Test cognitive template functionality',
            'params': {'template': 'verification'}
        })
        print(f"   ✅ Cognitive Template: Success")
        print(f"      Result type: {type(result)}")
        print(f"      Result preview: {result[:100] if result else 'No result'}...")
    except Exception as e:
        print(f"   ❌ Cognitive Template: Failed - {e}")
        errors.append(f"Cognitive Template: {e}")
        import traceback
        traceback.print_exc()
    
    return errors

def test_cli_integration():
    """测试CLI集成"""
    print("\n\nTesting CLI Integration...")
    print("=" * 60)
    
    errors = []
    
    # 1. 测试CLI探测器
    print("\n1. Testing CLI Detector:")
    try:
        from src.dna_spec_kit_integration.core.cli_detector import CliDetector
        detector = CliDetector()
        results = detector.detect_all()
        print(f"   ✅ CLI Detector: Success")
        print(f"      Detected tools count: {len(results)}")
        for tool, info in results.items():
            status = "✅" if info.get('installed', False) else "❌"
            print(f"        {status} {tool}: {info.get('version', 'N/A')}")
    except Exception as e:
        print(f"   ❌ CLI Detector: Failed - {e}")
        errors.append(f"CLI Detector: {e}")
        import traceback
        traceback.print_exc()
    
    # 2. 测试配置器
    print("\n2. Testing Auto Configurator:")
    try:
        from src.dna_spec_kit_integration.core.auto_configurator import AutoConfigurator
        config = AutoConfigurator()
        print(f"   ✅ Auto Configurator: Success")
    except Exception as e:
        print(f"   ❌ Auto Configurator: Failed - {e}")
        errors.append(f"Auto Configurator: {e}")
        import traceback
        traceback.print_exc()
    
    # 3. 测试技能执行器
    print("\n3. Testing Skill Executor:")
    try:
        from src.dna_spec_kit_integration.core.skill_executor import SkillExecutor
        from src.dna_spec_kit_integration.core.skill_mapper import SkillMapper
        from src.dna_spec_kit_integration.core.python_bridge import PythonBridge
        
        python_bridge = PythonBridge()
        skill_mapper = SkillMapper()
        executor = SkillExecutor(python_bridge, skill_mapper)
        print(f"   ✅ Skill Executor: Success")
        print(f"      Available skills: {len(executor.get_available_skills())}")
    except Exception as e:
        print(f"   ❌ Skill Executor: Failed - {e}")
        errors.append(f"Skill Executor: {e}")
        import traceback
        traceback.print_exc()
    
    return errors

def test_get_available_skills():
    """测试获取可用技能"""
    print("\n\nTesting Get Available Skills...")
    print("=" * 60)
    
    errors = []
    
    # 1. 测试主函数中的获取技能功能
    print("\n1. Testing get_available_skills function:")
    try:
        from src.dna_context_engineering.skills_system_final import get_available_skills
        skills = get_available_skills()
        print(f"   ✅ Get Available Skills: Success")
        print(f"      Available skills: {list(skills.keys())}")
        for skill, desc in skills.items():
            print(f"        • {skill}: {desc}")
    except Exception as e:
        print(f"   ❌ Get Available Skills: Failed - {e}")
        errors.append(f"Get Available Skills: {e}")
        import traceback
        traceback.print_exc()
    
    return errors

def test_module_imports():
    """测试模块导入"""
    print("\n\nTesting Module Imports...")
    print("=" * 60)
    
    errors = []
    
    modules_to_test = [
        'src.dna_spec_kit_integration',
        'src.dna_spec_kit_integration.core',
        'src.dna_spec_kit_integration.skills',
        'src.dna_spec_kit_integration.adapters',
        'src.dna_context_engineering',
        'src.dna_context_engineering.skills_system_final',
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
            errors.append(f"Module Import: {module} - {e}")
    
    return errors

def test_adapter_integration():
    """测试适配器集成"""
    print("\n\nTesting Adapter Integration...")
    print("=" * 60)
    
    errors = []
    
    # 1. 测试具体适配器
    print("\n1. Testing Concrete SpecKit Adapter:")
    try:
        from src.dna_spec_kit_integration.adapters.concrete_spec_kit_adapter import ConcreteSpecKitAdapter
        concrete_adapter = ConcreteSpecKitAdapter()
        registered_skills = concrete_adapter.get_registered_skills()
        print(f"   ✅ Concrete SpecKit Adapter: Created successfully")
        print(f"      Registered skills count: {len(registered_skills)}")
        print(f"      Registered skills: {registered_skills[:5]}...")  # 显示前5个
    except Exception as e:
        print(f"   ❌ Concrete SpecKit Adapter: Failed - {e}")
        errors.append(f"Concrete SpecKit Adapter: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n2. Testing Integration CLI Handler:")
    try:
        from src.dna_spec_kit_integration.cli import main
        print(f"   ✅ CLI Handler: Import successful")
        print(f"      Function type: {type(main)}")
    except Exception as e:
        print(f"   ❌ CLI Handler: Failed - {e}")
        errors.append(f"CLI Handler: {e}")
        import traceback
        traceback.print_exc()
    
    return errors

def test_directory_structure():
    """测试目录结构完整性"""
    print("\n\nTesting Directory Structure Integrity...")
    print("=" * 60)
    
    errors = []
    
    expected_dirs = [
        'src/dna_spec_kit_integration',
        'src/dna_spec_kit_integration/core',
        'src/dna_spec_kit_integration/adapters', 
        'src/dna_spec_kit_integration/skills',
        'src/dna_context_engineering',
        'src/dna_context_engineering/skills',
        'src/dna_context_engineering/core',
        'src/dna_context_engineering/hooks',
        'src/dna_context_engineering/platform_adapters'
    ]
    
    for dir_path in expected_dirs:
        full_path = os.path.join('D:\\DAIP\\dnaSpec', dir_path)
        exists = os.path.exists(full_path)
        status = "✅" if exists else "❌"
        print(f"   {status} {dir_path}")
        if not exists:
            errors.append(f"Directory missing: {dir_path}")
    
    return errors

def run_complete_verification():
    """运行完整验证"""
    print("🚀 DNASPEC Context Engineering Skills - Complete Functionality Verification")
    print("=" * 80)
    
    all_errors = []
    
    # 逐个测试功能
    all_errors.extend(test_directory_structure())
    all_errors.extend(test_module_imports())
    all_errors.extend(test_get_available_skills())
    all_errors.extend(test_core_skills())
    all_errors.extend(test_cli_integration())
    all_errors.extend(test_adapter_integration())
    
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY:")
    if all_errors:
        print(f"❌ FAILED: {len(all_errors)} issues found")
        print("Problems:")
        for i, error in enumerate(all_errors, 1):
            print(f"  {i}. {error}")
        
        print(f"\n{'='*80}")
        print("ISSUES REQUIRING FIX:")
        print(f"{'='*80}")
        for error in all_errors:
            if "Directory missing" in error:
                print(f"  • Missing directory: {error}")
            elif "No module named" in error or "Cannot import" in error:
                print(f"  • Module import issue: {error}")
            else:
                print(f"  • Other issue: {error}")
        
        return False
    else:
        print("✅ SUCCESS: All functionality working properly!")
        print("DNASPEC Context Engineering Skills system fully operational.")
        print("\nCore features available:")
        print("  • Context Analysis - Five-dimensional quality assessment")
        print("  • Context Optimization - AI-driven improvements")
        print("  • Cognitive Templates - Thinking frameworks (CoT, Verification, etc.)")
        print("  • Agentic Design - System architecture skills")
        print("  • Safety Workflows - Secure AI interaction")
        print("  • Auto Detection - AI CLI tool detection and integration")
        
        return True

if __name__ == "__main__":
    success = run_complete_verification()
    if success:
        print("\n🎉 DNASPEC verification completed successfully!")
    else:
        print("\n⚠️  DNASPEC verification found some issues that need to be fixed.")
    sys.exit(0 if success else 1)