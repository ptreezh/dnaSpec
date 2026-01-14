import os

skill_dir = 'D:/DAIP/dnaSpec/src/dna_spec_kit_integration/skills'
skill_files = [f for f in os.listdir(skill_dir) if f.endswith('.py') and f != '__init__.py']

print('Checking all skill files for execute function:')
execute_count = 0
no_execute_count = 0

for file in skill_files:
    file_path = os.path.join(skill_dir, file)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        if 'def execute(' in content:
            print(f'  ✅ {file} - has execute function')
            execute_count += 1
        else:
            print(f'  ❌ {file} - no execute function')
            no_execute_count += 1

print(f'\nSummary: {execute_count} files have execute function, {no_execute_count} files do not')