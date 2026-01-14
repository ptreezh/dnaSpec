#!/usr/bin/env python3
"""
DNASPEC 技能包优化架构 - 简单测试脚本
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """测试基本导入"""
    print("测试基本导入...")
    
    try:
        from plugin import MyOpenCodePlugin
        print("✓ MyOpenCodePlugin imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import MyOpenCodePlugin: {e}")
    
    try:
        from hooks.hook_system import hook_manager, HookContext, HookType
        print("✓ Hook system imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import hook system: {e}")
    
    try:
        from background_task_manager import BackgroundTaskManager
        print("✓ BackgroundTaskManager imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import BackgroundTaskManager: {e}")
    
    try:
        from sisyphus import SisyphusOrchestrator, TaskSpec
        print("✓ SisyphusOrchestrator imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import SisyphusOrchestrator: {e}")
    
    try:
        from agents.agent_manager import AgentManager, BaseAgent
        print("✓ AgentManager imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import AgentManager: {e}")
    
    try:
        from tools.tool_manager import ToolManager
        print("✓ ToolManager imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ToolManager: {e}")
    
    try:
        from context.context_sharing import ContextSharer
        print("✓ ContextSharer imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ContextSharer: {e}")
    
    try:
        from mcp.mcp_server import MCPServer
        print("✓ MCPServer imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import MCPServer: {e}")

def test_hook_system():
    """测试Hook系统"""
    print("\n测试Hook系统...")
    
    try:
        from hooks.hook_system import hook_manager, HookContext, HookType
        
        # 注册一个简单的hook回调
        def sample_callback(context):
            print(f"Hook '{context.hook_name}' triggered with data: {context.data}")
        
        hook_manager.register_hook('test_hook', sample_callback)
        
        # 触发hook
        context = HookContext(
            hook_name='test_hook',
            hook_type=HookType.SKILL,
            data={'message': 'Hello from hook system!'}
        )
        import asyncio
        asyncio.run(hook_manager.trigger_hook('test_hook', context))
        
        print("✓ Hook system test passed")
    except Exception as e:
        print(f"✗ Hook system test failed: {e}")

def test_plugin_creation():
    """测试插件创建"""
    print("\n测试插件创建...")
    
    try:
        from plugin import MyOpenCodePlugin
        
        config = {
            'name': 'TestPlugin',
            'version': '1.0.0'
        }
        
        plugin = MyOpenCodePlugin(config)
        print("✓ Plugin created successfully")
        
        plugin.initialize()
        print("✓ Plugin initialized successfully")
        
        plugin.shutdown()
        print("✓ Plugin shutdown successfully")
        
    except Exception as e:
        print(f"✗ Plugin test failed: {e}")

def test_agents():
    """测试代理系统"""
    print("\n测试代理系统...")
    
    try:
        from agents.agent_manager import AgentManager
        
        agent_manager = AgentManager()
        agent_manager.initialize()
        
        print(f"✓ Agent manager initialized with {len(agent_manager.list_agents())} agents")
        
        # 测试获取代理
        agent = agent_manager.get_agent('code_generation')
        if agent:
            print("✓ Successfully retrieved code_generation agent")
        else:
            print("✗ Failed to retrieve code_generation agent")
        
        agent_manager.shutdown()
        print("✓ Agent manager shutdown successfully")
        
    except Exception as e:
        print(f"✗ Agent system test failed: {e}")

def test_tools():
    """测试工具系统"""
    print("\n测试工具系统...")
    
    try:
        from tools.tool_manager import ToolManager
        
        tool_manager = ToolManager()
        tool_manager.initialize()
        
        print(f"✓ Tool manager initialized with {len(tool_manager.tools)} tools")
        
        # 测试执行一个工具
        result = tool_manager.execute_tool('glob', {'pattern': '*.py', 'recursive': False})
        print(f"✓ Glob tool executed successfully: {result}")
        
        tool_manager.shutdown()
        print("✓ Tool manager shutdown successfully")
        
    except Exception as e:
        print(f"✗ Tool system test failed: {e}")

def main():
    """主函数"""
    print("DNASPEC 技能包优化架构简单测试")
    print("=" * 50)
    
    test_imports()
    test_hook_system()
    test_plugin_creation()
    test_agents()
    test_tools()
    
    print("\n" + "=" * 50)
    print("测试完成！")

if __name__ == "__main__":
    main()