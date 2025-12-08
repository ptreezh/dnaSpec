#!/usr/bin/env python3
"""
DNASPEC技能部署器 - 独立的部署接口
用于在AI CLI工具中部署技能
"""
import sys
import os
import argparse
from typing import Dict, Any

# 添加项目路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

# 导入DNASPEC技能部署器
from src.dnaspec_spec_kit_integration.core.real_skill_deployer import RealSkillDeployer


def main():
    """主函数 - 部署器入口"""
    print("🚀 DNASPEC Skills Deployment System - 独立部署接口")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description='DNASPEC Skills Deployment System')
    parser.add_argument('--list', action='store_true', help='List available platforms')
    parser.add_argument('--platform', help='Specific platform to deploy to')
    parser.add_argument('--force', action='store_true', help='Force redeployment')

    args = parser.parse_args()

    try:
        deployer = RealSkillDeployer()
        
        if args.list:
            print('Available AI CLI Platforms:')
            for platform_name, path in deployer.extension_paths.items():
                exists = '✅' if os.path.exists(path) else '❌'
                print(f'  {exists} {platform_name}: {path}')
                
        elif args.platform:
            print(f'Integrating DNASPEC skills to {args.platform}...')
            from src.dnaspec_spec_kit_integration.core.cli_detector import CliDetector
            detector = CliDetector()
            detected_tools = detector.detect_all()
            tool_info = detected_tools.get(args.platform, {})
            
            result = deployer.deploy_skills_to_platform(args.platform, tool_info)
            if result['success']:
                print(f'✅ Successfully deployed to {args.platform}')
                print(f'Message: {result.get("message", "Deployment completed")}')
                if result.get('deployed_skills'):
                    print(f'Deployed: {result["deployed_skills"]}')
            else:
                print(f'❌ Failed to deploy to {args.platform}')
                print(f'Error: {result.get("error", "Unknown error")}')
                
        else:
            print('Deploying DNASPEC skills to all detected AI CLI platforms...')
            results = deployer.deploy_skills_to_all_platforms()
            print(f'✅ Deployment completed!')
            print(f'Successfully deployed to {results["successful_deployments"]}/{results["total_installed_platforms"]} platforms')
            for platform_name, result in results['deployment_results'].items():
                status = '✅' if result.get('success', False) else '❌'  
                message = result.get('message', result.get('error', 'Unknown'))
                print(f'  {status} {platform_name}: {message[:50]}...')

    except ImportError as e:
        print(f'❌ Failed to import deployment module: {e}')
        print('Deployment module not found in current environment')
        print('This may happen if the package is not properly installed')
        sys.exit(1)
    except Exception as e:
        print(f'❌ Deployment failed: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()