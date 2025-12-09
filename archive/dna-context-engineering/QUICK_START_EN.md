# DNASPEC Context Engineering Skills - Quick Start Guide (English)

## Project Overview

DNASPEC (Dynamic Specification Growth System) Context Engineering Skills is a professional AI-assisted development toolkit designed specifically for AI CLI platforms, providing context analysis, optimization, and cognitive templating capabilities with AI safety workflow.

## Core Improvements

### 1. Unified Skill Architecture
- **Consolidated Implementation**: Standard and enhanced mode skills merged into single implementation
- **Mode Toggle**: Use `mode` parameter to control functionality level ('standard' or 'enhanced')
- **Single Interface**: Simplified interface avoiding duplicate functionality

### 2. Flat Directory Structure
- **One Skill Per Directory**: Each skill in its own directory, no unnecessary nesting
- **Simplified Organization**: Intuitive skill layout, easier maintenance
- **Reduced Confusion**: Clear skill boundaries, no overlapping functionality

### 3. AI Safety Workflow
- **Temporary Workspace**: AI generated content first stored in temporary area
- **Auto-Management**: Automatic alert when file count exceeds 20
- **Confirmation Mechanism**: Content must be verified before main project inclusion
- **Auto-Cleanup**: Automatic clearing of temporary workspace after task completion

## Installation

```bash
# Clone repository
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaspec-context-engineering

# Install
pip install -e .
```

## Usage

### CLI Commands
```
/speckit.dnaspec.context-analysis "Analyze quality of this requirement doc" mode=enhanced
/speckit.dnaspec.cognitive-template "How to improve performance" template=verification
/speckit.dnaspec.context-optimization "Optimize this requirement" optimization_goals=clarity,relevance
/speckit.dnaspec.architect "Design e-commerce system architecture"
/speckit.dnaspec.git-skill operation=status
/speckit.dnaspec.temp-workspace operation=create-workspace
```

### Python API
```python
from clean_skills.context_analysis import execute as context_analysis_execute

# Standard Mode
result = context_analysis_execute({
    'context': 'Design user login feature',
    'mode': 'standard'
})

# Enhanced Mode
result = context_analysis_execute({
    'context': 'Design high-security user login feature', 
    'mode': 'enhanced'
})
```

## AI Safety Best Practices

1. **Before AI Generation**: Always create temporary workspace first
2. **Validate Content**: Use confirmation mechanism to verify AI generated content
3. **Regular Cleanup**: Monitor temporary file count
4. **Clear Workspace**: Clean temporary area after task completion

---
*Author: pTree Dr.Zhang*  
*Organization: AI Persona Lab 2025*  
*Contact: 3061176@qq.com*  
*Website: https://AgentPsy.com*