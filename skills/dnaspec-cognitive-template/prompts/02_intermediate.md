# DNASPEC Cognitive Template - 中级应用

## 高级模板模式

### 4. 设计模板 (Design Template)

**用途**：系统化设计解决方案

```yaml
design_template:
  phases:
    1. 需求分析:
       - 功能需求
       - 非功能需求
       - 约束条件

    2. 方案设计:
       - 架构设计
       - 接口设计
       - 数据设计

    3. 权衡分析:
       - 方案对比
       - 优劣分析
       - 风险评估

    4. 详细设计:
       - 实现细节
       - 技术选型
       - 开发计划

  example:
    设计: 用户认证系统

    需求分析:
      - 功能: 注册、登录、密码重置
      - 非功能: 安全、快速、可用
      - 约束: JWT、Node.js

    方案设计:
      - 架构: 认证服务 + JWT
      - 接口: REST API
      - 数据: 用户表 + token表

    权衡分析:
      - JWT vs Session: JWT无状态，适合分布式
      - 风险: Token过期处理

    详细设计:
      - bcrypt加密
      - 24小时有效期
```

### 5. 问题解决模板 (Problem-Solving Template)

**用途**：系统化解决复杂问题

```yaml
problem_solving_template:
  steps:
    1. 问题定义:
       - 清晰描述问题
       - 量化问题影响
       - 识别问题根源

    2. 方案生成:
       - 头脑风暴方案
       - 评估可行性
       - 选择最优方案

    3. 实施计划:
       - 制定步骤
       - 分配资源
       - 设定里程碑

    4. 执行验证:
       - 实施方案
       - 监控效果
       - 验证解决

  example:
    问题: 系统响应慢

    问题定义:
      - 响应时间: 平均5秒，目标<1秒
      - 影响: 用户体验差，流失率高
      - 根源: 数据库查询慢

    方案生成:
      - 方案1: 添加缓存
      - 方案2: 优化查询
      - 方案3: 读写分离
      - 选择: 方案1（最快速）

    实施计划:
      - 步骤1: 引入Redis
      - 步骤2: 缓存热点数据
      - 步骤3: 监控命中率

    执行验证:
      - 实施: 完成Redis集成
      - 效果: 响应时间降至0.5秒
      - 验证: ✅ 问题解决
```

## 模板组合

### 串行组合

```yaml
serial_composition:
  example: 设计并实现登录功能

  模板链:
    1. 理解模板 → 理解登录需求
    2. 设计模板 → 设计登录方案
    3. 推理模板 → 推导实现细节
    4. 验证模板 → 验证实现质量

  优势:
    - 系统化处理
    - 无遗漏
    - 质量保证
```

### 并行组合

```yaml
parallel_composition:
  example: 全面评估项目质量

  模板组:
    1. 验证模板 → 功能验证
    2. 验证模板 → 性能验证
    3. 验证模板 → 安全验证

  优势:
    - 全面覆盖
    - 并行处理
    - 效率提升
```

## 模板定制

### 场景适配

```yaml
context_adaptation:
  small_project:
    template: 简化版理解模板
    focus: 核心功能
    depth: 基础

  medium_project:
    template: 标准理解模板
    focus: 功能 + 非功能
    depth: 中等

  large_project:
    template: 增强理解模板
    focus: 全面考虑
    depth: 深入
```

### 角色适配

```yaml
role_adaptation:
  developer:
    focus: 实现细节
    template: 设计模板 + 推理模板

  architect:
    focus: 架构设计
    template: 设计模板 + 问题解决模板

  tester:
    focus: 质量验证
    template: 验证模板 + 理解模板
```
