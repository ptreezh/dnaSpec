# Contract模块 - 核心契约管理

## 📋 模块概述

Contract模块是DNASPEC系统的核心组件，负责API契约的生成、验证、版本管理和实现一致性检查。本模块采用TDD驱动开发，遵循单一职责原则，每个组件文件不超过300行。

## 🎯 核心功能

### 🔧 契约生成 (Contract Generation)
- 从TypeScript源代码自动生成API契约
- 支持OpenAPI 3.0、JSON Schema、Markdown格式
- 智能类型提取和端点识别
- 支持控制器装饰器和路由配置

### ✅ 契约验证 (Contract Validation)
- 结构完整性验证
- 端点规范性检查
- 数据模型一致性验证
- 引用完整性检查
- 最佳实践建议

### 📈 版本管理 (Version Management)
- 契约版本创建和管理
- 兼容性检查和破坏性变更检测
- 版本迁移路径生成
- 废弃功能管理

### 🔍 实现验证 (Implementation Validation)
- 代码与契约一致性检查
- 实现完整性验证
- 合规性检查和建议
- 自动化修复建议

## 🚀 快速开始

### 基本使用

```typescript
import { ContractManager } from './core/ContractManager';

const manager = new ContractManager();

// 生成契约
const generateRequest = {
  sourcePaths: ['./src/api'],
  format: 'openapi',
  options: {
    includePrivate: false,
    includeExamples: true,
    validate: true,
    version: '1.0.0'
  }
};

const result = await manager.generateContract(generateRequest);
console.log('Generated contract:', result.contract);

// 验证契约
const validateRequest = {
  contract: result.contract,
  validationLevel: 'normal',
  rules: []
};

const validationResult = await manager.validateContract(validateRequest);
console.log('Validation result:', validationResult.isValid);
```

### 高级使用

```typescript
import { ContractManager, GenerationConfig, ValidationConfig } from './core/ContractManager';

const manager = new ContractManager();

// 自定义生成配置
const config: GenerationConfig = {
  sourcePaths: ['./src/api'],
  format: 'openapi',
  options: {
    includePrivate: false,
    includeExamples: true,
    validate: true,
    version: '1.0.0'
  },
  analyzers: {
    includeDecorators: true,
    includeJSDoc: true,
    inferTypes: true
  },
  extractors: {
    extractEndpoints: true,
    extractModels: true,
    extractWebhooks: false
  }
};

const result = await manager.generateContract(config);

// 自定义验证配置
const validationConfig: ValidationConfig = {
  level: 'strict',
  rules: [
    {
      id: 'custom-rule',
      name: 'Custom Validation Rule',
      description: 'Custom business logic validation',
      type: 'business',
      severity: 'error',
      enabled: true,
      condition: {
        field: 'customField',
        operator: 'exists'
      }
    }
  ],
  validators: {
    structure: true,
    endpoints: true,
    models: true,
    references: true,
    custom: true
  }
};

const validationResult = await manager.validateContract({
  contract: result.contract,
  ...validationConfig
});
```

## 📊 API接口

### ContractManager

#### generateContract
```typescript
generateContract(request: GenerateContractRequest): Promise<GenerateContractResponse>
```
生成API契约

**参数**:
- `request.sourcePaths`: 源代码路径数组
- `request.format`: 输出格式 (openapi | json-schema | markdown)
- `request.options`: 生成选项

**返回**: 生成结果，包含契约和元数据

#### validateContract
```typescript
validateContract(request: ValidateContractRequest): Promise<ValidationResult>
```
验证API契约

**参数**:
- `request.contract`: 要验证的契约
- `request.validationLevel`: 验证级别 (strict | normal | lenient)
- `request.rules`: 自定义验证规则

**返回**: 验证结果，包含错误、警告和建议

#### createVersion
```typescript
createVersion(request: CreateVersionRequest): Promise<CreateVersionResponse>
```
创建契约新版本

**参数**:
- `request.version`: 版本号
- `request.contract`: 契约内容
- `request.description`: 版本描述

**返回**: 版本创建结果

#### validateImplementation
```typescript
validateImplementation(request: ValidateImplementationRequest): Promise<ValidateImplementationResponse>
```
验证实现代码与契约的一致性

**参数**:
- `request.contractVersion`: 契约版本
- `request.implementationPath`: 实现代码路径
- `request.validationLevel`: 验证级别

**返回**: 实现验证结果

## 🔧 配置选项

### 生成配置

```typescript
interface GenerationOptions {
  includePrivate: boolean;        // 是否包含私有成员
  includeExamples: boolean;       // 是否包含示例
  validate: boolean;             // 是否验证生成的契约
  version: string;               // 契约版本
  inferTypes: boolean;           // 是否推断类型
  strictValidation: boolean;     // 是否严格验证
}
```

### 验证配置

```typescript
interface ValidationConfig {
  level: 'strict' | 'normal' | 'lenient';  // 验证级别
  rules: ValidationRule[];                 // 自定义规则
  implementationPath?: string;            // 实现代码路径
}
```

## 📋 输出格式

### OpenAPI 3.0
```yaml
openapi: 3.0.0
info:
  title: DNASPEC API
  version: 1.0.0
  description: Dynamic Specification Growth System API
paths:
  /api/users:
    get:
      summary: Get users
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
```

### JSON Schema
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "DNASPEC API Contract",
  "version": "1.0.0",
  "definitions": {
    "User": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" }
      },
      "required": ["id", "name"]
    }
  }
}
```

### Markdown
```markdown
# DNASPEC API Contract

**Version**: 1.0.0

## API Endpoints

### GET /api/users
**Summary**: Get users

**Responses**:
- **200**: Successful response

## Data Models

### User
**Type**: object

**Properties**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | User ID |
| name | string | Yes | User name |
```

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
npm test

# 运行单元测试
npm run test:unit

# 运行集成测试
npm run test:integration

# 运行性能测试
npm run test:performance
```

### 测试覆盖率

```bash
# 生成测试覆盖率报告
npm run test:coverage

# 查看覆盖率详情
open coverage/lcov-report/index.html
```

## 🔍 故障排除

### 常见问题

**1. 契约生成失败**
```typescript
// 检查源代码路径
const files = await fs.readdir('./src/api');
console.log('Source files:', files);

// 检查TypeScript配置
const tsConfig = require('./tsconfig.json');
console.log('TypeScript config:', tsConfig);
```

**2. 验证错误过多**
```typescript
// 降低验证级别
const result = await manager.validateContract({
  contract,
  validationLevel: 'lenient'
});

// 查看详细错误信息
result.errors.forEach(error => {
  console.log(`${error.type}: ${error.message}`);
  console.log(`Location: ${error.location.component}`);
  console.log(`Suggestions: ${error.suggestions.join(', ')}`);
});
```

**3. 性能问题**
```typescript
// 使用增量生成
const result = await manager.generateContract({
  sourcePaths: ['./src/api'],
  format: 'openapi',
  options: {
    incremental: true,
    cache: true
  }
});

// 启用性能日志
const manager = new ContractManager({
  logging: {
    level: 'debug',
    performance: true
  }
});
```

## 📚 相关文档

- [类型定义](./types/README.md) - 详细的类型定义说明
- [核心实现](./core/README.md) - 核心模块实现细节
- [生成器模块](./core/generator/README.md) - 契约生成器详细说明
- [验证器模块](./core/validator/README.md) - 契约验证器详细说明
- [版本管理](./core/version/README.md) - 版本管理模块说明
- [实现验证](./core/implementation/README.md) - 实现验证模块说明
- [工具函数](./utils/README.md) - 工具函数说明
- [配置说明](./config/README.md) - 配置选项说明

## 🤝 贡献指南

1. 遵循TDD开发流程
2. 保持文件大小 < 300行
3. 确保测试覆盖率 > 90%
4. 遵循命名规范
5. 更新相关文档

---

**模块维护**: DNASPEC契约团队  
**最后更新**: 2025-08-11  
**版本**: 2.0