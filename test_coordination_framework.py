#!/usr/bin/env python3
"""
DNASPEC 协调框架综合测试
测试宪法检测、协调执行和优雅降级机制
"""

import sys
import os
import unittest
import json
import time
from datetime import datetime
from typing import Dict, Any, List

# 添加src路径到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dna_spec_kit_integration.core.coordination.constitution_detector import ConstitutionDetector, ConstitutionInfo
from dna_spec_kit_integration.core.coordination.coordination_manager import CoordinationManager, CoordinationWorkflow, CoordinationMode, CoordinationTask, TaskStatus
from dna_spec_kit_integration.core.coordination.graceful_degrader import GracefulDegrader, DegradationMode
from dna_spec_kit_integration.core.coordination.unified_executor import UnifiedExecutor, SkillRequest, ExecutionMode


class TestConstitutionDetection(unittest.TestCase):
    """测试宪法检测功能"""
    
    def setUp(self):
        """测试初始化"""
        self.detector = ConstitutionDetector()
    
    def test_constitution_detection(self):
        """测试宪法检测"""
        print("\n🔍 测试宪法检测...")
        
        # 执行宪法检测
        constitution_info = self.detector.detect_constitution()
        
        # 验证结果
        self.assertIsInstance(constitution_info, ConstitutionInfo)
        self.assertIn('has_project_constitution', constitution_info.__dict__)
        self.assertIn('confidence_score', constitution_info.__dict__)
        self.assertIn('coordination_recommended', constitution_info.__dict__)
        
        print(f"✅ 宪法检测完成")
        print(f"   - 项目宪法存在: {constitution_info.has_project_constitution}")
        print(f"   - 置信度分数: {constitution_info.confidence_score:.2f}")
        print(f"   - 建议协调: {constitution_info.coordination_recommended}")
        
        return constitution_info
    
    def test_constitution_file_detection(self):
        """测试宪法文件检测"""
        print("\n📋 测试宪法文件检测...")
        
        # 检查具体文件
        files_to_check = [
            'PROJECT_CONSTITUTION.md',
            '.dnaspec',
            'src/dna_spec_kit_integration/skills'
        ]
        
        for file_path in files_to_check:
            exists = os.path.exists(file_path)
            print(f"   - {file_path}: {'✅ 存在' if exists else '❌ 不存在'}")
        
        print("✅ 宪法文件检测完成")


class TestCoordinationManager(unittest.TestCase):
    """测试协调管理器功能"""
    
    def setUp(self):
        """测试初始化"""
        self.coordination_manager = CoordinationManager()
    
    def test_workflow_creation(self):
        """测试工作流创建"""
        print("\n🔧 测试工作流创建...")
        
        # 创建测试技能请求
        skill_requests = [
            {'skill_name': 'architect', 'params': 'system_type=web_app'},
            {'skill_name': 'task-decomposer', 'params': 'task=build_frontend'}
        ]
        
        # 创建工作流
        workflow = self.coordination_manager.create_workflow_from_requests(skill_requests, 'test_workflow')
        
        # 验证工作流
        self.assertIsNotNone(workflow)
        self.assertEqual(workflow.workflow_id, 'test_workflow')
        self.assertEqual(len(workflow.skills), 2)
        
        print(f"✅ 工作流创建成功")
        print(f"   - 工作流ID: {workflow.workflow_id}")
        print(f"   - 技能数量: {len(workflow.skills)}")
        print(f"   - 协调模式: {workflow.mode.value}")
        
        return workflow
    
    def test_sequential_execution(self):
        """测试顺序执行模式"""
        print("\n⚡ 测试顺序执行模式...")
        
        # 创建顺序工作流
        workflow = CoordinationWorkflow(
            workflow_id='sequential_test',
            name='Sequential Test Workflow',
            tasks=[
                CoordinationTask(
                    task_id='task1',
                    skill_name='context-analyzer',
                    input_data={'content': 'test'},
                    dependencies=[],
                    status=TaskStatus.PENDING
                ),
                CoordinationTask(
                    task_id='task2',
                    skill_name='context-optimizer',
                    input_data={'target': 'clarity'},
                    dependencies=[],
                    status=TaskStatus.PENDING
                )
            ],
            mode=CoordinationMode.SEQUENTIAL,
            context={},
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        )
        
        # 执行工作流
        result = self.coordination_manager.execute_workflow('sequential_test')
        
        # 验证结果
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn('success', result)
        
        print(f"✅ 顺序执行完成")
        print(f"   - 执行成功: {result.get('success', False)}")
        print(f"   - 执行时间: {result.get('execution_time', 0):.2f}秒")
        
        return result


class TestGracefulDegrader(unittest.TestCase):
    """测试优雅降级器功能"""
    
    def setUp(self):
        """测试初始化"""
        self.degrader = GracefulDegrader()
    
    def test_degradation_detection(self):
        """测试降级检测"""
        print("\n🛡️ 测试降级检测...")
        
        # 模拟协调失败结果
        coordination_result = {
            'success': False,
            'error': 'Constitution not found'
        }
        
        skill_requests = [
            {'skill_name': 'architect', 'params': 'test'},
            {'skill_name': 'task-decomposer', 'params': 'test'}
        ]
        
        # 检测降级需求
        degradation_mode = self.degrader.detect_degradation_need(coordination_result, skill_requests)
        
        # 验证检测结果
        self.assertIsNotNone(degradation_mode)
        self.assertEqual(degradation_mode, DegradationMode.CONSTITUTION_MISSING)
        
        print(f"✅ 降级检测成功")
        print(f"   - 检测到的降级模式: {degradation_mode.value}")
        
        return degradation_mode
    
    def test_constitution_missing_degradation(self):
        """测试宪法缺失降级"""
        print("\n📉 测试宪法缺失降级...")
        
        skill_requests = [
            {'skill_name': 'architect', 'input_data': {'test': True}},
            {'skill_name': 'task-decomposer', 'input_data': {'test': True}}
        ]
        
        # 执行降级
        result = self.degrader.execute_graceful_degradation(
            DegradationMode.CONSTITUTION_MISSING,
            skill_requests
        )
        
        # 验证降级结果
        self.assertIsNotNone(result)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.fallback_result)
        self.assertGreater(len(result.degraded_skills), 0)
        
        print(f"✅ 宪法缺失降级成功")
        print(f"   - 降级模式: {result.mode}")
        print(f"   - 降级技能数: {len(result.degraded_skills)}")
        print(f"   - 性能影响: {result.performance_impact}")
        
        return result
    
    def test_resource_exhausted_degradation(self):
        """测试资源耗尽降级"""
        print("\n💾 测试资源耗尽降级...")
        
        skill_requests = [
            {'skill_name': 'context-analyzer', 'input_data': {'content': 'test'}},
            {'skill_name': 'context-optimizer', 'input_data': {'target': 'optimization'}}
        ]
        
        # 执行降级
        result = self.degrader.execute_graceful_degradation(
            DegradationMode.RESOURCE_EXHAUSTED,
            skill_requests
        )
        
        # 验证降级结果
        self.assertIsNotNone(result)
        self.assertTrue(result.success)
        self.assertEqual(result.mode, "resource_limited_sequential")
        
        print(f"✅ 资源耗尽降级成功")
        print(f"   - 降级模式: {result.mode}")
        print(f"   - 性能影响: {result.performance_impact}")
        
        return result


class TestUnifiedExecutor(unittest.TestCase):
    """测试统一执行器功能"""
    
    def setUp(self):
        """测试初始化"""
        self.executor = UnifiedExecutor()
    
    def test_single_skill_execution(self):
        """测试单技能执行"""
        print("\n🎯 测试单技能执行...")
        
        # 创建技能请求
        skill_request = SkillRequest(
            skill_name='context-analyzer',
            params='content=This is a test content for analysis.',
            context={'analysis_type': 'basic'}
        )
        
        # 执行技能
        result = self.executor.execute_skill(skill_request)
        
        # 验证结果
        self.assertIsNotNone(result)
        self.assertIn('success', result)
        self.assertIn('mode', result)
        self.assertIn('context', result)
        
        print(f"✅ 单技能执行完成")
        print(f"   - 执行模式: {result['mode']}")
        print(f"   - 执行成功: {result['success']}")
        print(f"   - 宪法检测: {result['context']['constitution_detected']}")
        
        return result
    
    def test_workflow_execution(self):
        """测试工作流执行"""
        print("\n🔄 测试工作流执行...")
        
        # 创建技能请求列表
        skill_requests = [
            SkillRequest('context-analyzer', 'content=test1'),
            SkillRequest('context-optimizer', 'target=clarity'),
            SkillRequest('cognitive-templater', 'template_type=analysis')
        ]
        
        # 执行工作流
        result = self.executor.execute_workflow(skill_requests)
        
        # 验证结果
        self.assertIsNotNone(result)
        self.assertIn('mode', result)
        self.assertIn('workflow_results', result)
        
        print(f"✅ 工作流执行完成")
        print(f"   - 执行模式: {result['mode']}")
        print(f"   - 技能数量: {len(result['workflow_results'])}")
        
        return result
    
    def test_execution_statistics(self):
        """测试执行统计"""
        print("\n📊 测试执行统计...")
        
        # 执行几个技能来生成统计数据
        for i in range(3):
            skill_request = SkillRequest(f'skill_{i}', f'params_{i}')
            self.executor.execute_skill(skill_request)
        
        # 获取统计信息
        stats = self.executor.get_execution_stats()
        
        # 验证统计信息
        self.assertIsInstance(stats, dict)
        self.assertIn('total_requests', stats)
        self.assertIn('coordinated_executions', stats)
        self.assertIn('independent_executions', stats)
        self.assertIn('coordination_success_rate', stats)
        
        print(f"✅ 执行统计完成")
        print(f"   - 总请求数: {stats['total_requests']}")
        print(f"   - 协调执行数: {stats['coordinated_executions']}")
        print(f"   - 独立执行数: {stats['independent_executions']}")
        print(f"   - 协调成功率: {stats.get('coordination_success_rate', 0):.1f}%")
        
        return stats


class TestIntegrationScenarios(unittest.TestCase):
    """测试集成场景"""
    
    def setUp(self):
        """测试初始化"""
        self.detector = ConstitutionDetector()
        self.executor = UnifiedExecutor()
    
    def test_constitutional_project_scenario(self):
        """测试有宪法的项目场景"""
        print("\n🏛️ 测试有宪法的项目场景...")
        
        # 检测宪法状态
        constitution_info = self.detector.detect_constitution()
        
        # 创建多个相关技能请求
        skill_requests = [
            SkillRequest('architect', 'system_type=web_application'),
            SkillRequest('task-decomposer', 'task=develop_user_interface'),
            SkillRequest('constraint-generator', 'domain=performance')
        ]
        
        # 执行工作流
        result = self.executor.execute_workflow(skill_requests)
        
        print(f"✅ 有宪法项目场景测试完成")
        print(f"   - 宪法检测: {constitution_info.has_project_constitution}")
        print(f"   - 执行模式: {result['mode']}")
        print(f"   - 置信度: {constitution_info.confidence_score:.2f}")
        
        return result
    
    def test_no_constitution_scenario(self):
        """测试无宪法的项目场景"""
        print("\n🔧 测试无宪法的项目场景...")
        
        # 创建单独的技能请求（不形成工作流）
        skill_request = SkillRequest('context-analyzer', 'content=simple test')
        
        # 执行技能
        result = self.executor.execute_skill(skill_request)
        
        print(f"✅ 无宪法项目场景测试完成")
        print(f"   - 执行模式: {result['mode']}")
        print(f"   - 降级处理: {'degraded' in result['mode']}")
        
        return result
    
    def test_mixed_execution_scenario(self):
        """测试混合执行场景"""
        print("\n🔀 测试混合执行场景...")
        
        # 创建混合类型的请求
        requests = [
            SkillRequest('context-analyzer', 'content=test1'),  # 独立执行
            SkillRequest('architect', 'system=web_app'),       # 可能协调执行
            SkillRequest('constraint-generator', 'type=security')  # 独立执行
        ]
        
        results = []
        for request in requests:
            result = self.executor.execute_skill(request)
            results.append(result)
        
        print(f"✅ 混合执行场景测试完成")
        for i, result in enumerate(results):
            print(f"   - 请求 {i+1}: {result['mode']} ({'成功' if result['success'] else '失败'})")
        
        return results


def run_comprehensive_test():
    """运行综合测试"""
    print("🚀 开始DNASPEC协调框架综合测试")
    print("=" * 60)
    
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试类
    test_classes = [
        TestConstitutionDetection,
        TestCoordinationManager,
        TestGracefulDegrader,
        TestUnifiedExecutor,
        TestIntegrationScenarios
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 总结测试结果
    print("\n" + "=" * 60)
    print("📋 测试总结")
    print("=" * 60)
    print(f"总测试数: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ 失败的测试:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback.split(chr(10))[-2]}")
    
    if result.errors:
        print("\n💥 错误的测试:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback.split(chr(10))[-2]}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"\n✅ 测试成功率: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("🎉 协调框架测试通过！系统可以投入使用。")
    else:
        print("⚠️ 协调框架存在一些问题，需要进一步修复。")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
