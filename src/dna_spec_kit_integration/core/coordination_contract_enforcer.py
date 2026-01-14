"""
协同契约执行器 - 将契约检查集成到技能执行流程中
"""
import os
import sys
from pathlib import Path
import importlib.util
from typing import Dict, Any, Callable
from datetime import datetime

from .common_state_manager import COMMON_STATE_MANAGER, StateUpdateType
from .coordination_contract_checker import CONTRACT_CHECKER

class CoordinationContractEnforcer:
    """协同契约执行器 - 将契约检查集成到技能执行流程"""
    
    def __init__(self):
        self.state_manager = COMMON_STATE_MANAGER
        self.contract_checker = CONTRACT_CHECKER
        self.enhanced_skills = {}
        self.skill_execution_stats = {}
        
        # 需要强制协同的技能类型
        self.contractual_skills = {
            'temp_workspace', 'temp_workspace_constitutional',
            'context_analysis', 'context_optimization', 'cognitive_template',
            'context_analysis_constitutional', 'context_optimization_constitutional', 
            'cognitive_template_constitutional',
            'git_operations', 'git_operations_constitutional',
            'progressive_disclosure', 'progressive_disclosure_constitutional',
            'system_architect', 'system_architect_constitutional',
            'agent_creator_independent', 'agent_creator_constitutional'
        }
    
    def enforce_contract_on_skill_execution(self, skill_name: str, args: Dict[str, Any]) -> str:
        """在技能执行时强制执行契约"""
        
        # 1. 执行前契约检查
        is_allowed, pre_check_msg = self.contract_checker.check_contract_before_execution(skill_name, args)
        if not is_allowed:
            return pre_check_msg
        
        # 2. 根据技能类型确定执行策略
        if skill_name in self.contractual_skills:
            # 需要契约的技能，通过增强执行器执行
            result = self._execute_contractual_skill(skill_name, args)
        else:
            # 普通技能，直接执行
            result = self._execute_normal_skill(skill_name, args)
        
        # 3. 执行后契约检查
        final_result = self.contract_checker.check_contract_after_execution(skill_name, result, args)
        
        # 4. 更新执行统计
        self._update_execution_stats(skill_name, result)
        
        return final_result
    
    def _execute_contractual_skill(self, skill_name: str, args: Dict[str, Any]) -> str:
        """执行需要契约的技能"""
        try:
            # 加载技能模块
            skills_path = Path(__file__).parent.parent / "skills"
            skill_file = skills_path / f"{skill_name}.py"
            
            # 尝试寻找宪法级变体
            if not skill_file.exists():
                constitutional_variants = [
                    f"{skill_name}_constitutional.py",
                    f"{skill_name}_constitutational.py", 
                    f"{skill_name}_const.py",
                    f"constitutional_{skill_name}.py"
                ]
                
                found = False
                for variant in constitutional_variants:
                    variant_path = skills_path / variant
                    if variant_path.exists():
                        skill_file = variant_path
                        found = True
                        break
                
                if not found:
                    return f"❌ 技能文件不存在: {skill_name}"
            
            # 动态加载和执行
            spec = importlib.util.spec_from_file_location(skill_name, skill_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if not hasattr(module, 'execute'):
                return f"❌ 技能模块缺少execute函数: {skill_name}"
            
            # 执行技能
            result = module.execute(args)
            
            # 更新状态
            self._update_state_based_on_skill_execution(skill_name, args, result)
            
            return result
            
        except Exception as e:
            error_msg = f"❌ 技能执行异常: {str(e)}"
            # 记录异常到状态
            self.state_manager.increment_counter("security", "violation_count")
            return error_msg
    
    def _execute_normal_skill(self, skill_name: str, args: Dict[str, Any]) -> str:
        """执行普通技能"""
        try:
            # 同样需要加载和执行，但不做额外契约检查
            skills_path = Path(__file__).parent.parent / "skills"
            skill_file = skills_path / f"{skill_name}.py"
            
            # 尝试寻找宪法级变体
            if not skill_file.exists():
                constitutional_variants = [
                    f"{skill_name}_constitutional.py",
                    f"{skill_name}_constitutational.py", 
                    f"{skill_name}_const.py",
                    f"constitutional_{skill_name}.py"
                ]
                
                found = False
                for variant in constitutional_variants:
                    variant_path = skills_path / variant
                    if variant_path.exists():
                        skill_file = variant_path
                        found = True
                        break
                
                if not found:
                    return f"❌ 技能文件不存在: {skill_name}"
            
            # 动态加载和执行
            spec = importlib.util.spec_from_file_location(skill_name, skill_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if not hasattr(module, 'execute'):
                return f"❌ 技能模块缺少execute函数: {skill_name}"
            
            # 执行技能
            result = module.execute(args)
            
            # 即使是普通技能，也可以选择性地更新状态
            if skill_name in ["liveness", "health_check"]:  # 示例技能
                self.state_manager.update_state("workspace_state", "last_access_time", 
                                               datetime.now().isoformat())
            
            return result
            
        except Exception as e:
            return f"❌ 技能执行异常: {str(e)}"
    
    def _update_state_based_on_skill_execution(self, skill_name: str, args: Dict[str, Any], result: str):
        """根据技能执行结果更新状态"""
        try:
            # 临时文件管理技能
            if skill_name in ['temp_workspace', 'temp_workspace_constitutional']:
                if 'operation' in args:
                    operation = args['operation']
                    if operation == 'add-file':
                        file_path = args.get('file_path', 'unknown')
                        self.state_manager.append_to_list("temp_workspace", "temp_files", file_path)
                    elif operation == 'confirm-file':
                        file_path = args.get('confirm_file', 'unknown')
                        self.state_manager.remove_from_list("temp_workspace", "temp_files", file_path)
                        self.state_manager.append_to_list("temp_workspace", "confirmed_files", file_path)
                    elif operation == 'create-workspace':
                        session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                        self.state_manager.update_state("temp_workspace", "active_session", session_id)
                        self.state_manager.update_state("temp_workspace", "session_start_time", datetime.now().isoformat())
            
            # 上下文分析技能
            elif skill_name in ['context_analysis', 'context_analysis_constitutional']:
                # 更新上下文链状态
                if result and '分析结果' in result:
                    self.state_manager.update_state("context_chain", "current_analysis", {
                        "result": result,
                        "timestamp": datetime.now().isoformat(),
                        "context_id": args.get('context', '')[:50]  # 使用前50个字符作为ID
                    })
                    self.state_manager.append_to_list("context_chain", "analysis_history", {
                        "timestamp": datetime.now().isoformat(),
                        "result_summary": result[:100] + "..." if len(result) > 100 else result
                    })
            
            # 上下文优化技能
            elif skill_name in ['context_optimization', 'context_optimization_constitutional']:
                # 更新优化标志
                optimization_flag = f"optimized_{datetime.now().isoformat()}"
                self.state_manager.append_to_list("context_chain", "optimization_flags", optimization_flag)
            
            # Git操作技能
            elif skill_name in ['git_operations', 'git_operations_constitutional']:
                if 'operation' in args:
                    operation = args['operation']
                    if operation in ['smart-commit', 'commit-file', 'add-commit']:
                        # 更新Git操作计数
                        self.state_manager.increment_counter("security", "git_operations_count")
            
            # 记录执行时间
            execution_time = datetime.now().isoformat()
            self.state_manager.update_state("performance_metrics", f"last_execution_{skill_name}", execution_time)
            
        except Exception as e:
            print(f"⚠️  更新状态失败: {str(e)}")
    
    def _update_execution_stats(self, skill_name: str, result: str):
        """更新执行统计"""
        if skill_name not in self.skill_execution_stats:
            self.skill_execution_stats[skill_name] = {
                "execution_count": 0,
                "success_count": 0,
                "failure_count": 0,
                "last_execution": None,
                "average_execution_time": None
            }
        
        stats = self.skill_execution_stats[skill_name]
        stats["execution_count"] += 1
        stats["last_execution"] = datetime.now().isoformat()
        
        if result and not result.startswith("❌"):
            stats["success_count"] += 1
        else:
            stats["failure_count"] += 1
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """获取执行摘要"""
        total_executions = sum(stat["execution_count"] for stat in self.skill_execution_stats.values())
        total_successes = sum(stat["success_count"] for stat in self.skill_execution_stats.values())
        
        success_rate = (total_successes / total_executions * 100) if total_executions > 0 else 100.0
        
        return {
            "total_executions": total_executions,
            "total_successes": total_successes,
            "success_rate": success_rate,
            "contractual_violations": len(self.contract_checker.violation_log),
            "active_skills": list(self.skill_execution_stats.keys()),
            "state_integrity": self.state_manager.check_integrity()
        }

# 全局契约执行器实例
CONTRACT_ENFORCER = CoordinationContractEnforcer()