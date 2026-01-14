import asyncio
from typing import Callable, Any, List, Dict
from enum import Enum
from dataclasses import dataclass
from abc import ABC, abstractmethod

class HookType(Enum):
    PLUGIN = "plugin"
    TOOL = "tool"
    AGENT = "agent"
    SKILL = "skill"
    HOOK = "hook"

@dataclass
class HookContext:
    """Hook执行上下文"""
    hook_name: str
    hook_type: HookType
    data: Dict[str, Any]
    result: Any = None
    cancelled: bool = False

class HookManager:
    """Hook管理系统"""
    def __init__(self):
        self._hooks: Dict[str, List[Callable]] = {}
        self._middleware: List[Callable] = []
    
    def register_hook(self, hook_name: str, callback: Callable):
        """注册hook回调函数"""
        if hook_name not in self._hooks:
            self._hooks[hook_name] = []
        self._hooks[hook_name].append(callback)
    
    def unregister_hook(self, hook_name: str, callback: Callable):
        """注销hook回调函数"""
        if hook_name in self._hooks and callback in self._hooks[hook_name]:
            self._hooks[hook_name].remove(callback)
    
    async def trigger_hook(self, hook_name: str, context: HookContext) -> HookContext:
        """触发hook并执行所有注册的回调函数"""
        # 执行中间件
        for middleware in self._middleware:
            await middleware(context)
        
        # 如果被中间件取消，则不执行后续回调
        if context.cancelled:
            return context
        
        # 执行所有注册的回调
        if hook_name in self._hooks:
            for callback in self._hooks[hook_name]:
                try:
                    result = callback(context)
                    if asyncio.iscoroutine(result):
                        await result
                except Exception as e:
                    print(f"Hook {hook_name} callback failed: {e}")
        
        return context
    
    def add_middleware(self, middleware: Callable):
        """添加中间件"""
        self._middleware.append(middleware)

# 全局Hook管理器实例
hook_manager = HookManager()