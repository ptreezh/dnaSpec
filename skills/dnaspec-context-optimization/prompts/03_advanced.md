# DNASPEC Context Optimization - 高级应用

## 智能优化

### 基于诊断的优化

```yaml
diagnostic_based_optimization:
  clarity_issues:
    strategy: 简化语言、改进结构
    priority: 高

  completeness_gaps:
    strategy: 补充信息、添加细节
    priority: 高

  consistency_problems:
    strategy: 统一术语、统一风格
    priority: 中

  efficiency_issues:
    strategy: 删除冗余、提升密度
    priority: 中
```

### 自适应优化

```yaml
adaptive_optimization:
  context_size_based:
    small (< 3k tokens):
      - 聚焦清晰度
      - 改进结构

    medium (3k-10k tokens):
      - 删除冗余
      - 统一术语

    large (> 10k tokens):
      - 大幅压缩
      - 提取核心

  quality_based:
    low_quality (< 0.5):
      - 全面优化
      - 多轮改进

    medium_quality (0.5-0.8):
      - 针对性优化
      - 重点改进

    high_quality (> 0.8):
      - 微调优化
      - 精细打磨
```

## 大规模优化

### 批量优化

```yaml
batch_optimization:
  multiple_contexts:
    - 识别相似上下文
    - 批量应用优化
    - 统一质量标准

  example:
    contexts:
      - context_001_user_auth
      - context_002_order_flow
      - context_003_payment_api

    optimization:
      - 统一术语
      - 统一风格
      - 统一格式
```

### 模板化优化

```yaml
template_based_optimization:
  create_templates:
    - 识别重复模式
    - 创建优化模板
    - 批量应用

  example:
    template: |
      # {模块名称}系统

      ## 功能
      - {功能列表}

      ## 约束
      - {约束条件}

    application: 批量优化所有模块文档
```

## 企业级优化

### 自动化优化

```yaml
automated_optimization:
  pre_commit_hooks:
    - 自动检测冗余
    - 自动统一术语
    - 自动压缩内容

  ci_integration:
    - CI/CD集成优化
    - 自动质量检查
    - 自动修复问题
```

### 质量门禁

```yaml
quality_gates:
  minimum_quality:
    threshold: 0.65
    action: 不达标不允许合并

  target_quality:
    threshold: 0.80
    action: 鼓励达到

  optimization_required:
    - 质量评分 < 0.65
    - 必须优化后才能发布
```

## 最佳实践

### 优化原则

```yaml
principles:
  preserve_essence:
    - 不删除关键信息
    - 不改变核心含义
    - 不影响功能

  gradual_improvement:
    - 逐步优化
    - 避免大改
    - 保持稳定

  user_confirmed:
    - 优化需用户确认
    - 支持回滚
    - 记录变更
```

### 优化时机

```yaml
timing:
  ideal_moments:
    - 需求评审后
    - 设计评审后
    - 代码评审前
    - 发布前

  trigger_conditions:
    - context-analysis发现问题
    - 质量评分下降
    - 上下文膨胀
```
