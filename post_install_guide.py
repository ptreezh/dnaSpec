#!/usr/bin/env python3
"""
Post-installation Guide - DSGS系统安装后指引
为用户提供清晰的操作说明和功能介绍
"""
import sys
import os
import platform
from typing import Dict, Any

def display_post_installation_guide():
    """
    显示安装后指引
    """
    print("=" * 80)
    print("🎉 DNASPEC Context Engineering Skills - POST-INSTALLATION GUIDE")
    print("=" * 80)
    print()
    print("Thank you for installing DNASPEC (Dynamic Specification Growth System)!")
    print()
    print("DNASPEC is a professional context engineering toolkit that enhances your AI-assisted")
    print("development experience by providing advanced context analysis, optimization, and")  
    print("cognitive template application capabilities.")
    print()
    print("FEATURE ADVANTAGES:")
    print("  ✓ Context Quality Analysis: 5-dimensional assessment (clarity, relevance,")
    print("                               completeness, consistency, efficiency)")  
    print("  ✓ Context Optimization: AI-driven improvements based on specific goals")
    print("  ✓ Cognitive Templates: Professional thinking frameworks (CoT, Verification, etc.)")
    print("  ✓ Agentic Design: System architecture and task decomposition skills")
    print("  ✓ Safety Workflows: Secure AI interaction with temporary workspaces")
    print()
    print("GETTING STARTED - Next Steps:")
    print()
    print("  1. Run automatic configuration:")
    print("     dnaspec init")
    print()
    print("  2. Verify detected AI tools:")
    print("     dnaspec validate")
    print()
    print("  3. Deploy skills to AI platforms (if you have AI CLI tools installed):")
    print("     dnaspec deploy")
    print()
    print("USAGE EXAMPLES in AI CLI Tools:")
    print("  /speckit.dnaspec.context-analysis 'Analyze this requirement: ...'")
    print("  /speckit.dnaspec.context-optimization 'Optimize this context: ...'")
    print("  /speckit.dnaspec.cognitive-template 'Apply template to: ...' template=verification")
    print("  /speckit.dnaspec.architect 'Design system for: ...'")
    print()
    print("COMMAND REFERENCE:")
    print("  dnaspec list              - Show all available skills")
    print("  dnaspec deploy --list     - List detected AI platforms")  
    print("  dnaspec validate          - Check AI tool integration status")
    print("  dnaspec help              - Show help information")
    print()
    print("COMPATIBLE AI TOOLS:")
    print("  - Claude Desktop CLI (recommended)")
    print("  - Qwen CLI")
    print("  - Gemini CLI")
    print("  - Cursor IDE")
    print("  - GitHub Copilot CLI")
    print()
    print("IMPORTANT NOTES:")
    print("  - Skills will be available in supported AI CLI tools after deployment")
    print("  - All tools are locally installed with no external dependencies")
    print("  - Your privacy is protected - no data leaves your system")
    print()
    print("For support, visit: https://github.com/ptreezh/dnaSpec")
    print("Report issues at: https://github.com/ptreezh/dnaSpec/issues")
    print()
    print("=" * 80)

def main():
    """主入口"""
    if len(sys.argv) > 1 and sys.argv[1] == 'postinstall':
        # 如果是安装后自动调用
        display_post_installation_guide()
        return 0
    else:
        # 直接调用显示指引
        display_post_installation_guide()
        return 0

if __name__ == "__main__":
    sys.exit(main())