# DSGS Contract模块 - TDD重构设计文档

## 📋 设计原则

### 🎯 核心约束
- **单文件限制**: 每个实现文件不超过300行
- **树状结构**: 自顶向下的模块化分解
- **金字塔原则**: 每个目录有清晰的README说明
- **Agent友好**: 接口设计便于AI理解和操作

### 🏗️ 架构设计

```
src/modules/contract/
├── README.md                           # 模块总览 (金字塔顶部)
├── index.ts                           # 统一导出接口
├── types/                             # 类型定义层
│   ├── README.md                      # 类型说明
│   ├── index.ts                       # 类型导出
│   ├── public.ts                      # 对外接口类型
│   ├── internal.ts                    # 内部类型
│   └── shared.ts                      # 共享类型
├── core/                              # 核心实现层
│   ├── README.md                      # 核心模块说明
│   ├── ContractManager.ts             # 主管理器 (<300行)
│   ├── generator/                     # 生成器子模块
│   │   ├── README.md                  # 生成器说明
│   │   ├── index.ts                   # 生成器接口
│   │   ├── SourceAnalyzer.ts          # 源码分析器
│   │   ├── TypeExtractor.ts           # 类型提取器
│   │   ├── EndpointExtractor.ts       # 端点提取器
│   │   └── ModelExtractor.ts          # 模型提取器
│   ├── validator/                     # 验证器子模块
│   │   ├── README.md                  # 验证器说明
│   │   ├── index.ts                   # 验证器接口
│   │   ├── StructureValidator.ts      # 结构验证器
│   │   ├── EndpointValidator.ts       # 端点验证器
│   │   ├── ModelValidator.ts          # 模型验证器
│   │   └── ReferenceValidator.ts      # 引用验证器
│   ├── version/                       # 版本管理子模块
│   │   ├── README.md                  # 版本管理说明
│   │   ├── index.ts                   # 版本管理接口
│   │   ├── VersionManager.ts          # 版本管理器
│   │   ├── CompatibilityChecker.ts    # 兼容性检查器
│   │   └── BreakingChangeDetector.ts  # 破坏性变更检测器
│   └── implementation/                # 实现验证子模块
│       ├── README.md                  # 实现验证说明
│       ├── index.ts                   # 实现验证接口
│       ├── CodeAnalyzer.ts            # 代码分析器
│       └── ComplianceChecker.ts       # 合规性检查器
├── utils/                             # 工具层
│   ├── README.md                      # 工具说明
│   ├── index.ts                       # 工具导出
│   ├── TypeHelpers.ts                 # 类型工具
│   ├── ValidationHelpers.ts           # 验证工具
│   └── FileHelpers.ts                 # 文件工具
├── config/                            # 配置层
│   ├── README.md                      # 配置说明
│   ├── index.ts                       # 配置导出
│   ├── default.config.ts              # 默认配置
│   └── validation.config.ts            # 验证配置
└── test/                              # 测试层 (TDD驱动)
    ├── README.md                      # 测试说明
    ├── unit/                          # 单元测试
    │   ├── core/                      # 核心模块测试
    │   ├── generator/                 # 生成器测试
    │   ├── validator/                 # 验证器测试
    │   ├── version/                   # 版本管理测试
    │   └── implementation/            # 实现验证测试
    ├── integration/                   # 集成测试
    │   ├── ContractIntegration.test.ts # 契约集成测试
    │   └── EndToEnd.test.ts          # 端到端测试
    └── performance/                   # 性能测试
        ├── GenerationPerformance.test.ts # 生成性能测试
        └── ValidationPerformance.test.ts # 验证性能测试
```

## 📊 模块职责划分

### 🎯 主入口层 (ContractManager)
```typescript
// 职责：统一入口，协调各个子模块
// 约束：<300行，只负责协调，不包含具体实现
export class ContractManager {
  generateContract(request: GenerateContractRequest): Promise<GenerateContractResponse>
  validateContract(request: ValidateContractRequest): Promise<ValidationResult>
  createVersion(request: CreateVersionRequest): Promise<CreateVersionResponse>
  validateImplementation(request: ValidateImplementationRequest): Promise<ValidateImplementationResponse>
}
```

### 🔧 生成器模块 (generator/)
```typescript
// 职责：从源代码生成API契约
// 分解：每个提取器专注单一职责
export interface ContractGenerator {
  generate(config: GenerateContractConfig): Promise<GeneratedContract>
}

export interface SourceAnalyzer {
  analyze(paths: string[]): Promise<SourceAnalysis>
}

export interface TypeExtractor {
  extract(analysis: SourceAnalysis): Promise<TypeDefinitions>
}

export interface EndpointExtractor {
  extract(analysis: SourceAnalysis): Promise<EndpointDefinitions>
}

export interface ModelExtractor {
  extract(analysis: SourceAnalysis): Promise<ModelDefinitions>
}
```

### ✅ 验证器模块 (validator/)
```typescript
// 职责：验证契约的正确性和一致性
// 分解：每个验证器专注特定验证类型
export interface ContractValidator {
  validate(contract: ApiContract, config: ValidationConfig): Promise<ValidationResult>
}

export interface StructureValidator {
  validate(contract: ApiContract): Promise<StructureValidationResult>
}

export interface EndpointValidator {
  validate(endpoints: ApiEndpoint[]): Promise<EndpointValidationResult>
}

export interface ModelValidator {
  validate(models: DataModel[]): Promise<ModelValidationResult>
}

export interface ReferenceValidator {
  validate(contract: ApiContract): Promise<ReferenceValidationResult>
}
```

### 📈 版本管理模块 (version/)
```typescript
// 职责：管理契约版本和兼容性
// 分解：版本管理和兼容性检查分离
export interface VersionManager {
  createVersion(version: string, contract: ApiContract): Promise<VersionInfo>
  getVersion(version: string): Promise<ApiContract>
  listVersions(): Promise<VersionInfo[]>
}

export interface CompatibilityChecker {
  checkCompatibility(from: ApiContract, to: ApiContract): Promise<CompatibilityResult>
}

export interface BreakingChangeDetector {
  detectChanges(oldContract: ApiContract, newContract: ApiContract): Promise<BreakingChange[]>
}
```

### 🔍 实现验证模块 (implementation/)
```typescript
// 职责：验证实现代码与契约的一致性
// 分解：代码分析和合规性检查分离
export interface ImplementationValidator {
  validateImplementation(contract: ApiContract, codePath: string): Promise<ImplementationValidationResult>
}

export interface CodeAnalyzer {
  analyzeCode(codePath: string): Promise<CodeAnalysis>
}

export interface ComplianceChecker {
  checkCompliance(contract: ApiContract, analysis: CodeAnalysis): Promise<ComplianceResult>
}
```

## 📋 接口设计原则

### 🎯 对外接口 (保持兼容)
```typescript
// 保持现有接口，确保向后兼容
export interface GenerateContractRequest {
  sourcePaths: string[];
  outputPath?: string;
  format: 'openapi' | 'json-schema' | 'markdown';
  options: GenerationOptions;
}

export interface ValidateContractRequest {
  contract: ApiContract;
  implementationPath?: string;
  validationLevel: 'strict' | 'normal' | 'lenient';
  rules: ValidationRule[];
}

export interface ValidationResult {
  isValid: boolean;
  score: number;
  errors: ValidationError[];
  warnings: ValidationWarning[];
  suggestions: string[];
  statistics: ValidationStatistics;
  metadata: ValidationMetadata;
}
```

### 🔧 内部接口 (模块化设计)
```typescript
// 内部接口设计，便于测试和维护
export interface GenerateContractConfig {
  sourcePaths: string[];
  format: OutputFormat;
  options: GenerationOptions;
  analyzers: AnalyzerConfig;
  extractors: ExtractorConfig;
}

export interface SourceAnalysis {
  files: string[];
  types: Map<string, TypeInfo>;
  interfaces: Map<string, InterfaceInfo>;
  classes: Map<string, ClassInfo>;
  functions: Map<string, FunctionInfo>;
}

export interface ValidationConfig {
  level: ValidationLevel;
  rules: ValidationRule[];
  validators: ValidatorConfig;
}
```

## 🧪 TDD测试策略

### 📊 测试分层设计
```
测试金字塔 (70-20-10):
├── 单元测试 (70%) - 每个组件独立测试
├── 集成测试 (20%) - 组件间交互测试
└── E2E测试 (10%) - 完整流程测试
```

### 🎯 测试文件结构
```
test/
├── unit/                              # 单元测试
│   ├── ContractManager.test.ts        # 主管理器测试
│   ├── generator/                     # 生成器测试
│   │   ├── SourceAnalyzer.test.ts     # 源码分析器测试
│   │   ├── TypeExtractor.test.ts      # 类型提取器测试
│   │   ├── EndpointExtractor.test.ts  # 端点提取器测试
│   │   └── ModelExtractor.test.ts     # 模型提取器测试
│   ├── validator/                     # 验证器测试
│   │   ├── StructureValidator.test.ts # 结构验证器测试
│   │   ├── EndpointValidator.test.ts  # 端点验证器测试
│   │   ├── ModelValidator.test.ts     # 模型验证器测试
│   │   └── ReferenceValidator.test.ts # 引用验证器测试
│   ├── version/                       # 版本管理测试
│   │   ├── VersionManager.test.ts     # 版本管理器测试
│   │   ├── CompatibilityChecker.test.ts # 兼容性检查器测试
│   │   └── BreakingChangeDetector.test.ts # 破坏性变更检测器测试
│   └── implementation/                # 实现验证测试
│       ├── CodeAnalyzer.test.ts       # 代码分析器测试
│       └── ComplianceChecker.test.ts  # 合规性检查器测试
├── integration/                       # 集成测试
│   ├── ContractIntegration.test.ts    # 契约集成测试
│   ├── GeneratorIntegration.test.ts   # 生成器集成测试
│   ├── ValidatorIntegration.test.ts   # 验证器集成测试
│   └── EndToEnd.test.ts              # 端到端测试
└── performance/                       # 性能测试
    ├── GenerationPerformance.test.ts  # 生成性能测试
    ├── ValidationPerformance.test.ts  # 验证性能测试
    └── MemoryUsage.test.ts           # 内存使用测试
```

### 📋 测试用例设计示例

#### ContractManager测试
```typescript
describe('ContractManager', () => {
  let manager: ContractManager;
  
  beforeEach(() => {
    manager = new ContractManager();
  });
  
  describe('generateContract', () => {
    it('should generate contract from source code', async () => {
      const request: GenerateContractRequest = {
        sourcePaths: ['./test/fixtures/simple-api'],
        format: 'openapi',
        options: {
          includePrivate: false,
          includeExamples: true,
          validate: true,
          version: '1.0.0'
        }
      };
      
      const result = await manager.generateContract(request);
      
      expect(result.success).toBe(true);
      expect(result.contract).toBeDefined();
      expect(result.contract.metadata.version).toBe('1.0.0');
    });
    
    it('should handle invalid source paths', async () => {
      const request: GenerateContractRequest = {
        sourcePaths: ['./nonexistent'],
        format: 'openapi',
        options: {
          includePrivate: false,
          includeExamples: true,
          validate: true,
          version: '1.0.0'
        }
      };
      
      const result = await manager.generateContract(request);
      
      expect(result.success).toBe(false);
      expect(result.warnings).toContain('Source path not found');
    });
  });
  
  describe('validateContract', () => {
    it('should validate contract structure', async () => {
      const contract = createTestContract();
      const request: ValidateContractRequest = {
        contract,
        validationLevel: 'normal',
        rules: []
      };
      
      const result = await manager.validateContract(request);
      
      expect(result.isValid).toBe(true);
      expect(result.score).toBeGreaterThan(80);
    });
  });
});
```

#### SourceAnalyzer测试
```typescript
describe('SourceAnalyzer', () => {
  let analyzer: SourceAnalyzer;
  
  beforeEach(() => {
    analyzer = new SourceAnalyzer();
  });
  
  describe('analyze', () => {
    it('should analyze TypeScript source files', async () => {
      const result = await analyzer.analyze(['./test/fixtures/simple-api']);
      
      expect(result.files.length).toBeGreaterThan(0);
      expect(result.types.size).toBeGreaterThan(0);
      expect(result.interfaces.size).toBeGreaterThan(0);
      expect(result.classes.size).toBeGreaterThan(0);
    });
    
    it('should extract type definitions', async () => {
      const result = await analyzer.analyze(['./test/fixtures/types.ts']);
      
      const userType = result.types.get('User');
      expect(userType).toBeDefined();
      expect(userType?.kind).toBe('interface');
    });
    
    it('should handle empty directories', async () => {
      const result = await analyzer.analyze(['./test/fixtures/empty']);
      
      expect(result.files).toHaveLength(0);
      expect(result.types.size).toBe(0);
      expect(result.interfaces.size).toBe(0);
    });
  });
});
```

## 📊 性能和质量目标

### 🎯 性能指标
- **生成时间**: 大型项目 < 5秒
- **验证时间**: 单个契约 < 1秒
- **内存使用**: < 100MB
- **文件大小**: 每个文件 < 300行

### 📋 质量指标
- **测试覆盖率**: > 90%
- **代码复杂度**: 每个函数 < 10行
- **圈复杂度**: 每个函数 < 5
- **重复代码**: < 3%

### 🔧 开发规范
- **命名规范**: 遵循统一契约文档
- **注释规范**: JSDoc完整注释
- **错误处理**: 统一错误处理机制
- **日志记录**: 结构化日志输出

## 🚀 实施计划

### 📅 第一周：基础架构
- [ ] 创建目录结构
- [ ] 定义类型接口
- [ ] 实现ContractManager
- [ ] 编写基础测试

### 📅 第二周：生成器模块
- [ ] 实现SourceAnalyzer
- [ ] 实现TypeExtractor
- [ ] 实现EndpointExtractor
- [ ] 实现ModelExtractor

### 📅 第三周：验证器模块
- [ ] 实现StructureValidator
- [ ] 实现EndpointValidator
- [ ] 实现ModelValidator
- [ ] 实现ReferenceValidator

### 📅 第四周：集成优化
- [ ] 实现版本管理
- [ ] 实现实现验证
- [ ] 性能优化
- [ ] 集成测试

## 🎯 成功标准

### ✅ 功能标准
- [ ] 所有现有功能正常工作
- [ ] 向后兼容性100%
- [ ] 新功能按预期工作
- [ ] 错误处理完善

### ✅ 质量标准
- [ ] 测试覆盖率 > 90%
- [ ] 所有文件 < 300行
- [ ] 代码审查通过
- [ ] 性能测试通过

### ✅ 文档标准
- [ ] 每个目录有README
- [ ] API文档完整
- [ ] 使用指南清晰
- [ ] 示例代码可用

---

**文档维护**: DSGS架构团队  
**最后更新**: 2025-08-11  
**版本**: 2.0