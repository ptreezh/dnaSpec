# Contract模块 - 核心实现

## 📋 核心模块概述

Core模块是Contract模块的核心实现层，采用模块化设计，每个子模块职责单一，文件大小控制在300行以内。

## 🎯 模块结构

```
core/
├── ContractManager.ts         # 主管理器 (<300行)
├── generator/                  # 生成器子模块
│   ├── SourceAnalyzer.ts      # 源码分析器
│   ├── TypeExtractor.ts       # 类型提取器
│   ├── EndpointExtractor.ts   # 端点提取器
│   └── ModelExtractor.ts      # 模型提取器
├── validator/                  # 验证器子模块
│   ├── StructureValidator.ts  # 结构验证器
│   ├── EndpointValidator.ts   # 端点验证器
│   ├── ModelValidator.ts      # 模型验证器
│   └── ReferenceValidator.ts  # 引用验证器
├── version/                    # 版本管理子模块
│   ├── VersionManager.ts      # 版本管理器
│   ├── CompatibilityChecker.ts # 兼容性检查器
│   └── BreakingChangeDetector.ts # 破坏性变更检测器
└── implementation/             # 实现验证子模块
    ├── CodeAnalyzer.ts        # 代码分析器
    └── ComplianceChecker.ts   # 合规性检查器
```

## 🚀 核心设计原则

### 🎯 单一职责原则
每个组件只负责一个特定功能，确保代码可维护性。

### 📏 文件大小控制
每个TypeScript文件不超过300行，确保代码可读性。

### 🔧 接口分离
每个组件只暴露必要的接口，减少耦合度。

### 🧪 TDD驱动
所有组件都先编写测试，再实现功能。

## 📊 主要组件

### ContractManager (主管理器)

**职责**: 统一入口，协调各个子模块

**特点**:
- 只负责协调，不包含具体实现
- 提供统一的对外接口
- 处理错误处理和日志记录

**接口**:
```typescript
export class ContractManager {
  generateContract(request: GenerateContractRequest): Promise<GenerateContractResponse>
  validateContract(request: ValidateContractRequest): Promise<ValidationResult>
  createVersion(request: CreateVersionRequest): Promise<CreateVersionResponse>
  validateImplementation(request: ValidateImplementationRequest): Promise<ValidateImplementationResponse>
}
```

### Generator (生成器子模块)

**职责**: 从源代码生成API契约

**组件分解**:
- **SourceAnalyzer**: 分析源代码结构
- **TypeExtractor**: 提取类型定义
- **EndpointExtractor**: 提取API端点
- **ModelExtractor**: 提取数据模型

**特点**:
- 支持增量分析
- 智能类型推断
- 装饰器识别
- 错误恢复机制

### Validator (验证器子模块)

**职责**: 验证契约的正确性和一致性

**组件分解**:
- **StructureValidator**: 验证契约结构
- **EndpointValidator**: 验证端点规范
- **ModelValidator**: 验证数据模型
- **ReferenceValidator**: 验证引用完整性

**特点**:
- 可配置验证级别
- 自定义验证规则
- 详细的错误报告
- 性能优化

### Version (版本管理子模块)

**职责**: 管理契约版本和兼容性

**组件分解**:
- **VersionManager**: 版本创建和管理
- **CompatibilityChecker**: 兼容性检查
- **BreakingChangeDetector**: 破坏性变更检测

**特点**:
- 语义化版本控制
- 自动兼容性分析
- 迁移路径生成
- 版本回滚支持

### Implementation (实现验证子模块)

**职责**: 验证实现代码与契约的一致性

**组件分解**:
- **CodeAnalyzer**: 代码结构分析
- **ComplianceChecker**: 合规性检查

**特点**:
- 静态代码分析
- 智能模式匹配
- 自动修复建议
- 性能分析

## 🔧 使用示例

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

// 验证契约
const validationResult = await manager.validateContract({
  contract: result.contract,
  validationLevel: 'normal',
  rules: []
});
```

### 高级使用

```typescript
import { ContractManager } from './core/ContractManager';

const manager = new ContractManager({
  logging: {
    level: 'debug',
    performance: true
  },
  cache: {
    enabled: true,
    ttl: 3600
  }
});

// 批量处理
const results = await Promise.all([
  manager.generateContract(request1),
  manager.generateContract(request2),
  manager.generateContract(request3)
]);

// 版本管理
const versionResult = await manager.createVersion({
  version: '2.0.0',
  description: 'Major version update',
  contract: updatedContract,
  isBreakingChange: true,
  migrationGuide: '# Migration Guide'
});

// 实现验证
const implementationResult = await manager.validateImplementation({
  contractVersion: '2.0.0',
  implementationPath: './src',
  validationLevel: 'strict'
});
```

## 📊 性能特性

### 🚀 性能优化
- **增量分析**: 只分析变更的文件
- **智能缓存**: 缓存分析结果
- **并行处理**: 多线程并行分析
- **懒加载**: 按需加载组件

### 📈 性能指标
- **生成时间**: 大型项目 < 5秒
- **验证时间**: 单个契约 < 1秒
- **内存使用**: < 100MB
- **并发处理**: 支持100+并发请求

## 🧪 测试策略

### 📊 测试覆盖
- **单元测试**: 每个组件独立测试
- **集成测试**: 组件间交互测试
- **性能测试**: 响应时间和内存使用测试
- **错误测试**: 异常情况处理测试

### 🎯 测试质量
- **测试覆盖率**: > 90%
- **边界测试**: 覆盖所有边界条件
- **属性测试**: 使用随机数据测试
- **突变测试**: 验证测试质量

## 🔧 配置选项

### 全局配置

```typescript
interface ContractManagerConfig {
  /** 日志配置 */
  logging?: {
    level: 'debug' | 'info' | 'warn' | 'error';
    performance?: boolean;
  };
  /** 缓存配置 */
  cache?: {
    enabled: boolean;
    ttl: number;
  };
  /** 性能配置 */
  performance?: {
    maxConcurrency: number;
    timeout: number;
  };
}
```

### 生成器配置

```typescript
interface GeneratorConfig {
  /** 分析器配置 */
  analyzers: {
    includeDecorators: boolean;
    includeJSDoc: boolean;
    inferTypes: boolean;
  };
  /** 提取器配置 */
  extractors: {
    extractEndpoints: boolean;
    extractModels: boolean;
    extractWebhooks: boolean;
  };
}
```

### 验证器配置

```typescript
interface ValidatorConfig {
  /** 验证级别 */
  level: 'strict' | 'normal' | 'lenient';
  /** 验证器开关 */
  validators: {
    structure: boolean;
    endpoints: boolean;
    models: boolean;
    references: boolean;
  };
  /** 自定义规则 */
  customRules: ValidationRule[];
}
```

## 📋 错误处理

### 错误分类
- **输入错误**: 无效的请求参数
- **分析错误**: 源码分析失败
- **验证错误**: 契约验证失败
- **系统错误**: 内部系统错误

### 错误恢复
- **重试机制**: 自动重试失败操作
- **降级处理**: 部分功能失败时的降级
- **错误隔离**: 错误不会影响其他功能
- **详细日志**: 记录详细错误信息

## 📚 相关文档

- [生成器模块](./generator/README.md) - 契约生成器详细说明
- [验证器模块](./validator/README.md) - 契约验证器详细说明
- [版本管理](./version/README.md) - 版本管理模块说明
- [实现验证](./implementation/README.md) - 实现验证模块说明

## 🤝 开发指南

### 添加新组件
1. 在相应子模块目录创建新文件
2. 实现必要的接口
3. 编写完整的测试用例
4. 更新子模块的index.ts
5. 更新相关文档

### 性能优化
1. 使用性能分析工具识别瓶颈
2. 优化算法和数据结构
3. 添加缓存机制
4. 实现并行处理

### 错误处理
1. 定义清晰的错误类型
2. 实现错误恢复机制
3. 添加详细的错误日志
4. 提供用户友好的错误信息

---

**核心模块维护**: DSGS架构团队  
**最后更新**: 2025-08-11  
**版本**: 2.0