# API Documentation

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Core Classes](#core-classes)
- [CLI Commands](#cli-commands)
- [Configuration](#configuration)
- [Examples](#examples)

## Overview

The DSGS spec.kit Integration provides a comprehensive API for integrating professional AI skills with various AI CLI tools. The API is designed to be simple to use while providing powerful features.

## Installation

### Node.js Environment
```javascript
// Install via npm
npm install dsgs-spec-kit

// Import modules
const { SkillExecutor, CommandHandler, CliDetector } = require('dsgs-spec-kit');
```

### Python Environment
The integration requires Python 3.8+ for executing DSGS skills:
```bash
# Python dependencies are automatically managed
# but you can manually install if needed:
pip install pyyaml requests
```

## Core Classes

### SkillExecutor
The main class for executing DSGS skills.

#### Constructor
```javascript
const executor = new SkillExecutor(options);
```

**Options:**
- `pythonPath` (string): Path to Python executable
- `timeout` (number): Execution timeout in milliseconds
- `verbose` (boolean): Enable verbose logging

#### Methods

##### execute(skillName, params)
Execute a DSGS skill.

**Parameters:**
- `skillName` (string): Name of the skill to execute
- `params` (string): Parameters for the skill

**Returns:** Promise<Object>
```javascript
const result = await executor.execute('architect', 'Design a system');
// Returns: { success: true, result: {...}, skill: 'architect' }
```

##### getAvailableSkills()
Get a list of available skills.

**Returns:** Array<string>
```javascript
const skills = executor.getAvailableSkills();
// Returns: ['architect', 'agent-creator', 'task-decomposer', ...]
```

### CommandHandler
Handles spec.kit compatible commands.

#### Constructor
```javascript
const handler = new CommandHandler(skillExecutor, commandParser);
```

#### Methods

##### handleCommand(commandString)
Handle a spec.kit command string.

**Parameters:**
- `commandString` (string): The command to handle

**Returns:** Promise<Object>
```javascript
const result = await handler.handleCommand('/speckit.dsgs.architect "Design a system"');
```

##### getAvailableCommands()
Get a list of available commands.

**Returns:** Array<string>
```javascript
const commands = handler.getAvailableCommands();
```

### CliDetector
Detects installed AI CLI tools.

#### Methods

##### detectAll()
Detect all supported AI CLI tools.

**Returns:** Promise<Object>
```javascript
const tools = await detector.detectAll();
// Returns: { claude: {...}, gemini: {...}, ... }
```

##### detectClaude()
Detect Claude CLI specifically.

**Returns:** Promise<Object>
```javascript
const claude = await detector.detectClaude();
```

## CLI Commands

### dsgs-spec-kit
Main CLI entry point.

#### Usage
```bash
dsgs-spec-kit [command] [options]
```

#### Commands

##### init
Initialize the integration.

```bash
dsgs-spec-kit init [options]
```

**Options:**
- `-c, --config <path>`: Configuration file path
- `-f, --force`: Force re-initialization

##### integrate
Integrate with AI CLI tools.

```bash
dsgs-spec-kit integrate [options]
```

**Options:**
- `-a, --auto`: Automatic configuration
- `-i, --interactive`: Interactive configuration wizard
- `--no-validate`: Skip integration validation

##### exec
Execute a skill command.

```bash
dsgs-spec-kit exec <command>
```

**Arguments:**
- `command`: The command to execute

##### shell
Start interactive shell.

```bash
dsgs-spec-kit shell
```

##### list
List available skills.

```bash
dsgs-spec-kit list
```

## Configuration

### Configuration File
The integration uses a YAML configuration file located at `~/.dsgs/config.yaml` by default.

#### Structure
```yaml
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
  agent-creator:
    command: "/speckit.dsgs.agent-creator"
    enabled: true
settings:
  timeout: 30000
  retries: 3
  verbose: false
```

### Environment Variables
- `DSGS_CONFIG_PATH`: Path to configuration file
- `DSGS_PYTHON_PATH`: Path to Python executable
- `DSGS_VERBOSE`: Enable verbose logging

## Examples

### Basic Usage
```javascript
const { SkillExecutor } = require('dsgs-spec-kit');

async function basicExample() {
  const executor = new SkillExecutor();
  
  // Execute architecture design skill
  const result = await executor.execute('architect', 'Design an e-commerce platform');
  
  if (result.success) {
    console.log('Architecture Design:', result.result);
  } else {
    console.error('Error:', result.error);
  }
}
```

### Command Handling
```javascript
const { CommandHandler, SkillExecutor } = require('dsgs-spec-kit');

async function commandExample() {
  const executor = new SkillExecutor();
  const handler = new CommandHandler(executor);
  
  // Handle spec.kit command
  const result = await handler.handleCommand('/speckit.dsgs.agent-creator "Create a chatbot agent"');
  
  console.log('Command Result:', result);
}
```

### Integration Detection
```javascript
const { CliDetector } = require('dsgs-spec-kit');

async function detectionExample() {
  const detector = new CliDetector();
  
  // Detect all installed tools
  const tools = await detector.detectAll();
  
  console.log('Installed Tools:');
  for (const [name, info] of Object.entries(tools)) {
    if (info.installed) {
      console.log(`  ✅ ${name}: ${info.version}`);
    } else {
      console.log(`  ❌ ${name}: Not installed`);
    }
  }
}
```

### Configuration Management
```javascript
const fs = require('fs');
const yaml = require('js-yaml');

function configExample() {
  // Load configuration
  const configPath = process.env.DSGS_CONFIG_PATH || '~/.dsgs/config.yaml';
  const config = yaml.load(fs.readFileSync(configPath, 'utf8'));
  
  console.log('Current Configuration:', config);
  
  // Modify configuration
  config.platforms.find(p => p.name === 'claude').enabled = true;
  
  // Save configuration
  fs.writeFileSync(configPath, yaml.dump(config));
}
```