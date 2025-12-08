#!/usr/bin/env python3
"""
测试DNASPEC技能适配器
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.dnaspec_spec_kit_integration.adapters.concrete_spec_kit_adapter import ConcreteSpecKitAdapter
from src.dnaspec_context_engineering.skills_system_final import ContextAnalysisSkill, ContextOptimizationSkill, CognitiveTemplateSkill

def test_adapter():
    print("测试DNASPEC适配器...")
    
    # 创建适配器
    adapter = ConcreteSpecKitAdapter()
    
    # 注册上下文工程技能
    def context_analysis_wrapper(params):
        skill = ContextAnalysisSkill()
        return skill.process_request(params.get("params", ""), params)
    
    def context_optimization_wrapper(params):
        skill = ContextOptimizationSkill()
        return skill.process_request(params.get("params", ""), params)
    
    def cognitive_template_wrapper(params):
        skill = CognitiveTemplateSkill()
        return skill.process_request(params.get("params", ""), params)
    
    # 注册核心技能
    adapter.register_skill("dnaspec-context-analysis", context_analysis_wrapper)
    adapter.register_skill("dnaspec-context-optimization", context_optimization_wrapper)
    adapter.register_skill("dnaspec-cognitive-template", cognitive_template_wrapper)
    
    print(f"已注册技能: {adapter.get_registered_skills()}")
    
    # 测试命令解析
    test_command = "/speckit.dnaspec.context-analysis 测试上下文内容"
    parsed = adapter.parse_command(test_command)
    print(f"命令解析: {test_command}")
    print(f"解析结果: {parsed}")
    
    # 测试命令执行
    try:
        result = adapter.execute_command(test_command)
        print(f"执行结果: {result}")
    except Exception as e:
        print(f"执行异常: {e}")
    
    # 再测试一个命令
    test_command2 = "/speckit.dnaspec.context-optimization 优化这个"
    parsed2 = adapter.parse_command(test_command2)
    print(f"\n命令解析: {test_command2}")
    print(f"解析结果: {parsed2}")
    
    try:
        result2 = adapter.execute_command(test_command2)
        print(f"执行结果: {result2}")
    except Exception as e:
        print(f"执行异常: {e}")

if __name__ == "__main__":
    test_adapter()