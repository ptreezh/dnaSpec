import sys
print("=== Debug DNASPEC import ===")
print("Python paths:")
for i, p in enumerate(sys.path[:10]):
    print(f"  {i}: {p}")

print("\nTrying imports step by step...")
try:
    print("1. Importing dna_context_engineering...")
    import dna_context_engineering
    print("   SUCCESS")

    print("2. Importing dna_context_engineering.skills_system_final...")
    from dna_context_engineering import skills_system_final
    print("   SUCCESS")

    print("3. Accessing execute_architect...")
    execute_func = skills_system_final.execute_architect
    print("   SUCCESS")

    print("4. Testing execution...")
    result = execute_func("test task")
    print(f"   SUCCESS: {result[:50]}...")

except ImportError as e:
    print(f"   IMPORT ERROR: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"   EXECUTION ERROR: {e}")
    import traceback
    traceback.print_exc()