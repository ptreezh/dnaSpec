"""
spec.kit适配器单元测试
"""
import sys
import os
import pytest
from unittest.mock import Mock, patch

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.dnaspec_spec_kit_integration.adapters.spec_kit_adapter import SpecKitAdapter


# 定义测试用的SpecKitAdapter实现
class TestSpecKitAdapterImpl(SpecKitAdapter):
    """测试用的SpecKitAdapter实现"""
    def execute_skill(self, skill_name: str, params: dict) -> dict:
        """实现抽象方法"""
        return {"result": f"执行技能 {skill_name}", "params": params}


class TestSpecKitAdapter:
    """SpecKitAdapter单元测试"""
    
    def test_spec_kit_adapter_initialization(self):
        """测试spec.kit适配器初始化"""
        adapter = TestSpecKitAdapterImpl()
        assert adapter is not None
        assert hasattr(adapter, 'supported_agents')
        assert hasattr(adapter, 'command_prefix')
        assert adapter.command_prefix == "/speckit.dnaspec."
        assert adapter.is_initialized == False
    
    def test_spec_kit_adapter_supported_agents(self):
        """测试支持的AI代理列表"""
        adapter = TestSpecKitAdapterImpl()
        supported = adapter.get_supported_agents()
        assert isinstance(supported, list)
        assert len(supported) > 0
        assert 'claude' in supported
        assert 'gemini' in supported
        assert 'qwen' in supported
    
    def test_spec_kit_adapter_is_agent_supported(self):
        """测试代理支持检查功能"""
        adapter = TestSpecKitAdapterImpl()
        
        # 测试支持的代理
        assert adapter.is_agent_supported('claude') is True
        assert adapter.is_agent_supported('Claude') is True  # 大小写不敏感
        assert adapter.is_agent_supported('GEMINI') is True
        
        # 测试不支持的代理
        assert adapter.is_agent_supported('unsupported') is False
        assert adapter.is_agent_supported('') is False
    
    def test_spec_kit_adapter_check_dependencies(self):
        """测试依赖检查功能"""
        adapter = TestSpecKitAdapterImpl()
        
        # 模拟系统命令检查
        with patch('shutil.which') as mock_which:
            mock_which.return_value = '/usr/bin/git'
            result = adapter.check_dependencies()
            assert isinstance(result, dict)
            assert 'git' in result
            assert result['git'] is True
    
    def test_spec_kit_adapter_check_dependency(self):
        """测试单个依赖检查功能"""
        adapter = TestSpecKitAdapterImpl()
        
        # 模拟依赖存在
        with patch('shutil.which') as mock_which:
            mock_which.return_value = '/usr/bin/python'
            assert adapter._check_dependency('python') is True
            
            mock_which.return_value = None
            assert adapter._check_dependency('nonexistent') is False
    
    def test_spec_kit_adapter_parse_command_valid(self):
        """测试有效命令解析"""
        adapter = TestSpecKitAdapterImpl()
        
        # 测试带参数的命令
        result = adapter.parse_command("/speckit.dnaspec.architect 设计一个电商系统架构")
        assert result is not None
        assert result['skill_name'] == "dnaspec-architect"
        assert result['params'] == "设计一个电商系统架构"
        assert result['original_command'] == "/speckit.dnaspec.architect 设计一个电商系统架构"
        
        # 测试不带参数的命令
        result = adapter.parse_command("/speckit.dnaspec.agent-creator")
        assert result is not None
        assert result['skill_name'] == "dnaspec-agent-creator"
        assert result['params'] == ""
        assert result['original_command'] == "/speckit.dnaspec.agent-creator"
    
    def test_spec_kit_adapter_parse_command_invalid(self):
        """测试无效命令解析"""
        adapter = TestSpecKitAdapterImpl()
        
        # 测试不以指定前缀开头的命令
        result = adapter.parse_command("/invalid.command")
        assert result is None
        
        # 测试空命令
        result = adapter.parse_command("")
        assert result is None
        
        # 测试None命令
        result = adapter.parse_command(None)
        assert result is None
    
    def test_spec_kit_adapter_map_command_to_skill(self):
        """测试命令到技能的映射"""
        adapter = TestSpecKitAdapterImpl()
        
        # 测试有效的命令映射
        skill_name = adapter.map_command_to_skill("/speckit.dnaspec.architect 设计系统")
        assert skill_name == "dnaspec-architect"
        
        # 测试无效的命令映射
        skill_name = adapter.map_command_to_skill("/invalid.command")
        assert skill_name is None
    
    def test_spec_kit_adapter_initialize(self):
        """测试适配器初始化"""
        adapter = TestSpecKitAdapterImpl()
        
        # 模拟依赖检查通过
        with patch.object(adapter, 'check_dependencies') as mock_check:
            mock_check.return_value = {'git': True, 'python': True}
            result = adapter.initialize()
            assert result is True
            assert adapter.is_initialized is True
    
    def test_spec_kit_adapter_get_adapter_info(self):
        """测试获取适配器信息"""
        adapter = TestSpecKitAdapterImpl()
        
        # 模拟依赖检查
        with patch.object(adapter, 'check_dependencies') as mock_check:
            mock_check.return_value = {'git': True, 'python': True}
            info = adapter.get_adapter_info()
            
            assert isinstance(info, dict)
            assert 'name' in info
            assert 'supported_agents' in info
            assert 'command_prefix' in info
            assert 'is_initialized' in info
            assert 'dependencies' in info
            assert info['name'] == 'TestSpecKitAdapterImpl'
            assert info['command_prefix'] == "/speckit.dnaspec."
            assert info['dependencies']['git'] is True
            assert info['dependencies']['python'] is True
    
    def test_spec_kit_adapter_execute_skill_abstract(self):
        """测试抽象方法执行"""
        # 测试抽象类不能实例化
        with pytest.raises(TypeError):
            SpecKitAdapter()
        
        # 测试具体实现可以实例化
        adapter = TestSpecKitAdapterImpl()
        result = adapter.execute_skill("test-skill", {"param": "value"})
        assert result["result"] == "执行技能 test-skill"
        assert result["params"]["param"] == "value"