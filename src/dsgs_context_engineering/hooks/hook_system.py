"""
DNASPEC Hook System
基于spec.kit风格的文件变化监听和自动处理系统
"""
import os
import time
from typing import Dict, Any, Callable, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import fnmatch
import threading
from src.dnaspec_context_engineering.spec_engine import DSGSSpecEngine


class DSGSHookSystem:
    """
    DNASPEC Hook System
    基于文件系统变化的自动上下文工程处理系统
    """
    
    def __init__(self, spec_engine: DSGSSpecEngine):
        self.spec_engine = spec_engine
        self.hooks: List[Dict[str, Any]] = []
        self.observer = Observer()
        self.active_watchers = {}
    
    def register_hook(self, pattern: str, skill_name: str, params: Dict[str, Any] = None, 
                     triggers: List[str] = None) -> bool:
        """
        注册Hook
        
        Args:
            pattern: 文件匹配模式 (glob格式)
            skill_name: 要执行的技能名称
            params: 技能参数
            triggers: 触发事件类型 (created, modified, deleted)
        """
        if triggers is None:
            triggers = ['modified', 'created']  # 默认在文件修改和创建时触发
        
        hook_config = {
            'pattern': pattern,
            'skill_name': skill_name,
            'params': params or {},
            'triggers': triggers
        }
        
        self.hooks.append(hook_config)
        return True
    
    def load_hooks_from_config(self, config_path: str) -> bool:
        """
        从配置文件加载Hooks
        支持spec.kit风格的hook配置
        """
        import yaml
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            hooks_config = config.get('hooks', [])
            
            for hook_cfg in hooks_config:
                pattern = hook_cfg.get('pattern', '')
                skill_name = hook_cfg.get('skill', '')
                params = hook_cfg.get('params', {})
                triggers = hook_cfg.get('triggers', ['modified', 'created'])
                
                if pattern and skill_name:
                    self.register_hook(pattern, skill_name, params, triggers)
            
            return True
        except Exception as e:
            print(f"Error loading hooks from config: {str(e)}")
            return False
    
    def watch_directory(self, directory: str, recursive: bool = True) -> bool:
        """
        监视目录变化
        """
        try:
            event_handler = DSGSDirectoryEventHandler(
                self, 
                directory, 
                self.hooks
            )
            
            self.observer.schedule(event_handler, directory, recursive=recursive)
            return True
        except Exception as e:
            print(f"Error setting up directory watching: {str(e)}")
            return False
    
    def start_watching(self):
        """
        开始监视
        """
        self.observer.start()
    
    def stop_watching(self):
        """
        停止监视
        """
        self.observer.stop()
        self.observer.join()
    
    def process_file_change(self, file_path: str, event_type: str) -> List[Dict[str, Any]]:
        """
        处理文件变化事件
        执行匹配的Hook
        """
        results = []
        filename = os.path.basename(file_path)
        
        for hook in self.hooks:
            # 检查是否匹配模式和事件类型
            if event_type in hook['triggers'] and fnmatch.fnmatch(filename, hook['pattern']):
                # 读取文件内容
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    
                    # 执行对应的技能
                    params = hook['params'].copy()
                    params['file_path'] = file_path
                    
                    result = self.spec_engine.execute_skill(
                        hook['skill_name'], 
                        file_content, 
                        params
                    )
                    
                    results.append({
                        'hook': hook,
                        'file': file_path,
                        'event': event_type,
                        'result': result,
                        'processed_at': time.time()
                    })
                    
                except Exception as e:
                    results.append({
                        'hook': hook,
                        'file': file_path,
                        'event': event_type,
                        'error': str(e),
                        'processed_at': time.time()
                    })
        
        return results


class DSGSDirectoryEventHandler(FileSystemEventHandler):
    """
    DSGS目录事件处理器
    """
    
    def __init__(self, hook_system: DSGSHookSystem, watched_dir: str, hooks: List[Dict[str, Any]]):
        super().__init__()
        self.hook_system = hook_system
        self.watched_dir = watched_dir
        self.hooks = hooks
    
    def on_modified(self, event):
        if not event.is_directory:
            self._process_event(event.src_path, 'modified')
    
    def on_created(self, event):
        if not event.is_directory:
            self._process_event(event.src_path, 'created')
    
    def on_deleted(self, event):
        if not event.is_directory:
            self._process_event(event.src_path, 'deleted')
    
    def _process_event(self, file_path: str, event_type: str):
        """
        处理文件事件
        """
        # 在独立线程中处理以避免阻塞文件系统监听
        thread = threading.Thread(target=self._handle_event, args=(file_path, event_type))
        thread.daemon = True
        thread.start()
    
    def _handle_event(self, file_path: str, event_type: str):
        """
        实际处理事件的方法
        """
        results = self.hook_system.process_file_change(file_path, event_type)
        
        # 可以在这里添加结果处理逻辑
        # 例如：保存处理结果、发送通知等
        for result in results:
            if 'result' in result:
                print(f"Hook executed for {result['file']}: {result['result']['success']}")
            elif 'error' in result:
                print(f"Hook error for {result['file']}: {result['error']}")


# 示例Hook配置文件格式
HOOK_CONFIG_EXAMPLE = """
# hooks_config.yaml
# spec.kit风格的Hook配置文件

hooks:
  - pattern: "*.md"
    skill: "context-analysis"
    params:
      metrics: ["clarity", "completeness"]
    triggers: ["created", "modified"]
  
  - pattern: "*.py"
    skill: "context-optimization" 
    params:
      optimization_goals: ["clarity", "relevance"]
    triggers: ["modified"]
    
  - pattern: "*.txt"
    skill: "cognitive-template"
    params:
      template: "chain_of_thought"
    triggers: ["created"]
"""


def create_example_hook_config(config_path: str = "hooks_config.yaml"):
    """
    创建示例Hook配置文件
    """
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(HOOK_CONFIG_EXAMPLE)
    
    print(f"示例Hook配置文件已创建: {config_path}")


if __name__ == "__main__":
    # 示例使用
    from src.dnaspec_context_engineering.spec_engine import engine
    
    hook_system = DSGSHookSystem(engine)
    
    # 注册Hook
    hook_system.register_hook(
        pattern="*.md",
        skill_name="context-analysis", 
        params={"metrics": ["clarity", "completeness"]},
        triggers=["modified"]
    )
    
    # 开始监视当前目录
    hook_system.watch_directory("./documents")
    hook_system.start_watching()
    
    try:
        print("Hook系统正在运行，按Ctrl+C停止...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        hook_system.stop_watching()
        print("Hook系统已停止")