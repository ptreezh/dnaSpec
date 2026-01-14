#!/usr/bin/env python3
"""
Detailed test script to validate each DNASPEC skill functionality
and constitutional/contractual systems
"""
import os
import sys
import subprocess
import json
import time
from pathlib import Path


def run_command(cmd, description, expect_success=True):
    """Run a command and check its result"""
    print(f"\n🧪 Testing: {description}")
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
            print(f"   Stdout preview: {result.stdout[:200]}{'...' if len(result.stdout) > 200 else ''}")
        if result.stderr:
            print(f"   Stderr preview: {result.stderr[:200]}{'...' if len(result.stderr) > 200 else ''}")
        
        success = (result.returncode == 0) == expect_success
        if not success:
            print(f"   ❌ FAIL: Expected {'success' if expect_success else 'failure'}, got {'success' if result.returncode == 0 else 'failure'}")
        else:
            print(f"   ✅ PASS")
        
        return success, result
    except subprocess.TimeoutExpired:
        print(f"   ❌ FAIL: Command timed out")
        return False, None
    except Exception as e:
        print(f"   ❌ FAIL: Exception occurred: {str(e)}")
        return False, None


def test_context_skills():
    """Test context analysis, optimization, and cognitive template skills"""
    print("\n" + "="*70)
    print("TESTING: Context Engineering Skills")
    print("="*70)
    
    tests = [
        ("python -c \"from src.dna_context_engineering.skills_system_final import execute_context_analysis; result = execute_context_analysis('Simple test context for analysis'); print('Context analysis result type:', type(result).__name__)\"", "Context Analysis Function"),
        ("python -c \"from src.dna_context_engineering.skills_system_final import execute_context_optimization; result = execute_context_optimization('Simple context to optimize'); print('Context optimization result type:', type(result).__name__)\"", "Context Optimization Function"),
        ("python -c \"from src.dna_context_engineering.skills_system_final import execute_cognitive_template; result = execute_cognitive_template('Simple task for cognitive template'); print('Cognitive template result type:', type(result).__name__)\"", "Cognitive Template Function"),
    ]
    
    results = []
    for cmd, description in tests:
        success, _ = run_command(cmd, description)
        results.append((description, success))
    
    return results


def test_agent_skills():
    """Test agentic system skills"""
    print("\n" + "="*70)
    print("TESTING: Agentic System Skills")
    print("="*70)
    
    tests = [
        ("python -c \"from src.agent_creator_skill import AgentCreatorSkill; skill = AgentCreatorSkill(); result = skill.process_request('Helpful assistant', {}); print('Agent Creator success:', result.status.name)\"", "Agent Creator Skill"),
        ("python -c \"from src.task_decomposer_skill import TaskDecomposerSkill; skill = TaskDecomposerSkill(); result = skill.process_request('Build a simple web app', {}); print('Task Decomposer success:', result.status.name)\"", "Task Decomposer Skill"),
        ("python -c \"from src.constraint_generator_skill import ConstraintGeneratorSkill; skill = ConstraintGeneratorSkill(); result = skill.process_request('System needs to handle user data', {}); print('Constraint Generator success:', result.status.name)\"", "Constraint Generator Skill"),
    ]
    
    results = []
    for cmd, description in tests:
        success, _ = run_command(cmd, description)
        results.append((description, success))
    
    return results


def test_constitutional_systems():
    """Test constitutional and contractual systems"""
    print("\n" + "="*70)
    print("TESTING: Constitutional and Contractual Systems")
    print("="*70)
    
    tests = [
        ("python -c \"from src.dna_spec_kit_integration.core.constitutional_base_skill import ConstitutionalBaseSkill; print('Constitutional base skill importable')\"", "Constitutional Base Skill Import"),
        ("python -c \"from src.dna_spec_kit_integration.core.constitutional_enforcer import ConstitutionalEnforcer; print('Constitutional enforcer importable')\"", "Constitutional Enforcer Import"),
        ("python -c \"from src.dna_spec_kit_integration.core.coordination_contract_enforcer import CoordinationContractEnforcer; print('Coordination contract enforcer importable')\"", "Coordination Contract Enforcer Import"),
        ("python -c \"from src.dna_spec_kit_integration.core.coordination_contract_checker import CoordinationContractChecker; print('Coordination contract checker importable')\"", "Coordination Contract Checker Import"),
        ("dir *.md | findstr CONTRACT", "Check for CONTRACT files"),
        ("dir *.yaml | findstr CONTRACT", "Check for CONTRACT YAML files"),
    ]
    
    results = []
    for cmd, description in tests:
        success, result = run_command(cmd, description)
        results.append((description, success))
    
    return results


def test_cli_integration_skills():
    """Test CLI integration for each skill"""
    print("\n" + "="*70)
    print("TESTING: CLI Integration for Skills")
    print("="*70)
    
    tests = [
        ("dnaspec-spec-kit list", "List available skills"),
        ("python -c \"from src.dna_spec_kit_integration.cli_extension_handler import get_available_skills; skills = get_available_skills(); print(f'Available skills: {skills[\\'total_count\\']}'); print(f'Sample skills: {[s[\\'name\\'] for s in skills[\\'skills\\'][:3]]}')\"", "Get available skills via handler"),
    ]
    
    results = []
    for cmd, description in tests:
        success, result = run_command(cmd, description)
        results.append((description, success))
        
        if success and result and result.stdout:
            # Check if skills are properly configured
            if "context-analysis" in result.stdout or "architect" in result.stdout:
                print("   ✅ Skills are properly listed")
            else:
                print("   ⚠️  No skills found in output")
    
    return results


def test_specific_skill_commands():
    """Test specific skill commands where possible"""
    print("\n" + "="*70)
    print("TESTING: Specific Skill Commands")
    print("="*70)
    
    # Note: We might not be able to test exec commands directly due to argument parsing
    # Instead, we'll test skill functions directly
    tests = [
        ("python -c \"from src.dna_context_engineering.core_skill import SkillsManager, GenericAPIClient, TemplateRegistry; client = GenericAPIClient(); registry = TemplateRegistry(); manager = SkillsManager(client, registry); result = manager.execute_skill('context-analysis', 'Test context'); print('Skills manager context analysis:', result.success)\"", "Skills Manager Context Analysis"),
        ("python -c \"from src.dna_context_engineering.core_skill import SkillsManager, GenericAPIClient, TemplateRegistry; client = GenericAPIClient(); registry = TemplateRegistry(); manager = SkillsManager(client, registry); result = manager.execute_skill('context-optimization', 'Test context to optimize'); print('Skills manager context optimization:', result.success)\"", "Skills Manager Context Optimization"),
        ("python -c \"from src.dna_context_engineering.core_skill import SkillsManager, GenericAPIClient, TemplateRegistry; client = GenericAPIClient(); registry = TemplateRegistry(); manager = SkillsManager(client, registry); result = manager.execute_skill('cognitive-template', 'Test cognitive template'); print('Skills manager cognitive template:', result.success)\"", "Skills Manager Cognitive Template"),
    ]
    
    results = []
    for cmd, description in tests:
        success, result = run_command(cmd, description)
        results.append((description, success))
        
        if success and result and result.stdout:
            if "True" in result.stdout:
                print("   ✅ Skill executed successfully")
            else:
                print("   ⚠️  Skill may not have executed successfully")
    
    return results


def test_coordination_contracts():
    """Test coordination contract systems"""
    print("\n" + "="*70)
    print("TESTING: Coordination Contract Systems")
    print("="*70)
    
    tests = [
        ("python -c \"from src.dna_spec_kit_integration.core.coordination_contract_hooks import CoordinationContractHooks; hooks = CoordinationContractHooks(); print('Coordination contract hooks importable and instantiable')\"", "Coordination Contract Hooks"),
        ("python -c \"from src.dna_spec_kit_integration.core.cognitive_coordination_center import CognitiveCoordinationCenter; center = CognitiveCoordinationCenter(); print('Cognitive coordination center importable and instantiable')\"", "Cognitive Coordination Center"),
        ("dir *.yaml | findstr CONTRACT", "Look for contract YAML files"),
        ("dir *.yaml | findstr coordination", "Look for coordination YAML files"),
    ]
    
    results = []
    for cmd, description in tests:
        success, result = run_command(cmd, description)
        results.append((description, success))
    
    return results


def generate_detailed_report(results):
    """Generate a detailed test report"""
    print("\n" + "="*70)
    print("DETAILED SKILL FUNCTIONALITY REPORT")
    print("="*70)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    failed_tests = total_tests - passed_tests
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {passed_tests/total_tests*100:.1f}%" if total_tests > 0 else "Success Rate: 0%")
    
    print("\nDetailed Results:")
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {description}")
    
    # Generate detailed summary
    summary = {
        'total': total_tests,
        'passed': passed_tests,
        'failed': failed_tests,
        'success_rate': passed_tests/total_tests*100 if total_tests > 0 else 0,
        'details': results,
        'timestamp': time.time(),
        'categories': {
            'context_skills': 'Core Context Engineering Skills',
            'agent_skills': 'Agentic System Skills', 
            'constitutional': 'Constitutional and Contractual Systems',
            'cli_integration': 'CLI Integration',
            'specific_commands': 'Specific Skill Commands',
            'coordination_contracts': 'Coordination Contract Systems'
        }
    }
    
    return summary


def main():
    """Main test execution function"""
    print("🧪 DNASPEC Skill Functionality and Constitutional System Test Suite")
    print(f"Current directory: {os.getcwd()}")
    
    all_results = []
    
    # Run all test categories
    test_functions = [
        test_context_skills,
        test_agent_skills,
        test_constitutional_systems,
        test_cli_integration_skills,
        test_specific_skill_commands,
        test_coordination_contracts,
    ]
    
    for test_func in test_functions:
        try:
            results = test_func()
            all_results.extend(results)
        except Exception as e:
            print(f"❌ Error running {test_func.__name__}: {str(e)}")
            # Add a failure result for this test category
            all_results.append((f"{test_func.__name__} execution", False))
    
    # Generate final report
    report = generate_detailed_report(all_results)
    
    # Save detailed report to file
    report_path = "dnaspec_skill_functionality_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\n📊 Skill functionality report saved to: {report_path}")
    
    # Summary for CI/CD
    print(f"\n🎯 DNASPEC Skill Validation Summary:")
    print(f"   Overall Success Rate: {report['success_rate']:.1f}%")
    print(f"   Tests Passed: {report['passed']}/{report['total']}")
    
    # Success criteria: at least 80% success rate
    success = report['success_rate'] >= 80
    if success:
        print("   🎉 DNASPEC skill functionality validation PASSED!")
    else:
        print("   ⚠️  DNASPEC skill functionality validation needs attention.")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)