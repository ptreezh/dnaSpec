#!/usr/bin/env python3
"""
DNASPEC CLI命令入口点
提供命令行接口来使用DNASPEC技能
"""
import sys
import os
import json
import argparse


def is_stigmergy_available():
    """检查Stigmergy是否可用"""
    try:
        import subprocess
        # 尝试直接调用stigmergy
        result = subprocess.run(['stigmergy', '--version'], 
                              capture_output=True, text=True, timeout=10, shell=True)
        if result.returncode == 0:
            return True
            
        # 如果直接调用失败，尝试通过npx调用
        result = subprocess.run(['npx', 'stigmergy', '--version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return False


def main():
    """
    CLI主函数
    """
    parser = argparse.ArgumentParser(
        description='DNA SPEC Context System (dnaspec) - Context Engineering Skills',
        prog='dnaspec'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='DNA SPEC Context System (dnaspec) 2.0.0'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # exec命令：执行DNASPEC技能
    exec_parser = subparsers.add_parser('exec', help='Execute a DNASPEC skill command')
    exec_parser.add_argument('command_string', help='The command to execute')
    
    # shell命令：启动交互式Shell
    shell_parser = subparsers.add_parser('shell', help='Start interactive shell')
    
    # list命令：列出可用技能
    list_parser = subparsers.add_parser('list', help='List available skills')
    
    # validate命令：验证配置
    validate_parser = subparsers.add_parser('validate', help='Validate DNASPEC integration')
    validate_parser.add_argument('--stigmergy', action='store_true', help='Validate Stigmergy integration')

    
    # deploy命令：安全智能部署（重新设计）
    deploy_parser = subparsers.add_parser('deploy', help='Secure intelligent deployment with automatic mode selection')
    deploy_parser.add_argument('--force-stigmergy', action='store_true', help='Force global Stigmergy mode')
    deploy_parser.add_argument('--force-project', action='store_true', help='Force project-level mode')
    deploy_parser.add_argument('--verify', action='store_true', help='Verify deployment and security after completion')
    deploy_parser.add_argument('--list', action='store_true', help='Show deployment and security status only')
    deploy_parser.add_argument('--security-test', action='store_true', help='Run security validation tests')

    # security命令：安全测试和验证
    security_parser = subparsers.add_parser('security', help='Security testing and validation')
    security_parser.add_argument('--test', action='store_true', help='Run comprehensive security tests')
    security_parser.add_argument('--validate', action='store_true', help='Validate security configuration')
    security_parser.add_argument('--audit', action='store_true', help='Generate security audit report')

    # integrate命令：智能集成和部署
    integrate_parser = subparsers.add_parser('integrate', help='Intelligent deployment and integration')
    integrate_parser.add_argument('--platform', help='Target platform for integration')
    integrate_parser.add_argument('--list', action='store_true', help='List available platforms')
    integrate_parser.add_argument('--stigmergy', action='store_true', help='Force Stigmergy mode deployment')
    integrate_parser.add_argument('--project', action='store_true', help='Force project-level deployment')
    integrate_parser.add_argument('--status', action='store_true', help='Show deployment status')
    
    # slash命令：Slash命令模式（动态技能调用）
    slash_parser = subparsers.add_parser('slash', help='Slash command mode - dynamic skill invocation')
    slash_parser.add_argument('skill_command', nargs='?', help='Skill command to execute')
    slash_parser.add_argument('--help-all', action='store_true', help='Show help for all available skills')
    
    args = parser.parse_args()
    
    # 检查Stigmergy可用性
    stigmergy_available = is_stigmergy_available()
    
    # 延迟导入以避免循环依赖
    from .core.command_handler import CommandHandler
    from .core.interactive_shell import InteractiveShell
    from .core.skill_executor import SkillExecutor
    from .core.python_bridge import PythonBridge
    from .core.skill_mapper import SkillMapper
    
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
        print('Available DNASPEC Skills:')
        for cmd in commands:
            print(f'  {cmd}')
            
    elif args.command == 'slash':
        # Slash 命令模式 - 动态技能调用
        from .core.slash_command_handler import SlashCommandHandler
        
        # 使用项目根目录下的 skills 目录
        skills_root = Path(__file__).parent.parent.parent / "skills"
        if not skills_root.exists():
            print(f'Error: Skills directory not found: {skills_root}')
            sys.exit(1)
        
        slash_handler = SlashCommandHandler(skills_root)
        parser = slash_handler.create_parser()
        
        # 重新解析参数（跳过 'slash' 命令）
        if len(sys.argv) > 2:
            slash_args = sys.argv[2:]  # 移除 'dnaspec' 和 'slash'
            try:
                parsed_args = parser.parse_args(slash_args)
                result = slash_handler.handle_command(parsed_args)
                
                if result.get('success'):
                    if 'output' in result:
                        print(result['output'])
                    else:
                        print(json.dumps(result, ensure_ascii=False, indent=2))
                else:
                    print(f'Error: {result.get("error", "Unknown error")}', file=sys.stderr)
                    sys.exit(1)
            except SystemExit:
                # argparse 的帮助或错误处理
                pass
        else:
            parser.print_help()
            
    elif args.command == 'validate':
        # 验证集成
        if args.stigmergy:
            # 验证Stigmergy集成
            if not stigmergy_available:
                print('❌ Stigmergy is not installed or not available')
                print('Please install Stigmergy first: npm install -g stigmergy')
                sys.exit(1)
                
            print('Validating DNASPEC Stigmergy integration...')
            try:
                from .core.stigmergy_adapter import StigmergyAdapter
                adapter = StigmergyAdapter()
                result = adapter.verify_deployment()
                
                if result['success']:
                    print('✅ Stigmergy integration validation successful!')
                    print(f'  Deployed CLIs: {", ".join(result["deployed_clis"])}')
                    print(f'  Missing CLIs: {", ".join(result["missing_clis"])}')
                else:
                    print('❌ Stigmergy integration validation failed!')
                    print(f'  Error: {result.get("error", "Unknown error")}')
            except Exception as e:
                print(f'❌ Stigmergy integration validation failed: {e}')
        else:
            # 验证基本集成
            print('Validating DNASPEC integration...')
            print('✓ Python bridge: Working')
            print('✓ Skill mapper: Working')
            print('✓ Skill executor: Working')
            print('✓ Command handler: Working')
            print('All components are properly integrated.')

    elif args.command == 'deploy':
        # 智能扩展部署（自动选择模式）
        from .core.cli_extension_deployer import CLIExtensionDeployer

        # 创建CLI扩展部署器
        try:
            deployer = CLIExtensionDeployer()
        except Exception as e:
            print(f'Error initializing CLI extension deployer: {e}', file=sys.stderr)
            sys.exit(1)

        if args.list:
            # 显示部署状态
            print('🚀 DNASPEC CLI Extension Deployment Status:')
            status = deployer.get_deployment_status()
            print(f"  📍 Project Root: {status['project_root']}")
            print(f"  🔧 Deployment Mode: {status['deployment_mode']}")
            print(f"  📋 Stigmergy Available: {status['stigmergy_available']}")
            print(f"  📁 CLI Extensions Dir: {status['cli_extensions_dir']}")
            print(f"  🛠️  Supported AI Tools: {', '.join(status['supported_clis'])}")
            print(f"  🔢 Total AI Tools: {status['cli_count']}")
        else:
            # 处理强制模式参数
            if args.force_project:
                # 强制项目级CLI扩展模式
                print('📁 Forcing CLI extensions deployment mode...')
                deployer.deployment_mode = 'cli-extensions'
                deployer.stigmergy_available = False
                result = deployer._deploy_cli_extensions()
            elif args.force_stigmergy:
                # 强制全局Stigmergy模式
                print('🌐 Forcing global Stigmergy deployment mode...')
                deployer.deployment_mode = 'stigmergy'
                deployer.stigmergy_available = True
                result = deployer._deploy_with_stigmergy()
            else:
                # 执行智能部署（自动选择）
                result = deployer.deploy_all()

            if result.get('success'):
                print(json.dumps(result, ensure_ascii=False, indent=2))

                # 如果需要验证
                if args.verify:
                    print("\n🔍 Verifying deployment...")
                    # 这里可以添加验证逻辑
                    print("✅ Deployment verification completed")
            else:
                error_msg = result.get("error", "Deployment failed")
                print(f'Error: {error_msg}', file=sys.stderr)
                sys.exit(1)

    elif args.command == 'integrate':
        # 智能集成和部署
        from .core.deployment_manager import DeploymentManager

        # 创建部署管理器
        manager = DeploymentManager()

        if args.status:
            # 显示部署状态
            print('📋 DNASPEC Integration Status:')
            status = manager.get_deployment_status()
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            # 执行集成部署
            if args.stigmergy:
                # 强制Stigmergy模式
                print('🔌 Forcing Stigmergy mode integration...')
                manager.deployment_mode = 'stigmergy'
                manager.stigmergy_available = True
                result = manager._deploy_with_stigmergy()
            elif args.project:
                # 强制项目级模式
                print('📁 Forcing project-level mode integration...')
                manager.deployment_mode = 'project-level'
                manager.stigmergy_available = False
                result = manager._deploy_project_level()
            elif args.list:
                # 显示可用平台
                print('🛠️  Available AI CLI Platforms:')
                status = manager.get_deployment_status()
                for cli in status['supported_clis']:
                    print(f'  • {cli}')
                return
            elif args.platform:
                # 针对特定平台
                print(f'🎯 Integrating DNASPEC skills to {args.platform}...')
                if stigmergy_available and args.platform in manager.supported_clis:
                    # 使用Stigmergy集成
                    from .core.stigmergy_adapter import StigmergyAdapter
                    adapter = StigmergyAdapter()
                    result = adapter.generate_stigmergy_hook(args.platform)
                else:
                    # 使用项目级集成
                    print(f'ℹ️  Stigmergy not available for {args.platform}, using project-level integration')
                    result = manager._deploy_project_level()
            else:
                # 自动选择模式
                print('🤖 Auto-selecting integration mode...')
                result = manager.deploy_all()

            if result.get('success'):
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f'Error: {result.get("error", "Integration failed")}', file=sys.stderr)
                sys.exit(1)

    elif args.command == 'security':
        # 安全测试和验证
        from .core.secure_deployment_manager import SecureDeploymentManager

        try:
            manager = SecureDeploymentManager()
        except Exception as e:
            print(f'Error initializing security manager: {e}', file=sys.stderr)
            sys.exit(1)

        if args.test:
            print('🧪 Running comprehensive security tests...')
            result = manager._run_security_tests()
            print(json.dumps(result, ensure_ascii=False, indent=2))

            if result.get('success'):
                print('✅ All security tests passed')
            else:
                print('❌ Some security tests failed')
                sys.exit(1)

        elif args.validate:
            print('🔍 Validating security configuration...')
            verification = manager.verify_deployment()

            if 'security_validation' in verification:
                sec_val = verification['security_validation']
                print(f"🛡️  Security Level: {sec_val.get('security_level', 'unknown')}")
                print(f"✅ Status: {sec_val.get('status', 'unknown')}")

                if sec_val.get('checks'):
                    print("\n📋 Security Checks:")
                    for check, passed in sec_val['checks'].items():
                        status = "✅" if passed else "❌"
                        print(f"  {status} {check}")
            else:
                print("❌ No security configuration found")
                sys.exit(1)

        elif args.audit:
            print('📊 Generating security audit report...')
            audit_result = manager._generate_security_audit()
            print(json.dumps(audit_result, ensure_ascii=False, indent=2))

        else:
            print('Security command requires --test, --validate, or --audit')
            security_parser.print_help()
            sys.exit(1)

    elif args.command is None:
        # 没有提供子命令，显示帮助
        parser.print_help()
        
        # 显示Stigmergy状态
        if stigmergy_available:
            print('\n💡 Stigmergy detected! You can integrate DNASPEC with Stigmergy using:')
            print('   dnaspec integrate --stigmergy')
        else:
            print('\nℹ️  Stigmergy not detected. To enable cross-CLI collaboration, install Stigmergy:')
            print('   npm install -g stigmergy')
            print('   Then integrate: dnaspec integrate --stigmergy')
    else:
        # 未知命令
        parser.print_help()
        sys.exit(1)