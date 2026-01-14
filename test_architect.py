import sys
from pathlib import Path

skills_dir = Path(__file__).parent / 'skills' / 'dnaspec-architect'
sys.path.insert(0, str(skills_dir))

from scripts.executor import ArchitectExecutor

def test_basic_execution():
    print('\n' + '='*70)
    print('测试: 基本执行功能')
    print('='*70)

    executor = ArchitectExecutor()
    result = executor.execute('请设计一个多层调用架构')

    assert result['success'] == True
    print(f'✅ 提示词层次: {result["prompt_level"]}')
    print('✅ 测试通过')

def test_coordination_detection():
    print('\n' + '='*70)
    print('测试: 协调类型检测')
    print('='*70)

    executor = ArchitectExecutor()

    types = [
        ('多层调用', '请设计多层调用架构，确保协议对齐'),
        ('技能协调', '请协调多个技能完成复杂任务'),
        ('架构审查', '请审查现有架构，防止失控')
    ]

    for name, request in types:
        result = executor.execute(request)
        assert result['success'] == True
        print(f'✅ {name}: 层次 {result["prompt_level"]}')

    print('✅ 测试通过')

def run_all_tests():
    print('\n' + '='*70)
    print('DNASPEC ARCHITECT 测试套件')
    print('='*70)

    tests = [test_basic_execution, test_coordination_detection]
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
        print('\n🎉 所有测试通过！DNASPEC ARCHITECT 技能就绪。')
        return 0
    else:
        print(f'\n⚠️  有 {failed} 个测试失败，需要修复。')
        return 1

if __name__ == '__main__':
    sys.exit(run_all_tests())
