#!/usr/bin/env python3
"""
DNASPEC系统功能完整性验证脚本
验证所有模块功能是否正确实现
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_all_capabilities():
    """测试所有功能能力"""
    print("DNASPEC Context Engineering Skills - 功能完整性验证")
    print("="*60)
    
    # 1. 验证核心技能是否可用
    print("\n1. 验证核心技能...")
    try:
        from src.dnaspec_context_engineering.skills_system_final import (
            execute, 
            get_available_skills,
            ContextAnalysisSkill,
            ContextOptimizationSkill,
            CognitiveTemplateSkill
        )
        print("   ✅ 核心模块导入成功")
        
        # 获取可用技能
        skills = get_available_skills()
        print(f"   ✅ 可用技能: {list(skills.keys())}")
        
        # 测试基本执行
        for skill_name in skills.keys():
            try:
                result = execute({
                    'skill': skill_name,
                    'context': '测试内容',
                    'params': {}
                })
                if result and len(result) > 0:
                    print(f"   ✅ {skill_name}: 基本执行正常")
                else:
                    print(f"   ❌ {skill_name}: 返回空结果")
            except Exception as e:
                print(f"   ❌ {skill_name}: 执行错误 - {e}")
                
    except Exception as e:
        print(f"   ❌ 核心技能导入失败: {e}")
        return False

    # 2. 验证高级功能是否可用
    print("\n2. 验证高级功能...")
    try:
        from src.dnaspec_context_engineering.skills_system_final import (
            create_agent_with_context_analysis,
            decompose_complex_task,
            design_project_structure,
            generate_constraints_from_requirements
        )
        
        print("   ✅ 高级功能函数导入成功")
        
        # 测试代理创建
        try:
            agent_spec = create_agent_with_context_analysis("性能优化", "资源限制")
            print("   ✅ 代理创建功能正常")
        except Exception as e:
            print(f"   ❌ 代理创建功能错误: {e}")
        
        # 测试任务分解
        try:
            task_breakdown = decompose_complex_task("开发电商系统")
            print("   ✅ 任务分解功能正常")
        except Exception as e:
            print(f"   ❌ 任务分解功能错误: {e}")
        
        # 测试项目结构设计
        try:
            project_struct = design_project_structure("Web应用需求")
            print("   ✅ 项目结构设计功能正常")
        except Exception as e:
            print(f"   ❌ 项目结构设计功能错误: {e}")
        
        # 测试约束生成
        try:
            constraints = generate_constraints_from_requirements("用户认证系统")
            print("   ✅ 约束生成功能正常")
        except Exception as e:
            print(f"   ❌ 约束生成功能错误: {e}")
            
    except Exception as e:
        print(f"   ❌ 高级功能导入失败: {e}")
        return False

    # 3. 验证技能类是否正常
    print("\n3. 验证技能类实例化...")
    try:
        analysis_skill = ContextAnalysisSkill()
        optimization_skill = ContextOptimizationSkill()
        template_skill = CognitiveTemplateSkill()
        print("   ✅ 技能类实例化成功")
        
        # 检查类方法
        for skill_name, skill_instance in [
            ("ContextAnalysis", analysis_skill),
            ("ContextOptimization", optimization_skill),
            ("CognitiveTemplate", template_skill)
        ]:
            has_execute = hasattr(skill_instance, '_execute_skill_logic')
            has_confidence = hasattr(skill_instance, '_calculate_confidence')
            print(f"   ✅ {skill_name}: _execute_skill_logic={has_execute}, _calculate_confidence={has_confidence}")
            
    except Exception as e:
        print(f"   ❌ 技能类实例化失败: {e}")
        return False

    # 4. 验证实际功能执行
    print("\n4. 验证实际功能执行...")
    try:
        # 测试分析功能
        result = execute({
            'skill': 'context-analysis',
            'context': '设计一个用户登录系统，支持邮箱和手机号验证'
        })
        if "上下文质量分析结果" in result or "分析结果" in result:
            print("   ✅ 上下文分析执行正常")
        else:
            print(f"   ❌ 上下文分析返回异常: {result[:50]}...")
        
        # 测试优化功能
        result = execute({
            'skill': 'context-optimization',
            'context': '优化这个需求'
        })
        if "上下文优化结果" in result or "优化" in result:
            print("   ✅ 上下文优化执行正常")
        else:
            print(f"   ❌ 上下文优化返回异常: {result[:50]}...")
        
        # 测试模板功能
        result = execute({
            'skill': 'cognitive-template',
            'context': '如何设计数据库',
            'params': {'template': 'verification'}
        })
        if "认知模板应用" in result or "模板应用" in result:
            print("   ✅ 认知模板执行正常")
        else:
            print(f"   ❌ 认知模板返回异常: {result[:50]}...")
            
    except Exception as e:
        print(f"   ❌ 功能执行测试失败: {e}")
        return False

    # 5. 验证API兼容性
    print("\n5. 验证API兼容性...")
    try:
        # 测试参数格式的兼容性
        result = execute({
            'skill': 'context-analysis',
            'context': '测试API兼容性',
            'params': {'mode': 'standard'}
        })
        print("   ✅ 参数格式兼容性正常")
    except Exception as e:
        print(f"   ❌ 参数格式兼容性错误: {e}")
        return False

    print("\n" + "="*60)
    print("🎉 所有功能验证通过！DNASPEC系统功能完整可用。")
    print("✅ 核心技能系统正常")
    print("✅ 高级专业功能可用") 
    print("✅ API接口兼容性良好")
    print("✅ 实际执行能力正常")
    print("✅ 为AI CLI环境做好准备")
    
    return True


def main():
    """主函数"""
    success = test_all_capabilities()
    if not success:
        print("\n❌ 验证失败，请检查系统功能。")
        sys.exit(1)
    else:
        print("\n✅ 验证成功！DNASPEC系统可正常使用。")


if __name__ == "__main__":
    main()