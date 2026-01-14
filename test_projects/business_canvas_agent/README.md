# 商业画布分析智能体

一个使用 DNASPEC 命令开发的 AI 智能体，能够分析商业模式画布（Business Model Canvas），提供战略建议和优化方案。

## 🎯 项目特色

✨ **使用 DNASPEC 命令开发** - 展示了如何使用 `/dnaspec` 系列命令完成完整项目

🤖 **智能分析引擎** - 完整性检查、一致性验证、AI 深度分析

💡 **战略建议生成** - 基于分析结果提供可操作的优化建议

📊 **可视化报告** - 导出 Markdown 和 JSON 格式的详细报告

## 📁 项目结构

```
business_canvas_agent/
├── src/
│   └── business_canvas_agent.py  # 核心智能体代码
├── config/
│   └── agent_config.yaml         # 智能体配置
├── tests/
│   └── test_agent.py             # 测试文件
├── docs/
│   └── API.md                    # API 文档
├── demo.py                       # 使用示例
├── PROJECT.md                    # 项目文档（DNASPEC命令使用记录）
└── README.md                     # 本文件
```

## 🚀 快速开始

### 1. 运行示例

```bash
cd test_projects/business_canvas_agent
python demo.py
```

### 2. 基本使用

```python
from src.business_canvas_agent import analyze_canvas

# 定义你的商业画布
canvas_data = {
    'value_propositions': '为中小企业提供一键式财务自动化解决方案',
    'customer_segments': '中小企业（50-500人）',
    'channels': '在线营销、合作伙伴',
    'customer_relationships': '自助服务 + 专属客户经理',
    'revenue_streams': 'SaaS订阅费、实施服务费',
    'key_resources': '技术团队、云计算平台',
    'key_activities': '产品开发、客户支持',
    'cost_structure': '研发成本、服务器成本',
    'key_partners': '云服务商'  # 可选
}

# 分析画布
result = analyze_canvas(canvas_data)

# 查看结果
print(f"综合得分: {result.overall_score}/100")
print(f"完整性: {result.completeness_score}/100")
print(f"一致性: {result.consistency_score}/100")
```

### 3. 导出报告

```python
from src.business_canvas_agent import BusinessCanvasAgent

agent = BusinessCanvasAgent()
result = agent.analyze_canvas(canvas_data)

# 导出 Markdown 报告
markdown_report = agent.export_report(result, format='markdown')
with open('report.md', 'w') as f:
    f.write(markdown_report)

# 导出 JSON 报告
json_report = agent.export_report(result, format='json')
with open('report.json', 'w') as f:
    f.write(json_report)
```

## 📋 商业画布的9个模块

| 模块 | 描述 | 必填 |
|------|------|------|
| **价值主张** (Value Propositions) | 为客户创造价值的产品或服务 | ✅ |
| **客户细分** (Customer Segments) | 企业想要接触和服务的目标人群 | ✅ |
| **渠道通路** (Channels) | 如何将产品或服务传递给客户 | ✅ |
| **客户关系** (Customer Relationships) | 与客户建立的关系类型 | ✅ |
| **收入来源** (Revenue Streams) | 企业从每个客户群体获得的收入 | ✅ |
| **核心资源** (Key Resources) | 商业模式运行所需的最重要资产 | ✅ |
| **关键业务** (Key Activities) | 企业必须做的最重要的事情 | ✅ |
| **重要合作** (Key Partners) | 让商业模式运行的供应商和网络 | ⚠️ |
| **成本结构** (Cost Structure) | 运营商业模式发生的所有成本 | ✅ |

## 🎨 使用 DNASPEC 命令开发

本项目完整展示了如何使用 DNASPEC 的 iflow 命令来开发一个完整的 AI 智能体项目。

### 第一步：架构设计

使用 `/dnaspec.architect` 设计系统架构：

```
/dnaspec.architect 设计一个商业画布分析智能体系统，包括：
1. 数据输入模块（9个商业画布模块）
2. AI 分析引擎（评估完整性和一致性）
3. 建议生成模块（战略优化建议）
4. 可视化报告模块
```

**输出**: 详细的系统架构图和技术栈选择

### 第二步：任务分解

使用 `/dnaspec.task-decomposer` 分解开发任务：

```
/dnaspec.task-decomposer 将"商业画布分析智能体"项目分解为具体的开发任务，按照优先级排序
```

**输出**: 15个阶段的详细任务清单，从基础设施到部署

### 第三步：约束生成

使用 `/dnaspec.constraint-generator` 生成约束条件：

```
/dnaspec.constraint-generator 为商业画布分析智能体生成业务规则、数据验证和AI安全约束
```

**输出**:
- 业务规则约束（完整性要求、一致性规则、评分标准）
- 数据验证约束（输入验证、安全验证）
- AI 安全约束（Prompt 注入防护、输出验证、使用量控制）

### 第四步：智能体创建

使用 `/dnaspec.agent-creator` 创建智能体：

```
/dnaspec.agent-creator 创建一个商业画布分析智能代理，包含：
1. 自动分析工作流
2. 质量检查逻辑
3. 建议生成策略
4. 学习反馈机制
```

**输出**: 完整的智能体架构设计和配置

## 🔍 分析能力

### 1. 完整性检查

- ✅ 验证所有必填模块是否填写
- ✅ 检查内容长度是否足够
- ✅ 识别缺失信息
- ✅ 生成完整性评分（0-100）

### 2. 一致性验证

- ✅ 价值主张与客户细分匹配度
- ✅ 渠道与客户匹配度
- ✅ 收入与成本结构一致性
- ✅ 商业模式可行性评估

### 3. AI 深度分析

- ✅ 核心优势识别
- ✅ 潜在风险分析
- ✅ 战略建议生成
- ✅ 创新机会发现

### 4. 建议生成

- ✅ 基于完整性的改进建议
- ✅ 基于一致性的优化建议
- ✅ 战略层面的建议
- ✅ 优先级排序

## 📊 输出报告

分析结果包含：

- 📈 评分总览（完整性、一致性、综合得分）
- 🔍 详细的问题列表（按严重程度）
- 💡 优化建议（按优先级排序）
- 🎯 战略洞察
- 📝 可执行的行动项

## 🧪 测试

```bash
# 运行所有示例
python demo.py

# 运行单元测试（待实现）
python -m pytest tests/
```

## 🎯 应用场景

1. **创业者** - 验证和优化商业计划
2. **产品经理** - 分析商业模式可行性
3. **投资人** - 评估创业项目
4. **顾问** - 为客户提供战略建议
5. **教育** - 商业模式教学工具

## 🚧 未来改进

- [ ] 集成真实的 LLM API（OpenAI/Claude）
- [ ] 添加可视化图表生成
- [ ] 实现多语言支持
- [ ] 添加案例库和模板
- [ ] 开发 Web 界面
- [ ] 支持团队协作
- [ ] 添加历史记录和版本管理

## 📖 相关文档

- `PROJECT.md` - 详细的项目文档和 DNASPEC 命令使用记录
- `demo.py` - 完整的使用示例
- `src/business_canvas_agent.py` - 源代码（含详细注释）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可

MIT License

## 🙏 致谢

本项目使用 DNASPEC 框架开发，展示了 AI 辅助软件开发的最佳实践。

---

**Made with DNASPEC** 🧬
