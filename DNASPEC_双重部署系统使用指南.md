# DNASPEC 双重部署系统使用指南

## 系统概述

DNASPEC 技能系统现在支持**双重部署模式**，可以同时作为标准化技能和自定义 slash 命令使用，为您提供最大的灵活性和兼容性。

### 🎯 核心特性

- ✅ **标准化兼容**: 符合 agentskills.io 标准，支持 Claude Code 自动发现
- ✅ **CLI 命令支持**: 支持 slash 命令方式调用所有技能
- ✅ **动态参数**: 每个技能都有专门的命令行参数配置
- ✅ **自动映射**: 自动从 SKILL.md 生成命令映射
- ✅ **统一管理**: 同一套技能系统支持两种调用方式

## 部署模式

### 1. 标准化部署 (Claude Code 兼容)

#### 适用场景
- Claude Code IDE 用户
- 喜欢标准化工作流程的用户
- 需要与团队共享技能的用户

#### 部署步骤
```bash
# 1. 创建 Claude Code 技能目录
mkdir -p .claude/skills

# 2. 复制技能文件
cp -r skills/* .claude/skills/

# 3. 验证部署
ls .claude/skills/
# 应该看到所有技能目录和 SKILL.md 文件
```

#### 使用方式
在 Claude Code 中直接使用：
```
我需要分析这段代码的质量
[Claude Code 会自动选择 context-analyzer 技能]
```

```
设计一个电商系统的架构
[Claude Code 会自动选择 architect 技能]
```

### 2. CLI 命令部署 (Slash 命令)

#### 适用场景
- 命令行重度用户
- 需要批量处理的用户
- 自动化脚本集成

#### 部署步骤
```bash
# 1. 确保 DNASPEC CLI 可用
python cli_direct.py help

# 2. 使用 slash 命令模式
dnaspec slash <skill-name> --help
```

#### 使用方式
```bash
# 列出所有可用技能
dnaspec slash list

# 查看技能详细信息
dnaspec slash info agent-creator

# 使用技能命令
dnaspec slash context-analyzer --input "要分析的文本" --dimensions clarity relevance

dnaspec slash agent-creator --agent-description "数据分析专家" --capabilities python sql

dnaspec slash architect --requirements "设计一个博客系统" --architecture-type layered
```

## 技能列表

### 可用技能 (13个)

| 技能名称 | 分类 | 描述 | 主要用途 |
|---------|------|------|----------|
| `agent-creator` | 架构 | 创建智能体代理 | AI 代理设计和创建 |
| `architect` | 架构 | 系统架构设计 | 架构规划和技术规范 |
| `cache-manager` | 架构 | 文件管理 | AI 生成文件的管理和验证 |
| `cognitive-templater` | 模板 | 认知模板应用 | 思维模式和应用 |
| `constraint-generator` | 生成 | 约束生成 | 系统约束和验证规则 |
| `context-analyzer` | 分析 | 上下文分析 | 5 维度质量分析 |
| `context-optimizer` | 优化 | 上下文优化 | 上下文优化和提升 |
| `dapi-checker` | 检查 | API 检查 | API 设计和规范验证 |
| `git-operations` | 管理 | Git 操作 | 版本控制和协作 |
| `modulizer` | 模块化 | 模块化设计 | 系统模块化设计 |
| `simple-architect` | 架构 | 简单架构设计 | 基础架构设计 |
| `system-architect` | 架构 | 系统架构师 | 复杂系统架构 |
| `task-decomposer` | 分解 | 任务分解 | 复杂任务分解 |

### 分类统计

- **架构类**: 7 个技能 (agent-creator, architect, cache-manager, simple-architect, system-architect 等)
- **分析类**: 1 个技能 (context-analyzer)
- **优化类**: 1 个技能 (context-optimizer)
- **生成类**: 1 个技能 (constraint-generator)
- **管理类**: 1 个技能 (git-operations)
- **模块化**: 1 个技能 (modulizer)
- **分解类**: 1 个技能 (task-decomposer)

## 命令语法详解

### 基本语法
```bash
dnaspec slash <skill-name> [选项]
```

### 通用选项
```bash
--input, -i          # 输入内容
--output, -o         # 输出文件路径
--format, -f         # 输出格式 (json/yaml/text)
--detail-level       # 详细程度 (basic/standard/detailed)
--context, -c        # 上下文信息 (JSON 格式)
```

### 技能特定参数

#### agent-creator (智能体创建器)
```bash
dnaspec slash agent-creator \
  --agent-description "描述" \
  --capabilities python sql visualization \
  --domain "专业领域" \
  --personality "人格类型" \
  --agent-type "代理类型"
```
- `personality`: professional_precise, friendly_supportive, analytical_critical, creative_innovative, direct_efficient
- `agent-type`: domain_expert, task_specialist, role_assistant

#### context-analyzer (上下文分析器)
```bash
dnaspec slash context-analyzer \
  --input "要分析的文本" \
  --dimensions clarity relevance completeness \
  --benchmark "质量基准"
```
- `dimensions`: clarity, relevance, completeness, consistency, efficiency
- `benchmark`: academic, business, technical

#### architect (架构师)
```bash
dnaspec slash architect \
  --requirements "系统需求" \
  --architecture-type "架构类型" \
  --tech-stack "技术栈"
```
- `architecture-type`: microservice, layered, event_driven, domain_driven

#### task-decomposer (任务分解器)
```bash
dnaspec slash task-decomposer \
  --input "复杂任务" \
  --max-depth 3 \
  --isolation-level "medium"
```
- `isolation-level`: low, medium, high

#### constraint-generator (约束生成器)
```bash
dnaspec slash constraint-generator \
  --requirements "系统需求" \
  --change-request "变更请求" \
  --constraint-type "约束类型"
```
- `constraint-type`: security, performance, architecture, quality

## 实用工具命令

### 列出技能
```bash
# 列出所有技能
dnaspec slash list

# 按分类列出
dnaspec slash list --category architecture

# JSON 格式输出
dnaspec slash list --format json
```

### 查看技能信息
```bash
# 查看技能详细信息
dnaspec slash info agent-creator

# 查看技能验证状态
dnaspec slash validate agent-creator

# 验证所有技能
dnaspec slash validate
```

### 搜索技能
```bash
# 按关键词搜索
dnaspec slash search "分析"

# 限制搜索分类
dnaspec slash search "架构" --category architecture
```

### 生成文档
```bash
# 生成使用文档
dnaspec slash docs --output skills_guide.md

# HTML 格式文档
dnaspec slash docs --format html --output skills_guide.html
```

### 部署技能
```bash
# 部署所有技能
dnaspec slash deploy --mode both

# 只部署标准化格式
dnaspec slash deploy --mode standard

# 只部署 CLI 格式
dnaspec slash deploy --mode cli
```

## 输出格式

### JSON 格式 (默认)
```json
{
  "success": true,
  "skill": "context-analyzer",
  "result": {
    "analysis": "...",
    "score": 0.85
  },
  "metadata": {
    "format": "json",
    "detail_level": "standard"
  }
}
```

### YAML 格式
```yaml
success: true
skill: context-analyzer
result:
  analysis: "..."
  score: 0.85
metadata:
  format: yaml
  detail_level: standard
```

### 文本格式
```
技能 context-analyzer 执行完成
分析得分: 0.85/1.0
主要发现:
- 清晰度: 良好
- 完整性: 优秀
```

## 实际使用示例

### 示例 1: 代码质量分析
```bash
# 分析代码质量
dnaspec slash context-analyzer \
  --input "function calculate() { return x + y; }" \
  --dimensions clarity relevance \
  --format json \
  --output analysis_result.json
```

### 示例 2: 创建 AI 代理
```bash
# 创建数据分析专家代理
dnaspec slash agent-creator \
  --agent-description "专业的数据分析师" \
  --capabilities python sql pandas matplotlib seaborn \
  --domain "data_analysis" \
  --personality analytical_critical \
  --agent-type domain_expert
```

### 示例 3: 系统架构设计
```bash
# 设计微服务架构
dnaspec slash architect \
  --requirements "设计一个在线教育平台" \
  --architecture-type microservice \
  --tech-stack nodejs react mongodb redis \
  --detail-level detailed
```

### 示例 4: 任务分解
```bash
# 分解复杂任务
dnaspec slash task-decomposer \
  --input "开发一个完整的电商网站" \
  --max-depth 3 \
  --isolation-level high
```

## 错误处理

### 常见错误和解决方案

#### 1. 技能不存在
```bash
Error: Unknown command: unknown-skill
Available commands: [agent-creator, architect, context-analyzer, ...]
```
**解决方案**: 使用 `dnaspec slash list` 查看可用技能

#### 2. 参数错误
```bash
Error: Invalid argument value
```
**解决方案**: 使用 `--help` 查看参数要求

#### 3. 输入格式错误
```bash
Error: Invalid JSON format in context parameter
```
**解决方案**: 检查 JSON 格式是否正确

#### 4. 文件权限错误
```bash
Error: Cannot write to output file
```
**解决方案**: 检查文件路径和权限

## 高级用法

### 批量处理
```bash
# 创建批量处理脚本
#!/bin/bash
for file in *.txt; do
  echo "分析文件: $file"
  dnaspec slash context-analyzer --input "$(cat $file)" --output "${file%.txt}_analysis.json"
done
```

### 管道处理
```bash
# 分析代码文件并生成报告
find . -name "*.py" | \
  xargs -I {} dnaspec slash context-analyzer --input "$(cat {})" --format json | \
  jq '.result.score' | \
  awk '{sum+=$1; count++} END {print "平均质量得分:", sum/count}'
```

### 脚本集成
```bash
#!/bin/bash
# 在 CI/CD 中使用 DNASPEC 技能

# 1. 分析代码质量
QUALITY_SCORE=$(dnaspec slash context-analyzer --input "$(cat code.txt)" --format json | jq '.result.score')

# 2. 根据质量分数决定下一步
if (( $(echo "$QUALITY_SCORE > 0.8" | bc -l) )); then
    echo "代码质量良好，继续部署"
    dnaspec slash architect --requirements "部署到生产环境"
else
    echo "代码质量需要改进"
    exit 1
fi
```

## 故障排除

### 调试模式
```bash
# 启用详细输出
dnaspec slash <skill> --input "..." --detail-level detailed

# 查看技能验证信息
dnaspec slash validate --help
```

### 验证安装
```bash
# 运行完整测试
python test_dual_deployment.py

# 检查 CLI 状态
python cli_direct.py validate

# 查看技能列表
dnaspec slash list --format json
```

### 日志和调试
```bash
# 设置环境变量启用调试
export DNASPEC_DEBUG=1
dnaspec slash agent-creator --agent-description "测试代理"

# 查看详细错误信息
dnaspec slash validate --output validation_log.json
```

## 最佳实践

### 1. 技能选择
- 根据具体需求选择合适的技能
- 使用 `info` 命令了解技能详细功能
- 参考示例学习参数使用方法

### 2. 参数设置
- 使用 `--detail-level detailed` 获得更多细节
- 合理设置输出格式 (JSON 适合程序处理，文本适合人工阅读)
- 必要时使用 `--output` 保存结果

### 3. 批量操作
- 对大量数据使用脚本批量处理
- 利用 JSON 格式进行自动化分析
- 结合其他命令行工具进行管道处理

### 4. 团队协作
- 标准化部署模式便于团队共享
- 使用文档生成功能创建团队指南
- 定期验证技能配置的正确性

## 扩展和定制

### 添加新技能
1. 创建技能目录结构
2. 编写 SKILL.md 文件
3. 在 `skill_command_mapper.py` 中注册

### 自定义参数
- 在 `slash_command_handler.py` 中添加技能特定参数
- 更新参数验证逻辑
- 添加相应的处理代码

### 集成其他工具
- 与现有 CI/CD 工具集成
- 创建 IDE 插件
- 开发 Web 界面

## 更新和维护

### 更新技能
```bash
# 重新部署所有技能
dnaspec slash deploy --mode both

# 更新特定技能
cp -r skills/new-skill .claude/skills/
```

### 维护任务
- 定期运行验证测试
- 更新文档和示例
- 监控技能使用情况
- 收集用户反馈

---

## 总结

DNASPEC 双重部署系统为您提供了：

- 🎯 **双重兼容性**: 标准化 + CLI 命令
- 🔧 **灵活调用**: 适应不同工作流程
- 📦 **即开即用**: 13 个技能立即可用
- 🚀 **易于扩展**: 支持自定义和扩展
- 📖 **完整文档**: 详细的使用指南和示例

无论您是 Claude Code 用户还是命令行爱好者，DNASPEC 都能为您提供强大的技能支持！

---

**版本**: 2.0.0  
**最后更新**: 2025-12-21  
**支持平台**: Claude Code CLI, 标准命令行