import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from plugin import MyOpenCodePlugin
    print("SUCCESS: MyOpenCodePlugin imported successfully")
except ImportError as e:
    print(f"ERROR: Failed to import MyOpenCodePlugin: {e}")
    import traceback
    traceback.print_exc()

try:
    from hooks.hook_system import hook_manager, HookContext, HookType
    print("SUCCESS: Hook system imported successfully")
except ImportError as e:
    print(f"ERROR: Failed to import hook system: {e}")
    import traceback
    traceback.print_exc()

try:
    from background_task_manager import BackgroundTaskManager
    print("SUCCESS: BackgroundTaskManager imported successfully")
except ImportError as e:
    print(f"ERROR: Failed to import BackgroundTaskManager: {e}")
    import traceback
    traceback.print_exc()

try:
    from sisyphus import SisyphusOrchestrator
    print("SUCCESS: SisyphusOrchestrator imported successfully")
except ImportError as e:
    print(f"ERROR: Failed to import SisyphusOrchestrator: {e}")
    import traceback
    traceback.print_exc()

try:
    from agents.agent_manager import AgentManager
    print("SUCCESS: AgentManager imported successfully")
except ImportError as e:
    print(f"ERROR: Failed to import AgentManager: {e}")
    import traceback
    traceback.print_exc()

try:
    from tools.tool_manager import ToolManager
    print("SUCCESS: ToolManager imported successfully")
except ImportError as e:
    print(f"ERROR: Failed to import ToolManager: {e}")
    import traceback
    traceback.print_exc()

try:
    from context.context_sharing import ContextSharer
    print("SUCCESS: ContextSharer imported successfully")
except ImportError as e:
    print(f"ERROR: Failed to import ContextSharer: {e}")
    import traceback
    traceback.print_exc()

try:
    from mcp.mcp_server import MCPServer
    print("SUCCESS: MCPServer imported successfully")
except ImportError as e:
    print(f"ERROR: Failed to import MCPServer: {e}")
    import traceback
    traceback.print_exc()