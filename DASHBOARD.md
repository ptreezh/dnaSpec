# DNASPEC DASHBOARD - Core Mission & Modules Overview

## 🎯 CORE MISSION
**Context Engineering System**: Enhance AI interactions by managing context quality, preventing contamination, and enforcing system constraints.

**For New AI Systems**: Start with [PROJECT_ENTRY_GUIDE.md](PROJECT_ENTRY_GUIDE.md) for rapid understanding of navigation and core concepts.

---

## ⚡ QUICK ACCESS PANEL

### Agent Creator Skill
**Purpose**: Create specialized AI agents for focused tasks
**Command**: `/dnaspec.agent-create "role"`
**Key Params**: `capabilities`, `domain`
**Value**: Isolate AI contexts for specific roles

### Task Decomposer Skill
**Purpose**: Break complex tasks into atomic components with isolated workspaces
**Command**: `/dnaspec.task-decompose "task" max_depth=N`
**Key Params**: `max_depth`, `workspace_base`
**Value**: Prevent AI context explosion in complex tasks

### Constraint Generator Skill
**Purpose**: Generate system constraints and check change alignment
**Command**: `/dnaspec.constraint-gen "reqs" change_request="..."`
**Key Params**: `change_request`, `track_version`
**Value**: Maintain requirements consistency across changes

---

## 🔧 ARCHITECTURE OVERVIEW
- **Base Class**: All skills inherit from `DNASpecSkill`
- **Interface**: `request` (string) + `context` (object) pattern
- **Response**: Standardized JSON with `success`, `timestamp`, and domain-specific data
- **State**: Minimal, in-memory where needed

---

## 📊 PERFORMANCE METRICS
- Agent Creation: <100ms
- Task Decomposition: <200ms
- Constraint Generation: <50ms
- All operations lightweight with no external dependencies

---

## 🔄 WORKFLOW PATTERNS
- **Project Setup**: Agent Creator → Task Decomposer → Constraint Generator
- **Change Evaluation**: Constraint Generator → Task Decomposer → Agent Creator
- **Quality Assurance**: Task Decomposer → Constraint Generator

---

## 📋 REFERENCE
- **For New AIs**: See [PROJECT_ENTRY_GUIDE.md](PROJECT_ENTRY_GUIDE.md) for rapid onboarding sequence
- **Cognitive-Load-Optimized Overview**: [PROJECT_MEMORY_OPTIMIZED.md](PROJECT_MEMORY_OPTIMIZED.md) for reduced cognitive load
- **Navigation Hub**: [docs/INDEX.md](docs/INDEX.md) for complete documentation map
- **Quick Skill References**:
  - [Agent Creator](docs/agent_quick_ref.md)
  - [Task Decomposer](docs/task_quick_ref.md)
  - [Constraint Generator](docs/constraint_quick_ref.md)