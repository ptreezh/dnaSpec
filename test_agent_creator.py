import sys
from pathlib import Path

skills_dir = Path(__file__).parent / 'skills' / 'dnaspec-agent-creator'
sys.path.insert(0, str(skills_dir))

from scripts.executor import AgentCreatorExecutor

def test_basic_execution():
    print('\n' + '='*70)
    print('测试: 基本执行功能')
    print('='*70)

    executor = AgentCreatorExecutor()
    result = executor.execute('请创建一个代码审查智能体')

    assert result['success'] == True
    print(f'✅ 提示词层次: {result["prompt_level"]}')
    print('✅ 测试通过')

def test_agent_type_detection():
    print('\n' + '='*70)
    print('测试: 智能体类型检测')
    print('='*70)

    executor = AgentCreatorExecutor()

    types = [
        ('代码审查', '请创建一个代码审查智能体'),
        ('测试生成', '请创建一个测试生成智能体'),
        ('文档编写', '请创建一个文档编写智能体')
    ]

    for name, request in types:
        result = executor.execute(request)
        assert result['success'] == True
        print(f'✅ {name}: 层次 {result["prompt_level"]}')

    print('✅ 测试通过')

def run_all_tests():
    print('\n' + '='*70)
    print('DNASPEC AGENT CREATOR 测试套件')
    print('='*70)

    tests = [test_basic_execution, test_agent_type_detection]
    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f'\n❌ 测试失败: {test.__name__}')
            print(f'   错误: {e}')
        except Exception as e:
            failed += 1
            print(f'\n❌ 测试错误: {test.__name__}')
            print(f'   异常: {e}')

    print('\n' + '='*70)
    print('测试总结')
    print('='*70)
    print(f'总计: {len(tests)} 个测试')
    print(f'✅ 通过: {passed}')
    print(f'❌ 失败: {failed}')

    if failed == 0:
        print('\n🎉 所有测试通过！DNASPEC AGENT CREATOR 技能就绪。')
        return 0
    else:
        print(f'\n⚠️  有 {failed} 个测试失败，需要修复。')
        return 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
