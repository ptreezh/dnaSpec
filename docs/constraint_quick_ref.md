# CONSTRAINT GENERATOR - Quick Reference Card

## Purpose
Generate system constraints based on requirements and check alignment of change requests to ensure consistency and identify conflicts.

## Core Command
```
/dnaspec.constraint-gen <requirements>
```

## Parameters
- `change_request` (optional): Specific change to evaluate against requirements
- `track_version` (optional): Enable version tracking (default: false)

## Examples
```
# Generate constraints from requirements
/dnaspec.constraint-gen "High security financial system"

# Check change alignment against requirements
/dnaspec.constraint-gen "System with security" change_request="Add cryptocurrency support" track_version=true
```

## Output
```
{
  constraints: [
    {
      id: "constraint_unique_uuid", 
      type: "security|performance|data_integrity",
      description: "constraint details",
      severity: "high|medium|low",
      created_at: "2025-01-08T10:30:00"
    }
  ],
  alignment_check: {
    is_aligned: true/false,
    conflicts: [...],      // Array of conflict objects if any
    suggestions: [...]     // Alignment suggestions
  },
  version_info: {
    current_version: "version_tag",
    tracked: true/false
  }
}
```

## Key Benefits
- Identifies conflicts between changes and requirements
- Maintains system consistency during evolution
- Tracks version history for requirements

## Performance
- Generation time: <50ms
- Keywords-based constraint detection
- Efficient alignment checking