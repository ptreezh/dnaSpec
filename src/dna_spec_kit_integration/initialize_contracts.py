"""
DNASPEC项目初始化脚本 - 自动设置协同契约系统
"""
import os
import json
from pathlib import Path
from datetime import datetime

def initialize_coordination_contracts():
    """初始化协同契约系统"""
    print("🚀 初始化 DNASEC 协同契约系统...")
    
    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent
    print(f"📁 项目根目录: {project_root}")
    
    # 1. 创建项目配置目录
    dnaspec_dir = project_root / ".dnaspec"
    dnaspec_dir.mkdir(exist_ok=True)
    print("✅ 配置目录已创建")
    
    # 2. 创建共同状态文件
    state_file = dnaspec_dir / "common_state.json"
    if not state_file.exists():
        print("📄 创建共同状态文件...")
        from .core.common_state_manager import CommonStateManager
        state_mgr = CommonStateManager(str(state_file))
        
        # 初始化默认状态
        default_state = state_mgr._initialize_default_state()
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(default_state, f, ensure_ascii=False, indent=2)
        print("✅ 共同状态文件已创建")
    else:
        print("📋 共同状态文件已存在")
    
    # 3. 创建契约配置文件
    contract_config_file = dnaspec_dir / "contract_config.json"
    if not contract_config_file.exists():
        print("📄 创建契约配置文件...")
        contract_config = {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "contracts": {
                "temp_file_management": {
                    "enabled": True,
                    "critical": True,
                    "auto_fix": True,
                    "description": "临时文件管理契约"
                },
                "context_chain_integrity": {
                    "enabled": True,
                    "critical": True,
                    "auto_fix": False,
                    "description": "上下文链完整性契约"
                },
                "security_constraint": {
                    "enabled": True,
                    "critical": True,
                    "auto_fix": False,
                    "description": "安全约束契约"
                },
                "directory_structure_consistency": {
                    "enabled": True,
                    "critical": False,
                    "auto_fix": True,
                    "description": "目录结构一致性契约"
                },
                "quality_maintenance": {
                    "enabled": True,
                    "critical": False,
                    "auto_fix": False,
                    "description": "质量维护契约"
                }
            },
            "settings": {
                "auto_update_shared_state": True,
                "enforce_strict_security": True,
                "enable_performance_monitoring": True,
                "violation_reporting_limit": 100
            }
        }
        
        with open(contract_config_file, 'w', encoding='utf-8') as f:
            json.dump(contract_config, f, ensure_ascii=False, indent=2)
        print("✅ 契约配置文件已创建")
    else:
        print("📋 契约配置文件已存在")
    
    # 4. 创建技能合约注册表
    skill_registry_file = dnaspec_dir / "skill_contracts_registry.json"
    if not skill_registry_file.exists():
        print("📄 创建技能合约注册表...")
        contract_registry = {
            "version": "1.0.0",
            "created": datetime.now().isoformat(),
            "contractual_skills": [
                {
                    "name": "temp_workspace",
                    "contracts": ["temp_file_management"],
                    "priority": "high",
                    "enforcement_level": "hard_block"
                },
                {
                    "name": "temp_workspace_constitutional", 
                    "contracts": ["temp_file_management", "security_constraint"],
                    "priority": "high",
                    "enforcement_level": "hard_block"
                },
                {
                    "name": "context_analysis",
                    "contracts": ["context_chain_integrity", "quality_maintenance"],
                    "priority": "medium", 
                    "enforcement_level": "hard_block"
                },
                {
                    "name": "context_optimization",
                    "contracts": ["context_chain_integrity", "quality_maintenance"],
                    "priority": "medium",
                    "enforcement_level": "hard_block"
                },
                {
                    "name": "cognitive_template",
                    "contracts": ["context_chain_integrity", "quality_maintenance"],
                    "priority": "medium",
                    "enforcement_level": "hard_block"
                },
                {
                    "name": "git_operations",
                    "contracts": ["temp_file_management", "security_constraint", "directory_structure_consistency"],
                    "priority": "high",
                    "enforcement_level": "hard_block"
                },
                {
                    "name": "progressive_disclosure",
                    "contracts": ["directory_structure_consistency", "quality_maintenance"],
                    "priority": "medium",
                    "enforcement_level": "soft_block"
                }
            ],
            "registration_date": datetime.now().isoformat()
        }
        
        with open(skill_registry_file, 'w', encoding='utf-8') as f:
            json.dump(contract_registry, f, ensure_ascii=False, indent=2)
        print("✅ 技能合约注册表已创建")
    else:
        print("📋 技能合约注册表已存在")
    
    # 5. 创建契约监控仪表盘配置
    dashboard_config_file = dnaspec_dir / "contract_dashboard_config.json"
    if not dashboard_config_file.exists():
        print("📄 创建契约监控仪表盘配置...")
        dashboard_config = {
            "title": "DNASPEC 协同契约监控仪表盘",
            "refresh_interval": 5000,
            "sections": [
                {
                    "name": "状态概览",
                    "widgets": [
                        {"type": "status_summary", "position": {"x": 0, "y": 0, "width": 6, "height": 4}},
                        {"type": "violation_timeline", "position": {"x": 6, "y": 0, "width": 6, "height": 4}}
                    ]
                },
                {
                    "name": "契约详情",
                    "widgets": [
                        {"type": "contract_status", "position": {"x": 0, "y": 0, "width": 12, "height": 6}},
                        {"type": "violation_details", "position": {"x": 0, "y": 6, "width": 12, "height": 6}}
                    ]
                }
            ],
            "created": datetime.now().isoformat()
        }
        
        with open(dashboard_config_file, 'w', encoding='utf-8') as f:
            json.dump(dashboard_config, f, ensure_ascii=False, indent=2)
        print("✅ 契约监控仪表盘配置已创建")
    else:
        print("📋 契约监控仪表盘配置已存在")
    
    # 6. 创建初始化状态快照
    snapshot_file = dnaspec_dir / "initialization_snapshot.json"
    print("📸 创建初始化状态快照...")
    from .core.common_state_manager import COMMON_STATE_MANAGER
    
    snapshot_data = {
        "snapshot_version": "1.0.0",
        "created": datetime.now().isoformat(),
        "system_state": COMMON_STATE_MANAGER.get_full_state_snapshot(),
        "init_status": "completed",
        "contracts_active": True,
        "shared_state_initialized": True
    }
    
    with open(snapshot_file, 'w', encoding='utf-8') as f:
        json.dump(snapshot_data, f, ensure_ascii=False, indent=2)
    
    print("✅ 初始化状态快照已创建")
    
    # 7. 输出初始化摘要
    print("\n" + "="*60)
    print("🎉 DNASPEC 协同契约系统初始化完成!")
    print("="*60)
    print("📋 已创建的文件:")
    print(f"   • 共同状态文件: {state_file}")
    print(f"   • 契约配置文件: {contract_config_file}")
    print(f"   • 技能合约注册表: {skill_registry_file}")
    print(f"   • 监控仪表盘配置: {dashboard_config_file}")
    print(f"   • 初始化快照: {snapshot_file}")
    print("\n🛡️  系统现在受到以下契约保护:")
    print("   • 临时文件管理契约 (禁止提交临时文件)")
    print("   • 上下文链完整性契约 (确保上下文传递)")
    print("   • 安全约束契约 (强制宪法验证)")
    print("   • 目录结构一致性契约 (保持结构完整)")
    print("   • 质量维护契约 (监控输出质量)")
    print("\n✅ 所有技能现在都将在共同状态下协同工作")
    print("="*60)

def verify_initialization():
    """验证初始化是否成功"""
    print("\n🔍 验证协同契约系统初始化...")
    
    project_root = Path(__file__).parent.parent.parent
    dnaspec_dir = project_root / ".dnaspec"
    
    files_to_check = [
        dnaspec_dir / "common_state.json",
        dnaspec_dir / "contract_config.json", 
        dnaspec_dir / "skill_contracts_registry.json",
        dnaspec_dir / "contract_dashboard_config.json",
        dnaspec_dir / "initialization_snapshot.json"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if file_path.exists():
            print(f"✅ {file_path.name} - 存在")
        else:
            print(f"❌ {file_path.name} - 缺失")
            all_exist = False
    
    if all_exist:
        print("\n✅ 所有必需文件都已创建，初始化验证通过!")
        return True
    else:
        print("\n❌ 初始化验证失败，请重新运行初始化程序!")
        return False

if __name__ == "__main__":
    # 如果直接运行此脚本，执行初始化
    initialize_coordination_contracts()
    verify_initialization()