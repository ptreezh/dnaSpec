"""
商业画布分析智能体 - 使用示例

演示如何使用 DNASPEC 命令开发的智能体
"""

from src.business_canvas_agent import (
    BusinessCanvasAgent,
    analyze_canvas,
    AnalysisResult
)


def print_section(title: str):
    """打印分节标题"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


# 示例1: 完整的画布分析
def example_1_complete_canvas():
    """示例1: 分析一个完整的商业画布"""
    print_section("示例1: 完整商业画布分析")

    canvas_data = {
        'id': 'tech-startup-001',
        'value_propositions': '''
为科技初创公司提供智能财务预测和分析平台。
通过AI和机器学习技术，自动分析财务数据，
预测未来现金流，识别潜在风险，提供决策建议。
相比传统财务软件，准确率提升40%，预测时间缩短80%。
        '''.strip(),

        'customer_segments': '''
1. A轮到C轮的科技创业公司（50-500人）
2. 财务团队规模较小（3-10人）的公司
3. 快速增长需要专业财务工具但预算有限的企业
4. 位于北美和欧洲市场的SaaS公司
        '''.strip(),

        'channels': '''
1. 在线营销和内容营销（SEO、博客、网络研讨会）
2. SaaS评测平台和软件目录
3. 行业合作伙伴推荐（云服务商、孵化器）
4. 科技会议和创业活动
5. 直接销售（针对大客户）
        '''.strip(),

        'customer_relationships': '''
1. 自助服务 + 在线帮助中心
2. 客户成功经理（针对企业版客户）
3. 社区支持和用户论坛
4. 定期培训和最佳实践分享
5. 自动化客户健康度监控
        '''.strip(),

        'revenue_streams': '''
1. SaaS订阅费
   - 基础版: $99/月
   - 专业版: $299/月
   - 企业版: 定制定价
2. 实施和集成服务费（一次性）
3. 培训和咨询服务（按小时）
4. 未来：API调用费用（开放平台后）
        '''.strip(),

        'key_resources': '''
1. 技术研发团队（工程师、数据科学家）
2. 财务和AI领域专家团队
3. 云计算基础设施（AWS）
4. 知识产权和算法模型
5. 品牌和客户案例
        '''.strip(),

        'key_activities': '''
1. 产品开发和迭代
2. AI模型训练和优化
3. 客户获取和营销
4. 客户成功和支持
5. 数据安全和合规管理
        '''.strip(),

        'key_partners': '''
1. 云服务提供商（AWS、Google Cloud）
2. 会计师事务所和财务咨询公司
3. 创业加速器和孵化器
4. 第三方系统集成商
5. 数据提供商（金融数据API）
        '''.strip(),

        'cost_structure': '''
1. 研发成本（60%）- 工程师薪资、基础设施
2. 营销销售成本（25%）- 广告、销售团队
3. 客户支持成本（10%）- 支持团队、工具
4. 运营管理成本（5%）- 行政、法务、办公
        '''.strip()
    }

    # 创建智能体并分析
    agent = BusinessCanvasAgent()
    result = agent.analyze_canvas(canvas_data)

    # 打印结果摘要
    print(f"✅ 分析完成！")
    print(f"\n评分:")
    print(f"  完整性: {result.completeness_score}/100")
    print(f"  一致性: {result.consistency_score}/100")
    print(f"  综合得分: {result.overall_score}/100")

    print(f"\n发现 {len(result.issues)} 个问题")
    print(f"生成 {len(result.recommendations)} 条建议")
    print(f"提供 {len(result.strategic_insights)} 条战略洞察")

    # 导出完整报告
    report = agent.export_report(result, format='markdown')

    # 保存报告
    with open('analysis_report_example1.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n📄 完整报告已保存到: analysis_report_example1.md")


# 示例2: 不完整的画布
def example_2_incomplete_canvas():
    """示例2: 分析一个不完整的画布"""
    print_section("示例2: 不完整画布分析")

    canvas_data = {
        'id': 'incomplete-002',
        'value_propositions': '提供在线教育服务',  # 太简短
        'customer_segments': '',  # 空白
        'channels': '社交媒体',
        'customer_relationships': '在线客服',
        # 缺少其他字段
    }

    agent = BusinessCanvasAgent()
    result = agent.analyze_canvas(canvas_data)

    print(f"\n⚠️ 完整性得分较低: {result.completeness_score}/100")
    print(f"\n主要问题:")
    for issue in result.issues[:5]:
        print(f"  - {issue.message}")


# 示例3: 传统企业转型
def example_3_traditional_business():
    """示例3: 传统企业数字化转型"""
    print_section("示例3: 传统零售企业数字化转型")

    canvas_data = {
        'id': 'retail-transformation-003',
        'value_propositions': '''
将传统社区便利店转型为智能新零售平台。
通过数字化工具和供应链优化，为社区居民提供
更便捷、更实惠的购物体验，同时帮助小店主
提升经营效率和盈利能力。
        '''.strip(),

        'customer_segments': '''
1. 社区居民（主要服务对象）
   - 年龄25-65岁
   - 注重便利性和价格
   - 日常高频购买需求
2. 传统小店主
   - 经营社区便利店
   - 希望提升数字化能力
   - 需要供应链支持
        '''.strip(),

        'channels': '''
1. 线下实体店（核心渠道）
2. 社区团购小程序
3. 微信社群和私域流量
4. 本地配送服务
5. 品牌合作和联合推广
        '''.strip(),

        'customer_relationships': '''
1. 人性化邻里服务
2. 会员体系和积分制度
3. 社区活动和互动
4. 定期优惠和促销
5. 客户反馈和投诉快速响应
        '''.strip(),

        'revenue_streams': '''
1. 商品销售差价
2. 会员费和订阅服务
3. 广告和品牌展示费
4. 配送服务费
5. 数据分析和洞察服务（未来）
        '''.strip(),

        'key_resources': '''
1. 实体店铺和选址
2. 供应链网络和仓储
3. 数字化平台和技术系统
4. 本地配送团队
5. 品牌和社区关系
        '''.strip(),

        'key_activities': '''
1. 商品采购和供应链管理
2. 门店运营和客户服务
3. 数字化平台维护
4. 社群运营和营销
5. 数据分析和优化
        '''.strip(),

        'key_partners': '''
1. 供应商和批发商
2. 物流配送公司
3. 技术服务商
4. 支付平台
5. 社区组织和物业
        '''.strip(),

        'cost_structure': '''
1. 商品成本（50%）
2. 房租和水电（20%）
3. 人力成本（15%）
4. 配送成本（10%）
5. 技术和营销（5%）
        '''.strip()
    }

    agent = BusinessCanvasAgent()
    result = agent.analyze_canvas(canvas_data)

    print(f"\n💡 关键洞察:")
    for insight in result.strategic_insights:
        print(f"  {insight}")

    print(f"\n🎯 优先建议:")
    for i, rec in enumerate(result.recommendations[:3], 1):
        print(f"  {i}. {rec.title}")


# 示例4: 使用便捷函数
def example_4_quick_analysis():
    """示例4: 快速分析"""
    print_section("示例4: 使用便捷函数快速分析")

    canvas = {
        'id': 'quick-004',
        'value_propositions': '为自由职业者提供时间管理和 invoicing 工具',
        'customer_segments': '自由职业者、独立咨询师',
        'channels': '应用商店、内容营销',
        'customer_relationships': '自助服务 + 邮件支持',
        'revenue_streams': '订阅费',
        'key_resources': '技术平台、开发团队',
        'key_activities': '产品开发、客户支持',
        'cost_structure': '主要是开发成本',
        'key_partners': '支付网关'
    }

    # 使用便捷函数
    result = analyze_canvas(canvas)

    print(f"✨ 综合得分: {result.overall_score}/100")
    print(f"\n📊 评分明细:")
    print(f"  完整性: {result.completeness_score}/100")
    print(f"  一致性: {result.consistency_score}/100")


# 示例5: JSON 导出
def example_5_json_export():
    """示例5: 导出 JSON 格式报告"""
    print_section("示例5: 导出 JSON 报告")

    canvas = {
        'id': 'json-export-005',
        'value_propositions': '提供企业级 AI 聊天机器人平台',
        'customer_segments': '大型企业客户',
        'channels': '直销、合作伙伴',
        'customer_relationships': '专属客户经理',
        'revenue_streams': '企业授权费',
        'key_resources': 'AI技术团队',
        'key_activities': '产品开发',
        'cost_structure': '研发成本',
        'key_partners': '云服务商'
    }

    agent = BusinessCanvasAgent()
    result = agent.analyze_canvas(canvas)

    # 导出 JSON
    json_report = agent.export_report(result, format='json')

    # 保存到文件
    with open('analysis_report_example5.json', 'w', encoding='utf-8') as f:
        f.write(json_report)

    print("✅ JSON 报告已生成")
    print(f"\n报告预览 (前500字符):")
    print(json_report[:500] + "...")


# 主函数
def main():
    """运行所有示例"""
    print("\n" + "🚀" * 35)
    print("  商业画布分析智能体 - 使用示例")
    print("  使用 DNASPEC 命令开发的项目演示")
    print("🚀" * 35)

    # 运行示例
    example_1_complete_canvas()
    example_2_incomplete_canvas()
    example_3_traditional_business()
    example_4_quick_analysis()
    example_5_json_export()

    # 总结
    print_section("总结")

    print("""
✅ 所有示例运行完成！

这个商业画布分析智能体展示了如何使用 DNASPEC 命令：

1. /dnaspec.architect - 设计系统架构
2. /dnaspec.task-decomposer - 分解开发任务
3. /dnaspec.constraint-generator - 生成约束条件
4. /dnaspec.agent-creator - 创建智能代理

核心功能：
- ✓ 完整性检查（9个模块）
- ✓ 一致性验证（模块间逻辑）
- ✓ AI 深度分析（战略洞察）
- ✓ 建议生成（优化方案）
- ✓ 报告导出（Markdown/JSON）

项目位置：
test_projects/business_canvas_agent/

文件说明：
- src/business_canvas_agent.py - 核心智能体代码
- demo.py - 使用示例（本文件）
- PROJECT.md - 项目文档和DNASPEC命令使用记录
    """)

    print("\n" + "=" * 70)
    print("💡 提示: 运行此脚本后会生成报告文件")
    print("   - analysis_report_example1.md")
    print("   - analysis_report_example5.json")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
