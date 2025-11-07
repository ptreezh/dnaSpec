# Dynamic Specification Growth System (DSGS) - iFlow 上下文

## 项目概述

Dynamic Specification Growth System (DSGS) 是一个下一代规范管理系统，能够为软件开发任务动态生成上下文感知的约束。DSGS 通过提供最小化、任务特定的约束来帮助团队维护代码质量和一致性，这些约束会随着项目的发展而演进。

### 核心特性

- **动态约束生成**: 根据任务类型和上下文自动生成适当的约束
- **分层规范管理**: 从全局规则到任务特定约束的管理
- **实时IDE集成**: 与Cline、VS Studio和其他MCP兼容IDE的无缝集成
- **分阶段演进**: 支持从MVP到高级功能的增量采用
- **契约管理**: 完整的API契约生成、验证和版本管理功能
- **健康监控**: 系统组件健康检查和性能监控

### 关键组件

- **基本生存法则 (BSL)**: 定义系统范围约束的基础规则
- **任务上下文胶囊 (TCC)**: 提供任务特定约束的上下文感知容器
- **约束模板库**: 可扩展的安全性、性能和架构约束模板库
- **MCP集成**: 用于IDE和工具集成的标准化通信协议
- **契约管理模块**: API契约的生成、验证、版本管理和实现一致性检查
- **神经场系统**: 基于约束吸引子的动态约束演化系统
- **认知工具**: 问题理解、相关回忆、解决方案检查和错误回溯工具

## 项目类型

这是一个基于TypeScript的代码项目，使用Node.js运行环境。

## 构建和运行

### 前提条件
- Node.js v18.0.0 或更高版本
- npm v8.0.0 或更高版本

### 安装依赖
```bash
npm install
```

### 构建项目
```bash
npm run build
```

### 开发模式运行
```bash
npm run dev
```

### 生产模式运行
```bash
npm start
```

## 测试命令

```bash
# 运行所有测试
npm run test

# 运行单元测试
npm run test:unit

# 运行集成测试
npm run test:integration

# 运行端到端测试
npm run test:e2e

# 运行性能测试
npm run test:performance

# 运行属性测试
npm run test:property

# 运行契约高级测试
npm run test:contract:advanced

# 运行混沌测试
npm run test:chaos

# 生成测试覆盖率报告
npm run test:coverage
```

## 契约管理命令

```bash
# 生成契约
npm run contract:generate

# 验证契约
npm run contract:validate

# 发布契约
npm run contract:publish

# 生成契约文档
npm run contract:docs

# 初始化契约配置
npm run contract:init
```

## 监控和健康检查命令

```bash
# 系统健康检查
npm run health:check

# 收集系统指标
npm run metrics:collect

# 查看告警状态
npm run alerts:status
```

## 文档管理命令

```bash
# 检查文档完整性
npm run docs:check

# 文档合规性检查
npm run docs:compliance

# 设计文档检查
npm run docs:design

# 文档同步检查
npm run docs:sync-check

# 生成文档报告
npm run docs:report
```

## 核心架构

```
dsgs/
├── src/
│   ├── core/               # 核心业务逻辑
│   │   ├── cognitive-tools/    # 认知工具
│   │   ├── constraint/         # 约束生成
│   │   ├── evolution/          # 演化管理
│   │   ├── neural-field/       # 神经场系统
│   │   ├── protocol-engine/    # 协议引擎
│   │   ├── specification/      # 规范管理
│   │   ├── state/              # 状态管理
│   │   └── types/              # 类型定义
│   ├── integration/        # 外部集成
│   │   ├── cli/            # 命令行接口
│   │   └── mcp/            # MCP协议实现
│   ├── modules/            # 功能模块
│   │   ├── contract/       # 契约管理
│   │   └── monitoring/     # 监控系统
│   └── utils/              # 工具函数
├── docs/                   # 文档
├── config/                 # 配置文件
└── tools/                  # 开发工具
```

## IDE集成

DSGS与MCP兼容的IDE无缝集成：

1. 安装DSGS MCP服务器:
```bash
npm install -g dynamic-specs-growth
```

2. 在IDE的MCP设置中配置DSGS:
```json
{
  "mcpServers": {
    "dynamic-specs-growth-stdio": {
      "type": "stdio",
      "command": "node",
      "args": [
        "node_modules/dynamic-specs-growth/dist/integration/mcp/McpStdioServer.js"
      ]
    }
  }
}
```

## CLI使用

```bash
# 生成API契约
dsgs-contract-simple generate

# 验证API契约
dsgs-contract-simple validate

# 检查任务约束
dsgs check-constraints --tcc-path ./task.tcc --spec-path ./spec.json

# 获取系统状态
dsgs status

# 生成任务类型约束
dsgs generate-constraints --task-type SECURITY
```

## 开发约定

- 使用TypeScript进行开发，遵循严格类型检查
- 使用Jest进行测试，确保测试覆盖率
- 遵循模块化设计原则，保持文件简洁
- 采用TDD驱动开发，每个组件文件不超过300行
- 遵循单一职责原则和命名规范
- 保持代码可维护性和可扩展性