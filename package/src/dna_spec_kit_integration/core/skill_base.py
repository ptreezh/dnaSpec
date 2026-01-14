"""
DNASPEC技能基类
提供标准化的技能接口和渐进式信息披露支持
"""
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import time
from enum import Enum


class DetailLevel(Enum):
    """详细程度枚举"""
    BASIC = "basic"
    STANDARD = "standard"
    DETAILED = "detailed"


class ValidationError(Exception):
    """验证错误异常"""
    pass


class BaseSkill(ABC):
    """DNASPEC技能基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.version = "1.0.0"
    
    def execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行技能 - 标准化入口点
        
        Args:
            args: 标准化输入参数
                - input: 主要输入内容
                - detail_level: 详细程度 ("basic", "standard", "detailed")
                - options: 可选配置参数
                - context: 上下文信息
                
        Returns:
            标准化输出响应
        """
        start_time = time.time()
        
        try:
            # 验证输入参数
            validated_args = self._validate_input(args)
            input_text = validated_args["input"]
            detail_level = validated_args["detail_level"]
            options = validated_args["options"]
            context = validated_args["context"]
            
            # 执行技能逻辑
            result_data = self._execute_skill_logic(
                input_text, detail_level, options, context
            )
            
            # 格式化输出结果
            formatted_result = self._format_output(
                result_data, detail_level
            )
            
            execution_time = time.time() - start_time
            
            return {
                "status": "success",
                "data": formatted_result,
                "metadata": {
                    "skill_name": self.name,
                    "execution_time": execution_time,
                    "confidence": self._calculate_confidence(input_text),
                    "detail_level": detail_level.value if isinstance(detail_level, DetailLevel) else detail_level
                }
            }
            
        except ValidationError as e:
            execution_time = time.time() - start_time
            return {
                "status": "error",
                "error": {
                    "type": "VALIDATION_ERROR",
                    "message": str(e),
                    "code": "INVALID_INPUT"
                },
                "metadata": {
                    "skill_name": self.name,
                    "execution_time": execution_time
                }
            }
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "status": "error",
                "error": {
                    "type": type(e).__name__,
                    "message": str(e),
                    "code": "EXECUTION_ERROR"
                },
                "metadata": {
                    "skill_name": self.name,
                    "execution_time": execution_time
                }
            }
    
    def _validate_input(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证输入参数
        
        Args:
            args: 输入参数字典
            
        Returns:
            验证后的参数字典
            
        Raises:
            ValidationError: 当输入参数无效时
        """
        # 验证必需参数
        input_text = args.get("input", "")
        if not isinstance(input_text, str):
            raise ValidationError("Input must be a string")
        
        if not input_text.strip():
            raise ValidationError("Input cannot be empty")
        
        # 处理详细程度参数
        detail_level_str = args.get("detail_level", "standard")
        try:
            detail_level = DetailLevel(detail_level_str)
        except ValueError:
            # 如果不是有效的DetailLevel，使用默认值
            detail_level = DetailLevel.STANDARD
        
        # 处理可选参数
        options = args.get("options", {})
        if not isinstance(options, dict):
            options = {}
        
        context = args.get("context", {})
        if not isinstance(context, dict):
            context = {}
        
        return {
            "input": input_text,
            "detail_level": detail_level,
            "options": options,
            "context": context
        }
    
    @abstractmethod
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                           options: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """
        执行具体的技能逻辑 - 子类必须实现
        
        Args:
            input_text: 输入文本
            detail_level: 详细程度
            options: 可选配置参数
            context: 上下文信息
            
        Returns:
            技能执行结果
        """
        pass
    
    def _format_output(self, result_data: Any, detail_level: DetailLevel) -> Any:
        """
        根据详细程度格式化输出结果
        
        Args:
            result_data: 技能执行结果
            detail_level: 详细程度
            
        Returns:
            格式化后的结果
        """
        # 默认实现直接返回结果数据
        # 子类可以根据需要重写此方法以支持渐进式信息披露
        return result_data
    
    def _calculate_confidence(self, input_text: str) -> float:
        """
        计算结果置信度
        
        Args:
            input_text: 输入文本
            
        Returns:
            置信度分数 (0.0-1.0)
        """
        # 默认实现基于输入长度计算置信度
        if len(input_text) < 10:
            return 0.3
        elif len(input_text) < 50:
            return 0.6
        else:
            return 0.8