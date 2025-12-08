# DNASPEC 使用示例项目

这个项目展示了如何在不同场景下使用 DNASPEC (Dynamic Specification Growth System)。

## 📁 项目结构

```
dnaspec-examples/
├── basic-usage/           # 基础使用示例
├── code-review/          # 代码审查助手
├── architecture/         # 架构规范管理
├── testing/             # 测试用例生成
├── ai-integration/       # AI 助手集成
└── vs-code-extension/   # VS Code 插件示例
```

## 🚀 基础使用示例

### 1. 简单的约束生成
```javascript
// basic-usage/simple-constraint-generation.js
const { ContextEngineeringIntegration, createTCC } = require('../../src/index');

async function simpleExample() {
  console.log('=== DNASPEC 基础使用示例 ===\n');
  
  // 1. 创建 DNASPEC 实例
  const dnaspec = new ContextEngineeringIntegration({
    cognitive: {
      enableVerboseLogging: true,
      confidenceThreshold: 0.6
    }
  });
  
  // 2. 创建任务上下文
  const taskContext = createTCC(
    'example-001',
    'Create a secure user authentication system',
    'SECURITY'
  );
  
  // 3. 生成约束
  try {
    const result = await dnaspec.generateConstraints(taskContext, {
      includeReasoning: true,
      maxConstraints: 5
    });
    
    console.log('✅ 约束生成成功！');
    console.log(`📊 生成了 ${result.constraints.length} 个约束`);
    console.log(`🎯 置信度: ${(result.confidence * 100).toFixed(1)}%`);
    console.log(`⏱️  执行时间: ${result.executionTime}ms`);
    
    console.log('\n📋 生成的约束:');
    result.constraints.forEach((constraint, index) => {
      console.log(`${index + 1}. ${constraint.name} (${constraint.category})`);
      console.log(`   规则: ${constraint.rule}`);
      console.log(`   严重程度: ${constraint.severity}`);
    });
    
    if (result.reasoning.length > 0) {
      console.log('\n🧠 推理说明:');
      result.reasoning.forEach((reason, index) => {
        console.log(`${index + 1}. ${reason}`);
      });
    }
    
  } catch (error) {
    console.error('❌ 约束生成失败:', error.message);
  }
}

// 运行示例
simpleExample();
```

### 2. 批量处理
```javascript
// basic-usage/batch-processing.js
const { ContextEngineeringIntegration, createTCC } = require('../../src/index');

async function batchProcessingExample() {
  console.log('=== DNASPEC 批量处理示例 ===\n');
  
  const dnaspec = new ContextEngineeringIntegration();
  
  // 定义多个任务
  const tasks = [
    {
      id: 'auth-system',
      goal: 'Implement authentication system',
      type: 'SECURITY'
    },
    {
      id: 'api-design',
      goal: 'Design RESTful API',
      type: 'ARCHITECTURE'
    },
    {
      id: 'database-layer',
      goal: 'Create database access layer',
      type: 'PERFORMANCE'
    },
    {
      id: 'error-handling',
      goal: 'Implement error handling strategy',
      type: 'RELIABILITY'
    }
  ];
  
  console.log(`🔄 处理 ${tasks.length} 个任务...\n`);
  
  // 批量生成约束
  const results = await Promise.all(
    tasks.map(async (task) => {
      const taskContext = createTCC(task.id, task.goal, task.type);
      return dnaspec.generateConstraints(taskContext, {
        maxConstraints: 3,
        includeReasoning: false
      });
    })
  );
  
  // 输出结果
  tasks.forEach((task, index) => {
    const result = results[index];
    console.log(`${index + 1}. ${task.goal} (${task.type})`);
    console.log(`   约束数量: ${result.constraints.length}`);
    console.log(`   置信度: ${(result.confidence * 100).toFixed(1)}%`);
    console.log();
  });
  
  console.log('✅ 批量处理完成！');
}

batchProcessingExample();
```

## 🛠️ 代码审查助手示例

### 3. 智能代码审查
```javascript
// code-review/smart-code-review.js
const { ContextEngineeringIntegration, createTCC } = require('../../src/index');

class SmartCodeReviewer {
  constructor() {
    this.dnaspec = new ContextEngineeringIntegration({
      cognitive: {
        enableVerboseLogging: true,
        confidenceThreshold: 0.7
      }
    });
  }
  
  async reviewCode(sourceCode, filePath, projectContext) {
    console.log(`🔍 审查代码: ${filePath}\n`);
    
    const taskContext = createTCC(
      `review-${filePath}`,
      `Review ${filePath} for quality and best practices`,
      'CODE_REVIEW'
    );
    
    // 添加项目上下文
    taskContext.context.codebaseContext = {
      dependencies: projectContext.dependencies || [],
      architecture: projectContext.architecture || 'unknown',
      technologyStack: projectContext.technologyStack || []
    };
    
    // 添加代码片段
    taskContext.context.sourceCode = sourceCode;
    
    try {
      const result = await this.dnaspec.generateConstraints(taskContext, {
        includeReasoning: true,
        maxConstraints: 10
      });
      
      return {
        filePath,
        constraints: result.constraints,
        suggestions: result.reasoning,
        confidence: result.confidence,
        executionTime: result.executionTime
      };
      
    } catch (error) {
      console.error(`❌ 代码审查失败: ${error.message}`);
      return {
        filePath,
        constraints: [],
        suggestions: [`审查失败: ${error.message}`],
        confidence: 0,
        executionTime: 0
      };
    }
  }
  
  async reviewMultipleFiles(files, projectContext) {
    console.log(`🔄 批量审查 ${files.length} 个文件...\n`);
    
    const results = await Promise.all(
      files.map(async (file) => {
        const sourceCode = await this.readFile(file.path);
        return this.reviewCode(sourceCode, file.path, projectContext);
      })
    );
    
    // 生成汇总报告
    const totalConstraints = results.reduce((sum, r) => sum + r.constraints.length, 0);
    const avgConfidence = results.reduce((sum, r) => sum + r.confidence, 0) / results.length;
    
    console.log('📊 批量审查结果:');
    console.log(`   总约束数: ${totalConstraints}`);
    console.log(`   平均置信度: ${(avgConfidence * 100).toFixed(1)}%`);
    console.log();
    
    results.forEach((result, index) => {
      console.log(`${index + 1}. ${result.filePath}`);
      console.log(`   约束数: ${result.constraints.length}`);
      console.log(`   置信度: ${(result.confidence * 100).toFixed(1)}%`);
      
      if (result.constraints.length > 0) {
        console.log('   主要问题:');
        result.constraints.slice(0, 3).forEach((constraint, i) => {
          console.log(`     ${i + 1}. ${constraint.name} (${constraint.severity})`);
        });
      }
      console.log();
    });
    
    return results;
  }
  
  async readFile(filePath) {
    // 这里应该实现实际的文件读取逻辑
    // 为了示例，我们返回模拟的代码
    return `
function authenticateUser(username, password) {
  // TODO: 实现认证逻辑
  if (username && password) {
    return { success: true, user: { username } };
  }
  return { success: false, error: 'Invalid credentials' };
}
    `;
  }
}

// 使用示例
async function codeReviewExample() {
  const reviewer = new SmartCodeReviewer();
  
  const projectContext = {
    dependencies: ['express', 'typescript', 'jest'],
    architecture: 'layered',
    technologyStack: ['Node.js', 'TypeScript', 'Express']
  };
  
  const filesToReview = [
    { path: 'src/auth/service.ts' },
    { path: 'src/api/controller.ts' },
    { path: 'src/database/repository.ts' }
  ];
  
  await reviewer.reviewMultipleFiles(filesToReview, projectContext);
}

codeReviewExample();
```

## 🏗️ 架构规范管理示例

### 4. 动态架构规范
```javascript
// architecture/dynamic-architecture-standards.js
const { ContextEngineeringIntegration, createTCC } = require('../../src/index');

class ArchitectureStandardsManager {
  constructor() {
    this.dnaspec = new ContextEngineeringIntegration({
      cognitive: {
        enableVerboseLogging: true,
        confidenceThreshold: 0.8
      }
    });
  }
  
  async generateStandards(projectConfig) {
    console.log(`🏗️ 为项目生成架构规范: ${projectConfig.name}\n`);
    
    const taskContext = createTCC(
      `architecture-${projectConfig.type}`,
      `Generate architecture standards for ${projectConfig.name}`,
      'ARCHITECTURE'
    );
    
    // 添加项目上下文
    taskContext.context.codebaseContext = {
      dependencies: projectConfig.dependencies,
      architecture: projectConfig.architecture,
      technologyStack: projectConfig.technologyStack
    };
    
    taskContext.context.phaseContext = {
      phase: projectConfig.phase || 'DEVELOPMENT',
      teamSize: projectConfig.teamSize || 'medium',
      complexity: projectConfig.complexity || 'medium'
    };
    
    try {
      const result = await this.dnaspec.generateConstraints(taskContext, {
        includeReasoning: true,
        maxConstraints: 15
      });
      
      return {
        projectName: projectConfig.name,
        standards: this.categorizeConstraints(result.constraints),
        guidelines: result.reasoning,
        confidence: result.confidence,
        metadata: {
          generatedAt: new Date().toISOString(),
          totalConstraints: result.constraints.length,
          executionTime: result.executionTime
        }
      };
      
    } catch (error) {
      console.error(`❌ 架构规范生成失败: ${error.message}`);
      throw error;
    }
  }
  
  categorizeConstraints(constraints) {
    const categories = {
      security: [],
      performance: [],
      maintainability: [],
      scalability: [],
      reliability: [],
      other: []
    };
    
    constraints.forEach(constraint => {
      const category = this.determineCategory(constraint);
      categories[category].push(constraint);
    });
    
    return categories;
  }
  
  determineCategory(constraint) {
    const name = constraint.name.toLowerCase();
    const rule = constraint.rule.toLowerCase();
    
    if (name.includes('security') || rule.includes('security') || rule.includes('auth')) {
      return 'security';
    }
    if (name.includes('performance') || rule.includes('performance') || rule.includes('cache')) {
      return 'performance';
    }
    if (name.includes('maintain') || rule.includes('clean') || rule.includes('readable')) {
      return 'maintainability';
    }
    if (name.includes('scale') || rule.includes('distributed') || rule.includes('microservice')) {
      return 'scalability';
    }
    if (name.includes('error') || rule.includes('fail') || rule.includes('recovery')) {
      return 'reliability';
    }
    
    return 'other';
  }
  
  generateStandardsDocument(standards) {
    let document = `# ${standards.projectName} 架构规范\n\n`;
    document += `生成时间: ${standards.metadata.generatedAt}\n`;
    document += `置信度: ${(standards.confidence * 100).toFixed(1)}%\n`;
    document += `约束总数: ${standards.metadata.totalConstraints}\n\n`;
    
    // 添加分类的规范
    Object.entries(standards.standards).forEach(([category, constraints]) => {
      if (constraints.length > 0) {
        document += `## ${category.toUpperCase()}\n\n`;
        constraints.forEach((constraint, index) => {
          document += `${index + 1}. **${constraint.name}**\n`;
          document += `   - **规则**: ${constraint.rule}\n`;
          document += `   - **严重程度**: ${constraint.severity}\n`;
          document += `   - **适用任务**: ${constraint.applicableTasks.join(', ')}\n\n`;
        });
      }
    });
    
    // 添加指导原则
    if (standards.guidelines.length > 0) {
      document += `## 指导原则\n\n`;
      standards.guidelines.forEach((guideline, index) => {
        document += `${index + 1}. ${guideline}\n`;
      });
    }
    
    return document;
  }
}

// 使用示例
async function architectureStandardsExample() {
  const manager = new ArchitectureStandardsManager();
  
  const projectConfig = {
    name: 'E-Commerce Platform',
    type: 'microservices',
    dependencies: ['node.js', 'express', 'mongodb', 'redis', 'kafka'],
    architecture: 'microservices',
    technologyStack: ['Node.js', 'Express', 'MongoDB', 'Redis', 'Kafka'],
    phase: 'DEVELOPMENT',
    teamSize: 'large',
    complexity: 'high'
  };
  
  try {
    const standards = await manager.generateStandards(projectConfig);
    
    console.log('✅ 架构规范生成成功！');
    console.log(`📊 生成了 ${standards.metadata.totalConstraints} 个约束`);
    console.log(`🎯 置信度: ${(standards.confidence * 100).toFixed(1)}%`);
    
    // 显示分类统计
    console.log('\n📋 分类统计:');
    Object.entries(standards.standards).forEach(([category, constraints]) => {
      if (constraints.length > 0) {
        console.log(`   ${category}: ${constraints.length} 个约束`);
      }
    });
    
    // 生成规范文档
    const document = manager.generateStandardsDocument(standards);
    
    // 保存文档
    const fs = require('fs');
    const path = require('path');
    
    const docsDir = path.join(__dirname, 'generated-docs');
    if (!fs.existsSync(docsDir)) {
      fs.mkdirSync(docsDir, { recursive: true });
    }
    
    const docPath = path.join(docsDir, `${projectConfig.name.replace(/\s+/g, '-')}-architecture-standards.md`);
    fs.writeFileSync(docPath, document);
    
    console.log(`\n📄 规范文档已保存到: ${docPath}`);
    
  } catch (error) {
    console.error('❌ 架构规范生成失败:', error.message);
  }
}

architectureStandardsExample();
```

## 🧪 测试用例生成示例

### 5. 智能测试用例生成
```javascript
// testing/intelligent-test-generation.js
const { ContextEngineeringIntegration, createTCC } = require('../../src/index');

class IntelligentTestGenerator {
  constructor() {
    this.dnaspec = new ContextEngineeringIntegration({
      cognitive: {
        enableVerboseLogging: true,
        confidenceThreshold: 0.75
      }
    });
  }
  
  async generateTestCases(functionCode, functionSignature) {
    console.log(`🧪 为函数生成测试用例: ${functionSignature.name}\n`);
    
    const taskContext = createTCC(
      `test-${functionSignature.name}`,
      `Generate comprehensive test cases for ${functionSignature.name}`,
      'TESTING'
    );
    
    // 添加函数上下文
    taskContext.context.codebaseContext = {
      dependencies: ['jest', 'typescript', '@types/jest'],
      architecture: 'unit-testing',
      technologyStack: ['Jest', 'TypeScript']
    };
    
    // 添加函数信息
    taskContext.context.functionInfo = {
      signature: functionSignature,
      code: functionCode,
      complexity: this.calculateComplexity(functionCode),
      parameters: functionSignature.parameters || [],
      returnType: functionSignature.returnType || 'void'
    };
    
    try {
      const result = await this.dnaspec.generateConstraints(taskContext, {
        includeReasoning: true,
        maxConstraints: 12
      });
      
      return {
        functionName: functionSignature.name,
        testCases: this.convertConstraintsToTestCases(result.constraints),
        coverage: result.confidence,
        suggestions: result.reasoning,
        metadata: {
          totalConstraints: result.constraints.length,
          executionTime: result.executionTime,
          complexity: taskContext.context.functionInfo.complexity
        }
      };
      
    } catch (error) {
      console.error(`❌ 测试用例生成失败: ${error.message}`);
      throw error;
    }
  }
  
  convertConstraintsToTestCases(constraints) {
    return constraints.map((constraint, index) => {
      return {
        id: `test-${index + 1}`,
        name: constraint.name,
        description: constraint.rule,
        category: constraint.category,
        priority: this.mapSeverityToPriority(constraint.severity),
        test: this.generateTestFromConstraint(constraint),
        assertions: this.generateAssertionsFromConstraint(constraint)
      };
    });
  }
  
  generateTestFromConstraint(constraint) {
    // 根据约束生成测试代码
    const testTemplate = `
describe('${constraint.name}', () => {
  it('should satisfy the constraint: ${constraint.rule}', async () => {
    // TODO: 实现具体的测试逻辑
    // 约束: ${constraint.rule}
    // 类别: ${constraint.category}
    // 严重程度: ${constraint.severity}
    
    expect(true).toBe(true); // 占位符，需要根据实际约束实现
  });
});`;
    
    return testTemplate.trim();
  }
  
  generateAssertionsFromConstraint(constraint) {
    // 根据约束生成断言
    const assertions = [];
    
    if (constraint.category === 'SECURITY') {
      assertions.push('expect(securityMeasure).toBeImplemented()');
      assertions.push('expect(authentication).toBeRequired()');
    }
    
    if (constraint.category === 'PERFORMANCE') {
      assertions.push('expect(executionTime).toBeLessThan(maxAllowedTime)');
      assertions.push('expect(memoryUsage).toBeLessThan(maxAllowedMemory)');
    }
    
    if (constraint.category === 'RELIABILITY') {
      assertions.push('expect(errorHandling).toBeImplemented()');
      assertions.push('expect(recovery).toBePossible()');
    }
    
    return assertions;
  }
  
  mapSeverityToPriority(severity) {
    switch (severity) {
      case 'ERROR': return 'high';
      case 'WARNING': return 'medium';
      default: return 'low';
    }
  }
  
  calculateComplexity(code) {
    // 简单的复杂度计算
    const lines = code.split('\n').length;
    const branches = (code.match(/if|else|switch|case/g) || []).length;
    const loops = (code.match(/for|while|do/g) || []).length;
    
    const complexity = lines + branches * 2 + loops * 3;
    
    if (complexity < 10) return 'low';
    if (complexity < 25) return 'medium';
    return 'high';
  }
  
  generateTestSuite(testCases, functionName) {
    let testSuite = `import { ${functionName} } from '../src/${functionName.toLowerCase()}';\n\n`;
    testSuite += `describe('${functionName}', () => {\n`;
    
    testCases.forEach((testCase, index) => {
      testSuite += `  ${testCase.test}\n\n`;
    });
    
    testSuite += '});\n';
    
    return testSuite;
  }
}

// 使用示例
async function testGenerationExample() {
  const generator = new IntelligentTestGenerator();
  
  // 示例函数
  const functionCode = `
export function authenticateUser(username, password) {
  if (!username || !password) {
    throw new Error('Username and password are required');
  }
  
  if (password.length < 8) {
    throw new Error('Password must be at least 8 characters');
  }
  
  // 模拟数据库查询
  const user = database.query('SELECT * FROM users WHERE username = ?', [username]);
  
  if (!user) {
    throw new Error('User not found');
  }
  
  if (!bcrypt.compareSync(password, user.password)) {
    throw new Error('Invalid password');
  }
  
  return {
    id: user.id,
    username: user.username,
    email: user.email
  };
}
`;
  
  const functionSignature = {
    name: 'authenticateUser',
    parameters: [
      { name: 'username', type: 'string' },
      { name: 'password', type: 'string' }
    ],
    returnType: 'object'
  };
  
  try {
    const testGeneration = await generator.generateTestCases(functionCode, functionSignature);
    
    console.log('✅ 测试用例生成成功！');
    console.log(`📊 生成了 ${testGeneration.testCases.length} 个测试用例`);
    console.log(`🎯 预期覆盖率: ${(testGeneration.coverage * 100).toFixed(1)}%`);
    console.log(`⏱️  执行时间: ${testGeneration.metadata.executionTime}ms`);
    
    console.log('\n📋 生成的测试用例:');
    testGeneration.testCases.forEach((testCase, index) => {
      console.log(`${index + 1}. ${testCase.name} (${testCase.category})`);
      console.log(`   优先级: ${testCase.priority}`);
      console.log(`   描述: ${testCase.description}`);
    });
    
    // 生成完整的测试套件
    const testSuite = generator.generateTestSuite(testGeneration.testCases, functionSignature.name);
    
    // 保存测试文件
    const fs = require('fs');
    const path = require('path');
    
    const testDir = path.join(__dirname, 'generated-tests');
    if (!fs.existsSync(testDir)) {
      fs.mkdirSync(testDir, { recursive: true });
    }
    
    const testPath = path.join(testDir, `${functionSignature.name}.test.ts`);
    fs.writeFileSync(testPath, testSuite);
    
    console.log(`\n📄 测试文件已保存到: ${testPath}`);
    
    // 显示建议
    if (testGeneration.suggestions.length > 0) {
      console.log('\n💡 测试建议:');
      testGeneration.suggestions.forEach((suggestion, index) => {
        console.log(`${index + 1}. ${suggestion}`);
      });
    }
    
  } catch (error) {
    console.error('❌ 测试用例生成失败:', error.message);
  }
}

testGenerationExample();
```

## 🤖 AI 集成示例

### 6. MCP 服务器集成
```javascript
// ai-integration/mcp-server.js
const { ContextEngineeringIntegration, createTCC } = require('../../src/index');

class DNASPECMCPServer {
  constructor() {
    this.dnaspec = new ContextEngineeringIntegration({
      cognitive: {
        enableVerboseLogging: false,
        confidenceThreshold: 0.7
      }
    });
    
    this.tools = {
      'generate-constraints': this.generateConstraints.bind(this),
      'code-review': this.codeReview.bind(this),
      'architecture-standards': this.architectureStandards.bind(this),
      'test-generation': this.testGeneration.bind(this),
      'template-evolution': this.templateEvolution.bind(this)
    };
  }
  
  async generateConstraints(args) {
    const { taskType, goal, context } = args;
    
    const taskContext = createTCC(
      `mcp-${Date.now()}`,
      goal,
      taskType
    );
    
    // 添加上下文
    if (context) {
      Object.assign(taskContext.context, context);
    }
    
    const result = await this.dnaspec.generateConstraints(taskContext, {
      includeReasoning: true,
      maxConstraints: 10
    });
    
    return {
      success: true,
      constraints: result.constraints,
      confidence: result.confidence,
      reasoning: result.reasoning,
      executionTime: result.executionTime
    };
  }
  
  async codeReview(args) {
    const { code, filePath, projectContext } = args;
    
    const taskContext = createTCC(
      `mcp-review-${filePath}`,
      `Review code in ${filePath}`,
      'CODE_REVIEW'
    );
    
    taskContext.context.sourceCode = code;
    if (projectContext) {
      Object.assign(taskContext.context, projectContext);
    }
    
    const result = await this.dnaspec.generateConstraints(taskContext, {
      includeReasoning: true,
      maxConstraints: 8
    });
    
    return {
      success: true,
      review: {
        filePath,
        issues: result.constraints,
        suggestions: result.reasoning,
        confidence: result.confidence
      }
    };
  }
  
  async architectureStandards(args) {
    const { projectConfig } = args;
    
    const taskContext = createTCC(
      `mcp-architecture-${Date.now()}`,
      `Generate architecture standards for ${projectConfig.name}`,
      'ARCHITECTURE'
    );
    
    taskContext.context.codebaseContext = {
      dependencies: projectConfig.dependencies,
      architecture: projectConfig.architecture,
      technologyStack: projectConfig.technologyStack
    };
    
    const result = await this.dnaspec.generateConstraints(taskContext, {
      includeReasoning: true,
      maxConstraints: 15
    });
    
    return {
      success: true,
      standards: {
        projectName: projectConfig.name,
        constraints: result.constraints,
        guidelines: result.reasoning,
        confidence: result.confidence
      }
    };
  }
  
  async testGeneration(args) {
    const { functionCode, functionSignature } = args;
    
    const taskContext = createTCC(
      `mcp-test-${Date.now()}`,
      `Generate test cases for ${functionSignature.name}`,
      'TESTING'
    );
    
    taskContext.context.functionInfo = {
      signature: functionSignature,
      code: functionCode
    };
    
    const result = await this.dnaspec.generateConstraints(taskContext, {
      includeReasoning: true,
      maxConstraints: 12
    });
    
    return {
      success: true,
      testCases: this.convertConstraintsToTestCases(result.constraints),
      coverage: result.confidence,
      suggestions: result.reasoning
    };
  }
  
  convertConstraintsToTestCases(constraints) {
    return constraints.map((constraint, index) => ({
      id: `test-${index + 1}`,
      name: constraint.name,
      description: constraint.rule,
      category: constraint.category,
      priority: constraint.severity,
      test: this.generateTestTemplate(constraint)
    }));
  }
  
  generateTestTemplate(constraint) {
    return `// Test for ${constraint.name}
it('should satisfy: ${constraint.rule}', () => {
  // TODO: Implement test based on constraint
  expect(true).toBe(true);
});`;
  }
  
  async templateEvolution(args) {
    const { templateId, feedback, metrics } = args;
    
    // 这里应该调用 TemplateEvolver
    // 为了示例，我们返回模拟结果
    
    return {
      success: true,
      evolution: {
        templateId,
        currentEffectiveness: metrics?.effectiveness || 0.8,
        suggestedImprovements: [
          'Consider adding more specific validation rules',
          'Update template based on recent user feedback'
        ],
        nextReviewDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
      }
    };
  }
  
  // MCP 服务器处理逻辑
  async handleRequest(toolName, args) {
    const tool = this.tools[toolName];
    
    if (!tool) {
      return {
        success: false,
        error: `Unknown tool: ${toolName}`
      };
    }
    
    try {
      return await tool(args);
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
}

// 使用示例
async function mcpServerExample() {
  const server = new DNASPECMCPServer();
  
  // 模拟 MCP 请求
  const requests = [
    {
      tool: 'generate-constraints',
      args: {
        taskType: 'SECURITY',
        goal: 'Create secure authentication system',
        context: {
          projectType: 'web-app',
          teamSize: 'medium'
        }
      }
    },
    {
      tool: 'code-review',
      args: {
        code: 'function authenticateUser(username, password) { /* ... */ }',
        filePath: 'auth.service.ts',
        projectContext: {
          dependencies: ['express', 'bcrypt'],
          architecture: 'mvc'
        }
      }
    },
    {
      tool: 'architecture-standards',
      args: {
        projectConfig: {
          name: 'Microservices API',
          type: 'microservices',
          dependencies: ['node.js', 'express', 'mongodb'],
          architecture: 'microservices',
          technologyStack: ['Node.js', 'Express', 'MongoDB']
        }
      }
    }
  ];
  
  console.log('🤖 DNASPEC MCP 服务器示例\n');
  
  for (const request of requests) {
    console.log(`📤 处理请求: ${request.tool}`);
    
    const result = await server.handleRequest(request.tool, request.args);
    
    if (result.success) {
      console.log('✅ 请求处理成功');
      
      if (result.constraints) {
        console.log(`   生成约束: ${result.constraints.length} 个`);
      }
      
      if (result.review) {
        console.log(`   发现问题: ${result.review.issues.length} 个`);
      }
      
      if (result.standards) {
        console.log(`   架构规范: ${result.standards.constraints.length} 个`);
      }
      
      if (result.testCases) {
        console.log(`   测试用例: ${result.testCases.length} 个`);
      }
      
    } else {
      console.log(`❌ 请求处理失败: ${result.error}`);
    }
    
    console.log('');
  }
}

mcpServerExample();
```

## 🚀 运行示例

### 运行基础示例
```bash
cd dnaspec-examples
node basic-usage/simple-constraint-generation.js
```

### 运行代码审查示例
```bash
node code-review/smart-code-review.js
```

### 运行架构规范示例
```bash
node architecture/dynamic-architecture-standards.js
```

### 运行测试生成示例
```bash
node testing/intelligent-test-generation.js
```

### 运行 MCP 服务器示例
```bash
node ai-integration/mcp-server.js
```

## 📝 自定义配置

### 环境变量配置
```bash
# .env 文件
DNASPEC_LOG_LEVEL=debug
DNASPEC_MAX_CONSTRAINTS=20
DNASPEC_CONFIDENCE_THRESHOLD=0.7
DNASPEC_ENABLE_REASONING=true
```

### 配置文件
```javascript
// dnaspec.config.js
module.exports = {
  cognitive: {
    enableVerboseLogging: process.env.DNASPEC_LOG_LEVEL === 'debug',
    confidenceThreshold: parseFloat(process.env.DNASPEC_CONFIDENCE_THRESHOLD) || 0.7,
    maxExecutionTime: 30000
  },
  constraintGeneration: {
    maxConstraints: parseInt(process.env.DNASPEC_MAX_CONSTRAINTS) || 10,
    includeReasoning: process.env.DNASPEC_ENABLE_REASONING === 'true'
  }
};
```

## 🎯 下一步

1. **选择适合您的使用场景**
2. **运行相应的示例**
3. **根据需要修改配置**
4. **集成到您的项目中**

通过这些示例，您可以快速了解如何在不同场景下使用 DNASPEC 来提升开发效率和代码质量。

---
**示例项目版本**: 2.0.0  
**更新时间**: 2025-08-10  
**兼容性**: DNASPEC v2.0.0+