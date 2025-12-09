#!/usr/bin/env python3
"""
DSGS功能验证 - 直接运行模式
无subprocess调用，直接验证模块功能
"""

from src.dna_context_engineering.skills_system_final import execute, get_available_skills
from src.dna_spec_kit_integration.core.cli_detector import CliDetector
from src.dna_spec_kit_integration.adapters.concrete_spec_kit_adapter import ConcreteSpecKitAdapter


def test_direct_imports():
    """直接测试模块导入"""
    print("="*60)
    print("🚀 DNASPEC Context Engineering Skills - 功能验证")
    print("="*60)
    
    print("\n1. 模块直接导入测试:")
    
    # 测试1: 核心技能模块
    try:
        skills = get_available_skills()
        print(f"   ✅ Core Skills Module: {list(skills.keys())}")
    except Exception as e:
        print(f"   ❌ Core Skills Module: {e}")
    
    # 测试2: CLI检测器
    try:
        detector = CliDetector()
        print("   ✅ CLI Detector Module: Imported successfully")
    except Exception as e:
        print(f"   ❌ CLI Detector Module: {e}")
    
    # 测试3: 适配器
    try:
        adapter = ConcreteSpecKitAdapter()
        print("   ✅ Adapter Module: Imported successfully")
    except Exception as e:
        print(f"   ❌ Adapter Module: {e}")


def test_skill_execution():
    """测试技能执行"""
    print("\n2. 技能执行测试:")
    
    try:
        # 测试上下文分析
        result = execute({
            'skill': 'context-analysis',
            'context': 'Test DNASPEC skills functionality',
            'params': {}
        })
        print("   ✅ Context Analysis Skill: Executed successfully")
        print(f"     Result preview: {result[:80]}...")
    except Exception as e:
        print(f"   ❌ Context Analysis Skill: {e}")
        
    try:
        # 测试上下文优化
        result = execute({
            'skill': 'context-optimization',
            'context': 'Test context',
            'params': {}
        })
        print("   ✅ Context Optimization Skill: Executed successfully")
        print(f"     Result preview: {result[:80]}...")
    except Exception as e:
        print(f"   ❌ Context Optimization Skill: {e}")
        
    try:
        # 测试认知模板
        result = execute({
            'skill': 'cognitive-template',
            'context': 'Apply cognitive template to task',
            'params': {'template': 'chain_of_thought'}
        })
        print("   ✅ Cognitive Template Skill: Executed successfully")
        print(f"     Result preview: {result[:80]}...")
    except Exception as e:
        print(f"   ❌ Cognitive Template Skill: {e}")


def test_cli_detection():
    """测试CLI检测功能"""
    print("\n3. AI CLI工具检测测试:")
    
    try:
        detector = CliDetector()
        results = detector.detect_all()
        print(f"   ✅ CLI Detector: Detected {len(results)} tools")
        
        for tool, info in results.items():
            status = "✅" if info.get('installed', False) else "❌"
            version = info.get('version', 'N/A')
            print(f"     {status} {tool}: {version}")
            
    except Exception as e:
        print(f"   ❌ CLI Detection failed: {e}")
        import traceback
        traceback.print_exc()


def test_adapter_functionality():
    """测试适配器功能"""
    print("\n4. 适配器功能测试:")
    
    try:
        adapter = ConcreteSpecKitAdapter()
        registered_skills = adapter.get_registered_skills()
        print(f"   ✅ Adapter: Created successfully with {len(registered_skills)} registered skills")
        print(f"     Sample skills: {registered_skills[:5]}")  # 显示前5个
    except Exception as e:
        print(f"   ❌ Adapter functionality failed: {e}")


def main():
    """主函数"""
    print("DSGS Context Engineering Skills - Direct Functionality Validation")
    print("Testing all core features without subprocess to avoid encoding issues...")
    print()
    
    test_direct_imports()
    test_skill_execution()
    test_cli_detection()
    test_adapter_functionality()
    
    print()
    print("="*60)
    print("✅ DNASPEC系统功能验证完成！")
    print("如果大部分测试显示✅，则系统功能正常。")
    print("="*60)


if __name__ == "__main__":
    main()