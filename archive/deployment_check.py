"""
项目部署准备状态检查脚本
"""
import sys
import os
import subprocess

def check_python_version():
    """检查Python版本"""
    import sys
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python版本检查通过: {sys.version}")
        return True
    else:
        print(f"✗ Python版本过低: {sys.version} (需要 >= 3.8)")
        return False

def check_dependencies():
    """检查项目依赖"""
    required_packages = ["pyyaml", "requests", "pytest"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ 依赖包 {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ 依赖包 {package} 未安装")
    
    return len(missing_packages) == 0

def check_project_structure():
    """检查项目结构"""
    required_paths = [
        "src/dnaspec_spec_kit_integration",
        "src/dnaspec_spec_kit_integration/core",
        "src/dnaspec_spec_kit_integration/skills",
        "tests/unit"
    ]
    
    missing_paths = []
    for path in required_paths:
        full_path = os.path.join(os.path.dirname(__file__), path)
        if os.path.exists(full_path):
            print(f"✓ 项目路径 {path} 存在")
        else:
            missing_paths.append(path)
            print(f"✗ 项目路径 {path} 不存在")
    
    return len(missing_paths) == 0

def check_build_system():
    """检查构建系统"""
    try:
        # 尝试导入项目
        sys.path.insert(0, os.path.dirname(__file__))
        from src.dnaspec_spec_kit_integration.core.manager import SkillManager
        from src.dnaspec_spec_kit_integration.skills.examples import ArchitectSkill
        
        # 创建并测试基本功能
        manager = SkillManager()
        skill = ArchitectSkill()
        manager.register_skill(skill)
        
        result = manager.execute_skill("dnaspec-architect", "测试系统")
        if result.status.name == "COMPLETED":
            print("✓ 项目构建和基本功能测试通过")
            return True
        else:
            print("✗ 项目基本功能测试失败")
            return False
    except Exception as e:
        print(f"✗ 项目构建测试失败: {e}")
        return False

def check_installation():
    """检查项目安装"""
    try:
        # 尝试以可编辑模式安装
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ 项目可编辑安装成功")
            return True
        else:
            print(f"✗ 项目安装失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ 项目安装检查失败: {e}")
        return False

def main():
    """主检查函数"""
    print("开始项目部署准备状态检查...\n")
    
    checks = [
        ("Python版本检查", check_python_version),
        ("依赖项检查", check_dependencies),
        ("项目结构检查", check_project_structure),
        ("构建系统检查", check_build_system),
        ("安装检查", check_installation)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, check_func in checks:
        print(f"\n[{check_name}]")
        try:
            if check_func():
                passed += 1
            else:
                print(f"  {check_name} 失败")
        except Exception as e:
            print(f"  {check_name} 检查过程中出现错误: {e}")
    
    print(f"\n{'='*50}")
    print(f"部署准备状态检查完成: {passed}/{total} 项检查通过")
    
    if passed == total:
        print("🎉 项目已准备好部署!")
        return True
    else:
        print("❌ 项目尚未准备好部署，请解决上述问题")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)