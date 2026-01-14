import os
import glob
import re

# 查找技能目录中的execute函数
skills_dir = 'D:/DAIP/dnaSpec/src/dna_spec_kit_integration/skills'
for file in glob.glob(os.path.join(skills_dir, '*.py')):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        matches = re.findall(r'def execute_([a-zA-Z_]+)', content)
        if matches:
            print(f'{os.path.basename(file)}: {[m for m in matches]}')
    except Exception as e:
        print(f'Error reading {os.path.basename(file)}: {e}')

print("\n--- Actual Available Skills ---")
available_skills = {
    "context-analysis": "context_analysis_independent.py",
    "agent-creator": "agent_creator_independent.py",
    "simple-architect": "simple_architect_independent.py",
    "system-architect": "system_architect_independent.py",
    "modulizer": "modulizer_independent.py",
    "task-decomposer": "task_decomposer.py",
    "constraint-generator": "constraint_generator.py",
    "dapi-checker": "api_checker.py",
    "constitutional-module-formation": "constitutional_modulizer_independent.py",
    "reality-validation": "reality_validator.py"
}

for skill, file in available_skills.items():
    print(f"{skill}: {file}")