# AGENT CREATOR - Quick Reference Card

## Purpose
Create specialized AI agents with defined roles and capabilities to isolate contexts and prevent contamination.

## Core Command
```
/dnaspec.agent-create <role_description>
```

## Parameters
- `capabilities` (optional): List specific agent abilities
- `domain` (optional): Define area of expertise

## Examples
```
# Basic agent creation
/dnaspec.agent-create "Python code reviewer"

# Agent with custom capabilities  
/dnaspec.agent-create "Data analyst" capabilities=["visualization","statistics"] domain="finance"
```

## Output
```
{
  agent_config: {
    id: "agent_unique_uuid",
    role: "defined role",
    domain: "expertise area", 
    capabilities: ["list","of","abilities"],
    instructions: "role-specific instructions"
  }
}
```

## Key Benefits
- Context isolation for specific tasks
- Prevents contamination between different AI interactions
- Role-specific instruction generation

## Performance
- Creation time: <100ms
- Lightweight, no external dependencies