import sys, os
sys.path.insert(0, os.path.join('D:', 'DAIP', 'dnaSpec', 'src'))

# Import the function directly from the module
from src.dna_spec_kit_integration import cli_extension_handler

# Get the skills by calling the function
skills_info = cli_extension_handler.get_available_skills()
skills = skills_info.get('skills', [])
categories = skills_info.get('categories', [])

print(f"Total number of skills: {len(skills)}")
print(f"Total number of categories: {len(categories)}")
print("Skills:")
for i, skill in enumerate(skills, 1):
    print(f"  {i}. {skill['name']} (category: {skill['category']})")

print(f"\nCategories: {categories}")