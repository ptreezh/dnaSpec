#!/usr/bin/env python3
"""
DNASPEC 技能包优化架构 - 演示和测试脚本
"""

import asyncio
from src.plugin import MyOpenCodePlugin
from src.sisyphus import TaskSpec
from src.agents.agent_manager import AgentManager
from src.tools.tool_manager import ToolManager
from src.background_task_manager import BackgroundTaskManager
from src.context.context_sharing import ContextSharer
from src.mcp.mcp_server import setup_mcp_integration


async def demo_hook_system():
    """演示Hook系统的功能"""
    print("\n=== 演示Hook系统 ===")
    
    from src.hooks.hook_system import hook_manager, HookContext, HookType
    
    # 注册一个简单的hook回调
    def sample_callback(context):
        print(f"Hook '{context.hook_name}' triggered with data: {context.data}")
    
    hook_manager.register_hook('demo_hook', sample_callback)
    
    # 触发hook
    context = HookContext(
        hook_name='demo_hook',
        hook_type=HookType.SKILL,
        data={'message': 'Hello from hook system!'}
    )
    await hook_manager.trigger_hook('demo_hook', context)


async def demo_plugin_system():
    """演示插件系统"""
    print("\n=== 演示插件系统 ===")
    
    # 创建插件配置
    config = {
        'name': 'MyOpenCodePlugin',
        'version': '1.0.0',
        'features': ['hooks', 'agents', 'tools', 'background_tasks'],
        'mcp_config': {
            'enabled': True,
            'port': 8080
        }
    }
    
    # 创建并初始化插件
    plugin = MyOpenCodePlugin(config)
    plugin.initialize()
    
    print(f"Plugin initialized: {plugin.initialized}")
    
    # 演示配置更新
    new_config = {**config, 'version': '1.0.1'}
    plugin.update_config(new_config)
    
    # 关闭插件
    plugin.shutdown()
    print("Plugin shutdown completed")


async def demo_agents():
    """演示代理系统"""
    print("\n=== 演示代理系统 ===")
    
    agent_manager = AgentManager()
    agent_manager.initialize()
    
    # 获取并使用不同类型的代理
    agents_to_test = [
        ('data_analysis', {'dataset': 'sales_data.csv'}),
        ('code_generation', {'requirement': 'create a sorting algorithm'}),
        ('documentation', {'topic': 'API endpoints'}),
        ('testing', {'component': 'authentication module'}),
        ('planning', {'project': 'new website'}),
        ('optimization', {'target': 'database queries'}),
        ('security', {'asset': 'user database'})
    ]
    
    for agent_type, params in agents_to_test:
        agent = agent_manager.get_agent(agent_type)
        if agent:
            result = await agent.process(params)
            print(f"{agent_type} agent result: {result}")
    
    agent_manager.shutdown()


async def demo_tools():
    """演示工具系统"""
    print("\n=== 演示工具系统 ===")
    
    tool_manager = ToolManager()
    tool_manager.initialize()
    
    # 测试各种工具
    tools_to_test = [
        ('lsp', {'file_path': 'example.py', 'action': 'diagnostics'}),
        ('glob', {'pattern': '*.py', 'recursive': True}),
        ('bash', {'command': 'echo "Hello from bash tool"'}),
    ]
    
    for tool_name, params in tools_to_test:
        try:
            result = tool_manager.execute_tool(tool_name, params)
            print(f"{tool_name} tool result: {result}")
        except Exception as e:
            print(f"{tool_name} tool error: {e}")
    
    tool_manager.shutdown()


async def demo_background_tasks():
    """演示后台任务系统"""
    print("\n=== 演示后台任务系统 ===")
    
    task_manager = BackgroundTaskManager()
    task_manager.initialize()
    
    # 定义一个简单的后台任务
    def sample_task(name, duration):
        import time
        print(f"Starting task: {name}")
        time.sleep(duration)  # 模拟耗时操作
        print(f"Completed task: {name}")
        return f"Result of {name}"
    
    # 提交几个后台任务
    tasks = [
        ("Task-1", 1),
        ("Task-2", 2),
        ("Task-3", 1),
    ]
    
    submitted_tasks = []
    for name, duration in tasks:
        task = await task_manager.submit_task(name, sample_task, name, duration)
        if task:
            submitted_tasks.append(task)
    
    # 等待所有任务完成
    if submitted_tasks:
        await asyncio.gather(*submitted_tasks)
    
    print("All background tasks completed")
    task_manager.shutdown()


async def demo_sisyphus_orchestrator():
    """演示Sisyphus主编排器"""
    print("\n=== 演示Sisyphus主编排器 ===")
    
    from src.sisyphus import SisyphusOrchestrator, TaskSpec
    
    orchestrator = SisyphusOrchestrator()
    orchestrator.initialize()
    
    # 创建代理管理器并设置给编排器
    agent_manager = AgentManager()
    agent_manager.initialize()
    orchestrator.set_agent_manager(agent_manager)
    
    # 添加一些任务到编排器
    tasks = [
        TaskSpec(name="analyze_data", agent_type="data_analysis", params={"dataset": "customer_data.csv"}, priority=2),
        TaskSpec(name="generate_code", agent_type="code_generation", params={"requirement": "sort algorithm"}, priority=1),
        TaskSpec(name="create_docs", agent_type="documentation", params={"topic": "API endpoints"}, priority=3),
    ]
    
    for task in tasks:
        orchestrator.add_task(task)
    
    # 执行所有任务
    await orchestrator.execute_tasks()
    
    print("All orchestrated tasks completed")
    
    agent_manager.shutdown()
    orchestrator.shutdown()


async def demo_context_sharing():
    """演示上下文共享机制"""
    print("\n=== 演示上下文共享机制 ===")
    
    context_sharer = ContextSharer()
    
    # 演示目录共享
    context_sharer.share_directory('src_dir', './src')
    context_sharer.share_directory('test_dir', './tests')
    
    print(f"Shared src_dir: {context_sharer.get_shared_data('directory', 'src_dir')}")
    print(f"Shared test_dir: {context_sharer.get_shared_data('directory', 'test_dir')}")
    
    # 演示注释检查结果共享
    context_sharer.share_comment_result('file1.py', {'issues': 5, 'warnings': 2})
    context_sharer.share_comment_result('file2.py', {'issues': 0, 'warnings': 1})
    
    print(f"Comment check for file1.py: {context_sharer.get_shared_data('comment', 'file1.py')}")
    print(f"Comment check for file2.py: {context_sharer.get_shared_data('comment', 'file2.py')}")
    
    # 演示上下文窗口管理
    context_sharer.add_to_context_window('code_snippet', 'def hello():\n    print("Hello, world!")')
    context_sharer.add_to_context_window('documentation', '# This is a sample documentation')
    
    print(f"Context window size: {context_sharer.context_window_monitor.get_current_size()}")
    print(f"Code snippet: {context_sharer.get_shared_data('context_window', 'code_snippet')}")


async def main():
    """主函数 - 运行所有演示"""
    print("DNASPEC 技能包优化架构演示")
    print("=" * 50)
    
    await demo_hook_system()
    await demo_plugin_system()
    await demo_agents()
    await demo_tools()
    await demo_background_tasks()
    await demo_sisyphus_orchestrator()
    await demo_context_sharing()
    
    print("\n" + "=" * 50)
    print("所有演示完成！")


if __name__ == "__main__":
    asyncio.run(main())