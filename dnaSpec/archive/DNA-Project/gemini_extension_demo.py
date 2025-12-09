#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNASPEC Gemini CLI Extensions 使用示例
"""

import sys
import os

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gemini_hook_handler import get_hook_handler

def main():
    """主函数"""
    print("=== DNASPEC Gemini CLI Extensions 使用示例 ===")
    print()
    
    # 创建Hook处理器
    hook_handler = get_hook_handler()
    hook_handler.enable_debug()  # 启用调试模式以查看详细信息
    
    # 示例请求
    examples = [
        "创建一个电商系统的智能体架构",
        "分解用户注册登录功能的开发任务",
        "检查用户服务API接口的一致性",
        "对订单处理模块进行成熟度评估",
        "设计微服务系统架构",
        "生成数据处理智能体的角色定义",
        "验证支付接口的参数匹配",
        "执行用户管理模块的封装操作",
        "分析订单处理流程的任务依赖"
    ]
    
    print("示例请求处理:")
    print("=" * 50)
    
    for i, example in enumerate(examples, 1):
        print(f"\n示例 {i}: {example}")
        print("-" * 30)
        
        # 处理请求
        result = hook_handler.process_hook(example)
        
        if result:
            print("处理结果:")
            # 限制输出长度以保持可读性
            if len(result) > 500:
                print(result[:500] + "...")
            else:
                print(result)
        else:
            print("未匹配到合适的技能，将由原始Gemini CLI处理")
    
    print("\n" + "=" * 50)
    print("示例演示完成!")
    print("\n在实际使用中，这些技能会自动集成到Gemini CLI中，")
    print("您只需在Gemini CLI中输入自然语言请求即可。")

if __name__ == "__main__":
    main()