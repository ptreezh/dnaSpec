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
    print("\\n1. Testing Context Analysis Skill:")
    try:
        from src.dna_context_engineering.skills_system_final import ContextAnalysisSkill
        skill = ContextAnalysisSkill()
        result = skill.process_request("Test context analysis", {})
        print(f"   ✅ Context Analysis: Success")
        print(f"      Result type: {type(result)}")
    except Exception as e:
        print(f"   ❌ Context Analysis: Failed - {e}")
        errors.append(f"Context Analysis: {e}")
    
    # 2. 测试上下文优化技能
    print("\\n2. Testing Context Optimization Skill:")
    try:
        from src.dna_context_engineering.skills_system_final import ContextOptimizationSkill
        skill = ContextOptimizationSkill()
        result = skill.process_request("Test context optimization", {})
        print(f"   ✅ Context Optimization: Success")
        print(f"      Result type: {type(result)}")
    except Exception as e:
        print(f"   ❌ Context Optimization: Failed - {e}")
        errors.append(f"Context Optimization: {e}")
    
    # 3. 测试认知模板技能
    print("\\n3. Testing Cognitive Template Skill:")
    try:
        from src.dna_context_engineering.skills_system_final import CognitiveTemplateSkill
        skill = CognitiveTemplateSkill()
        result = skill.process_request("Test cognitive template", {})
        print(f"   ✅ Cognitive Template: Success")
        print(f"      Result type: {type(result)}")
    except Exception as e:
        print(f"   ❌ Cognitive Template: Failed - {e}")
        errors.append(f"Cognitive Template: {e}")
    
    # 4. 测试执行函数
    print("\\n4. Testing Main Execute Function:")
    try:
        from src.dna_context_engineering.skills_system_final import execute
        result = execute({'skill': 'context-analysis', 'context': 'Test execution'})
        print(f"   ✅ Main Execute: Success")
        print(f"      Result length: {len(result) if result else 0}")
    except Exception as e:
        print(f"   ❌ Main Execute: Failed - {e}")
        errors.append(f"Main Execute: {e}")
    
    return errors

def test_cli_integration():
    """测试CLI集成"""
    print("\\n\\nTesting CLI Integration...")
    print("=" * 60)
    
    errors = []
    
    # 1. 测试CLI探测器
    print("\\n1. Testing CLI Detector:")
    try:
        from src.dna_spec_kit_integration.core.cli_detector import CliDetector
        detector = CliDetector()
        results = detector.detect_all()
        print(f"   ✅ CLI Detector: Success")
        print(f"      Detected tools: {len(results)}")
        for tool, info in results.items():
            status = "✅" if info.get('installed', False) else "❌"
            print(f"        {status} {tool}: {info.get('version', 'N/A')}")
    except Exception as e:
        print(f"   ❌ CLI Detector: Failed - {e}")
        errors.append(f"CLI Detector: {e}")
    
    # 2. 测试配置器
    print("\\n2. Testing Auto Configurator:")
    try:
        from src.dna_spec_kit_integration.core.auto_configurator import AutoConfigurator
        config = AutoConfigurator()
        print(f"   ✅ Auto Configurator: Success")
    except Exception as e:
        print(f"   ❌ Auto Configurator: Failed - {e}")
        errors.append(f"Auto Configurator: {e}")
    
    # 3. 测试技能执行器
    print("\\n3. Testing Skill Executor:")
    try:
        from src.dna_spec_kit_integration.core.skill_executor import SkillExecutor
        from src.dna_spec_kit_integration.core.python_bridge import PythonBridge
        executor = SkillExecutor(PythonBridge())
        print(f"   ✅ Skill Executor: Success")
    except Exception as e:
        print(f"   ❌ Skill Executor: Failed - {e}")
        errors.append(f"Skill Executor: {e}")
    
    return errors

def test_available_skills():
    """测试可用技能列表"""
    print("\\n\\nTesting Available Skills...")
    print("=" * 60)
    
    errors = []
    
    # 1. 测试获取可用技能
    print("\\n1. Testing Get Available Skills Function:")
    try:
        from src.dna_context_engineering.skills_system_final import get_available_skills
        skills = get_available_skills()
        print(f"   ✅ Get Available Skills: Success")
        print(f"      Available skills: {list(skills.keys())}")
        
        # 2. 测试每个可用技能
        for skill_name, desc in skills.items():
            print(f"   Testing {skill_name}...")
            try:
                result = execute({'skill': skill_name, 'context': 'Test context'})
                print(f"      ✅ {skill_name}: Executable")
            except Exception as e:
                print(f"      ❌ {skill_name}: Failed - {e}")
                errors.append(f"{skill_name}: {e}")
    except Exception as e:
        print(f"   ❌ Get Available Skills: Failed - {e}")
        errors.append(f"Get Available Skills: {e}")
    
    return errors

def test_module_imports():
    """测试模块导入"""
    print("\\n\\nTesting Module Imports...")
    print("=" * 60)
    
    errors = []
    
    modules_to_test = [
        'src.dna_spec_kit_integration',
        'src.dna_spec_kit_integration.cli',
        'src.dna_spec_kit_integration.core',
        'src.dna_spec_kit_integration.core.cli_detector',
        'src.dna_spec_kit_integration.core.auto_configurator',
        'src.dna_spec_kit_integration.core.skill',
        'src.dna_spec_kit_integration.core.command_handler',
        'src.dna_context_engineering',
        'src.dna_context_engineering.skills_system_final',
        'src.dna_context_engineering.skills.context_analysis',
        'src.dna_context_engineering.skills.context_optimization',
        'src.dna_context_engineering.skills.cognitive_template'
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
    print("\\n\\nTesting Adapter Integration...")
    print("=" * 60)
    
    errors = []
    
    # 1. 测试适配器
    print("\\n1. Testing SpecKit Adapter:") 
    try:
        from src.dna_spec_kit_integration.adapters.spec_kit_adapter import SpecKitAdapter
        adapter = SpecKitAdapter()
        print(f"   ✅ SpecKit Adapter: Created successfully")
        print(f"      Registered skills: {len(adapter.get_registered_skills())}")
    except Exception as e:
        print(f"   ❌ SpecKit Adapter: Failed - {e}")
        errors.append(f"SpecKit Adapter: {e}")
    
    # 2. 测试具体适配器
    print("\\n2. Testing Concrete SpecKit Adapter:")
    try:
        from src.dna_spec_kit_integration.adapters.concrete_spec_kit_adapter import ConcreteSpecKitAdapter
        concrete_adapter = ConcreteSpecKitAdapter()
        print(f"   ✅ Concrete SpecKit Adapter: Created successfully")
        print(f"      Registered skills count: {len(concrete_adapter.get_registered_skills())}")
        print(f"      Registered skills: {concrete_adapter.get_registered_skills()[:5]}...")  # 显示前5个
    except Exception as e:
        print(f"   ❌ Concrete SpecKit Adapter: Failed - {e}")
        errors.append(f"Concrete SpecKit Adapter: {e}")
    
    return errors

def run_complete_verification():
    """运行完整验证"""
    print("🚀 DNASPEC Context Engineering Skills - Complete Functionality Verification")
    print("=" * 80)
    
    all_errors = []
    
    # 逐个测试功能
    all_errors.extend(test_module_imports())
    all_errors.extend(test_core_skills())
    all_errors.extend(test_cli_integration())
    all_errors.extend(test_available_skills())
    all_errors.extend(test_adapter_integration())
    
    print("\\n" + "=" * 80)
    print("VERIFICATION SUMMARY:")
    if all_errors:
        print(f"❌ FAILED: {len(all_errors)} errors found")
        for error in all_errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ SUCCESS: All functionality working properly!")
        print("DNASPEC Context Engineering Skills system fully operational.")
        return True

if __name__ == "__main__":
    success = run_complete_verification()
    sys.exit(0 if success else 1)