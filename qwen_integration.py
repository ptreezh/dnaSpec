#!/usr/bin/env python3
"""
DNASPEC Qwen 集成部署脚本

此脚本用于将 DNASPEC 架构与 Qwen 系统集成，
通过 MCP (Model Context Protocol) 提供技能服务。
"""

import asyncio
import json
import os
from pathlib import Path

# 添加 src 目录到 Python 路径
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.mcp.mcp_server import MCPServer
from skill_adapter import execute_original_skill_as_tool


class DnaSpecQwenIntegration:
    """DNASPEC 与 Qwen 系统集成类"""
    
    def __init__(self):
        self.config = {
            'name': 'DNASPEC-Qwen-Integration',
            'version': '1.0.0',
            'capabilities': {
                'prompts': {
                    'get': {'available': True}
                },
                'transports': {
                    'pipe': True,
                    'stdio': True
                }
            }
        }
        self.mcp_server = MCPServer(self.config)
        self.initialized = False
    
    def setup_handlers(self):
        """设置 MCP 处理器"""
        # 上下文分析处理器
        async def context_analyze_handler(params):
            """上下文分析处理器"""
            context = params.get('context', params.get('input', ''))
            result = execute_original_skill_as_tool('context-analyzer', {'context': context})
            return result
        
        # 约束生成处理器
        async def constraint_generate_handler(params):
            """约束生成处理器"""
            requirement = params.get('requirement', params.get('input', ''))
            result = execute_original_skill_as_tool('constraint-generator', {'requirement': requirement})
            return result
        
        # 模块化处理器
        async def modulizer_handler(params):
            """模块化处理器"""
            system_desc = params.get('system_description', params.get('input', ''))
            result = execute_original_skill_as_tool('modulizer', {'system_description': system_desc})
            return result
        
        # 代码生成处理器
        async def code_generation_handler(params):
            """代码生成处理器"""
            requirement = params.get('requirement', params.get('input', ''))
            from src.agents.agent_manager import CodeGenerationAgent
            agent = CodeGenerationAgent('code-generation-agent')
            result = await agent.process({'requirement': requirement})
            return {'result': result}
        
        # 注册处理器
        self.mcp_server.register_handler('dnaspec/context-analyze', context_analyze_handler)
        self.mcp_server.register_handler('dnaspec/generate-constraints', constraint_generate_handler)
        self.mcp_server.register_handler('dnaspec/modulize', modulizer_handler)
        self.mcp_server.register_handler('dnaspec/generate-code', code_generation_handler)
    
    def initialize(self):
        """初始化集成"""
        self.mcp_server.initialize()
        self.setup_handlers()
        self.initialized = True
        print("DNASPEC Qwen 集成初始化完成")
        print("可用 MCP 方法:")
        for method in self.mcp_server.handlers.keys():
            print(f"  - {method}")
    
    def get_capabilities(self):
        """获取 MCP 服务器能力"""
        return self.mcp_server.get_capabilities()
    
    async def handle_request(self, request):
        """处理 MCP 请求"""
        if not self.initialized:
            self.initialize()
        return await self.mcp_server.handle_request(request)


async def main():
    """主函数 - 启动 DNASPEC Qwen 集成"""
    print("启动 DNASPEC Qwen 集成服务...")
    
    integration = DnaSpecQwenIntegration()
    integration.initialize()
    
    print("\nDNASPEC Qwen 集成服务已启动")
    print("功能:")
    print("- 通过 MCP 协议提供 DNASPEC 技能")
    print("- 支持上下文分析、约束生成、模块化等功能")
    print("- 与 Qwen 的 /mcp 命令兼容")
    
    print("\n在 Qwen 中使用方法:")
    print("1. 确保此服务正在运行")
    print("2. 在 Qwen 中使用 /mcp 命令:")
    print("   /mcp dnaspec/context-analyze --context 'your context here'")
    print("   /mcp dnaspec/generate-constraints --requirement 'your requirement here'")
    print("   /mcp dnaspec/modulize --system_description 'your system description here'")
    
    # 保持服务运行
    try:
        # 这里可以实现实际的服务器循环
        # 为了演示，我们简单地等待
        print("\n服务正在运行... 按 Ctrl+C 停止")
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n服务已停止")


if __name__ == "__main__":
    asyncio.run(main())