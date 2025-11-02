# Contract模块 - 工具函数

## 📋 工具模块概述

工具模块提供各种辅助函数，支持契约生成、验证和管理。每个工具函数文件不超过300行，职责单一，便于测试和维护。

## 🎯 模块结构

```
utils/
├── README.md                      # 工具模块说明
├── index.ts                       # 工具函数统一导出
├── CommonUtils.ts                 # 通用工具函数
├── TypeHelpers.ts                 # 类型相关工具
├── ValidationHelpers.ts           # 验证相关工具
├── FileHelpers.ts                 # 文件操作工具
├── StringUtils.ts                 # 字符串处理工具
├── ArrayUtils.ts                  # 数组处理工具
├── ObjectUtils.ts                 # 对象处理工具
├── AsyncUtils.ts                  # 异步处理工具
├── Logger.ts                      # 日志工具
├── PerformanceMonitor.ts          # 性能监控工具
└── CacheManager.ts                # 缓存管理工具
```

## 🚀 主要工具类别

### 🔧 通用工具 (CommonUtils)
- 日期时间处理
- 字符串格式化
- 数组操作
- 对象操作
- 路径处理
- 验证函数

### 🎯 类型工具 (TypeHelpers)
- 类型检查函数
- 类型转换函数
- 类型保护函数
- 类型推断函数

### ✅ 验证工具 (ValidationHelpers)
- 契约验证工具
- 数据验证工具
- 格式验证工具
- 规则验证工具

### 📁 文件工具 (FileHelpers)
- 文件读取工具
- 文件写入工具
- 文件搜索工具
- 文件监控工具

### 📝 字符串工具 (StringUtils)
- 字符串格式化
- 字符串转换
- 字符串验证
- 字符串操作

### 📊 数组工具 (ArrayUtils)
- 数组操作
- 数组转换
- 数组过滤
- 数组排序

### 🗂️ 对象工具 (ObjectUtils)
- 对象操作
- 对象转换
- 对象合并
- 对象验证

### ⚡ 异步工具 (AsyncUtils)
- 异步控制
- 并发处理
- 重试机制
- 延迟执行

### 📊 日志工具 (Logger)
- 结构化日志
- 日志级别
- 日志格式化
- 日志轮转

### 📈 性能监控 (PerformanceMonitor)
- 性能指标收集
- 操作计时
- 统计信息
- 性能报告

### 💾 缓存管理 (CacheManager)
- 内存缓存
- 缓存策略
- 缓存清理
- 缓存统计

## 🔧 使用示例

### 通用工具

```typescript
import { StringUtils, ArrayUtils, ObjectUtils } from '../utils';

// 字符串处理
const camelCase = StringUtils.toCamelCase('hello_world'); // 'helloWorld'
const pascalCase = StringUtils.toPascalCase('hello_world'); // 'HelloWorld'

// 数组操作
const unique = ArrayUtils.unique([1, 2, 2, 3, 3, 4]); // [1, 2, 3, 4]
const grouped = ArrayUtils.groupBy(users, 'department');

// 对象操作
const merged = ObjectUtils.deepMerge(obj1, obj2);
const cloned = ObjectUtils.deepClone(original);
```

### 验证工具

```typescript
import { ValidationUtils } from '../utils';

// 验证格式
const isValid = ValidationUtils.isValidEmail('test@example.com');
const isValidVersion = ValidationUtils.isValidVersion('1.0.0');
const isValidPath = ValidationUtils.isValidPath('/api/users');
```

### 异步工具

```typescript
import { AsyncUtils } from '../utils';

// 延迟执行
await AsyncUtils.delay(1000);

// 重试机制
const result = await AsyncUtils.retry(() => fetchData(), 3, 1000);

// 并发控制
const results = await AsyncUtils.concurrent(items, processItem, 5);
```

### 性能监控

```typescript
import { PerformanceMonitor } from '../utils';

const monitor = new PerformanceMonitor();

// 开始监控
const operationId = monitor.startOperation('generate-contract');

// 执行操作
const result = await generateContract();

// 结束监控
monitor.endOperation(operationId);

// 获取统计信息
const stats = monitor.getStatistics();
```

### 缓存管理

```typescript
import { CacheManager } from '../utils';

const cache = new CacheManager({
  enabled: true,
  ttl: 3600 // 1小时
});

// 设置缓存
await cache.set('key', value);

// 获取缓存
const cached = await cache.get('key');

// 删除缓存
await cache.delete('key');

// 清理缓存
await cache.clear();
```

## 📊 工具函数列表

### 日期时间工具
- `formatDate(date: Date): string` - 格式化日期
- `parseDate(dateString: string): Date` - 解析日期字符串
- `getCurrentTimestamp(): number` - 获取当前时间戳
- `getTimeDiff(start: number, end: number): number` - 计算时间差

### 字符串工具
- `toCamelCase(str: string): string` - 转换为驼峰命名
- `toPascalCase(str: string): string` - 转换为帕斯卡命名
- `toKebabCase(str: string): string` - 转换为短横线命名
- `toSnakeCase(str: string): string` - 转换为下划线命名
- `capitalize(str: string): string` - 首字母大写
- `isEmpty(str: string): boolean` - 检查字符串是否为空
- `truncate(str: string, maxLength: number): string` - 截断字符串

### 数组工具
- `unique<T>(array: T[]): T[]` - 数组去重
- `groupBy<T>(array: T[], key: keyof T): Record<string, T[]>` - 数组分组
- `sortBy<T>(array: T[], key: keyof T, order: 'asc' | 'desc'): T[]` - 数组排序
- `paginate<T>(array: T[], page: number, pageSize: number)` - 数组分页
- `flatten<T>(array: (T | T[])[]): T[]` - 数组扁平化
- `intersection<T>(array1: T[], array2: T[]): T[]` - 数组交集
- `difference<T>(array1: T[], array2: T[]): T[]` - 数组差集

### 对象工具
- `deepMerge<T>(target: T, source: Partial<T>): T` - 深度合并对象
- `deepClone<T>(obj: T): T` - 深度克隆对象
- `getNestedValue(obj: any, path: string): any` - 获取嵌套属性值
- `setNestedValue(obj: any, path: string, value: any): void` - 设置嵌套属性值
- `mapKeys<T>(obj: T, mapper: (key: string) => K): Record<K, T[keyof T]>` - 键转换
- `mapValues<T, V>(obj: T, mapper: (value: T[keyof T]) => V): Record<keyof T, V>` - 值转换

### 路径工具
- `joinPath(...paths: string[]): string` - 连接路径
- `normalizePath(path: string): string` - 规范化路径
- `getParentPath(path: string): string` - 获取父路径
- `getBaseName(path: string): string` - 获取基础名称
- `getExtension(path: string): string` - 获取扩展名

### 验证工具
- `isValidEmail(email: string): boolean` - 验证邮箱格式
- `isValidUrl(url: string): boolean` - 验证URL格式
- `isValidVersion(version: string): boolean` - 验证版本格式
- `isValidPath(path: string): boolean` - 验证路径格式
- `isValidHttpMethod(method: string): boolean` - 验证HTTP方法

### 文件工具
- `getFileExtension(filename: string): string` - 获取文件扩展名
- `isTypeScriptFile(filename: string): boolean` - 检查是否为TypeScript文件
- `isTestFile(filename: string): boolean` - 检查是否为测试文件
- `isDefinitionFile(filename: string): boolean` - 检查是否为定义文件

### 性能工具
- `throttle<T>(func: T, delay: number): T` - 节流函数
- `debounce<T>(func: T, delay: number): T` - 防抖函数
- `memoize<T>(func: T, keyGenerator?: (...args: any[]) => string): T` - 记忆函数

### 异步工具
- `delay(ms: number): Promise<void>` - 延迟执行
- `retry<T>(func: () => Promise<T>, maxRetries: number, delayMs: number): Promise<T>` - 重试函数
- `concurrent<T, R>(items: T[], processor: (item: T) => Promise<R>, concurrency: number): Promise<R[]>` - 并发控制

## 🎯 设计原则

### 📏 文件大小控制
- 每个工具函数文件不超过300行
- 相关功能组织在同一文件中
- 便于测试和维护

### 🔧 职责单一
- 每个函数只做一件事
- 函数名称清晰表达功能
- 避免副作用

### 🧪 测试友好
- 纯函数设计
- 可预测的输出
- 易于单元测试

### 📚 文档完整
- JSDoc注释完整
- 使用示例清晰
- 参数和返回值说明

## 🚀 性能特性

### ⚡ 高性能
- 使用原生方法
- 避免不必要的计算
- 优化算法复杂度

### 💾 内存优化
- 避免内存泄漏
- 合理使用缓存
- 及时清理资源

### 🔧 可扩展
- 插件化设计
- 易于添加新功能
- 支持自定义配置

## 📋 使用建议

### 🎯 选择合适的工具
- 根据具体需求选择合适的工具函数
- 避免重复造轮子
- 优先使用经过测试的工具

### 📊 性能考虑
- 在性能敏感的场景使用缓存
- 合理使用并发控制
- 避免过度优化

### 🧪 测试覆盖
- 为新工具函数编写测试
- 确保边界条件覆盖
- 性能测试验证

## 📚 相关文档

- [通用工具](./CommonUtils.ts) - 通用工具函数
- [类型工具](./TypeHelpers.ts) - 类型相关工具
- [验证工具](./ValidationHelpers.ts) - 验证相关工具
- [文件工具](./FileHelpers.ts) - 文件操作工具
- [日志工具](./Logger.ts) - 日志处理工具
- [性能监控](./PerformanceMonitor.ts) - 性能监控工具
- [缓存管理](./CacheManager.ts) - 缓存管理工具

## 🤝 贡献指南

### 添加新工具
1. 在合适的分类中添加新函数
2. 编写完整的JSDoc注释
3. 添加相应的单元测试
4. 更新相关文档

### 性能优化
1. 使用性能分析工具
2. 优化算法和数据结构
3. 添加性能测试
4. 更新性能文档

### 代码规范
1. 遵循TypeScript规范
2. 保持函数简洁
3. 添加错误处理
4. 确保类型安全

---

**工具模块维护**: DSGS架构团队  
**最后更新**: 2025-08-11  
**版本**: 2.0