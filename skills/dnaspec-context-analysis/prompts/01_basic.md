# DNASPEC Context Analysis - 基础应用

## 五大质量维度详解

### 1. 清晰度 (Clarity)

**评估问题**：内容是否易于理解？

```yaml
clarity_assessment:
  good_indicators:
    - 使用简单明确的语言
    - 避免模糊术语
    - 逻辑清晰，易于跟随

  bad_indicators:
    - "智能分析"等模糊表述
    - 过多专业术语无解释
    - 逻辑跳跃，难以理解

  example:
    ❌ "做一个智能系统分析数据"
    ✅ "构建一个机器学习分类器，分析用户行为数据"
```

### 2. 相关性 (Relevance)

**评估问题**：内容是否与目标相关？

```yaml
relevance_assessment:
  good_indicators:
    - 所有内容与核心目标相关
    - 无冗余信息
    - 聚焦主题

  bad_indicators:
    - 包含不相关内容
    - 偏离主题
    - 信息冗余

  example:
    目标：设计用户认证系统
    ❌ 包含数据库设计细节（不相关）
    ✅ 聚焦认证流程和安全（相关）
```

### 3. 完整性 (Completeness)

**评估问题**：信息是否完整？

```yaml
completeness_assessment:
  good_indicators:
    - 包含所有必要信息
    - 无明显缺口
    - 考虑边界情况

  bad_indicators:
    - 缺少关键信息
    - 忽略重要场景
    - 功能定义不全

  example:
    用户系统需求
    ❌ "包括注册、登录"（不完整）
    ✅ "包括注册、登录、密码重置、账号管理"（完整）
```

### 4. 一致性 (Consistency)

**评估问题**：术语、逻辑是否一致？

```yaml
consistency_assessment:
  good_indicators:
    - 术语使用统一
    - 逻辑自洽
    - 风格一致

  bad_indicators:
    - 术语混用（用户/账号）
    - 逻辑矛盾
    - 风格不一致

  example:
    ❌ "用户"和"账号"混用
    ✅ 统一使用"用户"
```

### 5. 效率 (Efficiency)

**评估问题**：表达是否简洁高效？

```yaml
efficiency_assessment:
  good_indicators:
    - 简洁表达
    - 无重复内容
    - 信息密度高

  bad_indicators:
    - 冗长表述
    - 重复信息
    - 信息密度低

  example:
    ❌ "用户可以进行登录操作，登录后可以访问系统"
    ✅ "用户登录后可访问系统"
```

## 基础质量评分

```yaml
scoring:
  range: 0.0 - 1.0
  levels:
    0.8-1.0: 优秀
    0.6-0.8: 良好
    0.4-0.6: 中等
    0.2-0.4: 较差
    0.0-0.2: 差

  overall_quality:
    calculation: 加权平均
    weights:
      clarity: 0.25
      relevance: 0.20
      completeness: 0.25
      consistency: 0.20
      efficiency: 0.10
```
