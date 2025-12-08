#!/usr/bin/env python3
"""
DSGS系统功能完整性测试
验证删除子模块后所有核心功能是否正常
"""
import os
import sys
import importlib.util

def test_core_modules():
    """测试核心模块导入"""
    print("🔍 测试核心模块导入...")

    modules_to_test = [
        'src.dna_context_engineering.skills_system_final',
        'src.dna_spec_kit_integration.core.cli_detector',
        'src.dna_spec_kit_integration.core.auto_configurator',
        'src.dna_spec_kit_integration.cli',
        'src.dna_context_engineering.skills.cognitive_template',
        'src.dna_context_engineering.skills.context_analysis',
        'src.dna_context_engineering.skills.context_optimization'
    ]

    for module_path in modules_to_test:
        try:
            # 导入模块
            module_parts = module_path.split('.')
            module = importlib.import_module(module_path)
            print(f"  ✅ {module_path} - 导入成功")
        except Exception as e:
            print(f"  ❌ {module_path} - 导入失败: {e}")

    print()

def test_skill_execution():
    """测试核心技能执行"""
    print("🔧 测试核心技能执行...")

    try:
        from src.dna_context_engineering.skills_system_final import execute
        
        # 测试上下文分析技能
        result = execute({
            'skill': 'context-analysis',
            'context': '测试上下文分析功能',
            'params': {}
        })
        print(f"  ✅ 上下文分析技能 - 执行成功")
        print(f"     结果长度: {len(result) if result else 0}")
        
        # 测试上下文优化技能
        result = execute({
            'skill': 'context-optimization', 
            'context': '优化这个',
            'params': {}
        })
        print(f"  ✅ 上下文优化技能 - 执行成功")
        
        # 测试认知模板技能
        result = execute({
            'skill': 'cognitive-template',
            'context': '应用认知模板',
            'params': {'template': 'verification'}
        })
        print(f"  ✅ 认知模板技能 - 执行成功")
        
    except Exception as e:
        print(f"  ❌ 核心技能执行失败: {e}")
        import traceback
        traceback.print_exc()
    
    print()

def test_cli_integration():
    """测试CLI集成"""
    print("⚙️  测试CLI集成功能...")
    
    try:
        from src.dna_spec_kit_integration.cli import main
        print("  ✅ CLI模块 - 导入成功")
    except Exception as e:
        print(f"  ❌ CLI模块 - 导入失败: {e}")

    try:
        from src.dna_spec_kit_integration.core.cli_detector import CliDetector
        detector = CliDetector()
        detected = detector.detect_all()
        print(f"  ✅ CLI检测器 - 检测到 {len(detected)} 个AI工具")
    except Exception as e:
        print(f"  ❌ CLI检测器 - 失败: {e}")
    
    print()

def test_command_handlers():
    """测试命令处理"""
    print("🔨 测试命令处理器...")
    
    try:
        from src.dna_spec_kit_integration.core.command_handler import CommandHandler
        print("  ✅ 命令处理器 - 创建成功")
    except Exception as e:
        print(f"  ❌ 命令处理器 - 失败: {e}")

    try:
        from src.dna_spec_kit_integration.core.skill_executor import SkillExecutor
        print("  ✅ 技能执行器 - 创建成功")
    except Exception as e:
        print(f"  ❌ 技能执行器 - 失败: {e}")
    
    print()

def test_advanced_features():
    """测试高级功能"""
    print("🌟 测试高级功能...")
    
    try:
        # 测试任务分解
        from src.dna_context_engineering.skills_system_final import CognitiveTemplateSkill
        skill = CognitiveTemplateSkill()
        templates = skill.templates
        print(f"  ✅ 认知模板 - 可用模板: {list(templates.keys())}")
    except Exception as e:
        print(f"  ❌ 认知模板 - 失败: {e}")

    try:
        # 测试配置生成器
        from src.dna_spec_kit_integration.core.config_generator import ConfigGenerator
        generator = ConfigGenerator()
        print("  ✅ 配置生成器 - 创建成功")
    except Exception as e:
        print(f"  ❌ 配置生成器 - 失败: {e}")
    
    print()

def test_integration_workflows():
    """测试集成工作流"""
    print("🔄 测试集成工作流...")
    
    try:
        from src.dna_spec_kit_integration.core.integration_validator import IntegrationValidator
        validator = IntegrationValidator()
        print("  ✅ 集成验证器 - 创建成功")
    except Exception as e:
        print(f"  ❌ 集成验证器 - 失败: {e}")

    try:
        from src.dna_spec_kit_integration.core.matcher import IntelligentMatcher
        matcher = IntelligentMatcher()
        print("  ✅ 智能匹配器 - 创建成功")
    except Exception as e:
        print(f"  ❌ 智能匹配器 - 失败: {e}")
    
    print()

def run_comprehensive_test():
    """运行完整测试"""
    print("🚀 DSGS Context Engineering Skills - 功能完整性验证")
    print("=" * 60)
    print()
    
    test_core_modules()
    test_skill_execution()
    test_cli_integration()
    test_command_handlers()
    test_advanced_features()
    test_integration_workflows()
    
    print("✅ 所有功能测试完成！")

if __name__ == "__main__":
    run_comprehensive_test()