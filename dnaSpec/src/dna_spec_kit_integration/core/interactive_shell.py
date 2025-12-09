"""
交互式Shell模块
提供命令行交互界面
"""
import sys
from .command_handler import CommandHandler
from typing import Dict, Any


class InteractiveShell:
    """
    DNASPEC交互式Shell
    提供命令行交互界面
    """
    
    def __init__(self, command_handler: CommandHandler = None):
        """
        初始化交互式Shell
        
        Args:
            command_handler: 命令处理器实例
        """
        self.command_handler = command_handler or CommandHandler()
        self.running = False
    
    def start(self):
        """
        启动交互式Shell
        """
        print('DNASPEC spec.kit Integration Shell')
        print('Type "help" for available commands, "exit" to quit\n')
        
        self.running = True
        
        while self.running:
            try:
                # 显示提示符并读取用户输入
                command = input('DNASPEC> ').strip()
                
                if not command:
                    continue
                
                self.handle_line(command)
                
            except KeyboardInterrupt:
                print('\nReceived interrupt signal.')
                self.running = False
            except EOFError:
                print('\nReceived EOF signal.')
                self.running = False
        
        print('\nGoodbye!')
    
    def handle_line(self, line: str):
        """
        处理用户输入的一行命令
        
        Args:
            line: 用户输入的一行命令
        """
        line_lower = line.lower()
        
        if line_lower in ['exit', 'quit']:
            self.running = False
        elif line_lower == 'help':
            self.show_help()
        elif line_lower == 'list':
            self.list_skills()
        elif line_lower == 'status':
            self.show_status()
        else:
            # 尝试执行命令
            self.execute_command(line)
    
    def execute_command(self, command: str):
        """
        执行命令
        
        Args:
            command: 要执行的命令
        """
        try:
            result = self.command_handler.handle_command(command)
            
            if result['success']:
                print(f'Result: {result["result"]}')
            else:
                print(f'Error: {result.get("error", "Unknown error")}')
                
        except Exception as e:
            print(f'Execution error: {str(e)}')
    
    def show_help(self):
        """
        显示帮助信息
        """
        print('Available commands:')
        commands = self.command_handler.get_available_commands()
        for cmd in commands:
            print(f'  {cmd}')
        print('\nSystem commands:')
        print('  help - Show this help')
        print('  list - List available skills')
        print('  status - Show system status')
        print('  exit - Exit the shell')
    
    def list_skills(self):
        """
        列出可用技能
        """
        print('Available DNASPEC Skills:')
        commands = self.command_handler.get_available_commands()
        for cmd in commands:
            print(f'  {cmd}')
    
    def show_status(self):
        """
        显示系统状态
        """
        print('DNASPEC System Status:')
        print(f'  Command Handler: Initialized')
        print(f'  Available Skills: {len(self.command_handler.get_available_commands())}')
        print('  Status: OK')
    
    def is_running(self) -> bool:
        """
        检查Shell是否正在运行
        
        Returns:
            Shell是否正在运行
        """
        return self.running