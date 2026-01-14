"""
DNASPEC Constraint Generator Skill - 符合AgentSkills.io标准
基于TDD实现，遵循KISS、SOLID、YAGNI原则
"""
import json
import uuid
from typing import Dict, Any, List, Optional
from skills.dnaspec_skill_framework import (
    DNASpecSkillBase, 
    track_execution,
    validate_text_input,
    generate_constraint_id,
    SkillValidationError
)


@track_execution
class ConstraintGeneratorSkill(DNASpecSkillBase):
    """
    约束生成技能 - 生成系统约束和验证规则
    
    符合AgentSkills.io规范：
    - name: constraint-generator
    - description: Generates system constraints and validation rules based on requirements and specifications
    - 支持5种约束类型：安全、性能、功能、质量、运维
    """
    
    def __init__(self):
        super().__init__(
            name="constraint-generator",
            description="Generates system constraints and validation rules based on requirements and specifications. Use when you need to define system boundaries, quality criteria, security policies, or operational constraints.",
            version="2.0.0"
        )
        
        # 支持的约束类型
        self.constraint_types = [
            "security",
            "performance", 
            "functional",
            "quality",
            "operational"
        ]
        
        # 约束类别配置
        self.constraint_configs = {
            "security": {
                "name": "安全约束",
                "description": "系统安全和数据保护要求",
                "max_constraints": 20,
                "default_constraints": 5
            },
            "performance": {
                "name": "性能约束",
                "description": "系统性能和可扩展性要求",
                "max_constraints": 15,
                "default_constraints": 4
            },
            "functional": {
                "name": "功能约束",
                "description": "系统功能和行为要求",
                "max_constraints": 25,
                "default_constraints": 6
            },
            "quality": {
                "name": "质量约束",
                "description": "系统质量和可靠性要求",
                "max_constraints": 20,
                "default_constraints": 5
            },
            "operational": {
                "name": "运维约束",
                "description": "系统运维和维护要求",
                "max_constraints": 15,
                "default_constraints": 4
            }
        }
        
        # 优先级级别
        self.priority_levels = ["low", "medium", "high", "critical"]
    
    def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证输入数据
        
        Args:
            input_data: 包含需求和变更请求的输入数据
            
        Returns:
            验证结果字典
        """
        # 验证必需字段
        if 'requirements' not in input_data:
            return {
                'valid': False, 
                'error': 'Missing required field: requirements'
            }
        
        # 验证需求描述
        req_validation = validate_text_input(input_data['requirements'], 'requirements')
        if not req_validation['valid']:
            return req_validation
        
        # 验证变更请求（如果提供）
        if 'change_request' in input_data:
            change_validation = validate_text_input(input_data['change_request'], 'change_request')
            if not change_validation['valid']:
                return change_validation
        
        # 验证约束类别（如果提供）
        if 'constraint_categories' in input_data:
            categories = input_data['constraint_categories']
            if not isinstance(categories, list):
                return {
                    'valid': False,
                    'error': 'constraint_categories must be a list'
                }
            
            invalid_categories = [cat for cat in categories if cat not in self.constraint_types]
            if invalid_categories:
                return {
                    'valid': False,
                    'error': f'Invalid constraint categories: {", ".join(invalid_categories)}'
                }
        
        # 验证优先级焦点（如果提供）
        if 'priority_focus' in input_data:
            priority = input_data['priority_focus']
            if priority not in self.priority_levels:
                return {
                    'valid': False,
                    'error': f'Invalid priority_focus. Must be one of: {", ".join(self.priority_levels)}'
                }
        
        return {'valid': True}
    
    def execute_skill(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行约束生成核心逻辑
        
        Args:
            input_data: 验证过的输入数据
            
        Returns:
            约束生成结果
        """
        requirements = input_data['requirements']
        change_request = input_data.get('change_request', '')
        constraint_categories = input_data.get('constraint_categories', self._infer_constraint_categories(requirements))
        priority_focus = input_data.get('priority_focus', self._infer_priority_focus(requirements))
        
        # 分析需求特征
        requirement_analysis = self._analyze_requirements(requirements, change_request)
        
        # 生成约束
        constraints = self._generate_constraints(
            requirements, change_request, constraint_categories, priority_focus, requirement_analysis
        )
        
        # 计算约束质量指标
        quality_metrics = self._calculate_constraint_quality(constraints, requirement_analysis)
        
        # 生成执行建议
        enforcement_recommendations = self._generate_enforcement_recommendations(
            constraints, constraint_categories, requirement_analysis
        )
        
        return {
            'constraints': constraints,
            'constraint_metadata': {
                'total_constraints': len(constraints),
                'category_distribution': self._calculate_category_distribution(constraints),
                'priority_distribution': self._calculate_priority_distribution(constraints),
                'generation_timestamp': self._get_timestamp(),
                'change_request_addressed': bool(change_request),
                'requirement_complexity': requirement_analysis['complexity']
            },
            'quality_metrics': quality_metrics,
            'enforcement_recommendations': enforcement_recommendations
        }
    
    def _infer_constraint_categories(self, requirements: str) -> List[str]:
        """
        从需求中推断约束类别
        
        Args:
            requirements: 需求描述
            
        Returns:
            推断的约束类别列表
        """
        req_lower = requirements.lower()
        categories = []
        
        # 安全关键词
        security_keywords = ["安全", "认证", "加密", "权限", "登录", "密码", "漏洞", "攻击", "防护"]
        if any(keyword in req_lower for keyword in security_keywords):
            categories.append("security")
        
        # 性能关键词
        performance_keywords = ["性能", "响应", "并发", "扩展", "负载", "延迟", "吞吐", "效率", "速度"]
        if any(keyword in req_lower for keyword in performance_keywords):
            categories.append("performance")
        
        # 功能关键词
        functional_keywords = ["功能", "特性", "业务", "流程", "规则", "逻辑", "数据", "操作", "输入", "输出"]
        if any(keyword in req_lower for keyword in functional_keywords):
            categories.append("functional")
        
        # 质量关键词
        quality_keywords = ["质量", "可靠", "稳定", "测试", "验证", "检查", "标准", "规范", "准确", "一致性"]
        if any(keyword in req_lower for keyword in quality_keywords):
            categories.append("quality")
        
        # 运维关键词
        operational_keywords = ["运维", "监控", "日志", "备份", "部署", "更新", "维护", "报警", "恢复"]
        if any(keyword in req_lower for keyword in operational_keywords):
            categories.append("operational")
        
        # 如果没有匹配任何类别，返回默认类别
        if not categories:
            return ["functional", "quality"]  # 默认约束类别
        
        return categories
    
    def _infer_priority_focus(self, requirements: str) -> str:
        """
        从需求中推断优先级焦点
        
        Args:
            requirements: 需求描述
            
        Returns:
            推断的优先级焦点
        """
        req_lower = requirements.lower()
        
        # 关键关键词
        critical_keywords = ["关键", "核心", "重要", "紧急", "必须", "强制", "安全", "合规"]
        high_keywords = ["优先", "重点", "主要", "应该", "建议", "推荐"]
        low_keywords = ["可选", "建议", "辅助", "支持", "改善", "优化"]
        
        if any(keyword in req_lower for keyword in critical_keywords):
            return "critical"
        elif any(keyword in req_lower for keyword in high_keywords):
            return "high"
        elif any(keyword in req_lower for keyword in low_keywords):
            return "low"
        else:
            return "medium"
    
    def _analyze_requirements(self, requirements: str, change_request: str) -> Dict[str, Any]:
        """
        分析需求特征
        
        Args:
            requirements: 需求描述
            change_request: 变更请求
            
        Returns:
            需求分析结果
        """
        text = f"{requirements} {change_request}"
        
        # 分析复杂度指标
        complexity_indicators = {
            'technical_terms': len([term for term in ['系统', '架构', '算法', '接口', '数据库'] if term in text.lower()]),
            'domain_specific': len([term for term in ['金融', '医疗', '教育', '电商'] if term in text.lower()]),
            'integration_needs': len([term for term in ['集成', '对接', '联调', '协同'] if term in text.lower()]),
            'compliance_terms': len([term for term in ['合规', '法规', '标准', '认证'] if term in text.lower()]),
            'quantitative_terms': len([term for term in ['毫秒', '并发', '99.9%', '1000', '100%'] if term in text.lower()])
        }
        
        # 计算综合复杂度
        total_indicators = sum(complexity_indicators.values())
        if total_indicators >= 8:
            complexity = "very_complex"
        elif total_indicators >= 5:
            complexity = "complex"
        elif total_indicators >= 3:
            complexity = "medium"
        else:
            complexity = "simple"
        
        # 识别领域
        domain = self._identify_domain(text)
        
        # 分析变更影响
        change_impact = self._analyze_change_impact(change_request)
        
        return {
            'complexity': complexity,
            'complexity_indicators': complexity_indicators,
            'domain': domain,
            'change_impact': change_impact,
            'total_length': len(text),
            'technical_depth': complexity_indicators['technical_terms']
        }
    
    def _identify_domain(self, text: str) -> str:
        """
        识别业务领域
        
        Args:
            text: 需求文本
            
        Returns:
            识别的领域
        """
        text_lower = text.lower()
        
        domain_keywords = {
            "金融": ["银行", "支付", "金融", "交易", "账户", "信贷", "投资"],
            "医疗": ["医院", "患者", "医疗", "诊断", "药品", "医生", "护士"],
            "教育": ["学校", "学生", "教育", "课程", "教师", "考试", "学习"],
            "电商": ["商品", "订单", "购物", "用户", "库存", "物流", "支付"],
            "政府": ["政府", "部门", "审批", "公文", "政策", "法规", "公共"],
            "企业": ["企业", "员工", "部门", "管理", "流程", "报告", "工作流"],
            "互联网": ["网站", "APP", "用户", "访问", "注册", "登录", "社交"],
            "工业": ["工厂", "生产", "设备", "质量控制", "安全", "检测"],
            "交通": ["交通", "车辆", "路线", "调度", "导航", "票务"]
        }
        
        max_score = 0
        best_domain = "通用"
        
        for domain, keywords in domain_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > max_score:
                max_score = score
                best_domain = domain
        
        return best_domain
    
    def _analyze_change_impact(self, change_request: str) -> str:
        """
        分析变更影响
        
        Args:
            change_request: 变更请求
            
        Returns:
            变更影响级别
        """
        if not change_request:
            return "none"
        
        change_lower = change_request.lower()
        
        high_impact_keywords = ["重构", "架构", "核心", "重大", "全面", "根本"]
        medium_impact_keywords = ["新增", "修改", "调整", "部分", "改进", "优化"]
        low_impact_keywords = ["修复", "完善", "小改", "微调", "细节"]
        
        if any(keyword in change_lower for keyword in high_impact_keywords):
            return "high"
        elif any(keyword in change_lower for keyword in medium_impact_keywords):
            return "medium"
        elif any(keyword in change_lower for keyword in low_impact_keywords):
            return "low"
        else:
            return "unknown"
    
    def _generate_constraints(
        self, 
        requirements: str, 
        change_request: str,
        categories: List[str],
        priority_focus: str,
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        生成约束列表
        
        Args:
            requirements: 需求描述
            change_request: 变更请求
            categories: 约束类别
            priority_focus: 优先级焦点
            analysis: 需求分析结果
            
        Returns:
            生成的约束列表
        """
        constraints = []
        
        # 为每个类别生成约束
        for category in categories:
            if category in self.constraint_configs:
                constraints.extend(self._generate_category_constraints(
                    category, requirements, change_request, priority_focus, analysis
                ))
        
        # 为变更请求生成特定约束
        if change_request:
            constraints.extend(self._generate_change_constraints(
                change_request, priority_focus, analysis
            ))
        
        return constraints
    
    def _generate_category_constraints(
        self, 
        category: str, 
        requirements: str, 
        change_request: str,
        priority_focus: str,
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        生成特定类别的约束
        
        Args:
            category: 约束类别
            requirements: 需求描述
            change_request: 变更请求
            priority_focus: 优先级焦点
            analysis: 需求分析结果
            
        Returns:
            该类别的约束列表
        """
        config = self.constraint_configs[category]
        
        # 基础约束生成器
        constraint_generators = {
            "security": [
                {
                    "name": "访问控制",
                    "rule": "所有系统操作必须通过身份验证"
                },
                {
                    "name": "数据加密",
                    "rule": "敏感数据在传输和存储时必须加密"
                },
                {
                    "name": "安全审计",
                    "rule": "记录所有关键操作的审计日志"
                },
                {
                    "name": "权限管理",
                    "rule": "实施最小权限原则，用户只能访问必需资源"
                },
                {
                    "name": "漏洞管理",
                    "rule": "定期进行安全漏洞扫描和评估"
                }
            ],
            "performance": [
                {
                    "name": "响应时间",
                    "rule": "用户请求响应时间必须在99%的情况下小于2秒"
                },
                {
                    "name": "并发处理",
                    "rule": "系统必须支持至少1000个并发用户"
                },
                {
                    "name": "资源利用率",
                    "rule": "CPU利用率不超过80%，内存利用率不超过85%"
                },
                {
                    "name": "数据传输",
                    "rule": "网络带宽必须支持最低100Mbps数据传输"
                }
            ],
            "functional": [
                {
                    "name": "业务逻辑",
                    "rule": "系统功能必须符合业务流程规范"
                },
                {
                    "name": "数据验证",
                    "rule": "所有输入数据必须进行格式和有效性验证"
                },
                {
                    "name": "错误处理",
                    "rule": "系统必须提供清晰的错误信息和恢复机制"
                },
                {
                    "name": "用户体验",
                    "rule": "界面设计必须符合用户体验最佳实践"
                },
                {
                    "name": "业务规则",
                    "rule": "系统必须严格执行业务规则和策略"
                }
            ],
            "quality": [
                {
                    "name": "代码质量",
                    "rule": "代码必须通过静态分析和代码审查"
                },
                {
                    "name": "测试覆盖",
                    "rule": "单元测试覆盖率不低于80%"
                },
                {
                    "name": "可靠性",
                    "rule": "系统可用性必须达到99.9%"
                },
                {
                    "name": "可维护性",
                    "rule": "代码必须遵循设计模式和最佳实践"
                },
                {
                    "name": "文档标准",
                    "rule": "所有功能必须有完整的技术文档"
                }
            ],
            "operational": [
                {
                    "name": "监控告警",
                    "rule": "系统关键指标必须实时监控和告警"
                },
                {
                    "name": "备份策略",
                    "rule": "数据必须定期备份，备份保留至少30天"
                },
                {
                    "name": "部署流程",
                    "rule": "所有部署必须遵循标准化的部署流程"
                },
                {
                    "name": "维护计划",
                    "rule": "系统必须定期维护，维护窗口不超过4小时"
                }
            ]
        }
        
        # 获取该类别的约束生成器
        generators = constraint_generators.get(category, [])
        
        # 根据优先级和复杂度调整约束数量
        constraint_count = config["default_constraints"]
        if priority_focus == "critical":
            constraint_count = min(config["max_constraints"], constraint_count + 3)
        elif priority_focus == "high":
            constraint_count = min(config["max_constraints"], constraint_count + 2)
        elif analysis["complexity"] in ["complex", "very_complex"]:
            constraint_count = min(config["max_constraints"], constraint_count + 2)
        
        # 生成约束
        constraints = []
        for i, generator in enumerate(generators[:constraint_count]):
            # 确定优先级
            if i < 2:  # 前两个约束为高优先级
                priority = "critical" if priority_focus == "critical" else "high"
            elif i < constraint_count // 2:
                priority = priority_focus
            else:
                priority = "medium"
            
            # 根据需求和变更调整约束描述
            rule = generator["rule"]
            if "安全" in requirements or "安全" in change_request:
                if "访问" in generator["name"]:
                    rule += "，必须实施多因素认证"
                elif "数据" in generator["name"]:
                    rule += "，加密强度必须符合行业标准"
            
            constraint = {
                "id": generate_constraint_id(),
                "type": category,
                "name": generator["name"],
                "description": generator["name"] + "约束",
                "rule": rule,
                "priority": priority,
                "validation_method": self._determine_validation_method(generator["name"]),
                "scope": self._determine_scope(category, analysis),
                "impact_level": self._determine_impact_level(generator["name"], priority),
                "enforcement_automated": self._can_automate_enforcement(generator["name"])
            }
            
            constraints.append(constraint)
        
        return constraints
    
    def _generate_change_constraints(
        self, 
        change_request: str,
        priority_focus: str,
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        生成变更相关的约束
        
        Args:
            change_request: 变更请求
            priority_focus: 优先级焦点
            analysis: 需求分析结果
            
        Returns:
            变更约束列表
        """
        constraints = []
        
        # 变更影响评估约束
        impact_constraints = {
            "high": [
                {
                    "name": "变更影响评估",
                    "rule": "重大变更必须进行影响评估和风险评估"
                },
                {
                    "name": "回滚计划",
                    "rule": "重大变更必须准备详细的回滚计划"
                },
                {
                    "name": "分阶段部署",
                    "rule": "重大变更必须分阶段部署，每个阶段都要验证"
                }
            ],
            "medium": [
                {
                    "name": "变更测试",
                    "rule": "变更必须通过完整的测试验证"
                },
                {
                    "name": "文档更新",
                    "rule": "变更后必须及时更新相关文档"
                },
                {
                    "name": "用户培训",
                    "rule": "变更涉及的功能必须进行用户培训"
                }
            ],
            "low": [
                {
                    "name": "变更记录",
                    "rule": "所有变更必须记录变更历史和原因"
                },
                {
                    "name": "功能验证",
                    "rule": "变更后必须验证功能正常"
                }
            ]
        }
        
        # 根据变更影响选择约束
        change_impact = analysis["change_impact"]
        generators = impact_constraints.get(change_impact, impact_constraints["medium"])
        
        # 生成约束
        for generator in generators:
            priority = self._adjust_priority_for_change(generator["name"], priority_focus, change_impact)
            
            constraint = {
                "id": generate_constraint_id(),
                "type": "change_management",
                "name": generator["name"],
                "description": f"变更管理约束: {generator['name']}",
                "rule": generator["rule"],
                "priority": priority,
                "validation_method": "change_verification",
                "scope": "change_lifecycle",
                "impact_level": self._determine_change_impact_level(change_impact),
                "enforcement_automated": False,  # 变更管理通常需要人工干预
                "related_change": change_request[:100] if change_request else ""
            }
            
            constraints.append(constraint)
        
        return constraints
    
    def _determine_validation_method(self, constraint_name: str) -> str:
        """
        确定验证方法
        
        Args:
            constraint_name: 约束名称
            
        Returns:
            验证方法
        """
        validation_map = {
            "访问控制": "automated_testing",
            "数据加密": "security_scan", 
            "安全审计": "log_analysis",
            "权限管理": "automated_checking",
            "漏洞管理": "security_testing",
            "响应时间": "performance_monitoring",
            "并发处理": "load_testing",
            "资源利用率": "resource_monitoring",
            "数据传输": "network_testing",
            "业务逻辑": "unit_testing",
            "数据验证": "input_validation",
            "错误处理": "error_testing",
            "用户体验": "user_testing",
            "业务规则": "business_rule_validation",
            "代码质量": "static_analysis",
            "测试覆盖": "coverage_analysis",
            "可靠性": "reliability_monitoring",
            "可维护性": "code_review",
            "文档标准": "documentation_review"
        }
        
        return validation_map.get(constraint_name, "manual_review")
    
    def _determine_scope(self, category: str, analysis: Dict[str, Any]) -> str:
        """
        确定约束范围
        
        Args:
            category: 约束类别
            analysis: 需求分析结果
            
        Returns:
            约束范围
        """
        if category == "security":
            return "entire_system"
        elif category == "performance":
            return "performance_critical"
        elif category == "functional":
            return "business_logic"
        elif category == "quality":
            return "development_process"
        elif category == "operational":
            return "production_environment"
        else:
            return "general"
    
    def _determine_impact_level(self, constraint_name: str, priority: str) -> str:
        """
        确定影响级别
        
        Args:
            constraint_name: 约束名称
            priority: 优先级
            
        Returns:
            影响级别
        """
        if priority == "critical":
            return "system_critical"
        elif priority == "high":
            return "high_impact"
        elif "constraint_name" in ["数据加密", "安全审计", "用户认证"]:
            return "security_critical"
        else:
            return "standard"
    
    def _can_automate_enforcement(self, constraint_name: str) -> bool:
        """
        判断是否可以自动化执行
        
        Args:
            constraint_name: 约束名称
            
        Returns:
            是否可以自动化执行
        """
        automatable_constraints = {
            "数据验证", "错误处理", "代码质量", "测试覆盖",
            "响应时间", "并发处理", "资源利用率",
            "监控告警", "权限管理"
        }
        
        return constraint_name in automatable_constraints
    
    def _adjust_priority_for_change(self, constraint_name: str, priority_focus: str, change_impact: str) -> str:
        """
        根据变更影响调整优先级
        
        Args:
            constraint_name: 约束名称
            priority_focus: 优先级焦点
            change_impact: 变更影响
            
        Returns:
            调整后的优先级
        """
        if change_impact == "high":
            return "critical"
        elif change_impact == "medium" and constraint_name in ["变更影响评估", "回滚计划"]:
            return "critical"
        elif change_focus == "critical":
            return "critical"
        elif priority_focus == "high":
            return "high"
        else:
            return "medium"
    
    def _determine_change_impact_level(self, change_impact: str) -> str:
        """
        确定变更影响级别
        
        Args:
            change_impact: 变更影响
            
        Returns:
            变更影响级别
        """
        impact_map = {
            "none": "no_change",
            "low": "low_impact",
            "medium": "medium_impact", 
            "high": "high_impact",
            "unknown": "unknown_impact"
        }
        
        return impact_map.get(change_impact, "medium_impact")
    
    def _calculate_constraint_quality(
        self, 
        constraints: List[Dict[str, Any]], 
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        计算约束质量指标
        
        Args:
            constraints: 约束列表
            analysis: 需求分析结果
            
        Returns:
            约束质量指标
        """
        # 覆盖度评分
        category_coverage = len(set(c['type'] for c in constraints)) / len(self.constraint_types)
        
        # 优先级分布评分
        priority_weights = {"critical": 1.0, "high": 0.8, "medium": 0.6, "low": 0.4}
        priority_score = sum(priority_weights.get(c['priority'], 0.4) for c in constraints) / len(constraints)
        
        # 可执行性评分
        automatable_ratio = sum(1 for c in constraints if c.get('enforcement_automated', False)) / len(constraints)
        executability_score = 1.0 - (automatable_ratio * 0.3)  # 自动化的约束可执行性更高
        
        # 完整性评分
        validation_coverage = len(set(c.get('validation_method', 'manual_review') for c in constraints)) / len(constraints)
        
        # 综合质量评分
        overall_quality = (
            category_coverage * 0.25 +
            priority_score * 0.30 +
            executability_score * 0.25 +
            validation_coverage * 0.20
        )
        
        return {
            'category_coverage': round(category_coverage, 3),
            'priority_alignment': round(priority_score, 3),
            'executability': round(executability_score, 3),
            'validation_completeness': round(validation_coverage, 3),
            'overall_quality': round(min(1.0, overall_quality), 3),
            'total_constraints': len(constraints)
        }
    
    def _calculate_category_distribution(self, constraints: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        计算类别分布
        
        Args:
            constraints: 约束列表
            
        Returns:
            类别分布字典
        """
        distribution = {}
        for constraint in constraints:
            category = constraint['type']
            distribution[category] = distribution.get(category, 0) + 1
        
        return distribution
    
    def _calculate_priority_distribution(self, constraints: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        计算优先级分布
        
        Args:
            constraints: 约束列表
            
        Returns:
            优先级分布字典
        """
        distribution = {}
        for constraint in constraints:
            priority = constraint['priority']
            distribution[priority] = distribution.get(priority, 0) + 1
        
        return distribution
    
    def _generate_enforcement_recommendations(
        self, 
        constraints: List[Dict[str, Any]], 
        categories: List[str], 
        analysis: Dict[str, Any]
    ) -> List[str]:
        """
        生成执行建议
        
        Args:
            constraints: 约束列表
            categories: 约束类别
            analysis: 需求分析结果
            
        Returns:
            执行建议列表
        """
        recommendations = [
            f"建立约束管理委员会，定期评估约束的有效性",
            f"实施自动化约束检查工具，提高执行效率",
            f"将约束要求纳入CI/CD流程，确保持续合规"
        ]
        
        # 根据类别添加特定建议
        if "security" in categories:
            recommendations.extend([
                "定期进行安全渗透测试和漏洞扫描",
                "建立安全事件响应机制和应急预案"
            ])
        
        if "performance" in categories:
            recommendations.extend([
                "建立性能基准测试和监控体系",
                "实施负载测试和容量规划机制"
            ])
        
        if "quality" in categories:
            recommendations.extend([
                "建立代码质量度量和改进机制",
                "实施持续集成和持续交付(CI/CD)流程"
            ])
        
        # 根据复杂度添加建议
        if analysis["complexity"] in ["complex", "very_complex"]:
            recommendations.extend([
                "建立分阶段的约束实施计划",
                "提供专门的约束培训和指导文档"
            ])
        
        # 根据优先级添加建议
        critical_constraints = [c for c in constraints if c.get('priority') == 'critical']
        if critical_constraints:
            recommendations.append("优先实施关键约束，确保系统核心功能安全可靠")
        
        return recommendations[:10]  # 限制建议数量
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.utcnow().isoformat()


# 创建技能实例
constraint_generator_skill = ConstraintGeneratorSkill()

# 导出Lambda处理器（符合AgentSkills.io标准）
def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Lambda处理器入口点"""
    return constraint_generator_skill.lambda_handler(event, context)

# 导出技能实例（用于注册）
def get_skill():
    """获取技能实例"""
    return constraint_generator_skill