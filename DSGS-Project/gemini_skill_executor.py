#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DSGS技能执行引擎
负责实际执行技能并管理执行过程
"""

import sys
import os
import time
import json
import importlib
from typing import Dict, Any, Optional

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gemini_skills_core import get_skill_manager, SkillResult, SkillStatus

class SkillExecutionEngine:
    """技能执行引擎"""
    
    def __init__(self):
        self.skill_manager = get_skill_manager()
        self.execution_history = []
        self.debug_mode = False
    
    def execute_skill(self, skill_name: str, request: str, context: Dict[str, Any] = None) -> SkillResult:
        """执行技能"""
        start_time = time.time()
        
        if self.debug_mode:
            print(f"[DEBUG] 开始执行技能: {skill_name}")
        
        try:
            # 首先尝试获取已注册的技能实例
            skill = self.skill_manager.get_skill(skill_name)
            
            if skill:
                # 使用已注册的技能实例执行
                result = skill.process_request(request, context or {})
                execution_time = time.time() - start_time
                
                if self.debug_mode:
                    print(f"[DEBUG] 技能执行完成: {skill_name} (耗时: {execution_time:.3f}s)")
                
                # 记录执行历史
                self._record_execution(skill_name, request, result, execution_time)
                return result
            else:
                # 如果没有注册的实例，尝试动态导入并执行
                result = self._execute_dynamic_skill(skill_name, request, context or {})
                execution_time = time.time() - start_time
                
                # 记录执行历史
                self._record_execution(skill_name, request, result, execution_time)
                return result
                
        except Exception as e:
            execution_time = time.time() - start_time
            error_result = SkillResult(
                skill_name=skill_name,
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
            
            if self.debug_mode:
                print(f"[DEBUG] 技能执行错误: {skill_name} - {str(e)}")
            
            # 记录执行历史
            self._record_execution(skill_name, request, error_result, execution_time)
            return error_result
    
    def _execute_dynamic_skill(self, skill_name: str, request: str, context: Dict[str, Any]) -> SkillResult:
        """动态执行技能"""
        start_time = time.time()
        
        if self.debug_mode:
            print(f"[DEBUG] 动态执行技能: {skill_name}")
        
        try:
            # 根据技能名称动态导入相应的模块
            if skill_name == "dsgs-agent-creator":
                from .src.dsgs_agent_creator import agent_creator
                result = agent_creator.process_request(request, context)
            elif skill_name == "dsgs-task-decomposer":
                # 任务分解器可能需要特殊处理
                result = self._execute_task_decomposer(request, context)
            elif skill_name == "dsgs-dapi-checker":
                from .src.dsgs_dapi_checker import dapi_checker
                result = dapi_checker.process_request(request, context)
            elif skill_name == "dsgs-modulizer":
                from .src.dsgs_modulizer import modulizer
                result = modulizer.process_request(request, context)
            elif skill_name == "dsgs-constraint-generator":
                result = self._execute_constraint_generator(request, context)
            elif skill_name == "dsgs-architect":
                result = self._execute_architect(request, context)
            else:
                # 通用执行逻辑
                result = {
                    "skill": skill_name,
                    "status": "executed",
                    "message": f"技能 {skill_name} 已执行",
                    "request": request
                }
            
            execution_time = time.time() - start_time
            
            return SkillResult(
                skill_name=skill_name,
                status=SkillStatus.COMPLETED,
                result=result,
                confidence=0.9,
                execution_time=execution_time,
                metadata={
                    "processed_at": time.time(),
                    "execution_method": "dynamic"
                }
            )
            
        except ImportError as e:
            execution_time = time.time() - start_time
            if self.debug_mode:
                print(f"[DEBUG] 技能模块导入失败: {skill_name} - {str(e)}")
            
            # 返回通用执行结果
            return self._execute_generic_skill(skill_name, request, context, execution_time)
            
        except Exception as e:
            execution_time = time.time() - start_time
            if self.debug_mode:
                print(f"[DEBUG] 技能执行异常: {skill_name} - {str(e)}")
            
            return SkillResult(
                skill_name=skill_name,
                status=SkillStatus.ERROR,
                result=None,
                confidence=0.0,
                execution_time=execution_time,
                error_message=str(e),
                metadata={
                    "processed_at": time.time(),
                    "error_type": type(e).__name__,
                    "execution_method": "dynamic"
                }
            )
    
    def _execute_task_decomposer(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行任务分解器"""
        # 这里应该导入实际的任务分解器
        # 暂时返回模拟结果
        return {
            "skill": "dsgs-task-decomposer",
            "status": "completed",
            "message": f"任务分解器已处理请求: {request}",
            "tasks": [
                {"id": "T001", "name": "需求分析", "status": "pending"},
                {"id": "T002", "name": "架构设计", "status": "pending"},
                {"id": "T003", "name": "编码实现", "status": "pending"}
            ],
            "dependencies": ["T001->T002", "T002->T003"]
        }
    
    def _execute_constraint_generator(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行约束生成器"""
        return {
            "skill": "dsgs-constraint-generator",
            "status": "completed",
            "message": f"约束生成器已处理请求: {request}",
            "constraints": [
                "数据格式约束",
                "接口规范约束",
                "性能约束"
            ]
        }
    
    def _execute_architect(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行架构师技能"""
        return {
            "skill": "dsgs-architect",
            "status": "completed",
            "message": f"架构师已处理请求: {request}",
            "architecture": {
                "layers": ["表现层", "业务逻辑层", "数据访问层"],
                "patterns": ["MVC", "微服务"],
                "technologies": ["React", "Node.js", "MongoDB"]
            }
        }
    
    def _execute_generic_skill(self, skill_name: str, request: str, context: Dict[str, Any], execution_time: float) -> SkillResult:
        """执行通用技能"""
        return SkillResult(
            skill_name=skill_name,
            status=SkillStatus.COMPLETED,
            result={
                "skill": skill_name,
                "status": "executed",
                "message": f"通用执行器已处理技能: {skill_name}",
                "request": request
            },
            confidence=0.5,  # 通用执行置信度较低
            execution_time=execution_time,
            metadata={
                "processed_at": time.time(),
                "execution_method": "generic"
            }
        )
    
    def _record_execution(self, skill_name: str, request: str, result: SkillResult, execution_time: float):
        """记录执行历史"""
        self.execution_history.append({
            "skill_name": skill_name,
            "request": request,
            "result_status": result.status.name,
            "execution_time": execution_time,
            "timestamp": time.time()
        })
        
        # 保持历史记录在合理范围内
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-50:]
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """获取执行统计信息"""
        if not self.execution_history:
            return {"total_executions": 0}
        
        total_executions = len(self.execution_history)
        successful_executions = len([h for h in self.execution_history if h["result_status"] == "COMPLETED"])
        failed_executions = total_executions - successful_executions
        
        avg_execution_time = sum(h["execution_time"] for h in self.execution_history) / total_executions
        
        # 按技能统计
        skill_stats = {}
        for record in self.execution_history:
            skill_name = record["skill_name"]
            if skill_name not in skill_stats:
                skill_stats[skill_name] = {"total": 0, "successful": 0, "failed": 0, "total_time": 0.0}
            
            skill_stats[skill_name]["total"] += 1
            if record["result_status"] == "COMPLETED":
                skill_stats[skill_name]["successful"] += 1
            else:
                skill_stats[skill_name]["failed"] += 1
            skill_stats[skill_name]["total_time"] += record["execution_time"]
        
        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "success_rate": successful_executions / total_executions if total_executions > 0 else 0,
            "average_execution_time": avg_execution_time,
            "skill_statistics": skill_stats
        }
    
    def enable_debug(self):
        """启用调试模式"""
        self.debug_mode = True
    
    def disable_debug(self):
        """禁用调试模式"""
        self.debug_mode = False

# 全局执行引擎实例
execution_engine = SkillExecutionEngine()

def get_execution_engine() -> SkillExecutionEngine:
    """获取全局执行引擎"""
    return execution_engine

if __name__ == "__main__":
    # 测试技能执行引擎
    print("=== DSGS技能执行引擎测试 ===")
    
    engine = get_execution_engine()
    engine.enable_debug()
    
    test_cases = [
        ("dsgs-agent-creator", "创建一个项目管理智能体"),
        ("dsgs-task-decomposer", "分解用户注册功能的开发任务"),
        ("dsgs-dapi-checker", "检查用户服务API接口一致性"),
        ("dsgs-modulizer", "对订单处理模块进行成熟度评估"),
        ("dsgs-architect", "设计微服务系统架构")
    ]
    
    for skill_name, request in test_cases:
        print(f"\n测试技能: {skill_name}")
        print(f"请求: {request}")
        
        result = engine.execute_skill(skill_name, request)
        
        if result.status == SkillStatus.COMPLETED:
            print(f"执行成功 (耗时: {result.execution_time:.3f}s)")
            if isinstance(result.result, dict) and "message" in result.result:
                print(f"结果: {result.result['message']}")
        else:
            print(f"执行失败: {result.error_message}")
    
    # 显示统计信息
    stats = engine.get_execution_stats()
    print(f"\n执行统计:")
    print(f"  总执行次数: {stats['total_executions']}")
    print(f"  成功次数: {stats['successful_executions']}")
    print(f"  失败次数: {stats['failed_executions']}")
    print(f"  成功率: {stats['success_rate']:.2%}")
    print(f"  平均执行时间: {stats['average_execution_time']:.3f}s")
