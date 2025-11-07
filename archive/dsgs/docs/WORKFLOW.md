# DSGS 文档驱动开发工作流规范

## 📋 目标
- 强制保障所有开发活动必须参考现有文档
- 确保新功能设计前必须查阅相关文档
- 强制要求设计完成后必须更新对应文档
- 建立文档与代码的同步机制

---

## 🔄 完整工作流程

### 阶段 1: 开发前准备 (Pre-Development)

#### 1.1 任务接收和文档查阅
```bash
# 1. 接收任务时，必须先查阅相关文档
npm run docs:check [task-type]

# 示例：
npm run docs:check constraint-generation
npm run docs:check cognitive-tools
npm run docs:check api-integration
```

**强制检查清单**：
- [ ] 已查阅 [API 接口文档](../docs/API_INTERFACE_DOCUMENTATION.md)
- [ ] 已查阅 [函数调用字典](../docs/FUNCTION_CALL_DICTIONARY.md)
- [ ] 已查阅 [模块依赖关系](../docs/MODULE_DEPENDENCY_GRAPH.md)
- [ ] 已查阅 [类型定义参考](../docs/TYPE_DEFINITIONS_REFERENCE.md)
- [ ] 已确认相关模块的职责边界

#### 1.2 文档合规性检查
```bash
# 运行文档合规性检查
npm run docs:compliance [feature-name]

# 如果检查失败，禁止继续开发
```

**检查内容**：
- 是否了解现有 API 接口
- 是否清楚模块依赖关系
- 是否知道类型定义规范
- 是否理解设计模式约束

### 阶段 2: 设计阶段 (Design Phase)

#### 2.1 设计文档编写
```bash
# 创建设计文档
npm run docs:design [feature-name]

# 生成设计文档模板
npm run docs:template design
```

**设计文档必须包含**：
- [ ] 功能概述和目标
- [ ] API 接口设计 (包括类型定义)
- [ ] 模块依赖关系分析
- [ ] 与现有模块的集成方案
- [ ] 测试策略
- [ ] 文档更新计划

#### 2.2 设计评审
```bash
# 提交设计评审
npm run docs:review [design-doc-path]

# 评审通过后才能开始开发
```

**评审标准**：
- [ ] 设计符合现有架构规范
- [ ] API 接口与现有系统保持一致
- [ ] 依赖关系合理，无循环依赖
- [ ] 类型定义完整且规范
- [ ] 文档更新计划明确

### 阶段 3: 开发阶段 (Development Phase)

#### 3.1 开发环境检查
```bash
# 检查开发环境配置
npm run docs:env-check

# 确保文档工具可用
```

#### 3.2 实时文档同步
```bash
# 开发过程中，每次修改 API 时
npm run docs:update [api-name]

# 每次添加新类型时
npm run docs:type [type-name]

# 每次修改模块依赖时
npm run docs:dependency [module-name]
```

#### 3.3 文档完整性检查
```bash
# 提交代码前自动检查
npm run docs:verify

# 如果文档不完整，提交失败
```

### 阶段 4: 代码审查 (Code Review)

#### 4.1 文档同步检查
```bash
# 代码审查时自动检查文档同步
npm run docs:sync-check [pr-number]

# 文档不同步的 PR 会被拒绝
```

**检查内容**：
- [ ] 新增的 API 是否有对应的文档
- [ ] 修改的接口是否更新了文档
- [ ] 新增的类型是否已添加到类型字典
- [ ] 依赖关系变更是否已更新依赖图

#### 4.2 文档质量检查
```bash
# 检查文档质量
npm run docs:quality [doc-path]

# 文档质量不达标时，PR 被拒绝
```

### 阶段 5: 测试和部署 (Testing & Deployment)

#### 5.1 测试文档检查
```bash
# 运行测试时检查测试文档
npm run docs:test-check

# 确保测试用例有对应的文档说明
```

#### 5.2 部署前最终检查
```bash
# 部署前最终文档检查
npm run docs:pre-deploy

# 文档检查通过后才能部署
```

---

## 🛠️ 工具和脚本实现

### 1. 文档检查脚本
```bash
# scripts/docs-check.sh
#!/bin/bash

# docs:check 命令实现
TASK_TYPE=$1

echo "🔍 检查文档合规性..."
echo "📋 任务类型: $TASK_TYPE"

# 检查相关文档是否存在
case $TASK_TYPE in
  "constraint-generation")
    REQUIRED_DOCS=("API_INTERFACE_DOCUMENTATION.md" "FUNCTION_CALL_DICTIONARY.md")
    ;;
  "cognitive-tools")
    REQUIRED_DOCS=("API_INTERFACE_DOCUMENTATION.md" "TYPE_DEFINITIONS_REFERENCE.md")
    ;;
  "api-integration")
    REQUIRED_DOCS=("API_INTERFACE_DOCUMENTATION.md" "MODULE_DEPENDENCY_GRAPH.md")
    ;;
  *)
    REQUIRED_DOCS=("API_INTERFACE_DOCUMENTATION.md" "FUNCTION_CALL_DICTIONARY.md" "MODULE_DEPENDENCY_GRAPH.md" "TYPE_DEFINITIONS_REFERENCE.md")
    ;;
esac

# 检查文档是否存在
for doc in "${REQUIRED_DOCS[@]}"; do
  if [ ! -f "docs/$doc" ]; then
    echo "❌ 缺少必需文档: $doc"
    exit 1
  fi
done

echo "✅ 文档检查通过"
```

### 2. 文档更新脚本
```bash
# scripts/docs-update.sh
#!/bin/bash

# docs:update 命令实现
API_NAME=$1

echo "📝 更新 API 文档..."
echo "🔧 API 名称: $API_NAME"

# 检查是否需要更新文档
if grep -q "$API_NAME" docs/API_INTERFACE_DOCUMENTATION.md; then
  echo "📋 API 已存在于文档中，请确认是否需要更新"
  read -p "是否继续更新? (y/n): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 打开文档进行编辑
    ${EDITOR:-vim} docs/API_INTERFACE_DOCUMENTATION.md
    echo "✅ 文档已更新，请提交更改"
  else
    echo "🚫 取消文档更新"
  fi
else
  echo "📋 API 不存在于文档中，请添加"
  ${EDITOR:-vim} docs/API_INTERFACE_DOCUMENTATION.md
  echo "✅ 文档已添加，请提交更改"
fi
```

### 3. Git Hooks 配置
```bash
# .githooks/pre-commit
#!/bin/bash

echo "🔍 检查文档同步..."

# 检查是否有代码变更但没有文档变更
CODE_CHANGED=$(git diff --cached --name-only | grep -E "\.(ts|tsx|js|jsx)$" | wc -l)
DOCS_CHANGED=$(git diff --cached --name-only | grep "docs/" | wc -l)

if [ "$CODE_CHANGED" -gt 0 ] && [ "$DOCS_CHANGED" -eq 0 ]; then
  echo "❌ 检测到代码变更但没有文档变更"
  echo "📝 请运行 'npm run docs:update' 更新相关文档"
  exit 1
fi

echo "✅ 文档同步检查通过"
```

### 4. GitHub Actions 工作流
```yaml
# .github/workflows/docs-compliance.yml
name: Documentation Compliance Check

on:
  pull_request:
    types: [opened, synchronize, reopened]
  push:
    branches: [main, develop]

jobs:
  docs-compliance:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Check documentation compliance
        run: npm run docs:verify
        
      - name: Check API documentation
        run: npm run docs:api-check
        
      - name: Check type definitions
        run: npm run docs:type-check
        
      - name: Generate compliance report
        run: npm run docs:report
```

---

## 📋 强制执行机制

### 1. 开发流程强制检查

#### 提交前检查清单
```bash
# scripts/pre-commit-check.sh
#!/bin/bash

echo "🔍 执行提交前检查..."

# 1. 检查文档是否同步
npm run docs:sync-check
if [ $? -ne 0 ]; then
  echo "❌ 文档同步检查失败"
  exit 1
fi

# 2. 检查类型定义是否完整
npm run docs:type-verify
if [ $? -ne 0 ]; then
  echo "❌ 类型定义检查失败"
  exit 1
fi

# 3. 检查 API 文档是否更新
npm run docs:api-verify
if [ $? -ne 0 ]; then
  echo "❌ API 文档检查失败"
  exit 1
fi

echo "✅ 所有检查通过"
```

#### PR 模板
```markdown
## PR 文档合规性检查

### 📋 文档更新清单
- [ ] 我已查阅相关的 [API 接口文档](../docs/API_INTERFACE_DOCUMENTATION.md)
- [ ] 我已查阅相关的 [函数调用字典](../docs/FUNCTION_CALL_DICTIONARY.md)
- [ ] 我已查阅相关的 [模块依赖关系](../docs/MODULE_DEPENDENCY_GRAPH.md)
- [ ] 我已查阅相关的 [类型定义参考](../docs/TYPE_DEFINITIONS_REFERENCE.md)
- [ ] 我已更新所有相关的 API 文档
- [ ] 我已更新所有相关的类型定义
- [ ] 我已更新所有相关的模块依赖关系

### 📝 文档更新详情
请详细说明您更新了哪些文档：

1. **API 接口文档**: 更新了哪些接口，添加了哪些新接口
2. **函数调用字典**: 添加了哪些新函数，修改了哪些现有函数
3. **类型定义参考**: 添加了哪些新类型，修改了哪些现有类型
4. **模块依赖关系**: 依赖关系有哪些变化

### 🔗 相关文档链接
- [API 接口文档](../docs/API_INTERFACE_DOCUMENTATION.md)
- [函数调用字典](../docs/FUNCTION_CALL_DICTIONARY.md)
- [模块依赖关系](../docs/MODULE_DEPENDENCY_GRAPH.md)
- [类型定义参考](../docs/TYPE_DEFINITIONS_REFERENCE.md)
```

### 2. CI/CD 强制执行

#### 构建失败条件
```yaml
# 在 CI/CD 中强制执行文档检查
- 如果文档检查失败，构建失败
- 如果类型定义不完整，构建失败
- 如果 API 文档不同步，构建失败
- 如果依赖关系图不更新，构建失败
```

#### 部署检查清单
```bash
# scripts/pre-deploy-check.sh
#!/bin/bash

echo "🚀 执行部署前检查..."

# 1. 检查所有文档是否最新
npm run docs:latest-check
if [ $? -ne 0 ]; then
  echo "❌ 文档不是最新版本"
  exit 1
fi

# 2. 检查文档质量
npm run docs:quality-check
if [ $? -ne 0 ]; then
  echo "❌ 文档质量检查失败"
  exit 1
fi

# 3. 检查文档完整性
npm run docs:completeness-check
if [ $? -ne 0 ]; then
  echo "❌ 文档完整性检查失败"
  exit 1
fi

echo "✅ 部署前检查通过"
```

---

## 📊 监控和报告

### 1. 文档合规性监控
```bash
# scripts/docs-monitor.sh
#!/bin/bash

echo "📊 生成文档合规性报告..."

# 检查文档更新频率
echo "📅 文档更新频率:"
git log --oneline --since="1 month ago" -- docs/ | wc -l

# 检查文档覆盖率
echo "📈 文档覆盖率:"
find src/ -name "*.ts" -exec grep -l "@deprecated" {} \; | wc -l
find docs/ -name "*.md" -exec grep -l "deprecated" {} \; | wc -l

# 检查文档同步率
echo "🔄 文档同步率:"
npm run docs:sync-rate

# 生成报告
npm run docs:report
```

### 2. 定期报告
```markdown
## 文档合规性周报

### 📊 基本指标
- **文档更新次数**: 15
- **API 同步率**: 95%
- **类型定义完整度**: 98%
- **依赖关系图更新率**: 100%

### 📋 合规性检查结果
- **通过检查**: 45
- **失败检查**: 2
- **修复率**: 100%

### 🎯 改进建议
1. 加强新功能设计前的文档查阅培训
2. 完善自动化检查工具
3. 建立文档质量评估体系
```

---

## 🎯 培训和文化建设

### 1. 新人培训
```markdown
## DSGS 文档驱动开发培训

### 📚 必读文档
1. [API 接口文档](docs/API_INTERFACE_DOCUMENTATION.md)
2. [函数调用字典](docs/FUNCTION_CALL_DICTIONARY.md)
3. [模块依赖关系](docs/MODULE_DEPENDENCY_GRAPH.md)
4. [类型定义参考](docs/TYPE_DEFINITIONS_REFERENCE.md)
5. [文档驱动开发工作流](docs/WORKFLOW.md)

### 🛠️ 工具使用培训
1. 文档检查工具使用
2. 文档更新工具使用
3. 合规性检查工具使用

### 📝 实践练习
1. 模拟新功能开发流程
2. 文档更新练习
3. 代码审查练习
```

### 2. 团队文化建设
```markdown
## 文档优先文化

### 🎯 核心价值观
- **文档先于代码**: 设计阶段必须先编写文档
- **文档与代码同步**: 代码变更必须同步更新文档
- **文档质量即代码质量**: 文档质量与代码质量同等重要

### 🏆 激励机制
- **文档之星**: 每月评选文档贡献最大的开发者
- **合规性奖励**: 连续 3 个月文档合规率达到 100% 的团队奖励
- **创新奖**: 提出文档改进建议并被采纳的奖励

### 📈 持续改进
- **定期回顾**: 每月回顾文档工作流程的有效性
- **工具升级**: 持续改进文档工具和自动化程度
- **最佳实践**: 总结和推广文档最佳实践
```

---

## 🔄 持续改进

### 1. 定期评估
```bash
# 每月评估文档工作流程
npm run docs:workflow-eval

# 每季度评估文档质量
npm run docs:quality-eval

# 每年评估文档体系
npm run docs:system-eval
```

### 2. 反馈收集
```markdown
## 文档工作流程反馈

### 📝 反馈渠道
1. **GitHub Issues**: 提交文档相关问题
2. **团队会议**: 在团队会议上讨论文档问题
3. **匿名反馈**: 通过匿名表单收集反馈

### 🎯 改进重点
1. **工具易用性**: 改进文档工具的用户体验
2. **流程效率**: 优化文档工作流程的效率
3. **培训效果**: 提高文档培训的效果
```

---

## 📋 实施计划

### 第一阶段 (1-2 周)
- [ ] 建立文档检查脚本
- [ ] 配置 Git Hooks
- [ ] 创建 GitHub Actions 工作流
- [ ] 制定 PR 模板

### 第二阶段 (3-4 周)
- [ ] 开发监控工具
- [ ] 建立报告机制
- [ ] 开展团队培训
- [ ] 建立激励机制

### 第三阶段 (5-8 周)
- [ ] 完善自动化工具
- [ ] 建立持续改进机制
- [ ] 优化工作流程
- [ ] 推广最佳实践

---

## 🎯 成功指标

### 1. 量化指标
- **文档同步率**: > 95%
- **API 文档覆盖率**: > 98%
- **类型定义完整度**: > 99%
- **依赖关系图准确性**: > 95%
- **开发效率提升**: > 20%

### 2. 质量指标
- **文档准确性**: > 95%
- **文档完整性**: > 98%
- **文档可用性**: > 90%
- **团队满意度**: > 85%

### 3. 流程指标
- **合规检查通过率**: > 95%
- **文档更新及时性**: < 24小时
- **问题修复时间**: < 48小时
- **培训完成率**: 100%

---

**文档版本**: v1.0  
**实施日期**: 2025-08-11  
**负责人**: 开发团队  
**下次评估**: 2025-09-11