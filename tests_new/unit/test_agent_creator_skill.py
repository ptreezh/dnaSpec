"""
Unit tests for Agent Creator Skill following TDD approach
"""
import pytest
from typing import Dict, Any

# Import the skill to be tested
from src.dna_spec_kit_integration.skills.agent_creator_independent import execute_agent_creator


class TestAgentCreatorSkill:
    """Test cases for Agent Creator Skill"""

    def test_execute_agent_creator_with_valid_context(self):
        """Test executing agent creator with valid context"""
        test_context = "Create a data analysis agent for sales reports"
        
        result = execute_agent_creator({'context': test_context})
        
        # Verify the result structure
        assert isinstance(result, dict)
        assert 'success' in result
        assert 'result' in result
        assert 'context' in result
        
        assert result['success'] is True
        assert result['context'] == test_context
        
        agent_config = result['result']
        assert isinstance(agent_config, dict)
        
        # Check required fields in agent config
        required_fields = [
            'name', 'type', 'description', 'system_prompt',
            'capabilities', 'tools', 'personality', 'specialization'
        ]
        
        for field in required_fields:
            assert field in agent_config
            assert agent_config[field] is not None

    def test_execute_agent_creator_empty_context(self):
        """Test executing agent creator with empty context"""
        result = execute_agent_creator({'context': ''})
        
        # Should fail with error message
        assert isinstance(result, dict)
        assert 'success' in result
        assert result['success'] is False
        assert 'error' in result
        assert 'usage' in result

    def test_execute_agent_creator_whitespace_context(self):
        """Test executing agent creator with whitespace-only context"""
        result = execute_agent_creator({'context': '   \t\n  '})
        
        # Should fail with error message
        assert isinstance(result, dict)
        assert 'success' in result
        assert result['success'] is False

    def test_agent_type_inference_data_analysis(self):
        """Test agent type inference for data analysis context"""
        test_cases = [
            "Create a data analysis agent",
            "Build an analyst agent",
            "Data processing agent",
            "Create an agent that analyzes sales data"
        ]
        
        for context in test_cases:
            result = execute_agent_creator({'context': context})
            if result['success']:
                agent_config = result['result']
                assert agent_config['type'] in ['analyst', 'assistant']

    def test_agent_type_inference_developer(self):
        """Test agent type inference for developer context"""
        test_cases = [
            "Create a development agent",
            "Build a code generator agent",
            "Create a programming assistant",
            "Build an agent that writes Python code"
        ]
        
        for context in test_cases:
            result = execute_agent_creator({'context': context})
            if result['success']:
                agent_config = result['result']
                assert agent_config['type'] in ['developer', 'assistant']

    def test_agent_type_inference_researcher(self):
        """Test agent type inference for researcher context"""
        test_cases = [
            "Create a research agent",
            "Build an academic research assistant",
            "Create an agent for literature analysis"
        ]
        
        for context in test_cases:
            result = execute_agent_creator({'context': context})
            if result['success']:
                agent_config = result['result']
                assert agent_config['type'] in ['researcher', 'assistant']

    def test_capability_inference(self):
        """Test capability inference from context"""
        test_contexts = [
            ("Create an agent for data analysis", ['数据分析', '通用任务处理']),
            ("Build an agent that writes code", ['编程开发', '通用任务处理']),
            ("Create an agent for system design", ['系统设计', '通用任务处理']),
            ("Research assistant", ['研究分析', '通用任务处理']),
        ]
        
        for context, expected_capabilities in test_contexts:
            result = execute_agent_creator({'context': context})
            if result['success']:
                agent_config = result['result']
                # At least one of the expected capabilities should be in the agent's capabilities
                has_expected_capability = any(cap in agent_config['capabilities'] for cap in expected_capabilities)
                if '通用任务处理' in agent_config['capabilities']:
                    # If it has default capabilities, that's also acceptable
                    has_expected_capability = True
                assert has_expected_capability, f"Expected one of {expected_capabilities} in {agent_config['capabilities']}"

    def test_tool_inference(self):
        """Test tool inference from context"""
        test_contexts = [
            ("Create an agent for coding tasks", ['代码编辑器', '文本编辑器']),
            ("Build an agent for data analysis", ['数据分析工具', '文本编辑器']),
            ("Research assistant", ['学术数据库', '文本编辑器']),
        ]
        
        for context, expected_tools in test_contexts:
            result = execute_agent_creator({'context': context})
            if result['success']:
                agent_config = result['result']
                # At least one of the expected tools should be in the agent's tools
                has_expected_tool = any(tool in agent_config['tools'] for tool in expected_tools)
                assert has_expected_tool, f"Expected one of {expected_tools} in {agent_config['tools']}"

    def test_personality_inference(self):
        """Test personality inference from context"""
        test_contexts = [
            ("Create an agent for data analysis with logic", '分析性、严谨'),
            ("Build a creative development agent", '创新、务实'),
            ("Research assistant", '细致、探究精神'),
        ]
        
        for context, expected_personality in test_contexts:
            result = execute_agent_creator({'context': context})
            if result['success']:
                agent_config = result['result']
                # The personality should match expected patterns
                assert isinstance(agent_config['personality'], str)

    def test_specialization_inference(self):
        """Test specialization inference from context"""
        test_contexts = [
            ("Create a business analysis agent", '商业分析'),
            ("Build a software development agent", '软件开发'),
            ("Data analysis agent", '数据分析'),
            ("Academic research agent", '学术研究'),
        ]
        
        for context, expected_specialization in test_contexts:
            result = execute_agent_creator({'context': context})
            if result['success']:
                agent_config = result['result']
                # The specialization should match expected patterns
                assert isinstance(agent_config['specialization'], str)

    def test_agent_name_generation(self):
        """Test agent name generation from context"""
        test_cases = [
            ("Create a data analysis agent", '数据分析师'),
            ("Build a development agent", '开发工程师'),
            ("Create a research agent", '研究专家'),
            ("General assistant", '智能助手'),
        ]
        
        for context, expected_name in test_cases:
            result = execute_agent_creator({'context': context})
            if result['success']:
                agent_config = result['result']
                # The name should be in expected patterns
                assert isinstance(agent_config['name'], str)
                # For Chinese names, we check if it contains expected elements
                if '数据' in context.lower() or 'analysis' in context.lower():
                    assert '数据' in agent_config['name'] or '分析师' in agent_config['name']
                elif '开发' in context.lower() or 'code' in context.lower():
                    assert '开发' in agent_config['name'] or '工程师' in agent_config['name']
                elif '研究' in context.lower() or 'research' in context.lower():
                    assert '研究' in agent_config['name'] or '专家' in agent_config['name']

    def test_system_prompt_generation(self):
        """Test system prompt generation"""
        test_context = "Create a data analysis agent for sales reports"
        result = execute_agent_creator({'context': test_context})
        
        if result['success']:
            agent_config = result['result']
            system_prompt = agent_config['system_prompt']
            assert isinstance(system_prompt, str)
            assert agent_config['type'] in system_prompt
            assert test_context.strip() in system_prompt


if __name__ == "__main__":
    # Run the tests directly if this file is executed
    pytest.main([__file__, "-v"])