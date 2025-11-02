# Dynamic Specification Growth System (DSGS) Project Context

## 1. Project Directory Structure
```
dsgs/
├── docs/
│   ├── specs/
│   │   └── dsgs-srs.md
│   └── reports/
│       └── progress.md
├── src/
│   ├── core/
│   │   ├── specification/
│   │   │   ├── SpecificationManager.ts
│   │   │   └── TccGenerator.ts
│   │   ├── constraint/
│   │   │   ├── ConstraintGenerator.ts
│   │   │   └── templates/
│   │   └── evolution/
│   │       ├── EvolutionManager.ts
│   │       └── stages.json
│   ├── integration/
│   │   ├── mcp/
│   │   │   └── McpAdapter.ts
│   │   └── cli/
│   │       └── CliInterface.ts
│   └── utils/
│       ├── types/
│       │   ├── TCC.ts
│       │   └── ErrorTypes.ts
│       └── error/
│           └── RecoveryManager.ts
├── test/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── tools/
│   └── scripts/
└── config/
    ├── bsl.schema.json
    └── mcp-config.json
```

## 2. Naming Conventions
- **No Plural Forms**: All directory and file names use singular form
- **CamelCase**: All identifiers use camelCase (e.g., SpecificationManager, TccGenerator)
- **Type-Specific Suffixes**: 
  - Classes: No suffix
  - Interfaces: No suffix
  - Types: `.type.ts` suffix
  - Utilities: `.utils.ts` suffix
  - Configuration: `.config.json` suffix

## 3. File Organization Principles
- **Maximum 500 Lines**: No single file exceeds 500 lines of code
- **Single Responsibility**: Each file has one primary responsibility
- **Top-Level Documentation**: Each file begins with JSDoc comments describing:
  - Purpose of the file
  - Public interfaces and their usage
  - Dependencies and assumptions
  - Examples of usage
- **Directory File Limit**: No directory contains more than 7 files; if exceeded, create subdirectories to group related files

## 4. Directory-Level Documentation
Each directory must contain a `README.md` file at its root that includes:
- **Purpose**: What this directory's components do
- **External Interfaces**: Public APIs exposed by this directory
- **Dependencies**: Other directories or external libraries this directory depends on
- **Usage Examples**: How to use the components in this directory
- **Constraints**: Any specific rules or limitations for this directory
- **Subdirectory Guidance**: If subdirectories are created, update this document with necessary guidance for the new structure

## 5. Code Structure Guidelines
- **Top-Down Design**: Code organization follows a top-down approach from system level to implementation details
- **Bottom-Up Implementation**: Implementation proceeds from basic utilities to complex components
- **Layered Architecture**: Clear separation between core logic, integration, and utilities
- **Minimal Token Consumption**: Code structure optimized for minimal AI context consumption

## 6. Development Workflow
- **Task-Driven Development**: All development follows the task list in `tasks.md`
- **Test-Driven Development**: Write tests before implementation for all components
- **Incremental Integration**: Integrate components incrementally, ensuring each step works before proceeding
- **Continuous Validation**: Validate against requirements and design at each stage

## 7. Evolution Management
- **Stage-Based Development**: Follow the evolution path from MVP to advanced stages
- **Self-Referential Governance**: The system uses its own specifications to govern its development
- **Migration Path**: Clear migration path between evolutionary stages with backward compatibility
- **Version Tracking**: Track system evolution stage in configuration

## 8. Integration Standards
- **MCP Compliance**: All integration components comply with MCP protocol
- **CLI Standards**: Command-line interface follows POSIX standards
- **Real-Time Feedback**: IDE integration provides real-time feedback with <5% CPU overhead
- **CI/CD Compatibility**: CLI interface supports common CI/CD tools with appropriate exit codes

## 9. Testing Strategy
- **90%+ Coverage**: Core components have 90%+ code coverage
- **Performance Targets**: Constraint generation completes in <100ms
- **Error Handling**: All error categories have corresponding tests
- **Integration Testing**: Test component interactions and external integrations

## 10. Documentation Standards
- **JSDoc Comments**: All public interfaces documented with JSDoc
- **Inline Comments**: Complex logic explained with inline comments
- **Architecture Diagrams**: Key components and relationships documented with Mermaid diagrams
- **Progress Tracking**: Development progress documented in `docs/reports/progress.md`
