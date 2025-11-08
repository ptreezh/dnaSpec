# DSGS Context Engineering Skills - Open Source Release

## Repository Information

**Official Repository**: https://github.com/AgentPsy/dsgs-context-engineering  
**Author**: pTree Dr.Zhang  
**Organization**: AI Persona Lab 2025  
**Contact**: 3061176@qq.com  
**Website**: https://AgentPsy.com  
**License**: MIT

## Project Overview

DSGS (Dynamic Specification Growth System) Context Engineering Skills is a professional AI-assisted development toolkit that provides context analysis, optimization, and cognitive templating capabilities for AI CLI platforms including Claude, Qwen, and Gemini.

## Key Features

- **Unified Skill Structure**: Single skill implementation supporting both standard and enhanced modes via mode parameter
- **Flat Directory Structure**: One directory per skill, no unnecessary nesting
- **AI Safety Workflow**: Temporary workspace management preventing AI-generated files from polluting main project
- **Cross-Platform Support**: Compatible with Claude CLI, Qwen CLI, Gemini CLI and other AI platforms
- **Professional Context Engineering**: Industry-standard context analysis and optimization
- **Git Integration**: Full Git workflow support including worktree management

## Installation

```bash
git clone https://github.com/AgentPsy/dsgs-context-engineering.git
cd dsgs-context-engineering
pip install -e .
```

## Usage

### CLI Commands
```
/speckit.dsgs.context-analysis "Analyze this context for quality"
/speckit.dsgs.cognitive-template "How to improve performance" template=verification
/speckit.dsgs.context-optimization "Optimize this requirement" optimization_goals=clarity,relevance
/speckit.dsgs.architect "Design an e-commerce system"
/speckit.dsgs.git-skill operation=status
/speckit.dsgs.temp-workspace operation=create-workspace
```

### Python API
```python
from clean_skills import (
    context_analysis_execute,
    cognitive_template_execute,
    context_optimization_execute,
    architect_execute,
    git_execute,
    temp_workspace_execute
)

# Use standard mode
result = context_analysis_execute({'context': 'Analyze this text', 'mode': 'standard'})

# Use enhanced mode
result = context_analysis_execute({'context': 'Analyze deeply', 'mode': 'enhanced'})
```

## AI Safety Workflow

The system implements a secure AI workflow to prevent temporary files from polluting your project:

1. **Generation Phase**: AI outputs stored in temporary workspace
2. **Review Phase**: Human verification of generated content  
3. **Confirmation Phase**: Approved files moved to main project
4. **Cleanup Phase**: Automatic clearing of temporary workspace

## License

MIT License - see LICENSE file for details

## Contributions

We welcome contributions! Please see our CONTRIBUTING.md file for guidelines.

## Support

- Issues: https://github.com/AgentPsy/dsgs-context-engineering/issues
- Contact: 3061176@qq.com