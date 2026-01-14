#!/usr/bin/env python3
"""
真实场景演示 - 智选电商平台项目

这个脚本演示在实际项目场景中如何使用 DNASPEC 技能。
模拟项目经理、架构师、工程师等真实用户的使用流程。
"""
import sys
import os
import json

# 添加项目路径
sys.path.insert(0, 'D:/DAIP/dnaSpec')

from src.dna_spec_kit_integration.core.skill_executor import SkillExecutor
from src.dna_spec_kit_integration.core.python_bridge import PythonBridge
from src.dna_spec_kit_integration.core.skill_mapper import SkillMapper

class ProjectTeam:
    """项目团队模拟"""

    def __init__(self):
        self.python_bridge = PythonBridge()
        self.skill_mapper = SkillMapper()
        self.executor = SkillExecutor(self.python_bridge, self.skill_mapper)

        print("\n" + "="*70)
        print("智选电商平台 - 真实场景演示")
        print("="*70)

    def execute_skill(self, skill_name, params, role="Team Member"):
        """执行技能并格式化输出"""
        print(f"\n{'─'*70}")
        print(f"👤 角色: {role}")
        print(f"🔧 使用技能: {skill_name}")
        print(f"{'─'*70}")
        print(f"📝 输入:")
        print(params)
        print(f"{'─'*70}\n")

        result = self.executor.execute(skill_name, params)

        if result['success']:
            print("✅ 执行成功!\n")
            # 解析JSON结果
            try:
                body = result['rawResult']['body']
                data = json.loads(body) if isinstance(body, str) else body

                if data.get('statusCode') == 200:
                    result_data = json.loads(data['body']) if isinstance(data['body'], str) else data['body']

                    # 格式化输出
                    print("📊 结果:")
                    print(json.dumps(result_data, ensure_ascii=False, indent=2))
                else:
                    print("❌ 技能返回错误:")
                    print(data.get('body', 'Unknown error'))
            except Exception as e:
                print("结果:", result.get('result', 'No result'))
        else:
            print(f"❌ 执行失败: {result.get('error', 'Unknown error')}")

        return result


def scenario_1_project_manager(team):
    """场景1: 项目经理 - 任务分解"""
    print("\n" + "="*70)
    print("场景 1: 项目启动 - 任务分解")
    print("="*70)
    print("\n背景: 作为项目经理，我需要将整个电商平台项目分解为可管理的开发任务")
    print("时间: 项目第1周")
    print("目标: 为3个月的开发周期制定详细的任务计划\n")

    input_text = """
将智选电商平台的开发分解为具体任务。

项目概况：
- B2C电商平台，类似淘宝/京东
- 需要5个Epic：用户认证、商品浏览、购物车、订单管理、商家后台
- 技术栈：React + TypeScript前端，Node.js + Express后端，PostgreSQL数据库
- 团队规模：10人（2前端+3后端+1测试+1运维+2产品+1PM）
- 开发周期：3个月（12周）

开发阶段：
1. 第1-2周：基础架构搭建（CI/CD、开发环境、代码规范）
2. 第3-8周：核心功能开发（用户认证、商品、订单、支付）
3. 第9-11周：扩展功能（商家后台、数据统计、搜索推荐）
4. 第12周：测试、优化、上线准备

请按开发优先级和依赖关系进行任务分解，每个任务应该包含：
- 任务名称
- 预估工时
- 负责角色
- 依赖关系
"""

    team.execute_skill('task-decomposer', input_text, role="项目经理")


def scenario_2_architect(team):
    """场景2: 架构师 - 系统架构设计"""
    print("\n\n" + "="*70)
    print("场景 2: 技术架构设计")
    print("="*70)
    print("\n背景: 作为系统架构师，我需要设计高可用、可扩展的微服务架构")
    print("时间: 项目第1周")
    print("目标: 完成系统架构设计文档，指导团队开发\n")

    input_text = """
为智选电商平台设计微服务系统架构。

核心业务需求：
1. 支持百万级注册用户，10万日活
2. 双11大促期间支持10万并发用户
3. 99.99%可用性（每年停机不超过52分钟）
4. 响应时间：95%的API请求在200ms内完成

技术约束：
- 前端：React + TypeScript，使用Ant Design组件库
- 后端：Node.js + Express，微服务架构
- 数据库：PostgreSQL主从复制（1主2从）+ Redis集群
- 消息队列：RabbitMQ集群
- 部署：Docker + Kubernetes，阿里云ECS

核心服务模块：
1. 用户服务（User Service）- 注册、登录、权限
2. 商品服务（Product Service）- 商品管理、库存管理
3. 订单服务（Order Service）- 订单创建、状态流转
4. 支付服务（Payment Service）- 支付对接、退款
5. 搜索服务（Search Service）- 商品搜索、推荐
6. 通知服务（Notification Service）- 短信、邮件、推送

请设计：
1. 服务拆分方案（如何划分服务边界）
2. 数据流转设计（服务间通信方式）
3. 容错机制（如何保证高可用）
4. 扩展性方案（如何应对大促流量）
5. 数据一致性（分布式事务处理）
"""

    team.execute_skill('architect', input_text, role="系统架构师")


def scenario_3_security_engineer(team):
    """场景3: 安全工程师 - 安全约束生成"""
    print("\n\n" + "="*70)
    print("场景 3: 支付模块安全设计")
    print("="*70)
    print("\n背景: 作为安全工程师，我需要为支付模块生成安全约束")
    print("时间: 项目第3周")
    print("目标: 确保支付模块符合PCI DSS标准，防范各类安全风险\n")

    input_text = """
为智选电商的支付模块生成安全约束和规则。

支付场景：
1. 支持多种支付方式：微信支付、支付宝、银联信用卡
2. 涉及高度敏感信息：银行卡号、CVV码、有效期、密码
3. 必须符合PCI DSS支付卡行业数据安全标准
4. 需要防范的安全威胁：
   - 中间人攻击（MITM）
   - 重放攻击
   - SQL注入
   - XSS跨站脚本攻击
   - CSRF跨站请求伪造
   - 暴力破解

安全要求：
1. 支付数据必须加密存储（AES-256）
2. 传输过程必须使用TLS 1.3加密
3. 敏感信息（卡号、CVV）必须脱敏展示
4. 支付超时控制：15分钟内完成支付
5. 支付幂等性：同一订单只能支付一次
6. 三次密码错误锁定账户

请生成：
1. 具体的安全约束规则
2. 实施方案（技术实现）
3. 验证方法（如何测试）
4. 合规检查清单
"""

    team.execute_skill('constraint-generator', input_text, role="安全工程师")


def scenario_4_tech_lead(team):
    """场景4: 技术负责人 - 代码审查代理"""
    print("\n\n" + "="*70)
    print("场景 4: 代码质量保障")
    print("="*70)
    print("\n背景: 作为技术负责人，我需要创建自动化代码审查工具")
    print("时间: 项目第2周")
    print("目标: 在开发初期建立代码质量保障机制\n")

    input_text = """
创建一个自动化代码审查智能代理。

代理应用场景：
- 自动审查GitHub Pull Request
- 在CI/CD流程中执行代码检查
- 帮助初级工程师提升代码质量
- 减少高级工程师的Code Review时间

技术栈：
- 前端：React + TypeScript + Ant Design
- 后端：Node.js + Express + TypeScript
- 代码规范：Airbnb Style Guide + ESLint + Prettier
- 测试框架：Jest + Supertest

代码质量标准：
1. 代码规范：
   - 遵循Airbnb风格指南
   - 使用ESLint强制检查
   - 使用Prettier统一格式

2. 代码复杂度：
   - 单个函数不超过50行
   - 圈复杂度（Cyclomatic Complexity）不超过10
   - 嵌套层级不超过4层

3. 安全检查：
   - 检测SQL注入风险
   - 检测XSS漏洞
   - 检测敏感信息泄露（API密钥、密码）
   - 检测不安全的eval()使用

4. 最佳实践：
   - 必须编写单元测试（测试覆盖率>80%）
   - 使用async/await而非回调
   - 正确处理Promise错误
   - 避免全局变量污染

请创建这个代理的配置，包括：
1. 代理角色定义
2. 能力清单
3. 审查规则
4. 输出格式（如何给出审查意见）
"""

    team.execute_skill('agent-creator', input_text, role="技术负责人")


def main():
    """主演示流程"""
    team = ProjectTeam()

    # 场景1：项目启动
    scenario_1_project_manager(team)

    # 场景2：架构设计
    scenario_2_architect(team)

    # 场景3：安全设计
    scenario_3_security_engineer(team)

    # 场景4：质量保障
    scenario_4_tech_lead(team)

    # 总结
    print("\n\n" + "="*70)
    print("演示总结")
    print("="*70)
    print("""
✅ 本次演示涵盖了真实项目场景中的4个关键环节：

1. 项目启动阶段 - 项目经理使用任务分解技能制定开发计划
2. 架构设计阶段 - 架构师使用架构设计技能规划技术方案
3. 安全设计阶段 - 安全工程师使用约束生成技能制定安全规则
4. 工程准备阶段 - 技术负责人使用代理创建技能建立质量保障工具

💡 关键要点：

- DNASPEC 技能系统通过 Python API 调用
- 每个技能针对特定角色和场景设计
- 技能输出结构化、专业化的结果
- 可以直接应用于实际项目工作流程

🚀 下一步：

可以将这些技能集成到：
- CI/CD 流水线
- 项目管理工具（Jira、Trello）
- 代码审查平台（GitHub、GitLab）
- 文档生成系统
""")


if __name__ == '__main__':
    main()
