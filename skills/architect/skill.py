"""
DNASPEC Architect Skill - 符合AgentSkills.io标准
基于TDD实现，遵循KISS、SOLID、YAGNI原则
"""
import json
import uuid
from typing import Dict, Any, List, Optional
from skills.dnaspec_skill_framework import (
    DNASpecSkillBase, 
    track_execution,
    create_quality_metrics,
    create_architecture_mapping,
    match_architecture_type,
    validate_text_input,
    SkillValidationError
)


@track_execution
class ArchitectSkill(DNASpecSkillBase):
    """
    架构师技能 - 系统架构设计和分析
    
    符合AgentSkills.io规范：
    - name: architect
    - description: System architecture design and analysis tool
    - 提供架构模式识别、质量评估、架构生成功能
    """
    
    def __init__(self):
        super().__init__(
            name="architect",
            description="System architecture design and analysis tool that creates structured architecture diagrams and evaluates system quality. Use when user mentions architecture, system design, technical structure, or needs help organizing system components.",
            version="2.0.0"
        )
        
        # 支持的架构模式
        self.supported_patterns = [
            "microservices", "monolithic", "event-driven", 
            "layered", "serverless", "custom"
        ]
        
        # 架构组件映射
        self.component_mapping = {
            "用户认证": ["Auth Service", "User Database", "Session Store"],
            "商品管理": ["Product Service", "Product Database", "Image Storage"],
            "订单处理": ["Order Service", "Order Database", "Payment Integration"],
            "支付": ["Payment Service", "Payment Gateway", "Transaction Database"],
            "用户管理": ["User Service", "User Database", "Profile Storage"],
            "电商": ["Web Frontend", "API Gateway", "Microservices", "Database"],
            "博客": ["Web Application", "Content Database", "Comment System"],
            "实时系统": ["Data Ingestion", "Processing Engine", "Output Stream"],
            "api": ["API Gateway", "Backend Services", "Data Layer"]
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证输入数据
        
        Args:
            input_data: 包含系统需求或描述的输入数据
            
        Returns:
            验证结果字典
        """
        # 验证必需字段
        if 'input' not in input_data:
            return {
                'valid': False, 
                'error': 'Missing required field: input'
            }
        
        # 验证输入内容
        input_validation = validate_text_input(input_data['input'], 'input')
        if not input_validation['valid']:
            return input_validation
        
        # 验证可选字段
        optional_fields = ['architecture_style', 'complexity', 'scale']
        for field in optional_fields:
            if field in input_data and input_data[field] is not None:
                if field == 'complexity' and isinstance(input_data[field], str):
                    if input_data[field].lower() not in ['simple', 'medium', 'complex']:
                        return {
                            'valid': False,
                            'error': f'Invalid complexity level: {input_data[field]}. Must be simple, medium, or complex.'
                        }
        
        return {'valid': True}
    
    def execute_skill(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行架构设计技能核心逻辑
        
        Args:
            input_data: 验证过的输入数据
            
        Returns:
            架构设计结果
        """
        requirements = input_data['input']
        architecture_style = input_data.get('architecture_style', None)
        complexity = input_data.get('complexity', 'medium')
        scale = input_data.get('scale', 'medium')
        
        # 分析需求
        architecture_analysis = self._analyze_requirements(requirements)
        
        # 生成架构设计
        architecture_design = self._generate_architecture_design(
            requirements, architecture_analysis, architecture_style, complexity, scale
        )
        
        # 计算质量指标
        quality_metrics = self._calculate_quality_metrics(
            requirements, architecture_design, architecture_analysis
        )
        
        # 生成组件列表
        components = self._extract_components(architecture_design)
        
        # 生成建议
        recommendations = self._generate_recommendations(
            architecture_analysis, quality_metrics, complexity, scale
        )
        
        return {
            'architecture_type': architecture_analysis['type'],
            'design': architecture_design,
            'components': components,
            'context_quality': quality_metrics,
            'recommendations': recommendations,
            'analysis_metadata': {
                'complexity': complexity,
                'scale': scale,
                'confidence': architecture_analysis['confidence'],
                'matched_keywords': architecture_analysis['matched_keywords']
            }
        }
    
    def _analyze_requirements(self, requirements: str) -> Dict[str, Any]:
        """
        分析系统需求，识别架构模式和关键词
        
        Args:
            requirements: 系统需求描述
            
        Returns:
            分析结果
        """
        requirements_lower = requirements.lower()
        
        # 识别架构类型
        architecture_type = match_architecture_type(requirements)
        
        # 分析关键词匹配
        matched_keywords = []
        pattern_keywords = {
            'microservices': ['微服务', 'microservice', '分布式', 'distributed', '独立服务'],
            'monolithic': ['单体', 'monolithic', '统一架构', '集中式'],
            'event-driven': ['事件驱动', 'event-driven', '异步', 'asynchronous', '消息队列'],
            'layered': ['分层', 'layered', '多层', 'n-tier'],
            'serverless': ['无服务器', 'serverless', '函数', 'function', 'lambda']
        }
        
        for pattern, keywords in pattern_keywords.items():
            if any(keyword in requirements_lower for keyword in keywords):
                matched_keywords.append(pattern)
        
        # 计算置信度
        confidence = 0.5  # 基础置信度
        if architecture_type in self.component_mapping:
            confidence += 0.3
        
        # 根据关键词数量调整置信度
        confidence += min(0.2, len(matched_keywords) * 0.05)
        confidence = min(1.0, confidence)
        
        return {
            'type': architecture_type,
            'matched_keywords': matched_keywords,
            'confidence': round(confidence, 2)
        }
    
    def _generate_architecture_design(
        self, 
        requirements: str, 
        analysis: Dict[str, Any], 
        style: Optional[str], 
        complexity: str, 
        scale: str
    ) -> str:
        """
        生成架构设计
        
        Args:
            requirements: 系统需求
            analysis: 需求分析结果
            style: 指定的架构风格
            complexity: 复杂度级别
            scale: 系统规模
            
        Returns:
            架构设计字符串
        """
        # 如果用户指定了风格，优先使用
        if style and style.lower() in self.supported_patterns:
            architecture_type = style.lower()
        else:
            architecture_type = analysis['type']
        
        # 基础架构模板
        base_architectures = {
            'microservices': "[Frontend] -> [API Gateway] -> [Microservices] -> [Data Layer]",
            'monolithic': "[Web Application] -> [Business Logic] -> [Database]",
            'event-driven': "[Event Producers] -> [Event Bus] -> [Event Processors] -> [Data Stores]",
            'layered': "[Presentation Layer] -> [Business Logic Layer] -> [Data Access Layer] -> [Database]",
            'serverless': "[Client Apps] -> [API Gateway] -> [Functions] -> [Managed Services]"
        }
        
        # 获取基础架构
        if architecture_type in base_architectures:
            base_design = base_architectures[architecture_type]
        else:
            # 使用预定义的组件映射
            architecture_map = create_architecture_mapping()
            base_design = architecture_map.get(architecture_type, "[Custom Architecture]")
        
        # 根据复杂度调整设计
        if complexity == 'simple':
            # 简化设计，移除中间层
            if '-> [API Gateway] ->' in base_design:
                base_design = base_design.replace(' -> [API Gateway] ->', ' ->')
        
        elif complexity == 'complex':
            # 增加复杂度，添加中间件
            if '[Data Layer]' in base_design:
                base_design = base_design.replace('[Data Layer]', '[Cache Layer] -> [Data Layer]')
        
        # 根据规模调整
        if scale == 'large':
            # 添加负载均衡和集群
            if '[Frontend]' in base_design:
                base_design = base_design.replace('[Frontend]', '[Load Balancer] -> [Frontend Cluster]')
        
        return base_design
    
    def _calculate_quality_metrics(
        self, 
        requirements: str, 
        design: str, 
        analysis: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        计算架构质量指标
        
        Args:
            requirements: 需求描述
            design: 架构设计
            analysis: 需求分析结果
            
        Returns:
            质量指标字典
        """
        # 基础质量指标
        base_metrics = create_quality_metrics(requirements)
        
        # 根据架构特征调整指标
        design_features = design.lower()
        
        # 清晰度调整
        if len(design.split('->')) <= 4:  # 层次不过多
            base_metrics['clarity'] = min(1.0, base_metrics['clarity'] + 0.2)
        
        # 相关性调整
        if analysis['confidence'] > 0.8:
            base_metrics['relevance'] = min(1.0, base_metrics['relevance'] + 0.2)
        
        # 完整性调整
        if any(layer in design_features for layer in ['database', 'cache', 'security']):
            base_metrics['completeness'] = min(1.0, base_metrics['completeness'] + 0.1)
        
        # 一致性调整
        if design.count('[') == design.count(']'):  # 括号匹配
            base_metrics['consistency'] = min(1.0, base_metrics['consistency'] + 0.1)
        
        # 效率调整
        if len(design) < 200:  # 设计简洁
            base_metrics['efficiency'] = min(1.0, base_metrics['efficiency'] + 0.1)
        
        return base_metrics
    
    def _extract_components(self, design: str) -> List[Dict[str, Any]]:
        """
        从架构设计中提取组件列表
        
        Args:
            design: 架构设计字符串
            
        Returns:
            组件列表
        """
        import re
        
        # 提取方括号中的组件
        components = re.findall(r'\[([^\]]+)\]', design)
        
        component_list = []
        for i, component in enumerate(components):
            component_list.append({
                'id': f'component_{i+1}',
                'name': component,
                'type': self._classify_component(component),
                'layer': self._determine_layer(component, components)
            })
        
        return component_list
    
    def _classify_component(self, component: str) -> str:
        """分类组件类型"""
        component_lower = component.lower()
        
        if any(keyword in component_lower for keyword in ['frontend', 'web', 'ui', 'presentation']):
            return 'frontend'
        elif any(keyword in component_lower for keyword in ['api gateway', 'gateway', 'router']):
            return 'gateway'
        elif any(keyword in component_lower for keyword in ['service', 'business', 'logic']):
            return 'service'
        elif any(keyword in component_lower for keyword in ['database', 'db', 'data store']):
            return 'data'
        elif any(keyword in component_lower for keyword in ['cache', 'redis', 'memory']):
            return 'cache'
        elif any(keyword in component_lower for keyword in ['queue', 'bus', 'event']):
            return 'messaging'
        else:
            return 'infrastructure'
    
    def _determine_layer(self, component: str, all_components: List[str]) -> str:
        """确定组件所在层次"""
        component_index = all_components.index(component)
        total_components = len(all_components)
        
        if component_index == 0:
            return 'presentation'
        elif component_index == total_components - 1:
            return 'data'
        elif component_index < total_components // 2:
            return 'application'
        else:
            return 'integration'
    
    def _generate_recommendations(
        self, 
        analysis: Dict[str, Any], 
        quality_metrics: Dict[str, float], 
        complexity: str, 
        scale: str
    ) -> List[str]:
        """
        生成架构建议
        
        Args:
            analysis: 需求分析结果
            quality_metrics: 质量指标
            complexity: 复杂度级别
            scale: 系统规模
            
        Returns:
            建议列表
        """
        recommendations = []
        
        # 基于质量指标的建议
        if quality_metrics['clarity'] < 0.7:
            recommendations.append("Consider simplifying the architecture design for better clarity")
        
        if quality_metrics['completeness'] < 0.7:
            recommendations.append("Add more detailed components covering security, monitoring, and data validation")
        
        if quality_metrics['efficiency'] < 0.7:
            recommendations.append("Optimize the architecture for better performance and resource utilization")
        
        # 基于复杂度和规模的建议
        if complexity == 'simple' and scale == 'large':
            recommendations.append("Consider microservices architecture for large-scale systems")
        
        if complexity == 'complex' and scale == 'small':
            recommendations.append("Simplify the architecture for small systems to reduce maintenance overhead")
        
        # 基于分析置信度的建议
        if analysis['confidence'] < 0.7:
            recommendations.append("Provide more specific requirements for better architecture recommendations")
        
        # 基于架构类型的建议
        if analysis['type'] == 'custom':
            recommendations.append("Consider using established architecture patterns for better maintainability")
        
        # 确保至少有一条建议
        if not recommendations:
            recommendations.append("Architecture design looks good. Consider adding monitoring and logging components.")
        
        return recommendations


# 创建技能实例
architect_skill = ArchitectSkill()

# 导出Lambda处理器（符合AgentSkills.io标准）
def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Lambda处理器入口点"""
    return architect_skill.lambda_handler(event, context)

# 导出技能实例（用于注册）
def get_skill():
    """获取技能实例"""
    return architect_skill