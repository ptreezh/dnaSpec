# DNASPEC Context Optimization - 中级应用

## 压缩优化

### 上下文压缩

```yaml
compression_strategies:
  remove_redundancy:
    - 删除重复表述
    - 合并相似内容
    - 提取核心信息

  example:
    before: |
      用户认证系统包括登录功能。登录功能允许用户登录。
      登录时需要输入用户名和密码。用户名和密码用于验证。

    after: |
      用户认证系统支持用户名密码登录验证。
```

### 信息密度提升

```yaml
density_improvement:
  concise_expression:
    - 使用更少的词表达相同含义
    - 避免啰嗦
    - 提炼关键点

  example:
    before: "为了能够实现用户登录的功能，我们需要用户输入用户名和密码"
    after: "用户登录需输入用户名和密码"
```

## 结构化优化

### 层次结构

```yaml
hierarchical_structure:
  组织原则:
    - 使用标题分层
    - 使用列表组织
    - 使用代码块突出

  example:
    # 用户认证系统

    ## 功能列表
    - 注册
    - 登录
    - 密码重置

    ## 技术栈
    - Node.js
    - JWT
```

### 信息架构

```yaml
information_architecture:
  pyramid_principle:
    - 核心结论在前
    - 支持细节在后
    - 自顶向下组织

  example:
    系统概述 → 核心功能 → 技术细节 → 实现方案
```

## 术语统一

### 术语表建立

```yaml
terminology_management:
  establish_glossary:
    - 识别核心概念
    - 定义标准术语
    - 记录同义词映射

  example:
    用户 (User):
      - 标准：用户
      - 避免：账号、账户、使用者

    登录 (Login):
      - 标准：登录
      - 避免：登入、signin、登录系统
```

### 一致性检查

```yaml
consistency_check:
  automated:
    - 检测术语混用
    - 检测风格不一致
    - 生成不一致报告

  manual:
    - 人工审查术语使用
    - 统一表达方式
    - 更新术语表
```

## 与Context-Analysis配合

### 优化循环

```
1. context-analysis 诊断问题
2. 输出质量报告
3. context-optimization 实施优化
4. context-analysis 验证改进
5. 确认质量提升
```

### 持续改进

```yaml
continuous_improvement:
  iterative:
    - 多轮优化
    - 逐步提升
    - 持续监控

  threshold_based:
    - 质量评分 < 0.6: 必须优化
    - 质量评分 0.6-0.8: 建议优化
    - 质量评分 > 0.8: 维持现状
```
