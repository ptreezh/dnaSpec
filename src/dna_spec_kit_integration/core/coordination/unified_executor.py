"""
统一执行器模块
作为智能路由层，根据检测到的宪法机制决定使用协调模式还是独立模式执行技能
"""

import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from .constitution_detector import ConstitutionDetector, ConstitutionInfo, ConstitutionStatus
from .coordination_manager import CoordinationManager
from .graceful_degrader import GracefulDegrader, DegradationResult


class ExecutionMode(Enum):
    """执行模式枚举"""
    COORDINATED = "coordinated"
    INDEPENDENT = "independent"
    DEGRADED = "degraded"


class SkillRequest:
    """技能请求数据结构"""
    def __init__(self, skill_name: str, params: str, context: Dict[str, Any] = None):
        self.skill_name = skill_name
        self.params = params
        self.context = context or {}


@dataclass
class ExecutionContext:
    """执行上下文"""
    mode: ExecutionMode = ExecutionMode.INDEPENDENT
    constitution_detected: bool = False
    confidence_score: float = 0.0
    workflow_id: Optional[str] = None
    degradation_reason: Optional[str] = None
    coordination_metadata: Dict[str, Any] = field(default_factory=dict)


class UnifiedExecutor:
    """
    统一执行器
    智能路由层，根据检测到的宪法机制决定执行模式
    """
    
    def __init__(self):
        """初始化统一执行器"""
        self.constitution_detector = ConstitutionDetector()
        self.coordination_manager = CoordinationManager()
        self.graceful_degrader = GracefulDegrader()
        self.logger = logging.getLogger(__name__)
        
        # 性能统计
        self.execution_stats = {
            'total_requests': 0,
            'coordinated_executions': 0,
            'independent_executions': 0,
            'degraded_executions': 0,
            'coordination_failures': 0
        }
    
    def execute_skill(self, skill_request: SkillRequest) -> Dict[str, Any]:
        """
        执行技能的统一入口
        
        Args:
            skill_request: 技能请求
            
        Returns:
            执行结果
        """
        self.execution_stats['total_requests'] += 1
        self.logger.info(f"Executing skill: {skill_request.skill_name}")
        
        try:
            # 1. 检测宪法机制
            constitution_info = self.constitution_detector.detect_constitution()
            
            # 2. 决定执行模式
            execution_context = self._decide_execution_mode(skill_request, constitution_info)
            
            # 3. 根据模式执行
            if execution_context.mode == ExecutionMode.COORDINATED:
                return self._execute_coordinated(skill_request, execution_context)
            elif execution_context.mode == ExecutionMode.INDEPENDENT:
                return self._execute_independent(skill_request, execution_context)
            else:  # DEGRADED
                return self._execute_degraded(skill_request, execution_context)
                
        except Exception as e:
            self.logger.error(f"Execution failed: {str(e)}")
            self.execution_stats['coordination_failures'] += 1
            return self._create_error_response(skill_request, str(e))
    
    def execute_workflow(self, skill_requests: List[SkillRequest]) -> Dict[str, Any]:
        """
        执行技能工作流
        
        Args:
            skill_requests: 技能请求列表
            
        Returns:
            工作流执行结果
        """
        if not skill_requests:
            return self._create_error_response(None, "No skill requests provided")
        
        # 1. 检测宪法机制
        constitution_info = self.constitution_detector.detect_constitution()
        
        # 2. 决定执行模式
        execution_context = self._decide_workflow_execution_mode(skill_requests, constitution_info)
        
        # 3. 根据模式执行工作流
        if execution_context.mode == ExecutionMode.COORDINATED:
            return self._execute_coordinated_workflow(skill_requests, execution_context)
        else:
            return self._execute_independent_workflow(skill_requests, execution_context)
    
    def _decide_execution_mode(self, skill_request: SkillRequest, constitution_info: ConstitutionInfo) -> ExecutionContext:
        """决定单个技能的执行模式"""
        context = ExecutionContext()
        
        # 基于宪法状态决定是否推荐协调
        coordination_recommended = (
            constitution_info.status != ConstitutionStatus.NOT_CONFIGURED and
            constitution_info.confidence_score > 0.3
        )
        
        if coordination_recommended:
            context.constitution_detected = True
            context.confidence_score = constitution_info.confidence_score
            
            # 检查是否有工作流上下文
            if self._has_workflow_context(skill_request):
                context.mode = ExecutionMode.COORDINATED
                context.workflow_id = self._generate_workflow_id()
            else:
                context.mode = ExecutionMode.INDEPENDENT
        else:
            context.mode = ExecutionMode.INDEPENDENT
            
        return context
    
    def _decide_workflow_execution_mode(self, skill_requests: List[SkillRequest], constitution_info: ConstitutionInfo) -> ExecutionContext:
        """决定工作流的执行模式"""
        context = ExecutionContext()
        
        # 基于宪法状态决定是否推荐协调
        coordination_recommended = (
            constitution_info.status != ConstitutionStatus.NOT_CONFIGURED and
            constitution_info.confidence_score > 0.3 and
            len(skill_requests) > 1
        )
        
        if coordination_recommended:
            context.constitution_detected = True
            context.confidence_score = constitution_info.confidence_score
            context.mode = ExecutionMode.COORDINATED
            context.workflow_id = self._generate_workflow_id()
        else:
            context.mode = ExecutionMode.INDEPENDENT
            
        return context
    
    def _execute_coordinated(self, skill_request: SkillRequest, context: ExecutionContext) -> Dict[str, Any]:
        """执行协调模式"""
        self.execution_stats['coordinated_executions'] += 1
        
        try:
            # 创建工作流
            workflow = self.coordination_manager.create_workflow_from_request(skill_request, context.workflow_id)
            
            # 执行工作流
            result = self.coordination_manager.execute_workflow(workflow.workflow_id)
            
            return self._format_coordination_result(skill_request, result, context)
            
        except Exception as e:
            self.logger.warning(f"Coordination failed, degrading to independent mode: {str(e)}")
            self.execution_stats['coordination_failures'] += 1
            
            # 优雅降级到独立执行
            return self._execute_degraded(skill_request, context)
    
    def _execute_independent(self, skill_request: SkillRequest, context: ExecutionContext) -> Dict[str, Any]:
        """执行独立模式"""
        self.execution_stats['independent_executions'] += 1
        
        try:
            # 直接执行技能（使用现有的skill_executor）
            from ..skill_executor import SkillExecutor
            skill_executor = SkillExecutor()
            result = skill_executor.execute(skill_request.skill_name, skill_request.params)
            
            return self._format_independent_result(skill_request, result, context)
            
        except Exception as e:
            self.logger.error(f"Independent execution failed: {str(e)}")
            return self._create_error_response(skill_request, str(e))
    
    def _execute_degraded(self, skill_request: SkillRequest, context: ExecutionContext) -> Dict[str, Any]:
        """执行降级模式"""
        self.execution_stats['degraded_executions'] += 1
        
        try:
            # 使用优雅降级器
            degradation_result = self.graceful_degrader.execute_graceful_degradation(
                degradation_mode=self.graceful_degrader.DegradationMode.COORDINATION_FAILED,
                original_requests=[{
                    'skill_name': skill_request.skill_name,
                    'params': skill_request.params,
                    'context': skill_request.context
                }],
                coordination_context={'confidence_score': context.confidence_score}
            )
            
            return self._format_degradation_result(skill_request, degradation_result, context)
            
        except Exception as e:
            self.logger.error(f"Degraded execution failed: {str(e)}")
            return self._create_error_response(skill_request, str(e))
    
    def _execute_coordinated_workflow(self, skill_requests: List[SkillRequest], context: ExecutionContext) -> Dict[str, Any]:
        """执行协调工作流"""
        self.execution_stats['coordinated_executions'] += 1
        
        try:
            # 创建工作流
            workflow = self.coordination_manager.create_workflow_from_requests(skill_requests, context.workflow_id)
            
            # 执行工作流
            result = self.coordination_manager.execute_workflow(workflow.workflow_id)
            
            return self._format_coordination_result(None, result, context, workflow=True)
            
        except Exception as e:
            self.logger.warning(f"Coordinated workflow failed, degrading to independent mode: {str(e)}")
            self.execution_stats['coordination_failures'] += 1
            
            # 降级到独立执行
            return self._execute_independent_workflow(skill_requests, context)
    
    def _execute_independent_workflow(self, skill_requests: List[SkillRequest], context: ExecutionContext) -> Dict[str, Any]:
        """执行独立工作流"""
        self.execution_stats['independent_executions'] += 1
        
        results = []
        for skill_request in skill_requests:
            result = self._execute_independent(skill_request, context)
            results.append(result)
        
        return {
            'success': True,
            'mode': context.mode.value,
            'workflow_results': results,
            'context': {
                'constitution_detected': context.constitution_detected,
                'confidence_score': context.confidence_score
            }
        }
    
    def _format_coordination_result(self, skill_request: SkillRequest, workflow_result: Dict[str, Any], 
                                  context: ExecutionContext, workflow: bool = False) -> Dict[str, Any]:
        """格式化协调执行结果"""
        return {
            'success': workflow_result.get('success', False),
            'mode': context.mode.value,
            'coordination': {
                'workflow_id': context.workflow_id,
                'confidence_score': context.confidence_score,
                'execution_time': workflow_result.get('execution_time', 0),
                'resource_usage': workflow_result.get('resource_usage', {})
            },
            'results': workflow_result.get('results') if workflow_result.get('success') else None,
            'error': workflow_result.get('error') if not workflow_result.get('success') else None,
            'context': {
                'constitution_detected': context.constitution_detected,
                'workflow_type': 'coordinated'
            }
        }
    
    def _format_independent_result(self, skill_request: SkillRequest, result: Dict[str, Any], 
                                 context: ExecutionContext) -> Dict[str, Any]:
        """格式化独立执行结果"""
        return {
            'success': result.get('success', False),
            'mode': context.mode.value,
            'skill': skill_request.skill_name,
            'result': result.get('result', result.get('error', 'Unknown result')),
            'context': {
                'constitution_detected': context.constitution_detected,
                'workflow_type': 'independent'
            }
        }
    
    def _format_degradation_result(self, skill_request: SkillRequest, degradation_result: DegradationResult, 
                                 context: ExecutionContext) -> Dict[str, Any]:
        """格式化降级执行结果"""
        return {
            'success': degradation_result.success,
            'mode': context.mode.value,
            'skill': skill_request.skill_name,
            'result': degradation_result.result,
            'degradation': {
                'reason': degradation_result.degradation_reason,
                'fallback_strategy': degradation_result.fallback_strategy,
                'preserved_functionality': degradation_result.preserved_functionality
            },
            'context': {
                'constitution_detected': context.constitution_detected,
                'workflow_type': 'degraded'
            }
        }
    
    def _create_error_response(self, skill_request: Optional[SkillRequest], error: str) -> Dict[str, Any]:
        """创建错误响应"""
        return {
            'success': False,
            'mode': 'error',
            'skill': skill_request.skill_name if skill_request else None,
            'error': error,
            'context': {
                'execution_mode': 'error'
            }
        }
    
    def _has_workflow_context(self, skill_request: SkillRequest) -> bool:
        """检查是否有工作流上下文"""
        return skill_request.context.get('workflow_context', False) if skill_request.context else False
    
    def _generate_workflow_id(self) -> str:
        """生成工作流ID"""
        import time
        return f"workflow_{int(time.time() * 1000)}"
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """获取执行统计信息"""
        total = self.execution_stats['total_requests']
        if total > 0:
            self.execution_stats['coordination_success_rate'] = (
                self.execution_stats['coordinated_executions'] / total * 100
            )
            self.execution_stats['degradation_rate'] = (
                self.execution_stats['degraded_executions'] / total * 100
            )
        
        return self.execution_stats.copy()
    
    def reset_stats(self):
        """重置统计信息"""
        for key in self.execution_stats:
            if key != 'coordination_success_rate' and key != 'degradation_rate':
                self.execution_stats[key] = 0