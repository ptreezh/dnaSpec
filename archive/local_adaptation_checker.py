"""
本地适配系统配置验证器
专门用于检查和配置本地部署环境
"""
import sys
import os
import subprocess
import shutil
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

class LocalAdaptationSystem:
    """本地适配系统配置验证器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.config_dir = self.project_root / ".dnaspec"
        self.adaptation_config = {}
        self.system_status = {}
    
    def setup_config_directory(self) -> bool:
        """设置配置目录"""
        try:
            if not self.config_dir.exists():
                self.config_dir.mkdir(parents=True, exist_ok=True)
                print(f"📁 创建配置目录: {self.config_dir}")
            
            # 创建适配配置文件
            adaptation_config_file = self.config_dir / "adaptation.json"
            if not adaptation_config_file.exists():
                default_config = {
                    "version": "1.0.0",
                    "supported_agents": [
                        "claude", "gemini", "qwen", "copilot",
                        "cursor", "windsurf", "opencode", "codex"
                    ],
                    "local_tools": {
                        "uv": False,
                        "specify": False,
                        "git": True
                    },
                    "deployment_targets": {
                        "local": True,
                        "pypi": False,
                        "docker": False
                    }
                }
                with open(adaptation_config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, ensure_ascii=False, indent=2)
                print(f"📄 创建适配配置文件: {adaptation_config_file}")
            
            return True
        except Exception as e:
            print(f"❌ 创建配置目录失败: {e}")
            return False
    
    def check_uv_tool(self) -> Dict[str, Any]:
        """检查uv工具配置"""
        print("🔍 检查uv工具...")
        
        uv_info = {
            'installed': False,
            'version': None,
            'path': None,
            'can_install': False
        }
        
        # 检查uv是否已安装
        uv_path = shutil.which('uv')
        if uv_path:
            try:
                result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    uv_info['installed'] = True
                    uv_info['version'] = result.stdout.strip()
                    uv_info['path'] = uv_path
                    print(f"  uv: ✅ ({uv_info['version']})")
                else:
                    print("  uv: ❌ (无法获取版本信息)")
            except Exception as e:
                print(f"  uv: ❌ (执行失败: {e})")
        else:
            print("  uv: ❌ (未安装)")
            # 检查是否可以安装
            try:
                # 简单检查PowerShell是否可用
                result = subprocess.run(['powershell', '-Command', 'echo test'], 
                                      capture_output=True, text=True)
                uv_info['can_install'] = result.returncode == 0
                if uv_info['can_install']:
                    print("  uv: 🔄 可以通过PowerShell安装")
                else:
                    print("  uv: ❌ 无法自动安装 (缺少PowerShell)")
            except:
                print("  uv: ❌ 无法自动安装")
        
        self.system_status['uv'] = uv_info
        return uv_info
    
    def check_specify_cli(self) -> Dict[str, Any]:
        """检查specify-cli配置"""
        print("🔍 检查specify-cli...")
        
        specify_info = {
            'installed': False,
            'version': None,
            'path': None,
            'can_install': False
        }
        
        # 检查specify是否已安装
        specify_path = shutil.which('specify')
        if specify_path:
            try:
                result = subprocess.run(['specify', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    specify_info['installed'] = True
                    specify_info['version'] = result.stdout.strip()
                    specify_info['path'] = specify_path
                    print(f"  specify-cli: ✅ ({specify_info['version']})")
                else:
                    print("  specify-cli: ❌ (无法获取版本信息)")
            except Exception as e:
                print(f"  specify-cli: ❌ (执行失败: {e})")
        else:
            print("  specify-cli: ❌ (未安装)")
            # 检查是否可以通过uv安装
            uv_info = self.system_status.get('uv', {})
            if uv_info.get('installed', False):
                specify_info['can_install'] = True
                print("  specify-cli: 🔄 可以通过uv工具安装")
            else:
                print("  specify-cli: ❌ 无法自动安装 (需要uv工具)")
        
        self.system_status['specify'] = specify_info
        return specify_info
    
    def check_git_configuration(self) -> Dict[str, Any]:
        """检查Git配置"""
        print("🔍 检查Git配置...")
        
        git_info = {
            'installed': False,
            'version': None,
            'path': None,
            'repository': False,
            'configured': False
        }
        
        # 检查Git是否已安装
        git_path = shutil.which('git')
        if git_path:
            try:
                result = subprocess.run(['git', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    git_info['installed'] = True
                    git_info['version'] = result.stdout.strip()
                    git_info['path'] = git_path
                    print(f"  git: ✅ ({git_info['version']})")
                else:
                    print("  git: ❌ (无法获取版本信息)")
            except Exception as e:
                print(f"  git: ❌ (执行失败: {e})")
        else:
            print("  git: ❌ (未安装)")
            return git_info
        
        # 检查是否是Git仓库
        git_dir = self.project_root / ".git"
        if git_dir.exists():
            git_info['repository'] = True
            print("  仓库: ✅")
        else:
            print("  仓库: ❌")
        
        # 检查Git配置
        try:
            result = subprocess.run(['git', 'config', 'user.name'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0 and result.stdout.strip():
                git_info['configured'] = True
                print("  配置: ✅")
            else:
                print("  配置: ⚠️ (未配置用户名)")
        except Exception as e:
            print(f"  配置: ❌ (检查失败: {e})")
        
        self.system_status['git'] = git_info
        return git_info
    
    def check_python_environment(self) -> Dict[str, Any]:
        """检查Python环境"""
        print("🔍 检查Python环境...")
        
        python_info = {
            'version': sys.version,
            'version_info': {
                'major': sys.version_info.major,
                'minor': sys.version_info.minor,
                'micro': sys.version_info.micro
            },
            'path': sys.executable,
            'virtual_env': False,
            'requirements_installed': False
        }
        
        # 检查是否在虚拟环境中
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            python_info['virtual_env'] = True
            print("  虚拟环境: ✅")
        else:
            print("  虚拟环境: ❌")
        
        print(f"  Python版本: ✅ ({python_info['version'].split()[0]})")
        print(f"  Python路径: {python_info['path']}")
        
        # 检查项目依赖
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                installed_packages = result.stdout.lower()
                required_packages = ["pyyaml", "requests", "pytest"]
                missing_packages = []
                
                for package in required_packages:
                    if package.lower() in installed_packages:
                        print(f"  {package}: ✅")
                    else:
                        print(f"  {package}: ❌")
                        missing_packages.append(package)
                
                python_info['requirements_installed'] = len(missing_packages) == 0
            else:
                print("  依赖检查: ❌ (无法执行pip list)")
        except Exception as e:
            print(f"  依赖检查: ❌ ({e})")
        
        self.system_status['python'] = python_info
        return python_info
    
    def install_missing_tools(self) -> Dict[str, bool]:
        """安装缺失的工具"""
        print("\n🔧 安装缺失的工具...")
        
        installation_results = {
            'uv': False,
            'specify': False
        }
        
        # 安装uv工具
        uv_info = self.system_status.get('uv', {})
        if not uv_info.get('installed', False) and uv_info.get('can_install', False):
            print("  正在安装uv工具...")
            try:
                # 使用PowerShell安装uv
                install_cmd = 'powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"'
                result = subprocess.run(install_cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    installation_results['uv'] = True
                    print("  uv工具安装成功! ✅")
                else:
                    print(f"  uv工具安装失败: {result.stderr}")
            except Exception as e:
                print(f"  uv工具安装异常: {e}")
        elif uv_info.get('installed', False):
            installation_results['uv'] = True
            print("  uv工具已安装 ✅")
        else:
            print("  无法安装uv工具 ❌")
        
        # 安装specify-cli
        specify_info = self.system_status.get('specify', {})
        uv_installed = installation_results['uv'] or uv_info.get('installed', False)
        
        if not specify_info.get('installed', False) and uv_installed:
            print("  正在安装specify-cli...")
            try:
                result = subprocess.run(['uv', 'tool', 'install', 'specify-cli', 
                                       '--from', 'git+https://github.com/github/spec-kit.git'],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    installation_results['specify'] = True
                    print("  specify-cli安装成功! ✅")
                else:
                    print(f"  specify-cli安装失败: {result.stderr}")
            except Exception as e:
                print(f"  specify-cli安装异常: {e}")
        elif specify_info.get('installed', False):
            installation_results['specify'] = True
            print("  specify-cli已安装 ✅")
        else:
            print("  无法安装specify-cli (需要uv工具) ❌")
        
        return installation_results
    
    def configure_local_deployment(self) -> Dict[str, Any]:
        """配置本地部署环境"""
        print("\n⚙️ 配置本地部署环境...")
        
        config_results = {
            'project_installed': False,
            'editable_install': False,
            'tests_passed': False
        }
        
        # 安装项目为可编辑模式
        try:
            print("  安装项目为可编辑模式...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."],
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                config_results['project_installed'] = True
                config_results['editable_install'] = True
                print("  项目安装成功! ✅")
            else:
                print(f"  项目安装失败: {result.stderr}")
        except Exception as e:
            print(f"  项目安装异常: {e}")
        
        # 运行基本功能测试
        try:
            print("  运行基本功能测试...")
            test_script = self.project_root / "test_basic_functionality.py"
            if test_script.exists():
                result = subprocess.run([sys.executable, "test_basic_functionality.py"],
                                      capture_output=True, text=True, cwd=self.project_root)
                if result.returncode == 0:
                    config_results['tests_passed'] = True
                    print("  基本功能测试通过! ✅")
                else:
                    print(f"  基本功能测试失败: {result.stdout}")
            else:
                print("  测试脚本不存在")
        except Exception as e:
            print(f"  功能测试异常: {e}")
        
        return config_results
    
    def generate_adaptation_report(self) -> Dict[str, Any]:
        """生成适配系统报告"""
        print("\n" + "="*50)
        print("📋 本地适配系统配置报告")
        print("="*50)
        
        # 统计配置状态
        total_checks = 0
        passed_checks = 0
        
        # 检查各个组件
        components = ['uv', 'specify', 'git', 'python']
        for component in components:
            if component in self.system_status:
                total_checks += 1
                # 根据不同组件的检查标准判断是否通过
                component_info = self.system_status[component]
                if component == 'uv':
                    if component_info.get('installed', False):
                        passed_checks += 1
                elif component == 'specify':
                    # specify-cli不是必需的
                    total_checks -= 1  # 不计入必需检查
                elif component == 'git':
                    if component_info.get('installed', False) and component_info.get('repository', False):
                        passed_checks += 1
                elif component == 'python':
                    if component_info.get('requirements_installed', False):
                        passed_checks += 1
        
        # 计算通过率
        pass_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\n📊 配置概要:")
        print(f"  总检查项: {total_checks}")
        print(f"  通过项: {passed_checks}")
        print(f"  通过率: {pass_rate:.1f}%")
        
        # 配置建议
        print(f"\n💡 配置建议:")
        if pass_rate >= 80:
            print("  🎉 本地适配系统配置完成!")
            adaptation_ready = True
        elif pass_rate >= 60:
            print("  ⚠️  本地适配系统基本配置完成，但建议完善配置")
            adaptation_ready = True
        else:
            print("  ❌ 本地适配系统配置不完整，请解决上述问题")
            adaptation_ready = False
        
        return {
            'summary': {
                'total_checks': total_checks,
                'passed_checks': passed_checks,
                'pass_rate': pass_rate,
                'adaptation_ready': adaptation_ready
            },
            'system_status': self.system_status,
            'project_root': str(self.project_root)
        }
    
    def run_full_adaptation_check(self) -> Dict[str, Any]:
        """运行完整的本地适配系统检查"""
        print("🚀 开始本地适配系统配置检查...")
        print(f"项目路径: {self.project_root}")
        
        # 设置配置目录
        self.setup_config_directory()
        
        # 检查各个系统组件
        self.check_uv_tool()
        self.check_specify_cli()
        self.check_git_configuration()
        self.check_python_environment()
        
        # 生成适配报告
        report = self.generate_adaptation_report()
        
        # 保存适配配置
        adaptation_config_file = self.config_dir / "adaptation.json"
        if adaptation_config_file.exists():
            try:
                with open(adaptation_config_file, 'r', encoding='utf-8') as f:
                    existing_config = json.load(f)
                
                # 更新系统状态
                existing_config['system_status'] = self.system_status
                existing_config['last_check'] = report['summary']
                
                with open(adaptation_config_file, 'w', encoding='utf-8') as f:
                    json.dump(existing_config, f, ensure_ascii=False, indent=2)
                print(f"\n💾 适配配置已更新: {adaptation_config_file}")
            except Exception as e:
                print(f"\n⚠️  更新适配配置失败: {e}")
        
        return report

def main():
    """主函数"""
    adaptation_system = LocalAdaptationSystem()
    report = adaptation_system.run_full_adaptation_check()
    
    # 根据检查结果返回适当的退出码
    if report['summary']['adaptation_ready']:
        print("\n✅ 本地适配系统配置完成!")
        return 0
    else:
        print("\n❌ 本地适配系统配置未完成!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)