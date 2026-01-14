from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .hooks.hook_system import hook_manager, HookContext, HookType
from .background_task_manager import BackgroundTaskManager
from .sisyphus import SisyphusOrchestrator
from .agents.agent_manager import AgentManager
from .tools.tool_manager import ToolManager

class PluginInterface(ABC):
    """插件接口"""
    
    @abstractmethod
    def initialize(self):
        """初始化插件"""
        pass
    
    @abstractmethod
    def shutdown(self):
        """关闭插件"""
        pass


class MyOpenCodePlugin(PluginInterface):
    """主插件类，整合了所有功能"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.background_task_manager = BackgroundTaskManager()
        self.sisyphus_orchestrator = SisyphusOrchestrator()
        self.agent_manager = AgentManager()
        self.tool_manager = ToolManager()
        self.initialized = False
        
        # 注册插件相关的hooks
        self._register_plugin_hooks()
    
    def _register_plugin_hooks(self):
        """注册插件相关的hooks"""
        hook_manager.register_hook('plugin_loaded', self._on_plugin_loaded)
        hook_manager.register_hook('plugin_initialized', self._on_plugin_initialized)
        hook_manager.register_hook('plugin_config_changed', self._on_config_changed)
        hook_manager.register_hook('plugin_before_shutdown', self._on_before_shutdown)
        hook_manager.register_hook('plugin_after_shutdown', self._on_after_shutdown)
    
    def _on_plugin_loaded(self, context: HookContext):
        """插件加载后的处理"""
        print(f"MyOpenCodePlugin loaded with config: {self.config}")
    
    def _on_plugin_initialized(self, context: HookContext):
        """插件初始化后的处理"""
        print("MyOpenCodePlugin initialized successfully")
    
    def _on_config_changed(self, context: HookContext):
        """配置变更时的处理"""
        new_config = context.data.get('new_config')
        print(f"Configuration changed: {new_config}")
        self.config = new_config
    
    def _on_before_shutdown(self, context: HookContext):
        """插件关闭前的处理"""
        print("Shutting down MyOpenCodePlugin...")
        self.shutdown()
    
    def _on_after_shutdown(self, context: HookContext):
        """插件关闭后的处理"""
        print("MyOpenCodePlugin shut down successfully")
    
    def initialize(self):
        """初始化插件"""
        # 初始化各组件
        self.background_task_manager.initialize()
        self.sisyphus_orchestrator.initialize()
        self.agent_manager.initialize()
        self.tool_manager.initialize()
        
        # 触发插件加载hook
        context = HookContext(
            hook_name='plugin_loaded',
            hook_type=HookType.PLUGIN,
            data={'plugin': self}
        )
        hook_manager.trigger_hook('plugin_loaded', context)
        
        # 触发插件初始化hook
        context = HookContext(
            hook_name='plugin_initialized',
            hook_type=HookType.PLUGIN,
            data={'plugin': self}
        )
        hook_manager.trigger_hook('plugin_initialized', context)
        
        self.initialized = True
    
    def shutdown(self):
        """关闭插件"""
        # 关闭各组件
        self.background_task_manager.shutdown()
        self.sisyphus_orchestrator.shutdown()
        self.agent_manager.shutdown()
        self.tool_manager.shutdown()
    
    def update_config(self, new_config: Dict[str, Any]):
        """更新配置"""
        context = HookContext(
            hook_name='plugin_config_changed',
            hook_type=HookType.PLUGIN,
            data={'old_config': self.config, 'new_config': new_config}
        )
        hook_manager.trigger_hook('plugin_config_changed', context)