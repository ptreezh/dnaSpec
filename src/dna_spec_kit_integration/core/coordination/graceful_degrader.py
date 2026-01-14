"""
优雅降级器模块
负责在协调机制不可用时，提供优雅的降级到独立模式
"""
import traceback
import os
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import logging
import time

from .constitution_detector import ConstitutionDetector, ConstitutionStatus


class DegradationMode(Enum):
    """降级模式枚举"""
    COORDINATION_FAILED = "coordination_failed"    # 协调失败
    CONSTITUTION_MISSING = "constitution_missing"  # 宪法缺失
    SKILL_UNAVAILABLE = "skill_unavailable"       # 技能不可用
    RESOURCE_EXHAUSTED = "resource_exhausted"     # 资源耗尽
    CONFIGURATION_ERROR = "configuration_error"   # 配置错误


@dataclass
class DegradationResult:
    """降级结果数据类"""
    success: bool
    mode: str
    original_error: Optional[str] = None
    fallback_result: Optional[Dict[str, Any]] = None
    degraded_skills: List[str] = None
    performance_impact: Optional[str] = None
    recommendations: List[str] = None
    
    def __post_init__(self):
        if self.degraded_skills is None:
            self.degraded_skills = []
        if self.recommendations is None:
            self.recommendations = []


class GracefulDegrader:
    """
    优雅降级器
    负责在协调机制失败时，提供优雅的降级策略
    """
    
    def __init__(self, constitution_detector: ConstitutionDetector = None):
        """
        初始化优雅降级器
        
        Args:
            constitution_detector: 宪法检测器实例
        """
        self.constitution_detector = constitution_detector or ConstitutionDetector()
        self.logger = logging.getLogger(__name__)
        self.fallback_strategies: Dict[str, Callable] = {}
        self.performance_monitor = {}
        
        # 注册默认的降级策略
        self._register_default_strategies()
    
    def _register_default_strategies(self):
        """注册默认的降级策略"""
        self.fallback_strategies = {
            "single_skill_execution": self._execute_single_skill,
            "direct_skill_call": self._call_skill_directly,
            "basic_skill_wrapper": self._wrap_basic_skill,
            "minimal_skill_execution": self._minimal_skill_execution
        }
    
    def detect_degradation_need(self, 
                               coordination_attempt_result: Dict[str, Any],
                               skill_requests: List[Dict[str, Any]]) -> Optional[DegradationMode]:
        """
        检测是否需要降级
        
        Args:
            coordination_attempt_result: 协调尝试结果
            skill_requests: 技能请求列表
            
        Returns:
            Optional[DegradationMode]: 需要降级的模式，如果不需要降级返回None
        """
        # 检查协调是否成功
        if not coordination_attempt_result.get("success", False):
            error = coordination_attempt_result.get("error", "")
            if "constitution" in error.lower():
                return DegradationMode.CONSTITUTION_MISSING
            elif "skill" in error.lower():
                return DegradationMode.SKILL_UNAVAILABLE
            elif "resource" in error.lower() or "timeout" in error.lower():
                return DegradationMode.RESOURCE_EXHAUSTED
            else:
                return DegradationMode.COORDINATION_FAILED
        
        # 检查宪法状态
        constitution_info = self.constitution_detector.detect_constitution()
        if constitution_info.status == ConstitutionStatus.NOT_CONFIGURED:
            return DegradationMode.CONSTITUTION_MISSING
        
        # 检查技能可用性
        unavailable_skills = self._check_skill_availability(skill_requests)
        if unavailable_skills:
            return DegradationMode.SKILL_UNAVAILABLE
        
        return None
    
    def execute_graceful_degradation(self,
                                   degradation_mode: DegradationMode,
                                   original_requests: List[Dict[str, Any]],
                                   coordination_context: Dict[str, Any] = None) -> DegradationResult:
        """
        执行优雅降级
        
        Args:
            degradation_mode: 降级模式
            original_requests: 原始技能请求
            coordination_context: 协调上下文
            
        Returns:
            DegradationResult: 降级结果
        """
        start_time = time.time()
        
        try:
            if degradation_mode == DegradationMode.CONSTITUTION_MISSING:
                return self._handle_constitution_missing(original_requests, coordination_context)
            elif degradation_mode == DegradationMode.SKILL_UNAVAILABLE:
                return self._handle_skill_unavailable(original_requests, coordination_context)
            elif degradation_mode == DegradationMode.RESOURCE_EXHAUSTED:
                return self._handle_resource_exhausted(original_requests, coordination_context)
            elif degradation_mode == DegradationMode.CONFIGURATION_ERROR:
                return self._handle_configuration_error(original_requests, coordination_context)
            else:
                return self._handle_general_coordination_failure(original_requests, coordination_context)
        
        except Exception as e:
            self.logger.error(f"降级执行失败: {e}")
            return DegradationResult(
                success=False,
                mode=degradation_mode.value,
                original_error=str(e),
                performance_impact="high",
                recommendations=["检查系统配置", "重启协调服务"]
            )
    
    def _handle_constitution_missing(self,
                                   requests: List[Dict[str, Any]],
                                   context: Dict[str, Any] = None) -> DegradationResult:
        """处理宪法缺失的降级"""
        results = {}
        degraded_skills = []
        
        for request in requests:
            skill_name = request.get("skill_name")
            try:
                # 使用基础技能执行
                result = self._execute_single_skill(skill_name, request.get("input_data", {}))
                results[skill_name] = result
                degraded_skills.append(skill_name)
            except Exception as e:
                self.logger.warning(f"技能 {skill_name} 执行失败: {e}")
                results[skill_name] = {"error": str(e), "degraded": True}
                degraded_skills.append(skill_name)
        
        return DegradationResult(
            success=True,
            mode="constitution_missing_fallback",
            fallback_result=results,
            degraded_skills=degraded_skills,
            performance_impact="medium",
            recommendations=[
                "创建 PROJECT_CONSTITUTION.md 启用完整协调功能",
                "配置 .dnaspec 目录启用缓存和验证",
                "设置技能映射启用智能工作流"
            ]
        )
    
    def _handle_skill_unavailable(self,
                                requests: List[Dict[str, Any]],
                                context: Dict[str, Any] = None) -> DegradationResult:
        """处理技能不可用的降级"""
        results = {}
        degraded_skills = []
        available_count = 0
        
        for request in requests:
            skill_name = request.get("skill_name")
            
            # 检查技能是否可用
            if self._is_skill_available(skill_name):
                try:
                    result = self._execute_single_skill(skill_name, request.get("input_data", {}))
                    results[skill_name] = result
                    available_count += 1
                except Exception as e:
                    results[skill_name] = {"error": str(e), "degraded": True}
                    degraded_skills.append(skill_name)
            else:
                # 技能不可用，使用模拟结果
                results[skill_name] = self._generate_mock_result(skill_name)
                degraded_skills.append(skill_name)
        
        success = available_count > 0
        
        return DegradationResult(
            success=success,
            mode="skill_unavailable_fallback",
            fallback_result=results,
            degraded_skills=degraded_skills,
            performance_impact="low" if success else "high",
            recommendations=[
                "检查技能依赖和配置",
                "安装缺失的技能模块",
                "验证技能映射配置"
            ]
        )
    
    def _handle_resource_exhausted(self,
                                 requests: List[Dict[str, Any]],
                                 context: Dict[str, Any] = None) -> DegradationResult:
        """处理资源耗尽的降级"""
        # 资源耗尽时，限制并发执行，顺序处理
        results = {}
        degraded_skills = []
        
        # 限制并发数为1
        for i, request in enumerate(requests):
            skill_name = request.get("skill_name")
            try:
                # 添加延迟避免资源冲突
                if i > 0:
                    time.sleep(0.5)
                
                result = self._execute_single_skill(skill_name, request.get("input_data", {}))
                results[skill_name] = result
                degraded_skills.append(skill_name)
            except Exception as e:
                results[skill_name] = {"error": str(e), "degraded": True}
                degraded_skills.append(skill_name)
        
        return DegradationResult(
            success=True,
            mode="resource_limited_sequential",
            fallback_result=results,
            degraded_skills=degraded_skills,
            performance_impact="high",
            recommendations=[
                "增加系统资源",
                "优化技能执行效率",
                "启用缓存减少重复计算"
            ]
        )
    
    def _handle_configuration_error(self,
                                  requests: List[Dict[str, Any]],
                                  context: Dict[str, Any] = None) -> DegradationResult:
        """处理配置错误的降级"""
        # 配置错误时，使用最基础的技能执行
        results = {}
        degraded_skills = []
        
        for request in requests:
            skill_name = request.get("skill_name")
            try:
                # 使用最基础的执行方式
                result = self._minimal_skill_execution(skill_name, request.get("input_data", {}))
                results[skill_name] = result
                degraded_skills.append(skill_name)
            except Exception as e:
                results[skill_name] = {"error": str(e), "degraded": True}
                degraded_skills.append(skill_name)
        
        return DegradationResult(
            success=True,
            mode="configuration_error_fallback",
            fallback_result=results,
            degraded_skills=degraded_skills,
            performance_impact="medium",
            recommendations=[
                "检查配置文件格式",
                "验证技能映射配置",
                "重启系统加载正确配置"
            ]
        )
    
    def _handle_general_coordination_failure(self,
                                           requests: List[Dict[str, Any]],
                                           context: Dict[str, Any] = None) -> DegradationResult:
        """处理一般协调失败的降级"""
        results = {}
        degraded_skills = []
        
        for request in requests:
            skill_name = request.get("skill_name")
            try:
                result = self._execute_single_skill(skill_name, request.get("input_data", {}))
                results[skill_name] = result
                degraded_skills.append(skill_name)
            except Exception as e:
                # 最后的兜底方案
                results[skill_name] = {
                    "error": f"技能执行失败: {str(e)}",
                    "status": "failed",
                    "fallback": True
                }
                degraded_skills.append(skill_name)
        
        return DegradationResult(
            success=True,
            mode="general_fallback",
            fallback_result=results,
            degraded_skills=degraded_skills,
            performance_impact="high",
            recommendations=[
                "检查协调服务状态",
                "重启协调管理器",
                "联系技术支持"
            ]
        )
    
    def _execute_single_skill(self, skill_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行单个技能"""
        # 尝试动态导入和执行技能
        skill_impl = self._get_skill_implementation(skill_name)
        
        if skill_impl is None:
            # 技能不可用，返回模拟结果
            return self._generate_mock_result(skill_name)
        
        try:
            if hasattr(skill_impl, 'execute'):
                return skill_impl.execute(**input_data)
            elif hasattr(skill_impl, '_execute_skill_logic'):
                return skill_impl._execute_skill_logic(**input_data)
            else:
                return {"error": f"技能 {skill_name} 没有可执行的接口"}
                
        except Exception as e:
            return {"error": f"技能执行异常: {str(e)}"}
    
    def _call_skill_directly(self, skill_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """直接调用技能"""
        return self._execute_single_skill(skill_name, input_data)
    
    def _wrap_basic_skill(self, skill_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """包装基础技能"""
        # 添加基础的错误处理和日志
        try:
            result = self._execute_single_skill(skill_name, input_data)
            self.logger.info(f"技能 {skill_name} 执行成功")
            return result
        except Exception as e:
            self.logger.error(f"技能 {skill_name} 执行失败: {e}")
            return {"error": str(e), "wrapped": True}
    
    def _minimal_skill_execution(self, skill_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """最小化技能执行"""
        # 最基础的实现，只返回基本信息
        return {
            "skill_name": skill_name,
            "status": "executed_minimal",
            "input_data": input_data,
            "message": "最小化执行模式",
            "timestamp": time.time()
        }
    
    def _generate_mock_result(self, skill_name: str) -> Dict[str, Any]:
        """生成模拟结果"""
        return {
            "skill_name": skill_name,
            "status": "mock_result",
            "message": f"技能 {skill_name} 当前不可用，返回模拟结果",
            "timestamp": time.time(),
            "mock": True
        }
    
    def _get_skill_implementation(self, skill_name: str):
        """获取技能实现"""
        # 简化的技能映射
        skill_mappings = {
            "architect": "DNASPECSystemArchitect",
            "system-architect": "DNASPECSystemArchitect",
            "task-decomposer": "TaskDecomposer",
            "constraint-generator": "ConstraintGenerator",
            "api-checker": "APIChecker",
            "modulizer": "Modulizer",
            "context-analyzer": "ContextAnalyzer",
            "context-optimizer": "ContextOptimizer",
            "cognitive-templater": "CognitiveTemplater",
            "agent-creator": "AgentCreator",
            "cache-manager": "CacheManager",
            "git-operations": "GitOperations"
        }
        
        target_class = skill_mappings.get(skill_name)
        if not target_class:
            return None
        
        # 尝试动态导入
        try:
            if target_class == "DNASPECSystemArchitect":
                import importlib.util
                spec = importlib.util.spec_from_file_location("system_architect", 
                    os.path.join(os.path.dirname(__file__), "..", "..", "..", "spec-kit", "skills", "dna-system-architect", "scripts", "system_architect_designer.py"))
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    return module.DNASPECSystemArchitect()
            elif target_class == "TaskDecomposer":
                import importlib.util
                spec = importlib.util.spec_from_file_location("task_decomposer", 
                    os.path.join(os.path.dirname(__file__), "..", "..", "..", "spec-kit", "skills", "dna-task-decomposer", "scripts", "task_decomposer.py"))
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    return module.TaskDecomposer()
        except (ImportError, AttributeError, FileNotFoundError):
            pass
        
        return None
    
    def _is_skill_available(self, skill_name: str) -> bool:
        """检查技能是否可用"""
        skill_impl = self._get_skill_implementation(skill_name)
        return skill_impl is not None
    
    def _check_skill_availability(self, requests: List[Dict[str, Any]]) -> List[str]:
        """检查技能可用性"""
        unavailable = []
        for request in requests:
            skill_name = request.get("skill_name")
            if not self._is_skill_available(skill_name):
                unavailable.append(skill_name)
        return unavailable
    
    def register_fallback_strategy(self, name: str, strategy: Callable):
        """注册自定义降级策略"""
        self.fallback_strategies[name] = strategy
    
    def get_degradation_statistics(self) -> Dict[str, Any]:
        """获取降级统计信息"""
        return {
            "registered_strategies": list(self.fallback_strategies.keys()),
            "constitution_status": self.constitution_detector.detect_constitution().status.value,
            "monitoring_active": len(self.performance_monitor) > 0
        }