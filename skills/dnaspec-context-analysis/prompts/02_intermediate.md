# DNASPEC Context Analysis - 中级应用

## 演化质量监控

### 质量演化路径

```
阶段1：最简版本（MVP）
├─ 上下文大小：1千 tokens
├─ 质量评分：Clarity 0.85, Completeness 0.80
└─ ✅ 质量基准建立

↓ 演化监控

阶段2：功能增强
├─ 上下文大小：5千 tokens
├─ 质量评分：Clarity 0.82, Completeness 0.78
└─ ⚠️ 轻微下降，需要注意

↓ 继续监控

阶段3：系统完善
├─ 上下文大小：15千 tokens
├─ 质量评分：Clarity 0.70, Completeness 0.65
└─ 🚨 质量显著下降，需要优化
```

### 质量一致性保证

```yaml
evolution_monitoring:
  baseline:
    - 在简单系统建立质量基准
    - 记录各维度评分

  tracking:
    - 每次演化后重新评估
    - 对比基准评分
    - 识别下降维度

  intervention:
    - 当质量下降 > 10% 时警告
    - 当质量下降 > 20% 时必须优化
    - 使用context-optimization修复
```

## 风险检测

### 上下文爆炸风险

```yaml
explosion_risk_indicators:
  signals:
    - context_size: > 30k tokens (warning)
    - context_size: > 50k tokens (critical)
    - growth_rate: > 20% per version
    - redundancy_ratio: > 30%

  diagnosis_example:
    context_size: 45000 tokens
    growth_rate: "+25% from last version"
    redundancy: "35% (high)"
    risk_level: "CRITICAL"
    recommendation: "Immediate cleanup required"
```

### 上下文腐化风险

```yaml
corruption_risk_indicators:
  signals:
    - inconsistency: 术语冲突、逻辑矛盾
    - structure_chaos: 组织混乱、无序
    - information_burial: 关键信息被淹没
    - outdated_content: 过时信息未清理

  diagnosis_example:
    inconsistencies: "Multiple terms for same concept"
    structure: "Poor organization, no hierarchy"
    risk_level: "HIGH"
    recommendation: "Restructure and clean up"
```

## 缺口识别

### 信息缺口分析

```yaml
gap_analysis:
  missing_information:
    - 识别缺失的关键信息
    - 识别未覆盖的场景
    - 识别未定义的接口

  example:
    context: "用户认证系统"
    gaps:
      - 缺少密码策略定义
      - 缺少错误处理说明
      - 缺少会话管理细节
```

### 不一致点识别

```yaml
inconsistency_detection:
  types:
    terminology:
      - 术语混用（用户/账号）
      - 同一概念多种表述

    logical:
      - 前后矛盾
      - 逻辑冲突

    structural:
      - 风格不一致
      - 格式不统一

  example:
    context: "用户系统"
    inconsistencies:
      - "用户"和"账号"混用
      - 错误处理策略不统一
```

## 与Context-Optimization配合

### 连续改进循环

```
context-analysis (诊断)
    ↓
输出质量报告
    ↓
context-optimization (治疗)
    ↓
优化上下文
    ↓
context-analysis (复查)
    ↓
确认质量提升
```

### 配合策略

```yaml
collaboration:
  analysis_role: 诊断医生
    - 检测上下文质量
    - 识别问题症状
    - 确定严重程度
    - 提供诊断报告

  optimization_role: 治疗专家
    - 根据诊断报告
    - 实施治疗方案
    - 优化上下文
    - 提升质量指标

  verification: 复查确认
    - 重新分析质量
    - 验证改进效果
    - 确认无副作用
```
