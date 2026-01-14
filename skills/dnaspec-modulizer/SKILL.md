---
name: dnaspec-modulizer
description: Decompose system into reusable modules with bottom-up modularization. Prevent system from becoming overly complex. Ensure clear module boundaries with high cohesion, low coupling, clear interfaces, independent testability, and reusability. When you need modular design, module refactoring, or preventing system complexity, use this skill.
---

# DNASPEC Modulizer

## 使用时机

当用户提到以下需求时，使用此技能：
- "模块化设计" 或 "modularization design"
- "模块成熟度验证" 或 "module maturity verification"
- "自底向上模块化" 或 "bottom-up modularization"
- "模块重构" 或 "module refactoring"
- "高内聚低耦合" 或 "high cohesion low coupling"
- "避免系统过于庞杂" 或 "prevent system complexity"
- "模块边界清晰" 或 "clear module boundaries"
- 需要将系统分解为可重用模块
- 需要确保模块独立性

**不要在以下情况使用**：
- ❌ 初始系统架构设计（使用architect技能）
- ❌ 一般代码重构
- ❌ 具体实现细节

## 核心理念

### 🎯 自底向上模块化（Bottom-Up Modularization）

**什么是自底向上模块化？**

自底向上模块化是指从最底层的原子模块开始，逐步组装成更高级的模块，最终形成完整系统。

```
❌ 自顶向下（Top-Down）的问题：

先设计整体架构
    ↓
分解为子系统
    ↓
分解为模块
    ↓
实现模块

问题：
- 实现时发现架构不合理
- 模块间依赖复杂
- 难以独立测试
- 模块难以重用
```

```
✅ 自底向上（Bottom-Up）的优势：

从原子模块开始
├─ 模块1：独立、可测试、可重用
├─ 模块2：独立、可测试、可重用
└─ 模块3：独立、可测试、可重用
    ↓
组装为功能单元
├─ 功能单元A = 模块1 + 模块2
└─ 功能单元B = 模块2 + 模块3
    ↓
组装为子系统
└─ 子系统 = 功能单元A + 功能单元B
    ↓
完整系统

优势：
✅ 每个模块独立可测试
✅ 模块可重用
✅ 模块间依赖清晰
✅ 易于维护和演化
```

**自底向上的关键原则**：

**1. 原子模块优先**
```yaml
atomic_modules:
  definition: 最小功能单元，不可再分
  characteristics:
    - 单一职责
    - 独立可测试
    - 无外部依赖
    - 可独立版本管理

  example:
    - DateUtil: 日期处理工具
    - StringValidator: 字符串验证
    - HttpClient: HTTP请求封装
```

**2. 逐步组装**
```yaml
assembly_principle:
  step_1: 验证原子模块成熟度
    - test_coverage > 80%
    - 接口稳定
    - 文档完整

  step_2: 组装为功能单元
    - 组合多个原子模块
    - 定义新的接口
    - 保持独立性

  step_3: 继续组装
    - 从功能单元到子系统
    - 从子系统到完整系统
    - 每层都保持独立性
```

**3. 模块独立版本管理**
```yaml
independent_versioning:
  principle: 每个模块独立演进

  example:
    module_v1: "1.0.0" - 稳定版本
    module_v2: "2.0.0" - 新功能，向后兼容
    module_v3: "3.0.0" - 重构，可能不兼容

  benefit:
    - 模块可独立升级
    - 不影响其他模块
    - 降低维护成本
```

### 🎯 避免系统过于庞杂（Preventing System Bloat）

**什么是系统庞杂？**

系统庞杂是指：
- 模块数量过多但边界不清
- 模块间依赖复杂（循环依赖）
- 模块职责不清晰
- 难以理解和维护

**防止庞杂的措施**：

**措施1：模块数量控制**
```yaml
module_count_control:
  principle: 7±2原则（工作记忆容量）

  guidelines:
    - 一级模块：5-9个
    - 二级模块：每个一级模块下5-9个
    - 三级模块：必要时，但尽量少

  example:
    level_1: 7个一级模块 ✅ 在认知范围内
    level_2: 每个一级模块平均5个二级模块 ✅ 可控
    level_3: 少量三级模块 ✅ 必要时使用
```

**措施2：依赖方向控制**
```yaml
dependency_control:
  principle: 单向依赖，禁止循环

  rules:
    - 只允许单向依赖
    - 禁止循环依赖
    - 禁止跨层依赖

  example:
    ✅ valid:
      module_A → module_B → module_C
      (单向依赖链)

    ❌ invalid:
      module_A → module_B → module_A
      (循环依赖)

    ❌ invalid:
      level_3_module → level_1_module
      (跨层依赖)
```

**措施3：模块粒度控制**
```yaml
module_granularity:
  too_small:
    problem: 模块过多，管理复杂
    example: 每个函数一个模块 ❌

  too_large:
    problem: 模块职责不清晰
    example: 整个系统一个模块 ❌

  appropriate:
    principle: 单一职责，高内聚
    example: 用户认证模块 ✅
```

### 🎯 高内聚低耦合（High Cohesion, Low Coupling）

**内聚性（Cohesion）**：
- **高内聚**：模块内的元素紧密相关，共同完成一个功能
- **低内聚**：模块内的元素关系松散，职责不明确

**耦合度（Coupling）**：
- **低耦合**：模块间依赖少，接口清晰
- **高耦合**：模块间依赖多，接口模糊

```
❌ 低内聚、高耦合的例子：

UserService模块（低内聚）
├─ 用户登录功能
├─ 发送邮件功能  ← 不相关！
├─ 数据加密功能  ← 不相关！
└─ 日志记录功能  ← 不相关！

依赖关系（高耦合）：
UserService → DatabaseService
UserService → EmailService
UserService → CryptoService
UserService → LogService
EmailService → DatabaseService
LogService → DatabaseService
...（复杂的依赖网）

→ 问题：职责不清，依赖复杂
```

```
✅ 高内聚、低耦合的例子：

AuthService模块（高内聚）
├─ 用户登录
├─ 用户注册
├─ 密码管理
└─ 会话管理

依赖关系（低耦合）：
AuthService → DatabaseRepository (接口)
AuthService → CryptoModule (加密工具)

→ 其他模块只通过接口访问
→ 依赖清晰，易于维护
```

**高内聚低耦合的标准**：
```yaml
high_cohesion:
  criteria:
    - 模块内所有功能围绕一个目标
    - 功能相关性强
    - 删除模块会破坏系统完整性

low_coupling:
  criteria:
    - 模块间通过接口通信
    - 不依赖具体实现
    - 可独立替换
    - 最小化依赖数量
```

### 🎯 格式塔认知原则在模块化中的应用

**整体性原则**：

```
❌ 碎片化的模块：
模块A：用户登录
模块B：用户登出
模块C：用户注册
模块D：密码修改

问题：都是用户相关，却分散在多个模块

✅ 整体化的模块：
UserAuth模块（整体）
├─ 用户登录
├─ 用户登出
├─ 用户注册
└─ 密码修改

优势：高内聚，职责清晰，易于理解
```

**从简单到复杂演化**：

```
演化路径：

阶段1：原子模块（简单）
├─ DateUtil
├─ StringValidator
└─ HttpClient
→ 每个模块简单独立

↓ 逐步组装

阶段2：功能单元（稍复杂）
├─ UserAuth = HttpClient + CryptoUtil
├─ DataSync = HttpClient + DateUtil
└─ Notification = HttpClient + TemplateEngine
→ 组装，但保持独立

↓ 继续组装

阶段3：子系统（复杂）
└─ UserManagement = UserAuth + DataSync + Notification
→ 复杂，但每个组件都是成熟模块

关键：从简单模块开始，逐步组装成复杂系统
```

---

## 全生命周期应用

### 📋 Idea阶段：识别核心原子模块

**场景**：用户有一个想法，需要识别核心模块

**示例**：
```
用户想法："我想做一个电商平台"

模块识别：
📋 核心原子模块（自底向上）
├─ 用户模块（UserModule）
│   ├─ 注册
│   ├─ 登录
│   └─ 信息管理
├─ 商品模块（ProductModule）
│   ├─ 商品管理
│   ├─ 库存管理
│   └─ 价格管理
├─ 订单模块（OrderModule）
│   ├─ 订单创建
│   ├─ 订单支付
│   └─ 订单查询
└─ 支付模块（PaymentModule）
    ├─ 支付接口
    ├─ 退款处理
    └─ 对账管理

✅ 格式塔原则：每个模块都是"整体"
- 职责明确
- 高内聚
- 可独立开发
- 可独立测试
```

### 📋 需求阶段：确保模块边界清晰

**场景**：有完整需求，确保模块边界清晰

**示例**：
```
需求：电商平台的用户功能

模块边界定义：
📋 UserAuth模块（用户认证）
├─ 职责：用户身份认证
├─ 接口：
│   ├─ register(username, password)
│   ├─ login(username, password)
│   └─ logout(token)
└─ 边界：不处理用户资料（由UserProfile负责）

📋 UserProfile模块（用户资料）
├─ 职责：用户信息管理
├─ 接口：
│   ├─ getProfile(userId)
│   ├─ updateProfile(userId, data)
│   └─ uploadAvatar(userId, file)
└─ 边界：不处理认证（由UserAuth负责）

✅ 高内聚低耦合：
- UserAuth：只管认证
- UserProfile：只管资料
- 接口清晰
- 无职责重叠
```

### 📋 细化阶段：验证模块成熟度

**场景**：功能实现时，验证模块是否达到封装标准

**示例**：
```
模块：PaymentService

成熟度评估：
📊 Level 5 (封装级)

✅ 测试覆盖率：92%
✅ 接口稳定性：向后兼容3个版本
✅ 文档完整性：完整的API文档和使用示例
✅ 性能：P99响应时间 < 100ms
✅ 独立性：无外部依赖泄漏

✅ 可以封装为独立模块
📦 封装版本：1.0.0
📦 发布为：payment-service
📦 独立部署：支持
```

### 📋 智能阶段：模块化智能体系统

**场景**：智能体也需要模块化

**示例**：
```
智能体系统模块化：

📋 原子智能体（自底向上）
├─ CodeReviewAgent（代码审查）
├─ TestGenAgent（测试生成）
├─ DocGenAgent（文档生成）
└─ DeployAgent（部署助手）

📋 组装为功能单元
├─ QualityAssistant = CodeReviewAgent + TestGenAgent
└─ ReleaseAssistant = DocGenAgent + DeployAgent

📋 组装为子系统
└─ DevOpsTeam = QualityAssistant + ReleaseAssistant

✅ 格式塔原则：
- 每个智能体独立可测试
- 可组合为更高级的智能体系统
- 上下文隔离
- 接口统一
```

---

## 核心功能

### 1. 模块成熟度评估

**评估维度**：
- 功能完整性（10-30%）
- 测试覆盖率（30-50%）
- 文档完整性（50-70%）
- 接口稳定性（70-90%）
- 可封装性（90-100%）

**成熟度等级**：
```
Level 1: 初级 - 功能实现，基础测试
Level 2: 中级 - 完整测试，基本文档
Level 3: 高级 - 高覆盖率，完整文档
Level 4: 生产 - 稳定接口，性能优化
Level 5: 封装 - 可独立部署，版本管理
```

### 2. 自底向上封装策略

**封装条件**：
- ✅ 测试覆盖率 > 80%
- ✅ 接口文档完整
- ✅ 无外部依赖泄漏
- ✅ 性能达标

**封装步骤**：
1. 隔离模块接口
2. 创建版本标签
3. 生成API文档
4. 设置访问控制
5. 独立部署验证

### 3. 模块边界验证

**验证清单**：
- [ ] 职责单一明确
- [ ] 接口清晰稳定
- [ ] 无循环依赖
- [ ] 高内聚低耦合
- [ ] 可独立测试
- [ ] 可独立部署

---

## 输出格式

```json
{
  "modules": [
    {
      "name": "AuthService",
      "maturity_level": 5,
      "test_coverage": 0.92,
      "cohesion": "high",
      "coupling": "low",
      "can_encapsulate": true,
      "dependencies": ["Database", "Crypto"],
      "recommended_version": "1.0.0"
    }
  ],
  "assembly_plan": {
    "atomic_modules": ["DateUtil", "HttpClient", "CryptoUtil"],
    "functional_units": ["AuthService", "DataService"],
    "subsystems": ["UserManagement"]
  },
  "quality_metrics": {
    "total_modules": 15,
    "average_maturity": 4.2,
    "high_cohesion_modules": 13,
    "low_coupling_modules": 14
  }
}
```

---

## 质量检查清单

- [ ] 成熟度评估准确
- [ ] 遵循自底向上原则
- [ ] 模块边界清晰
- [ ] 高内聚低耦合
- [ ] 无循环依赖
- [ ] 可独立测试
- [ ] 可独立部署

---

## 协作技能

- **dnaspec-architect**: 整体架构设计
- **dnaspec-task-decomposer**: 任务分解协调
- **dnaspec-context-analysis**: 模块质量分析

---

## 关键成就

1. ✅ **自底向上模块化** - 从原子模块逐步组装
2. ✅ **高内聚低耦合** - 模块职责单一、依赖清晰
3. ✅ **避免系统庞杂** - 模块数量控制、依赖方向控制
4. ✅ **模块边界清晰** - 接口明确、职责单一
5. ✅ **独立测试能力** - 每个模块可独立测试
6. ✅ **可重用性设计** - 模块可在不同上下文重用

---

*此技能实现自底向上的模块化策略，通过高内聚低耦合的设计和清晰的模块边界，防止系统过于庞杂，确保模块的可重用性和可维护性。*
