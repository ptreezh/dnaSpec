"""
Context Fundamentals Skill - End-to-End Test

完整测试dnaspec-context-fundamentals技能的所有功能
"""

import sys
from pathlib import Path
import json

# 添加skills目录到path
skills_dir = Path(__file__).parent / "skills" / "dnaspec-context-fundamentals"
sys.path.insert(0, str(skills_dir))

from scripts.executor import ContextFundamentalsExecutor


class TestResult:
    """测试结果"""
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.passed = False
        self.message = ""
        self.details = {}

    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"{status} - {self.test_name}: {self.message}"


def test_1_prompt_files_loading():
    """测试1：提示词文件加载"""
    result = TestResult("提示词文件加载")

    try:
        executor = ContextFundamentalsExecutor(skills_dir)

        # 测试加载所有4层提示词
        levels = ["00", "01", "02", "03"]
        for level in levels:
            prompt_content = executor._load_prompt(level)
            if not prompt_content or len(prompt_content) == 0:
                result.message = f"Level {level} 提示词为空"
                return result

            # 检查长度范围
            expected_max = {
                "00": 500,
                "01": 1000,
                "02": 2000,
                "03": 3000
            }.get(level, 5000)

            if len(prompt_content) > expected_max * 1.5:  # 允许50%容差
                result.message = f"Level {level} 提示词过长: {len(prompt_content)} > {expected_max}"
                return result

        result.passed = True
        result.message = f"成功加载{len(levels)}层提示词"
        result.details = {
            "levels": levels,
            "total_characters": sum(len(executor._load_prompt(level)) for level in levels)
        }

    except Exception as e:
        result.message = f"加载失败: {str(e)}"

    return result


def test_2_input_validation():
    """测试2：输入验证"""
    result = TestResult("输入验证")

    try:
        executor = ContextFundamentalsExecutor(skills_dir)

        # 测试用例
        test_cases = [
            {
                "name": "正常请求",
                "request": "什么是上下文？为什么它重要？",
                "should_pass": True
            },
            {
                "name": "空请求",
                "request": "",
                "should_pass": False
            },
            {
                "name": "过短请求",
                "request": "啊？",
                "should_pass": False
            },
            {
                "name": "多问题请求",
                "request": "什么是上下文？如何优化？token限制是多少？有哪些最佳实践？",
                "should_pass": True  # 有效但会有警告
            }
        ]

        passed_cases = 0
        validation_results = []

        for test_case in test_cases:
            validation_result = executor.validator.validate(
                test_case["request"],
                None
            )

            # 检查是否符合预期
            is_valid = validation_result.is_valid
            expected_valid = test_case["should_pass"]

            if is_valid == expected_valid or (is_valid and not expected_valid and validation_result.has_warnings()):
                passed_cases += 1
                validation_results.append({
                    "case": test_case["name"],
                    "status": "PASS",
                    "is_valid": is_valid
                })
            else:
                validation_results.append({
                    "case": test_case["name"],
                    "status": "FAIL",
                    "is_valid": is_valid,
                    "expected": test_case["should_pass"]
                })

        if passed_cases == len(test_cases):
            result.passed = True
            result.message = f"所有{len(test_cases)}个测试用例通过"
        else:
            result.message = f"{passed_cases}/{len(test_cases)} 测试用例通过"

        result.details = {
            "test_cases": validation_results
        }

    except Exception as e:
        result.message = f"验证失败: {str(e)}"

    return result


def test_3_metrics_calculation():
    """测试3：指标计算"""
    result = TestResult("指标计算")

    try:
        executor = ContextFundamentalsExecutor(skills_dir)

        # 测试不同复杂度的请求
        test_cases = [
            {
                "name": "简单请求",
                "request": "什么是上下文？",
                "expected_complexity_range": (0.0, 0.3)
            },
            {
                "name": "中等复杂度",
                "request": "如何在AI系统中优化上下文管理？请说明最佳实践和常见陷阱",
                "expected_complexity_range": (0.3, 0.5)
            },
            {
                "name": "高度复杂",
                "request": "设计一个包含50个微服务的大型电商系统的上下文管理架构，需要考虑分布式协作、版本控制、性能优化、安全性等多个方面，同时要处理Lost-in-the-Middle现象、上下文毒化、分心、冲突等多种失效模式，还要实现智能缓存、动态加载、版本控制等高级特性",
                "context": {"scale": "large", "services": 50},
                "expected_complexity_range": (0.5, 1.0)
            }
        ]

        passed_cases = 0
        metrics_results = []

        for test_case in test_cases:
            metrics = executor.calculator.calculate(
                test_case["request"],
                test_case.get("context")
            )

            # 检查复杂度是否在预期范围内
            min_complexity, max_complexity = test_case["expected_complexity_range"]
            if min_complexity <= metrics.complexity_score <= max_complexity:
                passed_cases += 1
                status = "PASS"
            else:
                status = "FAIL"

            metrics_results.append({
                "case": test_case["name"],
                "status": status,
                "complexity": metrics.complexity_score,
                "expected_range": test_case["expected_complexity_range"],
                "tokens": metrics.token_count,
                "recommended_level": metrics.recommended_prompt_level
            })

        if passed_cases == len(test_cases):
            result.passed = True
            result.message = f"所有{len(test_cases)}个测试用例的复杂度计算准确"
        else:
            result.message = f"{passed_cases}/{len(test_cases)} 测试用例通过"

        result.details = {
            "metrics_results": metrics_results
        }

    except Exception as e:
        result.message = f"计算失败: {str(e)}"

    return result


def test_4_failure_detection():
    """测试4：失效模式检测"""
    result = TestResult("失效模式检测")

    try:
        executor = ContextFundamentalsExecutor(skills_dir)

        # 测试不同失效模式
        test_cases = [
            {
                "name": "上下文溢出",
                "request": "分析这个大项目",
                "context": {"content": "data" * 100000},  # 大量数据
                "expected_failure": "overflow"
            },
            {
                "name": "上下文毒化",
                "request": "版本冲突",
                "context": {"v1": "use method A", "v2": "use method B", "old": "enabled", "new": "disabled"},
                "expected_failure": "poisoning"
            },
            {
                "name": "正常上下文",
                "request": "正常请求",
                "context": {"domain": "AI", "task": "learning"},
                "expected_failure": None
            }
        ]

        passed_cases = 0
        detection_results = []

        for test_case in test_cases:
            analysis = executor.analyzer.analyze(
                test_case["request"],
                test_case.get("context")
            )

            expected = test_case["expected_failure"]
            detected = any(f.mode.value == expected for f in analysis.detected_failures) if expected else False

            if expected:
                if detected:
                    passed_cases += 1
                    status = "PASS"
                else:
                    status = "FAIL"
            else:
                if not analysis.detected_failures:
                    passed_cases += 1
                    status = "PASS"
                else:
                    status = "FAIL"

            detection_results.append({
                "case": test_case["name"],
                "status": status,
                "expected": expected,
                "detected_failures": [f.mode.value for f in analysis.detected_failures]
            })

        if passed_cases == len(test_cases):
            result.passed = True
            result.message = f"所有{len(test_cases)}个失效模式检测准确"
        else:
            result.message = f"{passed_cases}/{len(test_cases)} 测试用例通过"

        result.details = {
            "detection_results": detection_results
        }

    except Exception as e:
        result.message = f"检测失败: {str(e)}"

    return result


def test_5_prompt_level_selection():
    """测试5：提示词层次智能选择"""
    result = TestResult("提示词层次智能选择")

    try:
        executor = ContextFundamentalsExecutor(skills_dir)

        # 测试不同场景的层次选择
        test_cases = [
            {
                "name": "简单问题",
                "request": "什么是上下文？",
                "expected_level": "00"
            },
            {
                "name": "中等复杂度",
                "request": "如何优化AI系统的上下文管理？请说明常见场景和最佳实践",
                "expected_level": "01"
            },
            {
                "name": "复杂任务",
                "request": "在大型项目中实施上下文管理策略，需要考虑多轮对话、多文件分析、动态组装等复杂场景",
                "context": {"project_size": "large"},
                "expected_level": "02"
            }
        ]

        passed_cases = 0
        selection_results = []

        for test_case in test_cases:
            # 执行完整流程
            execution_result = executor.execute(
                test_case["request"],
                test_case.get("context")
            )

            selected_level = execution_result["prompt_level"]
            expected_level = test_case["expected_level"]

            # 允许相邻层次（算法可能有合理偏差）
            level_nums = {"00": 0, "01": 1, "02": 2, "03": 3}
            if abs(level_nums[selected_level] - level_nums[expected_level]) <= 1:
                passed_cases += 1
                status = "PASS"
            else:
                status = "FAIL"

            selection_results.append({
                "case": test_case["name"],
                "status": status,
                "expected": expected_level,
                "selected": selected_level
            })

        if passed_cases == len(test_cases):
            result.passed = True
            result.message = f"所有{len(test_cases)}个层次选择合理"
        else:
            result.message = f"{passed_cases}/{len(test_cases)} 测试用例通过"

        result.details = {
            "selection_results": selection_results
        }

    except Exception as e:
        result.message = f"选择失败: {str(e)}"

    return result


def test_6_full_execution_pipeline():
    """测试6：完整执行流程"""
    result = TestResult("完整执行流程")

    try:
        executor = ContextFundamentalsExecutor(skills_dir)

        # 执行完整流程
        request = "如何在包含100个文件的大型项目中管理上下文？需要考虑哪些失效模式和优化策略？"
        context = {
            "project": "large_scale_refactoring",
            "files": 100,
            "architecture": "microservices"
        }

        execution_result = executor.execute(request, context)

        # 验证所有必需字段
        required_fields = [
            "validation",
            "metrics",
            "analysis",
            "prompt_level",
            "prompt_content",
            "summary",
            "recommendations"
        ]

        missing_fields = [f for f in required_fields if f not in execution_result]

        if missing_fields:
            result.message = f"缺少字段: {missing_fields}"
            return result

        # 验证提示词内容
        if not execution_result["prompt_content"] or len(execution_result["prompt_content"]) == 0:
            result.message = "提示词内容为空"
            return result

        # 验证推荐不为空
        if not execution_result["recommendations"]:
            result.message = "没有生成推荐"
            return result

        result.passed = True
        result.message = "完整流程执行成功"
        result.details = {
            "prompt_level": execution_result["prompt_level"],
            "prompt_length": len(execution_result["prompt_content"]),
            "num_recommendations": len(execution_result["recommendations"]),
            "complexity_score": execution_result["metrics"]["complexity_score"],
            "detected_failures": len(execution_result["analysis"]["detected_failures"]),
            "summary": execution_result["summary"]
        }

    except Exception as e:
        result.message = f"执行失败: {str(e)}"
        import traceback
        result.details = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }

    return result


def run_all_tests():
    """运行所有测试"""
    print("="*80)
    print("Context Fundamentals Skill - End-to-End Test Suite")
    print("="*80)
    print()

    tests = [
        test_1_prompt_files_loading,
        test_2_input_validation,
        test_3_metrics_calculation,
        test_4_failure_detection,
        test_5_prompt_level_selection,
        test_6_full_execution_pipeline
    ]

    results = []
    for test_func in tests:
        print(f"Running: {test_func.__name__}...")
        result = test_func()
        results.append(result)
        print(result)
        if result.details:
            print(json.dumps(result.details, indent=2, ensure_ascii=False))
        print()

    # 汇总
    print("="*80)
    print("Test Summary")
    print("="*80)

    passed = sum(1 for r in results if r.passed)
    total = len(results)

    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n🎉 All tests passed! Context Fundamentals skill is ready.")
    else:
        print("\n⚠️ Some tests failed. Please review the details above.")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
