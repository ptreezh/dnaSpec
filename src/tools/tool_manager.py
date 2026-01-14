import subprocess
import os
from typing import Dict, Any, Callable
from .hooks.hook_system import hook_manager, HookContext, HookType

class ToolManager:
    """工具管理器，集成LSP, AST-Grep, Grep, Glob, Bash等工具"""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.initialized = False
        self._register_default_tools()
    
    def _register_default_tools(self):
        """注册默认工具"""
        self.tools['lsp'] = self._lsp_tool
        self.tools['ast_grep'] = self._ast_grep_tool
        self.tools['grep'] = self._grep_tool
        self.tools['glob'] = self._glob_tool
        self.tools['bash'] = self._bash_tool
    
    def initialize(self):
        """初始化工具管理器"""
        self.initialized = True
        print("ToolManager initialized with LSP, AST-Grep, Grep, Glob, Bash tools")
    
    def shutdown(self):
        """关闭工具管理器"""
        self.initialized = False
        print("ToolManager shutdown")
    
    def register_tool(self, name: str, func: Callable):
        """注册工具"""
        self.tools[name] = func
        
        # 触发工具注册hook
        context = HookContext(
            hook_name='tool_registered',
            hook_type=HookType.TOOL,
            data={'tool_name': name, 'tool_func': func}
        )
        hook_manager.trigger_hook('tool_registered', context)
    
    def execute_tool(self, name: str, params: Dict[str, Any]) -> Any:
        """执行工具"""
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found")
        
        # 触发工具执行前hook
        context = HookContext(
            hook_name='tool_before_execute',
            hook_type=HookType.TOOL,
            data={'tool_name': name, 'params': params}
        )
        hook_manager.trigger_hook('tool_before_execute', context)
        
        try:
            result = self.tools[name](params)
            
            # 触发工具执行后hook
            context = HookContext(
                hook_name='tool_after_execute',
                hook_type=HookType.TOOL,
                data={'tool_name': name, 'params': params, 'result': result}
            )
            hook_manager.trigger_hook('tool_after_execute', context)
            
            return result
        except Exception as e:
            # 触发工具错误hook
            context = HookContext(
                hook_name='tool_error',
                hook_type=HookType.TOOL,
                data={'tool_name': name, 'params': params, 'error': e}
            )
            hook_manager.trigger_hook('tool_error', context)
            
            raise e
    
    def _lsp_tool(self, params: Dict[str, Any]) -> Any:
        """LSP工具实现"""
        # 这里应该连接到实际的LSP服务器
        # 为了演示，我们返回模拟结果
        file_path = params.get('file_path', '')
        action = params.get('action', 'diagnostics')  # diagnostics, completion, definition等
        
        return {
            'tool': 'lsp',
            'file_path': file_path,
            'action': action,
            'result': f'LSP {action} for {file_path}'
        }
    
    def _ast_grep_tool(self, params: Dict[str, Any]) -> Any:
        """AST-Grep工具实现"""
        pattern = params.get('pattern', '')
        paths = params.get('paths', ['.'])
        
        # 模拟AST-Grep命令执行
        cmd = ['ast-grep', '--pattern', pattern] + paths
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return {
                'tool': 'ast-grep',
                'pattern': pattern,
                'paths': paths,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'tool': 'ast-grep',
                'pattern': pattern,
                'paths': paths,
                'error': 'Command timed out'
            }
        except FileNotFoundError:
            return {
                'tool': 'ast-grep',
                'pattern': pattern,
                'paths': paths,
                'error': 'ast-grep command not found'
            }
    
    def _grep_tool(self, params: Dict[str, Any]) -> Any:
        """Grep工具实现"""
        pattern = params.get('pattern', '')
        paths = params.get('paths', ['.'])
        flags = params.get('flags', '')
        
        # 构建grep命令
        cmd = ['grep', '-r', pattern] + paths
        if flags:
            cmd.insert(1, flags)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return {
                'tool': 'grep',
                'pattern': pattern,
                'paths': paths,
                'flags': flags,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'tool': 'grep',
                'pattern': pattern,
                'paths': paths,
                'flags': flags,
                'error': 'Command timed out'
            }
        except FileNotFoundError:
            return {
                'tool': 'grep',
                'pattern': pattern,
                'paths': paths,
                'flags': flags,
                'error': 'grep command not found'
            }
    
    def _glob_tool(self, params: Dict[str, Any]) -> Any:
        """Glob工具实现"""
        import glob
        
        pattern = params.get('pattern', '*')
        recursive = params.get('recursive', False)
        
        if recursive:
            matches = glob.glob(pattern, recursive=True)
        else:
            matches = glob.glob(pattern)
        
        return {
            'tool': 'glob',
            'pattern': pattern,
            'recursive': recursive,
            'matches': matches
        }
    
    def _bash_tool(self, params: Dict[str, Any]) -> Any:
        """Bash工具实现"""
        command = params.get('command', '')
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=60,
                cwd=params.get('cwd', os.getcwd())
            )
            return {
                'tool': 'bash',
                'command': command,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'tool': 'bash',
                'command': command,
                'error': 'Command timed out'
            }