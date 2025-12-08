# DNASPEC使用示例脚本

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, 'src')

def demo_dnaspec_usage():
    """演示DNASPEC系统的使用方法"""
    print("=== DNASPEC智能架构师系统使用演示 ===\n")
    
    # 导入主技能
    from dnaspec_architect import DNASPECArchitect
    
    # 创建主技能实例
    architect = DNASPECArchitect()
    
    print("✓ DNASPEC主技能加载成功")
    print(f"技能名称: {architect.name}")
    print(f"技能描述: {architect.description}")
    print(f"支持的子技能: {architect.subskills}")
    print("\n" + "="*50 + "\n")
    
    # 演示不同类型的请求处理
    demo_requests = [
        {
            "request": "Design architecture for a modern web application with REST API backend",
            "description": "系统架构设计请求"
        },
        {
            "request": "Decompose tasks for developing a mobile e-commerce application",
            "description": "任务分解请求"
        },
        {
            "request": "Create agents for implementing a microservices-based platform",
            "description": "智能体创建请求"
        },
        {
            "request": "Generate constraints for API design and data security requirements",
            "description": "约束生成请求"
        }
    ]
    
    for i, demo in enumerate(demo_requests, 1):
        print(f"演示 {i}: {demo['description']}")
        print(f"请求: {demo['request']}")
        
        # 处理请求
        result = architect.process_request(demo['request'])
        
        # 显示结果
        print(f"处理状态: {result['status']}")
        print(f"使用的技能: {result['skill_used']}")
        print(f"时间戳: {result['timestamp']}")
        
        print("-" * 30 + "\n")
    
    print("=== 演示完成 ===")
    print("DNASPEC智能架构师系统可以:")
    print("1. 根据自然语言请求自动选择合适的子技能")
    print("2. 处理复杂的软件架构设计任务")
    print("3. 提供结构化的输出结果")
    print("4. 支持多种类型的项目需求")
    
    print("\n=== 子技能独立使用演示 ===")
    
    # 演示子技能的独立使用
    from dnaspec_system_architect import DNASPECSystemArchitect
    from dnaspec_task_decomposer import DNASPECTaskDecomposer
    from dnaspec_agent_creator import DNASPECAgentCreator
    from dnaspec_constraint_generator import DNASPECConstraintGenerator
    
    # 系统架构师技能演示
    system_architect = DNASPECSystemArchitect()
    result1 = system_architect.process_request("Design a web application architecture")
    if result1["status"] == "completed":
        design = result1["architecture_design"]
        print(f"✓ 系统架构师技能: 生成了 {len(design.get('modules', []))} 个模块")
    
    # 任务分解器技能演示
    task_decomposer = DNASPECTaskDecomposer()
    result2 = task_decomposer.process_request("Decompose tasks for mobile app development")
    if result2["status"] == "completed":
        decomposition = result2["task_decomposition"]
        print(f"✓ 任务分解器技能: 生成了 {len(decomposition.get('atomic_tasks', []))} 个原子任务")
    
    # 智能体创建器技能演示
    agent_creator = DNASPECAgentCreator()
    result3 = agent_creator.process_request("Create agents for microservices system")
    if result3["status"] == "completed":
        configuration = result3["agent_configuration"]
        print(f"✓ 智能体创建器技能: 创建了 {len(configuration.get('agents', []))} 个智能体")
    
    # 约束生成器技能演示
    constraint_generator = DNASPECConstraintGenerator()
    result4 = constraint_generator.process_request("Generate constraints for API design")
    if result4["status"] == "completed":
        specification = result4["constraint_specification"]
        print(f"✓ 约束生成器技能: 生成了 {len(specification.get('system_constraints', []))} 个系统约束")

if __name__ == "__main__":
    demo_dnaspec_usage()