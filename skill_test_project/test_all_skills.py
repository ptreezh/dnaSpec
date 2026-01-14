#!/usr/bin/env python3
"""
全技能测试脚本 - 测试13个专业AI技能的可用性和有效性
"""

import json
import os
import sys
import traceback
from datetime import datetime
from typing import Dict, List, Any

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SkillTester:
    def __init__(self):
        self.test_results = {}
        self.test_start_time = datetime.now()
        
        # 定义要测试的技能列表
        self.skills_to_test = [
            "architect",
            "simple-architect", 
            "system-architect",
            "context-analyzer",
            "context-optimizer",
            "cognitive-templater",
            "agent-creator",
            "task-decomposer",
            "constraint-generator",
            "modulizer",
            "api-checker",
            "cache-manager",
            "git-operations"
        ]
    
    def test_skill_with_task(self, skill_name: str, test_description: str, test_prompt: str) -> Dict[str, Any]:
        """测试单个技能"""
        print(f"\n=== 测试技能: {skill_name} ===")
        
        result = {
            "skill_name": skill_name,
            "test_description": test_description,
            "test_prompt": test_prompt,
            "success": False,
            "error": None,
            "response": None,
            "execution_time": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            start_time = datetime.now()
            
            # 使用task工具调用技能
            from task import task
            response = task(
                description=f"测试{skill_name}技能",
                prompt=test_prompt,
                subagent_type=skill_name,
                useContext=True
            )
            
            end_time = datetime.now()
            result["execution_time"] = (end_time - start_time).total_seconds()
            result["response"] = str(response)
            result["success"] = True
            
            print(f"✅ {skill_name} 测试成功")
            print(f"   执行时间: {result['execution_time']:.2f}秒")
            
        except Exception as e:
            result["error"] = str(e)
            result["traceback"] = traceback.format_exc()
            print(f"❌ {skill_name} 测试失败: {str(e)}")
        
        return result
    
    def run_all_tests(self):
        """运行所有技能测试"""
        print("开始全技能测试...")
        print(f"测试开始时间: {self.test_start_time}")
        
        # 为每个技能设计测试用例
        test_cases = {
            "architect": {
                "description": "基础系统架构设计测试",
                "prompt": "为一个中等规模的电商系统设计基础架构，包括用户管理、商品管理、订单管理和支付模块。请提供技术栈选择和基本架构图。"
            },
            "simple-architect": {
                "description": "简化架构设计测试", 
                "prompt": "为一个简单的博客系统设计轻量级架构，使用Node.js和MongoDB，提供基本的CRUD功能。"
            },
            "system-architect": {
                "description": "高级系统架构设计测试",
                "prompt": "为一个大型分布式电商平台设计高级架构，考虑高可用性、可扩展性、微服务架构和云原生部署。"
            },
            "context-analyzer": {
                "description": "上下文质量分析测试",
                "prompt": "分析以下开发上下文的质量：'我需要做一个用户登录功能，使用JWT认证，连接MySQL数据库，前端用React。' 请评估上下文的完整性和相关性。"
            },
            "context-optimizer": {
                "description": "上下文优化测试",
                "prompt": "优化以下开发需求描述：'做个网站'。请提供更具体、更完整的上下文信息。"
            },
            "cognitive-templater": {
                "description": "认知模板应用测试",
                "prompt": "识别以下问题的认知模式并应用相应模板：'如何设计一个高效的任务管理系统？'"
            },
            "agent-creator": {
                "description": "AI代理创建测试",
                "prompt": "创建一个专门处理数据清洗任务的AI代理，包括代理架构设计、能力配置和行为定义。"
            },
            "task-decomposer": {
                "description": "任务分解测试",
                "prompt": "将'开发一个完整的用户管理系统'这个复杂任务分解为具体的、可执行的子任务。"
            },
            "constraint-generator": {
                "description": "约束生成测试",
                "prompt": "为一个金融支付系统生成安全性约束条件，包括数据保护、交易验证和访问控制等方面的约束。"
            },
            "modulizer": {
                "description": "模块化设计测试",
                "prompt": "将一个单体电商应用进行模块化设计，定义模块边界、接口依赖和通信机制。"
            },
            "api-checker": {
                "description": "API接口检查测试",
                "prompt": "检查以下REST API设计的规范性：GET /api/users/{id} - 获取用户信息，POST /api/users - 创建用户。评估接口设计质量和改进建议。"
            },
            "cache-manager": {
                "description": "缓存管理测试",
                "prompt": "为高并发的商品查询系统设计缓存策略，包括缓存架构、失效机制和数据一致性保证。"
            },
            "git-operations": {
                "description": "Git操作管理测试",
                "prompt": "设计一个适合团队开发的Git工作流，包括分支策略、提交规范和协作流程。"
            }
        }
        
        # 执行每个技能的测试
        for skill_name in self.skills_to_test:
            if skill_name in test_cases:
                test_case = test_cases[skill_name]
                result = self.test_skill_with_task(
                    skill_name, 
                    test_case["description"], 
                    test_case["prompt"]
                )
                self.test_results[skill_name] = result
            else:
                print(f"⚠️  技能 {skill_name} 没有对应的测试用例")
        
        self.generate_report()
    
    def generate_report(self):
        """生成测试报告"""
        end_time = datetime.now()
        total_time = (end_time - self.test_start_time).total_seconds()
        
        # 统计结果
        successful_tests = sum(1 for result in self.test_results.values() if result["success"])
        failed_tests = len(self.test_results) - successful_tests
        
        report = {
            "test_summary": {
                "total_skills": len(self.skills_to_test),
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": f"{(successful_tests/len(self.skills_to_test)*100):.1f}%",
                "total_execution_time": f"{total_time:.2f}秒",
                "start_time": self.test_start_time.isoformat(),
                "end_time": end_time.isoformat()
            },
            "detailed_results": self.test_results
        }
        
        # 保存报告
        report_path = os.path.join(os.path.dirname(__file__), "skill_test_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 打印摘要
        print("\n" + "="*60)
        print("全技能测试报告")
        print("="*60)
        print(f"总技能数: {report['test_summary']['total_skills']}")
        print(f"成功测试: {report['test_summary']['successful_tests']}")
        print(f"失败测试: {report['test_summary']['failed_tests']}")
        print(f"成功率: {report['test_summary']['success_rate']}")
        print(f"总执行时间: {report['test_summary']['total_execution_time']}")
        print(f"报告已保存到: {report_path}")
        
        # 详细结果
        print("\n详细结果:")
        for skill_name, result in self.test_results.items():
            status = "✅ 成功" if result["success"] else "❌ 失败"
            time_info = f"{result['execution_time']:.2f}秒" if result["success"] else "N/A"
            print(f"  {skill_name}: {status} ({time_info})")
            if not result["success"]:
                print(f"    错误: {result['error']}")

if __name__ == "__main__":
    tester = SkillTester()
    tester.run_all_tests()