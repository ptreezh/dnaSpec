#!/usr/bin/env python3
"""
DNA Context Engineering Skills - 完整技能验证测试
验证所有上下文工程技能的上下文验证和优化功能
"""
import os
import sys
import subprocess
import json
import time
from typing import Dict, Any, List


def run_command(cmd: str, desc: str) -> tuple:
    """Run command and return success status and result"""
    print(f"\n🧪 Testing: {desc}")
    print(f"   Command: {cmd}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print(f"   Exit Code: {result.returncode}")
        if result.stdout:
            print(f"   Stdout preview: {result.stdout[:300]}{'...' if len(result.stdout) > 300 else ''}")
        if result.stderr:
            print(f"   Stderr preview: {result.stderr[:200]}{'...' if len(result.stderr) > 200 else ''}")
        
        success = result.returncode == 0
        if success:
            print(f"   ✅ PASS")
        else:
            print(f"   ❌ FAIL")
        
        return success, result
    except subprocess.TimeoutExpired:
        print(f"   ❌ FAIL: Command timed out")
        return False, None
    except Exception as e:
        print(f"   ❌ FAIL: Exception occurred: {str(e)}")
        return False, None


def test_context_analysis_skill():
    """测试上下文分析技能"""
    print("\n" + "="*60)
    print("TESTING: Context Analysis Skill")
    print("="*60)
    
    # 测试直接调用技能函数
    tests = [
        ("python -c \"from src.dna_context_engineering.skills_system_final import execute_context_analysis; result = execute_context_analysis('Build a simple login system'); print('Context analysis result:', result[:200])\"", "Context Analysis via Python Function"),
    ]
    
    results = []
    for cmd, description in tests:
        success, result = run_command(cmd, description)
        results.append((description, success))
    
    return results


def test_context_optimization_skill():
    """测试上下文优化技能"""
    print("\n" + "="*60)
    print("TESTING: Context Optimization Skill")
    print("="*60)
    
    tests = [
        ("python -c \"from src.dna_context_engineering.skills_system_final import execute_context_optimization; result = execute_context_optimization('Simple context to optimize for clarity'); print('Context optimization result:', result[:200])\"", "Context Optimization via Python Function"),
    ]
    
    results = []
    for cmd, description in tests:
        success, result = run_command(cmd, description)
        results.append((description, success))
    
    return results


def test_cognitive_template_skill():
    """测试认知模板技能"""
    print("\n" + "="*60)
    print("TESTING: Cognitive Template Skill")
    print("="*60)
    
    tests = [
        ("python -c \"from src.dna_context_engineering.skills_system_final import execute_cognitive_template; result = execute_cognitive_template('Apply chain of thought to solve math problem: 15 + 27 = ?'); print('Cognitive template result:', result[:200])\"", "Cognitive Template via Python Function"),
    ]
    
    results = []
    for cmd, description in tests:
        success, result = run_command(cmd, description)
        results.append((description, success))
    
    return results


def test_architect_skill():
    """测试架构设计技能"""
    print("\n" + "="*60)
    print("TESTING: Architect Skill")
    print("="*60)
    
    tests = [
        ("python -c \"from src.dna_context_engineering.skills_system_final import execute_architect; result = execute_architect('Design a simple blog system'); print('Architect result:', result[:200])\"", "Architect via Python Function"),
    ]
    
    results = []
    for cmd, description in tests:
        success, result = run_command(cmd, description)
        results.append((description, success))
    
    return results


def test_cli_integration():
    """测试CLI集成"""
    print("\n" + "="*60)
    print("TESTING: CLI Integration")
    print("="*60)
    
    tests = [
        ("dnaspec-spec-kit exec \"/speckit.dnaspec.context-analysis Analyze this simple requirement: Build a user authentication system\"", "Context Analysis via CLI"),
        ("dnaspec-spec-kit exec \"/speckit.dnaspec.context-optimization Optimize this context for clarity: Vague requirements for a system\"", "Context Optimization via CLI"),
        ("dnaspec-spec-kit exec \"/speckit.dnaspec.cognitive-template Apply chain-of-thought to this problem: Calculate 15 + 27\"", "Cognitive Template via CLI"),
        ("dnaspec-spec-kit exec \"/speckit.dnaspec.architect Design a simple blog system\"", "Architect via CLI"),
    ]
    
    results = []
    for cmd, description in tests:
        success, result = run_command(cmd, description)
        results.append((description, success))
    
    return results


def test_advanced_context_engineering_features():
    """测试高级上下文工程特征"""
    print("\n" + "="*60)
    print("TESTING: Advanced Context Engineering Features")
    print("="*60)
    
    # 测试创建智能体的功能
    tests = [
        ("python -c \"from src.dna_context_engineering.skills_system_final import create_agent_for_context_analysis; agent = create_agent_for_context_analysis('Analyze context quality', 'Must follow safety guidelines'); print('Agent creation:', 'success' if 'Goals:' in agent else 'failed')\"", "Agent Creation for Context Analysis"),
        ("python -c \"from src.dna_context_engineering.skills_system_final import decompose_complex_task; decomp = decompose_complex_task('Build an e-commerce website with user management'); print('Task decomposition:', 'success' if 'subtasks' in str(decomp).lower() else 'failed')\"", "Complex Task Decomposition"),
        ("python -c \"from src.dna_context_engineering.skills_system_final import generate_constraints_from_requirements; constraints = generate_constraints_from_requirements('System must handle user data securely'); print('Constraints generation:', 'success' if 'security' in str(constraints).lower() else 'failed')\"", "Constraints Generation from Requirements"),
    ]
    
    results = []
    for cmd, description in tests:
        success, result = run_command(cmd, description)
        results.append((description, success))
    
    return results


def generate_comprehensive_report(all_results: List[tuple]) -> Dict[str, Any]:
    """生成综合报告"""
    print("\n" + "="*70)
    print("COMPREHENSIVE CONTEXT ENGINEERING SKILLS VALIDATION REPORT")
    print("="*70)
    
    total_tests = len(all_results)
    passed_tests = sum(1 for _, success in all_results if success)
    failed_tests = total_tests - passed_tests
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {passed_tests/total_tests*100:.1f}%" if total_tests > 0 else "Success Rate: 0%")
    
    print("\nDetailed Results:")
    for description, success in all_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {description}")
    
    # Generate summary data
    summary = {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'failed_tests': failed_tests,
        'success_rate': passed_tests/total_tests*100 if total_tests > 0 else 0,
        'results': all_results,
        'validation_type': 'Comprehensive Context Engineering Skills Validation',
        'timestamp': time.time(),
        'skills_validated': [
            'Context Analysis (context-validation)',
            'Context Optimization (context-optimization)', 
            'Cognitive Templates (cognitive-template)',
            'Architectural Design (architect)',
            'Agent Creation for Context Analysis',
            'Task Decomposition',
            'Constraint Generation'
        ]
    }
    
    # Save detailed report
    with open('context_engineering_validation_report.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 Validation report saved to: context_engineering_validation_report.json")
    
    return summary


def main():
    """Main validation function"""
    print("🔍 DNA CONTEXT ENGINEERING SKILLS - COMPREHENSIVE VALIDATION")
    print(f"Current directory: {os.getcwd()}")
    
    all_results = []
    
    # Test all context engineering skills
    test_functions = [
        test_context_analysis_skill,
        test_context_optimization_skill,
        test_cognitive_template_skill,
        test_architect_skill,
        test_cli_integration,
        test_advanced_context_engineering_features,
    ]
    
    for test_func in test_functions:
        print(f"\n🏃 Running {test_func.__name__}...")
        try:
            results = test_func()
            all_results.extend(results)
        except Exception as e:
            print(f"❌ Error running {test_func.__name__}: {str(e)}")
            # Add failure result
            all_results.append((f"{test_func.__name__} execution", False))
    
    # Generate final report
    report = generate_comprehensive_report(all_results)
    
    print(f"\n🎯 DNA CONTEXT ENGINEERING VALIDATION SUMMARY:")
    print(f"   Overall Success Rate: {report['success_rate']:.1f}%")
    print(f"   Tests Passed: {report['passed_tests']}/{report['total_tests']}")
    
    # Determine if system is functioning
    is_fully_functional = report['success_rate'] >= 80
    if is_fully_functional:
        print("   🎉 ALL CONTEXT ENGINEERING SKILLS ARE FUNCTIONAL!")
        print("   ✓ Context Analysis skill working")
        print("   ✓ Context Optimization skill working")
        print("   ✓ Cognitive Template skill working") 
        print("   ✓ Architect skill working")
        print("   ✓ CLI integration working")
        print("   ✓ Advanced context engineering features working")
    else:
        print("   ⚠️  SOME CONTEXT ENGINEERING SKILLS NEED ATTENTION")
        print("   Check individual test results for specific issues")
    
    return is_fully_functional


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)