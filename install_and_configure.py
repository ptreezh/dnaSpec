#!/usr/bin/env python3
"""
DNASPEC Context Engineering Skills - 一键安装和配置脚本
自动处理环境依赖安装和CLI工具自动配置
"""
import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(cmd, description="执行命令", check=True):
    """执行命令并显示进度"""
    print(f"🔧 {description}...")
    print(f"   命令: {cmd}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )
        
        if result.returncode != 0 and check:
            print(f"❌ {description}失败:")
            print(f"   错误: {result.stderr}")
            return False
        elif result.returncode == 0:
            print(f"✅ {description}成功")
        
        return result
    except subprocess.TimeoutExpired:
        print(f"❌ {description}超时")
        return False
    except Exception as e:
        print(f"❌ {description}出错: {str(e)}")
        return False


def check_dependencies():
    """检查必要的依赖"""
    print("🔍 检查依赖...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version < (3, 8):
        print(f"❌ 需要Python 3.8或更高版本，当前版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
        return False
    else:
        print(f"✅ 检测到Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查Git
    if not run_command("git --version", "检查Git版本", check=False):
        print("❌ 未找到Git，请先安装Git")
        return False
    
    print("✅ 依赖检查通过")
    return True


def install_dsgs():
    """安装DSGS包"""
    print("\n📦 安装DSGS Context Engineering Skills...")
    
    # 检查是否已存在项目目录
    project_dir = Path("dnaSpec")
    if project_dir.exists():
        print("🔄 更新现有项目...")
        os.chdir(project_dir)
        result = run_command("git pull", "更新项目")
        if not result or result.returncode != 0:
            return False
    else:
        print("📂 克隆项目...")
        result = run_command(
            "git clone https://github.com/ptreezh/dnaSpec.git",
            "克隆项目"
        )
        if not result or result.returncode != 0:
            return False
        
        os.chdir(project_dir)
    
    # 安装项目
    result = run_command("pip install -e .", "安装DSGS包")
    if not result:
        return False
    
    print("✅ DSGS包安装成功")
    return True


def run_auto_config():
    """运行自动配置"""
    print("\n🚀 运行自动配置...")

    # 设置环境变量以避免编码问题
    import os
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
    os.environ.setdefault('LANG', 'en_US.UTF-8')

    # 导入并运行自动配置器
    try:
        from src.dnaspec_spec_kit_integration.core.auto_configurator import AutoConfigurator

        print("   初始化自动配置器...")
        auto_config = AutoConfigurator()

        print("   开始自动配置流程...")
        result = auto_config.quick_configure()

        if result['success']:
            print("✅ 自动配置成功完成！")
            print(f"   配置文件位置: {result['configPath']}")
            print(f"   验证报告位置: {result['reportPath']}")

            # 显示检测到的平台
            detected_count = len(result.get('validation', {}))
            if detected_count > 0:
                print(f"   检测到 {detected_count} 个CLI工具:")
                for platform_name in result['validation'].keys():
                    print(f"     • {platform_name}")
            else:
                print("   未检测到已安装的CLI工具，但配置已生成")

            return True
        else:
            print(f"❌ 自动配置失败: {result.get('error', '未知错误')}")
            return False

    except ImportError as e:
        print(f"❌ 无法导入自动配置器: {e}")
        print("   尝试直接运行配置脚本...")

        # 备用方案：直接运行配置脚本
        result = run_command("python run_auto_config.py", "运行自动配置", check=False)
        return result is not None and result.returncode == 0
    except Exception as e:
        print(f"❌ 自动配置出错: {e}")
        return False


def main():
    """主函数"""
    print("\n" + "="*70)
    print("DNASPEC Context Engineering Skills - 一键安装配置脚本")
    print("自动处理环境依赖安装和CLI工具自动配置")
    print("="*70)
    
    # 检查依赖
    if not check_dependencies():
        print("\n❌ 依赖检查失败，安装终止")
        sys.exit(1)
    
    # 安装DSGS
    if not install_dsgs():
        print("\n❌ DSGS安装失败，安装终止")
        sys.exit(1)
    
    # 运行自动配置
    if not run_auto_config():
        print("\n❌ 自动配置失败，但DSGS已安装")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("🎉 安装和配置成功完成！")
    print("="*70)
    
    print("\n现在您可以在AI CLI工具中使用以下命令：")
    print("  /speckit.dnaspec.context-analysis [上下文] - 分析上下文质量")
    print("  /speckit.dnaspec.context-optimization [上下文] - 优化上下文")
    print("  /speckit.dnaspec.cognitive-template [任务] template=[模板类型] - 应用认知模板")
    print("  /speckit.dnaspec.architect [需求] - 系统架构设计")
    print("  ...以及其他DSGS专业技能")
    
    print(f"\n系统信息:")
    print(f"  操作系统: {platform.system()} {platform.release()}")
    print(f"  Python版本: {sys.version}")
    print(f"  工作目录: {os.getcwd()}")
    
    print("\n感谢使用DSGS Context Engineering Skills！")


if __name__ == "__main__":
    main()