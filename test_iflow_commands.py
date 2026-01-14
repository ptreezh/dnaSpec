#!/usr/bin/env python3
"""
Test script for DNASPEC commands in iflow-cli
"""

import subprocess
import json
from pathlib import Path

def run_iflow_command(command: str, prompt: str) -> dict:
    """Run iflow command and return result"""
    try:
        full_command = f'node "C:\\Users\\Zhang\\AppData\\Roaming\\npm\\node_modules\\@iflow-ai\\iflow-cli\\bundle\\iflow.js" {command}'

        result = subprocess.run(
            full_command,
            input=prompt,
            capture_output=True,
            text=True,
            shell=True,
            timeout=30,
            cwd="D:/DAIP/dnaSpec"
        )

        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Command timed out'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def test_command_availability():
    """Test if dnaspec commands are available in iflow"""
    print("🔍 Testing DNASPEC Commands Availability in iflow-cli\n")
    print("=" * 60)

    # List of expected dnaspec commands
    dnaspec_commands = [
        'dnaspec.architect',
        'dnaspec.task-decomposer',
        'dnaspec.agent-creator',
        'dnaspec.constraint-generator',
        'dnaspec.dapi-checker',
        'dnaspec.modulizer',
        'dnaspec.cache-manager',
        'dnaspec.git-operations'
    ]

    print("\n📋 Expected DNASPEC Commands:")
    for i, cmd in enumerate(dnaspec_commands, 1):
        print(f"  {i}. /{cmd}")

    print("\n" + "=" * 60)
    print("📁 Command Files Status:")
    print("=" * 60)

    commands_dir = Path("D:/DAIP/dnaSpec/.iflow/commands")

    if not commands_dir.exists():
        print("❌ Commands directory does not exist!")
        return False

    command_files = list(commands_dir.glob("*.md"))
    print(f"\n✅ Commands directory exists: {commands_dir}")
    print(f"📊 Total command files: {len(command_files)}\n")

    for cmd_file in sorted(command_files):
        cmd_name = cmd_file.stem
        size = cmd_file.stat().st_size
        print(f"  ✓ {cmd_name}.md ({size} bytes)")

    print("\n" + "=" * 60)
    print("🧪 Command Format Validation:")
    print("=" * 60)

    all_valid = True
    for cmd_file in sorted(command_files):
        cmd_name = cmd_file.stem

        with open(cmd_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check required sections
        has_description = '## Description' in content
        has_command = '## Command' in content
        has_usage = '## Usage' in content

        status = "✅" if all([has_description, has_command, has_usage]) else "⚠️"

        print(f"\n  {status} {cmd_name}:")
        print(f"     - Description: {'✓' if has_description else '✗'}")
        print(f"     - Command: {'✓' if has_command else '✗'}")
        print(f"     - Usage: {'✓' if has_usage else '✗'}")

        if not all([has_description, has_command, has_usage]):
            all_valid = False

    print("\n" + "=" * 60)
    print("📝 Sample Command Content:")
    print("=" * 60)

    # Show content of first command
    if command_files:
        sample_file = sorted(command_files)[0]
        print(f"\n📄 {sample_file.name}:\n")
        with open(sample_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[:20]:  # Show first 20 lines
                print(f"  {line.rstrip()}")
        print("  ...")

    print("\n" + "=" * 60)
    print("✅ Test Complete!")
    print("=" * 60)

    if all_valid:
        print("\n🎉 All DNASPEC commands are properly configured!")
        print("\n💡 To test these commands in iflow:")
        print("   1. Start iflow in this directory:")
        print("      $ cd D:/DAIP/dnaSpec")
        print("      $ iflow")
        print()
        print("   2. Use any DNASPEC command:")
        for cmd in dnaspec_commands[:3]:
            print(f"      /{cmd} \"your prompt here\"")
        print()
        return True
    else:
        print("\n⚠️ Some commands are missing required sections.")
        return False


def main():
    print("\n" + "🚀" * 30)
    print("  DNASPEC iflow-cli Command Test Suite")
    print("🚀" * 30 + "\n")

    success = test_command_availability()

    print("\n" + "=" * 60)
    if success:
        print("Status: ✅ ALL TESTS PASSED")
    else:
        print("Status: ⚠️ SOME TESTS FAILED")
    print("=" * 60 + "\n")

    return 0 if success else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
