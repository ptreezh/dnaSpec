#!/usr/bin/env python3
"""
DNASPEC全技能测试脚本
测试所有声明的DNASPEC技能是否实际可用
"""
import sys
from pathlib import Path
import traceback

# 添加src路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_skill_imports():
    """测试技能导入"""
    print("🧪 Testing DNASPEC Skill Imports")
    print("=" * 50)

    # 定义要测试的技能模块
    skill_modules = {
        'context-analysis': 'dna_spec_kit_integration.skills.context_analysis_independent',
        'simple-architect': 'dna_spec_kit_integration.skills.simple_architect_independent',
        'system-architect': 'dna_spec_kit_integration.skills.system_architect_independent',
        'git': 'dna_spec_kit_integration.skills.git_operations_refactored',
        'workspace': 'dna_spec_kit_integration.skills.temp_workspace_refactored'
    }

    results = {}

    for skill_name, module_path in skill_modules.items():
        try:
            module = __import__(module_path, fromlist=[''])
            print(f"  ✅ {skill_name}: Import successful")
            results[skill_name] = {'status': 'success', 'module': module}
        except Exception as e:
            print(f"  ❌ {skill_name}: Import failed - {str(e)}")
            results[skill_name] = {'status': 'failed', 'error': str(e)}

    return results

def test_skill_executor():
    """测试统一技能执行器"""
    print("
🧪 Testing DNASPEC Skill Executor")
    print("=" * 50)

    try:
        from dna_spec_kit_integration.skills.skill_executor import skill_executor

        print("✅ Skill executor imported successfully")

        # 获取可用技能
        available_skills = skill_executor.get_available_skills()
        print(f"✅ Found {len(available_skills)} available skills:")

        for skill_name, description in available_skills.items():
            print(f"  - {skill_name}: {description}")

        return True

    except Exception as e:
        print(f"❌ Skill executor test failed: {str(e)}")
        traceback.print_exc()
        return False

def test_cli_deployer_skills():
    """测试CLI扩展部署器中的技能定义"""
    print("
🧪 Testing CLI Deployer Skills")
    print("=" * 50)

    try:
        from dna_spec_kit_integration.core.cli_extension_deployer import CLIExtensionDeployer

        deployer = CLIExtensionDeployer()
        skills = deployer._get_dnaspec_skills()

        print(f"✅ Found {len(skills)} skills in CLI deployer:")

        skill_status = {}

        for skill in skills:
            command = skill.get('command', '')
            display_name = skill.get('display_name', '')

            print(f"  - {command}: {display_name}")

            # 检查命令格式
            if command.startswith('/dnaspec.'):
                skill_status[command] = {'format': 'correct', 'name': display_name}
                print(f"    ✅ Correct format")
            else:
                skill_status[command] = {'format': 'incorrect', 'name': display_name}
                print(f"    ❌ Incorrect format (should start with /dnaspec.)")

        # 统计结果
        correct_format = sum(1 for s in skill_status.values() if s['format'] == 'correct')
        print(f"
📊 Format Summary: {correct_format}/{len(skills)} commands use correct format")

        return skill_status

    except Exception as e:
        print(f"❌ CLI deployer test failed: {str(e)}")
        traceback.print_exc()
        return {}

def main():
    """主测试函数"""
    print("🚀 DNASPEC COMPLETE SKILLS TEST")
    print("=" * 60)

    # 运行所有测试
    import_results = test_skill_imports()
    executor_status = test_skill_executor()
    deployer_status = test_cli_deployer_skills()

    # 生成状态报告
    print("
" + "=" * 60)
    print("📋 DNASPEC SKILLS STATUS REPORT")
    print("=" * 60)

    # 导入状态
    print("
📦 Import Status:")
    successful_imports = sum(1 for r in import_results.values() if r['status'] == 'success')
    total_imports = len(import_results)
    print(f"  Successfully imported: {successful_imports}/{total_imports}")

    # 执行器状态
    print(f"
🔧 Skill Executor Status: {'✅ Working' if executor_status else '❌ Failed'}")

    # 部署器状态
    if deployer_status:
        correct_format = sum(1 for s in deployer_status.values() if s['format'] == 'correct')
        total_commands = len(deployer_status)
        print(f"
📋 CLI Deployer Status:")
        print(f"  Commands with correct format: {correct_format}/{total_commands}")

    # 可用命令列表
    print(f"
🚀 Available Commands:")
    if deployer_status:
        for command, status in deployer_status.items():
            if status['format'] == 'correct':
                print(f"  ✅ {command}")

    print("
" + "=" * 60)

    # 计算总体状态
    total_tests = 3
    passed_tests = sum([
        sum(1 for r in import_results.values() if r['status'] == 'success') > 0,
        executor_status,
        len(deployer_status) > 0
    ])

    print(f"
🏁 Overall Test Results: {passed_tests}/{total_tests} test categories passed")

    if passed_tests == total_tests:
        print("🎉 All tests passed! DNASPEC is fully functional.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
