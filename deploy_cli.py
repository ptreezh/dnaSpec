"""
DSGS Context Engineering Skills - 部署CLI工具
为AI CLI环境提供独立的部署功能
"""
import sys
import os
import platform
from typing import Dict, Any

# 确保模块路径正确
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
sys.path.insert(0, project_root)

def main():
    print("🚀 DSGS Skills Deployment System - 独立部署接口")
    print("=" * 60)
    
    # 确保在正确的环境中
    import argparse
    parser = argparse.ArgumentParser(description='DNASPEC Skills Deployment System')
    parser.add_argument('--list', action='store_true', help='List available platforms')
    parser.add_argument('--platform', help='Target platform for deployment')
    parser.add_argument('--force', action='store_true', help='Force redeployment')
    
    args = parser.parse_args()

    if args.list:
        print('Available AI CLI Platforms:')
        # 检测AI工具
        try:
            from src.dna_spec_kit_integration.core.cli_detector import CliDetector
            detector = CliDetector()
            results = detector.detect_all()

            for platform_name, result in results.items():
                status = "✅" if result.get('installed', False) else "❌"
                print(f"  {status} {platform_name}: {result.get('version', 'Not installed')}")
                
        except ImportError as e:
            print(f"❌ CLI Detector import failed: {e}")
            print("Available platforms: [Unable to detect - please check installation]")
    else:
        print('Deploying DSGS skills to all detected AI CLI platforms...')
        try:
            from src.dna_spec_kit_integration.core.real_skill_deployer import RealSkillDeployer
            deployer = RealSkillDeployer()
            results = deployer.install_skills_to_all_platforms()
            
            print(f"Deployment completed: {results['installed_count']}/{results['target_count']} platforms")
            
        except ImportError as e:
            print(f"❌ Deployment system import failed: {e}")
            print("This may be due to incorrect installation or module paths.")
            
            # 提供修复建议
            print("\\n💡 Suggested fix: Check module installation with:")
            print("   python -c \"import src.dna_spec_kit_integration.core.cli_detector\"")
            print("   If this fails, reinstall with: pip install -e .")

if __name__ == "__main__":
    main()