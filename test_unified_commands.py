#!/usr/bin/env python3
"""
DNASPEC统一命令格式测试脚本
验证所有命令都使用 /dnaspec.* 格式
"""
import re
import sys
from pathlib import Path

def check_command_format_in_file(file_path: Path) -> dict:
    """检查文件中的命令格式"""
    issues = []

    if not file_path.exists():
        return {"file": str(file_path), "issues": ["File not found"]}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查各种不统一的格式
        patterns = [
            (r'/speckit\.dnaspec\.[^\s\]]+', 'Old format: /speckit.dnaspec.* (should be /dnaspec.*)'),
            (r'/dnaspec-[^\s\]]+', 'Dash format: /dnaspec-* (should be /dnaspec.*)'),
            (r'["\`]dnaspec-[^\s\'"`\]]+["`]', 'No slash format: dnaspec-* (should be /dnaspec.*)'),
        ]

        for pattern, description in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                # 获取行号
                lines = content.split('\n')
                line_num = 0
                for i, line in enumerate(lines):
                    if match in line:
                        line_num = i + 1
                        break

                issues.append({
                    "line": line_num,
                    "issue": description,
                    "found": match,
                    "suggested": match.replace('/speckit.dnaspec.', '/dnaspec.').replace('/dnaspec-', '/dnaspec.')
                })

    except Exception as e:
        issues.append(f"Error reading file: {str(e)}")

    return {"file": str(file_path.relative_to(Path.cwd())), "issues": issues}

def test_unified_command_format():
    """测试统一的命令格式"""
    print("🧪 DNASPEC Unified Command Format Test")
    print("=" * 50)

    project_root = Path.cwd()

    # 定义标准命令格式
    standard_commands = [
        '/dnaspec.context-analysis',
        '/dnaspec.context-optimization',
        '/dnaspec.cognitive-template',
        '/dnaspec.architect',
        '/dnaspec.task-decomposer',
        '/dnaspec.agent-creator',
        '/dnaspec.constraint-generator',
        '/dnaspec.dapi-checker',
        '/dnaspec.modulizer',
        '/dnaspec.cache-manager',
        '/dnaspec.git-operations',
        '/dnaspec.temp-workspace',
        '/dnaspec.examples',
        '/dnaspec.liveness',
        '/dnaspec.version'
    ]

    print("✅ Standard command format: /dnaspec.*")
    print(f"📋 {len(standard_commands)} standard commands defined")
    print("")

    # 检查关键文件
    test_files = [
        'src/dna_spec_kit_integration/core/cli_extension_deployer.py',
        'src/dna_context_engineering/skills_system_final.py',
        'src/dna_spec_kit_integration/adapters/spec_kit_adapter.py',
        'init_dnaspec_complete.py',
        'DNASPEC_SECURE_WORKFLOW_GUIDE.md',
        'DNASPEC_UNIFIED_COMMANDS.md'
    ]

    total_issues = 0
    files_with_issues = 0

    print("🔍 Checking command format consistency...")
    print("")

    for file_path in test_files:
        full_path = project_root / file_path
        result = check_command_format_in_file(full_path)

        if result["issues"]:
            files_with_issues += 1
            print(f"❌ {result['file']}:")

            for issue in result["issues"]:
                if isinstance(issue, dict):
                    print(f"   Line {issue['line']}: {issue['issue']}")
                    print(f"     Found: {issue['found']}")
                    print(f"     Suggested: {issue['suggested']}")
                    total_issues += 1
                else:
                    print(f"   {issue}")
        else:
            print(f"✅ {result['file']}: No format issues")

    print("")
    print("📊 Test Summary:")
    print(f"  Files checked: {len(test_files)}")
    print(f"  Files with issues: {files_with_issues}")
    print(f"  Total issues found: {total_issues}")

    # 验证标准命令格式
    print("")
    print("✅ Standard Command Examples:")
    for i, cmd in enumerate(standard_commands[:8], 1):
        print(f"  {i:2d}. {cmd}")

    print("")
    if total_issues == 0:
        print("🎉 All command formats are unified!")
        print("✅ Ready to use DNASPEC with consistent /dnaspec.* commands")
        return True
    else:
        print("⚠️  Command format issues found!")
        print("💡 Run the fix script: python fix_command_format.py")
        return False

def generate_command_test_cases():
    """生成命令测试用例"""
    test_cases = [
        # 基本命令测试
        ("/dnaspec.context-analysis", "Valid format", True),
        ("/dnaspec.architect", "Valid format", True),
        ("/dnaspec.temp-workspace operation=create", "Valid format with args", True),

        # 无效格式测试
        ("/speckit.dnaspec.context-analysis", "Old format", False),
        ("/dnaspec-context-analysis", "Dash format", False),
        ("dnaspec.context-analysis", "Missing slash", False),

        # 边界情况
        ("/dnaspec.", "Empty skill name", False),
        ("/dnaspec", "Missing dot", False),
        ("", "Empty command", False),
    ]

    print("\n🧪 Command Format Test Cases:")
    print("=" * 40)

    passed = 0
    total = len(test_cases)

    for command, description, expected in test_cases:
        # 简单的格式验证
        is_valid = bool(re.match(r'^/dnaspec\.[a-zA-Z][a-zA-Z0-9_-]*(\s.*)?$', command))

        status = "✅" if is_valid == expected else "❌"
        result = "PASS" if is_valid == expected else "FAIL"

        print(f"{status} {description}")
        print(f"   Command: {command}")
        print(f"   Expected: {expected}, Got: {is_valid}, Result: {result}")
        print("")

        if is_valid == expected:
            passed += 1

    print(f"Test Results: {passed}/{total} passed")
    return passed == total

def main():
    """主测试函数"""
    print("🚀 Starting DNASPEC Command Format Tests")
    print("=" * 60)

    # 测试1: 文件格式检查
    format_test_passed = test_unified_command_format()

    # 测试2: 命令格式验证
    print("\n" + "=" * 60)
    validation_test_passed = generate_command_test_cases()

    # 总体结果
    print("\n" + "=" * 60)
    print("🏁 Overall Test Results:")
    print(f"  Format consistency test: {'PASSED' if format_test_passed else 'FAILED'}")
    print(f"  Command validation test: {'PASSED' if validation_test_passed else 'FAILED'}")

    if format_test_passed and validation_test_passed:
        print("\n🎉 All tests passed!")
        print("✅ DNASPEC commands are properly unified with /dnaspec.* format")
        print("\n📋 Next steps:")
        print("1. Test commands in your AI CLI tools")
        print("2. Verify all commands work correctly")
        print("3. Update team documentation if needed")
        return 0
    else:
        print("\n❌ Some tests failed!")
        print("💡 To fix issues:")
        print("1. Run: python fix_command_format.py")
        print("2. Review and test the changes")
        print("3. Re-run this test script")
        return 1

if __name__ == "__main__":
    sys.exit(main())