from typing import Dict, Any, Optional
from .hooks.hook_system import hook_manager, HookContext, HookType

class DirectoryInjector:
    """目录注入器 - 用于在不同组件间共享目录信息"""
    
    def __init__(self):
        self.shared_directories: Dict[str, str] = {}
    
    def inject_directory(self, key: str, path: str):
        """注入目录路径"""
        self.shared_directories[key] = path
        
        # 触发上下文更新hook
        context = HookContext(
            hook_name='agent_context_updated',
            hook_type=HookType.AGENT,
            data={'context_type': 'directory', 'key': key, 'path': path}
        )
        hook_manager.trigger_hook('agent_context_updated', context)
    
    def get_directory(self, key: str) -> Optional[str]:
        """获取目录路径"""
        return self.shared_directories.get(key)

class CommentChecker:
    """注释检查器 - 用于在不同组件间共享注释检查结果"""
    
    def __init__(self):
        self.comment_results: Dict[str, Any] = {}
    
    def store_result(self, file_path: str, result: Any):
        """存储注释检查结果"""
        self.comment_results[file_path] = result
        
        # 触发上下文更新hook
        context = HookContext(
            hook_name='agent_context_updated',
            hook_type=HookType.AGENT,
            data={'context_type': 'comment_check', 'file_path': file_path, 'result': result}
        )
        hook_manager.trigger_hook('agent_context_updated', context)
    
    def get_result(self, file_path: str) -> Optional[Any]:
        """获取注释检查结果"""
        return self.comment_results.get(file_path)

class ContextWindowMonitor:
    """上下文窗口监视器 - 监控和管理上下文窗口大小"""
    
    def __init__(self, max_size: int = 8000):  # 默认8000个token
        self.max_size = max_size
        self.current_size = 0
        self.context_items: Dict[str, Any] = {}
    
    def add_context_item(self, key: str, content: str):
        """添加上下文项"""
        size = len(content.encode('utf-8'))  # 简单估算大小
        if self.current_size + size > self.max_size:
            # 如果超出限制，移除最旧的项直到空间足够
            self._evict_old_items(size)
        
        self.context_items[key] = content
        self.current_size += size
        
        # 触发上下文更新hook
        context = HookContext(
            hook_name='agent_context_updated',
            hook_type=HookType.AGENT,
            data={'context_type': 'window_monitor', 'key': key, 'size_added': size, 'current_size': self.current_size}
        )
        hook_manager.trigger_hook('agent_context_updated', context)
    
    def get_context_item(self, key: str) -> Optional[str]:
        """获取上下文项"""
        return self.context_items.get(key)
    
    def get_current_size(self) -> int:
        """获取当前上下文大小"""
        return self.current_size
    
    def _evict_old_items(self, needed_size: int):
        """移除旧的上下文项以腾出空间"""
        # 简单实现：按添加顺序移除项
        keys_to_remove = []
        freed_size = 0
        
        for key, content in self.context_items.items():
            size = len(content.encode('utf-8'))
            keys_to_remove.append(key)
            freed_size += size
            
            if self.current_size - freed_size <= self.max_size - needed_size:
                break
        
        for key in keys_to_remove:
            content = self.context_items.pop(key)
            self.current_size -= len(content.encode('utf-8'))

class ContextSharer:
    """上下文共享器 - 整合所有上下文共享组件"""
    
    def __init__(self):
        self.directory_injector = DirectoryInjector()
        self.comment_checker = CommentChecker()
        self.context_window_monitor = ContextWindowMonitor()
    
    def share_directory(self, key: str, path: str):
        """共享目录路径"""
        self.directory_injector.inject_directory(key, path)
    
    def share_comment_result(self, file_path: str, result: Any):
        """共享注释检查结果"""
        self.comment_checker.store_result(file_path, result)
    
    def add_to_context_window(self, key: str, content: str):
        """添加到上下文窗口"""
        self.context_window_monitor.add_context_item(key, content)
    
    def get_shared_data(self, component_type: str, key: str):
        """根据组件类型和键获取共享数据"""
        if component_type == 'directory':
            return self.directory_injector.get_directory(key)
        elif component_type == 'comment':
            return self.comment_checker.get_result(key)
        elif component_type == 'context_window':
            return self.context_window_monitor.get_context_item(key)
        else:
            return None