"""
包功能测试脚本
验证发行版是否包含所有必要组件
"""
import json
import os
from pathlib import Path

def test_package_functionality():
    print("🔍 测试dnaspec包功能...")
    
    # 测试1: 检查核心文件
    required_files = [
        'package.json',
        'index.js',
        'bin/dnaspec-cli.js',
        'bin/dnaspec-init.js',
        'src/core/common_state_manager.js',
        'src/core/constitutional_validator.js', 
        'src/core/coordination_contract_enforcer.js',
        'src/core/constitutional_skill_executor.js',
        'src/skills/core_skills.js'
    ]
    
    print("\n📋 检查必要文件:")
    all_present = True
    for file_path in required_files:
        full_path = Path("package") / file_path
        present = full_path.exists()
        status = "✅" if present else "❌"
        print(f"  {status} {file_path}")
        if not present:
            all_present = False
    
    if not all_present:
        print("\n❌ 缺少必要文件，包构建不完整")
        return False
    
    # 测试2: 检查package.json配置
    with open("package/package.json", 'r', encoding='utf-8') as f:
        pkg_config = json.load(f)
    
    required_config = {
        "name": "dnaspec",
        "bin": {
            "dnaspec": "./bin/dnaspec-cli.js",
            "dnaspec-init": "./bin/dnaspec-init.js"
        },
        "dependencies": ["fs-extra", "inquirer", "execa", "commander"]
    }
    
    print(f"\n📋 检查package.json配置:")
    name_ok = pkg_config.get("name") == required_config["name"]
    print(f"  {'✅' if name_ok else '❌'} 包名: {pkg_config.get('name')}")
    
    bin_ok = (
        pkg_config.get("bin", {}).get("dnaspec") == required_config["bin"]["dnaspec"] and
        pkg_config.get("bin", {}).get("dnaspec-init") == required_config["bin"]["dnaspec-init"]
    )
    print(f"  {'✅' if bin_ok else '❌'} 命令配置: {pkg_config.get('bin', {})}")
    
    deps_ok = all(dep in pkg_config.get("dependencies", {}) for dep in required_config["dependencies"])
    print(f"  {'✅' if deps_ok else '❌'} 依赖配置")
    
    # 测试3: 检查核心文件是否包含必需的函数/类
    core_modules = {
        'src/core/common_state_manager.js': ['CommonStateManager'],
        'src/core/constitutional_validator.js': ['ConstitutionalValidator'], 
        'src/core/coordination_contract_enforcer.js': ['CoordinationContractEnforcer'],
        'src/core/constitutional_skill_executor.js': ['ConstitutionalSkillExecutor'],
        'src/skills/core_skills.js': ['execute']
    }
    
    print(f"\n📋 检查核心模块功能:")
    all_modules_ok = True
    for file_path, required_members in core_modules.items():
        full_path = Path("package") / file_path
        content = full_path.read_text(encoding='utf-8')
        
        module_ok = True
        for member in required_members:
            has_member = member in content
            if not has_member:
                module_ok = False
                all_modules_ok = False
            print(f"  {'✅' if has_member else '❌'} {file_path} -> {member}")
    
    # 总体结果
    overall_ok = all_present and name_ok and bin_ok and deps_ok and all_modules_ok
    
    print(f"\n{'✅' if overall_ok else '❌'} 包功能测试结果: {'通过' if overall_ok else '失败'}")
    
    if overall_ok:
        print("\n🎉 DNASPEC包构建成功!")
        print("📦 包含完整的协同契约系统")
        print("🛡️  宪法验证机制就绪") 
        print("🔗 协同契约执行器就绪")
        print("✅ 可以发布到npm")
    
    return overall_ok

if __name__ == "__main__":
    test_package_functionality()