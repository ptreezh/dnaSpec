# Contract模块 - 类型定义

## 📋 类型定义概述

本模块包含Contract模块的所有类型定义，采用分层设计，确保类型安全和可维护性。

## 🎯 类型分层

### 📢 对外接口类型 (public.ts)
定义模块对外的公共接口类型，确保向后兼容性。

### 🔒 内部实现类型 (internal.ts)  
定义模块内部使用的类型，不对外暴露。

### 🔄 共享类型 (shared.ts)
定义模块间共享的通用类型。

## 🚀 快速开始

### 导入类型

```typescript
// 导入公共类型
import type {
  GenerateContractRequest,
  ValidateContractRequest,
  ValidationResult,
  ApiContract
} from './types/public';

// 导入内部类型 (仅模块内部使用)
import type {
  SourceAnalysis,
  ValidationConfig,
  GeneratorConfig
} from './types/internal';

// 导入共享类型
import type {
  ErrorLocation,
  Severity,
  ValidationRule
} from './types/shared';
```

### 使用示例

```typescript
import type { GenerateContractRequest } from './types/public';

const request: GenerateContractRequest = {
  sourcePaths: ['./src/api'],
  format: 'openapi',
  options: {
    includePrivate: false,
    includeExamples: true,
    validate: true,
    version: '1.0.0'
  }
};
```

## 📊 主要类型定义

### 契约生成相关

```typescript
/**
 * 契约生成请求
 */
export interface GenerateContractRequest {
  /** 源代码路径数组 */
  sourcePaths: string[];
  /** 输出路径 (可选) */
  outputPath?: string;
  /** 输出格式 */
  format: 'openapi' | 'json-schema' | 'markdown';
  /** 生成选项 */
  options: GenerationOptions;
}

/**
 * 生成选项
 */
export interface GenerationOptions {
  /** 是否包含私有成员 */
  includePrivate: boolean;
  /** 是否包含示例 */
  includeExamples: boolean;
  /** 是否验证生成的契约 */
  validate: boolean;
  /** 契约版本 */
  version: string;
  /** 是否推断类型 */
  inferTypes?: boolean;
  /** 是否严格验证 */
  strictValidation?: boolean;
}

/**
 * 契约生成响应
 */
export interface GenerateContractResponse {
  /** 生成是否成功 */
  success: boolean;
  /** 生成的契约 */
  contract: ApiContract;
  /** 警告信息 */
  warnings: string[];
  /** 元数据 */
  metadata: GenerationMetadata;
}
```

### 契约验证相关

```typescript
/**
 * 契约验证请求
 */
export interface ValidateContractRequest {
  /** 要验证的契约 */
  contract: ApiContract;
  /** 实现代码路径 (可选) */
  implementationPath?: string;
  /** 验证级别 */
  validationLevel: 'strict' | 'normal' | 'lenient';
  /** 自定义验证规则 */
  rules: ValidationRule[];
}

/**
 * 验证结果
 */
export interface ValidationResult {
  /** 验证是否通过 */
  isValid: boolean;
  /** 验证分数 (0-100) */
  score: number;
  /** 错误列表 */
  errors: ValidationError[];
  /** 警告列表 */
  warnings: ValidationWarning[];
  /** 建议列表 */
  suggestions: string[];
  /** 统计信息 */
  statistics: ValidationStatistics;
  /** 元数据 */
  metadata: ValidationMetadata;
}

/**
 * 验证错误
 */
export interface ValidationError {
  /** 错误ID */
  id: string;
  /** 错误类型 */
  type: ErrorType;
  /** 严重程度 */
  severity: Severity;
  /** 错误消息 */
  message: string;
  /** 错误位置 */
  location: ErrorLocation;
  /** 详细信息 */
  details?: any;
  /** 修复建议 */
  suggestions: string[];
  /** 违反的规则 */
  rule: string;
}
```

### 契约数据模型

```typescript
/**
 * API契约
 */
export interface ApiContract {
  /** 契约元数据 */
  metadata: ContractMetadata;
  /** API端点 */
  endpoints: ApiEndpoint[];
  /** 数据模型 */
  dataModels: DataModel[];
  /** Webhook定义 */
  webhooks: WebhookDefinition[];
  /** 事件定义 */
  events: EventDefinition[];
  /** 安全定义 */
  security: SecurityDefinition[];
  /** 服务器定义 */
  servers: ServerDefinition[];
  /** 标签定义 */
  tags: TagDefinition[];
  /** 版本兼容性 */
  compatibility: CompatibilityMatrix;
  /** 示例集合 */
  examples: ExampleCollection;
}

/**
 * API端点
 */
export interface ApiEndpoint {
  /** API路径 */
  path: string;
  /** HTTP方法 */
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  /** 端点摘要 */
  summary: string;
  /** 端点描述 */
  description: string;
  /** 参数定义 */
  parameters: Parameter[];
  /** 请求体 */
  requestBody?: RequestBody;
  /** 响应定义 */
  responses: ResponseDefinition[];
  /** 安全要求 */
  security: SecurityRequirement[];
  /** 标签 */
  tags: string[];
  /** 是否废弃 */
  deprecated?: boolean;
  /** 示例 */
  examples: Example[];
  /** 外部文档 */
  externalDocs?: ExternalDocs;
}

/**
 * 数据模型
 */
export interface DataModel {
  /** 模型名称 */
  name: string;
  /** 模型类型 */
  type: 'object' | 'array' | 'string' | 'number' | 'boolean' | 'integer';
  /** 模型描述 */
  description: string;
  /** 属性定义 */
  properties?: PropertyDefinition[];
  /** 必需属性 */
  required?: string[];
  /** 额外属性 */
  additionalProperties?: boolean | DataModel;
  /** 数组项类型 */
  items?: DataModel;
  /** 枚举值 */
  enum?: any[];
  /** 格式 */
  format?: string;
  /** 默认值 */
  default?: any;
  /** 示例 */
  example?: any;
  /** 是否废弃 */
  deprecated?: boolean;
  /** 外部文档 */
  externalDocs?: ExternalDocs;
}
```

### 版本管理相关

```typescript
/**
 * 版本管理请求
 */
export interface CreateVersionRequest {
  /** 版本号 */
  version: string;
  /** 版本描述 */
  description: string;
  /** 契约内容 */
  contract: ApiContract;
  /** 是否为破坏性变更 */
  isBreakingChange: boolean;
  /** 迁移指南 */
  migrationGuide?: string;
}

/**
 * 版本创建响应
 */
export interface CreateVersionResponse {
  /** 创建是否成功 */
  success: boolean;
  /** 版本号 */
  version: string;
  /** 破坏性变更 */
  breakingChanges: BreakingChange[];
  /** 是否需要迁移 */
  migrationRequired: boolean;
  /** 元数据 */
  metadata: VersionMetadata;
}

/**
 * 兼容性矩阵
 */
export interface CompatibilityMatrix {
  /** 当前版本 */
  current: string;
  /** 支持的版本 */
  supported: string[];
  /** 废弃的版本 */
  deprecated: string[];
  /** 不兼容的版本 */
  incompatible: string[];
  /** 破坏性变更 */
  breakingChanges: BreakingChange[];
  /** 迁移路径 */
  migrationPaths: MigrationPath[];
}
```

### 实现验证相关

```typescript
/**
 * 实现验证请求
 */
export interface ValidateImplementationRequest {
  /** 契约版本 */
  contractVersion?: string;
  /** 实现代码路径 */
  implementationPath: string;
  /** 验证级别 */
  validationLevel: 'strict' | 'normal' | 'lenient';
}

/**
 * 实现验证响应
 */
export interface ValidateImplementationResponse {
  /** 验证是否通过 */
  isValid: boolean;
  /** 兼容性结果 */
  compatibility: CompatibilityResult;
  /** 违规列表 */
  violations: ContractViolation[];
  /** 建议 */
  recommendations: Recommendation[];
  /** 元数据 */
  metadata: ImplementationMetadata;
}

/**
 * 契约违规
 */
export interface ContractViolation {
  /** 违规ID */
  id: string;
  /** 违规类型 */
  type: 'missing_endpoint' | 'missing_parameter' | 'type_mismatch' | 'missing_response' | 'security_violation';
  /** 严重程度 */
  severity: Severity;
  /** 违规消息 */
  message: string;
  /** 违规位置 */
  location: ErrorLocation;
  /** 修复建议 */
  suggestion: string;
  /** 影响分析 */
  impact: ImpactAnalysis;
}
```

## 🔄 枚举类型

### 错误类型

```typescript
/**
 * 错误类型枚举
 */
export enum ErrorType {
  /** 结构错误 */
  STRUCTURE = 'structure',
  /** 端点错误 */
  ENDPOINT = 'endpoint',
  /** 参数错误 */
  PARAMETER = 'parameter',
  /** 响应错误 */
  RESPONSE = 'response',
  /** 模型错误 */
  MODEL = 'model',
  /** 安全错误 */
  SECURITY = 'security',
  /** 命名错误 */
  NAMING = 'naming',
  /** 引用错误 */
  REFERENCE = 'reference',
  /** 格式错误 */
  FORMAT = 'format',
  /** 业务逻辑错误 */
  BUSINESS = 'business'
}
```

### 严重程度

```typescript
/**
 * 严重程度枚举
 */
export enum Severity {
  /** 低 */
  LOW = 'low',
  /** 中 */
  MEDIUM = 'medium',
  /** 高 */
  HIGH = 'high',
  /** 严重 */
  CRITICAL = 'critical'
}
```

### 输出格式

```typescript
/**
 * 输出格式枚举
 */
export enum OutputFormat {
  /** OpenAPI 3.0 */
  OPENAPI = 'openapi',
  /** JSON Schema */
  JSON_SCHEMA = 'json-schema',
  /** Markdown */
  MARKDOWN = 'markdown'
}
```

## 📋 工具类型

### 通用工具类型

```typescript
/**
 * 深度部分类型
 */
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

/**
 * 只读类型
 */
export type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

/**
 * 可选类型
 */
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

/**
 * 必需类型
 */
export type Required<T, K extends keyof T> = T & Required<Pick<T, K>>;
```

### 验证相关工具类型

```typescript
/**
 * 验证规则类型
 */
export type ValidationRuleType = 'structure' | 'endpoint' | 'model' | 'security' | 'naming';

/**
 * 验证级别类型
 */
export type ValidationLevel = 'strict' | 'normal' | 'lenient';

/**
 * 验证条件操作符
 */
export type ValidationOperator = 
  | 'exists' 
  | 'not_exists' 
  | 'equals' 
  | 'not_equals' 
  | 'matches' 
  | 'not_matches' 
  | 'contains' 
  | 'not_contains';
```

## 🎯 使用建议

### 类型导入

```typescript
// 推荐的方式：按需导入类型
import type { GenerateContractRequest } from './types/public';
import type { ValidationResult } from './types/public';

// 避免的方式：导入所有类型
// import * as Types from './types';
```

### 类型保护

```typescript
// 使用类型保护函数
function isValidationError(error: any): error is ValidationError {
  return error && typeof error.id === 'string' && typeof error.message === 'string';
}

// 使用类型保护
function handleError(error: unknown) {
  if (isValidationError(error)) {
    console.log(`Validation error: ${error.message}`);
    console.log(`Location: ${error.location.component}`);
  } else {
    console.log('Unknown error:', error);
  }
}
```

### 类型断言

```typescript
// 谨慎使用类型断言
const contract = data as ApiContract;

// 更安全的方式：类型检查
if (isApiContract(data)) {
  const contract = data;
  // 使用contract
}
```

## 📚 相关文档

- [公共类型](./public.ts) - 对外接口类型定义
- [内部类型](./internal.ts) - 内部实现类型定义
- [共享类型](./shared.ts) - 通用类型定义
- [工具类型](./utils.ts) - 工具类型定义

---

**类型维护**: DNASPEC契约团队  
**最后更新**: 2025-08-11  
**版本**: 2.0