---
name: dnaspec-system-architect
description: Design system architecture, select technology stacks, define module boundaries, and specify interfaces. Focus on technical architecture decisions. When you need system architecture design, technology selection, module partitioning, or interface definition, use this skill. This is a technical architecture skill, not a coordination skill. Use dnaspec-architect for multi-layer alignment and coordination.
---

# DNASPEC System Architect

## 使用时机

当用户提到以下需求时，使用此技能：
- "系统架构设计" 或 "system architecture design"
- "技术栈选择" 或 "technology stack selection"
- "模块划分" 或 "module partitioning"
- "接口定义" 或 "interface definition"
- "架构决策" 或 "architecture decision"
- 需要选择技术栈
- 需要定义模块边界
- 需要设计API接口

**不要在以下情况使用**：
- ❌ 多层级调用对齐（使用architect技能）
- ❌ 协调多个子技能（使用architect技能）
- ❌ 讨论具体编码实现

## 核心理念

### 🎯 与architect的职责区分

**dnaspec-system-architect（系统架构师）**：
- 专注于**技术架构设计**
- 负责**技术栈选择**
- 负责**模块划分**
- 负责**接口定义**
- 输出：技术架构文档

**dnaspec-architect（架构协调器）**：
- 专注于**架构协调和对齐**
- 负责**多层级调用对齐**
- 负责**防止架构失控**
- 负责**智能体集成协调**
- 协调：协调多个子技能完成复杂任务

```
dnaspec-architect (主协调器)
    ↓ 需要系统架构设计时
dnaspec-system-architect (系统架构师)
    ↓ 输出技术架构
dnaspec-architect (继续协调)
    ↓ 需要验证多层级对齐
dnaspec-dapi-checker (API检查)
```

### 🎯 技术架构设计的核心原则

**1. 从简单到复杂演化**

```
阶段1：最简架构（MVP）
├─ 单体应用
├─ 单数据库
└─ 少量用户

→ 遵循格式塔原则：简单但完整的整体

↓ 逐步演化

阶段2：分层架构
├─ 前后端分离
├─ 引入缓存
└─ 更多用户

→ 复杂度增加，但架构清晰

↓ 继续演化

阶段3：微服务架构
├─ 服务拆分
├─ 消息队列
└─ 大量用户

→ 高度复杂，但架构可控
```

**2. 技术选型的关键因素**

```yaml
selection_criteria:
  team_fit:
    - 团队技能匹配度
    - 学习曲线可接受
    - 文档和支持完善

  project_fit:
    - 满足性能要求
    - 满足扩展性要求
    - 满足安全性要求

  ecosystem:
    - 社区活跃度
    - 第三方库丰富度
    - 长期维护性

  operational:
    - 部署复杂度
    - 监控工具支持
    - 故障排查能力
```

**3. 模块划分原则**

```yaml
modularity_principles:
  high_cohesion:
    - 模块内功能相关
    - 单一职责
    - 业务领域驱动

  low_coupling:
    - 模块间依赖少
    - 接口清晰
    - 可独立部署

  boundaries:
    - 业务边界清晰
    - 数据访问隔离
    - 接口版本管理
```

---

## 全生命周期应用

### 📋 Idea阶段：为概念选择技术栈

**场景**：用户有一个想法，需要选择初始技术

**示例**：
```
用户想法："我想做一个AI代码助手"

技术选型：
📋 需求分析
- 核心功能：AI代码分析和建议
- 用户群体：开发者
- 规模：从小规模开始
- 约束：需要集成AI API

🎯 技术栈选择（最简架构）
前端：
  ├─ 框架：React（生态丰富）
  ├─ UI：Material-UI（组件完善）
  └─ 状态：React Query（简单高效）

后端：
  ├─ 语言：Node.js（前后端统一语言）
  ├─ 框架：Express（简单轻量）
  ├─ AI集成：OpenAI API
  └─ 数据库：PostgreSQL（关系型数据）

✅ 格式塔原则：简单但完整
- 技术栈成熟
- 团队易于学习
- 可独立部署
- 可逐步扩展
```

### 📋 需求阶段：设计模块架构

**场景**：有完整需求，需要设计模块划分

**示例**：
```
需求：电商平台

模块划分：
📋 领域驱动设计

用户领域（User Domain）
├─ 用户模块（UserModule）
│   ├─ 用户管理
│   ├─ 认证授权
│   └─ 个人资料
└─ 边界：清晰的接口定义

商品领域（Product Domain）
├─ 商品模块（ProductModule）
│   ├─ 商品管理
│   ├─ 库存管理
│   └─ 价格管理
└─ 边界：独立的领域逻辑

订单领域（Order Domain）
├─ 订单模块（OrderModule）
│   ├─ 订单创建
│   ├─ 订单支付
│   └─ 订单查询
└─ 边界：独立的状态管理

✅ 模块化原则：
- 高内聚：每个模块职责单一
- 低耦合：模块间接口清晰
- 可独立测试
- 可独立部署
```

### 📋 细化阶段：定义接口规范

**场景**：模块间需要清晰的接口定义

**示例**：
```
细化需求：用户模块和订单模块的接口

接口定义：
📋 REST API规范

用户模块提供的接口：
├─ POST /api/users/register
│   ├─ 请求：{ username, password, email }
│   ├─ 响应：{ userId, token }
│   └─ 错误：{ error: "USER_EXISTS", message: "..." }
├─ GET /api/users/{id}
│   ├─ 响应：{ userId, username, email }
│   └─ 错误：{ error: "USER_NOT_FOUND" }
└─ PUT /api/users/{id}
    ├─ 请求：{ email, profile }
    ├─ 响应：{ success: true }
    └─ 错误：{ error: "VALIDATION_ERROR" }

订单模块调用的接口：
├─ GET /api/users/{id}/orders
│   └─ 响应：{ orders: [...] }
└─ POST /api/users/{id}/orders
    ├─ 请求：{ items: [...] }
    └─ 响应：{ orderId, status }

✅ 接口设计原则：
- RESTful风格
- 统一的错误格式
- 清晰的HTTP状态码
- 完整的请求/响应示例
```

### 📋 智能阶段：智能体系统架构

**场景**：设计支持智能体的系统架构

**示例**：
```
智能体系统架构：

🏗️ 系统架构设计

架构模式：主协调器 + 局部智能体

┌─────────────────────────────────┐
│   主协调器层                       │
│   ProjectHealthCoordinator       │
│   ├─ 任务分发                     │
│   ├─ 结果聚合                     │
│   └─ 错误处理                     │
├─────────────────────────────────┤
│   智能体通信层                     │
│   ├─ REST API                     │
│   ├─ 消息队列（可选）              │
│   └─ 服务发现                     │
├─────────────────────────────────┤
│   局部智能体层                     │
│   ├─ CodeReviewAgent             │
│   ├─ TestCoverageAgent           │
│   └─ DependencyHealthAgent       │
└─────────────────────────────────┘

🎯 技术栈选择：
通信协议：REST/JSON（统一）
消息格式：{ "task": "...", "params": {...} }
错误处理：{ "error": "...", "message": "..." }
超时设置：30秒（协调器）→ 10秒（智能体）

✅ 架构特点：
- 轻量级主协调器
- 局部智能体独立上下文
- 统一的通信协议
- 失败隔离
```

---

## 核心功能

### 1. 需求分析

**功能需求**
- 业务功能清单
- 用户角色定义
- 用例场景分析

**非功能需求**
- 性能要求
- 可扩展性
- 可用性
- 安全性

### 2. 架构模式选择

**分层架构**
```
┌─────────────────────┐
│   Presentation     │  UI层
├─────────────────────┤
│   Application      │  应用层
├─────────────────────┤
│   Business         │  业务层
├─────────────────────┤
│   Data             │  数据层
└─────────────────────┘
```

**微服务架构**
```
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Service │  │ Service │  │ Service │
│   A     │  │   B     │  │   C     │
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
┌─────────────────────────────────┐
│   API Gateway / Service Mesh    │
└─────────────────────────────────┘
```

**事件驱动架构**
```
Producer          Event Bus          Consumer
   │                │                 │
   ├──Event──────→  │                 ├──Event──────→
   │                │                 │
   └──Event──────→  │                 └──Event──────→
                    │
                 ┌──┴──┐
                 │Queue│
                 └─────┘
```

### 3. 技术栈选择

**后端技术栈**
```yaml
language_options:
  - Node.js: 事件驱动，生态丰富
  - Python: AI友好，库丰富
  - Java: 企业级，稳定成熟
  - Go: 高性能，并发优秀

framework_options:
  - Node.js: Express, NestJS, Fastify
  - Python: Django, FastAPI, Flask
  - Java: Spring Boot, Micronaut
  - Go: Gin, Echo, Fiber
```

**数据库选择**
```yaml
relational:
  - PostgreSQL: 功能强大，扩展性好
  - MySQL: 成熟稳定，云支持好
  - SQL Server: 企业级，Windows生态

nosql:
  - MongoDB: 文档型，灵活
  - Redis: 缓存，会话存储
  - Cassandra: 分布式，高可用
```

**前端技术栈**
```yaml
frameworks:
  - React: 生态最丰富
  - Vue: 学习曲线平缓
  - Angular: 企业级框架

state_management:
  - Redux: 可预测，生态成熟
  - Zustand: 简单轻量
  - MobX: 响应式，易用
```

### 4. 模块划分

**划分原则**
- 高内聚低耦合
- 单一职责
- 业务领域驱动

**模块边界**
```
用户模块（User Module）
├─ 职责：用户管理、认证授权
├─ 接口：REST API
└─ 依赖：数据库、缓存

商品模块（Product Module）
├─ 职责：商品管理、库存管理
├─ 接口：REST API
└─ 依赖：数据库、搜索引擎

订单模块（Order Module）
├─ 职责：订单处理、支付流程
├─ 接口：REST API
└─ 依赖：数据库、消息队列
```

### 5. 接口定义

**RESTful API**
```yaml
GET /api/resources
  响应：200 [{ resource1 }, { resource2 }]

GET /api/resources/{id}
  响应：200 { resource }
  错误：404 { "error": "NOT_FOUND" }

POST /api/resources
  请求：{ name, value }
  响应：201 { id, name, value }
  错误：400 { "error": "VALIDATION_ERROR" }

PUT /api/resources/{id}
  请求：{ name, value }
  响应：200 { id, name, value }
  错误：404 { "error": "NOT_FOUND" }

DELETE /api/resources/{id}
  响应：204
  错误：404 { "error": "NOT_FOUND" }
```

**数据契约**
- JSON Schema
- Protobuf定义
- OpenAPI规范

---

## 输出格式

```markdown
# 系统架构设计文档

## 1. 架构概览
- 架构模式
- 架构图
- 设计原则

## 2. 技术栈
### 2.1 后端技术栈
- 语言
- 框架
- 数据库
- 中间件

### 2.2 前端技术栈
- 框架
- 状态管理
- UI库

### 2.3 技术选型理由
- 团队匹配度
- 性能考虑
- 生态系统
- 运维要求

## 3. 模块划分
### 3.1 模块列表
- 模块名称
- 职责描述
- 接口定义

### 3.2 模块依赖
- 依赖关系图
- 接口调用关系

## 4. 接口规范
### 4.1 REST API
- 端点定义
- 请求/响应格式
- 错误处理

### 4.2 数据契约
- JSON Schema
- 数据模型

## 5. 部署架构
### 5.1 部署方案
- 容器化
- 编排方案
- 监控日志

## 6. 扩展性设计
### 6.1 水平扩展
- 负载均衡
- 服务集群

### 6.2 垂直扩展
- 性能优化
- 缓存策略
```

---

## 使用示例

### 示例1：SaaS平台架构设计

**输入**："设计一个多租户SaaS平台"

**输出**：
```
🏗️ 架构设计
模式：多租户微服务架构

📦 模块划分
核心模块：
- TenantService: 租户管理
- AuthService: 认证授权
- BillingService: 计费管理
- DataService: 数据隔离

🔧 技术栈
后端：
  - 框架：Node.js + NestJS
  - 数据库：PostgreSQL (schema隔离)
  - 缓存：Redis (租户级隔离)

前端：
  - 框架：React
  - 状态：Zustand
  - UI：Ant Design

🔗 接口设计
REST API + JWT认证
多租户隔离：tenant_id header
```

---

## 质量检查清单

- [ ] 需求分析完整
- [ ] 架构模式合理
- [ ] 技术选型有依据
- [ ] 模块边界清晰
- [ ] 接口定义完整
- [ ] 考虑扩展性
- [ ] 考虑安全性

---

## 协作技能

- **dnaspec-architect**: 主架构协调器（调用此技能）
- **dnaspec-modulizer**: 模块化验证和封装
- **dnaspec-context-analysis**: 需求分析质量评估

---

## 关键成就

1. ✅ **技术架构设计** - 系统化的架构设计方法
2. ✅ **技术栈选择** - 基于多因素的选择框架
3. ✅ **模块划分** - 领域驱动的模块化设计
4. ✅ **接口定义** - 清晰的API规范
5. ✅ **全生命周期应用** - Idea→需求→细化→智能四阶段
6. ✅ **职责明确** - 与architect协调器职责清晰区分

---

*此技能专注于技术架构设计，包括技术栈选择、模块划分和接口定义。它是dnaspec-architect协调器调用的子技能，专注于技术架构层面的设计和决策。*
