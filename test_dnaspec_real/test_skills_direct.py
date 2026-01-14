#!/usr/bin/env python3
"""
直接测试 DNASPEC 技能
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, 'D:/DAIP/dnaSpec')

from src.dna_spec_kit_integration.core.skill_executor import SkillExecutor
from src.dna_spec_kit_integration.core.python_bridge import PythonBridge
from src.dna_spec_kit_integration.core.skill_mapper import SkillMapper

def test_skill(skill_name, params):
    """测试单个技能"""
    print(f"\n{'='*60}")
    print(f"测试技能: {skill_name}")
    print(f"{'='*60}")
    print(f"参数: {params}")
    print(f"{'-'*60}")

    try:
        # 创建执行器
        python_bridge = PythonBridge()
        skill_mapper = SkillMapper()
        executor = SkillExecutor(python_bridge, skill_mapper)

        # 执行技能
        result = executor.execute(skill_name, params)

        # 显示结果
        if result['success']:
            print(f"\n✅ 成功!")
            print(f"\n结果:\n{result['result']}")
        else:
            print(f"\n❌ 失败!")
            print(f"错误: {result.get('error', 'Unknown error')}")

        return result

    except Exception as e:
        print(f"\n❌ 异常: {str(e)}")
        return {'success': False, 'error': str(e)}

def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("DNASPEC 技能直接测试")
    print("="*60)

    # 测试场景
    test_cases = [
        {
            'skill': 'task-decomposer',
            'params': '开发一个待办事项应用，需要包含添加、完成、删除和分类功能',
            'description': '任务分解技能测试'
        },
        {
            'skill': 'architect',
            'params': '为一个个人博客系统设计系统架构，需要支持用户认证、文章管理和评论功能',
            'description': '系统架构技能测试'
        },
        {
            'skill': 'agent-creator',
            'params': '创建一个自动化代码审查代理，能够检查代码质量和安全问题',
            'description': '代理创建技能测试'
        },
        {
            'skill': 'constraint-generator',
            'params': '为用户登录功能生成安全约束，包括密码策略和会话管理',
            'description': '约束生成技能测试'
        }
    ]

    results = []

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n\n测试 {i}/{len(test_cases)}: {test_case['description']}")
        result = test_skill(test_case['skill'], test_case['params'])
        results.append({
            'test': test_case['description'],
            'skill': test_case['skill'],
            'success': result.get('success', False),
            'result': result
        })

    # 生成测试报告
    print("\n\n" + "="*60)
    print("测试总结")
    print("="*60)

    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)

    print(f"\n总测试数: {total_count}")
    print(f"成功: {success_count}")
    print(f"失败: {total_count - success_count}")
    print(f"成功率: {success_count/total_count*100:.1f}%")

    print("\n详细结果:")
    for r in results:
        status = "✅ 通过" if r['success'] else "❌ 失败"
        print(f"  {status} - {r['test']} ({r['skill']})")

if __name__ == '__main__':
    main()
