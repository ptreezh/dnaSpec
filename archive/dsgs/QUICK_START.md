# DNASPEC 快速开始指南

## 🚀 5分钟快速上手

### 安装
```bash
# 1. 克隆项目
git clone <repository-url>
cd dnaspec

# 2. 安装依赖
npm install

# 3. 验证安装
npm test
```

### 基础使用

#### 方式一：JavaScript/TypeScript 项目
```javascript
// 1. 导入 DNASPEC
const { ContextEngineeringIntegration, createTCC } = require('./src/index');

// 2. 创建实例
const dnaspec = new ContextEngineeringIntegration();

// 3. 创建任务上下文
const taskContext = createTCC(
  'my-task',
  'Implement secure authentication',
  'SECURITY'
);

// 4. 生成约束
dnaspec.generateConstraints(taskContext).then(result => {
  console.log('生成的约束:', result.constraints);
  console.log('置信度:', result.confidence);
});
```

#### 方式二：命令行工具
```bash
# 生成 API 契约
node src/modules/contract/cli-simple.js generate \
  --source ./src \
  --output ./contract.yaml

# 运行测试
npm test

# 查看项目状态
npm run view:state
```

#### 方式三：AI 助手集成
```json
// 在 AI 助手中配置 MCP
{
  "mcpServers": {
    "dnaspec": {
      "command": "node",
      "args": ["./src/mcp/server.js"]
    }
  }
}
```

## 🎯 主要使用场景

### 1. 代码审查助手
```javascript
// 自动代码审查
const reviewResult = await dnaspec.generateConstraints({
  taskId: 'code-review',
  taskType: 'CODE_REVIEW',
  context: {
    relevantConstraints: ['security', 'performance'],
    codebaseContext: {
      dependencies: ['express', 'typescript'],
      architecture: 'mvc'
    }
  }
});
```

### 2. 架构规范管理
```javascript
// 生成架构约束
const architectureRules = await dnaspec.generateConstraints({
  taskId: 'architecture-design',
  taskType: 'ARCHITECTURE',
  context: {
    projectType: 'microservices',
    teamSize: 'large'
  }
});
```

### 3. 测试用例生成
```javascript
// 生成测试约束
const testConstraints = await dnaspec.generateConstraints({
  taskId: 'test-generation',
  taskType: 'TESTING',
  context: {
    sourceCode: functionCode,
    complexity: 'medium'
  }
});
```

## 🔧 配置选项

### 基础配置
```javascript
const config = {
  cognitive: {
    enableVerboseLogging: true,
    confidenceThreshold: 0.6
  }
};

const dnaspec = new ContextEngineeringIntegration(config);
```

### 高级配置
```javascript
const advancedConfig = {
  cognitive: {
    enableVerboseLogging: false,
    confidenceThreshold: 0.8,
    maxExecutionTime: 30000
  },
  neuralField: {
    dimension: 256,
    learningRate: 0.1
  }
};
```

## 📚 用户界面

### 1. 编程接口 (API)
- **适合**: 开发者集成
- **复杂度**: 中等
- **灵活性**: 高

### 2. 命令行工具 (CLI)
- **适合**: 快速测试、脚本化
- **复杂度**: 低
- **灵活性**: 中等

### 3. VS Code 插件
- **适合**: 日常开发
- **复杂度**: 低
- **灵活性**: 中等

### 4. MCP 工具
- **适合**: AI 助手集成
- **复杂度**: 中等
- **灵活性**: 高

## 🐛 常见问题

### 安装失败
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### 测试失败
```bash
npm test -- --verbose
# 查看详细错误信息
```

### 内存不足
```bash
node --max-old-space-size=4096 index.js
```

## 📞 获取帮助

- 📖 完整文档: [USAGE_GUIDE.md](./USAGE_GUIDE.md)
- 🐛 问题报告: [GitHub Issues](https://github.com/dnaspec/issues)
- 💬 社区讨论: [Discord](https://discord.gg/dnaspec)

## 🎉 开始使用！

选择适合您的使用方式，立即开始使用 DNASPEC 提升您的开发体验！

---
**快速开始版本**: 2.0.0  
**更新时间**: 2025-08-10