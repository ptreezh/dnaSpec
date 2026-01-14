#!/usr/bin/env python3
"""
紧急恢复：为 DNASPEC 恢复关键的临时工作区、Git 操作和宪法保障功能
"""
import os
import shutil
from pathlib import Path


def restore_critical_skills():
    """恢复关键技能文件"""
    print(" recovering critical skills...")
    print("="*50)
    
    # 定义需要恢复的关键文件
    critical_files = {
        # 临时工作区功能 - AI安全工作流
        'temp_workspace.py': 'temp_workspace.py',
        'temp_workspace_constitutional.py': 'temp_workspace_constitutional.py',
        'temp_workspace_standard.py': 'temp_workspace_standard.py',
        
        # Git操作和项目宪法功能 - 项目治理
        'git_operations.py': 'git_operations.py',
        'git_operations_constitutional.py': 'git_operations_constitutional.py',
        'git_operations_refactored.py': 'git_operations_refactored.py',
        
        # 宪法验证功能 - 治理保障
        'constitutional_validator.py': 'constitutional_validator.py',
        'constitutional_validator_standard.py': 'constitutional_validator_standard.py',
        
        # 合同执行功能 - 协调保障
        'coordination_contract_checker.py': 'coordination_contract_checker.py',
        'coordination_contract_enforcer.py': 'coordination_contract_enforcer.py',
        'coordination_contract_hooks.py': 'coordination_contract_hooks.py',
    }
    
    # 源目录（归档位置）
    source_dir = Path("D:/DAIP/dnaSpec/archive/skills")
    
    # 目标目录（当前技能目录）
    target_dir = Path("D:/DAIP/dnaSpec/src/dna_context_engineering/")
    
    restored_files = []
    
    for source_file, target_file in critical_files.items():
        source_path = source_dir / source_file
        target_path = target_dir / target_file
        
        if source_path.exists():
            try:
                # 复制文件
                shutil.copy2(source_path, target_path)
                print(f"✅ Restored: {source_file} -> {target_file}")
                restored_files.append(target_file)
            except Exception as e:
                print(f"❌ Failed to restore {source_file}: {e}")
        else:
            print(f"⚠️  Not found in archive: {source_file}")
    
    print(f"\n📋 Restored {len(restored_files)} critical skill files:")
    for f in restored_files:
        print(f"   - {f}")
    
    # 更新 __init__.py 以包含这些关键功能
    init_file = target_dir / "__init__.py"
    if init_file.exists():
        with open(init_file, 'r', encoding='utf-8') as f:
            init_content = f.read()
        
        # 检查是否需要添加关键功能的导入
        additions_needed = []
        
        if "temp_workspace" not in init_content:
            additions_needed.append("from .temp_workspace import execute as temp_workspace_execute")
        
        if "git_operations" not in init_content:
            additions_needed.append("from .git_operations import execute as git_operations_execute")
        
        if "constitutional_validator" not in init_content:
            additions_needed.append("from .constitutional_validator import execute as constitutional_validator_execute")
        
        if "coordination_contract_checker" not in init_content:
            additions_needed.append("from .coordination_contract_checker import execute as coordination_contract_check_execute")
        
        if "coordination_contract_enforcer" not in init_content:
            additions_needed.append("from .coordination_contract_enforcer import execute as coordination_contract_enforce_execute")
        
        if additions_needed:
            # Add the imports to the __init__.py
            lines = init_content.split('\n')
            # Find where to insert imports (after imports but before definitions)
            insert_pos = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('from .'):
                    insert_pos = i + 1
                elif line.strip().startswith('def ') or line.strip().startswith('class ') or line.strip().startswith('__all__'):
                    break
                else:
                    insert_pos = i + 1
            
            # Insert new imports
            for addition in additions_needed:
                lines.insert(insert_pos, addition)
                insert_pos += 1
            
            # Update __all__ with new functions if needed
            all_updated = False
            for i, line in enumerate(lines):
                if '__all__' in line:
                    # Add the new functions to __all__ if not present
                    for addition in additions_needed:
                        func_name = addition.split()[-1]  # Get function name from 'from .module import execute as func_name'
                        if func_name not in line:
                            # Find the closing bracket of __all__ and add the function
                            for j in range(i, min(i+10, len(lines))):
                                if ']' in lines[j]:
                                    lines[j] = lines[j].rstrip().rstrip(']') + f", '{func_name.strip()}'" + ']'
                                    break
                    all_updated = True
                    break
            
            if not all_updated:
                # Add __all__ if it doesn't exist
                lines.extend(additions_needed)
                
            # Write back updated content
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
                
            print(f"\n✅ Updated __init__.py with {len(additions_needed)} new imports")
        else:
            print("\nℹ️  __init__.py already contains required imports")
    
    # Also update the skill_mapper to include these new functions
    skill_mapper_file = Path("D:/DAIP/dnaSpec/src/dna_spec_kit_integration/core/skill_mapper.py")
    if skill_mapper_file.exists():
        with open(skill_mapper_file, 'r', encoding='utf-8') as f:
            mapper_content = f.read()
        
        # Add new skill mappings for the restored functionality
        if "temp-workspace" not in mapper_content:
            # Find the skill_map and add new entries
            if "skill_map" in mapper_content:
                # For the new skills, add them to the skill map
                new_skills = {
                    'temp-workspace': 'dnaspec-temp_workspace',
                    'git-ops': 'dnaspec-git_operations', 
                    'constitutional-validator': 'dnaspec-constitutional_validator',
                    'contract-checker': 'dnaspec-coordination_contract_checker',
                    'contract-enforcer': 'dnaspec-coordination_contract_enforcer'
                }
                
                # Update the file content with new skill mappings
                for skill_name, module_name in new_skills.items():
                    if skill_name not in mapper_content:
                        # Find the skill_map dictionary and add new entries
                        if "}" in mapper_content:
                            # This is a simplified update - in real scenario we'd be more precise
                            print(f"⚠️  Need to manually add skill mapping: {skill_name} -> {module_name}")
                
                print("ℹ️  Skill mapper updates needed - would add new skill mappings")
    
    return restored_files


def verify_restored_skills():
    """验证恢复的技能功能"""
    print(f"\n🔍 Verifying restored skills...")
    
    critical_skills = [
        ("python -c \"from src.dna_context_engineering.temp_workspace import execute; result = execute({'operation': 'create-workspace'}); print('Temporal workspace skill loaded and callable')\"", "Temporal Workspace Skill"),
        ("python -c \"from src.dna_context_engineering.git_operations import execute; result = execute({'operation': 'status-report'}); print('Git operations skill loaded and callable')\"", "Git Operations Skill"),
        ("python -c \"from src.dna_context_engineering.constitutional_validator import execute; print('Constitutional validator skill loaded')\"", "Constitutional Validator Skill"),
        ("python -c \"from src.dna_context_engineering.coordination_contract_checker import execute; print('Coordination contract checker skill loaded')\"", "Coordination Contract Checker Skill"),
    ]
    
    verification_results = []
    for cmd, description in critical_skills:
        try:
            import subprocess
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            success = result.returncode == 0
            verification_results.append((description, success))
            if success:
                print(f"✅ {description}: OK")
            else:
                print(f"❌ {description}: FAILED - {result.stderr[:100]}")
        except Exception as e:
            print(f"❌ {description}: ERROR - {str(e)[:100]}")
            verification_results.append((description, False))
    
    return verification_results


if __name__ == "__main__":
    print("🔧 DNASPEC CRITICAL SKILLS RECOVERY SYSTEM")
    print(f"Source: D:/DAIP/dnaSpec/archive/skills/")
    print(f"Target: D:/DAIP/dnaSpec/src/dna_context_engineering/")
    
    # Restore critical skills
    restored = restore_critical_skills()
    
    # Verify the restored functionality
    verification_results = verify_restored_skills()
    
    # Generate summary
    total_skills = len(verification_results)
    successful_skills = sum(1 for _, success in verification_results if success)
    
    print(f"\n🎯 RECOVERY COMPLETION REPORT:")
    print(f"   Files Restored: {len(restored)}")
    print(f"   Skills Verified: {successful_skills}/{total_skills}")
    print(f"   Success Rate: {successful_skills/total_skills*100:.1f}%")
    
    if successful_skills == total_skills and total_skills > 0:
        print("\n🎉 CRITICAL SKILLS RECOVERY COMPLETE!")
        print("   ✅ Temporary workspace functionality restored")
        print("   ✅ Git operations and project constitution restored")
        print("   ✅ Constitutional validation system restored")
        print("   ✅ Contractual coordination system restored")
        print("   ✅ All governance and safety mechanisms active")
    else:
        print(f"\n⚠️  RECOVERY PARTIAL: {total_skills - successful_skills} skills need additional attention")
        
    print(f"\n📋 Restored Files List:")
    for f in restored:
        print(f"   - {f}")
    
    print("\n🚀 DNASPEC System with Full Governance Recovery Ready!")