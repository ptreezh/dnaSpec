# DNASPEC Project Memory - Optimized for AI Systems

## 🚀 Core Purpose (Layer 1: 30-second scan)
**DNASPEC** = Context Engineering System for enhancing AI interactions

**Core Functions**:
- **Context Isolation**: Prevent contamination between AI interactions
- **Task Management**: Break complex work into atomic components  
- **Constraint Enforcement**: Maintain system consistency

**Entry Point**: Read `DASHBOARD.md` first, then `docs/INDEX.md` for navigation

---

## ⚙️ System Architecture (Layer 2: 2-minute read)

### Three Core Skills
| Skill | Purpose | Command |
|-------|---------|---------|
| **Agent Creator** | Create specialized agents for focused tasks | `/dnaspec.agent-create` |
| **Task Decomposer** | Break complex tasks into isolated workspaces | `/dnaspec.task-decompose` |
| **Constraint Generator** | Enforce system constraints and check alignment | `/dnaspec.constraint-gen` |

### Key Principles
- **Lightweight**: All operations <200ms
- **Consistent Interface**: Inherit from `DNASpecSkill` base
- **Isolation**: Prevent context contamination between components

---

## 📋 Functional Overview (Layer 3: 5-minute read)

### Agent Creator
- Creates specialized AI agents based on role descriptions
- Generates role-specific instructions and capabilities
- Enables context isolation for different AI tasks

### Task Decomposer  
- Recursively breaks complex tasks into atomic components
- Creates isolated workspaces to prevent context explosion
- Controls decomposition depth (max 3 levels)

### Constraint Generator
- Generates constraints from system requirements
- Checks alignment of change requests
- Tracks requirements evolution with versioning

---

## 🔧 Technical Implementation (Layer 4: In-depth)

### Architecture Pattern
- Base class: `DNASpecSkill`
- Interface: `request` (string) + `context` (object)
- Response: Standardized JSON with success/timestamp/data
- File system: Workspace management for isolation

### Performance Metrics
- Agent Creation: <100ms
- Task Decomposition: <200ms
- Constraint Generation: <50ms

### Integration Points
- AI CLI Platforms (Claude, Qwen, etc.)
- File System for workspace management
- Standard JSON interfaces for all components

---

## 🎯 Key Milestones

### Phase 1: Internationalization
- Pure ANSI English interfaces
- Cross-platform compatibility
- English skill implementations

### Phase 2: Agentic Implementation
- Agent Creator with role analysis
- Task Decomposer with NLP parsing
- Constraint Generator with verification methods

### Phase 3: Integration
- Cross-CLI collaboration (Stigmergy)
- Complete functionality testing
- Performance optimization

---

## 📖 Next Steps for AI Systems

1. **Start Here**: `DASHBOARD.md` for core mission and quick access
2. **Navigate**: `docs/INDEX.md` for complete documentation map
3. **Reference**: Quick reference cards for specific skills
4. **Explore**: Follow progressive documentation layers as needed