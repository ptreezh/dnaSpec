"""
商业画布分析智能体
Business Model Canvas Analysis Agent

使用 DNASPEC 命令开发的项目演示
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import re


@dataclass
class CanvasBlock:
    """商业画布单个模块"""
    name: str
    display_name: str
    content: str
    required: bool = True
    min_length: int = 10
    completeness_score: float = 0.0


@dataclass
class AnalysisIssue:
    """分析发现的问题"""
    block_name: str
    severity: str  # 'error', 'warning', 'info'
    message: str
    suggestion: str = ""


@dataclass
class Recommendation:
    """优化建议"""
    category: str  # 'completeness', 'consistency', 'strategy'
    priority: int  # 1-5, 5 highest
    title: str
    description: str
    action_items: List[str] = field(default_factory=list)


@dataclass
class AnalysisResult:
    """完整分析结果"""
    canvas_id: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    # 评分
    completeness_score: float = 0.0
    consistency_score: float = 0.0
    overall_score: float = 0.0

    # 分析内容
    issues: List[AnalysisIssue] = field(default_factory=list)
    recommendations: List[Recommendation] = field(default_factory=list)
    strategic_insights: List[str] = field(default_factory=list)

    # 详细报告
    summary: str = ""
    detailed_analysis: Dict = field(default_factory=dict)


class BusinessCanvasAgent:
    """
    商业画布分析智能体

    功能：
    1. 完整性检查 - 验证9个模块是否填写完整
    2. 一致性验证 - 检查模块间的逻辑一致性
    3. AI 深度分析 - 使用 LLM 进行战略分析
    4. 建议生成 - 提供优化建议
    """

    # 商业画布9个模块定义
    CANVAS_BLOCKS = [
        {
            'name': 'value_propositions',
            'display_name': '价值主张',
            'description': '为核心客户创造价值的产品或服务',
            'required': True
        },
        {
            'name': 'customer_segments',
            'display_name': '客户细分',
            'description': '企业想要接触和服务的不同人群或组织',
            'required': True
        },
        {
            'name': 'channels',
            'display_name': '渠道通路',
            'description': '如何将产品或服务传递给客户',
            'required': True
        },
        {
            'name': 'customer_relationships',
            'display_name': '客户关系',
            'description': '与客户建立的关系类型',
            'required': True
        },
        {
            'name': 'revenue_streams',
            'display_name': '收入来源',
            'description': '企业从每个客户群体获得的收入',
            'required': True
        },
        {
            'name': 'key_resources',
            'display_name': '核心资源',
            'description': '商业模式有效运行所必需的最重要资产',
            'required': True
        },
        {
            'name': 'key_activities',
            'display_name': '关键业务',
            'description': '企业为了实现商业模式必须做的最重要的事情',
            'required': True
        },
        {
            'name': 'key_partners',
            'display_name': '重要合作',
            'description': '让商业模式有效运行的供应商和网络',
            'required': False
        },
        {
            'name': 'cost_structure',
            'display_name': '成本结构',
            'description': '运营商业模式所发生的所有成本',
            'required': True
        }
    ]

    def __init__(self, config: Optional[Dict] = None):
        """初始化智能体"""
        self.config = config or {}
        self.canvas_blocks: List[CanvasBlock] = []
        self.issues: List[AnalysisIssue] = []
        self.recommendations: List[Recommendation] = []

    def analyze_canvas(self, canvas_data: Dict) -> AnalysisResult:
        """
        分析商业画布

        Args:
            canvas_data: 包含9个模块的画布数据

        Returns:
            AnalysisResult: 完整的分析结果
        """
        print("🤖 开始分析商业画布...\n")

        # 1. 解析画布数据
        self._parse_canvas(canvas_data)
        print(f"✓ 解析了 {len(self.canvas_blocks)} 个模块\n")

        # 2. 完整性检查
        print("📊 检查完整性...")
        completeness_result = self._check_completeness()
        print(f"✓ 完整性得分: {completeness_result['score']:.1f}/100\n")

        # 3. 一致性验证
        print("🔍 验证一致性...")
        consistency_result = self._check_consistency()
        print(f"✓ 一致性得分: {consistency_result['score']:.1f}/100\n")

        # 4. AI 深度分析
        print("🧠 执行 AI 深度分析...")
        ai_insights = self._ai_deep_analysis()
        print(f"✓ 生成了 {len(ai_insights['insights'])} 条战略洞察\n")

        # 5. 生成建议
        print("💡 生成优化建议...")
        self._generate_recommendations()
        print(f"✓ 生成了 {len(self.recommendations)} 条建议\n")

        # 6. 综合评分
        overall_score = self._calculate_overall_score(
            completeness_result,
            consistency_result,
            ai_insights
        )

        # 7. 生成摘要
        summary = self._generate_summary(
            completeness_result,
            consistency_result,
            ai_insights
        )

        print("✅ 分析完成！\n")
        print("=" * 60)
        print(f"综合评分: {overall_score:.1f}/100")
        print("=" * 60)

        return AnalysisResult(
            canvas_id=canvas_data.get('id', 'unknown'),
            completeness_score=completeness_result['score'],
            consistency_score=consistency_result['score'],
            overall_score=overall_score,
            issues=self.issues,
            recommendations=self.recommendations,
            strategic_insights=ai_insights['insights'],
            summary=summary,
            detailed_analysis={
                'completeness': completeness_result,
                'consistency': consistency_result,
                'ai_insights': ai_insights
            }
        )

    def _parse_canvas(self, canvas_data: Dict):
        """解析画布数据"""
        self.canvas_blocks = []

        for block_def in self.CANVAS_BLOCKS:
            name = block_def['name']
            content = canvas_data.get(name, '')

            block = CanvasBlock(
                name=name,
                display_name=block_def['display_name'],
                content=content.strip(),
                required=block_def['required']
            )
            self.canvas_blocks.append(block)

    def _check_completeness(self) -> Dict:
        """检查完整性"""
        filled_count = 0
        total_chars = 0

        for block in self.canvas_blocks:
            content_length = len(block.content)

            if content_length == 0:
                if block.required:
                    self.issues.append(AnalysisIssue(
                        block_name=block.name,
                        severity='error',
                        message=f"{block.display_name} 未填写",
                        suggestion=f"请填写{block.display_name}：{self._get_block_description(block.name)}"
                    ))
            elif content_length < block.min_length:
                self.issues.append(AnalysisIssue(
                    block_name=block.name,
                    severity='warning',
                    message=f"{block.display_name} 内容太少（{content_length} 字符）",
                    suggestion=f"建议至少补充到 {block.min_length} 字符以上"
                ))
            elif content_length < 50:
                self.issues.append(AnalysisIssue(
                    block_name=block.name,
                    severity='info',
                    message=f"{block.display_name} 可以更详细",
                    suggestion=f"建议补充更多细节，超过50字符"
                ))
            else:
                filled_count += 1
                block.completeness_score = min(100, content_length / 2)

            total_chars += content_length

        # 计算完整性得分
        score = (filled_count / len(self.canvas_blocks)) * 100

        return {
            'score': round(score, 1),
            'filled_blocks': filled_count,
            'total_blocks': len(self.canvas_blocks),
            'total_chars': total_chars
        }

    def _check_consistency(self) -> Dict:
        """检查一致性"""
        consistency_issues = []

        # 1. 检查价值主张与客户细分匹配
        value_content = self._get_block_content('value_propositions')
        customer_content = self._get_block_content('customer_segments')

        if value_content and customer_content:
            match_score = self._analyze_text_relevance(
                value_content, customer_content
            )

            if match_score < 0.3:
                consistency_issues.append({
                    'type': 'value_customer_mismatch',
                    'severity': 'error',
                    'message': '价值主张与客户细分匹配度很低',
                    'score': match_score
                })
            elif match_score < 0.5:
                consistency_issues.append({
                    'type': 'value_customer_weak',
                    'severity': 'warning',
                    'message': '价值主张与客户细分匹配度较低',
                    'score': match_score
                })

        # 2. 检查渠道与客户匹配
        channel_content = self._get_block_content('channels')
        if customer_content and channel_content:
            if not self._has_channel_customer_alignment(customer_content, channel_content):
                consistency_issues.append({
                    'type': 'channel_customer_mismatch',
                    'severity': 'warning',
                    'message': '渠道可能无法有效触达目标客户'
                })

        # 3. 检查收入与成本匹配
        revenue_content = self._get_block_content('revenue_streams')
        cost_content = self._get_block_content('cost_structure')

        if revenue_content and cost_content:
            if self._has_multiple_revenue_streams(revenue_content):
                if 'subscription' not in revenue_content.lower():
                    self.recommendations.append(Recommendation(
                        category='strategy',
                        priority=3,
                        title='探索订阅制收入模式',
                        description='订阅制可以提供稳定的经常性收入',
                        action_items=['评估产品是否适合订阅模式', '设计订阅层级和定价']
                    ))

        # 转换为 issues
        for issue in consistency_issues:
            self.issues.append(AnalysisIssue(
                block_name='consistency',
                severity=issue['severity'],
                message=issue['message'],
                suggestion=self._get_consistency_suggestion(issue['type'])
            ))

        # 计算一致性得分
        penalty = len(consistency_issues) * 15
        score = max(0, 100 - penalty)

        return {
            'score': round(score, 1),
            'issues': consistency_issues,
            'checks_performed': 3
        }

    def _ai_deep_analysis(self) -> Dict:
        """AI 深度分析（模拟版本）"""
        # 实际应用中会调用 LLM API
        # 这里提供模拟输出

        canvas_summary = self._build_canvas_summary()

        # 模拟 AI 分析结果
        insights = []

        # 基于已填充内容生成洞察
        filled_blocks = [b for b in self.canvas_blocks if len(b.content) >= 50]

        if len(filled_blocks) >= 6:
            insights.append("**核心优势**: 商业模式构思较为完整，各模块基本覆盖")
        else:
            insights.append("**待改进**: 商业模式尚需完善，建议优先补充核心模块")

        # 价值主张分析
        value_content = self._get_block_content('value_propositions')
        if value_content and len(value_content) > 100:
            insights.append("**价值主张**: 价值主张描述清晰，建议进一步量化价值")
        elif value_content:
            insights.append("**价值主张**: 建议更具体地描述为客户创造的独特价值")

        # 客户分析
        customer_content = self._get_block_content('customer_segments')
        if customer_content:
            if 'b2b' in customer_content.lower() or '企业' in customer_content:
                insights.append("**客户特征**: 面向企业客户，建议重点关注关系维护和价值证明")
            else:
                insights.append("**客户特征**: 面向个人消费者，建议重视用户体验和口碑传播")

        # 收入模式分析
        revenue_content = self._get_block_content('revenue_streams')
        if revenue_content:
            revenue_keywords = re.findall(r'(订阅|一次性|免费|广告|佣金|许可)', revenue_content, re.I)
            if revenue_keywords:
                insights.append(f"**收入模式**: 检测到 {' + '.join(set(revenue_keywords))} 等收入模式")

        return {
            'insights': insights,
            'confidence': 0.75,
            'analysis_depth': 'basic'
        }

    def _generate_recommendations(self):
        """生成优化建议"""
        # 基于完整性问题生成建议
        for issue in self.issues:
            if issue.severity == 'error':
                self.recommendations.append(Recommendation(
                    category='completeness',
                    priority=5,
                    title=f'补充 {issue.block_name}',
                    description=issue.message,
                    action_items=[issue.suggestion]
                ))

        # 基于战略建议
        self.recommendations.extend([
            Recommendation(
                category='strategy',
                priority=4,
                title='验证核心假设',
                description='在投入大量资源前，验证商业模式的关键假设',
                action_items=[
                    '识别最重要的3-5个假设',
                    '设计MVP进行快速验证',
                    '收集真实用户反馈'
                ]
            ),
            Recommendation(
                category='strategy',
                priority=3,
                title='建立竞争壁垒',
                description='识别并强化你的竞争优势',
                action_items=[
                    '分析竞争对手的弱点',
                    '找到差异化定位',
                    '构建网络效应或规模优势'
                ]
            ),
            Recommendation(
                category='consistency',
                priority=3,
                title='优化商业模式循环',
                description='确保各模块相互强化，形成正向循环',
                action_items=[
                    '检查价值主张是否真正解决客户痛点',
                    '验证渠道是否有效触达目标客户',
                    '确保收入模式可持续'
                ]
            )
        ])

        # 按优先级排序
        self.recommendations.sort(key=lambda x: x.priority, reverse=True)

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

        # AI 质量评分（基于洞察数量）
        ai_score = min(100, 60 + len(ai_insights['insights']) * 5)

        overall = (
            completeness['score'] * weights['completeness'] +
            consistency['score'] * weights['consistency'] +
            ai_score * weights['ai_quality']
        )

        return round(overall, 1)

    def _generate_summary(
        self,
        completeness: Dict,
        consistency: Dict,
        ai_insights: Dict
    ) -> str:
        """生成分析摘要"""
        lines = [
            "# 商业画布分析报告\n",
            f"**完整性得分**: {completeness['score']}/100 "
            f"({completeness['filled_blocks']}/{completeness['total_blocks']} 模块已填写)\n",
            f"**一致性得分**: {consistency['score']}/100\n",
            f"**发现问题**: {len(self.issues)} 个\n",
            f"**优化建议**: {len(self.recommendations)} 条\n",
            "\n## 关键洞察\n"
        ]

        for insight in ai_insights['insights'][:3]:
            lines.append(f"- {insight}")

        return "\n".join(lines)

    def _get_block_content(self, block_name: str) -> str:
        """获取模块内容"""
        for block in self.canvas_blocks:
            if block.name == block_name:
                return block.content
        return ""

    def _get_block_description(self, block_name: str) -> str:
        """获取模块描述"""
        for block_def in self.CANVAS_BLOCKS:
            if block_def['name'] == block_name:
                return block_def['description']
        return ""

    def _build_canvas_summary(self) -> str:
        """构建画布摘要"""
        lines = []
        for block in self.canvas_blocks:
            if block.content:
                lines.append(f"**{block.display_name}**:")
                lines.append(f"{block.content}\n")
        return "\n".join(lines)

    def _analyze_text_relevance(self, text1: str, text2: str) -> float:
        """分析两段文本的相关性（简化版）"""
        # 实际应用中可以使用更复杂的NLP方法
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union) if union else 0.0

    def _has_channel_customer_alignment(self, customers: str, channels: str) -> bool:
        """检查渠道与客户是否匹配"""
        # 简化的匹配逻辑
        customer_lower = customers.lower()
        channel_lower = channels.lower()

        # 企业客户匹配 B2B 渠道
        if '企业' in customer_lower or 'b2b' in customer_lower:
            return any(kw in channel_lower for kw in ['销售团队', '分销商', '展会', 'linkedin'])

        # 个人客户匹配 B2C 渠道
        if any(kw in customer_lower for kw in ['个人', '消费者', '用户', '大众']):
            return any(kw in channel_lower for kw in ['电商', '社交媒体', '应用商店', '零售'])

        return True  # 默认通过

    def _has_multiple_revenue_streams(self, revenue_content: str) -> bool:
        """检查是否有多种收入来源"""
        # 检查是否包含"和"、"或"等连接词，或使用换行、列表
        indicators = ['和', '或', '、', '\n', '1.', '2.']
        return any(indicator in revenue_content for indicator in indicators)

    def _get_consistency_suggestion(self, issue_type: str) -> str:
        """获取一致性问题的建议"""
        suggestions = {
            'value_customer_mismatch': '确保价值主张明确指出为客户解决的具体问题',
            'value_customer_weak': '建议更清晰地说明产品/服务如何满足目标客户的需求',
            'channel_customer_mismatch': '验证所选渠道是否能有效触达定义的客户群体',
            'revenue_cost_mismatch': '确保收入模式能够覆盖运营成本并产生利润'
        }
        return suggestions.get(issue_type, '请检查相关模块的逻辑一致性')

    def export_report(self, result: AnalysisResult, format: str = 'markdown') -> str:
        """导出分析报告"""
        if format == 'markdown':
            return self._export_markdown(result)
        elif format == 'json':
            return json.dumps(result.__dict__, ensure_ascii=False, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _export_markdown(self, result: AnalysisResult) -> str:
        """导出为 Markdown 格式"""
        lines = [
            "# 商业画布分析报告",
            f"\n**生成时间**: {result.timestamp}",
            f"**画布ID**: {result.canvas_id}\n",
            "---\n",
            "## 评分总览\n",
            f"- **完整性**: {result.completeness_score}/100",
            f"- **一致性**: {result.consistency_score}/100",
            f"- **综合得分**: {result.overall_score}/100\n",
            "---\n",
            "## 分析摘要\n",
            result.summary,
            "\n---\n",
            "## 发现的问题\n"
        ]

        for issue in result.issues:
            icon = {'error': '❌', 'warning': '⚠️', 'info': 'ℹ️'}[issue.severity]
            lines.append(f"### {icon} {issue.block_name}")
            lines.append(f"{issue.message}\n")
            if issue.suggestion:
                lines.append(f"**建议**: {issue.suggestion}\n")

        lines.append("\n---\n")
        lines.append("## 优化建议\n")

        for i, rec in enumerate(result.recommendations, 1):
            lines.append(f"### {i}. {rec.title} (优先级: {'⭐' * rec.priority})")
            lines.append(f"{rec.description}\n")
            if rec.action_items:
                lines.append("**行动项**:")
                for item in rec.action_items:
                    lines.append(f"- {item}")
                lines.append("")

        lines.append("\n---\n")
        lines.append("## 战略洞察\n")

        for insight in result.strategic_insights:
            lines.append(f"- {insight}")

        return "\n".join(lines)


# 便捷函数
def analyze_canvas(canvas_data: Dict, config: Optional[Dict] = None) -> AnalysisResult:
    """分析商业画布的便捷函数"""
    agent = BusinessCanvasAgent(config)
    return agent.analyze_canvas(canvas_data)


if __name__ == '__main__':
    # 示例使用
    sample_canvas = {
        'id': 'example-001',
        'value_propositions': '为中小企业提供一键式财务自动化解决方案，节省60%的财务处理时间',
        'customer_segments': '中小企业（50-500人），财务团队人数少于10人',
        'channels': '在线营销、合作伙伴销售网络、行业展会',
        'customer_relationships': '自助服务 + 专属客户经理',
        'revenue_streams': 'SaaS订阅费（月费/年费）、实施服务费、培训服务',
        'key_resources': '技术团队、财务领域专家、云计算平台',
        'key_activities': '产品开发、客户支持、市场营销',
        'key_partners': '会计师事务所、ERP系统集成商',
        'cost_structure': '研发成本、服务器成本、营销销售成本、客户支持成本'
    }

    agent = BusinessCanvasAgent()
    result = agent.analyze_canvas(sample_canvas)

    # 导出报告
    print("\n" + "="*60)
    print("分析报告 (Markdown)")
    print("="*60 + "\n")
    print(agent.export_report(result, format='markdown'))
