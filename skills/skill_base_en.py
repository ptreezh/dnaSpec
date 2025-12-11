"""
DNASPEC Skill Base Class
Provides standardized skill interface and progressive disclosure support
"""
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import time
from enum import Enum


class DetailLevel(Enum):
    """Detail Level Enumeration"""
    BASIC = "basic"
    STANDARD = "standard"
    DETAILED = "detailed"


class ValidationError(Exception):
    """Validation Error Exception"""
    pass


class BaseSkill(ABC):
    """DNASPEC Skill Base Class"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.version = "1.0.0"
    
    def execute(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Skill - Standardized Entry Point
        
        Args:
            args: Standardized input parameters
                - input: Main input content
                - detail_level: Detail level ("basic", "standard", "detailed")
                - options: Optional configuration parameters
                - context: Context information
                
        Returns:
            Standardized output response
        """
        start_time = time.time()
        
        try:
            # Validate input parameters
            validated_args = self._validate_input(args)
            input_text = validated_args["input"]
            detail_level = validated_args["detail_level"]
            options = validated_args["options"]
            context = validated_args["context"]
            
            # Execute skill logic
            result_data = self._execute_skill_logic(
                input_text, detail_level, options, context
            )
            
            # Format output result
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
        Validate Input Parameters
        
        Args:
            args: Input parameter dictionary
            
        Returns:
            Validated parameter dictionary
            
        Raises:
            ValidationError: When input parameters are invalid
        """
        # Validate required parameters
        input_text = args.get("input", "")
        if not isinstance(input_text, str):
            raise ValidationError("Input must be a string")
        
        if not input_text.strip():
            raise ValidationError("Input cannot be empty")
        
        # Process detail level parameter
        detail_level_str = args.get("detail_level", "standard")
        try:
            detail_level = DetailLevel(detail_level_str)
        except ValueError:
            # If not a valid DetailLevel, use default value
            detail_level = DetailLevel.STANDARD
        
        # Process optional parameters
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
        Execute Specific Skill Logic - Subclasses Must Implement
        
        Args:
            input_text: Input text
            detail_level: Detail level
            options: Optional configuration parameters
            context: Context information
            
        Returns:
            Skill execution result
        """
        pass
    
    def _format_output(self, result_data: Any, detail_level: DetailLevel) -> Any:
        """
        Format Output Result Based on Detail Level
        
        Args:
            result_data: Skill execution result
            detail_level: Detail level
            
        Returns:
            Formatted result
        """
        # Default implementation directly returns result data
        # Subclasses can override this method to support progressive disclosure
        return result_data
    
    def _calculate_confidence(self, input_text: str) -> float:
        """
        Calculate Result Confidence
        
        Args:
            input_text: Input text
            
        Returns:
            Confidence score (0.0-1.0)
        """
        # Default implementation calculates confidence based on input length
        if len(input_text) < 10:
            return 0.3
        elif len(input_text) < 50:
            return 0.6
        else:
            return 0.8