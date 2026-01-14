"""
DNASPEC Skill Framework - 符合AgentSkills.io标准
基于TDD方法实现，遵循KISS、SOLID、YAGNI原则
"""
import json
import uuid
import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SkillValidationError(Exception):
    """技能验证错误"""
    pass


class SkillExecutionError(Exception):
    """技能执行错误"""
    pass


class DNASpecSkillBase(ABC):
    """DNASPEC技能基类 - 符合AgentSkills.io标准"""
    
    def __init__(self, name: str, description: str, version: str = "1.0.0"):
        """
        初始化技能
        
        Args:
            name: 技能名称（符合AgentSkills.io命名规范）
            description: 技能描述
            version: 技能版本
        """
        self.name = self._validate_skill_name(name)
        self.description = self._validate_description(description)
        self.version = version
        self.execution_id: Optional[str] = None
        self.start_time: Optional[float] = None
    
    def _validate_skill_name(self, name: str) -> str:
        """验证技能名称符合AgentSkills.io规范"""
        if not name:
            raise SkillValidationError("Skill name cannot be empty")
        
        if len(name) > 64:
            raise SkillValidationError("Skill name cannot exceed 64 characters")
        
        # 检查字符集：仅允许小写字母、数字和连字符
        import re
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
            raise SkillValidationError(
                "Skill name must contain only lowercase letters, numbers, and hyphens. "
                "Cannot start or end with hyphen, and no consecutive hyphens allowed."
            )
        
        return name
    
    def _validate_description(self, description: str) -> str:
        """验证技能描述符合AgentSkills.io规范"""
        if not description or not description.strip():
            raise SkillValidationError("Skill description cannot be empty")
        
        if len(description) > 1024:
            raise SkillValidationError("Skill description cannot exceed 1024 characters")
        
        return description.strip()
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证输入数据
        
        Args:
            input_data: 输入数据字典
            
        Returns:
            验证结果字典 {'valid': bool, 'error': str|null}
        """
        pass
    
    @abstractmethod
    def execute_skill(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行技能核心逻辑
        
        Args:
            input_data: 验证过的输入数据
            
        Returns:
            技能执行结果
        """
        pass
    
    def lambda_handler(self, event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
        """
        标准Lambda处理器 - 符合Claude Skills和AgentSkills.io格式
        
        Args:
            event: 包含inputs数组和tool_name的字典
            context: 上下文对象（可选）
            
        Returns:
            标准响应格式
        """
        self.start_time = time.time()
        self.execution_id = str(uuid.uuid4())
        
        try:
            # 记录开始
            self._log_execution_start()
            
            # 验证事件格式
            validation_result = self._validate_event_format(event)
            if not validation_result['valid']:
                return self._create_error_response(
                    f"Invalid event format: {validation_result['error']}", 
                    400
                )
            
            # 解析输入数据
            input_data = self._parse_input_data(event)
            
            # 验证输入
            input_validation = self.validate_input(input_data)
            if not input_validation.get('valid', True):
                return self._create_error_response(
                    f"Input validation failed: {input_validation.get('error', 'Unknown validation error')}", 
                    400
                )
            
            # 执行技能
            result = self.execute_skill(input_data)
            
            # 记录成功
            self._log_execution_success()
            
            return self._create_success_response(result)
            
        except SkillValidationError as e:
            self._log_execution_error(e)
            return self._create_error_response(f"Validation error: {str(e)}", 400)
        
        except SkillExecutionError as e:
            self._log_execution_error(e)
            return self._create_error_response(f"Execution error: {str(e)}", 500)
        
        except Exception as e:
            self._log_execution_error(e)
            return self._create_error_response(f"Internal error: {str(e)}", 500)
    
    def _validate_event_format(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """验证事件格式"""
        if not isinstance(event, dict):
            return {'valid': False, 'error': 'Event must be a dictionary'}
        
        if 'inputs' not in event:
            return {'valid': False, 'error': 'Missing inputs field'}
        
        inputs = event.get('inputs', [])
        if not inputs or not isinstance(inputs, list):
            return {'valid': False, 'error': 'Inputs must be a non-empty list'}
        
        if 'tool_name' not in event:
            return {'valid': False, 'error': 'Missing tool_name field'}
        
        return {'valid': True}
    
    def _parse_input_data(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """解析输入数据"""
        inputs = event.get('inputs', [])
        return inputs[0] if inputs else {}
    
    def _create_success_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """创建成功响应"""
        execution_time = time.time() - self.start_time if self.start_time else 0
        
        response_body = {
            'success': True,
            'result': result,
            'metadata': {
                'skill': self.name,
                'execution_id': self.execution_id,
                'timestamp': datetime.utcnow().isoformat(),
                'execution_time': round(execution_time, 3),
                'version': self.version
            }
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(response_body, ensure_ascii=False)
        }
    
    def _create_error_response(self, error_message: str, status_code: int = 500) -> Dict[str, Any]:
        """创建错误响应"""
        execution_time = time.time() - self.start_time if self.start_time else 0
        
        response_body = {
            'success': False,
            'error': error_message,
            'metadata': {
                'skill': self.name,
                'execution_id': self.execution_id,
                'timestamp': datetime.utcnow().isoformat(),
                'execution_time': round(execution_time, 3),
                'version': self.version
            }
        }
        
        return {
            'statusCode': status_code,
            'body': json.dumps(response_body, ensure_ascii=False)
        }
    
    def _log_execution_start(self) -> None:
        """记录执行开始"""
        logger.info(f"[{self.name}] Execution started: {self.execution_id}")
    
    def _log_execution_success(self) -> None:
        """记录执行成功"""
        execution_time = time.time() - self.start_time if self.start_time else 0
        logger.info(f"[{self.name}] Execution completed: {self.execution_id} in {execution_time:.3f}s")
    
    def _log_execution_error(self, error: Exception) -> None:
        """记录执行错误"""
        execution_time = time.time() - self.start_time if self.start_time else 0
        logger.error(f"[{self.name}] Execution failed: {self.execution_id} in {execution_time:.3f}s - {str(error)}")


class SkillRegistry:
    """技能注册表 - 管理所有可用的技能"""
    
    def __init__(self):
        self._skills: Dict[str, DNASpecSkillBase] = {}
    
    def register_skill(self, skill: DNASpecSkillBase) -> None:
        """注册技能"""
        self._skills[skill.name] = skill
        logger.info(f"Registered skill: {skill.name}")
    
    def get_skill(self, name: str) -> Optional[DNASpecSkillBase]:
        """获取技能"""
        return self._skills.get(name)
    
    def list_skills(self) -> List[str]:
        """列出所有技能名称"""
        return list(self._skills.keys())
    
    def get_all_skills(self) -> Dict[str, DNASpecSkillBase]:
        """获取所有技能"""
        return self._skills.copy()


class SkillMetrics:
    """技能性能指标收集器"""
    
    def __init__(self):
        self._metrics: Dict[str, Dict[str, Any]] = {}
    
    def record_execution(self, skill_name: str, execution_time: float, success: bool) -> None:
        """记录执行指标"""
        if skill_name not in self._metrics:
            self._metrics[skill_name] = {
                'total_executions': 0,
                'successful_executions': 0,
                'failed_executions': 0,
                'total_execution_time': 0.0,
                'avg_execution_time': 0.0,
                'min_execution_time': float('inf'),
                'max_execution_time': 0.0
            }
        
        metrics = self._metrics[skill_name]
        metrics['total_executions'] += 1
        metrics['total_execution_time'] += execution_time
        
        if success:
            metrics['successful_executions'] += 1
        else:
            metrics['failed_executions'] += 1
        
        metrics['avg_execution_time'] = metrics['total_execution_time'] / metrics['total_executions']
        metrics['min_execution_time'] = min(metrics['min_execution_time'], execution_time)
        metrics['max_execution_time'] = max(metrics['max_execution_time'], execution_time)
    
    def get_metrics(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """获取技能指标"""
        return self._metrics.get(skill_name)
    
    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        """获取所有技能指标"""
        return self._metrics.copy()


# 全局实例
skill_registry = SkillRegistry()
skill_metrics = SkillMetrics()


def register_skill(skill: DNASpecSkillBase) -> None:
    """注册技能的便捷函数"""
    skill_registry.register_skill(skill)


def get_skill(name: str) -> Optional[DNASpecSkillBase]:
    """获取技能的便捷函数"""
    return skill_registry.get_skill(name)


def record_skill_execution(skill_name: str, execution_time: float, success: bool) -> None:
    """记录技能执行指标的便捷函数"""
    skill_metrics.record_execution(skill_name, execution_time, success)


# 装饰器：自动记录技能执行指标
def track_execution(skill_class: DNASpecSkillBase):
    """装饰器：自动跟踪技能执行指标"""
    original_lambda_handler = skill_class.lambda_handler
    
    def tracked_lambda_handler(self, event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
        start_time = time.time()
        try:
            result = original_lambda_handler(self, event, context)
            success = result.get('statusCode', 500) < 400
            execution_time = time.time() - start_time
            record_skill_execution(self.name, execution_time, success)
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            record_skill_execution(self.name, execution_time, False)
            raise e
    
    skill_class.lambda_handler = tracked_lambda_handler
    return skill_class


# 辅助函数
def create_quality_metrics(text: str) -> Dict[str, float]:
    """
    创建标准质量指标
    
    Args:
        text: 要分析的文本
        
    Returns:
        5维质量指标字典
    """
    text_lower = text.lower()
    text_length = len(text)
    
    # 基于启发式规则计算质量指标
    clarity = min(1.0, max(0.0, 0.5 + text_length * 0.00001))
    
    relevance = min(1.0, max(0.0, 0.6 + (
        0.2 if any(kw in text_lower for kw in [
            'system', 'function', 'task', 'requirement', '系统', '功能', '任务', '需求'
        ]) else 0
    )))
    
    completeness = min(1.0, max(0.0, 0.3 + (
        0.4 if any(kw in text_lower for kw in [
            'constraint', 'goal', 'specification', '约束', '目标', '规范'
        ]) else 0
    )))
    
    consistency = min(1.0, max(0.0, 0.8 - (
        0.3 if any(kw in text_lower for kw in [
            'but', 'however', '但是', '然而', '矛盾'
        ]) else 0
    )))
    
    efficiency = min(1.0, max(0.0, 1.0 - text_length * 0.00005))
    
    return {
        'clarity': round(clarity, 3),
        'relevance': round(relevance, 3),
        'completeness': round(completeness, 3),
        'consistency': round(consistency, 3),
        'efficiency': round(efficiency, 3)
    }


def create_architecture_mapping() -> Dict[str, str]:
    """创建系统架构映射"""
    return {
        "电商": "[WebApp] -> [API Server] -> [Database]",
        "博客": "[WebApp] -> [Database]",
        "用户管理": "[Frontend] -> [API Gateway] -> [Auth Service] -> [User DB]",
        "认证": "[Auth Service] -> [User DB] -> [Session Store]",
        "微服务": "[API Gateway] -> [Microservices] -> [Data Layer]",
        "实时系统": "[Data Ingestion] -> [Processing Engine] -> [Output Stream]",
        "文件处理": "[Upload Handler] -> [Processing Queue] -> [Storage Service]",
        "api": "[API Gateway] -> [Microservices] -> [Data Layer]",
        "用户认证": "[Auth Service] -> [User Database] -> [Session Store]"
    }


def match_architecture_type(input_text: str) -> str:
    """
    匹配架构类型
    
    Args:
        input_text: 输入文本
        
    Returns:
        匹配的架构类型
    """
    text_lower = input_text.lower()
    architecture_map = create_architecture_mapping()
    
    for keyword, architecture in architecture_map.items():
        if keyword in text_lower:
            return keyword
    
    return "custom"


def generate_task_id() -> str:
    """生成任务ID"""
    return str(uuid.uuid4())[:8]


def generate_constraint_id() -> str:
    """生成约束ID"""
    return f"constraint_{str(uuid.uuid4())[:8]}"


def validate_text_input(text: str, field_name: str = "input") -> Dict[str, Any]:
    """
    验证文本输入
    
    Args:
        text: 要验证的文本
        field_name: 字段名称
        
    Returns:
        验证结果
    """
    if not isinstance(text, str):
        return {'valid': False, 'error': f'{field_name} must be a string'}
    
    if not text.strip():
        return {'valid': False, 'error': f'{field_name} cannot be empty'}
    
    if len(text) > 10000:  # 合理的最大长度限制
        return {'valid': False, 'error': f'{field_name} too long (max 10000 characters)'}
    
    return {'valid': True}


def validate_positive_integer(value: Any, field_name: str = "value") -> Dict[str, Any]:
    """
    验证正整数
    
    Args:
        value: 要验证的值
        field_name: 字段名称
        
    Returns:
        验证结果
    """
    try:
        int_value = int(value)
        if int_value <= 0:
            return {'valid': False, 'error': f'{field_name} must be positive'}
        if int_value > 10:  # 合理的最大深度限制
            return {'valid': False, 'error': f'{field_name} too large (max 10)'}
        return {'valid': True}
    except (ValueError, TypeError):
        return {'valid': False, 'error': f'{field_name} must be an integer'}