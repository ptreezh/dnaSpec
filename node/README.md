# DSGS Skills for spec.kit Integration

DSGS (Dynamic Specification Growth System) Skills integration with GitHub spec.kit toolkit. This package provides professional AI skills for architecture design, agent creation, and more, with seamless integration across multiple AI CLI platforms.

## 🚀 Quick Start

### Installation
```bash
# Install globally
npm install -g dsgs-spec-kit

# Or install locally
npm install dsgs-spec-kit
```

### Initialization
```bash
# Run initialization wizard
dsgs-spec-kit init

# Or auto-detect and configure
dsgs-spec-kit integrate --auto
```

### Usage
```bash
# Use spec.kit compatible commands
/speckit.dsgs.architect "Design an e-commerce system architecture"
/speckit.dsgs.agent-creator "Create an order processing agent"
/speckit.dsgs.task-decomposer "Break down user management module"

# Or use CLI commands
dsgs-spec-kit exec "/speckit.dsgs.architect 'Design a system'"
```

## 🎯 Features

### Professional Skill System
- **Architecture Design** (`dsgs-architect`): Professional system architecture design
- **Agent Creation** (`dsgs-agent-creator`): Intelligent agent creation and configuration
- **Task Decomposition** (`dsgs-task-decomposer`): Complex task breakdown and atomicization
- **Constraint Generation** (`dsgs-constraint-generator`): System constraints and specifications
- **API Consistency Check** (`dsgs-dapi-checker`): Interface consistency verification
- **Module Refactoring** (`dsgs-modulizer`): Module maturity assessment and refactoring

### Cross-Platform Support
- **Claude CLI** ✅
- **Gemini CLI** ✅
- **Qwen CLI** ✅
- **GitHub Copilot CLI** ✅
- **Cursor CLI** ✅

### Unified Interface
- spec.kit compatible slash commands (`/speckit.dsgs.*`)
- Interactive shell mode
- Programmatic API

## 📋 Installation Requirements

- Node.js 14+
- Python 3.8+
- Git version control system
- At least one supported AI CLI tool

## 🛠️ Installation

### Prerequisites
```bash
# Install Node.js (v14+)
# Visit https://nodejs.org/

# Install Python (3.8+)
# Visit https://www.python.org/

# Install Git
# Visit https://git-scm.com/
```

### Install DSGS spec.kit Integration
```bash
# Global installation (recommended)
npm install -g dsgs-spec-kit

# Verify installation
dsgs-spec-kit --version
```

### Platform-Specific Installation

#### Windows
```bash
# Install using npm
npm install -g dsgs-spec-kit

# If you encounter permission issues
npm install -g dsgs-spec-kit --unsafe-perm
```

#### macOS
```bash
# Install using npm
npm install -g dsgs-spec-kit

# If you encounter permission issues
sudo npm install -g dsgs-spec-kit
```

#### Linux
```bash
# Install using npm
npm install -g dsgs-spec-kit

# If you encounter permission issues
sudo npm install -g dsgs-spec-kit
```

## ⚙️ Configuration

### Automatic Configuration
```bash
# Auto-detect and configure installed AI CLI tools
dsgs-spec-kit integrate --auto

# Interactive configuration wizard
dsgs-spec-kit integrate --interactive
```

### Manual Configuration
```bash
# Create configuration file manually
mkdir -p ~/.dsgs
cat > ~/.dsgs/config.yaml << EOF
version: "1.0.0"
platforms:
  - name: "claude"
    enabled: true
    config_path: "~/.config/claude/skills/"
  - name: "gemini"
    enabled: false
skills:
  architect:
    command: "/speckit.dsgs.architect"
    enabled: true
EOF
```

## 🚀 Usage

### Command Line Usage

#### Skill Execution
```bash
# Execute skills using spec.kit compatible commands
dsgs-spec-kit exec "/speckit.dsgs.architect 'Design a microservice architecture'"
dsgs-spec-kit exec "/speckit.dsgs.agent-creator 'Create a project management agent'"
dsgs-spec-kit exec "/speckit.dsgs.task-decomposer 'Break down user authentication'"

# List available skills
dsgs-spec-kit list
```

#### Interactive Shell
```bash
# Start interactive shell
dsgs-spec-kit shell

# In the shell:
DSGS> /speckit.dsgs.architect "Design a system"
DSGS> /speckit.dsgs.agent-creator "Create an agent"
DSGS> help
DSGS> exit
```

### Integration with AI CLI Tools

#### Claude CLI Integration
```bash
# The integration will automatically create skill files in:
# ~/.config/claude/skills/

# After integration, you can use commands directly in Claude:
# /speckit.dsgs.architect "Design a system architecture"
```

#### Gemini CLI Integration
```bash
# The integration will automatically create extensions in:
# ~/.local/share/gemini/extensions/

# After integration, you can use commands in Gemini:
# /speckit.dsgs.task-decomposer "Break down development tasks"
```

#### Qwen CLI Integration
```bash
# The integration will automatically create plugins in:
# ~/.qwen/plugins/

# After integration, you can use commands in Qwen:
# /speckit.dsgs.agent-creator "Create an intelligent agent"
```

## 📚 API Reference

### CLI Commands

#### `dsgs-spec-kit`
```bash
dsgs-spec-kit [command] [options]
```

**Commands:**
- `init` - Initialize configuration
- `integrate` - Integrate with AI CLI tools
- `exec <command>` - Execute a skill command
- `shell` - Start interactive shell
- `list` - List available skills
- `help` - Show help information

**Options:**
- `-V, --version` - Output the version number
- `-h, --help` - Display help for command

#### `dsgs-spec-kit integrate`
```bash
dsgs-spec-kit integrate [options]
```

**Options:**
- `-a, --auto` - Automatic configuration
- `-i, --interactive` - Interactive configuration wizard
- `-c, --config <path>` - Configuration file path
- `--no-validate` - Skip integration validation

#### `dsgs-spec-kit exec`
```bash
dsgs-spec-kit exec <command>
```

**Arguments:**
- `command` - The spec.kit compatible command to execute

### Programmatic Usage
```javascript
const { SkillExecutor, CommandHandler } = require('dsgs-spec-kit');

// Create skill executor
const executor = new SkillExecutor();

// Execute skills programmatically
const result = await executor.execute('architect', 'Design a system');

// Handle results
if (result.success) {
  console.log('Result:', result.result);
} else {
  console.error('Error:', result.error);
}
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
npm test

# Run unit tests
npm run test:unit

# Run integration tests
npm run test:integration

# Run end-to-end tests
npm run test:e2e
```

### Test Coverage
```bash
# Generate test coverage report
npm run test:coverage

# View coverage report
npm run test:coverage:view
```

## 🔧 Troubleshooting

### Common Issues

#### Installation Issues
```bash
# If you encounter permission errors
sudo npm install -g dsgs-spec-kit

# If you encounter Python issues
# Make sure Python 3.8+ is installed and in PATH
python --version
```

#### Integration Issues
```bash
# Check installed AI CLI tools
dsgs-spec-kit integrate detect

# Re-run integration
dsgs-spec-kit integrate --auto
```

#### Skill Execution Issues
```bash
# Check skill availability
dsgs-spec-kit list

# Run with verbose output
dsgs-spec-kit exec "/speckit.dsgs.architect 'test'" --verbose
```

### Getting Help
- 📖 Documentation: [GitHub Docs](https://github.com/dsgs-project/spec-kit-integration/docs)
- 🐛 Issues: [GitHub Issues](https://github.com/dsgs-project/spec-kit-integration/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/dsgs-project/spec-kit-integration/discussions)

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [spec.kit](https://github.com/github/spec-kit) for the integration standard
- [DSGS Project](https://github.com/ptreezh/Dynamic-Specification-Growth-System-DSGS) for the core skills
- The open-source community for inspiration and support

## 👤 Author Information

**Project Maintainer**: ptreezh  
**Homepage**: [agentpsy.com](https://agentpsy.com)  
**Contact**: [contact@agentpsy.com](mailto:contact@agentpsy.com)  
**GitHub**: [ptreezh](https://github.com/ptreezh)

### About the Author

ptreezh is a developer focused on AI-assisted development tools and intelligent system architecture. As a core contributor to the DSGS (Dynamic Specification Growth System) project,致力于打造专业的AI技能系统，帮助开发者提升编码效率和软件质量.

### Project Vision

We believe that future software development will be more intelligent and automated. By combining professional AI skills with user-friendly toolkits, we hope to provide developers with powerful intelligent assistants, making complex system design and development tasks simpler and more efficient.

---
**DSGS spec.kit Integration** - Making AI-assisted development more professional and accessible