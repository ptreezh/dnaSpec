#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini CLI Hook处理器
用于拦截用户请求并智能调用DNASPEC技能
"""

import sys
import os
import json
import time
from typing import Dict, Any, Optional

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gemini_skills_core import get_skill_manager, SkillResult
from gemini_intelligent_matcher import get_intelligent_matcher
from gemini_skill_executor import get_execution_engine

class GeminiHookHandler:
    """Gemini CLI Hook处理器"""
    
    def __init__(self):
        self.skill_manager = get_skill_manager()
        self.intelligent_matcher = get_intelligent_matcher()
        self.hook_enabled = True
        self.debug_mode = False
    
    def process_hook(self, user_input: str) -> Optional[str]:
        """处理Hook，返回技能执行结果或None（表示不处理）"""
        if not self.hook_enabled:
            return None
        
        if self.debug_mode:
            print(f"[DEBUG] Hook接收到用户输入: {user_input}")
        
        # 使用智能匹配器找到最合适的技能
        match_result = self.intelligent_matcher.match_skill_intelligently(user_input)
        
        if match_result and match_result.confidence > 0.2:  # 降低阈值以提高匹配率
            if self.debug_mode:
                print(f"[DEBUG] 智能匹配成功: {match_result.skill_info.name} (置信度: {match_result.confidence:.3f})")
            
            # 执行匹配到的技能
            skill_result = self._execute_matched_skill(match_result.skill_info.name, user_input)
            
            if skill_result and skill_result.status.name != 'ERROR':
                return self._format_skill_result(skill_result)
            else:
                if self.debug_mode and skill_result:
                    print(f"[DEBUG] 技能执行失败: {skill_result.error_message if skill_result else '未知错误'}")
        else:
            if self.debug_mode and match_result:
                print(f"[DEBUG] 智能匹配失败，置信度过低: {match_result.confidence if match_result else 0:.3f}")
            elif self.debug_mode:
                print("[DEBUG] 未找到匹配的技能")
        
        return None  # 表示不处理此请求，让原始Gemini CLI处理
    
    def _execute_matched_skill(self, skill_name: str, user_input: str) -> Optional[SkillResult]:
        """执行匹配到的技能"""
        try:
            # 使用执行引擎来执行技能
            execution_engine = get_execution_engine()
            
            context = {
                'user_input': user_input,
                'timestamp': time.time(),
                'source': 'gemini_cli_hook'
            }
            
            result = execution_engine.execute_skill(skill_name, user_input, context)
            return result
                
        except Exception as e:
            if self.debug_mode:
                print(f"[DEBUG] 技能执行异常: {str(e)}")
            return None
    
    def _execute_generic_skill(self, skill_name: str, user_input: str) -> SkillResult:
        """执行通用技能（当具体技能实例不存在时）"""
        start_time = time.time()
        
        # 使用执行引擎执行技能
        execution_engine = get_execution_engine()
        context = {
            'user_input': user_input,
            'timestamp': time.time(),
            'source': 'gemini_cli_hook_generic'
        }
        
        return execution_engine.execute_skill(skill_name, user_input, context)
    
    
    
    
    
    
    
    
    
    
    
    
    
    def _format_skill_result(self, skill_result: SkillResult) -> str:
        """格式化技能执行结果"""
        if skill_result.status.name == 'ERROR':
            return f"[DNASPEC技能执行错误] {skill_result.error_message}"
        
        result = skill_result.result
        
        if isinstance(result, dict):
            if 'error' in result:
                return f"[DNASPEC技能错误] {result['error']}"
            
            # 格式化输出
            formatted_output = f"[DNASPEC技能执行结果 - {skill_result.skill_name}]\n"
            
            if 'message' in result:
                formatted_output += f"{result['message']}\n"
            
            if 'suggestions' in result and result['suggestions']:
                formatted_output += "\n建议:\n"
                for suggestion in result['suggestions']:
                    formatted_output += f"• {suggestion}\n"
            
            if 'agent_configuration' in result:
                formatted_output += "\n智能体配置:\n"
                agents = result['agent_configuration'].get('agents', [])
                for agent in agents[:3]:  # 只显示前3个智能体
                    formatted_output += f"• {agent.get('name', 'Unknown')} - {', '.join(agent.get('capabilities', []))}\n"
            
            if 'modularization_result' in result:
                formatted_output += "\n模块化分析:\n"
                maturity_summary = result['modularization_result'].get('summary', {})
                formatted_output += f"成熟度: {maturity_summary.get('compliance_rate', 0):.1f}%\n"
            
            if 'check_result' in result:
                formatted_output += "\n一致性检查:\n"
                check_summary = result['check_result'].get('summary', {})
                formatted_output += f"问题数量: {check_summary.get('total_issues', 0)}\n"
            
            return formatted_output.strip()
        
        return f"[DNASPEC技能结果] {str(result)}"
    
    def enable_debug(self):
        """启用调试模式"""
        self.debug_mode = True
    
    def disable_debug(self):
        """禁用调试模式"""
        self.debug_mode = False
    
    def toggle_hook(self):
        """切换Hook状态"""
        self.hook_enabled = not self.hook_enabled
        return self.hook_enabled

# 全局Hook处理器实例
hook_handler = GeminiHookHandler()

def get_hook_handler() -> GeminiHookHandler:
    """获取全局Hook处理器"""
    return hook_handler

def process_gemini_request(user_input: str) -> Optional[str]:
    """处理Gemini CLI请求的入口函数"""
    return hook_handler.process_hook(user_input)

if __name__ == "__main__":
    # 测试Hook处理器
    print("=== Gemini CLI Hook处理器测试 ===")
    
    test_inputs = [
        "创建一个项目管理智能体",
        "分解复杂的软件开发任务",
        "检查API接口一致性",
        "对系统进行模块化重构",
        "设计系统架构",
        "普通聊天内容，不需要技能处理",
        "生成智能体角色定义"
    ]
    
    hook_handler.enable_debug()
    
    for test_input in test_inputs:
        print(f"\n测试输入: '{test_input}'")
        result = process_gemini_request(test_input)
        if result:
            print(f"Hook处理结果: {result}")
        else:
            print("Hook未处理此请求，将由原始CLI处理")
