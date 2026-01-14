#!/usr/bin/env python3
"""
DNASPEC 架构 - TDD 测试 ContextSharer 系统
使用文件写入来记录测试结果
"""

def log_test_result(message, success=True):
    """记录测试结果到文件"""
    with open('tdd_test_results_context_sharer.txt', 'a', encoding='utf-8') as f:
        status = "✓" if success else "✗"
        f.write(f"{status} {message}\n")

def test_context_sharer_concept():
    """测试 ContextSharer 系统的概念实现"""
    try:
        # 定义 ContextSharer 组件
        from typing import Dict, Any, Optional
        
        class DirectoryInjector:
            """目录注入器"""
            def __init__(self):
                self.shared_directories: Dict[str, str] = {}
            
            def inject_directory(self, key: str, path: str):
                self.shared_directories[key] = path
            
            def get_directory(self, key: str) -> Optional[str]:
                return self.shared_directories.get(key)

        class CommentChecker:
            """注释检查器"""
            def __init__(self):
                self.comment_results: Dict[str, Any] = {}
            
            def store_result(self, file_path: str, result: Any):
                self.comment_results[file_path] = result
            
            def get_result(self, file_path: str) -> Optional[Any]:
                return self.comment_results.get(file_path)

        class ContextWindowMonitor:
            """上下文窗口监视器"""
            def __init__(self, max_size: int = 8000):
                self.max_size = max_size
                self.current_size = 0
                self.context_items: Dict[str, Any] = {}
            
            def add_context_item(self, key: str, content: str):
                size = len(content.encode('utf-8'))
                if self.current_size + size > self.max_size:
                    # 简单的清理策略：移除最旧的项
                    if self.context_items:
                        oldest_key = next(iter(self.context_items))
                        old_content = self.context_items.pop(oldest_key)
                        self.current_size -= len(old_content.encode('utf-8'))
                
                self.context_items[key] = content
                self.current_size += size
            
            def get_context_item(self, key: str) -> Optional[str]:
                return self.context_items.get(key)
            
            def get_current_size(self) -> int:
                return self.current_size

        class ContextSharer:
            """上下文共享器"""
            def __init__(self):
                self.directory_injector = DirectoryInjector()
                self.comment_checker = CommentChecker()
                self.context_window_monitor = ContextWindowMonitor()
            
            def share_directory(self, key: str, path: str):
                self.directory_injector.inject_directory(key, path)
            
            def share_comment_result(self, file_path: str, result: Any):
                self.comment_checker.store_result(file_path, result)
            
            def add_to_context_window(self, key: str, content: str):
                self.context_window_monitor.add_context_item(key, content)
            
            def get_shared_data(self, component_type: str, key: str):
                if component_type == 'directory':
                    return self.directory_injector.get_directory(key)
                elif component_type == 'comment':
                    return self.comment_checker.get_result(key)
                elif component_type == 'context_window':
                    return self.context_window_monitor.get_context_item(key)
                else:
                    return None

        # 测试 ContextSharer 功能
        context_sharer = ContextSharer()
        
        # 测试目录共享
        context_sharer.share_directory('src_dir', './src')
        src_path = context_sharer.get_shared_data('directory', 'src_dir')
        assert src_path == './src'
        
        # 测试注释检查结果共享
        context_sharer.share_comment_result('file1.py', {'issues': 5, 'warnings': 2})
        comment_result = context_sharer.get_shared_data('comment', 'file1.py')
        assert comment_result['issues'] == 5
        
        # 测试上下文窗口
        context_sharer.add_to_context_window('code', 'def hello(): pass')
        code_snippet = context_sharer.get_shared_data('context_window', 'code')
        assert 'hello' in code_snippet
        
        log_test_result("ContextSharer 系统概念验证通过", True)
        return True
        
    except Exception as e:
        log_test_result(f"ContextSharer 系统概念验证失败: {e}", False)
        return False

if __name__ == "__main__":
    test_context_sharer_concept()