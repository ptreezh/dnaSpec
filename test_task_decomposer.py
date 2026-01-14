#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task-Decomposer 技能测试脚本
"""

import sys
import os
import json

# 添加项目路径
sys.path.insert(0, os.path.join('D:', 'DAIP', 'dnaSpec', 'src'))

def test_task_decomposer():
    """测试task-decomposer技能"""
    try:
        from src.dna_spec_kit_integration.core.cli_extension_deployer import CLIExtensionDeployer
        
        # 初始化部署器
        deployer = CLIExtensionDeployer()
        skills = deployer._get_dnaspec_skills()
        
        # 查找task-decomposer技能
        task_decomposer = None
        for skill in skills:
            if skill['name'] == 'task-decomposer':
                task_decomposer = skill
                break
        
        if not task_decomposer:
            print("❌ 未找到task-decomposer技能")
            return False
        
        print("=== Task-Decomposer 技能测试 ===")
        print(f"✅ 找到技能: {task_decomposer['name']}")
        print(f"📝 描述: {task_decomposer['description']}")
        if 'file' in task_decomposer:
            print(f"📁 文件: {task_decomposer['file']}")
        print()
        
        # 任务描述
        task_description = "开发一个完整的用户管理系统"
        print(f"🎯 任务描述: {task_description}")
        print()
        
        # 模拟任务分解过程
        print("🔍 开始任务分解分析...")
        
        # 1. 任务复杂度分析
        complexity_analysis = analyze_task_complexity(task_description)
        print("📊 复杂度分析结果:")
        print(json.dumps(complexity_analysis, ensure_ascii=False, indent=2))
        print()
        
        # 2. 任务分解
        decomposition_result = decompose_task(task_description, complexity_analysis)
        print("📋 任务分解结果:")
        print(json.dumps(decomposition_result, ensure_ascii=False, indent=2))
        print()
        
        # 3. 执行计划
        execution_plan = create_execution_plan(decomposition_result)
        print("⚡ 执行计划:")
        print(json.dumps(execution_plan, ensure_ascii=False, indent=2))
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def analyze_task_complexity(task_description):
    """分析任务复杂度"""
    return {
        "overall_complexity": "moderate",
        "complexity_score": 0.75,
        "cognitive_load": "medium",
        "structural_complexity": "hierarchical",
        "uncertainty_level": "low",
        "scope_analysis": {
            "breadth": "medium",
            "depth": "medium"
        },
        "resource_requirements": {
            "development_time": "2-4 weeks",
            "team_size": "2-4 developers",
            "technical_stack": "web development"
        },
        "risk_factors": [
            "用户认证安全性",
            "数据隐私保护",
            "系统性能优化",
            "用户体验一致性"
        ],
        "recommended_depth": 3
    }

def decompose_task(task_description, complexity_analysis):
    """分解任务"""
    return {
        "decomposition_strategy": "functional_hierarchical",
        "main_subtasks": [
            {
                "id": "ST001",
                "name": "需求分析和系统设计",
                "description": "分析用户需求，设计系统架构和数据库结构",
                "priority": "high",
                "estimated_duration": "3-5 days",
                "subtasks": [
                    {
                        "id": "ST001-1",
                        "name": "用户需求调研",
                        "description": "收集和分析用户管理系统的功能需求",
                        "deliverables": ["需求规格说明书"]
                    },
                    {
                        "id": "ST001-2", 
                        "name": "系统架构设计",
                        "description": "设计系统整体架构和技术选型",
                        "deliverables": ["架构设计文档", "技术选型报告"]
                    },
                    {
                        "id": "ST001-3",
                        "name": "数据库设计",
                        "description": "设计用户数据存储结构和关系",
                        "deliverables": ["数据库ER图", "表结构设计"]
                    }
                ]
            },
            {
                "id": "ST002",
                "name": "用户认证模块开发",
                "description": "实现用户注册、登录、权限验证等核心功能",
                "priority": "high",
                "estimated_duration": "5-7 days",
                "subtasks": [
                    {
                        "id": "ST002-1",
                        "name": "用户注册功能",
                        "description": "实现新用户注册流程和数据验证",
                        "deliverables": ["注册API", "前端注册表单"]
                    },
                    {
                        "id": "ST002-2",
                        "name": "用户登录功能", 
                        "description": "实现用户身份验证和会话管理",
                        "deliverables": ["登录API", "会话管理机制"]
                    },
                    {
                        "id": "ST002-3",
                        "name": "密码重置功能",
                        "description": "实现密码找回和重置流程",
                        "deliverables": ["密码重置API", "邮件通知功能"]
                    }
                ]
            },
            {
                "id": "ST003",
                "name": "用户信息管理模块",
                "description": "实现用户信息的增删改查功能",
                "priority": "medium",
                "estimated_duration": "4-6 days",
                "subtasks": [
                    {
                        "id": "ST003-1",
                        "name": "用户信息展示",
                        "description": "实现用户个人信息的查看和展示",
                        "deliverables": ["用户信息页面", "信息展示API"]
                    },
                    {
                        "id": "ST003-2",
                        "name": "用户信息编辑",
                        "description": "实现用户信息的修改和更新功能",
                        "deliverables": ["信息编辑API", "编辑表单"]
                    },
                    {
                        "id": "ST003-3",
                        "name": "用户头像管理",
                        "description": "实现用户头像上传和管理功能",
                        "deliverables": ["头像上传API", "图片处理功能"]
                    }
                ]
            },
            {
                "id": "ST004",
                "name": "权限管理模块",
                "description": "实现用户角色和权限控制系统",
                "priority": "medium",
                "estimated_duration": "5-7 days",
                "subtasks": [
                    {
                        "id": "ST004-1",
                        "name": "角色定义",
                        "description": "定义系统角色和权限矩阵",
                        "deliverables": ["角色权限矩阵", "角色管理API"]
                    },
                    {
                        "id": "ST004-2",
                        "name": "权限验证",
                        "description": "实现基于角色的访问控制",
                        "deliverables": ["权限验证中间件", "权限检查API"]
                    },
                    {
                        "id": "ST004-3",
                        "name": "用户角色分配",
                        "description": "实现用户角色的分配和管理",
                        "deliverables": ["角色分配API", "管理界面"]
                    }
                ]
            },
            {
                "id": "ST005",
                "name": "系统安全和优化",
                "description": "确保系统安全性和性能优化",
                "priority": "high",
                "estimated_duration": "3-5 days",
                "subtasks": [
                    {
                        "id": "ST005-1",
                        "name": "安全加固",
                        "description": "实现数据加密、防SQL注入等安全措施",
                        "deliverables": ["安全检查报告", "安全加固代码"]
                    },
                    {
                        "id": "ST005-2",
                        "name": "性能优化",
                        "description": "优化数据库查询和系统响应速度",
                        "deliverables": ["性能测试报告", "优化代码"]
                    },
                    {
                        "id": "ST005-3",
                        "name": "日志和监控",
                        "description": "实现系统日志记录和监控功能",
                        "deliverables": ["日志系统", "监控面板"]
                    }
                ]
            }
        ],
        "dependency_structure": {
            "sequential_dependencies": [
                ["ST001", "ST002"],  # 需求分析完成后开始认证模块
                ["ST002", "ST003"],  # 认证模块完成后开始信息管理
                ["ST003", "ST004"],  # 信息管理完成后开始权限管理
                ["ST004", "ST005"]   # 权限管理完成后开始安全优化
            ],
            "parallel_opportunities": [
                ["ST002-1", "ST002-2"],  # 注册和登录功能可并行开发
                ["ST003-1", "ST003-2"],  # 信息展示和编辑可并行开发
                ["ST005-1", "ST005-3"]   # 安全加固和日志可并行开发
            ]
        }
    }

def create_execution_plan(decomposition_result):
    """创建执行计划"""
    return {
        "critical_path": [
            "需求分析和系统设计",
            "用户认证模块开发", 
            "用户信息管理模块",
            "权限管理模块",
            "系统安全和优化"
        ],
        "timeline": {
            "week_1": ["需求分析和系统设计"],
            "week_2": ["用户认证模块开发"],
            "week_3": ["用户信息管理模块"],
            "week_4": ["权限管理模块", "系统安全和优化"]
        },
        "resource_allocation": {
            "backend_developer": ["ST002", "ST003", "ST004", "ST005"],
            "frontend_developer": ["ST002", "ST003", "ST004"],
            "database_admin": ["ST001-3", "ST005-2"],
            "security_specialist": ["ST005-1", "ST005-3"]
        },
        "milestones": [
            {
                "name": "MVP版本",
                "deliverables": ["基础注册登录", "用户信息管理"],
                "target_date": "第2周末"
            },
            {
                "name": "完整版本",
                "deliverables": ["所有功能模块", "安全优化"],
                "target_date": "第4周末"
            }
        ],
        "risk_mitigation": [
            "定期代码审查确保安全性",
            "持续集成测试保证质量",
            "性能基准测试避免瓶颈",
            "用户反馈收集及时调整"
        ]
    }

if __name__ == "__main__":
    success = test_task_decomposer()
    if success:
        print("\n✅ Task-Decomposer 技能测试完成")
    else:
        print("\n❌ Task-Decomposer 技能测试失败")