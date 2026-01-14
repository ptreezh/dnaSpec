---
name: dnaspec-constraint-generator
description: Generate dynamic constraints based on initial constitutional requirements with version management and time-point recovery. Ensure evolving requirements align with original goals. When you need constraint generation, API specifications, validation rules, or to prevent requirement drift from original vision, use this skill.
---

# DNASPEC Constraint Generator

## 使用时机

当用户提到以下需求时，使用此技能：
- "生成约束" 或 "generate constraints"
- "API规范" 或 "API specification"
- "数据验证规则" 或 "data validation rules"
- "质量约束" 或 "quality constraints"
- "宪法需求" 或 "constitutional requirements"
- "版本管理" 或 "version management"
- "防止偏离" 或 "prevent drift"
- "锁定需求" 或 "lock requirements"
- 需要确保系统演化不偏离基本目标

**不要在以下情况使用**：
- ❌ 讨论具体实现细节
- ❌ 代码调试

## 核心概念

### 🎯 宪法需求（Constitutional Requirements）

**什么是宪法需求？**

宪法需求是系统的**根本大法**，是项目初始阶段锁定的核心需求，具有以下特性：

**不可违背性**
- 宪法需求是系统的基石
- 所有后续需求必须对齐宪法
- 违反宪法的需求必须被拒绝

**时间稳定性**
- 一旦锁定，不得随意修改
- 修改需要经过正式的宪法修订流程
- 确保系统的长期一致性

**最高优先级**
- 当新需求与宪法冲突时，宪法优先
- 所有技术和业务决策都必须符合宪法
- 是所有约束的源头

**示例**：
```markdown
# 项目宪法 (Project Constitution)

## 核心目标
构建一个用户友好的AI代码助手

## 不可妥协原则
1. 用户体验优先
2. 隐私保护
3. 开源透明

## 技术边界
- 只支持Python和JavaScript
- 不收集用户代码
- 所有建议本地生成

## 质量标准
- 建议准确率 > 90%
- 响应时间 < 2秒
- 系统可用性 > 99.5%
```

### 🎯 时空记忆机制

**需求的时间线管理**

```
时间线 → T0 (宪法) → T1 → T2 → T3 → T4 → 现在
          ↓        ↓    ↓    ↓    ↓
        快照1    快照2  快照3 快照4 快照5
```

每个时间点都有需求快照：
- **T0**: 宪法需求（初始版本）
- **T1-Tn**: 演化过程中的需求版本
- **可以回滚**到任何历史时间点

**时间点恢复**

当需求偏离太远时，可以回滚到历史版本：

```bash
# 查看历史版本
dnaspec.constraint-generator "list-versions"
输出:
- v1.0 (2025-01-01) - 宪法版本
- v1.1 (2025-01-15) - 添加支付功能
- v1.2 (2025-02-01) - 添加社交功能
- v1.3 (2025-02-15) - 添加AI功能（偏离）
- v1.4 (2025-03-01) - 当前版本（严重偏离）

# 回滚到v1.2
dnaspec.constraint-generator "rollback-to-version v1.2"
→ 恢复到2025-02-01的需求状态
→ 重新审视偏离的需求
```

### 🎯 动态约束生成

**从宪法生成约束**

宪法需求 → 解析原则 → 生成约束

```
宪法: "用户体验优先"
  ↓
原则: "界面响应时间 < 2秒"
  ↓
约束: {
  "api_response_time": {
    "max": 2000,
    "unit": "ms",
    "enforcement": "strict"
  }
}
```

**约束随时间演化**

约束不是一成不变的，可以演化，但必须对齐宪法：

```
T0 (宪法): "隐私保护"
  ↓
约束1.0: "不收集用户数据"
  ↓
演化: 需要添加分析功能
  ↓
约束2.0: "只收集匿名统计数据"
  ↓
验证: ✅ 仍然对齐宪法
```

### 🎯 防止需求偏离

**偏离检测机制**

持续监控需求演化，检测偏离宪法的倾向：

```json
{
  "requirement": "添加广告系统",
  "constitutional_analysis": {
    "constitution": "用户体验优先",
    "alignment_score": 0.2,
    "conflicts": [
      "广告会损害用户体验"
    ],
    "recommendation": "拒绝此需求"
  }
}
```

**偏离纠正**

当检测到偏离时：
1. 警告：需求偏离宪法
2. 分析：偏离程度和原因
3. 建议：如何修正需求以对齐宪法
4. 决策：接受修正或拒绝需求

---

## 全生命周期应用

### 📋 Idea阶段：锁定初始需求为宪法版本

**场景**：项目初始阶段，需要确立根本原则

**操作**：
```
/dnaspec.constraint-generator "create-constitution"

系统提示：
"请提供初始核心需求"

用户输入：
"构建一个AI代码助手，核心价值是帮助开发者提高效率"

生成宪法：
---
# 项目宪法 v1.0

## 核心使命
帮助开发者提高编码效率

## 不可妥协原则
1. 开发者效率第一
2. 建议质量优先于数量
3. 尊重开发者意愿

## 技术边界
- 支持主流编程语言
- 不强制执行建议
- 提供解释和理由

## 质量标准
- 建议相关率 > 95%
- 建议准确率 > 85%
- 响应时间 < 1秒
---

宪法已锁定，所有后续需求必须对齐此宪法
```

**时间点标记**：T0 - 宪法版本

### 📋 需求阶段：生成新需求与宪法的对齐约束

**场景**：有新功能需求

**操作**：
```
用户需求："添加代码重构功能"

宪法对齐检查：
/dnaspec.constraint-generator "check-alignment '添加代码重构功能'"

分析：
宪法: "开发者效率第一"
需求: "代码重构"
对齐分析:
  ✅ 重构提高长期效率
  ✅ 符合核心使命
  ✅ 不违反任何原则

对齐分数: 0.95

生成约束：
{
  "refactoring_constraints": {
    "scope": "single_file_only",
    "safety": "must_preserve_behavior",
    "user_control": "require_explicit_approval"
  }
}
```

**版本更新**：T1 - 添加代码重构功能

### 📋 细化阶段：监控功能实现与宪法的一致性

**场景**：功能实现过程中

**操作**：
```
/dnaspec.constraint-generator "monitor-implementation"

当前实现：
- 代码重构功能 ✅ (对齐宪法)
- 性能分析功能 ✅ (对齐宪法)
- 代码分享功能 ⚠️ (偏离风险)

偏离检测：
"代码分享功能可能导致隐私问题，
 违反宪法'尊重开发者意愿'原则"

建议修正：
"如需添加分享功能，必须：
1. 显式获得用户同意
2. 提供匿名化选项
3. 不分享敏感代码"
```

**持续监控**：每个实现点都检查宪法一致性

### 📋 智能阶段：确保智能体行为符合宪法约束

**场景**：智能体执行任务时

**操作**：
```
智能体A: 代码审查智能体

宪法约束：
{
  "agent_constraints": {
    "scope": "code_quality_only",
    "privacy": "never_share_code",
    "transparency": "explain_reasoning"
  }
}

智能体执行：
任务: 审查用户代码
检查: ✅ 只关注质量
检查: ✅ 不分享代码
检查: ✅ 提供解释

结果: 符合宪法约束 ✅
```

**智能体级约束**：
- 行为边界
- 决策依据
- 输出约束

---

## 核心功能

### 1. 宪法创建

**宪法结构**：
```markdown
# 项目宪法 v{version}

## 核心使命
[项目的根本目标]

## 不可妥协原则
[绝对不能违背的原则]

## 技术边界
[技术选型和限制]

## 质量标准
[质量要求]

## 价值观
[项目坚持的价值观]

## 版本历史
- v1.0: {date} - 创始版本
```

**创建流程**：
1. 收集初始核心需求
2. 提取根本原则
3. 定义质量标准
4. 确立价值观
5. 锁定为宪法

### 2. 约束生成

**约束类型**：

**功能约束**
```json
{
  "feature_constraints": {
    "must_have": ["user_auth", "data_encryption"],
    "must_not_have": ["third_party_tracking"],
    "performance_limits": {
      "response_time": "< 2s",
      "throughput": "> 1000 req/s"
    }
  }
}
```

**API约束**
```yaml
api_constraints:
  endpoint_naming: "kebab-case"
  versioning: "url_based"
  error_handling: "standardized_codes"
  authentication: "jwt_required"
```

**数据约束**
```json
{
  "data_constraints": {
    "user_data": {
      "retention": "30_days",
      "encryption": "at_rest_and_transit",
      "anonymization": "required_for_analytics"
    }
  }
}
```

**质量约束**
```json
{
  "quality_constraints": {
    "code_coverage": "> 80%",
    "test_automation": "required",
    "documentation": "complete",
    "review": "peer_review_required"
  }
}
```

### 3. 版本管理

**需求版本化**：
```
v1.0 (T0) - 宪法
  ├─ 核心使命、原则、边界
  └─ 锁定状态

v1.1 (T1) - 添加功能A
  ├─ 继承v1.0
  ├─ 新增：功能A需求
  └─ 约束：功能A对齐宪法

v1.2 (T2) - 添加功能B
  ├─ 继承v1.1
  ├─ 新增：功能B需求
  └─ 约束：功能B对齐宪法

v1.3 (T3) - 功能A细化
  ├─ 继承v1.2
  ├─ 细化：功能A详细需求
  └─ 约束：细化后的功能A仍对齐宪法
```

**快照管理**：
```bash
# 创建快照
dnaspec.constraint-generator "create-snapshot"
→ 保存当前需求状态
→ 版本号自动递增
→ 记录时间戳和变更说明

# 列出版本
dnaspec.constraint-generator "list-versions"
→ 显示所有历史版本
→ 每个版本的变更说明
→ 版本间的差异对比

# 查看特定版本
dnaspec.constraint-generator "show-version v1.2"
→ 显示该版本的需求
→ 显示该版本的约束
→ 显示与宪法的对齐情况
```

### 4. 偏离检测

**检测维度**：

**原则偏离**
```
需求: "添加强制广告"
宪法: "用户体验优先"
检测: ❌ 严重偏离
原因: 广告损害用户体验
建议: 拒绝此需求
```

**边界偏离**
```
需求: "支持所有编程语言"
宪法: "支持主流编程语言"
检测: ⚠️ 部分偏离
原因: 扩大范围可能超出技术边界
建议: 限定在Top 10语言
```

**质量偏离**
```
需求: "响应时间可接受即可"
宪法: "响应时间 < 1秒"
检测: ⚠️ 质量降低
原因: "可接受"模糊，可能降低标准
建议: 明确具体指标
```

### 5. 纠正机制

**纠正流程**：

```
检测到偏离
    ↓
分析偏离程度和原因
    ↓
  轻微偏离 → 建议修正
  中度偏离 → 强烈建议修正
  严重偏离 → 拒绝需求
    ↓
修正后重新检查
    ↓
对齐宪法 → 接受
```

**修正示例**：
```
原需求: "添加用户数据收集功能"

偏离分析:
- 违反宪法: "隐私保护"
- 偏离程度: 严重

修正建议:
1. 只收集必要数据
2. 提供明确的隐私政策
3. 获得用户明确同意
4. 提供数据删除选项

修正后需求:
"添加用户偏好设置功能，
 只收集用户明确授权的最小必要数据"

重新检查: ✅ 对齐宪法
```

---

## 输出格式

### 宪法文档

```markdown
# {项目名称} 宪法 v{version}

## 核心使命
{项目的根本目标}

## 不可妥协原则
1. {原则1}
2. {原则2}
3. {原则3}

## 技术边界
- 技术栈限制
- 功能边界
- 质量标准

## 价值观
- 价值观1
- 价值观2
- 价值观3

## 版本信息
- 创建日期: {date}
- 创建者: {author}
- 修订历史: [{...}]

---
**此宪法是项目的根本大法，所有后续需求必须对齐此宪法。**
```

### 约束规范

```json
{
  "constitution_version": "v1.0",
  "constraints": {
    "functional": {
      "must_implement": [...],
      "must_not_implement": [...]
    },
    "api": {
      "naming_convention": "kebab-case",
      "versioning": "url_based"
    },
    "data": {
      "validation_rules": [...],
      "encryption_requirements": [...]
    },
    "quality": {
      "performance_targets": {...},
      "reliability_targets": {...}
    }
  },
  "alignment_check": {
    "score": 0.95,
    "conflicts": [],
    "recommendations": []
  }
}
```

### 版本历史

```json
{
  "versions": [
    {
      "version": "v1.0",
      "date": "2025-01-01",
      "type": "constitution",
      "description": "创始宪法版本",
      "requirements": [...],
      "constraints": [...]
    },
    {
      "version": "v1.1",
      "date": "2025-01-15",
      "type": "feature_addition",
      "description": "添加代码重构功能",
      "parent": "v1.0",
      "alignment_score": 0.95,
      "new_requirements": [...],
      "new_constraints": [...]
    }
  ]
}
```

---

## 使用示例

### 示例1: 创建宪法

**用户输入**：
```
"我要构建一个AI写作助手"
```

**生成宪法**：
```markdown
# AI写作助手宪法 v1.0

## 核心使命
帮助创作者提高写作效率和质量

## 不可妥协原则
1. 创作者控制权 - AI辅助而非替代
2. 内容原创性 - 确保内容原创
3. 隐私保护 - 保护用户创作内容

## 技术边界
- 支持中文和英文
- 不强制执行建议
- 本地处理，不上传云端

## 质量标准
- 建议相关率 > 90%
- 内容原创性保证
- 响应时间 < 3秒
```

### 示例2: 检查需求对齐

**用户需求**：
```
"添加内容分享功能"
```

**对齐检查**：
```json
{
  "requirement": "添加内容分享功能",
  "constitutional_analysis": {
    "constitution": "AI写作助手宪法 v1.0",
    "principles": {
      "creator_control": "⚠️ 分享可能降低控制权",
      "originality": "✅ 不影响原创性",
      "privacy": "❌ 分享违反隐私保护"
    },
    "alignment_score": 0.4,
    "verdict": "需要修正",
    "suggestions": [
      "添加明确的用户授权机制",
      "只分享摘要，不分享完整内容",
      "提供详细的隐私设置"
    ]
  }
}
```

### 示例3: 版本管理

**操作**：
```bash
# 创建v1.2版本
/dnaspec.constraint-generator "create-snapshot message='添加多语言支持'"

# 检查当前偏离
/dnaspec.constraint-generator "check-drift"
输出:
"当前版本: v1.3
偏离检测: 发现2个轻微偏离
建议: 审查'内容推荐'功能的实现"

# 回滚到v1.2
/dnaspec.constraint-generator "rollback v1.2"
```

---

## 质量检查清单

### 宪法质量检查
- [ ] 核心使命清晰明确
- [ ] 不可妥协原则具体
- [ ] 技术边界合理
- [ ] 质量标准可量化
- [ ] 价值观表述完整

### 约束质量检查
- [ ] 约束对齐宪法
- [ ] 约束具体可执行
- [ ] 约束可验证
- [ ] 约束有明确的执行机制

### 版本管理检查
- [ ] 每个版本有清晰的时间戳
- [ ] 版本间差异明确
- [ ] 对齐分数可追踪
- [ ] 回滚机制可用

### 偏离检测检查
- [ ] 检测维度全面
- [ ] 偏离程度评估准确
- [ ] 纠正建议可行
- [ ] 检测结果可解释

---

## 协作技能

- **dnaspec-architect**: 整体架构协调
- **dnaspec-task-decomposer**: 任务分解符合约束
- **dnaspec-modulizer**: 模块化遵循约束
- **dnaspec-dapi-checker**: API符合约束规范

---

## 关键成就

1. ✅ **宪法需求概念** - 初始需求的根本地位
2. ✅ **时空记忆机制** - 需求版本管理和时间点恢复
3. ✅ **动态约束生成** - 从宪法生成演化约束
4. ✅ **防止偏离机制** - 持续监控和纠正
5. ✅ **全生命周期应用** - Idea→需求→细化→智能
6. ✅ **版本管理** - 完整的需求历史和回滚能力

---

*此技能实现需求的时空记忆机制，确保系统在演进过程中不偏离基本目标，通过宪法需求、版本管理和偏离检测，维持项目的长期一致性和质量。*
