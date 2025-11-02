"""
Hook系统
提供命令拦截、用户意图检测和自动技能调用功能
"""
import re
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass


@dataclass
class HookResult:
    """Hook处理结果"""
    intercepted: bool
    handled: bool
    skill_name: Optional[str] = None
    skill_result: Optional[Dict[str, Any]] = None
    processing_time: float = 0.0
    error_message: str = ""


class HookConfig:
    """Hook配置管理"""
    
    def __init__(self):
        self.enabled = True
        self.intercept_spec_kit_commands = True
        self.intercept_text_commands = True
        self.auto_invoke_threshold = 0.6  # 自动调用置信度阈值
        self.enabled_skills = []  # 启用的技能列表
        self.disabled_patterns = []  # 禁用的模式列表
        self.hook_timeout = 5.0  # Hook处理超时时间（秒）
    
    def enable_skill(self, skill_name: str):
        """启用特定技能"""
        if skill_name not in self.enabled_skills:
            self.enabled_skills.append(skill_name)
    
    def disable_skill(self, skill_name: str):
        """禁用特定技能"""
        if skill_name in self.enabled_skills:
            self.enabled_skills.remove(skill_name)
    
    def add_disabled_pattern(self, pattern: str):
        """添加禁用模式"""
        if pattern not in self.disabled_patterns:
            self.disabled_patterns.append(pattern)
    
    def is_skill_enabled(self, skill_name: str) -> bool:
        """检查技能是否启用"""
        return not self.enabled_skills or skill_name in self.enabled_skills
    
    def is_pattern_disabled(self, text: str) -> bool:
        """检查模式是否被禁用"""
        for pattern in self.disabled_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False


class HookSystem:
    """Hook系统主类"""
    
    def __init__(self, skill_manager=None):
        self.skill_manager = skill_manager
        self.config = HookConfig()
        self._interceptors = []  # 拦截器列表
        self._processors = []    # 处理器列表
        self._hooks = {}         # 注册的钩子函数
        self._command_patterns = self._initialize_command_patterns()
    
    def _initialize_command_patterns(self) -> Dict[str, re.Pattern]:
        """初始化命令模式"""
        return {
            'spec_kit_command': re.compile(r'^/speckit\.dsgs\.\w+', re.IGNORECASE),
            'slash_command': re.compile(r'^/\w+'),
            'natural_language': re.compile(r'(?:设计|创建|分解|检查|生成|优化)\s+\w+'),
        }
    
    def register_interceptor(self, interceptor_func: Callable[[str], bool]):
        """注册拦截器"""
        self._interceptors.append(interceptor_func)
    
    def register_processor(self, processor_func: Callable[[str], Dict[str, Any]]):
        """注册处理器"""
        self._processors.append(processor_func)
    
    def register_hook(self, hook_name: str, hook_func: Callable[[str], HookResult]):
        """注册钩子函数"""
        self._hooks[hook_name] = hook_func
    
    def intercept_request(self, user_request: str) -> HookResult:
        """拦截用户请求"""
        import time
        start_time = time.time()
        
        # 检查Hook系统是否启用
        if not self.config.enabled:
            return HookResult(intercepted=False, handled=False)
        
        # 检查是否被禁用模式匹配
        if self.config.is_pattern_disabled(user_request):
            return HookResult(intercepted=False, handled=False)
        
        try:
            # 1. 检查是否为spec.kit命令
            if self.config.intercept_spec_kit_commands and self._is_spec_kit_command(user_request):
                result = self._handle_spec_kit_command(user_request)
                result.processing_time = time.time() - start_time
                return result
            
            # 2. 检查是否为自然语言请求
            if self.config.intercept_text_commands and self._is_natural_language_request(user_request):
                result = self._handle_natural_language_request(user_request)
                result.processing_time = time.time() - start_time
                return result
            
            # 3. 检查其他拦截器
            for interceptor in self._interceptors:
                if interceptor(user_request):
                    # 尝试处理请求
                    for processor in self._processors:
                        try:
                            process_result = processor(user_request)
                            if process_result:
                                result = HookResult(
                                    intercepted=True,
                                    handled=True,
                                    skill_name=process_result.get('skill_name'),
                                    skill_result=process_result
                                )
                                result.processing_time = time.time() - start_time
                                return result
                        except Exception:
                            continue
            
            # 没有拦截到请求
            return HookResult(intercepted=False, handled=False)
            
        except Exception as e:
            return HookResult(
                intercepted=True,
                handled=False,
                error_message=str(e),
                processing_time=time.time() - start_time
            )
    
    def _is_spec_kit_command(self, request: str) -> bool:
        """检查是否为spec.kit命令"""
        return bool(self._command_patterns['spec_kit_command'].match(request))
    
    def _is_natural_language_request(self, request: str) -> bool:
        """检查是否为自然语言请求"""
        # 简单检查：包含中文或英文单词，且长度适中
        return bool(re.search(r'[\u4e00-\u9fff\w]', request)) and len(request.strip()) > 2
    
    def _handle_spec_kit_command(self, command: str) -> HookResult:
        """处理spec.kit命令"""
        if not self.skill_manager:
            return HookResult(
                intercepted=True,
                handled=False,
                error_message="Skill manager not available"
            )
        
        # 解析命令，提取技能名称
        skill_name_match = re.search(r'/speckit\.dsgs\.(\w+)', command, re.IGNORECASE)
        if not skill_name_match:
            return HookResult(
                intercepted=True,
                handled=False,
                error_message="Invalid spec.kit command format"
            )
        
        skill_name = f"dsgs-{skill_name_match.group(1)}"
        
        # 检查技能是否启用
        if not self.config.is_skill_enabled(skill_name):
            return HookResult(
                intercepted=True,
                handled=False,
                error_message=f"Skill {skill_name} is disabled"
            )
        
        # 执行技能
        try:
            result = self.skill_manager.execute_spec_kit_command(command)
            return HookResult(
                intercepted=True,
                handled=True,
                skill_name=skill_name,
                skill_result=result
            )
        except Exception as e:
            return HookResult(
                intercepted=True,
                handled=False,
                error_message=str(e)
            )
    
    def _handle_natural_language_request(self, request: str) -> HookResult:
        """处理自然语言请求"""
        if not self.skill_manager:
            return HookResult(
                intercepted=True,
                handled=False,
                error_message="Skill manager not available"
            )
        
        # 使用智能匹配系统
        match_result = self.skill_manager.match_skill_intelligently(request)
        
        if not match_result:
            return HookResult(
                intercepted=True,
                handled=False,
                error_message="No matching skill found"
            )
        
        # 检查置信度和技能启用状态
        if match_result['confidence'] < self.config.auto_invoke_threshold:
            return HookResult(
                intercepted=True,
                handled=False,
                error_message=f"Confidence too low: {match_result['confidence']:.2f}"
            )
        
        if not self.config.is_skill_enabled(match_result['skill_name']):
            return HookResult(
                intercepted=True,
                handled=False,
                error_message=f"Skill {match_result['skill_name']} is disabled"
            )
        
        # 自动执行匹配的技能
        try:
            skill_result = self.skill_manager.execute_skill(
                match_result['skill_name'], 
                request
            )
            
            return HookResult(
                intercepted=True,
                handled=True,
                skill_name=match_result['skill_name'],
                skill_result={
                    'skill_result': skill_result,
                    'match_info': match_result
                }
            )
        except Exception as e:
            return HookResult(
                intercepted=True,
                handled=False,
                error_message=str(e)
            )
    
    def get_hook_info(self) -> Dict[str, Any]:
        """获取Hook系统信息"""
        return {
            'enabled': self.config.enabled,
            'interceptor_count': len(self._interceptors),
            'processor_count': len(self._processors),
            'hook_count': len(self._hooks),
            'enabled_skills': self.config.enabled_skills,
            'disabled_patterns': self.config.disabled_patterns,
            'auto_invoke_threshold': self.config.auto_invoke_threshold
        }