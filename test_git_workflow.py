#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('.')

def test_git_workflow_design():
    """测试Git工作流设计功能"""
    try:
        from check_skills import test_skill
        
        # 测试参数
        test_params = {
            'team_size': 'medium',
            'project_type': 'web_application',
            'deployment_frequency': 'weekly',
            'experience_level': 'mixed'
        }
        
        print("=== Git工作流设计测试 ===")
        print(f"测试参数: {test_params}")
        print("-" * 50)
        
        # 执行测试
        test_result = test_skill('git-operations', 'design_team_workflow', test_params)
        
        # 输出结果
        print(f"测试状态: {test_result.get('status', '未知')}")
        print(f"响应内容: {test_result.get('response', '无响应')}")
        print(f"执行时间: {test_result.get('execution_time', 0):.2f}秒")
        print(f"错误信息: {test_result.get('error', '无错误')}")
        
        return test_result
        
    except Exception as e:
        print(f"测试执行失败: {str(e)}")
        return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    result = test_git_workflow_design()