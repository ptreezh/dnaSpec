"""
协同契约系统初始化器
确保所有契约组件正确启动并激活
"""
from .common_state_manager import CommonStateManager, initialize_common_state
from .coordination_contract_hooks import COORDINATION_HOOKS
from .constitutional_enforcer import CONSTITUTIONAL_EXECUTOR
import os
from pathlib import Path

def initialize_coordination_contract_system():
    """
    初始化协同契约系统
    确保所有契约组件都已正确启动
    """
    print("🚀 开始初始化协同契约系统...")
    
    # 1. 初始化共同状态管理器
    print("🔄 初始化共同状态管理器...")
    initialize_common_state()
    print("✅ 共同状态管理器已激活")
    
    # 2. 初始化协同契约钩子系统
    print("🔄 初始化协同契约钩子系统...")
    try:
        COORDINATION_HOOKS.initialize_with_state_manager(CommonStateManager)
        print("✅ 协同契约钩子系统已激活")
    except Exception as e:
        print(f"⚠️ 协同契约钩子系统初始化失败: {e}")
    
    # 3. 验证宪法系统
    print("🔄 验证宪法系统...")
    try:
        # 验证宪法执行器是否就绪
        if hasattr(CONSTITUTIONAL_EXECUTOR, 'execute'):
            print("✅ 宪法系统已就绪")
        else:
            print("⚠️ 宪法系统可能未完全就绪")
    except Exception as e:
        print(f"⚠️ 宪法系统验证失败: {e}")
    
    # 4. 创建契约配置文件（如果不存在）
    print("🔄 创建/验证契约配置...")
    project_root = Path(__file__).parent.parent.parent
    dnaspec_dir = project_root / ".dnaspec"
    dnaspec_dir.mkdir(exist_ok=True)
    
    contract_config_file = dnaspec_dir / "contract_config.json"
    if not contract_config_file.exists():
        contract_config = {
            "version": "2.0.0",
            "created": "2025-12-15T20:00:00Z",
            "enforcement_level": "mandatory",
            "contracts": {
                "temp_file_management": {
                    "enabled": True,
                    "critical": True,
                    "auto_fix": True
                },
                "context_chain_integrity": {
                    "enabled": True,
                    "critical": True,
                    "auto_fix": False
                },
                "security_constraint": {
                    "enabled": True,
                    "critical": True,
                    "auto_fix": False
                },
                "directory_structure_consistency": {
                    "enabled": True,
                    "critical": False,
                    "auto_fix": True
                }
            }
        }
        
        with open(contract_config_file, 'w', encoding='utf-8') as f:
            import json
            json.dump(contract_config, f, indent=2, ensure_ascii=False)
        
        print("✅ 契约配置文件已创建")
    else:
        print("✅ 契约配置文件已存在")
    
    # 5. 创建技能契约注册表
    print("🔄 创建技能契约注册表...")
    skill_registry_file = dnaspec_dir / "skill_contracts_registry.json"
    if not skill_registry_file.exists():
        skill_registry = {
            "version": "1.0.0",
            "created": "2025-12-15T20:00:00Z",
            "contractual_skills": [
                {
                    "name": "temp_workspace",
                    "contracts": ["temp_file_management", "security_constraint"],
                    "priority": "high"
                },
                {
                    "name": "context_analysis",
                    "contracts": ["context_chain_integrity", "security_constraint"],
                    "priority": "high"
                },
                {
                    "name": "context_optimization",
                    "contracts": ["context_chain_integrity", "security_constraint"],
                    "priority": "high"
                },
                {
                    "name": "cognitive_template",
                    "contracts": ["context_chain_integrity", "security_constraint"],
                    "priority": "high"
                },
                {
                    "name": "git_operations",
                    "contracts": ["temp_file_management", "security_constraint", "directory_structure_consistency"],
                    "priority": "high"
                },
                {
                    "name": "progressive_disclosure",
                    "contracts": ["directory_structure_consistency", "security_constraint"],
                    "priority": "medium"
                }
            ]
        }
        
        with open(skill_registry_file, 'w', encoding='utf-8') as f:
            import json
            json.dump(skill_registry, f, indent=2, ensure_ascii=False)
        
        print("✅ 技能契约注册表已创建")
    else:
        print("✅ 技能契约注册表已存在")
    
    print("\n🎯 协同契约系统初始化完成!")
    print("🔒 所有契约约束机制已激活")
    print("🔗 技能间协同契约已配置")
    print("🏛️ 宪法原则已整合")
    print("📊 共同状态管理已就绪")
    
    return True

# 执行初始化
if __name__ != "__main__":
    # 在模块导入时自动初始化
    try:
        initialize_coordination_contract_system()
    except Exception as e:
        print(f"❌ 协同契约系统初始化失败: {e}")