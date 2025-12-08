#!/usr/bin/env python3
"""
DSGS Skills Deployment CLI Interface
独立的部署命令行接口，避免导入问题
"""
import sys
import os
import argparse

# 添加项目路径到Python模块搜索路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
sys.path.insert(0, project_root)

from src.dsgs_spec_kit_integration.core.real_skill_deployer import RealSkillDeployer


def main():
    """
    独立的部署CLI主函数
    解决导入问题，直接执行部署功能
    """
    parser = argparse.ArgumentParser(description='DSGS Skills Deployment Interface')
    parser.add_argument('command', nargs='?', default='deploy', help='Command to execute')
    parser.add_argument('--platform', help='Target platform for deployment')
    parser.add_argument('--list', action='store_true', help='List available platforms')
    parser.add_argument('--force', action='store_true', help='Force redeployment if already deployed')
    
    args = parser.parse_args()
    
    # 修正参数名称映射
    if hasattr(args, 'list') and args.list:
        command = 'list'
    elif hasattr(args, 'command'):
        command = args.command
    else:
        command = 'deploy'
    
    print("🚀 DSGS Skills Deployment System - 独立部署接口")
    print("="*60)
    
    if command == 'list' or command == '--list':
        # 创建部署器实例并列出平台
        deployer = RealSkillDeployer()
        print('Available AI CLI Platforms:')
        for platform_name, path in deployer.extension_paths.items():
            exists = '✅' if os.path.exists(path) else '❌'
            print(f'  {exists} {platform_name}: {path}')
    elif command == 'deploy':
        # 执行部署
        deployer = RealSkillDeployer()
        
        if args.platform:
            print(f'Deploying DSGS skills to {args.platform}...')
            # 使用检测器获取平台信息
            from src.dsgs_spec_kit_integration.core.cli_detector import CliDetector
            detector = CliDetector()
            detected_tools = detector.detect_all()
            tool_info = detected_tools.get(args.platform, {})
            
            result = deployer.deploy_skills_to_platform(args.platform, tool_info)
            if result['success']:
                print(f'✅ Successfully deployed to {args.platform}')
                print(f'Message: {result.get("message", "Deployment completed")}')
            else:
                print(f'❌ Failed to deploy to {args.platform}')
                print(f'Error: {result.get("error", "Unknown error")}')
        else:
            print('Deploying DSGS skills to all detected AI CLI platforms...')
            results = deployer.deploy_skills_to_all_platforms()
            print(f'✅ Deployment completed!')
            print(f'Successfully deployed to {results["successful_deployments"]}/{results["total_installed_platforms"]} platforms')
            for platform_name, result in results['deployment_results'].items():
                status = '✅' if result.get('success', False) else '❌'
                message = result.get('message', result.get('error', 'Unknown'))
                print(f'  {status} {platform_name}: {message}')
    else:
        print(f"Unknown command: {command}. Available: 'deploy', 'list'")

if __name__ == "__main__":
    main()