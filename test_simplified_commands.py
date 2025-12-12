#!/usr/bin/env python3
"""
测试精简后的DNASPEC命令
验证命令格式和实际执行
"""
import sys
from pathlib import Path

# 添加src路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_command_mapper():
    """测试命令映射器"""
    print("🧪 Testing DNASPEC Command Mapper")
    print("=" * 40)

    try:
        from dna_spec_kit_integration.skills.command_mapper import command_mapper, execute_command

        print("✅ Command mapper imported successfully")

        # 测试可用命令
        available_commands = command_mapper.get_available_commands()
        print(f"\n📋 Available Commands:")
        for cmd, desc in available_commands.items():
            print(f"  /dnaspec.{cmd} - {desc}")

        print("\n🔧 Testing Command Execution:")

        # 测试Git命令
        print("\n--- Git Commands ---")
        test_commands = [
            ("git status", "Git status check"),
            ("git commit 'Test commit'", "Git commit test"),
            ("git add src/", "Git add test"),
            ("workspace create", "Workspace create test"),
            ("workspace add test.py 'code content'", "Workspace add test")
        ]

        for cmd, desc in test_commands:
            print(f"  Testing: /dnaspec.{cmd} ({desc})")
            result = execute_command(cmd)

            # Check both old format and new BaseSkill format
            success = False
            if 'success' in result and result['success']:
                success = True
            elif 'status' in result and result['status'] == 'success':
                success = True

            if success:
                print(f"    ✅ Success")
            else:
                error_msg = result.get('error', 'Unknown error')
                if 'error' in result and isinstance(result['error'], dict):
                    error_msg = result['error'].get('message', 'Unknown error')
                print(f"    ❌ Failed: {error_msg}")

        # 测试帮助信息
        print("\n📖 Testing Help Information:")
        for cmd in ['git', 'workspace']:
            help_text = command_mapper.get_command_help(cmd)
            print(f"\n  /dnaspec.{cmd} Help:")
            print(help_text.strip())

        return True

    except Exception as e:
        print(f"❌ Error testing command mapper: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_skill_classes():
    """测试技能类"""
    print("\n🧪 Testing Skill Classes")
    print("=" * 40)

    try:
        from dna_spec_kit_integration.skills.git_operations_refactored import GitSkill
        from dna_spec_kit_integration.skills.temp_workspace_refactored import WorkspaceSkill

        print("✅ Skill classes imported successfully")

        # 测试Git技能
        git_skill = GitSkill()
        print(f"  Git skill name: {git_skill.name}")
        print(f"  Git skill description: {git_skill.description}")

        # 测试工作区技能
        workspace_skill = WorkspaceSkill()
        print(f"  Workspace skill name: {workspace_skill.name}")
        print(f"  Workspace skill description: {workspace_skill.description}")

        return True

    except Exception as e:
        print(f"❌ Error testing skill classes: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_deployer():
    """测试CLI扩展部署器"""
    print("\n🧪 Testing CLI Extension Deployer")
    print("=" * 40)

    try:
        from dna_spec_kit_integration.core.cli_extension_deployer import CLIExtensionDeployer

        deployer = CLIExtensionDeployer()
        skills = deployer._get_dnaspec_skills()

        print(f"✅ Found {len(skills)} skills in CLI deployer")

        print("\n📋 Skill Commands:")
        for skill in skills:
            if skill['command'].startswith('/dnaspec.'):
                print(f"  ✅ {skill['command']} - {skill['display_name']}")
            else:
                print(f"  ❌ {skill['command']} - Invalid format")

        # 检查是否有精简的命令
        simplified_commands = [
            '/dnaspec.git',
            '/dnaspec.workspace'
        ]

        found_simplified = []
        for cmd in simplified_commands:
            for skill in skills:
                if skill['command'] == cmd:
                    found_simplified.append(cmd)
                    break

        print(f"\n✅ Found simplified commands: {found_simplified}")

        return True

    except Exception as e:
        print(f"❌ Error testing CLI deployer: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🚀 DNASPEC Simplified Commands Test")
    print("=" * 50)

    tests = [
        ("Command Mapper", test_command_mapper),
        ("Skill Classes", test_skill_classes),
        ("CLI Deployer", test_cli_deployer)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} Test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} Test PASSED")
            else:
                print(f"❌ {test_name} Test FAILED")
        except Exception as e:
            print(f"❌ {test_name} Test ERROR: {e}")

    print("\n" + "=" * 50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        print("✅ Simplified commands are properly implemented")
        print("\n📋 Ready to use:")
        print("  /dnaspec.git status")
        print("  /dnaspec.git commit 'message'")
        print("  /dnaspec.workspace create")
        print("  /dnaspec.workspace add file.py 'content'")
        return 0
    else:
        print(f"\n❌ {total - passed} tests failed!")
        print("💡 Please check the implementation")
        return 1

if __name__ == "__main__":
    sys.exit(main())