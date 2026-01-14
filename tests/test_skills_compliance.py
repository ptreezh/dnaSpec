"""
DNASPEC Skills TDD Test Suite - 符合AgentSkills.io标准
基于TDD方法实现，遵循KISS、SOLID、YAGNI原则
"""
import pytest
import json
import uuid
import time
from typing import Dict, Any
from unittest.mock import Mock, patch
from datetime import datetime

# 导入要测试的技能模块
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'skills'))

# 导入重构后的技能
from architect.skill import architect_skill, lambda_handler as architect_lambda_handler
from context_analyzer.skill import context_analyzer_skill, lambda_handler as context_analyzer_lambda_handler


class TestSkillBase:
    """技能测试基类 - 提供通用的测试方法和断言"""
    
    def assert_valid_response_format(self, response: Dict[str, Any]) -> None:
        """验证标准响应格式"""
        assert isinstance(response, dict)
        assert 'statusCode' in response
        assert 'body' in response
        
        # 验证body是JSON字符串
        assert isinstance(response['body'], str)
        body_data = json.loads(response['body'])
        
        # 验证body内容结构
        assert 'success' in body_data
        assert 'metadata' in body_data
        assert 'timestamp' in body_data['metadata']
        assert 'skill' in body_data['metadata']
    
    def assert_error_response_format(self, response: Dict[str, Any], expected_status: int = 500) -> None:
        """验证错误响应格式"""
        assert response['statusCode'] == expected_status
        body_data = json.loads(response['body'])
        assert body_data['success'] == False
        assert 'error' in body_data
    
    def create_valid_event(self, tool_name: str, input_data: str = "测试输入", **kwargs) -> Dict[str, Any]:
        """创建有效的测试事件"""
        event = {
            "inputs": [{"input": input_data, **kwargs}],
            "tool_name": tool_name
        }
        return event
    
    def create_invalid_event(self, tool_name: str) -> Dict[str, Any]:
        """创建无效的测试事件"""
        return {
            "inputs": [],
            "tool_name": tool_name
        }


class TestArchitectSkill(TestSkillBase):
    """架构师技能测试类"""
    
    def test_architect_skill_valid_input(self):
        """测试架构师技能处理有效输入"""
        event = self.create_valid_event("architect", "设计用户认证系统")
        
        response = architect_lambda_handler(event)
        
        # 验证响应格式
        self.assert_valid_response_format(response)
        assert response['statusCode'] == 200
        
        # 验证结果内容
        body_data = json.loads(response['body'])
        assert body_data['success'] == True
        assert 'result' in body_data
        
        result = body_data['result']
        assert 'architecture_type' in result
        assert 'design' in result
        assert 'context_quality' in result
        assert isinstance(result['context_quality'], dict)
        
        # 验证质量指标
        quality = result['context_quality']
        assert 'clarity' in quality
        assert 'relevance' in quality
        assert 'completeness' in quality
        assert 'consistency' in quality
        assert 'efficiency' in quality
        
        # 验证质量指标数值范围
        for metric, value in quality.items():
            assert isinstance(value, (int, float))
            assert 0 <= value <= 1
    
    def test_architect_skill_empty_input(self):
        """测试架构师技能处理空输入"""
        event = self.create_valid_event("architect", "")
        
        response = lambda_handler(event)
        
        # 应该返回错误但不应该崩溃
        self.assert_error_response_format(response, 400)
    
    def test_architect_skill_ecommerce_scenario(self):
        """测试架构师技能处理电商场景"""
        event = self.create_valid_event("architect", "设计电商平台，支持用户登录、商品管理、订单处理")
        
        response = lambda_handler(event)
        
        self.assert_valid_response_format(response)
        body_data = json.loads(response['body'])
        result = body_data['result']
        
        # 应该识别为电商类型
        assert result['architecture_type'] == '电商'
        assert 'WebApp' in result['design']
        assert 'API Server' in result['design']
        assert 'Database' in result['design']
    
    def test_architect_skill_unknown_scenario(self):
        """测试架构师技能处理未知场景"""
        event = self.create_valid_event("architect", "设计一个全新的量子计算系统")
        
        response = lambda_handler(event)
        
        self.assert_valid_response_format(response)
        body_data = json.loads(response['body'])
        result = body_data['result']
        
        # 应该处理为自定义类型
        assert result['architecture_type'] == 'custom'
        assert 'design' in result


class TestContextAnalysisSkill(TestSkillBase):
    """上下文分析技能测试类"""
    
    def test_context_analysis_valid_input(self):
        """测试上下文分析技能处理有效输入"""
        event = self.create_valid_event("context-analyzer", "分析这个用户认证系统的需求文档")
        
        response = lambda_handler(event)
        
        self.assert_valid_response_format(response)
        assert response['statusCode'] == 200
        
        body_data = json.loads(response['body'])
        assert body_data['success'] == True
        
        result = body_data['result']
        assert 'context_length' in result
        assert 'quality_metrics' in result
        assert isinstance(result['quality_metrics'], dict)
        
        # 验证质量指标
        quality = result['quality_metrics']
        required_metrics = ['clarity', 'relevance', 'completeness', 'consistency', 'efficiency']
        for metric in required_metrics:
            assert metric in quality
            assert isinstance(quality[metric], (int, float))
            assert 0 <= quality[metric] <= 1
    
    def test_context_analysis_empty_input(self):
        """测试上下文分析技能处理空输入"""
        event = self.create_valid_event("context-analyzer", "")
        
        response = lambda_handler(event)
        
        self.assert_error_response_format(response, 400)
    
    def test_context_analysis_system_keywords(self):
        """测试上下文分析技能识别系统关键词"""
        event = self.create_valid_event("context-analyzer", "system function task requirement")
        
        response = lambda_handler(event)
        
        self.assert_valid_response_format(response)
        body_data = json.loads(response['body'])
        result = body_data['result']
        
        # 应该识别为相关度高
        quality = result['quality_metrics']
        assert quality['relevance'] >= 0.7


class TestCognitiveTemplateSkill(TestSkillBase):
    """认知模板技能测试类"""
    
    def test_cognitive_template_chain_of_thought(self):
        """测试认知模板技能应用思维链"""
        event = self.create_valid_event(
            "cognitive-templater", 
            "如何提高系统性能",
            template_type="chain_of_thought"
        )
        
        response = lambda_handler(event)
        
        self.assert_valid_response_format(response)
        body_data = json.loads(response['body'])
        result = body_data['result']
        
        assert result['template_type'] == 'chain_of_thought'
        assert 'template_description' in result
        assert 'enhanced_output' in result
        assert result['cognitive_framework_applied'] == True
        assert '链式思维' in result['enhanced_output']
    
    def test_cognitive_template_verification(self):
        """测试认知模板技能应用验证模板"""
        event = self.create_valid_event(
            "cognitive-templater",
            "审查这个设计方案",
            template_type="verification"
        )
        
        response = lambda_handler(event)
        
        self.assert_valid_response_format(response)
        body_data = json.loads(response['body'])
        result = body_data['result']
        
        assert result['template_type'] == 'verification'
        assert 'verification' in result['enhanced_output'].lower()
    
    def test_cognitive_template_missing_template_type(self):
        """测试认知模板技能缺少模板类型"""
        event = self.create_valid_event("cognitive-templater", "测试输入")
        
        response = lambda_handler(event)
        
        self.assert_error_response_format(response, 400)


class TestTaskDecomposerSkill(TestSkillBase):
    """任务分解技能测试类"""
    
    @patch('main.uuid')  # Mock uuid模块
    def test_task_decomposer_valid_input(self, mock_uuid):
        """测试任务分解技能处理有效输入"""
        mock_uuid.uuid4.return_value = uuid.UUID('12345678-1234-5678-1234-567812345678')
        
        event = self.create_valid_event("task-decomposer", "开发电商平台")
        
        response = lambda_handler(event)
        
        self.assert_valid_response_format(response)
        body_data = json.loads(response['body'])
        result = body_data['result']
        
        assert 'tasks' in result
        assert isinstance(result['tasks'], list)
        assert len(result['tasks']) > 0
        
        # 验证任务结构
        for task in result['tasks']:
            assert 'id' in task
            assert 'description' in task
            assert 'status' in task
    
    @patch('main.uuid')
    def test_task_decomposer_max_depth(self, mock_uuid):
        """测试任务分解技能最大深度设置"""
        mock_uuid.uuid4.return_value = uuid.UUID('12345678-1234-5678-1234-567812345678')
        
        event = self.create_valid_event("task-decomposer", "开发电商平台", max_depth=2)
        
        response = lambda_handler(event)
        
        self.assert_valid_response_format(response)
        body_data = json.loads(response['body'])
        result = body_data['result']
        
        # 验证深度限制
        for task in result['tasks']:
            if 'subtasks' in task:
                for subtask in task['subtasks']:
                    assert 'subtasks' not in subtask  # 不应该有第三层


class TestAgentCreatorSkill(TestSkillBase):
    """智能体创建技能测试类"""
    
    @patch('main.uuid')
    def test_agent_creator_valid_input(self, mock_uuid):
        """测试智能体创建技能处理有效输入"""
        mock_uuid.uuid4.return_value = uuid.UUID('12345678-1234-5678-1234-567812345678')
        
        event = self.create_valid_event("agent-creator", "创建React前端开发者智能体")
        
        response = lambda_handler(event)
        
        self.assert_valid_response_format(response)
        body_data = json.loads(response['body'])
        result = body_data['result']
        
        assert 'agent_config' in result
        assert 'id' in result['agent_config']
        assert 'role' in result['agent_config']
        assert 'capabilities' in result['agent_config']
        assert 'instructions' in result['agent_config']
        
        assert result['agent_config']['role'] == '创建React前端开发者智能体'
        assert isinstance(result['agent_config']['capabilities'], list)
    
    @patch('main.uuid')
    def test_agent_creator_with_custom_capabilities(self, mock_uuid):
        """测试智能体创建技能使用自定义能力"""
        mock_uuid.uuid4.return_value = uuid.UUID('12345678-1234-5678-1234-567812345678')
        
        event = self.create_valid_event(
            "agent-creator", 
            "创建数据分析师智能体",
            capabilities=["数据分析", "报告生成", "可视化"]
        )
        
        response = lambda_handler(event)
        
        self.assert_valid_response_format(response)
        body_data = json.loads(response['body'])
        result = body_data['result']
        
        capabilities = result['agent_config']['capabilities']
        assert "数据分析" in capabilities
        assert "报告生成" in capabilities
        assert "可视化" in capabilities


class TestConstraintGeneratorSkill(TestSkillBase):
    """约束生成技能测试类"""
    
    @patch('main.uuid')
    def test_constraint_generator_valid_input(self, mock_uuid):
        """测试约束生成技能处理有效输入"""
        mock_uuid.uuid4.return_value = uuid.UUID('12345678-1234-5678-1234-567812345678')
        
        event = self.create_valid_event("constraint-generator", "金融系统需要高安全性")
        
        response = lambda_handler(event)
        
        self.assert_valid_response_format(response)
        body_data = json.loads(response['body'])
        result = body_data['result']
        
        assert 'constraints' in result
        assert isinstance(result['constraints'], list)
        assert len(result['constraints']) > 0
        
        # 验证约束结构
        for constraint in result['constraints']:
            assert 'id' in constraint
            assert 'type' in constraint
            assert 'description' in constraint
            assert 'priority' in constraint
    
    @patch('main.uuid')
    def test_constraint_generator_with_change_request(self, mock_uuid):
        """测试约束生成技能处理变更请求"""
        mock_uuid.uuid4.return_value = uuid.UUID('12345678-1234-5678-1234-567812345678')
        
        event = self.create_valid_event(
            "constraint-generator",
            "金融系统需要高安全性",
            change_request="添加新的支付方式"
        )
        
        response = lambda_handler(event)
        
        self.assert_valid_response_format(response)
        body_data = json.loads(response['body'])
        result = body_data['result']
        
        # 应该包含变更相关的约束
        constraints = result['constraints']
        payment_constraints = [c for c in constraints if '支付' in c['description']]
        assert len(payment_constraints) > 0


class TestContextOptimizationSkill(TestSkillBase):
    """上下文优化技能测试类"""
    
    def test_context_optimization_valid_input(self):
        """测试上下文优化技能处理有效输入"""
        event = self.create_valid_event(
            "context-optimizer",
            "系统需要处理用户数据",
            optimization_goals=["clarity", "completeness"]
        )
        
        response = lambda_handler(event)
        
        self.assert_valid_response_format(response)
        body_data = json.loads(response['body'])
        result = body_data['result']
        
        assert 'optimized_context' in result
        assert 'optimization_applied' in result
        assert 'quality_improvement' in result
        
        # 验证优化结果
        assert len(result['optimized_context']) > 0
        assert isinstance(result['optimization_applied'], dict)
        assert isinstance(result['quality_improvement'], dict)
    
    def test_context_optimization_missing_goals(self):
        """测试上下文优化技能缺少优化目标"""
        event = self.create_valid_event("context-optimizer", "系统需要处理用户数据")
        
        response = lambda_handler(event)
        
        # 应该使用默认目标
        self.assert_valid_response_format(response)


class TestLambdaHandlerIntegration(TestSkillBase):
    """Lambda处理器集成测试类"""
    
    def test_lambda_handler_invalid_tool_name(self):
        """测试Lambda处理器处理无效工具名称"""
        event = self.create_valid_event("nonexistent-tool", "测试输入")
        
        response = lambda_handler(event)
        
        self.assert_error_response_format(response, 404)
    
    def test_lambda_handler_missing_inputs(self):
        """测试Lambda处理器缺少输入"""
        event = {"tool_name": "architect"}
        
        response = lambda_handler(event)
        
        self.assert_error_response_format(response, 400)
    
    def test_lambda_handler_execution_time_tracking(self):
        """测试Lambda处理器执行时间跟踪"""
        event = self.create_valid_event("context-analyzer", "测试输入")
        
        start_time = time.time()
        response = lambda_handler(event)
        end_time = time.time()
        
        self.assert_valid_response_format(response)
        body_data = json.loads(response['body'])
        
        # 验证执行时间被记录
        assert 'execution_time' in body_data['metadata']
        recorded_time = body_data['metadata']['execution_time']
        
        # 验证时间合理性
        assert 0 <= recorded_time <= (end_time - start_time + 0.1)  # 允许小误差
    
    def test_lambda_handler_error_handling(self):
        """测试Lambda处理器错误处理"""
        # 创建会导致错误的输入
        event = self.create_valid_event("architect", "")  # 空输入应该导致错误
        
        response = lambda_handler(event)
        
        # 应该优雅处理错误，不崩溃
        assert 'statusCode' in response
        assert 'body' in response
        
        body_data = json.loads(response['body'])
        assert body_data['success'] == False
        assert 'error' in body_data


class TestSkillPerformance(TestSkillBase):
    """技能性能测试类"""
    
    def test_architect_skill_performance(self):
        """测试架构师技能性能"""
        event = self.create_valid_event("architect", "设计用户认证系统")
        
        start_time = time.time()
        response = lambda_handler(event)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # 应该在2秒内完成
        assert execution_time < 2.0
        self.assert_valid_response_format(response)
    
    def test_context_analysis_skill_performance(self):
        """测试上下文分析技能性能"""
        # 创建较长的输入
        long_input = "这是一个很长的需求描述。" * 100
        event = self.create_valid_event("context-analyzer", long_input)
        
        start_time = time.time()
        response = lambda_handler(event)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # 即使长输入也应该在1秒内完成
        assert execution_time < 1.0
        self.assert_valid_response_format(response)


if __name__ == "__main__":
    # 运行所有测试
    pytest.main([__file__, "-v", "--tb=short"])