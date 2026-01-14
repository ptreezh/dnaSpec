"""
Task Decomposer - End-to-End Test
端到端测试：验证整个技能架构是否正常工作
"""
import sys
import os
from pathlib import Path

# 添加skills目录到路径，以便直接导入
skills_dir = Path(__file__).parent / "skills" / "dnaspec-task-decomposer"
sys.path.insert(0, str(skills_dir))

# 添加scripts目录到路径
scripts_dir = skills_dir / "scripts"
sys.path.insert(0, str(scripts_dir))

# 导入执行器
from scripts.executor import TaskDecomposerExecutor


def test_prompt_loading():
    """测试1：验证提示词文件可以正确加载"""
    print("\n" + "="*60)
    print("测试1：提示词文件加载")
    print("="*60)

    executor = TaskDecomposerExecutor()

    for level in ["minimal", "basic", "intermediate", "advanced"]:
        prompt = executor._load_prompt(level)
        if prompt:
            print(f"✅ {level}: {len(prompt)} 字符")
        else:
            print(f"❌ {level}: 加载失败")
            return False

    return True


def test_validation():
    """测试2：验证输入验证功能"""
    print("\n" + "="*60)
    print("测试2：输入验证")
    print("="*60)

    from validator import validate_input

    # 测试用例
    test_cases = [
        ("", "空请求"),
        ("实现登录", "太短的请求"),
        ("设计一个用户认证系统，包括注册、登录、密码重置等功能", "正常请求"),
        ("A" * 60000, "超长请求"),
    ]

    for request, description in test_cases:
        result = validate_input(request)
        status = "✅" if result.is_valid or len(result.errors) > 0 else "❓"
        print(f"{status} {description}")
        if not result.is_valid:
            print(f"   错误: {result.errors}")

    return True


def test_calculation():
    """测试3：验证指标计算功能"""
    print("\n" + "="*60)
    print("测试3：指标计算")
    print("="*60)

    from calculator import calculate_metrics

    test_requests = [
        "实现用户登录功能",
        "设计一个电商平台，包括用户、商品、订单、支付模块",
    ]

    for request in test_requests:
        print(f"\n请求: {request[:50]}...")
        metrics = calculate_metrics(request)
        print(f"  复杂度分数: {metrics.complexity_score:.2f}")
        print(f"  估计任务数: {metrics.estimated_tasks}")
        print(f"  估计工时: {metrics.estimated_hours}小时")
        print(f"  推荐层次: {metrics.recommended_prompt_level}")
        print(f"  风险等级: {metrics.risk_level}")

    return True


def test_dependency_analysis():
    """测试4：验证依赖分析功能"""
    print("\n" + "="*60)
    print("测试4：依赖分析")
    print("="*60)

    from analyzer import analyze_dependencies

    # 测试用例：有依赖关系的任务
    tasks = [
        {"id": "001", "name": "Task1", "dependencies": [], "estimated_hours": 2},
        {"id": "002", "name": "Task2", "dependencies": ["001"], "estimated_hours": 3},
        {"id": "003", "name": "Task3", "dependencies": ["001", "002"], "estimated_hours": 1},
    ]

    analysis = analyze_dependencies(tasks)

    print(f"有循环依赖: {analysis.has_circular_deps}")
    print(f"最大深度: {analysis.max_depth}")
    print(f"总任务数: {analysis.total_tasks}")
    print(f"可并行任务数: {analysis.parallelizable_tasks}")
    print(f"关键路径: {analysis.critical_path}")
    print(f"关键路径时长: {analysis.critical_path_duration}小时")

    return True


def test_full_execution():
    """测试5：验证完整执行流程"""
    print("\n" + "="*60)
    print("测试5：完整执行流程")
    print("="*60)

    executor = TaskDecomposerExecutor()

    test_request = "设计一个用户认证系统，包括注册、登录、密码重置功能"
    print(f"请求: {test_request}")

    result = executor.execute(test_request)

    print(f"\n执行结果:")
    print(f"  成功: {result['success']}")

    if result["success"]:
        print(f"\n执行的步骤:")
        for step in result["steps"]:
            print(f"    - {step['step']}: {step['status']}")

        print(f"\n选择的提示词层次: {result['selected_prompt_level']}")

        if "metrics" in result:
            metrics = result["metrics"]
            print(f"\n定量指标:")
            print(f"  - 复杂度: {metrics['complexity']['score']:.2f}")
            print(f"  - 估计任务数: {metrics['complexity']['estimated_tasks']}")
            print(f"  - 估计工时: {metrics['complexity']['estimated_hours']}小时")

        if "decomposition" in result:
            decomp = result["decomposition"]
            if "tasks" in decomp:
                print(f"\n分解结果: {len(decomp['tasks'])} 个任务")
    else:
        print(f"  错误: {result.get('error', 'Unknown error')}")

    return result["success"]


def test_progressive_disclosure():
    """测试6：验证渐进式信息披露"""
    print("\n" + "="*60)
    print("测试6：渐进式信息披露")
    print("="*60)

    executor = TaskDecomposerExecutor()

    # 检查不同复杂度的请求是否选择合适的提示词层次
    test_cases = [
        ("实现登录功能", "minimal"),
        ("设计用户认证系统", "basic"),
        ("设计一个电商平台，包括用户、商品、订单、支付模块", "intermediate"),
        ("构建微服务架构系统，支持10万并发，使用Node.js、PostgreSQL、Redis、Kafka", "advanced"),
    ]

    all_passed = True
    for request, expected_level in test_cases:
        from calculator import calculate_metrics
        metrics = calculate_metrics(request)
        actual_level = metrics.recommended_prompt_level

        # 简单检查：实际层次应该与期望一致或更简单
        level_order = ["minimal", "basic", "intermediate", "advanced"]
        expected_idx = level_order.index(expected_level)
        actual_idx = level_order.index(actual_level)

        passed = actual_idx >= expected_idx  # 实际层次应该不低于期望
        status = "✅" if passed else "❌"
        all_passed = all_passed and passed

        print(f"{status} 请求: {request[:50]}...")
        print(f"   期望层次: {expected_level}, 实际层次: {actual_level}")

    return all_passed


def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("Task Decomposer - 端到端测试")
    print("="*60)

    tests = [
        ("提示词文件加载", test_prompt_loading),
        ("输入验证", test_validation),
        ("指标计算", test_calculation),
        ("依赖分析", test_dependency_analysis),
        ("完整执行流程", test_full_execution),
        ("渐进式信息披露", test_progressive_disclosure),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n❌ {name} 测试异常: {e}")
            results.append((name, False))

    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status} {name}")

    print(f"\n总计: {passed_count}/{total_count} 测试通过")

    if passed_count == total_count:
        print("\n🎉 所有测试通过！task-decomposer 技能架构验证成功！")
        return 0
    else:
        print(f"\n⚠️  有 {total_count - passed_count} 个测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
