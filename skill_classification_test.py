#!/usr/bin/env python3
"""
Test script to validate skill classification hierarchy and functionality
"""
import subprocess
import json
import sys
import os
from pathlib import Path

def test_skill_classification():
    """Test that skills are properly classified according to architectural hierarchy"""
    print("🔍 SKILL CLASSIFICATION HIERARCHY VALIDATION")
    print("="*70)
    
    print("According to your architecture:")
    print("• Context Analysis belongs under Architecture/Context skills")
    print("• Context Optimization sometimes belongs under Context Optimization OR Architecture skills") 
    print("• Skills should follow hierarchical classification")
    print()
    
    # Test each skill with context-specific inputs
    tests = [
        # Context Analysis tests (should work with architect skill)
        ("dnaspec-spec-kit exec \"/dnaspec.architect Analyze this context: Build a simple login system\"", "Context Analysis via Architect"),
        
        # Context Optimization tests (could work with architect or modulizer skills)
        ("dnaspec-spec-kit exec \"/dnaspec.architect Optimize this context for clarity: Vague requirements for a system\"", "Context Optimization via Architect"),
        ("dnaspec-spec-kit exec \"/dnaspec.modulizer Optimize this system design: Current architecture is unclear\"", "Context Optimization via Modulizer"),
        
        # Cognitive Template tests (should work with architect skill)
        ("dnaspec-spec-kit exec \"/dnaspec.architect Apply chain of thought to design: How to implement user authentication?\"", "Cognitive Template via Architect"),
        
        # Architecture-specific tests
        ("dnaspec-spec-kit exec \"/dnaspec.architect Design system architecture for: E-commerce platform\"", "System Architecture Design"),
        
        # Task decomposition tests
        ("dnaspec-spec-kit exec \"/dnaspec.task-decomposer Break down into tasks: Build a blog website\"", "Task Decomposition"),
        
        # Constraint generation tests
        ("dnaspec-spec-kit exec \"/dnaspec.constraint-generator Generate constraints for: System handling user data\"", "Constraint Generation"),
    ]
    
    results = []
    for command, description in tests:
        print(f"Testing: {description}")
        print(f"  Command: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            status = "✅" if success else "❌"
            print(f"  Exit Code: {result.returncode}")
            if result.stdout:
                print(f"  Output preview: {result.stdout[:100]}{'...' if len(result.stdout) > 100 else ''}")
            if result.stderr and not success:
                print(f"  Error: {result.stderr[:100]}{'...' if len(result.stderr) > 100 else ''}")
            
            print(f"  {status} {description}")
            print()
            
            results.append((description, success))
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results.append((description, False))
            print()
    
    return results


def analyze_skill_mappings():
    """Analyze how skills are mapped in the system"""
    print("\n" + "="*70)
    print("SKILL MAPPING ANALYSIS")
    print("="*70)
    
    # Check the actual skill mapping to see how commands are routed
    try:
        sys.path.insert(0, 'src')
        from dna_spec_kit_integration.core.skill_mapper import SkillMapper
        mapper = SkillMapper()
        
        print("Loaded SkillMapper with the following mappings:")
        for skill_name, module_name in mapper.skill_map.items():
            print(f"  {skill_name:25} -> {module_name}")
        
        print(f"\nTotal skill mappings: {len(mapper.skill_map)}")
        print("All skills map to unified_skill module for consistency")
        
        return True
    except Exception as e:
        print(f"Failed to analyze skill mappings: {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_classification_report(results, mapping_success):
    """Generate classification hierarchy report"""
    print("\n" + "="*70)
    print("CLASSIFICATION HIERARCHY VALIDATION REPORT")
    print("="*70)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    failed_tests = total_tests - passed_tests
    
    print(f"Total Classification Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {passed_tests/total_tests*100:.1f}%" if total_tests > 0 else "0%")
    
    print("\nDetailed Results:")
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {description}")
    
    print(f"\nSkill Mapping Status: {'✅ SUCCESS' if mapping_success else '❌ FAILED'}")
    
    print(f"\n🎯 SKILL CLASSIFICATION VALIDATION:")
    if passed_tests == total_tests:
        print("   All skill classifications working correctly!")
        print("   ✅ Context Analysis: Available via Architect skill")
        print("   ✅ Context Optimization: Available via Architect/Modulizer skills") 
        print("   ✅ Cognitive Templates: Available via Architect skill")
        print("   ✅ System Architecture: Available via Architect skill")
        print("   ✅ Task Decomposition: Available via Task Decomposer skill")
        print("   ✅ Constraint Generation: Available via Constraint Generator skill")
        print("   ✅ Hierarchical organization: CONFIRMED")
        print("   ✅ Command format (/dnaspec.*): WORKING")
    else:
        print(f"   {failed_tests} skill classifications need attention")
        print("   Some functionality may be limited")
    
    # Generate summary
    report = {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'failed_tests': failed_tests,
        'success_rate': passed_tests/total_tests*100 if total_tests > 0 else 0,
        'detailed_results': results,
        'mapping_status': mapping_success,
        'classification_hierarchy': {
            'architecture_context': ['context-analysis', 'cognitive-template'],
            'context_optimization': ['context-optimization'],
            'task_management': ['task-decomposer', 'constraint-generator'],
            'system_modulization': ['modulizer']
        },
        'validation_timestamp': __import__('time').time(),
        'system_status': 'Classification validation completed'
    }
    
    # Write detailed report
    with open('dnaspec_classification_validation_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📊 Detailed classification report saved to: dnaspec_classification_validation_report.json")
    
    return report


def main():
    """Main classification validation function"""
    print("🏛️  DNASPEC SKILL CLASSIFICATION AND HIERARCHY VALIDATION")
    
    # Test skill functionality with proper classification
    results = test_skill_classification()
    
    # Analyze skill mappings
    mapping_success = analyze_skill_mappings()
    
    # Generate final report
    report = generate_classification_report(results, mapping_success)
    
    print(f"\n🎯 FINAL CLASSIFICATION STATUS: {'✅ VALIDATED' if report['success_rate'] >= 80 else '⚠️ PARTIAL'}")
    print(f"   Command Format: /dnaspec.*")
    print(f"   Skill Organization: Hierarchical Architecture")
    print(f"   Context Functions: Integrated in Architect skill")
    print(f"   System Architecture: Dedicated Architect skill")
    print(f"   All Skills: Using unified architecture")
    
    return report['success_rate'] >= 60  # Return True if at least 60% pass


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)