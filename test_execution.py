#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from dna_spec_kit_integration.core.command_handler import CommandHandler
from dna_spec_kit_integration.core.skill_executor import SkillExecutor
from dna_spec_kit_integration.core.python_bridge import PythonBridge
from dna_spec_kit_integration.core.skill_mapper import SkillMapper

def test_execution():
    # Create components
    python_bridge = PythonBridge()
    skill_mapper = SkillMapper()
    skill_executor = SkillExecutor(python_bridge, skill_mapper)
    command_handler = CommandHandler(None, skill_executor)

    # Test command
    command = "/speckit.dnaspec.architect Design a simple todo application"
    print(f"Testing command: {command}")

    result = command_handler.handle_command(command)
    print(f"Result: {result}")

if __name__ == "__main__":
    test_execution()