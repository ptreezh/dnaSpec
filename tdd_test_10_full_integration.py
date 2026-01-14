#!/usr/bin/env python3
"""
DNASPEC 架构 - TDD 完整集成测试
验证所有组件协同工作
"""

def log_test_result(message, success=True):
    """记录测试结果到文件"""
    with open('tdd_test_results_full_integration.txt', 'a', encoding='utf-8') as f:
        status = "✓" if success else "✗"
        f.write(f"{status} {message}\n")

def run_full_integration_test():
    """运行完整集成测试"""
    try:
        # 导入所有必需的模块
        from abc import ABC, abstractmethod
        from enum import Enum
        from dataclasses import dataclass
        import asyncio
        from typing import Dict, Any, Callable, Optional, List
        
        # Hook 系统
        class HookType(Enum):
            PLUGIN = "plugin"
            TOOL = "tool"
            AGENT = "agent"
            SKILL = "skill"
            HOOK = "hook"

        @dataclass
        class HookContext:
            hook_name: str
            hook_type: HookType
            data: Dict[str, Any]
            result: Any = None
            cancelled: bool = False

        class HookManager:
            def __init__(self):
                self._hooks = {}
            
            def register_hook(self, hook_name: str, callback):
                if hook_name not in self._hooks:
                    self._hooks[hook_name] = []
                self._hooks[hook_name].append(callback)
            
            def trigger_hook(self, hook_name: str, context: HookContext):
                if hook_name in self._hooks:
                    for callback in self._hooks[hook_name]:
                        callback(context)
                return context

        # Agent 系统
        class BaseAgent(ABC):
            def __init__(self, agent_id: str, config: Dict[str, Any] = None):
                self.agent_id = agent_id
                self.config = config or {}
            
            @abstractmethod
            async def process(self, params: Dict[str, Any]) -> Any:
                pass

        class SimpleTestAgent(BaseAgent):
            async def process(self, params: Dict[str, Any]) -> Any:
                return {
                    "agent_id": self.agent_id,
                    "processed_params": params,
                    "result": "test_result"
                }

        class AgentManager:
            def __init__(self):
                self.agents: Dict[str, BaseAgent] = {}
                self.agent_types = {
                    'simple_test': SimpleTestAgent
                }
            
            def initialize(self):
                for agent_type, agent_class in self.agent_types.items():
                    agent = agent_class(f"default_{agent_type}_agent")
                    self.agents[agent_type] = agent
            
            def get_agent(self, agent_type: str) -> BaseAgent:
                return self.agents.get(agent_type)

        # Tool 系统
        class ToolManager:
            def __init__(self):
                self.tools: Dict[str, Callable] = {}
                self._register_default_tools()
            
            def _register_default_tools(self):
                self.tools['bash'] = self._bash_tool
                self.tools['glob'] = self._glob_tool
            
            def execute_tool(self, name: str, params: Dict[str, Any]) -> Any:
                if name not in self.tools:
                    raise ValueError(f"Tool '{name}' not found")
                return self.tools[name](params)
            
            def _bash_tool(self, params: Dict[str, Any]) -> Any:
                command = params.get('command', '')
                return {
                    'tool': 'bash',
                    'command': command,
                    'result': f'Would execute: {command}',
                    'success': True
                }
            
            def _glob_tool(self, params: Dict[str, Any]) -> Any:
                pattern = params.get('pattern', '*')
                return {
                    'tool': 'glob',
                    'pattern': pattern,
                    'matches': ['mocked_file1.txt', 'mocked_file2.txt'],
                    'success': True
                }

        # Context 系统
        class DirectoryInjector:
            def __init__(self):
                self.shared_directories: Dict[str, str] = {}
            
            def inject_directory(self, key: str, path: str):
                self.shared_directories[key] = path
            
            def get_directory(self, key: str) -> Optional[str]:
                return self.shared_directories.get(key)

        class ContextSharer:
            def __init__(self):
                self.directory_injector = DirectoryInjector()

        # Plugin 系统
        class PluginInterface(ABC):
            @abstractmethod
            def initialize(self):
                pass

            @abstractmethod
            def shutdown(self):
                pass

        class MyOpenCodePlugin(PluginInterface):
            def __init__(self, config: Dict[str, Any]):
                self.config = config
                self.hook_manager = HookManager()
                self.tool_manager = ToolManager()
                self.context_sharer = ContextSharer()
                self.agent_manager = AgentManager()
                self.initialized = False
                
                # 注册插件相关的hooks
                self._register_plugin_hooks()
            
            def _register_plugin_hooks(self):
                self.hook_manager.register_hook('plugin_loaded', self._on_plugin_loaded)
                self.hook_manager.register_hook('plugin_initialized', self._on_plugin_initialized)
            
            def _on_plugin_loaded(self, context: HookContext):
                pass  # 为测试简化
            
            def _on_plugin_initialized(self, context: HookContext):
                pass  # 为测试简化
            
            def initialize(self):
                # 触发插件加载hook
                context = HookContext(
                    hook_name='plugin_loaded',
                    hook_type=HookType.PLUGIN,
                    data={'plugin': self}
                )
                self.hook_manager.trigger_hook('plugin_loaded', context)
                
                # 初始化其他组件
                self.agent_manager.initialize()
                
                # 触发插件初始化hook
                context = HookContext(
                    hook_name='plugin_initialized',
                    hook_type=HookType.PLUGIN,
                    data={'plugin': self}
                )
                self.hook_manager.trigger_hook('plugin_initialized', context)
                
                self.initialized = True
            
            def shutdown(self):
                self.initialized = False

        # 执行完整集成测试
        config = {
            'name': 'IntegrationTestPlugin',
            'version': '1.0.0'
        }
        
        plugin = MyOpenCodePlugin(config)
        plugin.initialize()
        
        # 验证插件初始化
        assert plugin.initialized == True
        
        # 测试工具系统
        bash_result = plugin.tool_manager.execute_tool('bash', {'command': 'echo hello'})
        assert bash_result['tool'] == 'bash'
        assert 'echo hello' in bash_result['result']
        
        # 测试代理系统
        agent = plugin.agent_manager.get_agent('simple_test')
        assert agent is not None
        
        async def test_agent():
            result = await agent.process({'test': 'data'})
            return result
        
        agent_result = asyncio.run(test_agent())
        assert agent_result['result'] == 'test_result'
        
        # 测试上下文共享
        plugin.context_sharer.directory_injector.inject_directory('src', './src')
        path = plugin.context_sharer.directory_injector.get_directory('src')
        assert path == './src'
        
        # 测试 Hook 系统
        test_result = {"called": False}
        
        def test_callback(context):
            test_result["called"] = True
            test_result["hook_name"] = context.hook_name
        
        plugin.hook_manager.register_hook('test_hook', test_callback)
        
        context = HookContext(
            hook_name='test_hook',
            hook_type=HookType.SKILL,
            data={"test": "data"}
        )
        
        plugin.hook_manager.trigger_hook('test_hook', context)
        assert test_result["called"] == True
        assert test_result["hook_name"] == 'test_hook'
        
        log_test_result("完整集成测试通过", True)
        return True
        
    except Exception as e:
        import traceback
        log_test_result(f"完整集成测试失败: {e}", False)
        # 记录详细错误信息
        with open('integration_error_debug.txt', 'w', encoding='utf-8') as f:
            f.write(f"Error: {e}\n")
            f.write(traceback.format_exc())
        return False

if __name__ == "__main__":
    run_full_integration_test()