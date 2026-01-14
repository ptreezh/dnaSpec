"""
DNASPEC Agent Creator Skill - 符合AgentSkills.io标准
基于TDD实现，遵循KISS、SOLID、YAGNI原则
"""
import json
import uuid
from typing import Dict, Any, List, Optional
from skills.dnaspec_skill_framework import (
    DNASpecSkillBase, 
    track_execution,
    validate_text_input,
    SkillValidationError
)


@track_execution
class AgentCreatorSkill(DNASpecSkillBase):
    """
    智能体创建技能 - 专业化AI代理生成
    
    符合AgentSkills.io规范：
    - name: agent-creator
    - description: Creates specialized AI agents with specific roles, capabilities, and instructions
    - 支持3种智能体类型：领域专家、任务专家、角色助手
    """
    
    def __init__(self):
        super().__init__(
            name="agent-creator",
            description="Creates specialized AI agents with specific roles, capabilities, and instructions. Use when you need to create focused AI assistants for particular tasks, domains, or expertise areas.",
            version="2.0.0"
        )
        
        # 支持的智能体类型
        self.agent_types = [
            "domain_expert",
            "task_specialist", 
            "role_assistant"
        ]
        
        # 可用能力列表
        self.available_capabilities = {
            "technical": ["programming", "database", "security", "system_administration", "data_analysis"],
            "communication": ["writing", "presentation", "documentation", "translation"],
            "analysis": ["research", "evaluation", "problem_solving", "market_analysis"],
            "creative": ["design", "content_creation", "innovation", "ideation"],
            "management": ["planning", "coordination", "leadership", "project_management"]
        }
        
        # 人格类型定义
        self.personality_types = {
            "professional_precise": {
                "name": "专业精确型",
                "traits": "正式、准确、细节导向",
                "style": "正式沟通，精确表达，关注细节"
            },
            "friendly_supportive": {
                "name": "友好支持型", 
                "traits": "鼓励、耐心、乐于助人",
                "style": "友好沟通，耐心指导，提供支持"
            },
            "analytical_critical": {
                "name": "分析批判型",
                "traits": "系统性、质疑、彻底",
                "style": "逻辑分析，批判思考，深度审查"
            },
            "creative_innovative": {
                "name": "创新思维型",
                "traits": "想象力、开放、解决方案导向", 
                "style": "创造性思维，开放心态，寻求创新"
            },
            "direct_efficient": {
                "name": "直接高效型",
                "traits": "简洁、行动导向、实用",
                "style": "简洁表达，行动优先，务实解决"
            }
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证输入数据
        
        Args:
            input_data: 包含智能体描述和配置的输入数据
            
        Returns:
            验证结果字典
        """
        # 验证必需字段
        if 'agent_description' not in input_data:
            return {
                'valid': False, 
                'error': 'Missing required field: agent_description'
            }
        
        # 验证智能体描述
        desc_validation = validate_text_input(input_data['agent_description'], 'agent_description')
        if not desc_validation['valid']:
            return desc_validation
        
        # 验证能力列表（如果提供）
        if 'capabilities' in input_data:
            capabilities = input_data['capabilities']
            if not isinstance(capabilities, list):
                return {
                    'valid': False,
                    'error': 'capabilities must be a list'
                }
            
            if len(capabilities) > 20:
                return {
                    'valid': False,
                    'error': 'Too many capabilities (maximum 20)'
                }
            
            # 验证每个能力
            for cap in capabilities:
                if not isinstance(cap, str):
                    return {
                        'valid': False,
                        'error': 'All capabilities must be strings'
                    }
        
        # 验证可选字段
        if 'domain' in input_data:
            domain = input_data['domain']
            if not isinstance(domain, str):
                return {
                    'valid': False,
                    'error': 'domain must be a string'
                }
        
        if 'personality' in input_data:
            personality = input_data['personality']
            if personality not in self.personality_types:
                valid_personalities = list(self.personality_types.keys())
                return {
                    'valid': False,
                    'error': f'Invalid personality. Must be one of: {", ".join(valid_personalities)}'
                }
        
        if 'agent_type' in input_data:
            agent_type = input_data['agent_type']
            if agent_type not in self.agent_types:
                return {
                    'valid': False,
                    'error': f'Invalid agent_type. Must be one of: {", ".join(self.agent_types)}'
                }
        
        return {'valid': True}
    
    def execute_skill(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行智能体创建核心逻辑
        
        Args:
            input_data: 验证过的输入数据
            
        Returns:
            智能体配置结果
        """
        agent_description = input_data['agent_description']
        capabilities = input_data.get('capabilities', self._get_default_capabilities())
        domain = input_data.get('domain', self._infer_domain(agent_description))
        personality = input_data.get('personality', self._select_default_personality(agent_description))
        agent_type = input_data.get('agent_type', self._determine_agent_type(agent_description, capabilities))
        
        # 生成智能体配置
        agent_config = self._generate_agent_config(
            agent_description, capabilities, domain, personality, agent_type
        )
        
        # 计算智能体质量指标
        quality_metrics = self._calculate_agent_quality(agent_config, capabilities)
        
        # 生成使用建议
        usage_recommendations = self._generate_usage_recommendations(agent_config, agent_type)
        
        return {
            'agent_config': agent_config,
            'creation_metadata': {
                'agent_type': agent_type,
                'complexity': self._determine_complexity(capabilities),
                'estimated_effectiveness': quality_metrics['effectiveness'],
                'creation_timestamp': self._get_timestamp(),
                'total_capabilities': len(capabilities)
            },
            'quality_metrics': quality_metrics,
            'usage_recommendations': usage_recommendations
        }
    
    def _get_default_capabilities(self) -> List[str]:
        """获取默认能力列表"""
        return [
            "Task execution",
            "Information retrieval", 
            "Decision making",
            "Problem analysis"
        ]
    
    def _infer_domain(self, description: str) -> str:
        """
        从描述中推断领域
        
        Args:
            description: 智能体描述
            
        Returns:
            推断的领域
        """
        desc_lower = description.lower()
        
        # 领域关键词映射
        domain_keywords = {
            "software_development": ["编程", "开发", "代码", "programming", "development", "code"],
            "business": ["商业", "业务", "营销", "business", "marketing", "sales"],
            "academic": ["学术", "研究", "教学", "academic", "research", "teaching"],
            "creative": ["创意", "设计", "内容", "creative", "design", "content"],
            "analysis": ["分析", "数据", "研究", "analysis", "data", "research"],
            "technical": ["技术", "系统", "工程", "technical", "system", "engineering"],
            "management": ["管理", "协调", "计划", "management", "coordination", "planning"]
        }
        
        # 计算匹配度
        max_score = 0
        best_domain = "general"
        
        for domain, keywords in domain_keywords.items():
            score = sum(1 for kw in keywords if kw in desc_lower)
            if score > max_score:
                max_score = score
                best_domain = domain
        
        return best_domain
    
    def _select_default_personality(self, description: str) -> str:
        """
        根据描述选择默认人格类型
        
        Args:
            description: 智能体描述
            
        Returns:
            选择的人格类型
        """
        desc_lower = description.lower()
        
        # 人格关键词映射
        personality_keywords = {
            "professional_precise": ["专业", "精确", "准确", "professional", "precise", "accurate"],
            "friendly_supportive": ["友好", "支持", "帮助", "friendly", "supportive", "helpful"],
            "analytical_critical": ["分析", "批判", "审查", "analytical", "critical", "review"],
            "creative_innovative": ["创意", "创新", "想象", "creative", "innovative", "imaginative"],
            "direct_efficient": ["直接", "高效", "实用", "direct", "efficient", "practical"]
        }
        
        # 计算匹配度
        max_score = 0
        best_personality = "professional_precise"
        
        for personality, keywords in personality_keywords.items():
            score = sum(1 for kw in keywords if kw in desc_lower)
            if score > max_score:
                max_score = score
                best_personality = personality
        
        return best_personality
    
    def _determine_agent_type(self, description: str, capabilities: List[str]) -> str:
        """
        确定智能体类型
        
        Args:
            description: 智能体描述
            capabilities: 能力列表
            
        Returns:
            智能体类型
        """
        desc_lower = description.lower()
        
        # 类型关键词映射
        type_keywords = {
            "domain_expert": ["专家", "专长", "领域", "expert", "specialist", "domain"],
            "task_specialist": ["任务", "专门", "功能", "task", "specialized", "function"],
            "role_assistant": ["助手", "角色", "协助", "assistant", "role", "helper"]
        }
        
        # 计算关键词匹配
        max_score = 0
        best_type = "role_assistant"
        
        for agent_type, keywords in type_keywords.items():
            score = sum(1 for kw in keywords if kw in desc_lower)
            if score > max_score:
                max_score = score
                best_type = agent_type
        
        # 基于能力数量调整类型
        if len(capabilities) > 8:
            return "domain_expert"
        elif len(capabilities) > 4:
            return "task_specialist"
        else:
            return best_type
    
    def _generate_agent_config(
        self, 
        description: str, 
        capabilities: List[str], 
        domain: str, 
        personality: str,
        agent_type: str
    ) -> Dict[str, Any]:
        """
        生成智能体配置
        
        Args:
            description: 智能体描述
            capabilities: 能力列表
            domain: 领域
            personality: 人格类型
            agent_type: 智能体类型
            
        Returns:
            智能体配置字典
        """
        personality_config = self.personality_types[personality]
        
        agent_config = {
            'id': f"agent_{str(uuid.uuid4())[:8]}",
            'role': description,
            'domain': domain,
            'agent_type': agent_type,
            'capabilities': self._validate_and_enhance_capabilities(capabilities),
            'instructions': self._generate_instructions(description, personality_config, domain),
            'personality': {
                'type': personality,
                'name': personality_config['name'],
                'traits': personality_config['traits'],
                'style': personality_config['style']
            },
            'interaction_guidelines': self._generate_interaction_guidelines(personality_config),
            'scope_limitations': self._generate_scope_limitations(agent_type, domain),
            'success_metrics': self._generate_success_metrics(capabilities, domain)
        }
        
        return agent_config
    
    def _validate_and_enhance_capabilities(self, capabilities: List[str]) -> List[str]:
        """
        验证和增强能力列表
        
        Args:
            capabilities: 原始能力列表
            
        Returns:
            验证和增强后的能力列表
        """
        # 标准化能力名称
        enhanced_caps = []
        
        for cap in capabilities:
            # 检查是否匹配已知能力类别
            matched = False
            for category, category_caps in self.available_capabilities.items():
                if any(cat.lower() in cap.lower() for cat in category_caps):
                    enhanced_caps.extend([c for c in category_caps if c.lower() in cap.lower()])
                    matched = True
                    break
            
            if not matched:
                # 保持原能力名称
                enhanced_caps.append(cap)
        
        # 去重并排序
        unique_caps = list(set(enhanced_caps))
        
        # 如果能力太少，添加一些基础能力
        if len(unique_caps) < 3:
            basic_caps = ["Task execution", "Information retrieval", "Basic communication"]
            unique_caps.extend([cap for cap in basic_caps if cap not in unique_caps])
        
        return unique_caps[:15]  # 限制最大能力数量
    
    def _generate_instructions(
        self, 
        description: str, 
        personality_config: Dict[str, str], 
        domain: str
    ) -> str:
        """
        生成智能体指令
        
        Args:
            description: 智能体描述
            personality_config: 人格配置
            domain: 领域
            
        Returns:
            生成的指令文本
        """
        base_instruction = f"You are acting as a {description} in the {domain} domain. "
        
        # 根据人格添加特性指导
        personality_guidance = f"Your personality is {personality_config['traits']}. {personality_config['style']} "
        
        # 添加职责说明
        role_instruction = "Your primary function is to assist with tasks related to your role. "
        
        # 添加通用指导原则
        general_guidelines = (
            "Be helpful, professional, and stay within your defined capabilities. "
            "Provide clear, accurate, and relevant information. "
            "Ask for clarification when needed to ensure you fully understand requirements."
        )
        
        return base_instruction + personality_guidance + role_instruction + general_guidelines
    
    def _generate_interaction_guidelines(self, personality_config: Dict[str, str]) -> List[str]:
        """
        生成交互指导原则
        
        Args:
            personality_config: 人格配置
            
        Returns:
            交互指导原则列表
        """
        guidelines = [
            f"Maintain {personality_config['traits']} throughout interactions",
            f"Communicate using {personality_config['style']}",
            "Be consistent in responses and behavior",
            "Adapt communication style based on user preferences",
            "Focus on providing value and achieving user goals"
        ]
        
        return guidelines
    
    def _generate_scope_limitations(self, agent_type: str, domain: str) -> List[str]:
        """
        生成范围限制
        
        Args:
            agent_type: 智能体类型
            domain: 领域
            
        Returns:
            范围限制列表
        """
        limitations = [
            "Operate within defined domain expertise",
            "Do not provide information outside knowledge scope",
            "Maintain professional boundaries",
            "Escalate issues beyond capability to human experts"
        ]
        
        # 根据智能体类型添加特定限制
        if agent_type == "domain_expert":
            limitations.extend([
                "Focus primarily on deep domain knowledge",
                "Avoid giving advice in unrelated domains"
            ])
        elif agent_type == "task_specialist":
            limitations.extend([
                "Concentrate on specific task completion",
                "Do not expand scope beyond defined tasks"
            ])
        elif agent_type == "role_assistant":
            limitations.extend([
                "Act within defined role boundaries",
                "Do not overstep assistant responsibilities"
            ])
        
        return limitations
    
    def _generate_success_metrics(self, capabilities: List[str], domain: str) -> List[str]:
        """
        生成成功指标
        
        Args:
            capabilities: 能力列表
            domain: 领域
            
        Returns:
            成功指标列表
        """
        metrics = [
            "Response relevance and accuracy",
            "Task completion efficiency",
            "User satisfaction and clarity",
            "Information quality and reliability"
        ]
        
        # 根据能力添加特定指标
        if any("programming" in cap.lower() for cap in capabilities):
            metrics.extend(["Code quality and best practices compliance"])
        
        if any("communication" in cap.lower() for cap in capabilities):
            metrics.extend(["Communication clarity and effectiveness"])
        
        if any("analysis" in cap.lower() for cap in capabilities):
            metrics.extend(["Insight depth and analytical accuracy"])
        
        return metrics[:8]  # 限制指标数量
    
    def _calculate_agent_quality(
        self, 
        agent_config: Dict[str, Any], 
        capabilities: List[str]
    ) -> Dict[str, Any]:
        """
        计算智能体质量指标
        
        Args:
            agent_config: 智能体配置
            capabilities: 能力列表
            
        Returns:
            质量指标字典
        """
        # 能力覆盖度评分
        capability_score = min(1.0, len(capabilities) / 8.0)  # 8个能力为满分
        
        # 领域专精度评分
        domain_score = 0.8  # 基础分
        if agent_config['domain'] != 'general':
            domain_score = 0.9
        
        # 人格一致性评分
        personality_score = 0.85  # 基础分
        if agent_config.get('personality') in self.personality_types:
            personality_score = 1.0
        
        # 指令完整性评分
        instructions = agent_config.get('instructions', '')
        instruction_score = min(1.0, len(instructions) / 200.0)  # 200字符为满分
        
        # 计算综合质量评分
        weights = {'capability': 0.3, 'domain': 0.25, 'personality': 0.2, 'instruction': 0.25}
        overall_score = (
            capability_score * weights['capability'] +
            domain_score * weights['domain'] +
            personality_score * weights['personality'] +
            instruction_score * weights['instruction']
        )
        
        return {
            'capability_coverage': round(capability_score, 3),
            'domain_specialization': round(domain_score, 3),
            'personality_consistency': round(personality_score, 3),
            'instruction_completeness': round(instruction_score, 3),
            'overall_quality': round(overall_score, 3),
            'effectiveness': round(min(1.0, overall_score * 1.1), 3)
        }
    
    def _generate_usage_recommendations(
        self, 
        agent_config: Dict[str, Any], 
        agent_type: str
    ) -> List[str]:
        """
        生成使用建议
        
        Args:
            agent_config: 智能体配置
            agent_type: 智能体类型
            
        Returns:
            使用建议列表
        """
        recommendations = [
            "Deploy agent in appropriate domain context",
            "Monitor agent performance regularly",
            "Update capabilities based on usage patterns",
            "Provide clear task definitions for best results"
        ]
        
        # 根据智能体类型添加特定建议
        if agent_type == "domain_expert":
            recommendations.extend([
                "Use for specialized knowledge tasks",
                "Combine with general assistants for broader coverage"
            ])
        elif agent_type == "task_specialist":
            recommendations.extend([
                "Assign specific, well-defined tasks",
                "Monitor task completion quality metrics"
            ])
        elif agent_type == "role_assistant":
            recommendations.extend([
                "Use for ongoing support roles",
                "Maintain consistent interaction patterns"
            ])
        
        return recommendations[:6]  # 限制建议数量
    
    def _determine_complexity(self, capabilities: List[str]) -> str:
        """
        确定智能体复杂度
        
        Args:
            capabilities: 能力列表
            
        Returns:
            复杂度级别
        """
        cap_count = len(capabilities)
        
        if cap_count <= 4:
            return "simple"
        elif cap_count <= 8:
            return "medium"
        else:
            return "complex"
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.utcnow().isoformat()


# 创建技能实例
agent_creator_skill = AgentCreatorSkill()

# 导出Lambda处理器（符合AgentSkills.io标准）
def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Lambda处理器入口点"""
    return agent_creator_skill.lambda_handler(event, context)

# 导出技能实例（用于注册）
def get_skill():
    """获取技能实例"""
    return agent_creator_skill