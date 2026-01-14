"""
Reality Validator Skill - Validates actual functionality of implementations
"""
from typing import Dict, Any
import tempfile
import subprocess
import os
import sys
import ast
from pathlib import Path

def execute(args: Dict[str, Any]) -> str:
    """
    Validate actual functionality of AI-generated implementations
    """
    implementation_code = args.get("code", "")
    claimed_functionality = args.get("functionality_description", "")
    requirements = args.get("requirements", "")
    test_environment = args.get("test_environment", None)
    
    if not implementation_code.strip():
        return "❌ Reality Validator: No implementation code provided"
    
    if not claimed_functionality.strip():
        return "❌ Reality Validator: No functionality description provided"
    
    if not test_environment:
        # Create temporary test environment
        test_environment = create_temp_test_environment()
    
    try:
        # Validate syntax first
        try:
            ast.parse(implementation_code)
            syntax_valid = True
        except SyntaxError as e:
            syntax_valid = False
            syntax_error = str(e)
        
        if not syntax_valid:
            return f"❌ Reality Validator: Syntax Error in implementation - {syntax_error}"
        
        # Execute the code to test functionality
        execution_result = execute_implementation_code(implementation_code, test_environment)
        
        # Generate reality report
        reality_report = compare_claims_vs_reality(
            claimed_functionality, 
            execution_result, 
            implementation_code
        )
        
        # Identify discrepancies
        discrepancies = identify_functionality_gaps(reality_report)
        
        return format_reality_validation_report(
            execution_result, 
            reality_report, 
            discrepancies
        )
    except Exception as e:
        return f"❌ Reality Validator: Error during validation: {str(e)}"
    finally:
        if not args.get("test_environment"):  # Only cleanup if we created it
            cleanup_test_environment(test_environment)

def execute_implementation_code(code: str, env_path: str) -> dict:
    """Execute the implementation code in a safe environment"""
    # Create a temporary Python file with the code
    test_file = Path(env_path) / "test_implementation.py"
    
    # Write the implementation code to file
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(code)
        f.write("\n\n# Test execution\n")
        f.write("if __name__ == '__main__':\n")
        f.write("    print('Code executed successfully')\n")
    
    # Try to execute the code
    try:
        # Execute in a subprocess to isolate from main process
        result = subprocess.run([
            sys.executable, str(test_file)
        ], capture_output=True, text=True, timeout=10, cwd=env_path)
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'return_code': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Test execution timed out'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def compare_claims_vs_reality(claimed: str, actual_results: dict, implementation: str) -> dict:
    """Compare claimed functionality with actual test results"""
    return {
        'claimed': claimed,
        'actual_success': actual_results.get('success', False),
        'actual_output': actual_results.get('stdout', ''),
        'actual_errors': actual_results.get('stderr', ''),
        'implementation': implementation
    }

def identify_functionality_gaps(reality_report: dict) -> list:
    """Identify gaps between claimed and actual functionality"""
    gaps = []
    
    if not reality_report.get('actual_success', False):
        gaps.append("Implementation fails to execute properly")
    
    return gaps

def format_reality_validation_report(results: dict, report: dict, gaps: list) -> str:
    """Format the reality validation report"""
    output = "🔍 Reality Validator Report\n"
    output += "=" * 40 + "\n\n"
    
    output += f"Claimed Functionality: {report['claimed']}\n\n"
    
    if report['actual_success']:
        output += "✅ Implementation executes successfully\n\n"
    else:
        output += "❌ Implementation has execution issues\n\n"
    
    if 'actual_output' in report and report['actual_output']:
        output += f"Execution Output:\n{report['actual_output']}\n\n"
    
    if 'actual_errors' in report and report['actual_errors']:
        output += f"Execution Errors:\n{report['actual_errors']}\n\n"
    
    if gaps:
        output += "⚠️  Gaps Identified:\n"
        for gap in gaps:
            output += f"  • {gap}\n\n"
    else:
        output += "✅ No major gaps identified between claimed and actual functionality\n\n"
    
    return output

def create_temp_test_environment() -> str:
    """Create a safe temporary environment for testing"""
    temp_dir = tempfile.mkdtemp()
    return temp_dir

def cleanup_test_environment(env_path: str):
    """Clean up the test environment"""
    import shutil
    shutil.rmtree(env_path, ignore_errors=True)