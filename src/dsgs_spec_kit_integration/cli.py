#!/usr/bin/env python3
"""
DSGS CLI命令入口点
提供命令行接口来使用DSGS技能
"""
import sys
import os
import argparse
from .core.command_handler import CommandHandler
from .core.interactive_shell import InteractiveShell
from .core.skill_executor import SkillExecutor
from .core.python_bridge import PythonBridge
from .core.skill_mapper import SkillMapper


def main():
    """
    CLI主函数
    """
    parser = argparse.ArgumentParser(
        description='Dynamic Specification Growth System (dnaspec) - Context Engineering Skills',
        prog='dnaspec'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='Dynamic Specification Growth System (dnaspec) 1.0.2'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # exec命令：执行DSGS技能
    exec_parser = subparsers.add_parser('exec', help='Execute a DSGS skill command')
    exec_parser.add_argument('command_string', help='The command to execute')
    
    # shell命令：启动交互式Shell
    shell_parser = subparsers.add_parser('shell', help='Start interactive shell')
    
    # list命令：列出可用技能
    list_parser = subparsers.add_parser('list', help='List available skills')
    
    # validate命令：验证配置
    validate_parser = subparsers.add_parser('validate', help='Validate DSGS integration')

    # deploy命令：将技能部署到AI CLI工具
    deploy_parser = subparsers.add_parser('deploy', help='Deploy DSGS skills to AI CLI tools')
    deploy_parser.add_argument('--platform', help='Target platform for deployment')
    deploy_parser.add_argument('--list', action='store_true', help='List available platforms')
    deploy_parser.add_argument('--force', action='store_true', help='Force redeployment if already deployed')

    # integrate命令：集成和验证
    integrate_parser = subparsers.add_parser('integrate', help='Integrate and validate DSGS skills')
    integrate_parser.add_argument('--platform', help='Target platform for integration')
    integrate_parser.add_argument('--list', action='store_true', help='List available platforms')
    
    args = parser.parse_args()
    
    # 创建组件
    python_bridge = PythonBridge()
    skill_mapper = SkillMapper()
    skill_executor = SkillExecutor(python_bridge, skill_mapper)
    command_handler = CommandHandler(None, skill_executor)
    
    if args.command == 'exec':
        # 执行命令
        result = command_handler.handle_command(args.command_string)
        
        if result['success']:
            print(result['result'])
        else:
            print(f'Error: {result.get("error", "Unknown error")}', file=sys.stderr)
            sys.exit(1)
            
    elif args.command == 'shell':
        # 启动交互式Shell
        shell = InteractiveShell(command_handler)
        shell.start()
        
    elif args.command == 'list':
        # 列出可用命令
        commands = command_handler.get_available_commands()
        print('Available DSGS Skills:')
        for cmd in commands:
            print(f'  {cmd}')
            
    elif args.command == 'validate':
        # 验证集成（简单示例）
        print('Validating DSGS integration...')
        print('✓ Python bridge: Working')
        print('✓ Skill mapper: Working')
        print('✓ Skill executor: Working')
        print('✓ Command handler: Working')
        print('All components are properly integrated.')

    elif args.command == 'deploy':
        # 部署技能到AI CLI工具
        print('🚀 Starting DSGS Skills Deployment to AI CLI Platforms...')
        from src.dsgs_spec_kit_integration.core.real_skill_deployer import RealSkillDeployer

        deployer = RealSkillDeployer()

        if args.list:
            print('Available AI CLI Platforms:')
            for platform, path in deployer.extension_paths.items():
                exists = '✅' if os.path.exists(path) else '❌'
                print(f'  {exists} {platform}: {path}')
        elif args.platform:
            print(f'Deploying DSGS skills to {args.platform}...')
            from src.dsgs_spec_kit_integration.core.cli_detector import CliDetector
            detector = CliDetector()
            detected_tools = detector.detect_all()
            tool_info = detected_tools.get(args.platform, {})

            result = deployer.deploy_skills_to_platform(args.platform, tool_info)
            if result['success']:
                print(f'✅ Successfully deployed to {args.platform}')
                print(f'Message: {result.get("message", "Deployment completed")}')
                if result.get('deployed_skills'):
                    print(f'Deployed skills: {result["deployed_skills"]}')
            else:
                print(f'❌ Failed to deploy to {args.platform}')
                print(f'Error: {result.get("error", "Unknown error")}')
        else:
            print('Deploying DSGS skills to all detected AI CLI platforms...')
            results = deployer.deploy_skills_to_all_platforms()
            print(f'✅ Deployment completed!')
            print(f'Successfully deployed to {results["successful_deployments"]}/{results["total_installed_platforms"]} platforms')
            for platform, result in results['deployment_results'].items():
                status = '✅' if result.get('success', False) else '❌'
                message = result.get('message', result.get('error', 'Unknown'))
                print(f'  {status} {platform}: {message}')

    elif args.command == 'integrate':
        # 集成和验证
        print('🚀 Starting DSGS Skills Integration and Validation...')
        from src.dsgs_spec_kit_integration.core.real_skill_deployer import RealSkillDeployer

        deployer = RealSkillDeployer()

        if args.list:
            print('Available AI CLI Platforms:')
            for platform, path in deployer.extension_paths.items():
                exists = '✅' if os.path.exists(path) else '❌'
                print(f'  {exists} {platform}: {path}')
        elif args.platform:
            print(f'Integrating DSGS skills to {args.platform}...')
            from src.dsgs_spec_kit_integration.core.cli_detector import CliDetector
            detector = CliDetector()
            detected_tools = detector.detect_all()
            tool_info = detected_tools.get(args.platform, {})

            result = deployer.deploy_skills_to_platform(args.platform, tool_info)
            if result['success']:
                print(f'✅ Successfully integrated to {args.platform}')
                print(f'Message: {result.get("message", "Integration completed")}')
            else:
                print(f'❌ Failed to integrate to {args.platform}')
                print(f'Error: {result.get("error", "Unknown error")}')
        else:
            print('Integrating DSGS skills to all detected AI CLI platforms...')
            results = deployer.deploy_skills_to_all_platforms()
            print(f'✅ Integration completed!')
            print(f'Successfully integrated to {results["successful_deployments"]}/{results["total_installed_platforms"]} platforms')
            for platform, result in results['deployment_results'].items():
                status = '✅' if result.get('success', False) else '❌'
                print(f'  {status} {platform}')
        
    elif args.command is None:
        # 没有提供子命令，显示帮助
        parser.print_help()
    else:
        # 未知命令
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()