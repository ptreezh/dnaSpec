import sys, os
sys.path.insert(0, os.path.join('D:', 'DAIP', 'dnaSpec', 'src'))
from src.dna_spec_kit_integration.core.cli_extension_handler import CLISkillsHandler

handler = CLISkillsHandler()
skills_info = handler.get_available_skills()
print('Skills info keys:', skills_info.keys() if skills_info else "No skills_info")
if skills_info:
    print('Total count:', skills_info.get('total_count'))
    print('Skills length:', len(skills_info.get('skills', [])))
    print('Categories length:', len(skills_info.get('categories', [])))
    print('Categories:', skills_info.get('categories'))
    print('Skills sample:', skills_info.get('skills', [])[:3] if skills_info.get('skills') else "No skills")