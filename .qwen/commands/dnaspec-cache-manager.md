# DNASPEC Cache Manager

## Description
Manage AI-generated files with staging and validation to prevent workspace pollution

## Command
`/dnaspec.cache-manager`

## Usage
Use this command to manage AI-generated files and prevent workspace pollution through intelligent caching and staging.

### Examples
```bash
# Initialize cache system for the project
/dnaspec.cache-manager "operation=init-cache project_path=."

# Stage a file for validation
/dnaspec.cache-manager "operation=stage-file file_path=example.py content='import os'

# Validate staged files
/dnaspec.cache-manager "operation=validate-staged project_path=."

# Commit validated files
/dnaspec.cache-manager "operation=commit-staged project_path=. message='Add validated AI-generated code'

# Clean up cache
/dnaspec.cache-manager "operation=cleanup-cache project_path=."

# Get cache status
/dnaspec.cache-manager "operation=cache-status project_path=."
```

## Operations
- **init-cache**: Initialize cache system with staging areas
- **stage-file**: Stage files for validation before commit
- **validate-staged**: Validate staged files for quality and security
- **commit-staged**: Commit validated files to main workspace
- **cleanup-cache**: Clean expired files and free up space
- **cache-status**: Display cache system status and statistics

## Integration with DNASPEC
This command implements DNASPEC's workspace protection strategy to maintain clean development environments while leveraging AI assistance.

---
*Generated for qwen CLI*
*Project: dnaSpec*
*Generated on: 2025-12-12 14:07:41*
