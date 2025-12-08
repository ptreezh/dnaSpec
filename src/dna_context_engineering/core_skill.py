"""
Core Skills Base Class
DNASPEC Context Engineering Skills 的核心基类
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .ai_client import AIModelClient
from .instruction_template import TemplateRegistry


class SkillResult:
    """技能执行结果"""
    
    def __init__(self, success: bool, data: Dict[str, Any], error: str = None, 
                 execution_time: float = 0.0, confidence: float = 0.0):
        self.success = success
        self.data = data or {}
        self.error = error
        self.execution_time = execution_time
        self.confidence = confidence
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'success': self.success,
            'data': self.data,
            'error': self.error,
            'execution_time': self.execution_time,
            'confidence': self.confidence
        }


class ContextEngineeringSkill(ABC):
    """上下文工程技能基类"""
    
    def __init__(self, name: str, description: str, 
                 ai_client: AIModelClient, 
                 template_registry: TemplateRegistry):
        self.name = name
        self.description = description
        self.ai_client = ai_client
        self.template_registry = template_registry
        self.stats = {
            'executions': 0,
            'successes': 0,
            'failures': 0,
            'total_execution_time': 0.0
        }
    
    @abstractmethod
    def execute(self, context: str, params: Dict[str, Any] = None) -> SkillResult:
        """执行技能的核心方法"""
        pass
    
    def _construct_instruction(self, template_name: str, context: str, 
                             params: Dict[str, Any] = None) -> str:
        """使用模板构造指令"""
        return self.template_registry.create_prompt(template_name, context, params)
    
    def _send_to_ai_and_parse(self, instruction: str, template_name: str) -> SkillResult:
        """发送指令到AI并解析响应"""
        import time
        start_time = time.time()
        
        try:
            # 发送指令到AI
            response = self.ai_client.send_instruction(instruction)
            
            # 解析AI响应
            parsed_result = self.template_registry.parse_response(template_name, response)
            
            execution_time = time.time() - start_time
            
            # 更新统计信息
            self.stats['executions'] += 1
            self.stats['successes'] += 1
            self.stats['total_execution_time'] += execution_time
            
            # 计算置信度（这里简单基于响应长度，实际可更复杂）
            confidence = min(1.0, len(response) / 1000)
            
            return SkillResult(
                success=True,
                data=parsed_result,
                execution_time=execution_time,
                confidence=confidence
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # 更新统计信息
            self.stats['executions'] += 1
            self.stats['failures'] += 1
            self.stats['total_execution_time'] += execution_time
            
            return SkillResult(
                success=False,
                data={},
                error=str(e),
                execution_time=execution_time,
                confidence=0.0
            )
    
    def get_stats(self) -> Dict[str, Any]:
        """获取技能执行统计信息"""
        stats_copy = self.stats.copy()
        if stats_copy['executions'] > 0:
            stats_copy['avg_execution_time'] = (
                stats_copy['total_execution_time'] / stats_copy['executions']
            )
            stats_copy['success_rate'] = (
                stats_copy['successes'] / stats_copy['executions'] * 100
            )
        else:
            stats_copy['avg_execution_time'] = 0.0
            stats_copy['success_rate'] = 0.0
        
        return stats_copy
    
    def reset_stats(self):
        """重置统计信息"""
        self.stats = {
            'executions': 0,
            'successes': 0,
            'failures': 0,
            'total_execution_time': 0.0
        }
    
    def validate_input(self, context: str, params: Dict[str, Any] = None) -> Optional[str]:
        """验证输入参数"""
        if not context or len(context.strip()) == 0:
            return "Context cannot be empty"
        
        if len(context) > 10000:  # 限制上下文长度
            return "Context is too long (max 10000 characters)"
        
        return None


class ContextAnalysisSkill(ContextEngineeringSkill):
    """上下文分析技能"""
    
    def __init__(self, ai_client: AIModelClient, template_registry: TemplateRegistry):
        super().__init__(
            name="context-analysis",
            description="分析上下文质量的五维指标",
            ai_client=ai_client,
            template_registry=template_registry
        )
    
    def execute(self, context: str, params: Dict[str, Any] = None) -> SkillResult:
        """执行上下文分析"""
        # 验证输入
        validation_error = self.validate_input(context, params)
        if validation_error:
            return SkillResult(success=False, data={}, error=validation_error)
        
        # 设置默认参数
        if params is None:
            params = {}
        
        # 构造分析指令
        instruction = self._construct_instruction("context-analysis", context, params)
        
        # 发送至AI并解析结果
        return self._send_to_ai_and_parse(instruction, "context-analysis")


class ContextOptimizationSkill(ContextEngineeringSkill):
    """上下文优化技能"""
    
    def __init__(self, ai_client: AIModelClient, template_registry: TemplateRegistry):
        super().__init__(
            name="context-optimization", 
            description="优化上下文内容的技能",
            ai_client=ai_client,
            template_registry=template_registry
        )
    
    def execute(self, context: str, params: Dict[str, Any] = None) -> SkillResult:
        """执行上下文优化"""
        # 验证输入
        validation_error = self.validate_input(context, params)
        if validation_error:
            return SkillResult(success=False, data={}, error=validation_error)
        
        # 设置默认参数
        if params is None:
            params = {}
        
        # 构造优化指令
        instruction = self._construct_instruction("context-optimization", context, params)
        
        # 发送至AI并解析结果
        return self._send_to_ai_and_parse(instruction, "context-optimization")


class CognitiveTemplateSkill(ContextEngineeringSkill):
    """认知模板应用技能"""
    
    def __init__(self, ai_client: AIModelClient, template_registry: TemplateRegistry):
        super().__init__(
            name="cognitive-template",
            description="应用认知模板的技能", 
            ai_client=ai_client,
            template_registry=template_registry
        )
    
    def execute(self, context: str, params: Dict[str, Any] = None) -> SkillResult:
        """执行认知模板应用"""
        # 验证输入
        validation_error = self.validate_input(context, params)
        if validation_error:
            return SkillResult(success=False, data={}, error=validation_error)
        
        # 设置默认参数
        if params is None:
            params = {}
        
        # 构造认知模板指令
        instruction = self._construct_instruction("cognitive-template", context, params)
        
        # 发送至AI并解析结果
        return self._send_to_ai_and_parse(instruction, "cognitive-template")


class SkillsManager:
    """技能管理器"""
    
    def __init__(self, ai_client: AIModelClient, template_registry: TemplateRegistry):
        self.ai_client = ai_client
        self.template_registry = template_registry
        self.skills = {
            'context-analysis': ContextAnalysisSkill(ai_client, template_registry),
            'context-optimization': ContextOptimizationSkill(ai_client, template_registry),
            'cognitive-template': CognitiveTemplateSkill(ai_client, template_registry)
        }
    
    def register_skill(self, skill_name: str, skill_instance: 'ContextEngineeringSkill') -> bool:
        """注册新技能"""
        if skill_name in self.skills:
            return False  # 技能已存在
        
        self.skills[skill_name] = skill_instance
        return True
    
    def execute_skill(self, skill_name: str, context: str, params: Dict[str, Any] = None) -> SkillResult:
        """执行指定技能"""
        if skill_name not in self.skills:
            available_skills = list(self.skills.keys())
            return SkillResult(
                success=False,
                data={},
                error=f"Skill '{skill_name}' not found. Available: {available_skills}"
            )
        
        skill = self.skills[skill_name]
        return skill.execute(context, params)
    
    def list_skills(self) -> Dict[str, str]:
        """列出所有可用技能"""
        return {name: skill.description for name, skill in self.skills.items()}
    
    def get_skill_stats(self, skill_name: str) -> Dict[str, Any]:
        """获取指定技能的统计信息"""
        if skill_name not in self.skills:
            return {}
        
        skill = self.skills[skill_name]
        return skill.get_stats()