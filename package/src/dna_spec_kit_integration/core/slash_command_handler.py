#!/usr/bin/env python3
"""
DNASPEC Slash 命令处理器
处理技能作为 CLI 命令的调用
"""
import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
from .skill_command_mapper import SkillCommandMapper, SkillCommand


class SlashCommandHandler:
    """Slash 命令处理器"""
    
    def __init__(self, skills_root: Path):
        """
        初始化处理器
        
        Args:
            skills_root: 技能根目录
        """
        self.skills_root = Path(skills_root)
        self.mapper = SkillCommandMapper(self.skills_root)
        self.commands: Dict[str, SkillCommand] = {}
        self._load_commands()
    
    def _load_commands(self):
        """加载所有命令"""
        self.commands = self.mapper.scan_skills()
    
    def create_parser(self) -> argparse.ArgumentParser:
        """
        创建命令解析器
        
        Returns:
            参数解析器
        """
        parser = argparse.ArgumentParser(
            prog='dnaspec',
            description='DNASPEC Context Engineering Skills - Dual Deployment System',
            epilog='使用 "dnaspec <command> --help" 查看具体命令帮助'
        )
        
        parser.add_argument(
            '--version',
            action='version',
            version='DNASPEC Skills System 2.0.0'
        )
        
        # 创建子命令解析器
        subparsers = parser.add_subparsers(
            dest='command',
            help='可用技能命令',
            metavar='<command>'
        )
        
        # 为每个技能创建子命令
        for skill_name, command in self.commands.items():
            skill_parser = subparsers.add_parser(
                skill_name,
                help=command.description,
                aliases=command.aliases[1:]  # 除了第一个别名（技能名）
            )
            
            # 添加动态参数
            self._add_skill_arguments(skill_parser, command)
            
        # 添加特殊命令
        self._add_utility_commands(subparsers)
        
        return parser
    
    def _add_skill_arguments(self, parser: argparse.ArgumentParser, command: SkillCommand):
        """
        为技能添加参数
        
        Args:
            parser: 参数解析器
            command: 技能命令
        """
        # 添加通用参数
        parser.add_argument(
            '--input', '-i',
            help='输入内容',
            type=str
        )
        
        parser.add_argument(
            '--output', '-o',
            help='输出文件路径',
            type=str
        )
        
        parser.add_argument(
            '--format', '-f',
            choices=['json', 'yaml', 'text'],
            default='json',
            help='输出格式'
        )
        
        parser.add_argument(
            '--detail-level',
            choices=['basic', 'standard', 'detailed'],
            default='standard',
            help='详细程度'
        )
        
        parser.add_argument(
            '--context', '-c',
            help='上下文信息 (JSON 格式)',
            type=str
        )
        
        # 根据技能类型添加特定参数
        self._add_skill_specific_arguments(parser, command)
    
    def _add_skill_specific_arguments(self, parser: argparse.ArgumentParser, command: SkillCommand):
        """
        添加技能特定参数
        
        Args:
            parser: 参数解析器
            command: 技能命令
        """
        skill_name = command.name
        
        if skill_name == 'agent-creator':
            parser.add_argument(
                '--agent-description',
                required=True,
                help='代理描述'
            )
            parser.add_argument(
                '--capabilities',
                nargs='+',
                help='能力列表'
            )
            parser.add_argument(
                '--domain',
                help='专业领域'
            )
            parser.add_argument(
                '--personality',
                choices=['professional_precise', 'friendly_supportive', 'analytical_critical', 'creative_innovative', 'direct_efficient'],
                default='professional_precise',
                help='人格类型'
            )
            parser.add_argument(
                '--agent-type',
                choices=['domain_expert', 'task_specialist', 'role_assistant'],
                default='role_assistant',
                help='代理类型'
            )
            
        elif skill_name == 'context-analyzer':
            parser.add_argument(
                '--dimensions',
                nargs='+',
                choices=['clarity', 'relevance', 'completeness', 'consistency', 'efficiency'],
                default=['clarity', 'relevance', 'completeness'],
                help='分析维度'
            )
            parser.add_argument(
                '--benchmark',
                choices=['academic', 'business', 'technical'],
                default='technical',
                help='质量基准'
            )
            
        elif skill_name == 'context-optimizer':
            parser.add_argument(
                '--optimization-goals',
                nargs='+',
                choices=['clarity', 'completeness', 'precision', 'efficiency', 'consistency'],
                help='优化目标'
            )
            parser.add_argument(
                '--constraints',
                help='约束条件 (JSON 格式)'
            )
            
        elif skill_name == 'architect':
            parser.add_argument(
                '--requirements',
                required=True,
                help='系统需求描述'
            )
            parser.add_argument(
                '--architecture-type',
                choices=['microservice', 'layered', 'event_driven', 'domain_driven'],
                help='架构类型'
            )
            parser.add_argument(
                '--tech-stack',
                nargs='+',
                help='技术栈'
            )
            
        elif skill_name == 'task-decomposer':
            parser.add_argument(
                '--max-depth',
                type=int,
                default=3,
                help='最大分解深度'
            )
            parser.add_argument(
                '--isolation-level',
                choices=['low', 'medium', 'high'],
                default='medium',
                help='隔离级别'
            )
            
        elif skill_name == 'constraint-generator':
            parser.add_argument(
                '--requirements',
                required=True,
                help='系统需求'
            )
            parser.add_argument(
                '--change-request',
                help='变更请求'
            )
            parser.add_argument(
                '--constraint-type',
                choices=['security', 'performance', 'architecture', 'quality'],
                help='约束类型'
            )
    
    def _add_utility_commands(self, subparsers):
        """
        添加实用工具命令
        
        Args:
            subparsers: 子命令解析器
        """
        # 列出所有命令
        list_parser = subparsers.add_parser('list', help='列出所有可用技能')
        list_parser.add_argument(
            '--category',
            help='按分类过滤'
        )
        list_parser.add_argument(
            '--format',
            choices=['table', 'json', 'yaml'],
            default='table'
        )
        
        # 显示命令信息
        info_parser = subparsers.add_parser('info', help='显示技能详细信息')
        info_parser.add_argument(
            'skill_name',
            help='技能名称'
        )
        
        # 验证技能
        validate_parser = subparsers.add_parser('validate', help='验证技能配置')
        validate_parser.add_argument(
            'skill_name',
            nargs='?',
            help='技能名称（不指定则验证所有）'
        )
        
        # 生成文档
        docs_parser = subparsers.add_parser('docs', help='生成技能文档')
        docs_parser.add_argument(
            '--output', '-o',
            default='skills_documentation.md',
            help='输出文件路径'
        )
        docs_parser.add_argument(
            '--format',
            choices=['markdown', 'html'],
            default='markdown'
        )
        
        # 部署技能
        deploy_parser = subparsers.add_parser('deploy', help='部署技能到不同平台')
        deploy_parser.add_argument(
            '--mode',
            choices=['standard', 'cli', 'both'],
            default='both',
            help='部署模式'
        )
        deploy_parser.add_argument(
            '--target',
            help='目标平台'
        )
        
        # 搜索技能
        search_parser = subparsers.add_parser('search', help='搜索技能')
        search_parser.add_argument(
            'query',
            help='搜索关键词'
        )
        search_parser.add_argument(
            '--category',
            help='限制搜索分类'
        )
    
    def handle_command(self, args: argparse.Namespace) -> Dict[str, Any]:
        """
        处理命令
        
        Args:
            args: 解析后的参数
            
        Returns:
            处理结果
        """
        command = args.command
        
        if command is None:
            return self._show_help()
        
        # 处理实用命令
        if command == 'list':
            return self._handle_list(args)
        elif command == 'info':
            return self._handle_info(args)
        elif command == 'validate':
            return self._handle_validate(args)
        elif command == 'docs':
            return self._handle_docs(args)
        elif command == 'deploy':
            return self._handle_deploy(args)
        elif command == 'search':
            return self._handle_search(args)
        
        # 处理技能命令
        if command in self.commands:
            return self._handle_skill(command, args)
        else:
            return {
                'success': False,
                'error': f'Unknown command: {command}',
                'available_commands': list(self.commands.keys())
            }
    
    def _handle_skill(self, skill_name: str, args: argparse.Namespace) -> Dict[str, Any]:
        """
        处理技能调用
        
        Args:
            skill_name: 技能名称
            args: 参数
            
        Returns:
            执行结果
        """
        command = self.commands[skill_name]
        
        # 准备输入数据
        input_data = self._prepare_input_data(args)
        
        try:
            # 模拟技能执行（在实际实现中，这里会调用真实的技能）
            result = self._execute_skill_simulation(command, input_data)
            
            # 格式化输出
            output = self._format_output(result, args.format)
            
            # 保存到文件（如果指定）
            if args.output:
                self._save_output(output, args.output, args.format)
            
            return {
                'success': True,
                'skill': skill_name,
                'result': output,
                'metadata': {
                    'format': args.format,
                    'detail_level': args.detail_level,
                    'execution_time': 'N/A'  # 在真实实现中会记录
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'skill': skill_name,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def _prepare_input_data(self, args: argparse.Namespace) -> Dict[str, Any]:
        """
        准备输入数据
        
        Args:
            args: 解析后的参数
            
        Returns:
            输入数据字典
        """
        input_data = {
            'input': args.input or '',
            'detail_level': args.detail_level,
            'options': {}
        }
        
        # 添加上下文
        if args.context:
            try:
                input_data['context'] = json.loads(args.context)
            except json.JSONDecodeError:
                input_data['context'] = {'raw': args.context}
        
        # 添加技能特定参数
        skill_name = args.command
        if skill_name in self.commands:
            command = self.commands[skill_name]
            
            # 提取所有技能相关参数
            for param_name, param_info in command.parameters.items():
                if hasattr(args, param_name):
                    value = getattr(args, param_name)
                    if value is not None:
                        input_data['options'][param_name] = value
        
        return input_data
    
    def _execute_skill_simulation(self, command: SkillCommand, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        模拟技能执行（在实际实现中替换为真实调用）
        
        Args:
            command: 技能命令
            input_data: 输入数据
            
        Returns:
            模拟结果
        """
        # 这里是模拟实现，实际中会调用真实的技能
        return {
            'status': 'success',
            'skill_name': command.name,
            'input_summary': {
                'input_length': len(input_data.get('input', '')),
                'detail_level': input_data.get('detail_level'),
                'options_count': len(input_data.get('options', {}))
            },
            'output': f"技能 {command.name} 执行完成",
            'execution_metadata': {
                'skill_description': command.description,
                'category': command.category,
                'version': command.version
            }
        }
    
    def _format_output(self, result: Dict[str, Any], format_type: str) -> Any:
        """
        格式化输出
        
        Args:
            result: 执行结果
            format_type: 格式类型
            
        Returns:
            格式化后的输出
        """
        if format_type == 'json':
            return json.dumps(result, ensure_ascii=False, indent=2)
        elif format_type == 'yaml':
            try:
                import yaml
                return yaml.dump(result, allow_unicode=True, default_flow_style=False)
            except ImportError:
                return json.dumps(result, ensure_ascii=False, indent=2)
        else:  # text
            if isinstance(result, dict):
                if 'output' in result:
                    return result['output']
                else:
                    return json.dumps(result, ensure_ascii=False, indent=2)
            return str(result)
    
    def _save_output(self, output: Any, output_path: str, format_type: str):
        """
        保存输出到文件
        
        Args:
            output: 输出内容
            output_path: 输出路径
            format_type: 格式类型
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if isinstance(output, str):
            output_file.write_text(output, encoding='utf-8')
        else:
            output_file.write_text(str(output), encoding='utf-8')
    
    def _show_help(self) -> Dict[str, Any]:
        """显示帮助信息"""
        return {
            'success': True,
            'message': 'DNASPEC Skills System',
            'available_commands': list(self.commands.keys()),
            'usage': 'dnaspec <command> [options]'
        }
    
    def _handle_list(self, args: argparse.Namespace) -> Dict[str, Any]:
        """处理列表命令"""
        commands = self.mapper.list_commands(args.category)
        
        if args.format == 'json':
            return {
                'success': True,
                'commands': [cmd.__dict__ for cmd in commands],
                'total': len(commands)
            }
        elif args.format == 'yaml':
            try:
                import yaml
                return {
                    'success': True,
                    'commands': yaml.dump([cmd.__dict__ for cmd in commands], allow_unicode=True),
                    'total': len(commands)
                }
            except ImportError:
                return {
                    'success': True,
                    'commands': [cmd.__dict__ for cmd in commands],
                    'total': len(commands)
                }
        else:  # table
            output_lines = [
                "DNASPEC 可用技能:",
                "=" * 50,
                f"总计: {len(commands)} 个技能"
            ]
            
            for command in commands:
                output_lines.append(f"\n{command.name}")
                output_lines.append(f"  描述: {command.description}")
                output_lines.append(f"  分类: {command.category}")
                if command.aliases:
                    output_lines.append(f"  别名: {', '.join(command.aliases)}")
            
            return {
                'success': True,
                'output': '\n'.join(output_lines)
            }
    
    def _handle_info(self, args: argparse.Namespace) -> Dict[str, Any]:
        """处理信息命令"""
        skill_name = args.skill_name
        command = self.mapper.get_command(skill_name)
        
        if not command:
            return {
                'success': False,
                'error': f'Skill not found: {skill_name}',
                'available_skills': list(self.commands.keys())
            }
        
        info = {
            'success': True,
            'skill_info': {
                'name': command.name,
                'description': command.description,
                'category': command.category,
                'version': command.version,
                'aliases': command.aliases,
                'parameters': command.parameters,
                'examples': command.examples,
                'skill_path': str(command.skill_path)
            }
        }
        
        return info
    
    def _handle_validate(self, args: argparse.Namespace) -> Dict[str, Any]:
        """处理验证命令"""
        if args.skill_name:
            # 验证特定技能
            command = self.mapper.get_command(args.skill_name)
            if not command:
                return {
                    'success': False,
                    'error': f'Skill not found: {args.skill_name}'
                }
            
            validation_result = self._validate_skill(command)
            return {
                'success': validation_result['valid'],
                'skill': args.skill_name,
                'validation': validation_result
            }
        else:
            # 验证所有技能
            validation_results = {}
            for skill_name, command in self.commands.items():
                validation_results[skill_name] = self._validate_skill(command)
            
            valid_count = sum(1 for result in validation_results.values() if result['valid'])
            
            return {
                'success': True,
                'total_skills': len(self.commands),
                'valid_skills': valid_count,
                'invalid_skills': len(self.commands) - valid_count,
                'validation_results': validation_results
            }
    
    def _validate_skill(self, command: SkillCommand) -> Dict[str, Any]:
        """验证单个技能"""
        issues = []
        
        # 检查 SKILL.md 文件
        skill_file = command.skill_path / "SKILL.md"
        if not skill_file.exists():
            issues.append("Missing SKILL.md file")
        
        # 检查必需字段
        if not command.name:
            issues.append("Missing skill name")
        
        if not command.description:
            issues.append("Missing skill description")
        
        # 检查目录结构
        required_dirs = ['scripts', 'references', 'assets']
        for dir_name in required_dirs:
            dir_path = command.skill_path / dir_name
            if not dir_path.exists():
                issues.append(f"Missing required directory: {dir_name}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'score': max(0, 100 - len(issues) * 10)
        }
    
    def _handle_docs(self, args: argparse.Namespace) -> Dict[str, Any]:
        """处理文档命令"""
        from .skill_command_mapper import generate_usage_guide
        guide_path = Path(args.output)
        
        try:
            generate_usage_guide(self.mapper, guide_path)
            return {
                'success': True,
                'output_file': str(guide_path),
                'message': f'Documentation generated: {guide_path}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _handle_deploy(self, args: argparse.Namespace) -> Dict[str, Any]:
        """处理部署命令"""
        from .skill_command_mapper import create_dual_deployment_system
        
        if args.mode in ['standard', 'both']:
            # 标准化部署
            standard_success = self._deploy_standard()
            
        if args.mode in ['cli', 'both']:
            # CLI 部署
            cli_success = self._deploy_cli()
        
        return {
            'success': True,
            'deployment_mode': args.mode,
            'standard_deployment': standard_success if args.mode in ['standard', 'both'] else None,
            'cli_deployment': cli_success if args.mode in ['cli', 'both'] else None
        }
    
    def _deploy_standard(self) -> bool:
        """部署标准化技能"""
        try:
            # 创建 .claude/skills 目录
            claude_skills_dir = Path('.claude/skills')
            claude_skills_dir.mkdir(parents=True, exist_ok=True)
            
            # 复制技能文件
            import shutil
            for skill_name, command in self.commands.items():
                skill_src = command.skill_path
                skill_dst = claude_skills_dir / skill_name
                
                if skill_dst.exists():
                    shutil.rmtree(skill_dst)
                shutil.copytree(skill_src, skill_dst)
            
            return True
        except Exception:
            return False
    
    def _deploy_cli(self) -> bool:
        """部署 CLI 命令"""
        # 这里可以实现 CLI 命令的注册逻辑
        # 比如创建符号链接、更新 PATH 等
        return True
    
    def _handle_search(self, args: argparse.Namespace) -> Dict[str, Any]:
        """处理搜索命令"""
        query = args.query.lower()
        category = args.category
        
        matching_commands = []
        for skill_name, command in self.commands.items():
            if category and command.category != category:
                continue
            
            # 在名称、描述和别名中搜索
            search_text = f"{skill_name} {command.description} {' '.join(command.aliases)}".lower()
            if query in search_text:
                matching_commands.append(command)
        
        return {
            'success': True,
            'query': args.query,
            'category': category,
            'results': [cmd.__dict__ for cmd in matching_commands],
            'total_results': len(matching_commands)
        }


def main():
    """主函数 - CLI 入口点"""
    skills_root = Path("../skills")
    
    if not skills_root.exists():
        print(f"Error: Skills directory not found: {skills_root}")
        sys.exit(1)
    
    handler = SlashCommandHandler(skills_root)
    parser = handler.create_parser()
    
    args = parser.parse_args()
    result = handler.handle_command(args)
    
    # 输出结果
    if result.get('success'):
        if 'output' in result:
            print(result['output'])
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Error: {result.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()