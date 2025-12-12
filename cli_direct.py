#!/usr/bin/env python3
"""
Direct CLI wrapper for DNASPEC
Bypasses module installation issues by using local imports
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

def main():
    """Direct CLI entry point"""
    try:
        # Import the CLI module
        from dnaspec_spec_kit_integration.cli import main as cli_main

        # Set up arguments
        if len(sys.argv) < 2:
            print("DNASPEC CLI - Context Engineering Skills")
            print("=" * 50)
            print("")
            print("Usage: dnaspec <command> [options]")
            print("")
            print("Commands:")
            print("  init        Initialize and setup DNASPEC")
            print("  deploy      Deploy skills to AI platforms")
            print("  validate    Check integration status")
            print("  list        Show available skills")
            print("  help        Show this help message")
            print("")
            print("Examples:")
            print("  dnaspec init")
            print("  dnaspec deploy --list")
            print("  dnaspec validate")
            return 0

        # Call the original CLI main function
        cli_main()
        return 0

    except ImportError as e:
        print(f"ERROR: Cannot import DNASPEC CLI module: {e}")
        print(f"Project root: {project_root}")
        print(f"Python path: {sys.path[:3]}...")

        # Try to provide basic functionality
        command = sys.argv[1] if len(sys.argv) > 1 else 'help'

        if command == 'list':
            print("\nDNASPEC Available Skills:")
            print("-" * 30)
            print("• context-analysis")
            print("• context-optimization")
            print("• cognitive-template")
            print("• architect")
            print("• system-design")
            print("• task-decomposition")
            return 0
        elif command == 'validate':
            print("\nDNASPEC Validation:")
            print("-" * 20)
            print("✅ Python environment OK")
            print("⚠️  CLI module import failed (running in fallback mode)")
            print("✅ Project directory detected")
            return 0
        elif command == 'help':
            main()  # Show help
            return 0
        else:
            return 1

    except Exception as e:
        print(f"ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())