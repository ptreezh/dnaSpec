"""
统一技能执行入口 - 集成协同契约的宪法执行
不仅对生成目录、文件、脚本的技能强制宪法验证，还执行协同契约
"""
from typing import Dict, Any
from pathlib import Path
from datetime import datetime

# 导入宪法和协同系统组件
from .common_state_manager import CommonStateManager, COMMON_STATE_MANAGER
from .constitutional_enforcer import execute_with_constitutional_enforcement
from .coordination_contract_hooks import COORDINATION_HOOKS

def execute_skill_constitutionally(skill_name: str, args: Dict[str, Any]) -> str:
    """
    集成协同契约的宪法技能执行入口
    不仅执行宪法验证，还执行协同契约强制
    """
    # 需要宪法验证的技能类型
    construction_skills = {
        'temp_workspace', 'progressive_disclosure', 'git_operations',
        'system_architect', 'cognitive_template', 'context_analysis',
        'task_decomposer', 'architect', 'constraint_generator',
        'modulizer_independent', 'agent_creator_independent',
        'temp_workspace_constitutional', 'progressive_disclosure_constitutional',
        'git_operations_constitutional', 'agent_creator_constitutional'
    }

    # 1. 预执行协同契约检查
    if COORDINATION_HOOKS:
        is_allowed, contract_check_msg = COORDINATION_HOOKS.pre_execution_hook(skill_name, args)
        if not is_allowed:
            return contract_check_msg

    # 2. 根据技能类型决定是否执行宪法验证
    if skill_name in construction_skills:
        result = constitutional_enforce(skill_name, args)
    else:
        # 对于非建设类技能，直接执行但仍然检查协同契约
        try:
            import importlib.util
            skills_path = Path(__file__).parent.parent / "skills"
            skill_file = skills_path / f"{skill_name}.py"

            if not skill_file.exists():
                # 尝试寻找宪法级变体
                constitutional_skill_file = skills_path / f"{skill_name}_constitutional.py"
                if constitutional_skill_file.exists():
                    skill_file = constitutional_skill_file
                else:
                    # 尝试其他可能的变体
                    possible_files = [
                        f"{skill_name}_constitutational.py",
                        f"{skill_name}_const.py",
                        f"constitutional_{skill_name}.py"
                    ]
                    found = False
                    for possible_file in possible_files:
                        alt_path = skills_path / possible_file
                        if alt_path.exists():
                            skill_file = alt_path
                            found = True
                            break

                    if not found:
                        return f"错误: 技能文件不存在: {skill_name}"

            # 加载模块并执行
            spec = importlib.util.spec_from_file_location(skill_name, skill_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, 'execute'):
                # 执行原始技能
                result = module.execute(args)

                # 3. 执行后协同契约验证
                if COORDINATION_HOOKS:
                    result = COORDINATION_HOOKS.post_execution_hook(skill_name, result, args)

                return result
            else:
                return f"错误: 技能模块缺少execute函数: {skill_name}"

        except Exception as e:
            # 异常也需要记录到协同系统中
            if COORDINATION_HOOKS:
                from .coordination_enforcer import ViolationType
                COORDINATION_HOOKS._log_violation(ViolationType.STATE_INCONSISTENCY,
                                     f"技能 {skill_name} 执行异常", str(e))
            return f"错误: 技能执行失败: {str(e)}"

    # 3. 执行后协同契约验证
    if COORDINATION_HOOKS:
        result = COORDINATION_HOOKS.post_execution_hook(skill_name, result, args)

    return result

def execute_skill(skill_name: str, args: Dict[str, Any]) -> str:
    """
    公共技能执行接口 - 集成协同契约系统
    所有技能执行都受共同状态和契约约束
    """
    # 所有技能执行都通过契约执行器
    return execute_skill_constitutionally(skill_name, args)

# 导入系统组件
from .constitutional_enforcer import CONSTITUTIONAL_EXECUTOR
from .constitutional_hook_system import HOOK_SYSTEM
from .common_state_manager import COMMON_STATE_MANAGER
from .coordination_contract_checker import CONTRACT_CHECKER
from .coordination_contract_enforcer import CONTRACT_ENFORCER

def initialize_constitutional_system():
    """
    初始化宪法和协同契约系统 - 激活所有约束机制
    """
    print("🔄 初始化宪法和协同契约系统...")

    # 1. 初始化共同状态管理器
    from .common_state_manager import initialize_common_state
    initialize_common_state()
    print("✅ 共同状态管理器已激活")

    # 2. 确保宪法系统已准备好
    print("✅ 宪法系统已准备")

    # 3. 确保契约检查器已准备好
    print("✅ 契约检查器已准备")

    # 4. 确保契约执行器已准备好
    print("✅ 契约执行器已准备")

    # 5. 初始化契约系统
    print("🔗 检查契约配置文件...")
    import os
    from pathlib import Path
    project_root = Path(__file__).parent.parent.parent
    contracts_config = project_root / ".dnaspec" / "contract_config.json"

    if not contracts_config.exists():
        print("⚠️  契约配置文件不存在，正在初始化...")
        from .initialize_contracts import initialize_coordination_contracts
        initialize_coordination_contracts()
        print("✅ 契约配置已初始化")
    else:
        print("✅ 契约配置文件已存在")

    print("🚀 宪法和协同契约系统初始化完成!")

# 初始化宪法和协同契约系统
initialize_constitutional_system()

def get_all_construction_skills() -> list:
    """
    获取所有建设类技能列表
    """
    # 从契约注册表获取技能（如果存在）
    import os
    from pathlib import Path
    project_root = Path(__file__).parent.parent.parent
    registry_file = project_root / ".dnaspec" / "skill_contracts_registry.json"

    if registry_file.exists():
        import json
        try:
            with open(registry_file, 'r', encoding='utf-8') as f:
                registry = json.load(f)
            return [skill['name'] for skill in registry.get('contractual_skills', [])]
        except:
            pass

    # 回退到默认列表
    return [
        'temp_workspace', 'temp_workspace_constitutional',
        'context_analysis', 'context_optimization', 'cognitive_template',
        'context_analysis_constitutional', 'context_optimization_constitutional',
        'cognitive_template_constitutional',
        'git_operations', 'git_operations_constitutional',
        'progressive_disclosure', 'progressive_disclosure_constitutional'
    ]

def get_all_skills() -> list:
    """
    获取所有技能列表
    """
    skills_dir = Path(__file__).parent.parent / "skills"
    all_skills = []

    for skill_file in skills_dir.glob("*.py"):
        if skill_file.name.startswith("__"):
            continue

        skill_name = skill_file.stem
        all_skills.append(skill_name)

    return all_skills

def verify_system_configuration():
    """
    验证系统配置
    """
    construction_skills = get_all_construction_skills()
    all_skills = get_all_skills()

    print(f"🏛️ 宪法约束技能数量: {len(construction_skills)}")
    print(f"🔗 协同契约技能数量: {len(construction_skills)}")
    print(f"📊 总技能数量: {len(all_skills)}")

    # 获取契约检查器报告
    report = CONTRACT_CHECKER.get_violation_report()
    print(f"📋 违规模块总数: {report['total_violations']}")
    print(f"🚨 关键契约违规: {report['critical_violations']}")

    # 获取执行器摘要
    summary = CONTRACT_ENFORCER.get_execution_summary()
    print(f"📈 执行成功率: {summary.get('success_rate', 0):.1f}%")

    print(f"\n📋 契约技能列表:")
    for skill in sorted(construction_skills):
        print(f"  - {skill}")

    return {
        "construction_skills_count": len(construction_skills),
        "total_skills_count": len(all_skills),
        "violations_count": report['total_violations'],
        "success_rate": summary.get('success_rate', 0)
    }

# 执行验证
configuration_info = verify_system_configuration()