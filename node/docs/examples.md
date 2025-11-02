# Usage Examples

## Table of Contents
- [Quick Start Examples](#quick-start-examples)
- [Advanced Usage](#advanced-usage)
- [Integration Examples](#integration-examples)
- [Customization](#customization)

## Quick Start Examples

### 1. Basic Installation and Initialization
```bash
# Install the package globally
npm install -g dsgs-spec-kit

# Run automatic initialization
dsgs-spec-kit integrate --auto

# List available skills
dsgs-spec-kit list
```

### 2. Executing Skills via CLI
```bash
# Design system architecture
dsgs-spec-kit exec "/speckit.dsgs.architect 'Design a microservice architecture for e-commerce'"

# Create intelligent agents
dsgs-spec-kit exec "/speckit.dsgs.agent-creator 'Create a customer service chatbot agent'"

# Decompose complex tasks
dsgs-spec-kit exec "/speckit.dsgs.task-decomposer 'Break down user authentication implementation'"
```

### 3. Interactive Shell Usage
```bash
# Start interactive shell
dsgs-spec-kit shell

# In the shell:
DSGS> /speckit.dsgs.architect "Design a system"
DSGS> /speckit.dsgs.agent-creator "Create an agent"
DSGS> help
DSGS> exit
```

## Advanced Usage

### 1. Programmatic Skill Execution
```javascript
const { SkillExecutor } = require('dsgs-spec-kit');

async function advancedSkillExecution() {
  // Create executor with custom options
  const executor = new SkillExecutor({
    timeout: 60000,  // 60 second timeout
    verbose: true,   // Enable verbose logging
    retries: 3       // Retry failed executions 3 times
  });
  
  try {
    // Execute multiple skills
    const architecture = await executor.execute('architect', 'Design a scalable web application');
    const agents = await executor.execute('agent-creator', 'Create frontend and backend development agents');
    const tasks = await executor.execute('task-decomposer', 'Break down the implementation plan');
    
    console.log('Architecture:', architecture.result);
    console.log('Agents:', agents.result);
    console.log('Tasks:', tasks.result);
  } catch (error) {
    console.error('Execution failed:', error.message);
  }
}
```

### 2. Custom Command Handling
```javascript
const { CommandHandler, SkillExecutor } = require('dsgs-spec-kit');

class CustomCommandHandler extends CommandHandler {
  constructor(skillExecutor) {
    super(skillExecutor);
    this.customCommands = new Map();
  }
  
  registerCustomCommand(name, handler) {
    this.customCommands.set(name, handler);
  }
  
  async handleCommand(commandString) {
    // Check for custom commands first
    const customCommand = this.parseCustomCommand(commandString);
    if (customCommand && this.customCommands.has(customCommand.name)) {
      const handler = this.customCommands.get(customCommand.name);
      return await handler(customCommand.params);
    }
    
    // Fall back to standard command handling
    return await super.handleCommand(commandString);
  }
  
  parseCustomCommand(commandString) {
    const match = commandString.match(/^\/custom\.([a-zA-Z0-9-]+)(?:\s+(.+))?$/);
    if (match) {
      return {
        name: match[1],
        params: match[2] || ''
      };
    }
    return null;
  }
}

// Usage
async function customCommandExample() {
  const executor = new SkillExecutor();
  const handler = new CustomCommandHandler(executor);
  
  // Register custom command
  handler.registerCustomCommand('hello', async (params) => {
    return {
      success: true,
      result: `Hello ${params || 'World'}!`
    };
  });
  
  // Handle custom command
  const result = await handler.handleCommand('/custom.hello "DSGS User"');
  console.log(result.result); // "Hello DSGS User!"
}
```

### 3. Batch Skill Execution
```javascript
const { SkillExecutor } = require('dsgs-spec-kit');

class BatchSkillExecutor {
  constructor(skillExecutor) {
    this.skillExecutor = skillExecutor;
  }
  
  async executeBatch(skillRequests) {
    const results = [];
    const errors = [];
    
    // Execute skills in parallel
    const promises = skillRequests.map(async (request, index) => {
      try {
        const result = await this.skillExecutor.execute(request.skill, request.params);
        results[index] = { index, success: true, result };
      } catch (error) {
        errors[index] = { index, success: false, error: error.message };
      }
    });
    
    await Promise.all(promises);
    
    return {
      results: results.filter(r => r),
      errors: errors.filter(e => e),
      total: skillRequests.length
    };
  }
  
  async executeSequence(skillRequests) {
    const results = [];
    const errors = [];
    
    // Execute skills in sequence
    for (let i = 0; i < skillRequests.length; i++) {
      const request = skillRequests[i];
      try {
        const result = await this.skillExecutor.execute(request.skill, request.params);
        results.push({ index: i, success: true, result });
      } catch (error) {
        errors.push({ index: i, success: false, error: error.message });
      }
    }
    
    return {
      results,
      errors,
      total: skillRequests.length
    };
  }
}

// Usage
async function batchExecutionExample() {
  const executor = new SkillExecutor();
  const batchExecutor = new BatchSkillExecutor(executor);
  
  const skillRequests = [
    { skill: 'architect', params: 'Design authentication system' },
    { skill: 'agent-creator', params: 'Create auth service agent' },
    { skill: 'task-decomposer', params: 'Break down auth implementation' }
  ];
  
  // Execute in parallel
  console.log('Executing skills in parallel...');
  const parallelResults = await batchExecutor.executeBatch(skillRequests);
  console.log(`Completed: ${parallelResults.results.length}/${parallelResults.total}`);
  
  // Execute in sequence
  console.log('Executing skills in sequence...');
  const sequenceResults = await batchExecutor.executeSequence(skillRequests);
  console.log(`Completed: ${sequenceResults.results.length}/${sequenceResults.total}`);
}
```

## Integration Examples

### 1. Claude CLI Integration
```bash
# Auto-detect and configure Claude CLI
dsgs-spec-kit integrate --auto

# Verify integration
dsgs-spec-kit integrate validate --platform claude

# Use in Claude:
# /speckit.dsgs.architect "Design a system"
```

### 2. Gemini CLI Integration
```bash
# Configure Gemini CLI integration
dsgs-spec-kit integrate --interactive

# Select Gemini when prompted
# Follow the configuration wizard

# Use in Gemini:
# /speckit.dsgs.task-decomposer "Break down development tasks"
```

### 3. Multi-Platform Integration
```javascript
const { CliDetector, ConfigGenerator } = require('dsgs-spec-kit');

async function multiPlatformIntegration() {
  const detector = new CliDetector();
  const generator = new ConfigGenerator();
  
  // Detect all installed platforms
  console.log('Detecting installed AI CLI tools...');
  const detectedTools = await detector.detectAll();
  
  // Generate configuration for all detected tools
  const config = generator.generate(detectedTools);
  
  // Enable all detected platforms
  config.platforms.forEach(platform => {
    if (platform.installed) {
      platform.enabled = true;
      console.log(`✅ Enabled ${platform.name}`);
    }
  });
  
  // Save configuration
  const configPath = './.dsgs/multi-platform-config.yaml';
  generator.save(config, configPath);
  
  console.log(`Configuration saved to ${configPath}`);
  console.log('You can now use DSGS skills with all detected platforms!');
}
```

## Customization

### 1. Custom Skill Configuration
```yaml
# ~/.dsgs/config.yaml
version: "1.0.0"
skills:
  architect:
    command: "/speckit.dsgs.architect"
    enabled: true
    custom_prompts:
      - "Focus on cloud-native architecture"
      - "Consider microservices design patterns"
  agent-creator:
    command: "/speckit.dsgs.agent-creator"
    enabled: true
    custom_templates:
      - name: "dev-ops-agent"
        description: "DevOps automation agent"
      - name: "security-agent"
        description: "Security monitoring agent"
settings:
  custom_context: |
    You are an expert in software architecture and AI agent design.
    Always provide practical, implementable solutions.
```

### 2. Custom Platform Integration
```javascript
const { CliDetector } = require('dsgs-spec-kit');

class CustomPlatformDetector extends CliDetector {
  constructor() {
    super();
    // Register custom platform detector
    this.detectors['custom-ai'] = this.detectCustomAI.bind(this);
  }
  
  async detectCustomAI() {
    try {
      const version = await this.executeCommand('custom-ai --version');
      const installPath = await this.getInstallPath('custom-ai');
      
      return {
        installed: true,
        version: version.trim(),
        installPath: installPath,
        configPath: this.getCustomAIConfigPath()
      };
    } catch (error) {
      return {
        installed: false,
        error: error.message
      };
    }
  }
  
  getCustomAIConfigPath() {
    const home = process.env.HOME || process.env.USERPROFILE;
    return `${home}/.custom-ai/plugins/`;
  }
  
  async executeCommand(command) {
    const { exec } = require('child_process');
    return new Promise((resolve, reject) => {
      exec(command, (error, stdout, stderr) => {
        if (error) {
          reject(error);
        } else {
          resolve(stdout || stderr);
        }
      });
    });
  }
}

// Usage
async function customPlatformExample() {
  const detector = new CustomPlatformDetector();
  const result = await detector.detectCustomAI();
  
  if (result.installed) {
    console.log(`Custom AI detected: ${result.version}`);
  } else {
    console.log('Custom AI not installed');
  }
}
```

### 3. Performance Optimization
```javascript
const { SkillExecutor } = require('dsgs-spec-kit');

class OptimizedSkillExecutor extends SkillExecutor {
  constructor(options = {}) {
    super(options);
    this.cache = new Map();
    this.stats = {
      hits: 0,
      misses: 0,
      averageExecutionTime: 0
    };
  }
  
  async execute(skillName, params) {
    // Create cache key
    const cacheKey = `${skillName}:${params}`;
    
    // Check cache first
    if (this.cache.has(cacheKey)) {
      this.stats.hits++;
      return this.cache.get(cacheKey);
    }
    
    this.stats.misses++;
    const startTime = Date.now();
    
    // Execute skill
    const result = await super.execute(skillName, params);
    
    // Cache successful results
    const executionTime = Date.now() - startTime;
    if (result.success) {
      this.cache.set(cacheKey, result);
      
      // Update statistics
      this.stats.averageExecutionTime = 
        (this.stats.averageExecutionTime * (this.stats.hits + this.stats.misses - 1) + executionTime) / 
        (this.stats.hits + this.stats.misses);
    }
    
    return result;
  }
  
  getCacheStats() {
    return {
      ...this.stats,
      cacheSize: this.cache.size,
      hitRate: this.stats.hits / (this.stats.hits + this.stats.misses)
    };
  }
  
  clearCache() {
    this.cache.clear();
    this.stats = {
      hits: 0,
      misses: 0,
      averageExecutionTime: 0
    };
  }
}

// Usage
async function optimizedExecutionExample() {
  const executor = new OptimizedSkillExecutor({ timeout: 30000 });
  
  // First execution (cache miss)
  const result1 = await executor.execute('architect', 'Design a system');
  console.log('First execution:', result1.success);
  
  // Second execution (cache hit)
  const result2 = await executor.execute('architect', 'Design a system');
  console.log('Second execution:', result2.success);
  
  // Check cache statistics
  const stats = executor.getCacheStats();
  console.log('Cache Statistics:', stats);
}
```