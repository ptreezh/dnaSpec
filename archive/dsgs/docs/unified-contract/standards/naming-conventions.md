# DSGS命名规范

## 🎯 命名原则

DSGS系统采用统一的命名规范，确保代码、API、数据模型的一致性和可读性。

### 核心原则
- **一致性**：整个系统使用相同的命名风格
- **可读性**：名称应该清晰表达其用途
- **简洁性**：避免冗余和过长的名称
- **标准化**：遵循行业标准和最佳实践

### 命名风格
| 类型 | 风格 | 示例 | 用途 |
|------|------|------|------|
| **类名** | PascalCase | `TaskContextCapsule` | 类、接口、类型 |
| **方法名** | camelCase | `generateConstraints` | 方法、函数 |
| **变量名** | camelCase | `taskContext` | 变量、属性 |
| **常量名** | SCREAMING_SNAKE_CASE | `MAX_RETRY_COUNT` | 常量、枚举 |
| **文件名** | kebab-case | `task-context-capsule.ts` | 文件、目录 |
| **API路径** | kebab-case | `/api/health-check` | API端点 |
| **数据库表名** | snake_case | `task_context_capsules` | 数据库表 |
| **环境变量** | SCREAMING_SNAKE_CASE | `DATABASE_URL` | 环境变量 |

## 📋 详细规范

### 1. 类和接口命名

#### 类名规范
```typescript
// ✅ 正确示例
class TaskContextCapsule {}
class ConstraintGenerator {}
class HealthCheckService {}

// ❌ 错误示例
class taskContextCapsule {}       // 首字母小写
class Constraint_Generator {}     // 使用下划线
class constraintgenerator {}      // 全部小写
```

#### 接口命名
```typescript
// ✅ 正确示例
interface ApiResponse<T> {}
interface HealthStatus {}
interface McpRequest {}

// ❌ 错误示例
interface apiResponse<T> {}       // 首字母小写
interface API_Response {}        // 使用下划线
interface Api_Response {}         // 混合风格
```

#### 泛型类型参数
```typescript
// ✅ 正确示例
interface Repository<T> {}
interface Builder<T, R> {}
type Handler<T = any> = (input: T) => void;

// ❌ 错误示例
interface Repository<t> {}        // 单个小写字母
interface Builder<TYPE, RESULT> {} // 过长的泛型名
```

### 2. 方法和函数命名

#### 动词前缀规范
```typescript
// ✅ 正确示例
class ConstraintService {
  // 获取类方法
  getConstraints(): Constraint[]
  getConstraintById(id: string): Constraint
  
  // 创建类方法
  createConstraint(input: CreateConstraintInput): Constraint
  generateConstraints(context: TaskContext): GeneratedConstraint[]
  
  // 更新类方法
  updateConstraint(id: string, updates: UpdateConstraintInput): Constraint
  
  // 删除类方法
  deleteConstraint(id: string): void
  
  // 检查类方法
  validateConstraint(constraint: Constraint): ValidationResult
  checkHealth(): HealthStatus
  
  // 转换类方法
  convertToDto(entity: Constraint): ConstraintDto
  parseFromJson(json: string): Constraint
}

// ❌ 错误示例
class ConstraintService {
  constraints(): Constraint[]           // 缺少动词
  makeConstraint(input: any): Constraint // 不明确的动词
  constraintData(): Constraint[]        // 名词而非动词
}
```

#### 布尔值方法命名
```typescript
// ✅ 正确示例
class Validator {
  isValid(): boolean
  hasConstraints(): boolean
  canGenerate(): boolean
  shouldRetry(): boolean
  isHealthy(): boolean
  supportsFeature(feature: string): boolean
}

// ❌ 错误示例
class Validator {
  valid(): boolean                    // 不完整
  constraintExist(): boolean          // 语法错误
  generateable(): boolean            // 不自然的词汇
}
```

### 3. 变量和属性命名

#### 变量命名
```typescript
// ✅ 正确示例
const taskContext: TaskContextCapsule = new TaskContextCapsule();
const constraintList: Constraint[] = [];
const maxRetryCount: number = 3;
const isHealthy: boolean = true;
const apiUrl: string = 'https://api.example.com';

// ❌ 错误示例
const tc: TaskContextCapsule = new TaskContextCapsule();    // 过度缩写
const data: any = {};                                         // 过于通用
const flag: boolean = true;                                   // 不明确的名称
const temp: string = 'temporary';                             // 临时变量应有意义
```

#### 属性命名
```typescript
// ✅ 正确示例
interface TaskContextCapsule {
  taskId: string;              // 任务ID
  taskType: TaskType;          // 任务类型
  createdAt: string;           // 创建时间
  isActive: boolean;           // 是否活跃
  relatedConstraints: Constraint[]; // 相关约束
}

// ❌ 错误示例
interface TaskContextCapsule {
  id: string;                  // 不明确的ID
  type: any;                  // 过于通用
  date: string;                // 不明确的日期
  flag: boolean;               // 不明确的标志
  constraints: any[];          // 缺少描述性前缀
}
```

### 4. 常量和枚举命名

#### 常量命名
```typescript
// ✅ 正确示例
const MAX_RETRY_COUNT = 3;
const DEFAULT_TIMEOUT = 5000;
const API_VERSION = '2.0.0';
const HEALTH_CHECK_INTERVAL = 30000;

// ❌ 错误示例
const maxRetryCount = 3;           // 首字母小写
const Max_Retry_Count = 3;          // 混合风格
const maxretrycount = 3;           // 全部小写
```

#### 枚举命名
```typescript
// ✅ 正确示例
enum TaskType {
  SECURITY_AUDIT = 'security_audit',
  PERFORMANCE_OPTIMIZATION = 'performance_optimization',
  CODE_REVIEW = 'code_review',
  TESTING = 'testing',
  DEPLOYMENT = 'deployment'
}

enum Severity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

// ❌ 错误示例
enum taskType {                    // 首字母小写
  SecurityAudit = 'security_audit', // 驼峰命名
  performance_optimization = 'performance_optimization' // 下划线命名
}
```

### 5. 文件和目录命名

#### 文件命名
```typescript
// ✅ 正确示例
// 类文件
task-context-capsule.ts
constraint-generator.ts
health-check-service.ts

// 接口文件
api-response.interface.ts
health-status.interface.ts

// 工具文件
validation-utils.ts
date-utils.ts
logger-utils.ts

// 配置文件
database.config.ts
api.config.ts
monitoring.config.ts

// ❌ 错误示例
TaskContextCapsule.ts              // 首字母大写
taskContextCapsule.ts              // 驼峰命名
task_context_capsule.ts            // 下划线命名
taskcontextcapsule.ts              // 无分隔符
```

#### 目录命名
```typescript
// ✅ 正确示例
src/
├── core/
│   ├── constraint/
│   ├── monitoring/
│   └── contract/
├── api/
│   ├── routes/
│   ├── middleware/
│   └── controllers/
├── utils/
├── config/
└── types/

// ❌ 错误示例
src/
├── Core/                          // 首字母大写
├── constraintGenerator/           // 驼峰命名
├── api_routes/                    // 下划线命名
└── Utils/                         // 首字母大写
```

### 6. API路径命名

#### RESTful API路径
```typescript
// ✅ 正确示例
// 资源路径
GET /api/constraints
GET /api/constraints/{id}
POST /api/constraints
PUT /api/constraints/{id}
DELETE /api/constraints/{id}

// 嵌套资源
GET /api/tasks/{taskId}/constraints
POST /api/tasks/{taskId}/constraints

// 动作路径
POST /api/constraints/{id}/validate
POST /api/constraints/{id}/activate
POST /api/health/check

// ❌ 错误示例
GET /api/getConstraints                    // 使用动词
GET /api/constraints/getAll                // 不必要的路径
POST /api/createConstraint                 // 使用动词
GET /api/constraintsById/{id}             // 混合风格
```

#### 查询参数命名
```typescript
// ✅ 正确示例
GET /api/constraints?page=1&limit=10&sort=createdAt&order=desc
GET /api/constraints?category=security&severity=high
GET /api/constraints?search=authentication&status=active

// ❌ 错误示例
GET /api/constraints?p=1&l=10              // 过度缩写
GET /api/constraints?category=Security    // 首字母大写
GET /api/constraints?filter=active        // 过于通用
```

### 7. 数据库命名

#### 表名命名
```sql
-- ✅ 正确示例
CREATE TABLE task_context_capsules (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(255) NOT NULL,
    task_type VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE constraints (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL
);

-- ❌ 错误示例
CREATE TABLE TaskContextCapsules (        -- 驼峰命名
CREATE TABLE task_context_capsule (        -- 单数形式
CREATE TABLE taskContextCapsules (        -- 混合风格
CREATE TABLE tcc (                         // 过度缩写
```

#### 字段命名
```sql
-- ✅ 正确示例
CREATE TABLE constraints (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ❌ 错误示例
CREATE TABLE constraints (
    ID SERIAL PRIMARY KEY,                -- 大写字母
    Name VARCHAR(255) NOT NULL,           -- 首字母大写
    categoryName VARCHAR(100),           -- 驼峰命名
    isActive BOOLEAN DEFAULT true,        -- 驼峰命名
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 驼峰命名
);
```

## 🔧 特殊命名约定

### 1. 事件和消息命名
```typescript
// ✅ 正确示例
// 事件命名
interface ConstraintGeneratedEvent {
  eventType: 'constraint.generated';
  constraintId: string;
  taskId: string;
  timestamp: string;
}

interface HealthCheckFailedEvent {
  eventType: 'health.check.failed';
  componentName: string;
  error: string;
  timestamp: string;
}

// 消息队列命名
const QUEUES = {
  CONSTRAINT_GENERATION: 'constraint.generation',
  HEALTH_CHECK: 'health.check',
  NOTIFICATION: 'notification'
} as const;
```

### 2. 配置项命名
```typescript
// ✅ 正确示例
interface DatabaseConfig {
  host: string;
  port: number;
  database: string;
  username: string;
  password: string;
  ssl: boolean;
  connectionPool: {
    min: number;
    max: number;
    idleTimeoutMillis: number;
  };
}

interface MonitoringConfig {
  enabled: boolean;
  healthCheckInterval: number;
  metricsCollectionInterval: number;
  alerting: {
    enabled: boolean;
    channels: ('email' | 'slack')[];
  };
}
```

### 3. 错误码命名
```typescript
// ✅ 正确示例
enum ErrorCode {
  // 认证错误 (1000-1999)
  UNAUTHORIZED = '1001',
  FORBIDDEN = '1003',
  TOKEN_EXPIRED = '1004',
  
  // 参数错误 (2000-2999)
  INVALID_PARAMETER = '2001',
  MISSING_PARAMETER = '2002',
  VALIDATION_ERROR = '2003',
  
  // 业务错误 (3000-3999)
  CONSTRAINT_GENERATION_FAILED = '3001',
  CONTRACT_VALIDATION_FAILED = '3002',
  CONFLICT_DETECTION_FAILED = '3003'
}
```

### 4. 测试文件命名
```typescript
// ✅ 正确示例
// 单元测试
constraint-generator.spec.ts
health-check-service.spec.ts
api-routes.spec.ts

// 集成测试
constraint-generator.integration.spec.ts
api-endpoints.integration.spec.ts

// 端到端测试
constraint-generation.e2e.spec.ts
health-monitoring.e2e.spec.ts

// 测试工具
test-utils.ts
mock-data.ts
test-fixtures.ts

// ❌ 错误示例
ConstraintGeneratorTest.ts           // 首字母大写
constraint_generator_test.ts        // 下划线命名
constraintGenerator.test.ts         // 使用.test扩展名
```

## 🔍 命名检查清单

### 类和接口检查
- [ ] 使用PascalCase
- [ ] 名称清晰表达用途
- [ ] 避免缩写（除非广泛认可）
- [ ] 接口名称以I开头（根据语言习惯）

### 方法检查
- [ ] 使用camelCase
- [ ] 以动词开头
- [ ] 布尔值方法以is/has/can/should开头
- [ ] 避免歧义词汇

### 变量检查
- [ ] 使用camelCase
- [ ] 名称具有描述性
- [ ] 避免单字母变量（除循环计数器外）
- [ ] 布尔值变量使用is/has/can前缀

### 常量检查
- [ ] 使用SCREAMING_SNAKE_CASE
- [ ] 名称具有描述性
- [ ] 避免魔法数字，使用命名常量

### 文件检查
- [ ] 使用kebab-case
- [ ] 名称与内容一致
- [ ] 目录结构清晰

## 🔗 相关文档

### 核心文档
- [系统架构总览](../architecture/overview.md) - 系统整体架构
- [API契约总览](../api/contract-overview.md) - API接口契约
- [数据模型字典](../data-models/dictionary.md) - 数据结构定义

### 规范文档
- [接口规范](../api/specifications.md) - 详细接口定义
- [错误处理](../standards/error-handling.md) - 错误处理机制
- [版本管理](../standards/versioning.md) - 版本兼容性管理

### 工具文档
- [ESLint配置](../tools/eslint-config.md) - 代码检查配置
- [Prettier配置](../tools/prettier-config.md) - 代码格式化配置
- [TypeScript配置](../tools/typescript-config.md) - TypeScript配置

---

**文档维护**：DSGS架构团队  
**最后更新**：2025-08-06  
**版本**：2.0