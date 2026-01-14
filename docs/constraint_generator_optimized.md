# Constraint Generator Skill - Optimized Documentation

## Layer 1: Conceptual Overview
**Purpose**: Creates and manages system constraints based on requirements with alignment checking
**Value**: Ensures change requests align with base requirements and identifies conflicts
**Quick Start**: `/dnaspec.constraint-gen "System with security" change_request="Add new feature"`

---

## Layer 2: Core Usage

### Basic Command
```
/dnaspec.constraint-gen <requirements>
```

### Common Parameters
- `change_request`: Specific change to evaluate against requirements
- `track_version`: Enable version tracking for requirements evolution

### Examples
```
# Generate constraints from requirements
/dnaspec.constraint-gen "Financial system with high security"

# Check change alignment
/dnaspec.constraint-gen "System with security" change_request="Add cryptocurrency support" track_version=true
```

### Expected Output
- Generated constraint list
- Alignment check results
- Conflict detection
- Version tracking information

### Error Handling
- Contradictory terms trigger conflict alerts
- Missing requirements return guidance for improvement

---

## Layer 3: Advanced Features

### Configuration Options
- Custom constraint types
- Advanced conflict detection
- Requirements version management
- Constraint severity levels

### Integration Patterns
- Use with task decomposer to enforce task constraints
- Combine with agent creator to limit agent capabilities

### Performance Considerations
- Constraint generation time: <50ms
- Alignment checking efficiency for requirement sets

### Troubleshooting
- If constraints seem inappropriate: Review requirement clarity
- If alignment checks are too permissive: Add more specific requirements

---

## Layer 4: Implementation Details

### API Specification
```
Input: {
  requirements: string (required),
  change_request?: string,
  track_version?: boolean (default: false)
}
Output: {
  constraints: [
    {
      id: string,
      type: string,
      description: string,
      severity: string,
      created_at: string
    }
  ],
  alignment_check: {
    is_aligned: boolean,
    conflicts: [...],
    suggestions: [...]
  },
  version_info: {
    current_version: string,
    tracked: boolean
  },
  success: boolean,
  timestamp: number
}
```

### Architecture
- Keyword-based constraint generation
- Requirements vs changes alignment engine
- Version tracking and management system
- Conflict detection algorithms

### Extension Points
- Advanced constraint types
- Machine learning-based alignment checking
- Integration with requirements management tools