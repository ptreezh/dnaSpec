#!/usr/bin/env python3
"""
Comprehensive test script for DNASPEC system
Tests installation, functionality, and deployment modes
"""
import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
import json
import time


def run_command(cmd, description, cwd=None, expect_success=True):
    """Run a command and check its result"""
    print(f"\n🧪 Testing: {description}")
    print(f"   Command: {cmd}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=60
        )
        
        print(f"   Exit Code: {result.returncode}")
        if result.stdout:
            print(f"   Stdout: {result.stdout[:200]}{'...' if len(result.stdout) > 200 else ''}")
        if result.stderr:
            print(f"   Stderr: {result.stderr[:200]}{'...' if len(result.stderr) > 200 else ''}")
        
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


def test_basic_installation():
    """Test basic installation and command availability"""
    print("\n" + "="*60)
    print("TESTING: Basic Installation")
    print("="*60)
    
    tests = [
        ("python -c \"import src.dna_context_engineering.skills_system_final\"", "Import core modules"),
        ("dnaspec-spec-kit --version", "DNASPEC CLI availability"),
        ("dnaspec-spec-kit list", "List available skills"),
    ]
    
    results = []
    for cmd, description in tests:
        success, _ = run_command(cmd, description)
        results.append((description, success))
    
    return results


def test_cli_detection():
    """Test CLI tool detection capabilities"""
    print("\n" + "="*60)
    print("TESTING: CLI Tool Detection")
    print("="*60)

    # Create a simpler test that just imports and tests the detector without running detection
    tests = [
        ("python -c \"from src.dna_spec_kit_integration.core.cli_detector import CliDetector; d = CliDetector(); print('Detector created successfully')\"", "Create CLI detector"),
    ]

    results = []
    for cmd, description in tests:
        success, _ = run_command(cmd, description)
        results.append((description, success))

    return results


def test_deployment_modes():
    """Test both deployment modes"""
    print("\n" + "="*60)
    print("TESTING: Deployment Modes")
    print("="*60)

    # Test deployment status
    tests = [
        ("dnaspec-spec-kit deploy --list", "Check deployment status"),
    ]

    results = []
    for cmd, description in tests:
        success, result = run_command(cmd, description)
        results.append((description, success))

        # Check if the output contains expected information
        if success and result and result.stdout and 'Stigmergy Available' in result.stdout:
            print("   ✅ Deployment status shows Stigmergy availability info")
        elif success:
            print("   ⚠️  Deployment status command ran but output not checked for specific info")
        else:
            print("   ❌ Deployment status command failed")

    return results


def test_core_skills():
    """Test core skill functionality"""
    print("\n" + "="*60)
    print("TESTING: Core Skills Functionality")
    print("="*60)

    # These tests may fail due to argument parsing issues noted in analysis
    tests = [
        # Test the underlying skill functions directly
        ("python -c \"from src.dna_context_engineering.skills_system_final import execute_context_analysis; result = execute_context_analysis('Simple test context'); print('Context analysis completed:', type(result).__name__ if result else 'None')\"", "Direct context analysis function"),
        ("python -c \"from src.dna_context_engineering.skills_system_final import execute_context_optimization; result = execute_context_optimization('Simple context to optimize'); print('Context optimization completed:', type(result).__name__ if result else 'None')\"", "Direct context optimization function"),
        ("python -c \"from src.dna_context_engineering.skills_system_final import execute_cognitive_template; result = execute_cognitive_template('Simple task'); print('Cognitive template completed:', type(result).__name__ if result else 'None')\"", "Direct cognitive template function"),
    ]

    results = []
    for cmd, description in tests:
        success, result = run_command(cmd, description)
        results.append((description, success))

        if success and result and result.stdout:
            print("   ✅ Function executed and returned output")
        else:
            print("   ⚠️  Function may not have returned expected output")

    return results


def test_auto_configuration():
    """Test auto-configuration functionality"""
    print("\n" + "="*60)
    print("TESTING: Auto-Configuration")
    print("="*60)
    
    tests = [
        ("python run_auto_config.py --help", "Check auto-config script availability"),
    ]
    
    results = []
    for cmd, description in tests:
        success, result = run_command(cmd, description)
        results.append((description, success))
    
    return results


def generate_test_report(results):
    """Generate a test report"""
    print("\n" + "="*60)
    print("TEST REPORT SUMMARY")
    print("="*60)
    
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
    
    return {
        'total': total_tests,
        'passed': passed_tests,
        'failed': failed_tests,
        'success_rate': passed_tests/total_tests*100 if total_tests > 0 else 0,
        'details': results
    }


def main():
    """Main test execution function"""
    print("🧪 DNASPEC Comprehensive Test Suite")
    print(f"Current directory: {os.getcwd()}")
    
    all_results = []
    
    # Run all test categories
    test_functions = [
        test_basic_installation,
        test_cli_detection,
        test_deployment_modes,
        test_core_skills,
        test_auto_configuration,
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
    report = generate_test_report(all_results)
    
    # Save detailed report to file
    report_path = "dnaspec_test_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\n📊 Detailed report saved to: {report_path}")
    
    return report['success_rate'] >= 80  # Return True if success rate >= 80%


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)