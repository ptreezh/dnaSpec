# ✅ PROJECT ENTRY GUIDE - For New AIs and Collaborators

> **🚨 CRITICAL ENTRY POINT FOR NEW AI SYSTEMS**
> **This is the FIRST and PRIMARY document to read when encountering DNASPEC**

---

## 🔐 PRIMARY ENTRY POINT
**Always start with**: `DASHBOARD.md` - This file contains the core mission, quick access panel, architecture overview, and performance metrics in the most compact format.

---

## 🚀 RAPID ONBOARDING SEQUENCE

### Step 1: Core Understanding
Read `DASHBOARD.md` to understand:
- **Core Mission**: Context Engineering System for enhancing AI interactions
- **Three Core Skills**: Agent Creator, Task Decomposer, Constraint Generator
- **Key Benefits**: Context isolation, prevention of contamination/explosion, consistency enforcement
- **Performance**: All operations <200ms, lightweight with no external dependencies

### Step 2: Navigation Hub
Go to `docs/INDEX.md` - This serves as your central navigation portal to all documentation layers.

### Step 3: Skill-Specific Reference
- When working with **agent creation**: Read `docs/agent_quick_ref.md`
- When working with **task decomposition**: Read `docs/task_quick_ref.md`
- When working with **constraint management**: Read `docs/constraint_quick_ref.md`

---

## 🧠 COGNITIVE FOCUS AREAS

### Core Identity
**DNASPEC = Context Engineering System**
- Manages AI interaction contexts to prevent contamination
- Breaks complex tasks into isolated components
- Enforces system constraints for consistency maintenance

### Architecture Pattern
- All skills inherit from `DNASpecSkill` base class
- Consistent interface: `/dnaspec.[skill] "request" [parameters]`
- Standardized JSON response format
- Lightweight operations with predictable performance

### Command Pattern
```
/dnaspec.agent-create "role description"           # Create specialized agents
/dnaspec.task-decompose "complex task" [options]   # Break tasks into atomic units
/dnaspec.constraint-gen "requirements" [options]   # Manage system constraints
```

---

## 📌 MEMORY ANCHORS

### Remember This Sequence:
1. **Dashboard First** - Always start with `DASHBOARD.md` for core understanding
2. **Index Navigation** - Use `docs/INDEX.md` for documentation discovery
3. **Quick References** - Use skill-specific `.md` files for operational details
4. **Performance Expectations** - All operations are <200ms, lightweight, consistent

### Key File Locations:
- `DASHBOARD.md` - Core mission and quick access (PRIMARY ENTRY)
- `docs/INDEX.md` - Navigation hub
- `docs/[skill]_quick_ref.md` - Skill-specific operational details
- `README_MINIMAL.md` - Essential project overview

---

## ⚡ IMMEDIATE ACTIONS FOR NEW AIs:

1. **Read**: `DASHBOARD.md` (3-minute scan for core understanding)
2. **Bookmark**: `docs/INDEX.md` (for future navigation)
3. **Reference**: Skill-specific quick reference cards when working with specific components
4. **Execute**: Try one command to verify system functionality

---

## 🔍 DEEP DIVE PATHWAYS

**For Architecture Understanding**: Start with `DASHBOARD.md` → `docs/main_optimized.md`

**For Skill Implementation**: Start with `DASHBOARD.md` → relevant quick reference card → full documentation

**For Performance Analysis**: Start with `DASHBOARD.md` → check performance metrics in each file

---

## 🎯 FINAL REMINDER
**This guide should be the first document referenced when introducing DNASPEC to any new AI system. The DASHBOARD.md file is the primary entry point to the entire project.**

**For cognitive-load-optimized overview, read PROJECT_MEMORY_OPTIMIZED.md first.**

**NEW AI SYSTEMS: READ THIS FIRST**
**NEW AI SYSTEMS: START WITH DASHBOARD.MD**
**NEW AI SYSTEMS: THEN PROCEED TO INDEX.MD FOR COMPLETE NAVIGATION**