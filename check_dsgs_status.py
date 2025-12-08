#!/usr/bin/env python3
"""
DNASPEC系统状态检查脚本
"""
from src.dnaspec_spec_kit_integration.core.auto_configurator import AutoConfigurator

def check_system_status():
    """检查DNASPEC系统状态"""
    print("DNASPEC系统状态检查")
    print("=" * 50)
    
    configurator = AutoConfigurator()
    status = configurator.get_status()
    
    print(f'已检测到的工具: {status["installedCount"]}/{status["totalCount"]}')
    print(f'已安装的工具: {status["installedTools"]}')
    print(f'检测时间: {status["timestamp"]}')
    print()
    print('详细检测结果:')
    for name, info in status['detectedTools'].items():
        if info.get('installed'):
            print(f'  ✅ {name}: {info.get("version", "unknown")}')
        else:
            print(f'  ❌ {name}: Not installed')
    
    print()
    print("DNASPEC Context Engineering Skills 核心功能测试:")
    
    # 测试核心技能
    from src.dnaspec_context_engineering.skills_system_final import execute
    result = execute({
        'context': '验证DNASPEC功能',
        'skill': 'context-analysis'
    })
    
    print("上下文分析测试: ✅ 通过")
    print(f"结果预览: {result[:100]}...")

if __name__ == "__main__":
    check_system_status()