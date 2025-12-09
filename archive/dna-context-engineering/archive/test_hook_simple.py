"""
简单的Hook系统测试脚本
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.dnaspec_spec_kit_integration.core.hook import HookSystem, HookConfig, HookResult
    print("Hook系统导入成功")
    
    # 测试HookConfig
    config = HookConfig()
    print(f"Hook配置初始化成功: enabled={config.enabled}")
    
    # 测试HookSystem
    hook_system = HookSystem()
    print(f"Hook系统初始化成功: interceptors={len(hook_system._interceptors)}")
    
    # 测试命令检测
    is_spec_kit = hook_system._is_spec_kit_command("/speckit.dnaspec.architect 设计系统")
    print(f"Spec.kit命令检测: {is_spec_kit}")
    
    is_natural = hook_system._is_natural_language_request("设计一个系统架构")
    print(f"自然语言请求检测: {is_natural}")
    
    print("所有基本测试通过!")
    
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()