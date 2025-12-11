# DNA SPEC Context System - Context Engineering Skills

## Project Overview

The DNA SPEC Context System Context Engineering Skills is a professional context engineering enhancement toolkit. Built on AI-native design principles, this system implements context analysis, optimization, and structuring functions through standardized instruction templates. It includes a complete set of context engineering skills, Git operation skills, and temporary workspace management systems, specifically designed for secure AI-assisted development workflows.

This project implements an independent skill system focused on the context engineering domain, without relying on external spec.kit systems.

## Key Features

- **Professional Skill System**: Specialized skills for context analysis, optimization, and cognitive template application
- **Context Engineering Enhancement**: Added context analysis, optimization, and cognitive template application skills
- **AI Safety Workflow**: Prevents AI-generated temporary files from polluting the main project through a temporary workspace management system
- **Git Operation Integration**: Complete Git workflow support including worktree and CI/CD functionality
- **Cross-Platform Support**: Supports multiple AI tools including Claude CLI, Gemini CLI, and Qwen CLI
- **Unified Interface**: Provides a unified slash command interface (/speckit.dnaspec.*)
- **Intelligent Matching**: Maintains DNA Spec System's unique intelligent matching and Hook system advantages

## Core Skill Set

### Context Engineering Skills

1. **Context Analysis Skill** (`dnaspec-context-analysis`)
   - Analyze context effectiveness
   - Evaluate five-dimensional quality metrics (clarity, relevance, completeness, consistency, efficiency)
   - Provide optimization suggestions
   - Supports both standard and enhanced modes

2. **Context Optimization Skill** (`dnaspec-context-optimization`)
   - Optimize context quality based on analysis results
   - Improve clarity, relevance, completeness, and conciseness
   - Supports token budget optimization and memory integration considerations
   - Supports both standard and enhanced modes

3. **Cognitive Template Skill** (`dnaspec-cognitive-template`)
   - Apply cognitive templates to context engineering tasks
   - Provide frameworks such as chain-of-thought, few-shot learning, and verification checks
   - Supports both standard and enhanced modes

### Git Operation Skills

4. **Git Skill** (`dnaspec-git-skill`)
   - Basic operations: status, add, commit, push, pull
   - Branch management: create, switch, merge
   - Advanced features: worktree management, stash, diff, log
   - CI/CD integration: supports automated commit workflows

### Temporary Workspace Management Skills

5. **Temporary Workspace Skill** (`dnaspec-temp-workspace-skill`)
   - **AI File Isolation**: AI-generated files are first stored in a temporary workspace
   - **Automatic Organization**: Triggers organization reminders when temporary files exceed 20
   - **Confirmation Mechanism**: Files can only be moved to the confirmation area after verification
   - **Git Integration**: Confirmed files can be directly synchronized to the Git repository
   - **Automatic Cleanup**: Automatically cleans up the temporary workspace after completion

### Management and System Skills

6. **Context Engineering Manager** (`dnaspec-context-engineering-manager`)
   - Unified management of context engineering skills

7. **Context Engineering System** (`dnaspec-context-engineering-system`)
   - Complete context engineering solution
   - Supports project decomposition and AI Agentic architecture context management

## AI Safety Workflow

AI-generated content follows this safety process to prevent project contamination by temporary files:

1. **Generation Phase**: AI output is first stored in a temporary workspace
2. **Organization Phase**: Automatic reminders when temporary files exceed 20
3. **Confirmation Phase**: Files are moved to the confirmation area after manual verification
4. **Commit Phase**: Confirmed files can be safely committed to the Git repository
5. **Cleanup Phase**: Automatic cleanup of the temporary workspace

## Author Information

- **Author**: pTree Dr.Zhang
- **Organization**: AI Persona Lab 2025
- **Contact Email**: 3061176@qq.com
- **Official Website**: https://AgentPsy.com
- **License**: MIT License
- **Version**: v1.0.2

## Installation Requirements

- Python 3.8+
- Git version control system

## Quick Installation (Recommended)

### npm Method (Easiest)

```bash
# Install from npm (recommended)
npm install -g dnaspec

# Or install directly from GitHub repository (requires Git to be installed first)
npm install -g ptreezh/dnaSpec

# Then run the short command
dnaspec
```

### Or Local Installation After Download

```bash
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaSpec

# Install locally as a global command (provides short command dnaspec)
npm install -g .

# Then run the short command
dnaspec
```

### Or Run Script (One Command Completes Everything)

```bash
# Directly run the installation script (automatically completes all steps)
git clone https://github.com/ptreezh/dnaSpec.git && cd dnaSpec && node index.js
```

Note: After running the installation command, the system will:

1. Automatically detect Python and Git environment
2. Clone or use project code
3. Install Python dependencies
4. Automatically detect installed AI CLI tools
5. Generate corresponding configuration files

Installation command:

```bash
# Recommended installation method
npm install -g dnaspec
dnaspec
```

### Windows System

```bash
# Method 1: Run one-click installation script
curl -O https://raw.githubusercontent.com/ptreezh/dnaSpec/main/install_and_configure.bat
install_and_configure.bat

# Method 2: Use short command to start (requires Node.js to be installed first)
npm install -g ptreezh/dnaSpec
dnaspec
```

### Linux/Mac System

```bash
# Method 1: Run one-click installation script
curl -O https://raw.githubusercontent.com/ptreezh/dnaSpec/main/install_and_configure.sh
chmod +x install_and_configure.sh
./install_and_configure.sh

# Method 2: Use short command to start (requires Node.js to be installed first)
npm install -g ptreezh/dnaSpec
dnaspec
```

## Manual Installation

If manual installation is needed:

### Method 1: Complete Installation

```bash
# Clone the project
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaSpec

# Install this project
pip install -e .

# Run auto-configuration
python run_auto_config.py
```

### Method 2: Short Command Installation (Recommended)

```bash
# Clone the project
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaSpec

# Install locally as a global command (provides short command dnaspec)
npm install -g .

# Or run the installation script (automatically completes all steps)
./index.js
# Or
node index.js
```

Using method 2, you can directly run the `dnaspec` command for installation and configuration.

### Method 3: Using Launch Script (Windows Users)

Download and use the launch script to run from any location:

```bash
# Download the launch script
curl -O https://raw.githubusercontent.com/ptreezh/dnaSpec/main/launch_dnaspec.bat

# Run installation configuration
launch_dnaspec.bat
```

Place the `launch_dnaspec.bat` file in a directory in the system PATH, then you can run the `launch_dnaspec.bat` command from any location.

## Usage

### Auto Configuration (Recommended)

```bash
# Run auto-configuration after first installation to detect and configure local AI CLI tools
python run_auto_config.py
```

### Command Line Usage

```bash
# Use slash commands to call skills
/speckit.dnaspec.context-analysis "Analyze the quality of this requirement document"
/speckit.dnaspec.context-optimization "Optimize the clarity of this requirement"
/speckit.dnaspec.cognitive-template "How to improve performance template=verification"
/speckit.dnaspec.architect "Design e-commerce system architecture"
/speckit.dnaspec.agent-creator "Create AI agent"
/speckit.dnaspec.task-decomposer "Decompose complex tasks"
/speckit.dnaspec.constraint-generator "Generate system constraints"
/speckit.dnaspec.dapi-checker "Check API interface"
/speckit.dnaspec.modulizer "Modularize system design"
/speckit.dnaspec.git-skill "operation=status"
/speckit.dnaspec.temp-workspace "operation=create-workspace"
```

### Python API Usage

```python
from src.dna_context_engineering.skills_system_final import ContextAnalysisSkill

# Use context analysis skill
skill = ContextAnalysisSkill()
result = skill.process_request("Design a user authentication system", {})
print(result)
```

### As a Library

```python
from clean_skills.context_analysis import execute as context_analysis_execute

# Standard mode
result = context_analysis_execute({'context': 'Text to analyze', 'mode': 'standard'})

# Enhanced mode
result = context_analysis_execute({'context': 'Text to analyze', 'mode': 'enhanced'})
```

### Git Operation Examples

```python
from clean_skills.git_skill import execute as git_execute

# Check Git status
result = git_execute({'operation': 'status'})

# Commit files
result = git_execute({'operation': 'commit', 'message': 'Commit message', 'files': '.'})

# Create worktree (isolates experimental development)
result = git_execute({
    'operation': 'worktree-add', 
    'branch': 'feature/new-feature'
})
```

### Temporary Workspace Usage Examples

```python
from clean_skills.temp_workspace_skill import execute as temp_workspace_execute

# Create temporary workspace (required before AI generation)
result = temp_workspace_execute({'operation': 'create-workspace'})

# Add AI-generated files
result = temp_workspace_execute({
    'operation': 'add-file', 
    'file_path': 'generated_code.py', 
    'file_content': '# Code content'
})

# Confirm files (after verification)
result = temp_workspace_execute({'operation': 'confirm-file', 'confirm_file': 'generated_code.py'})

# Clean up temporary workspace
result = temp_workspace_execute({'operation': 'clean-workspace'})
```

## Contributing

Welcome contributions! Please follow these guidelines:

1. Fork the project and clone to local
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open a Pull Request

## Support

- Issue reporting: https://github.com/ptreezh/dnaSpec/issues
- Contact email: 3061176@qq.com
- Official website: https://AgentPsy.com

## One-Click Installation Configuration Features

This project achieves the goal of "one installation, automatic detection of local CLI programming tools, and complete automatic configuration":

✅ **Automatic Environment Dependency Installation** - Automatically handles all Python dependencies through `pip install -e .`
✅ **Automatic CLI Tool Detection** - Automatically scans for installed AI CLI tools (Claude, Qwen, Gemini, Copilot, Cursor, etc.)
✅ **Automatic Configuration Generation** - Automatically generates configuration files based on detection results
✅ **One-Click Run Script** - Provides `install_and_configure.py` to complete installation and configuration in one click
✅ **Cross-Platform Support** - Full support for Windows, Linux, and Mac
✅ **Fixed Configuration Path Issues** - Resolves path issues during npm installation (v1.0.3)

---

DNA Spec System - Professional AI-Assisted Development Toolkit
© 2025 AI Persona Lab. Released under MIT License.