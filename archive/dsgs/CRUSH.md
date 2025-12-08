# CRUSH.md - Dynamic Specification Growth System (DNASPEC)

## Build & Test Commands
- `npm test` - Run all tests
- `npm run test:watch` - Run tests in watch mode  
- `npm run test:coverage` - Run tests with coverage
- `npm run test:integration` - Run integration tests only
- `npm run test:unit` - Run unit tests only
- `npm run test:spec` - Run specific specification tests
- `npm run test:property` - Run property-based tests with full reports
- `npm run test:property:quick` - Quick property-based test run
- `npm run test:property:performance` - Performance benchmarks only
- `npm run test:baseline` - Manage test baselines and smart execution
- `npm run test:analysis` - Analyze test coverage and gaps
- `npm test -- <test-file-pattern>` - Run specific test file
- `npm test -- --testNamePattern="<test-name>"` - Run specific test
- `npm run build` - Build TypeScript to dist/
- `npm start` - Start the application
- `npm run dev` - Start development server

## Project Memory
- **持久记忆系统**: `PROJECT_MEMORY.md` - 项目完整状态和架构记忆
- **TDD专门角色**: `docs/tdd-role-plan.md` - TestCraft AI测试驱动设计计划
- **契约管理**: `CONTRACT_INTEGRATION_REPORT.md` - 契约集成状态
- **项目状态**: 57%完成，Phase 5测试优化进行中

## Service Monitoring Commands
- `npm run health:check` - Check system health status
- `npm run metrics:collect` - Collect system metrics
- `npm run alerts:status` - Check active alerts
- `npm run monitoring:dashboard` - Open Grafana dashboard

## Contract Management Commands
- `npm run contract:generate` - Generate API contract from source
- `npm run contract:validate` - Validate contract against implementation
- `npm run contract:publish` - Publish contract version
- `npm run contract:docs` - Generate contract documentation

## Code Style Guidelines

### TypeScript Configuration
- Target: ES2022, Module: CommonJS
- Strict mode enabled with all strict checks
- Path aliases: @core/*, @integration/*, @utils/*, @modules/*

### Naming Conventions (遵循统一契约文档规范)
- Classes: PascalCase (TaskContextCapsule, ConstraintGenerator)
- Interfaces: PascalCase (ApiResponse, HealthStatus)
- Methods: camelCase (generateConstraints, validateContract)
- Variables: camelCase (taskContext, validationResult)
- Constants: UPPER_SNAKE_CASE (MAX_RETRY_COUNT, API_VERSION)
- Files: kebab-case (task-context-capsule.ts, health-check-service.ts)
- API Paths: kebab-case (/api/health-check, /api/contract/generate)
- Database Tables: snake_case (task_context_capsules, constraints)

### API Design Standards
- 统一响应格式：所有API返回 ApiResponse<T> 结构
- 错误处理标准化：使用统一的错误码和错误信息格式
- 版本管理：API版本管理，确保向后兼容
- 认证授权：JWT Token认证，基于角色的访问控制

### Import Organization
- Use type imports for types: `import type { ConstraintTemplate } from './types'`
- Group imports: third-party, internal types, internal values
- Use path aliases for internal imports: @core/*, @modules/*, @utils/*
- Import ordering: external libs, internal types, internal values

### Error Handling
- Always type error parameters: `catch (error: unknown)`
- Check error type before accessing properties: `if (error instanceof Error)`
- Use console.warn for non-critical errors
- No linting setup - focus on TypeScript strict mode errors

### Documentation
- JSDoc comments for all public methods and interfaces
- Include @param and @returns tags
- Module-level JSDoc comments for files
- 遵循统一契约文档体系的文档规范
- 使用金字塔原则组织文档内容

### Testing
- Test files in test/ directory with .test.ts suffix
- Use Jest with ts-jest preset
- Run single test: `npm test -- <file-path>`
- Run test by name: `npm test -- --testNamePattern="<name>"`
- Describe blocks for class/method grouping
- beforeEach/afterEach for test setup/teardown
- Async/await for async operations
- Test timeout: 30 seconds

### Project Structure
- src/core/ - Core business logic
- src/integration/ - External integrations (MCP, CLI)
- src/utils/ - Utility functions and types
- src/modules/ - Module implementations (monitoring, contract, constraint)
- docs/unified-contract/ - Unified contract documentation
- test/unit/ - Unit tests
- test/integration/ - Integration tests
- test/e2e/ - End-to-end tests

### Monitoring & Health Checks
- 所有核心组件必须实现健康检查接口
- 关键指标必须通过 Prometheus 导出
- 告警规则必须配置阈值和通知机制
- 自动恢复机制必须处理常见故障场景

### Contract Management
- API契约必须从 TypeScript 类型定义自动生成
- 契约验证必须集成到 CI/CD 流程
- 版本变更必须经过兼容性检查
- 破坏性变更必须提供迁移指南

### Quick Reference
- Single test: `npm test -- test/unit/SpecificationManager.test.ts`
- Build + validate: `npm run build`
- Dev server: `npm run dev`
- Contract generation: `npm run contract:generate`