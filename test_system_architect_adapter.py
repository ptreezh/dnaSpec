#!/usr/bin/env python3
"""
Test script for System Architect Skill adapter
"""
import sys
import os

# Add the adapter path to sys.path
sys.path.insert(0, 'spec-kit/skills/dna-system-architect/scripts')

try:
    from system_architect_designer import DNASPECSystemArchitect
    
    print("Testing System Architect Skill Adapter...")
    
    # Test instantiation
    architect = DNASPECSystemArchitect()
    print("✅ DNASPECSystemArchitect instantiation successful")
    
    # Test basic methods
    result = architect.identify_architecture_type("Build a microservices e-commerce platform")
    print(f"✅ identify_architecture_type: {result.value}")
    
    # Test main method
    design = architect.generate_architecture_design("Simple web application")
    print(f"✅ generate_architecture_design:")
    print(f"   Architecture Type: {design.get('architecture_type')}")
    print(f"   Tech Stack: {design.get('recommended_tech_stack')}")
    print(f"   Modules: {len(design.get('modules', []))}")
    
    print("\n🎉 System Architect Skill Adapter working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()