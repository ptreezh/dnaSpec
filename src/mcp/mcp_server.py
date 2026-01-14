import asyncio
import json
from typing import Dict, Any, Callable
from .hooks.hook_system import hook_manager, HookContext, HookType

class MCPServer:
    """MCP集成：支持内置MCP服务器，自定义配置"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.capabilities = {}
        self.handlers = {}
        self.initialized = False
    
    def initialize(self):
        """初始化MCP服务器"""
        self._setup_capabilities()
        self.initialized = True
        print("MCPServer initialized")
    
    def shutdown(self):
        """关闭MCP服务器"""
        self.initialized = False
        print("MCPServer shutdown")
    
    def _setup_capabilities(self):
        """设置MCP能力"""
        self.capabilities = {
            "prompts": {
                "get": {
                    "available": True
                }
            },
            "transports": {
                "pipe": True,
                "stdio": True
            }
        }
    
    def register_handler(self, method: str, handler: Callable):
        """注册MCP方法处理器"""
        self.handlers[method] = handler
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理MCP请求"""
        method = request.get('method')
        params = request.get('params', {})
        
        if method in self.handlers:
            try:
                result = await self.handlers[method](params)
                
                # 触发工具执行后hook（将MCP视为一种工具）
                context = HookContext(
                    hook_name='tool_after_execute',
                    hook_type=HookType.TOOL,
                    data={'tool_name': 'mcp', 'method': method, 'params': params, 'result': result}
                )
                await hook_manager.trigger_hook('tool_after_execute', context)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request.get('id'),
                    "result": result
                }
            except Exception as e:
                # 触发工具错误hook
                context = HookContext(
                    hook_name='tool_error',
                    hook_type=HookType.TOOL,
                    data={'tool_name': 'mcp', 'method': method, 'params': params, 'error': e}
                )
                await hook_manager.trigger_hook('tool_error', context)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request.get('id'),
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.get('id'),
                "error": {
                    "code": -32601,
                    "message": f"Method {method} not found"
                }
            }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """获取MCP服务器能力"""
        return self.capabilities

# MCP集成示例
def setup_mcp_integration(plugin_instance):
    """设置MCP集成到主插件"""
    mcp_server = MCPServer(plugin_instance.config.get('mcp_config', {}))
    mcp_server.initialize()
    
    # 注册示例处理器
    async def get_prompts_handler(params):
        return {
            "prompts": [
                {
                    "name": "analyze-code",
                    "description": "Analyze code for potential issues",
                    "arguments": [
                        {
                            "name": "file_path",
                            "type": "string",
                            "description": "Path to the file to analyze"
                        }
                    ]
                }
            ]
        }
    
    mcp_server.register_handler('prompts/get', get_prompts_handler)
    
    # 将MCP服务器添加到插件实例
    plugin_instance.mcp_server = mcp_server
    return mcp_server