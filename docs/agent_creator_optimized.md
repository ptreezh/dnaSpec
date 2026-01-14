# Agent Creator Skill - Optimized Documentation

## Layer 1: Conceptual Overview
**Purpose**: Creates specialized AI agents with predefined roles and capabilities
**Value**: Prevents context contamination by isolating specific AI tasks
**Quick Start**: `/dnaspec.agent-create "Python code reviewer"`

---

## Layer 2: Core Usage

### Basic Command
```
/dnaspec.agent-create <role_description>
```

### Common Parameters
- `capabilities`: List of specific abilities for the agent
- `domain`: Area of expertise for the agent

### Examples
```
# Create a simple code reviewer agent
/dnaspec.agent-create "Python code reviewer"

# Create with specific capabilities
/dnaspec.agent-create "Data analyst" capabilities=["visualization","statistics"] domain="finance"
```

### Expected Output
- Agent ID (unique identifier)
- Role description
- Available capabilities
- Specialized instructions

### Error Handling
- Invalid role descriptions return error suggestions
- Malformed parameters return usage guidance

---

## Layer 3: Advanced Features

### Configuration Options
- Custom instructions via `instructions` parameter
- Personality settings via `personality` parameter  
- Capability limits and validation

### Integration Patterns
- Combine with task decomposer for project-specific agents
- Use with constraint generator to enforce agent boundaries

### Performance Considerations
- Agent creation time: <100ms
- No external dependencies required

### Troubleshooting
- If agent doesn't respond: Check role description clarity
- If capabilities not working: Verify capability names are supported

---

## Layer 4: Implementation Details

### API Specification
```
Input: {
  role_description: string (required),
  capabilities?: string[],
  domain?: string
}
Output: {
  agent_config: {
    id: string,
    role: string,
    domain: string,
    capabilities: string[],
    instructions: string,
    personality: string
  },
  success: boolean,
  timestamp: number
}
```

### Architecture
- Inheritance: DNASpecSkill base class
- State management: In-memory agent configurations
- Validation: Input sanitization and constraint checking

### Extension Points
- Custom agent templates
- Additional capability types
- Enhanced instruction generation