# DNASPEC Skills Navigation Guide

This document serves as the master navigation guide for all DNASPEC skills, providing organized access to detailed documentation for each skill module.

## Core Skills Documentation

### 1. Modularization Skill (模块化技能)
**Purpose**: Reduce system complexity through structured decomposition
- [View Detailed Documentation](skills/modularization_skill.md)
- **Implementation Status**: Implemented in spec-kit, not yet in clean_skills

### 2. DAPI Check Skill (DAPI检查技能)
**Purpose**: Align APIs between different system components
- [View Detailed Documentation](skills/dapi_check_skill.md)
- **Implementation Status**: Implemented in spec-kit, not yet in clean_skills

### 3. Architecture Skill (架构技能)
**Purpose**: Generate layered closure recursive decomposition contexts
- [View Detailed Documentation](skills/architecture_skill.md)
- **Implementation Status**: ✅ Fully implemented and available

### 4. Temporary Workspace Skill (动态工作区技能)
**Purpose**: Safe AI code generation with validation and cleanup
- [View Detailed Documentation](skills/temp_workspace_skill.md)
- **Implementation Status**: ✅ Fully implemented and available

### 5. Agentic Skills (Agentic功能模块)
**Purpose**: Create agent-capable functional modules
- [View Detailed Documentation](skills/agentic_skills_overview.md)
- **Implementation Status**: Conceptually documented, partially implemented

## Skill Categories

### Context Engineering Skills
- [Context Analysis Skill](skills/context_analysis_skill.md) - ✅ Implemented
- [Context Optimization Skill](skills/context_optimization_skill.md) - ✅ Implemented
- [Cognitive Template Skill](skills/cognitive_template_skill.md) - ⚠️ Documentation only

### System Management Skills
- [Git Operations Skill](skills/git_operations_skill.md) - ✅ Implemented
- [System Architect Skill](skills/system_architect_skill.md) - ✅ Implemented

### Utility Skills
- [Liveness Check Skill](skills/liveness_check_skill.md) - ✅ Implemented

## Implementation Status Legend
- ✅ **Fully Implemented**: Available in clean_skills directory and ready for use
- ⚠️ **Partially Implemented**: Exists but not fully integrated or available
- **Documentation Only**: Conceptually described but not yet implemented

## Important Notes
Some skills are implemented in the spec-kit directory but have not yet been moved to the clean_skills production directory. See [SKILL_IMPLEMENTATION_NOTE.md](SKILL_IMPLEMENTATION_NOTE.md) for details.

---

*This navigation guide follows Gestalt principles and progressive disclosure for optimal AI readability.*