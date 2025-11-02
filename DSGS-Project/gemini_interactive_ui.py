#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DSGS Gemini CLI 扩展 - 交互式用户界面
"""

import sys
import os
import time
from typing import Dict, Any, Optional

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gemini_hook_handler import get_hook_handler
from gemini_skills_core import get_skill_manager
from gemini_skill_executor import get_execution_engine

class DSGSInteractiveInterface:
    """DSGS交互式用户界面"""
    
    def __init__(self):
        self.hook_handler = get_hook_handler()
        self.skill_manager = get_skill_manager()
        self.execution_engine = get_execution_engine()
        self.is_running = False
        
    def display_welcome(self):
        """显示欢迎信息"""
        print("=" * 60)
        print("           DSGS Gemini CLI Extensions")
        print("        DSGS智能架构师系统交互界面")
        print("=" * 60)
        print()
        
        # 显示可用技能
        skills = self.skill_manager.list_skills()
        print(f"可用技能 ({len(skills)} 个):")
        for skill in skills:
            print(f"  • {skill.name} - {skill.description}")
        print()
        
        self.display_help()
    
    def display_help(self):
        """显示帮助信息"""
        print("使用说明:")
        print("  • 直接输入自然语言请求，系统将自动匹配并执行相应技能")
        print("  • 输入 'help' 或 'h' 查看帮助")
        print("  • 输入 'skills' 或 's' 查看可用技能")
        print("  • 输入 'stats' 查看执行统计")
        print("  • 输入 'debug' 切换调试模式")
        print("  • 输入 'quit' 或 'q' 退出程序")
        print()
    
    def display_skills(self):
        """显示可用技能"""
        skills = self.skill_manager.list_skills()
        print(f"\n可用技能 ({len(skills)} 个):")
        for i, skill in enumerate(skills, 1):
            print(f"  {i}. {skill.name}")
            print(f"     {skill.description}")
            print(f"     关键词: {', '.join(skill.keywords[:5])}{'...' if len(skill.keywords) > 5 else ''}")
        print()
    
    def display_stats(self):
        """显示执行统计"""
        stats = self.execution_engine.get_execution_stats()
        
        print(f"\n执行统计:")
        print(f"  总执行次数: {stats['total_executions']}")
        if stats['total_executions'] > 0:
            print(f"  成功次数: {stats['successful_executions']}")
            print(f"  失败次数: {stats['failed_executions']}")
            print(f"  成功率: {stats['success_rate']:.2%}")
            print(f"  平均执行时间: {stats['average_execution_time']:.3f}s")
        
        if 'skill_statistics' in stats:
            print(f"\n各技能执行情况:")
            for skill_name, skill_stats in stats['skill_statistics'].items():
                print(f"  {skill_name}:")
                print(f"    总执行: {skill_stats['total']}")
                print(f"    成功: {skill_stats['successful']}")
                print(f"    平均耗时: {skill_stats['total_time'] / skill_stats['total']:.3f}s")
        print()
    
    def toggle_debug(self):
        """切换调试模式"""
        current_debug = self.hook_handler.debug_mode
        self.hook_handler.toggle_debug()
        new_debug = self.hook_handler.debug_mode
        
        print(f"\n调试模式: {'开启' if new_debug else '关闭'}")
        if new_debug:
            self.execution_engine.enable_debug()
        else:
            self.execution_engine.disable_debug()
        print()
    
    def process_user_input(self, user_input: str) -> bool:
        """处理用户输入"""
        user_input = user_input.strip()
        
        if not user_input:
            return True  # 继续运行
        
        # 处理命令
        lower_input = user_input.lower()
        
        if lower_input in ['quit', 'q', 'exit', '退出']:
            return False  # 退出
        
        elif lower_input in ['help', 'h', '帮助']:
            self.display_help()
            return True
        
        elif lower_input in ['skills', 's', '技能']:
            self.display_skills()
            return True
        
        elif lower_input in ['stats', '统计']:
            self.display_stats()
            return True
        
        elif lower_input in ['debug', '调试']:
            self.toggle_debug()
            return True
        
        elif lower_input in ['clear', 'cls', '清屏']:
            os.system('cls' if os.name == 'nt' else 'clear')
            return True
        
        # 处理技能请求
        else:
            print(f"\n处理请求: {user_input}")
            print("-" * 40)
            
            # 使用Hook处理器处理请求
            start_time = time.time()
            result = self.hook_handler.process_hook(user_input)
            processing_time = time.time() - start_time
            
            if result:
                print("处理结果:")
                print(result)
                
                # 显示处理时间
                print(f"\n处理耗时: {processing_time:.3f}秒")
            else:
                print("系统: 未匹配到合适的技能，将由原始Gemini CLI处理")
                print("提示: 您可以尝试更具体的描述来激活相应的技能")
            
            print("-" * 40)
            print()
            return True
    
    def run(self):
        """运行交互式界面"""
        self.is_running = True
        self.display_welcome()
        
        print("开始交互 (输入 'help' 查看帮助, 'quit' 退出):")
        print()
        
        while self.is_running:
            try:
                user_input = input("DSGS> ").strip()
                if not self.process_user_input(user_input):
                    break
            except (KeyboardInterrupt, EOFError):
                print("\n\n再见!")
                break
        
        print("\n感谢使用 DSGS Gemini CLI Extensions!")

def main():
    """主函数"""
    interface = DSGSInteractiveInterface()
    
    if len(sys.argv) > 1 and sys.argv[1] in ['--demo', '-d']:
        # 演示模式
        print("DSGS Gemini CLI Extensions 演示模式")
        print("运行一些预设示例...")
        print()
        
        # 运行一些示例
        examples = [
            "设计微服务系统架构",
            "创建项目管理智能体",
            "检查API接口一致性"
        ]
        
        hook_handler = get_hook_handler()
        for example in examples:
            print(f"示例: {example}")
            result = hook_handler.process_hook(example)
            if result:
                print(f"结果: {result[:200]}...")
            else:
                print("未匹配到技能")
            print()
        
        print("演示完成!")
        
    else:
        # 交互模式
        interface.run()

if __name__ == "__main__":
    main()