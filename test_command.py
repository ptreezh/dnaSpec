#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from dna_spec_kit_integration.core.command_parser import CommandParser

def test_command_parsing():
    parser = CommandParser()
    test_commands = [
        "/speckit.dnaspec.architect Design a simple todo application",
        "architect Design a simple todo application",
        "speckit.dnaspec.architect Design a simple todo application"
    ]

    for cmd in test_commands:
        print(f"Testing command: {cmd}")
        result = parser.parse(cmd)
        print(f"Result: {result}")
        print("-" * 50)

if __name__ == "__main__":
    test_command_parsing()