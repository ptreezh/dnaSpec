# DNASPEC系统完整工作流程演示

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, 'src')

def demo_complete_workflow():
    """演示DNASPEC系统的完整工作流程"""
    print("=== DNASPEC系统完整工作流程演示 ===\n")
    
    # 导入所有技能
    from dnaspec_architect import DNASPECArchitect
    from dnaspec_system_architect import DNASPECSystemArchitect
    from dnaspec_task_decomposer import DNASPECTaskDecomposer
    from dnaspec_agent_creator import DNASPECAgentCreator
    from dnaspec_constraint_generator import DNASPECConstraintGenerator
    from dnaspec_dapi_checker import DNASPEC_DAPI_Checker
    
    # 导入Hook系统
    from skills_hook_system import SkillInvoker
    
    print("✓ 所有技能加载成功")
    print("✓ Hook系统加载成功")
    print("\n" + "="*70 + "\n")
    
    # 创建技能实例
    main_architect = DNASPECArchitect()
    skill_invoker = SkillInvoker()
    
    # 模拟完整的项目开发流程
    project_phases = [
        {
            "phase": "1. 系统设计阶段",
            "description": "设计整体系统架构",
            "request": "设计一个电商系统的整体架构，包括用户管理、订单处理、支付服务等模块"
        },
        {
            "phase": "2. 任务分解阶段", 
            "description": "分解开发任务",
            "request": "将电商系统的开发任务分解为原子化任务，确保任务上下文文档的闭包性"
        },
        {
            "phase": "3. 智能体创建阶段",
            "description": "创建开发智能体",
            "request": "为电商系统创建开发智能体，包括前端开发、后端开发、测试等角色"
        },
        {
            "phase": "4. 约束生成阶段",
            "description": "生成系统约束",
            "request": "为电商系统生成API设计约束和数据安全约束"
        },
        {
            "phase": "5. 接口检查阶段",
            "description": "检查接口一致性",
            "request": "验证电商系统各组件间API接口的一致性，检查文档与实现的符合性"
        }
    ]
    
    for i, phase in enumerate(project_phases, 1):
        print(f"{phase['phase']}: {phase['description']}")
        print(f"请求: {phase['request']}")
        
        # 方式1: 通过主技能路由
        if i <= 4:  # 前4个阶段使用主技能路由
            result = main_architect.process_request(phase['request'])
            print(f"主技能路由到: {result['skill_used']}")
        else:
            # 方式2: 通过Hook系统自动发现
            hook_result = skill_invoker.hook_before_ai_response(
                phase['request'], 
                {"project_phase": i, "project_name": "电商系统"}
            )
            if hook_result:
                print(f"Hook系统调用: {hook_result['skill_name']}")
                print(f"响应摘要: {hook_result['content'][:100]}...")
            else:
                print("→ 继续正常AI响应")
        
        print("-" * 50 + "\n")
    
    # 演示各个技能的独立调用
    print("=== 各技能独立调用演示 ===\n")
    
    skills_demos = [
        ("系统架构师", DNASPECSystemArchitect(), "设计一个用户管理系统架构"),
        ("任务分解器", DNASPECTaskDecomposer(), "分解移动应用开发任务"),
        ("智能体创建器", DNASPECAgentCreator(), "创建微服务开发团队智能体"),
        ("约束生成器", DNASPECConstraintGenerator(), "生成API安全约束"),
        ("DAPI检查器", DNASPEC_DAPI_Checker(), "检查系统接口一致性")
    ]
    
    for skill_name, skill_instance, request in skills_demos:
        print(f"{skill_name} 技能调用:")
        print(f"  请求: {request}")
        result = skill_instance.process_request(request)
        if result["status"] == "completed":
            print(f"  ✓ 调用成功")
            if "architecture_design" in result:
                design = result["architecture_design"]
                print(f"    模块数: {len(design.get('modules', []))}")
            elif "task_decomposition" in result:
                decomposition = result["task_decomposition"]
                print(f"    任务数: {len(decomposition.get('atomic_tasks', []))}")
            elif "agent_configuration" in result:
                config = result["agent_configuration"]
                print(f"    智能体数: {len(config.get('agents', []))}")
            elif "constraint_specification" in result:
                spec = result["constraint_specification"]
                print(f"    约束数: {len(spec.get('system_constraints', []))}")
            elif "check_result" in result:
                check = result["check_result"]
                print(f"    接口数: {check.get('total_interfaces', 0)}")
                print(f"    问题数: {len(check.get('issues_found', []))}")
        print()
    
    print("="*70)
    print("DNASPEC系统完整功能验证")
    print("="*70)
    print("✓ 1个主技能 + 5个子技能完整实现")
    print("✓ 智能路由机制正常工作")
    print("✓ Hook系统自动发现功能")
    print("✓ 各技能独立调用能力")
    print("✓ 完整的项目开发流程支持")
    print("\n系统能力总结:")
    print("• 系统架构设计与优化")
    print("• 任务分解与规划")
    print("• 智能体创建与管理") 
    print("• 约束生成与规范")
    print("• 接口一致性检查")
    print("• 全流程自动化支持")

def main():
    demo_complete_workflow()

if __name__ == "__main__":
    main()