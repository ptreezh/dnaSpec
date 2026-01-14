"""
项目初始化脚本 - 自动生成协同契约和钩子系统
"""
import os
import sys
import json
from pathlib import Path

def initialize_coordination_contract():
    """初始化协同契约系统"""
    print("🔄 初始化DNASPEC认知协同契约系统...")
    
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    
    # 1. 创建契约文件（如果不存在）
    contract_path = project_root / "CONTRACT.yaml"
    if not contract_path.exists():
        print(f"📄 创建协同契约文件: {contract_path}")
        create_contract_file(contract_path)
    else:
        print(f"✅ 协同契约文件已存在: {contract_path}")
    
    # 2. 确保核心协同模块存在
    core_path = project_root / "src" / "dna_spec_kit_integration" / "core"
    
    # 3. 增强所有技能以支持协同
    print("🔧 增强技能以支持协同契约...")
    enhance_all_skills_with_coordination()
    
    # 4. 生成契约初始化报告
    print("📋 生成协同契约初始化报告...")
    generate_contract_report()
    
    print("✅ DNASPEC认知协同契约系统初始化完成!")
    print("🔒 所有技能现在都受协同契约约束")
    print("🛡️  一级优先级协同（强制执行）已激活")
    print("⚠️  二级优先级协同（推荐执行）已配置")

def create_contract_file(contract_path: Path):
    """创建契约文件"""
    contract_content = """---
version: "1.0.0"
created: "2025-12-15T20:00:00Z"
last_updated: "2025-12-15T20:00:00Z"

contract:
  title: "DNASPEC认知协同契约"
  description: "定义技能间协同机制的强制性契约"
  
  enforcement:
    # 一级优先级（强制执行）
    mandatory_coordination:
      - name: "temp_file_management"
        description: "临时文件管理协同：prevent提交临时文件到Git"
        level: "HARD_BLOCK"
        skills: ["temp_workspace", "temp_workspace_constitutional", "git_operations", "git_operations_constitutional"]
      
      - name: "context_chain_integrity" 
        description: "上下文链完整性：ensure context passing between analysis→optimization→template"
        level: "HARD_BLOCK"
        skills: ["context_analysis", "context_optimization", "cognitive_template", 
                "context_analysis_constitutional", "context_optimization_constitutional", "cognitive_template_constitutional"]
      
      - name: "security_constraint"
        description: "安全约束：force constitutional validation for all operations"
        level: "HARD_BLOCK" 
        skills: ["all_skills"]
    
    # 二级优先级（推荐执行）
    recommended_coordination:
      - name: "directory_structure_consistency"
        description: "目录结构一致性：maintain structural integrity during operations"
        level: "SOFT_BLOCK"
        skills: ["progressive_disclosure", "progressive_disclosure_constitutional", "git_operations", "git_operations_constitutional"]
      
      - name: "state_sharing"
        description: "状态共享：share quality metrics and validation status"
        level: "WARN"
        skills: ["all_construction_skills"]
      
      - name: "workspace_coordination" 
        description: "工作区协同：manage concurrent workspace access"
        level: "SOFT_BLOCK"
        skills: ["temp_workspace", "temp_workspace_constitutional"]
  
  shared_state_schema:
    temp_workspace:
      active_session: nullable string
      temp_files: array of string
      confirmed_files: array of string  
      session_start_time: nullable string
      
    context_chain:
      current_analysis: nullable object
      optimization_flags: array of string
      quality_scores: object
      context_id: nullable string
      
    security:
      validation_rules: array of string
      violation_tracker: array of object
      access_control: object
      
    directory_structure:
      current_structure: object
      proposed_changes: array of string
      consistency_status: string
      
    performance:
      quality_scores: object
      validation_stats: object
      execution_times: object

  hooks:
    pre_execution:
      - name: "contract_enforcement_check"
        description: "Execute contract checks before skill execution"
        mandatory: true
        
    post_execution: 
      - name: "contract_compliance_verification"
        description: "Verify contract compliance after skill execution"
        mandatory: true
        
    state_update:
      - name: "shared_state_sync"
        description: "Sync shared state after coordinated operations"
        mandatory: true

  violation_penalties:
    HARD_BLOCK:
      description: "Block operation execution"
      trigger: "Critical contract violations"
      
    SOFT_BLOCK:
      description: "Warn and suggest correction"
      trigger: "Significant contract violations"
      
    WARN:
      description: "Log violation for monitoring"
      trigger: "Minor contract inconsistencies"
..."""
    
    with open(contract_path, 'w', encoding='utf-8') as f:
        f.write(contract_content)

def enhance_all_skills_with_coordination():
    """增强所有技能以支持协同契约"""
    from .core.coordination_hooks_injector import initialize_coordination_enforcement
    
    # 获取技能目录
    skills_dir = Path(__file__).parent / "skills"
    
    # 初始化协同执法系统
    enhanced_count, total_count = initialize_coordination_enforcement(str(skills_dir))
    
    print(f"✅ 协同强化: {enhanced_count}/{total_count} 个技能")

def generate_contract_report():
    """生成契约初始化报告"""
    from .core.coordination_enforcer import ENFORCER
    
    report = ENFORCER.get_violation_report()
    
    print(f"📊 协同执法系统状态:")
    print(f"   - 总违规模块: {report['total_violations']}")
    print(f"   - 最近违规模块: {len(report['recent_violations'])}")
    
    # 按类型统计违规
    type_counts = report['violations_by_type']
    non_zero_types = {k: v for k, v in type_counts.items() if v > 0}
    if non_zero_types:
        print("   - 违规类型统计:")
        for vtype, count in non_zero_types.items():
            print(f"     * {vtype}: {count}")

def verify_contract_enforcement():
    """验证契约强制执行是否正常工作"""
    print("🔍 验证协同契约强制执行...")
    
    # 测试协同执法器是否正常工作
    from .core.coordination_enforcer import ENFORCER
    
    test_args = {"test": "data"}
    is_valid, message = ENFORCER.enforce_contract_before_execution("test_skill", test_args)
    
    if is_valid:
        print("✅ 协同执法器工作正常")
    else:
        print(f"⚠️  协同执法器测试: {message}")

if __name__ == "__main__":
    # 只当直接运行该脚本时才执行初始化
    initialize_coordination_contract()
    verify_contract_enforcement()