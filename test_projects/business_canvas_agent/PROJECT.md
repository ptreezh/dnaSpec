# 商业画布分析智能体项目

## 项目概述

创建一个 AI 智能体，能够分析商业模式画布（Business Model Canvas），提供战略建议和优化方案。

**项目目标**：
- 输入商业画布的9个模块信息
- AI 分析各个模块的完整性和一致性
- 提供优化建议和战略洞察
- 生成可视化报告

## 使用 DNASPEC 命令开发

本文档展示如何使用 DNASPEC 的 iflow 命令来完成这个项目。

---

## 第一步：系统架构设计

**命令**：
```
/dnaspec.architect 设计一个商业画布分析智能体系统，包括：
1. 数据输入模块（9个商业画布模块）
2. AI 分析引擎（评估完整性和一致性）
3. 建议生成模块（战略优化建议）
4. 可视化报告模块
5. 技术栈：Python + LLM API + React 前端
```

**生成的架构**：

### 系统架构图

```
┌─────────────────────────────────────────────────────────┐
│                  前端界面层 (React)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │输入表单  │  │分析报告  │  │可视化图表 │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
                         ↕ REST API
┌─────────────────────────────────────────────────────────┐
│                后端服务层 (FastAPI)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │API 网关  │  │任务队列  │  │结果缓存  │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│                 业务逻辑层 (Python)                      │
│  ┌──────────────────┐  ┌──────────────────┐           │
│  │ 画布分析引擎     │  │ 建议生成器       │           │
│  │ - 完整性检查     │  │ - 战略洞察       │           │
│  │ - 一致性验证     │  │ - 优化方案       │           │
│  └──────────────────┘  └──────────────────┘           │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│                  AI 分析层 (LLM)                         │
│  ┌──────────────────┐  ┌──────────────────┐           │
│  │ OpenAI GPT-4     │  │ Claude 3.5       │           │
│  │ - 结构化分析     │  │ - 战略建议       │           │
│  └──────────────────┘  └──────────────────┘           │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│                  数据持久层                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ PostgreSQL│  │ Redis    │  │ S3存储   │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
```

### 技术栈

**后端**：
- FastAPI (Web 框架)
- Celery (异步任务)
- SQLAlchemy (ORM)
- OpenAI API (AI 分析)
- LangChain (LLM 编排)

**前端**：
- React + TypeScript
- Material-UI
- Recharts (图表)
- Axios (HTTP 客户端)

**数据存储**：
- PostgreSQL (关系数据)
- Redis (缓存和队列)
- AWS S3 (文件存储)

### 模块划分

1. **canvas_analyzer** - 核心分析引擎
2. **recommendation_engine** - 建议生成器
3. **api_server** - FastAPI 服务
4. **web_ui** - React 前端
5. **data_models** - 数据模型定义

---

## 第二步：任务分解

**命令**：
```
/dnaspec.task-decomposer 将"商业画布分析智能体"项目分解为具体的开发任务，按照优先级排序
```

**生成的任务清单**：

### 阶段 1: 基础设施搭建 (优先级: P0)

1. **项目初始化**
   - [ ] 创建项目仓库
   - [ ] 设置虚拟环境
   - [ ] 配置依赖管理
   - [ ] 设置代码规范 (black, pylint, mypy)

2. **数据模型设计**
   - [ ] 定义商业画布9模块的数据结构
   - [ ] 设计数据库 schema
   - [ ] 创建 SQLAlchemy models
   - [ ] 编写数据迁移脚本

3. **基础 API 框架**
   - [ ] 搭建 FastAPI 项目结构
   - [ ] 实现健康检查端点
   - [ ] 配置 CORS 和中间件
   - [ ] 设置日志系统

### 阶段 2: 核心分析引擎 (优先级: P0)

4. **画布完整性检查**
   - [ ] 实现9模块必填字段验证
   - [ ] 检查信息缺失项
   - [ ] 生成完整性评分

5. **一致性验证算法**
   - [ ] 实现价值主张-客户匹配检查
   - [ ] 验证收入-成本结构一致性
   - [ ] 检查渠道-客户关系匹配
   - [ ] 生成一致性报告

6. **AI 分析集成**
   - [ ] 集成 OpenAI API
   - [ ] 实现结构化分析 prompt
   - [ ] 处理 AI 响应解析
   - [ ] 添加错误重试机制

### 阶段 3: 建议生成器 (优先级: P1)

7. **战略建议引擎**
   - [ ] 实现建议模板系统
   - [ ] 开发 SWOT 分析算法
   - [ ] 生成优化建议
   - [ ] 实现建议优先级排序

8. **行业知识库**
   - [ ] 构建行业规则库
   - [ ] 实现案例匹配系统
   - [ ] 添加最佳实践数据库
   - [ ] 实现知识检索

### 阶段 4: API 服务开发 (优先级: P1)

9. **核心 API 端点**
   - [ ] POST /api/canvas/analyze - 分析画布
   - [ ] GET /api/canvas/{id} - 获取结果
   - [ ] GET /api/canvas/{id}/recommendations - 获取建议
   - [ ] POST /api/canvas/validate - 验证画布

10. **异步任务处理**
    - [ ] 集成 Celery 任务队列
    - [ ] 实现任务状态追踪
    - [ ] 添加任务取消功能
    - [ ] 实现结果缓存

### 阶段 5: 前端界面 (优先级: P2)

11. **输入界面**
    - [ ] 设计9模块输入表单
    - [ ] 实现表单验证
    - [ ] 添加自动保存功能
    - [ ] 实现模板加载

12. **结果展示**
    - [ ] 设计分析报告页面
    - [ ] 实现评分可视化
    - [ ] 创建建议卡片组件
    - [ ] 添加导出功能

13. **可视化图表**
    - [ ] 实现画布布局图
    - [ ] 创建关系网络图
    - [ ] 添加趋势分析图
    - [ ] 实现交互式图表

### 阶段 6: 测试和部署 (优先级: P2)

14. **测试覆盖**
    - [ ] 单元测试 (pytest)
    - [ ] 集成测试
    - [ ] API 测试
    - [ ] E2E 测试

15. **部署准备**
    - [ ] Docker 容器化
    - [ ] CI/CD 流程
    - [ ] 监控和告警
    - [ ] 文档完善

---

## 第三步：约束生成

**命令**：
```
/dnaspec.constraint-generator 为商业画布分析智能体生成业务规则、数据验证和AI安全约束
```

**生成的约束条件**：

### 业务规则约束

1. **完整性要求**
   - 价值主张：至少1个核心价值
   - 客户细分：至少1个目标客户群
   - 渠道：至少1个分销渠道
   - 客户关系：明确定义关系类型
   - 收入流：至少1个收入来源
   - 关键资源：列出核心资源
   - 关键活动：列出核心活动
   - 关键伙伴：可选但建议填写
   - 成本结构：明确主要成本项

2. **一致性规则**
   - 价值主张必须与客户细分匹配
   - 渠道必须能够触达定义的客户细分
   - 收入流必须与价值主张一致
   - 成本结构必须覆盖关键活动成本
   - 关键资源必须支持关键活动

3. **评分标准**
   - 完整性评分：0-100分
   - 一致性评分：0-100分
   - 可行性评分：0-100分
   - 综合评分：加权平均

### 数据验证约束

1. **输入验证**
   ```python
   # 字段长度限制
   MAX_TEXT_LENGTH = 2000
   MIN_TEXT_LENGTH = 10

   # 必填字段
   REQUIRED_FIELDS = [
       'value_propositions',
       'customer_segments',
       'channels',
       'customer_relationships',
       'revenue_streams',
       'key_resources',
       'key_activities',
       'cost_structure'
   ]

   # 数据格式
   ALLOWED_FORMATS = ['text', 'markdown', 'json']
   ```

2. **安全验证**
   ```python
   # 内容安全检查
   FORBIDDEN_PATTERNS = [
       r'<script[^>]*>',
       r'javascript:',
       r'data:text/html'
   ]

   # API 速率限制
   RATE_LIMIT = "10/minute"
   MAX_REQUEST_SIZE = "1MB"
   ```

### AI 安全约束

1. **Prompt 注入防护**
   - 输入内容过滤和清洗
   - 限制用户输入长度
   - 检测恶意模式

2. **输出验证**
   - AI 响应内容审核
   - 敏感信息过滤
   - 建议合理性检查

3. **使用量控制**
   ```python
   MAX_TOKENS_PER_REQUEST = 2000
   MAX_REQUESTS_PER_HOUR = 50
   DAILY_BUDGET_LIMIT = 100  # USD
   ```

4. **数据隐私**
   - 不存储敏感商业信息
   - 实现数据匿名化
   - 提供数据删除功能

### 质量保证约束

1. **分析质量标准**
   - 必须提供可操作的建议
   - 建议必须基于画布内容
   - 避免空泛的通用建议
   - 提供具体改进方向

2. **响应时间约束**
   - API 响应 < 2秒 (健康检查)
   - 分析任务 < 30秒 (完整分析)
   - 异步任务 < 5分钟

---

## 第四步：智能体创建

**命令**：
```
/dnaspec.agent-creator 创建一个商业画布分析智能代理，包含：
1. 自动分析工作流
2. 质量检查逻辑
3. 建议生成策略
4. 学习反馈机制
```

**生成的智能体配置**：

### 智能体架构

```python
# src/agents/business_canvas_agent.py

from typing import Dict, List, Optional
from dataclasses import dataclass
import json

@dataclass
class CanvasBlock:
    """商业画布单个模块"""
    name: str
    content: str
    priority: int = 1
    completeness_score: float = 0.0

@dataclass
class AnalysisResult:
    """分析结果"""
    canvas_id: str
    completeness_score: float
    consistency_score: float
    overall_score: float
    issues: List[str]
    recommendations: List[str]
    strategic_insights: List[str]

class BusinessCanvasAgent:
    """商业画布分析智能体"""

    def __init__(self, config: Dict):
        self.config = config
        self.canvas_blocks = []
        self.analysis_rules = self._load_rules()

    def analyze_canvas(self, canvas_data: Dict) -> AnalysisResult:
        """分析商业画布"""
        # 1. 解析画布数据
        self._parse_canvas(canvas_data)

        # 2. 完整性检查
        completeness = self._check_completeness()

        # 3. 一致性验证
        consistency = self._check_consistency()

        # 4. AI 深度分析
        ai_insights = self._ai_deep_analysis()

        # 5. 生成建议
        recommendations = self._generate_recommendations()

        # 6. 综合评分
        overall = self._calculate_overall_score(
            completeness, consistency, ai_insights
        )

        return AnalysisResult(
            canvas_id=canvas_data.get('id'),
            completeness_score=completeness['score'],
            consistency_score=consistency['score'],
            overall_score=overall,
            issues=completeness['issues'] + consistency['issues'],
            recommendations=recommendations,
            strategic_insights=ai_insights['insights']
        )

    def _parse_canvas(self, canvas_data: Dict):
        """解析画布数据"""
        blocks = [
            'value_propositions',
            'customer_segments',
            'channels',
            'customer_relationships',
            'revenue_streams',
            'key_resources',
            'key_activities',
            'key_partners',
            'cost_structure'
        ]

        self.canvas_blocks = []
        for block in blocks:
            content = canvas_data.get(block, '')
            self.canvas_blocks.append(CanvasBlock(
                name=block,
                content=content
            ))

    def _check_completeness(self) -> Dict:
        """检查完整性"""
        issues = []
        filled_blocks = 0

        for block in self.canvas_blocks:
            if len(block.content) < 10:
                issues.append(f"❌ {block.name}: 内容太少")
            elif len(block.content) < 50:
                issues.append(f"⚠️ {block.name}: 建议补充更多细节")
            else:
                filled_blocks += 1

        score = (filled_blocks / len(self.canvas_blocks)) * 100

        return {
            'score': score,
            'issues': issues,
            'filled_blocks': filled_blocks
        }

    def _check_consistency(self) -> Dict:
        """检查一致性"""
        issues = []

        # 检查价值主张与客户细分匹配
        value_props = self._get_block_content('value_propositions')
        customers = self._get_block_content('customer_segments')

        if value_props and customers:
            # AI 分析匹配度
            match_score = self._analyze_value_customer_match(
                value_props, customers
            )
            if match_score < 0.6:
                issues.append("⚠️ 价值主张与客户细分匹配度较低")

        # 检查收入与成本匹配
        revenue = self._get_block_content('revenue_streams')
        costs = self._get_block_content('cost_structure')

        if revenue and costs:
            # 验证商业模式可行性
            viability = self._check_business_viability(revenue, costs)
            if viability < 0.5:
                issues.append("❌ 收入模式可能无法覆盖成本")

        score = max(0, 100 - len(issues) * 15)

        return {
            'score': score,
            'issues': issues
        }

    def _ai_deep_analysis(self) -> Dict:
        """AI 深度分析"""
        # 构建分析 prompt
        canvas_summary = self._build_canvas_summary()

        prompt = f"""
        作为一位商业战略专家，分析以下商业模式画布：

        {canvas_summary}

        请提供：
        1. 核心优势识别（2-3条）
        2. 潜在风险分析（2-3条）
        3. 战略建议（3-5条）
        4. 创新机会（2-3条）
        """

        # 调用 LLM API
        response = self._call_llm(prompt)

        # 解析响应
        insights = self._parse_ai_response(response)

        return {
            'insights': insights,
            'raw_response': response
        }

    def _generate_recommendations(self) -> List[str]:
        """生成优化建议"""
        recommendations = []

        # 基于完整性的建议
        for block in self.canvas_blocks:
            if len(block.content) < 50:
                recommendations.append(
                    f"💡 完善 {block.name}: 添加更多细节和具体信息"
                )

        # 基于一致性的建议
        recommendations.extend(self._get_consistency_recommendations())

        # AI 生成的战略建议
        ai_recommendations = self._get_ai_recommendations()
        recommendations.extend(ai_recommendations)

        return recommendations

    def _calculate_overall_score(
        self,
        completeness: Dict,
        consistency: Dict,
        ai_insights: Dict
    ) -> float:
        """计算综合评分"""
        weights = {
            'completeness': 0.3,
            'consistency': 0.4,
            'ai_quality': 0.3
        }

        ai_score = self._evaluate_ai_insights(ai_insights)

        overall = (
            completeness['score'] * weights['completeness'] +
            consistency['score'] * weights['consistency'] +
            ai_score * weights['ai_quality']
        )

        return round(overall, 2)

    def _get_block_content(self, block_name: str) -> str:
        """获取模块内容"""
        for block in self.canvas_blocks:
            if block.name == block_name:
                return block.content
        return ""

    def _build_canvas_summary(self) -> str:
        """构建画布摘要"""
        summary = []
        for block in self.canvas_blocks:
            summary.append(f"**{block.name}**:\n{block.content}\n")
        return "\n".join(summary)

    def _call_llm(self, prompt: str) -> str:
        """调用 LLM API"""
        # 实际实现中调用 OpenAI/Claude API
        # 这里返回模拟数据
        return """
        ### 核心优势
        1. 价值主张清晰，专注解决特定客户痛点
        2. 多元化收入模式，降低单一依赖风险

        ### 潜在风险
        1. 客户获取成本可能较高
        2. 关键资源依赖外部伙伴

        ### 战略建议
        1. 优先验证核心假设，快速迭代
        2. 建立差异化竞争壁垒
        3. 优化成本结构，提高利润率

        ### 创新机会
        1. 探索订阅制收入模式
        2. 利用数据资产创造新价值
        """

    def _parse_ai_response(self, response: str) -> List[str]:
        """解析 AI 响应"""
        insights = []
        lines = response.split('\n')
        current_section = None

        for line in lines:
            line = line.strip()
            if line.startswith('###'):
                current_section = line.replace('###', '').strip()
            elif line and line.startswith(('1.', '2.', '3.', '4.')):
                insights.append(f"**{current_section}**: {line[3:]}")

        return insights

    def _load_rules(self) -> Dict:
        """加载分析规则"""
        # 从配置文件或数据库加载
        return {}

    def _analyze_value_customer_match(self, value: str, customers: str) -> float:
        """分析价值主张与客户匹配度"""
        # AI 分析匹配度
        return 0.75  # 模拟值

    def _check_business_viability(self, revenue: str, costs: str) -> float:
        """检查商业可行性"""
        # AI 分析可行性
        return 0.65  # 模拟值

    def _get_consistency_recommendations(self) -> List[str]:
        """获取一致性建议"""
        return [
            "💡 确保渠道能够有效触达定义的客户细分",
            "💡 验证收入流与价值主张的一致性"
        ]

    def _get_ai_recommendations(self) -> List[str]:
        """获取 AI 建议"""
        return [
            "💡 考虑引入免费增值模式扩大用户基础",
            "💡 建立社区增强客户粘性",
            "💡 探索平台化战略，连接供需双方"
        ]

    def _evaluate_ai_insights(self, insights: Dict) -> float:
        """评估 AI 洞察质量"""
        # 基于洞察数量、深度、相关性评分
        base_score = 70
        insight_count = len(insights.get('insights', []))
        return min(100, base_score + insight_count * 3)
```

### 智能体配置文件

```yaml
# config/agent_config.yaml

agent:
  name: "Business Canvas Analyzer"
  version: "1.0.0"
  description: "智能商业画布分析助手"

capabilities:
  - completeness_check
  - consistency_validation
  - ai_analysis
  - recommendation_generation

analysis:
  completeness:
    min_score: 60
    weight: 0.3

  consistency:
    min_score: 50
    weight: 0.4

  ai_quality:
    weight: 0.3

ai_providers:
  - name: "openai"
    model: "gpt-4"
    max_tokens: 2000
    temperature: 0.7

  - name: "anthropic"
    model: "claude-3-5-sonnet"
    max_tokens: 2000
    temperature: 0.7

rules:
  min_text_length: 10
  max_text_length: 2000
  required_fields:
    - value_propositions
    - customer_segments
    - channels
    - customer_relationships
    - revenue_streams
    - key_resources
    - key_activities
    - cost_structure

output_format:
  - summary
  - detailed_analysis
  - recommendations
  - score_breakdown
  - visual_charts
```

---

## 项目实现

现在我们将实现这个项目！
