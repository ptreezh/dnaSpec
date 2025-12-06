#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI钩子系统 - 智能路由钩子实现
允许在CLI内进行自然语言路由
"""

import re
import subprocess
from typing import Dict, Any, Optional


class CLIRoutingHookInterface:
    """CLI路由钩子接口"""
    
    def extract_route_info(self, user_input: str) -> Optional[Dict[str, str]]:
        """
        提取路由信息
        返回: {'target_tool': str, 'remaining_input': str, 'original_input': str} 或 None
        """
        raise NotImplementedError
    
    def execute_remote_tool(self, target_tool: str, instruction: str) -> Dict[str, Any]:
        """执行远程工具"""
        raise NotImplementedError


class SmartRoutingHook(CLIRoutingHookInterface):
    """智能路由钩子实现"""
    
    def __init__(self, cli_name: str):
        self.cli_name = cli_name
        self.route_patterns = {
            'claude': [
                r'(?i)用claude\s*(?:帮我|帮我写|帮我翻译|帮我解释|写|翻译|解释|分析|优化)',
                r'(?i)让claude\s*(?:帮我|帮我写|帮我翻译|帮我解释|写|翻译|解释|分析|优化)',
                r'(?i)请claude\s*(?:帮忙|写|翻译|解释|分析|优化)'
            ],
            'gemini': [
                r'(?i)用gemini\s*(?:帮我|帮我写|帮我翻译|帮我解释|写|翻译|解释|分析|优化)',
                r'(?i)让gemini\s*(?:帮我|帮我写|帮我翻译|帮我解释|写|翻译|解释|分析|优化)',
                r'(?i)请gemini\s*(?:帮忙|写|翻译|解释|分析|优化)'
            ],
            'qwen': [
                r'(?i)用qwen\s*(?:帮我|帮我写|帮我翻译|帮我解释|写|翻译|解释|分析|优化)',
                r'(?i)让qwen\s*(?:帮我|帮我写|帮我翻译|帮我解释|写|翻译|解释|分析|优化)',
                r'(?i)请qwen\s*(?:帮忙|写|翻译|解释|分析|优化)'
            ],
            'kimi': [
                r'(?i)用kimi\s*(?:帮我|帮我写|帮我翻译|帮我解释|写|翻译|解释|分析|优化)',
                r'(?i)让kimi\s*(?:帮我|帮我写|帮我翻译|帮我解释|写|翻译|解释|分析|优化)',
                r'(?i)请kimi\s*(?:帮忙|写|翻译|解释|分析|优化)'
            ],
            'codebuddy': [
                r'(?i)用codebuddy\s*(?:帮我|帮我写代码|帮我分析|写|翻译|解释|分析|代码|优化)',
                r'(?i)让codebuddy\s*(?:帮我|帮我写代码|帮我分析|写|翻译|解释|分析|代码|优化)',
                r'(?i)请codebuddy\s*(?:帮忙|写代码|代码|分析|优化)'
            ],
            'copilot': [
                r'(?i)用copilot\s*(?:帮我|帮我写代码|帮我分析|写|翻译|解释|分析|代码|优化)',
                r'(?i)让copilot\s*(?:帮我|帮我写代码|帮我分析|写|翻译|解释|分析|代码|优化)',
                r'(?i)请copilot\s*(?:帮忙|写代码|代码|分析|优化)'
            ],
            'qoder': [
                r'(?i)用qoder\s*(?:帮我|帮我写代码|帮我分析|写|翻译|解释|分析|代码|优化)',
                r'(?i)让qoder\s*(?:帮我|帮我写代码|帮我分析|写|翻译|解释|分析|代码|优化)',
                r'(?i)请qoder\s*(?:帮忙|写代码|代码|分析|优化)'
            ],
            'iflow': [
                r'(?i)用iflow\s*(?:帮我|帮我写|帮我翻译|帮我解释|写|翻译|解释|分析|优化)',
                r'(?i)让iflow\s*(?:帮我|帮我写|帮我翻译|帮我解释|写|翻译|解释|分析|优化)',
                r'(?i)请iflow\s*(?:帮忙|写|翻译|解释|分析|优化)'
            ]
        }
        
        self.tool_commands = {
            'claude': 'claude',
            'gemini': 'gemini',
            'qwen': 'qwen',
            'kimi': 'kimi',
            'codebuddy': 'codebuddy',
            'copilot': 'gh copilot',
            'qoder': 'qoder',
            'iflow': 'iflow'
        }
    
    def extract_route_info(self, user_input: str) -> Optional[Dict[str, str]]:
        """
        从用户输入中提取路由信息
        """
        user_lower = user_input.lower()
        
        for target_tool, patterns in self.route_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, user_lower)
                if match:
                    # 提取剩余输入
                    remaining = re.sub(pattern, '', user_input, count=1, flags=re.IGNORECASE)
                    # 清理多余的前导词
                    remaining = re.sub(r'^(?:用|让|请|麻烦|帮我|帮我写|帮我翻译|帮我解释)\s*', '', remaining, flags=re.IGNORECASE).strip()
                    
                    return {
                        'target_tool': target_tool,
                        'remaining_input': remaining,
                        'original_input': user_input
                    }
        
        return None
    
    def execute_remote_tool(self, target_tool: str, instruction: str) -> Dict[str, Any]:
        """执行远程工具"""
        if target_tool not in self.tool_commands:
            return {
                'success': False,
                'error': f'工具不存在: {target_tool}',
                'target_tool': target_tool,
                'instruction': instruction
            }
        
        try:
            command_template = self.tool_commands[target_tool]
            
            if target_tool == 'copilot':
                # GitHub Copilot 特殊处理
                cmd = ['gh', 'copilot', 'advise', instruction or 'help']
            else:
                # 一般工具处理
                cmd_parts = command_template.split()
                cmd = cmd_parts + [instruction] if instruction else cmd_parts
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': cmd,
                'target_tool': target_tool,
                'instruction': instruction
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': '命令执行超时',
                'timeout': True,
                'target_tool': target_tool,
                'instruction': instruction
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'exception_type': type(e).__name__,
                'target_tool': target_tool,
                'instruction': instruction
            }


class HookRegistry:
    """钩子注册表"""
    
    def __init__(self):
        self.hooks = {}
        self.cli_specific_hooks = {}
    
    def register_cli_hook(self, cli_name: str, hook_instance: CLIRoutingHookInterface):
        """注册特定CLI的钩子"""
        if cli_name not in self.cli_specific_hooks:
            self.cli_specific_hooks[cli_name] = []
        self.cli_specific_hooks[cli_name].append(hook_instance)
    
    def process_input_for_cli(self, cli_name: str, user_input: str) -> Dict[str, Any]:
        """
        为特定CLI处理输入
        """
        # 首先检查CLI特定钩子
        if cli_name in self.cli_specific_hooks:
            for hook in self.cli_specific_hooks[cli_name]:
                route_info = hook.extract_route_info(user_input)
                if route_info:
                    # 发现路由意图，执行路由
                    result = hook.execute_remote_tool(
                        route_info['target_tool'],
                        route_info['remaining_input']
                    )
                    
                    return {
                        'should_intercept': True,
                        'route_target': route_info['target_tool'],
                        'processed_input': route_info['remaining_input'],
                        'execution_result': result,
                        'original_input': user_input,
                        'handled_by': 'cli_specific_hook'
                    }
        
        # 没有发现路由意图，返回原始处理指示
        return {
            'should_intercept': False,
            'original_input': user_input,
            'handled_by': 'none'
        }


# 全局钩子注册表
hook_registry = HookRegistry()