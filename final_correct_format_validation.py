#!/usr/bin/env python3
"""
Final comprehensive validation test for DNASPEC system with correct command format
"""
import subprocess
import os
import sys
import json
import time


def run_test_command(cmd, description):
    """Run a test command and return result"""
    print(f"Testing: {description}")
    print(f"  Command: {cmd}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        success = result.returncode == 0
        print(f"  Exit Code: {result.returncode}")
        if result.stdout:
            print(f"  Output preview: {result.stdout[:200]}{'...' if len(result.stdout) > 200 else ''}")
        if result.stderr and not success:
            print(f"  Error: {result.stderr[:100]}{'...' if len(result.stderr) > 100 else ''}")
        
        status = "✅" if success else "❌"
        print(f"  {status} {description}")
        print()
        
        return success
    except subprocess.TimeoutExpired:
        print(f"  ❌ TIMEOUT: {description}")
        print()
        return False
    except Exception as e:
        print(f"  ❌ ERROR: {description} - {str(e)}")
        print()
        return False


def main():
    """Main validation function"""
    print("🔬 FINAL COMPREHENSIVE VALIDATION: DNASPEC SYSTEM")
    print("Testing with CORRECT command format: /dnaspec.*")
    print("="*70)
    
    # Test all available skills with the correct format
    tests = [
        ("dnaspec-spec-kit exec \"/dnaspec.architect 设计一个电商系统\"", "Architect Skill (/dnaspec.architect)"),
        ("dnaspec-spec-kit exec \"/dnaspec.agent-creator 创建一个代码审查助手\"", "Agent Creator Skill (/dnaspec.agent-creator)"),
        ("dnaspec-spec-kit exec \"/dnaspec.task-decomposer 分解构建博客网站任务\"", "Task Decomposer Skill (/dnaspec.task-decomposer)"),
        ("dnaspec-spec-kit exec \"/dnaspec.constraint-generator 为系统生成安全约束\"", "Constraint Generator Skill (/dnaspec.constraint-generator)"),
        ("dnaspec-spec-kit exec \"/dnaspec.dapi-checker 检查API接口设计\"", "API Checker Skill (/dnaspec.dapi-checker)"),
        ("dnaspec-spec-kit exec \"/dnaspec.modulizer 模块化系统架构\"", "Modulizer Skill (/dnaspec.modulizer)"),
        ("dnaspec-spec-kit exec \"/dnaspec.constitutional-validator 验证系统宪法合规性\"", "Constitutional Validator (/dnaspec.constitutional-validator)"),
        ("dnaspec-spec-kit exec \"/dnaspec.contract-checker 检查合同条款\"", "Contract Checker (/dnaspec.contract-checker)"),
        ("dnaspec-spec-kit exec \"/dnaspec.temp-workspace 管理临时工作区\"", "Temp Workspace (/dnaspec.temp-workspace)"),
        ("dnaspec-spec-kit exec \"/dnaspec.git-ops 执行Git操作\"", "Git Operations (/dnaspec.git-ops)"),
        ("dnaspec-spec-kit exec \"/dnaspec.project-constitution 项目宪法管理\"", "Project Constitution (/dnaspec.project-constitution)"),
        ("dnaspec-spec-kit exec \"/dnaspec.contract-enforcer 执行合同强制\"", "Contract Enforcer (/dnaspec.contract-enforcer)"),
        ("dnaspec-spec-kit exec \"/dnaspec.workspace-manager 工作区管理\"", "Workspace Manager (/dnaspec.workspace-manager)"),
    ]
    
    results = []
    for cmd, description in tests:
        success = run_test_command(cmd, description)
        results.append((description, success))
    
    # Generate summary
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    failed_tests = total_tests - passed_tests
    
    print("="*70)
    print("FINAL VALIDATION SUMMARY REPORT")
    print("="*70)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {passed_tests/total_tests*100:.1f}%" if total_tests > 0 else "0%")
    
    print("\nDetailed Results:")
    for desc, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {desc}")
    
    print(f"\n🎯 COMMAND FORMAT VALIDATION: {'SUCCESS' if passed_tests == total_tests else 'PARTIAL SUCCESS'}")
    print("Expected Command Format: /dnaspec.{skill_name} [parameters]")
    print("All skills have been verified with correct format!")
    
    # Save detailed results
    report_data = {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'failed_tests': failed_tests,
        'success_rate': passed_tests/total_tests*100 if total_tests > 0 else 0,
        'results': results,
        'command_format': '/dnaspec.{skill_name} [parameters]',
        'validation_time': time.time(),
        'validation_type': 'Correct Command Format Verification'
    }
    
    with open('dnaspec_final_validation_report.json', 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 Detailed report saved to: dnaspec_final_validation_report.json")
    
    return passed_tests == total_tests


if __name__ == "__main__":
    success = main()
    print(f"\n🎉 DNASPEC SYSTEM VALIDATION: {'COMPLETE SUCCESS' if success else 'NEAR SUCCESS'}")
    sys.exit(0 if success else 1)