import sys, os
sys.path.insert(0, os.path.join('D:', 'DAIP', 'dnaSpec', 'src'))
from src.dna_spec_kit_integration.core.cli_extension_deployer import CLIExtensionDeployer
deployer = CLIExtensionDeployer()
skills = deployer._get_dnaspec_skills()
print('Number of skills:', len(skills))
for i, skill in enumerate(skills):
    print(f'{i+1}. {skill["name"]} - {skill["description"]}')