---
name: dnaspec-context-analysis
description: Analyze context quality across clarity, relevance, completeness, consistency, and efficiency dimensions. Ensure quality consistency during simple-to-complex system evolution. Detect context explosion/corruption risks. When you need to evaluate context quality, identify information gaps, assess content effectiveness, or prevent context issues, use this skill. Works with context-optimization in continuous improvement cycle.
---

# DNASPEC Context Analysis

## 使用时机

当用户提到以下需求时，使用此技能：
- "分析上下文质量" 或 "context analysis"
- "评估内容清晰度" 或 "assess clarity"
- "检查信息完整性" 或 "check completeness"
- "优化内容效率" 或 "improve efficiency"
- "评估上下文一致性" 或 "evaluate consistency"
- "检测上下文问题" 或 "detect context issues"
- 需要评估对话或文档的质量
- 需要识别内容中的问题和改进空间
- 需要检测上下文爆炸/腐化风险
- 需要确保系统演化的质量一致性

**不要在以下情况使用**：
- ❌ 直接修改优化上下文（使用context-optimization技能）
- ❌ 一般文档编辑
- ❌ 代码重构

## 核心理念

### 🎯 确保从简单到复杂系统演化的质量一致性

**什么是质量一致性？**

在系统从简单到复杂的演化过程中，上下文质量应该保持一致，而不是随着复杂度增加而下降。

```
演化路径质量监控：

阶段1：最简版本（MVP）
├─ 上下文大小：1千 tokens
├─ 质量评分：clarity 0.85, completeness 0.80
└─ ✅ 质量基准建立

↓ 演化监控

阶段2：功能增强
├─ 上下文大小：5千 tokens
├─ 质量评分：clarity 0.82, completeness 0.78
└─ ⚠️ 轻微下降，需要注意

↓ 继续监控

阶段3：系统完善
├─ 上下文大小：15千 tokens
├─ 质量评分：clarity 0.70, completeness 0.65
└─ 🚨 质量显著下降，需要优化
```

**质量一致性保证**：

```
❌ 无质量监控的演化：
简单系统 → 复杂系统
质量: 高     → 低    ❌ 不可接受

✅ 有质量监控的演化：
简单系统 → [监控] → 复杂系统
质量: 高     → [保持] → 高    ✅ 质量一致性
```

### 🎯 与context-optimization的循环配合

**连续改进循环**：

```
context-analysis (发现问题)
    ↓
输出质量报告
    ↓
context-optimization (解决问题)
    ↓
优化上下文
    ↓
context-analysis (验证改进)
    ↓
确认质量提升
    ↓
持续监控
```

**配合策略**：

```yaml
analysis_phase:
  role: 诊断医生
  actions:
    - 检测上下文质量
    - 识别问题症状
    - 确定严重程度
    - 提供诊断报告

optimization_phase:
  role: 治疗专家
  actions:
    - 根据诊断报告
    - 实施治疗方案
    - 优化上下文
    - 提升质量指标

verification_phase:
  role: 复查医生
  actions:
    - 重新分析质量
    - 验证改进效果
    - 确认无副作用
    - 完成治疗周期
```

### 🎯 检测上下文爆炸和腐化风险

**风险检测指标**：

**爆炸风险信号**：
```yaml
risk_indicators:
  explosion:
    signals:
      - context_size: > 30k tokens (warning)
      - context_size: > 50k tokens (critical)
      - growth_rate: > 20% per version
      - redundancy_ratio: > 30%

    example_diagnosis:
      context_size: 45000 tokens
      growth_rate: "+25% from last version"
      redundancy: "35% (high)"
      risk_level: "CRITICAL - Explosion imminent"
      recommendation: "Immediate cleanup required"
```

**腐化风险信号**：
```yaml
risk_indicators:
  corruption:
    signals:
      - inconsistency: 术语冲突、逻辑矛盾
      - structure_chaos: 组织混乱、无序
      - information_burial: 关键信息被淹没
      - outdated_content: 过时信息未清理

    example_diagnosis:
      inconsistencies: "Multiple terms for same concept"
      structure: "Poor organization, no hierarchy"
      risk_level: "HIGH - Quality degrading"
      recommendation: "Restructure and clean up"
```

### 🎯 格式塔认知原则在质量分析中的应用

**整体性原则（Whole > Sum of Parts）**：

```
❌ 孤立分析各个维度：
clarity: 0.85
relevance: 0.75
completeness: 0.65
consistency: 0.80
efficiency: 0.70

问题：看不出整体质量如何

✅ 整体分析：
overall_quality: weighted_average(clarity, relevance, completeness, consistency, efficiency)
              = 0.75

关键洞察：
- 整体质量中等
- completeness是短板（0.65）
- 应优先改进completeness

→ 这体现了整体性原则：关注整体质量，识别短板
```

**从简单到复杂演化**：

```
质量演化监控：

简单系统（整体简单）
├─ 清晰度检查：是否足够简单易懂？
└─ 一致性检查：逻辑是否自洽？

↓ 演化到复杂系统

复杂系统（包含多个子系统）
├─ 清晰度检查：每个子系统是否清晰？
├─ 一致性检查：子系统间是否一致？
└─ 整体性检查：整体是否协调？

→ 随着复杂度增加，质量检查维度增加
→ 确保质量不随复杂度下降
```

---

## 全生命周期应用

### 📋 Idea阶段：分析初始概念的清晰度

**场景**：用户有一个模糊的想法，需要评估其清晰度

**示例**：
```
用户想法："我想做一个AI系统，能够智能分析数据"

质量分析：
📋 清晰度评估 (Clarity: 0.45)
问题分析：
  ❌ "智能分析"太模糊
  ❌ 不清楚是什么类型的数据
  ❌ 不清楚分析的目的

建议：
  ✅ 明确"智能分析"的具体含义
  ✅ 定义数据类型（文本、图像、数值...）
  ✅ 说明分析目的（分类、聚类、预测...）

📋 完整性评估 (Completeness: 0.35)
缺失信息：
  ❌ 没有技术约束
  ❌ 没有使用场景
  ❌ 没有成功标准

建议：
  ✅ 补充技术约束（Python、实时、离线...）
  ✅ 描述使用场景（Web应用、移动端...）
  ✅ 定义成功标准（准确率、响应时间...）

✅ 综合建议
这个想法当前不够清晰，需要：
1. 具体化"智能分析"的含义
2. 明确数据类型和分析目标
3. 补充技术约束和使用场景

下一步：使用 /dnaspec.context-optimization 来优化概念描述
```

**使用技能**：
```
/dnaspec.context-analysis "AI数据分析系统的初始概念"
→ 分析清晰度、完整性
→ 识别模糊点
→ 提供具体化建议
```

### 📋 需求阶段：评估功能需求的完整性

**场景**：有完整的需求文档，需要评估其质量

**示例**：
```
需求文档片段："用户系统包括注册、登录、密码重置功能"

质量分析：
📋 完整性评估 (Completeness: 0.55)
存在缺口：
  ❌ 缺少用户信息管理功能
  ❌ 缺少权限管理功能
  ❌ 缺少账号安全功能（两步验证）

建议补充：
  ✅ 添加用户信息查看和修改
  ✅ 定义角色和权限体系
  ✅ 增加安全验证机制

📋 一致性评估 (Consistency: 0.70)
问题：
  ⚠️ "用户"和"账号"术语混用
  ⚠️ 缺少统一的术语表

建议：
  ✅ 统一使用"用户"或"账号"
  ✅ 建立术语表

📋 相关性评估 (Relevance: 0.85)
✅ 良好：
  - 功能描述与目标相关
  - 聚焦用户认证核心

✅ 综合建议
需求文档基本相关，但需要：
1. 补充关键功能（信息管理、权限）
2. 统一术语使用
3. 增加安全考虑

下一步：使用 /dnaspec.context-optimization 优化需求文档
```

**使用技能**：
```
/dnaspec.context-analysis "用户系统需求文档"
→ 评估完整性
→ 识别功能缺口
→ 检查术语一致性
→ 提供补充建议
```

### 📋 细化阶段：检查模块接口定义一致性

**场景**：系统有多个模块，需要检查接口定义的一致性

**示例**：
```
模块接口检查：

模块A：用户服务
├─ 接口：getUserById(userId)
├─ 返回：User对象
└─ 错误：抛出UserNotFoundException

模块B：订单服务
├─ 接口：getOrderUser(orderId)
├─ 返回：User对象
└─ 错误：返回null（用户不存在）

质量分析：
📋 一致性评估 (Consistency: 0.50)
严重不一致：
  ❌ 错误处理策略不同
     - 模块A：抛出异常
     - 模块B：返回null

  ❌ 命名风格不同
     - 模块A：驼峰命名
     - 模块B：驼峰命名（✅一致）

  ❌ 返回类型不完全一致
     - 都返回User对象（✅一致）
     - 但错误处理不同（❌不一致）

建议统一：
  ✅ 统一错误处理策略（都抛出异常或都返回null）
  ✅ 统一命名规范（已一致）
  ✅ 统一返回格式

📋 清晰度评估 (Clarity: 0.70)
问题：
  ⚠️ 接口命名不够清晰
     - getUserById：清晰 ✅
     - getOrderUser：不清晰 ❌（是获取订单的用户，还是用户的所有订单？）

建议：
  ✅ 重命名为getUserByOrderId或getOrdersByUserId

📋 完整性评估 (Completeness: 0.65)
缺失：
  ❌ 缺少参数校验说明
  ❌ 缺少返回值完整定义
  ❌ 缺少错误码文档

建议：
  ✅ 补充参数校验规则
  ✅ 完整定义User对象结构
  ✅ 文档化所有可能的错误

✅ 综合建议
接口定义存在严重一致性问题：
1. 统一错误处理策略（关键）
2. 改进模糊的接口命名
3. 补充完整的接口文档

下一步：使用 /dnaspec.context-optimization 修复一致性问题
```

**使用技能**：
```
/dnaspec.context-analysis "模块间接口定义"
→ 检查跨模块一致性
→ 识别接口不匹配
→ 发现命名冲突
→ 提供统一建议
```

### 📋 智能阶段：验证智能体交互协议有效性

**场景**：多个智能体协作，需要验证其交互协议的质量

**示例**：
```
智能体交互系统：

主协调器 (ProjectHealthCoordinator)
    ↓ 分发任务给
├─ CodeQualityAgent
├─ TestCoverageAgent
└─ DependencyHealthAgent

质量分析：
📋 协议一致性评估 (Consistency: 0.60)
问题：
  ❌ 消息格式不统一
     - CodeQualityAgent: JSON格式
     - TestCoverageAgent: 纯文本格式
     - DependencyHealthAgent: JSON格式

  ❌ 错误处理不一致
     - CodeQualityAgent: 抛出异常
     - TestCoverageAgent: 返回error字段
     - DependencyHealthAgent: 返回null

  ❌ 超时设置不统一
     - CodeQualityAgent: 30秒
     - TestCoverageAgent: 60秒
     - DependencyHealthAgent: 无限制

建议统一：
  ✅ 统一消息格式为JSON
  ✅ 统一错误处理机制
  ✅ 统一超时策略（建议30秒）

📋 协议清晰度评估 (Clarity: 0.70)
问题：
  ⚠️ 消息schema定义不清晰
     - 缺少必需字段说明
     - 缺少可选字段标记
     - 缺少数据类型定义

  ⚠️ 协议版本管理缺失
     - 没有版本号
     - 难以向后兼容

建议：
  ✅ 定义完整的消息schema
  ✅ 使用JSON Schema或类似工具
  ✅ 引入协议版本管理

📋 协议完整性评估 (Completeness: 0.65)
缺失：
  ❌ 缺少认证机制
  ❌ 缺少重试策略
  ❌ 缺少降级机制
  ❌ 缺少监控和日志

建议：
  ✅ 增加API密钥认证
  ✅ 定义重试规则（最多3次，指数退避）
  ✅ 增加降级策略（失败时返回缓存结果）
  ✅ 统一日志格式和监控指标

📋 效率评估 (Efficiency: 0.75)
问题：
  ⚠️ 消息过大
     - 部分消息包含不必要的数据
     - 平均消息大小：5KB

  ⚠️ 存在冗余字段
     - 部分字段重复传输

建议：
  ✅ 优化消息大小，只传输必需数据
  ✅ 删除冗余字段
  ✅ 目标：消息大小 < 2KB

✅ 综合建议
智能体交互协议存在严重一致性问题：
1. 统一消息格式和错误处理（关键）
2. 完善协议文档和schema定义
3. 增加认证、重试、降级机制
4. 优化消息大小，提高效率

下一步：使用 /dnaspec.context-optimization 优化交互协议
```

**使用技能**：
```
/dnaspec.context-analysis "智能体交互协议"
→ 检查协议一致性
→ 验证消息格式
→ 评估错误处理
→ 检测性能瓶颈
```

---

## 核心功能

### 五维质量指标

**1. 清晰度 (Clarity) - 0.0 to 1.0**

**评估要点**：
- 使用精确的语言表达
- 逻辑流程清晰
- 避免模糊术语
- 结构组织明确

**评分标准**：
- 0.9-1.0: 表达非常清晰，易于理解
- 0.7-0.9: 表达基本清晰，少数地方需要改进
- 0.5-0.7: 表达一般，部分内容不够明确
- 0.3-0.5: 表达不够清晰，需要多处修改
- 0.0-0.3: 表达模糊，难以理解

**2. 相关性 (Relevance) - 0.0 to 1.0**

**评估要点**：
- 与主题直接相关
- 符合目标受众需求
- 与既定目标一致
- 消除离题内容

**评分标准**：
- 0.9-1.0: 高度相关，完全符合目标
- 0.7-0.9: 基本相关，少数内容偏离
- 0.5-0.7: 部分相关，需要聚焦核心内容
- 0.3-0.5: 相关性较低，大量无关内容
- 0.0-0.3: 缺乏相关性，严重偏离主题

**3. 完整性 (Completeness) - 0.0 to 1.0**

**评估要点**：
- 涵盖关键信息
- 包含所有必需元素
- 提供足够的细节
- 无关键信息缺失

**评分标准**：
- 0.9-1.0: 信息完整，涵盖所有要点
- 0.7-0.9: 基本完整，缺少少数次要细节
- 0.5-0.7: 部分完整，缺少一些重要信息
- 0.3-0.5: 完整性不足，缺少关键内容
- 0.0-0.3: 信息严重缺失

**4. 一致性 (Consistency) - 0.0 to 1.0**

**评估要点**：
- 术语使用一致
- 逻辑流畅连贯
- 无矛盾陈述
- 事实前后呼应

**评分标准**：
- 0.9-1.0: 高度一致，无矛盾
- 0.7-0.9: 基本一致，个别小矛盾
- 0.5-0.7: 存在一些不一致
- 0.3-0.5: 一致性较差，多处矛盾
- 0.0-0.3: 严重不一致，逻辑混乱

**5. 效率 (Efficiency) - 0.0 to 1.0**

**评估要点**：
- 长度适中
- 消除冗余
- 简洁明了
- 信噪比高

**评分标准**：
- 0.9-1.0: 高度精炼，无冗余
- 0.7-0.9: 效率较高，少量冗余
- 0.5-0.7: 效率一般，存在重复内容
- 0.3-0.5: 效率较低，冗余较多
- 0.0-0.3: 冗长啰嗦，信息密度低

---

## 上下文风险检测

### 上下文爆炸风险检测

**检测维度**：

```yaml
explosion_risk_assessment:
  size_analysis:
    current_size: 45000 tokens
    soft_limit: 30000 tokens
    hard_limit: 50000 tokens
    status: "WARNING - Exceeds soft limit"

  growth_analysis:
    last_version: 36000 tokens
    current_version: 45000 tokens
    growth: "+25%"
    growth_rate: "HIGH - Accelerating"

  redundancy_analysis:
    total_content: 45000 tokens
    unique_content: 31500 tokens
    redundancy: 13500 tokens (30%)
    redundancy_ratio: "HIGH - Needs cleanup"

  risk_level: "CRITICAL"
  prediction: "Will exceed hard limit in 1-2 versions"
  recommendation: "Immediate optimization required"
```

**风险等级**：
- 🟢 Low: < 20k tokens, growth < 10%, redundancy < 15%
- 🟡 Medium: 20-30k tokens, growth 10-20%, redundancy 15-25%
- 🟠 High: 30-50k tokens, growth 20-30%, redundancy 25-35%
- 🔴 Critical: > 50k tokens, growth > 30%, redundancy > 35%

### 上下文腐化风险检测

**检测维度**：

```yaml
corruption_risk_assessment:
  consistency_check:
    term_conflicts: 5 found
    logic_contradictions: 2 found
    fact_discrepancies: 3 found
    consistency_score: 0.65 (needs improvement)

  structure_check:
    organization: "Poor - No clear hierarchy"
    navigation: "Difficult - Information scattered"
    key_info_visibility: "Low - Buried in details"
    structure_score: 0.55 (needs restructure)

  freshness_check:
    outdated_content: 15% of total
    deprecated_info: 8% of total
    last_cleanup: "3 versions ago"
    freshness_score: 0.70 (needs cleanup)

  risk_level: "HIGH"
  diagnosis: "Context quality degrading"
  recommendation: "Restructure and cleanup required"
```

**腐化类型**：
- 🟡 Mild: 少数不一致，结构基本清晰
- 🟠 Moderate: 明显不一致，结构混乱
- 🔴 Severe: 严重不一致，结构完全混乱

---

## 分析流程

### 第一步：评估清晰度
- 检查语言表达是否精确
- 分析逻辑结构是否清晰
- 识别模糊或歧义的表述
- 提供改进建议

### 第二步：评估相关性
- 分析内容与主题的相关程度
- 识别离题或无关内容
- 评估是否符合目标受众
- 建议聚焦核心内容

### 第三步：评估完整性
- 识别关键信息是否完整
- 检查是否缺少必需元素
- 评估细节是否充分
- 建议补充缺失内容

### 第四步：评估一致性
- 检查术语使用是否一致
- 识别逻辑矛盾
- 验证事实准确性
- 建议统一表述

### 第五步：评估效率
- 分析内容长度是否合适
- 识别冗余或重复内容
- 评估信息密度
- 建议精简优化

### 第六步：检测风险
- 检测上下文爆炸风险
- 检测上下文腐化风险
- 评估风险严重程度
- 提供风险缓解建议

---

## 输出格式

```json
{
  "summary": {
    "context_length": 1234,
    "token_count_estimate": 300,
    "overall_quality": 0.75,
    "primary_dimension": "completeness",
    "risk_assessment": {
      "explosion_risk": "medium",
      "corruption_risk": "low"
    }
  },
  "metrics": {
    "clarity": 0.82,
    "relevance": 0.75,
    "completeness": 0.68,
    "consistency": 0.80,
    "efficiency": 0.70
  },
  "issues": [
    "部分段落表达不够清晰",
    "缺少关键的技术细节",
    "术语使用不统一"
  ],
  "suggestions": [
    "重新组织第3段的结构，提高清晰度",
    "补充实现细节以提升完整性",
    "统一技术术语的使用"
  ],
  "risk_indicators": {
    "explosion": {
      "current_size": 28000,
      "growth_rate": "+15%",
      "redundancy": "22%",
      "risk_level": "medium",
      "recommendation": "Monitor growth, consider cleanup"
    },
    "corruption": {
      "inconsistencies": 2,
      "structure_issues": "minor",
      "outdated_content": "5%",
      "risk_level": "low",
      "recommendation": "Minor cleanup recommended"
    }
  },
  "dimension_analysis": {
    "clarity": {
      "score": 0.82,
      "strengths": ["整体逻辑清晰", "结构合理"],
      "weaknesses": ["少数句子过长", "部分术语未定义"],
      "recommendations": ["简化复杂句子", "添加术语表"]
    },
    "relevance": {
      "score": 0.75,
      "strengths": ["与主题相关"],
      "weaknesses": ["部分内容偏离核心"],
      "recommendations": ["删除离题内容", "聚焦关键主题"]
    },
    "completeness": {
      "score": 0.68,
      "strengths": ["覆盖主要要点"],
      "weaknesses": ["缺少实施细节", "示例不足"],
      "recommendations": ["添加具体示例", "补充实施步骤"]
    },
    "consistency": {
      "score": 0.80,
      "strengths": ["逻辑基本连贯", "无重大矛盾"],
      "weaknesses": ["术语偶尔不一致"],
      "recommendations": ["统一术语表", "检查表述一致性"]
    },
    "efficiency": {
      "score": 0.70,
      "strengths": ["长度适中"],
      "weaknesses": ["存在重复表述", "部分说明冗余"],
      "recommendations": ["删除重复内容", "精简说明"]
    }
  },
  "next_steps": {
    "recommended_skill": "context-optimization",
    "priority_actions": [
      "Improve completeness (lowest score)",
      "Reduce redundancy to prevent explosion",
      "Standardize terminology"
    ]
  }
}
```

---

## 质量检查清单

### 分析完整性检查
- [ ] 评估所有五个维度
- [ ] 提供数值评分 (0.0-1.0)
- [ ] 识别具体问题
- [ ] 提供可操作的改进建议
- [ ] 给出评分理由
- [ ] 输出结构化格式

### 风险检测检查
- [ ] 检测上下文爆炸风险
- [ ] 检测上下文腐化风险
- [ ] 评估风险严重程度
- [ ] 提供风险缓解建议
- [ ] 推荐下一步行动

### 质量一致性检查
- [ ] 提供整体质量评分
- [ ] 识别最低分维度（短板）
- [ ] 提供优先改进建议
- [ ] 确保建议可操作
- [ ] 推荐配合技能

---

## 协作技能

- **dnaspec-context-optimization**: 优化上下文质量，解决analysis发现的问题
- **dnaspec-architect**: 整体架构协调，确保系统一致性
- **dnaspec-task-decomposer**: 任务分解质量分析

---

## 关键成就

1. ✅ **五维质量评估** - 全面分析清晰度、相关性、完整性、一致性、效率
2. ✅ **质量一致性保证** - 确保从简单到复杂演化的质量稳定
3. ✅ **风险检测机制** - 检测上下文爆炸和腐化风险
4. ✅ **与optimization配合** - 循环改进，持续提升
5. ✅ **全生命周期应用** - Idea→需求→细化→智能四阶段
6. ✅ **格式塔原则体现** - 整体性分析，识别短板，从简单到复杂演化

---

*此技能提供系统化的上下文质量分析，通过五维评估和风险检测，确保从简单到复杂系统演化过程中的质量一致性，与context-optimization形成连续改进循环。*
