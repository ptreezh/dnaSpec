"""
DNASPEC核心模块
提供技能管理和集成功能
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class SkillStatus(Enum):
    """技能状态"""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class SkillInfo:
    """技能信息"""
    name: str
    description: str
    version: str = "1.0.0"
    author: str = "DNASPEC System"
    keywords: List[str] = None
    confidence: float = 0.0
    execution_time: float = 0.0
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []


@dataclass
class SkillResult:
    """技能执行结果"""
    skill_name: str
    status: SkillStatus
    result: Any
    confidence: float
    execution_time: float
    error_message: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class DNASpecSkill:
    """DNASPEC技能基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.version = "1.0.0"
        self.created_time = __import__('time').time()
    
    def process_request(self, request: str, context: Dict[str, Any] = None) -> SkillResult:
        """处理请求"""
        import time
        start_time = time.time()
        
        try:
            # 执行具体的技能逻辑
            result_data = self._execute_skill_logic(request, context or {})
            execution_time = time.time() - start_time
            
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.COMPLETED,
                result=result_data,
                confidence=self._calculate_confidence(request),
                execution_time=execution_time,
                metadata={
                    "processed_at": time.time(),
                    "request_length": len(request)
                }
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.ERROR,
                result=None,
                confidence=0.0,
                execution_time=execution_time,
                error_message=str(e),
                metadata={
                    "processed_at": time.time(),
                    "error_type": type(e).__name__
                }
            )
    
    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """执行具体的技能逻辑 - 子类需要实现"""
        raise NotImplementedError("子类必须实现 _execute_skill_logic 方法")
    
    def _calculate_confidence(self, request: str) -> float:
        """计算匹配置信度"""
        # 简单的默认实现
        return 0.8
    
    def get_skill_info(self) -> Dict[str, Any]:
        """获取技能信息"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version
        }