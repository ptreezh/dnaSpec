"""
自动部署配置检查器
借鉴spec.kit实现方式，自动检查和配置部署环境
"""
import sys
import os
import subprocess
import shutil
import json
from typing import Dict, List, Optional, Any
from pathlib import Path

class DeploymentConfigChecker:
    """自动部署配置检查器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.config_file = self.project_root / "deployment_config.json"
        self.system_info = {}
        self.check_results = {}
    
    def check_system_environment(self) -> Dict[str, Any]:
        """检查系统环境"""
        print("🔍 检查系统环境...")
        
        # 检查Python版本
        python_version = sys.version_info
        python_ok = python_version.major >= 3 and python_version.minor >= 8
        self.system_info['python_version'] = f"{python_version.major}.{python_version.minor}.{python_version.micro}"
        self.system_info['python_ok'] = python_ok
        
        # 检查系统命令
        required_commands = ['git', 'python', 'pip']
        command_checks = {}
        for cmd in required_commands:
            cmd_path = shutil.which(cmd)
            command_checks[cmd] = {
                'available': cmd_path is not None,
                'path': cmd_path
            }
        
        self.system_info['commands'] = command_checks
        
        # 检查操作系统
        import platform
        self.system_info['os'] = {
            'system': platform.system(),
            'release': platform.release(),
            'machine': platform.machine()
        }
        
        print(f"  Python版本: {self.system_info['python_version']} ({'✅' if python_ok else '❌'})")
        print(f"  操作系统: {self.system_info['os']['system']} {self.system_info['os']['release']}")
        
        for cmd, info in command_checks.items():
            status = '✅' if info['available'] else '❌'
            print(f"  {cmd}: {status} ({info['path'] or '未找到'})")
        
        return self.system_info
    
    def check_project_dependencies(self) -> Dict[str, Any]:
        """检查项目依赖"""
        print("\n📦 检查项目依赖...")
        
        # 检查项目配置文件
        pyproject_file = self.project_root / "pyproject.toml"
        has_pyproject = pyproject_file.exists()
        print(f"  pyproject.toml: {'✅' if has_pyproject else '❌'}")
        
        if not has_pyproject:
            self.check_results['dependencies'] = {'error': '缺少pyproject.toml文件'}
            return self.check_results['dependencies']
        
        # 检查已安装的依赖
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list"],
                capture_output=True, text=True, cwd=self.project_root
            )
            installed_packages = result.stdout.lower()
            
            # 检查必需依赖
            required_packages = ["pyyaml", "requests"]
            missing_packages = []
            
            for package in required_packages:
                if package.lower() in installed_packages:
                    print(f"  {package}: ✅")
                else:
                    print(f"  {package}: ❌")
                    missing_packages.append(package)
            
            # 检查开发依赖
            dev_packages = ["pytest", "black", "flake8"]
            missing_dev_packages = []
            
            for package in dev_packages:
                if package.lower() in installed_packages:
                    print(f"  {package} (dev): ✅")
                else:
                    print(f"  {package} (dev): ❌")
                    missing_dev_packages.append(package)
            
            self.check_results['dependencies'] = {
                'required_missing': missing_packages,
                'dev_missing': missing_dev_packages,
                'all_required_installed': len(missing_packages) == 0,
                'all_dev_installed': len(missing_dev_packages) == 0
            }
            
        except Exception as e:
            self.check_results['dependencies'] = {'error': f'检查依赖失败: {e}'}
            print(f"  检查依赖失败: {e}")
        
        return self.check_results['dependencies']
    
    def check_project_structure(self) -> Dict[str, Any]:
        """检查项目结构"""
        print("\n📁 检查项目结构...")
        
        required_paths = [
            "src/dsgs_spec_kit_integration",
            "src/dsgs_spec_kit_integration/core",
            "src/dsgs_spec_kit_integration/skills",
            "src/dsgs_spec_kit_integration/adapters",
            "tests/unit"
        ]
        
        missing_paths = []
        existing_paths = []
        
        for path in required_paths:
            full_path = self.project_root / path
            if full_path.exists():
                existing_paths.append(path)
                print(f"  {path}: ✅")
            else:
                missing_paths.append(path)
                print(f"  {path}: ❌")
        
        self.check_results['structure'] = {
            'missing_paths': missing_paths,
            'existing_paths': existing_paths,
            'all_paths_exist': len(missing_paths) == 0
        }
        
        return self.check_results['structure']
    
    def check_spec_kit_integration(self) -> Dict[str, Any]:
        """检查spec.kit集成配置"""
        print("\n🔧 检查spec.kit集成...")
        
        # 检查适配器实现
        adapter_files = [
            "src/dsgs_spec_kit_integration/adapters/spec_kit_adapter.py",
            "src/dsgs_spec_kit_integration/adapters/concrete_spec_kit_adapter.py"
        ]
        
        missing_adapters = []
        existing_adapters = []
        
        for adapter_file in adapter_files:
            full_path = self.project_root / adapter_file
            if full_path.exists():
                existing_adapters.append(adapter_file)
                print(f"  {adapter_file}: ✅")
            else:
                missing_adapters.append(adapter_file)
                print(f"  {adapter_file}: ❌")
        
        # 检查支持的AI代理
        supported_agents = [
            'claude', 'gemini', 'qwen', 'copilot',
            'cursor', 'windsurf', 'opencode', 'codex'
        ]
        
        print(f"  支持的AI代理: {', '.join(supported_agents)}")
        
        self.check_results['spec_kit'] = {
            'missing_adapters': missing_adapters,
            'existing_adapters': existing_adapters,
            'all_adapters_exist': len(missing_adapters) == 0,
            'supported_agents': supported_agents
        }
        
        return self.check_results['spec_kit']
    
    def check_local_adaptation_system(self) -> Dict[str, Any]:
        """检查本地适配系统配置"""
        print("\n⚙️ 检查本地适配系统...")
        
        adaptation_info = {
            'uv_tool': False,
            'specify_cli': False,
            'git_repo': False,
            'local_config': False
        }
        
        # 检查uv工具
        uv_path = shutil.which('uv')
        if uv_path:
            try:
                result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    adaptation_info['uv_tool'] = True
                    print(f"  uv工具: ✅ ({result.stdout.strip()})")
                else:
                    print("  uv工具: ❌")
            except:
                print("  uv工具: ❌")
        else:
            print("  uv工具: ❌")
        
        # 检查specify-cli
        specify_path = shutil.which('specify')
        if specify_path:
            try:
                result = subprocess.run(['specify', '--help'], capture_output=True, text=True)
                if result.returncode == 0:
                    adaptation_info['specify_cli'] = True
                    print("  specify-cli: ✅")
                else:
                    print("  specify-cli: ❌")
            except:
                print("  specify-cli: ❌")
        else:
            print("  specify-cli: ❌")
        
        # 检查Git仓库
        git_dir = self.project_root / ".git"
        if git_dir.exists():
            adaptation_info['git_repo'] = True
            print("  Git仓库: ✅")
        else:
            print("  Git仓库: ❌")
        
        # 检查本地配置文件
        config_files = [".gitignore", "README.md", "pyproject.toml"]
        existing_configs = []
        
        for config_file in config_files:
            if (self.project_root / config_file).exists():
                existing_configs.append(config_file)
        
        if len(existing_configs) >= 2:  # 至少需要2个配置文件
            adaptation_info['local_config'] = True
            print(f"  本地配置文件: ✅ ({', '.join(existing_configs)})")
        else:
            print(f"  本地配置文件: ❌ (找到: {', '.join(existing_configs)})")
        
        self.check_results['adaptation'] = adaptation_info
        return adaptation_info
    
    def generate_deployment_report(self) -> Dict[str, Any]:
        """生成部署报告"""
        print("\n" + "="*50)
        print("📋 部署配置检查报告")
        print("="*50)
        
        # 统计检查结果
        total_checks = 0
        passed_checks = 0
        
        # 系统环境检查
        if 'python_ok' in self.system_info:
            total_checks += 1
            if self.system_info['python_ok']:
                passed_checks += 1
        
        # 命令检查
        if 'commands' in self.system_info:
            for cmd_info in self.system_info['commands'].values():
                total_checks += 1
                if cmd_info['available']:
                    passed_checks += 1
        
        # 依赖检查
        if 'dependencies' in self.check_results:
            deps = self.check_results['dependencies']
            if isinstance(deps, dict) and 'all_required_installed' in deps:
                total_checks += 1
                if deps['all_required_installed']:
                    passed_checks += 1
        
        # 结构检查
        if 'structure' in self.check_results:
            struct = self.check_results['structure']
            if isinstance(struct, dict) and 'all_paths_exist' in struct:
                total_checks += 1
                if struct['all_paths_exist']:
                    passed_checks += 1
        
        # spec.kit检查
        if 'spec_kit' in self.check_results:
            spec_kit = self.check_results['spec_kit']
            if isinstance(spec_kit, dict) and 'all_adapters_exist' in spec_kit:
                total_checks += 1
                if spec_kit['all_adapters_exist']:
                    passed_checks += 1
        
        # 适配系统检查
        if 'adaptation' in self.check_results:
            adapt = self.check_results['adaptation']
            if isinstance(adapt, dict):
                adapt_checks = sum(1 for v in adapt.values() if v)
                total_checks += len(adapt)
                passed_checks += adapt_checks
        
        # 计算通过率
        pass_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\n📊 检查概要:")
        print(f"  总检查项: {total_checks}")
        print(f"  通过项: {passed_checks}")
        print(f"  通过率: {pass_rate:.1f}%")
        
        # 部署建议
        print(f"\n💡 部署建议:")
        if pass_rate >= 90:
            print("  🎉 项目已准备好部署!")
            deployment_ready = True
        elif pass_rate >= 70:
            print("  ⚠️  项目基本可以部署，但建议解决警告项")
            deployment_ready = True
        else:
            print("  ❌ 项目尚未准备好部署，请解决上述问题")
            deployment_ready = False
        
        return {
            'summary': {
                'total_checks': total_checks,
                'passed_checks': passed_checks,
                'pass_rate': pass_rate,
                'deployment_ready': deployment_ready
            },
            'detailed_results': self.check_results,
            'system_info': self.system_info
        }
    
    def run_full_check(self) -> Dict[str, Any]:
        """运行完整的部署配置检查"""
        print("🚀 开始自动部署配置检查...")
        print(f"项目路径: {self.project_root}")
        
        # 执行各项检查
        self.check_system_environment()
        self.check_project_dependencies()
        self.check_project_structure()
        self.check_spec_kit_integration()
        self.check_local_adaptation_system()
        
        # 生成报告
        report = self.generate_deployment_report()
        
        # 保存配置文件
        if self.config_file:
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(report, f, ensure_ascii=False, indent=2)
                print(f"\n💾 检查报告已保存到: {self.config_file}")
            except Exception as e:
                print(f"\n⚠️  保存报告失败: {e}")
        
        return report

def main():
    """主函数"""
    checker = DeploymentConfigChecker()
    report = checker.run_full_check()
    
    # 根据检查结果返回适当的退出码
    if report['summary']['deployment_ready']:
        print("\n✅ 部署检查完成 - 项目已准备好部署!")
        return 0
    else:
        print("\n❌ 部署检查完成 - 项目尚未准备好部署!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)