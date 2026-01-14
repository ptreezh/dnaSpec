"""
协同契约检查器 - 在特定场景下调用钩子进行契约检查
"""
import threading
from typing import Dict, Any, Tuple, Callable
from datetime import datetime
from enum import Enum

from .common_state_manager import COMMON_STATE_MANAGER, StateUpdateType

class ContractViolation(Enum):
    """契约违规类型"""
    TEMP_FILE_COMMIT_VIOLATION = "temp_file_commit_violation"
    CONTEXT_CHAIN_BREAK = "context_chain_break"
    SECURITY_BYPASS = "security_bypass"
    STRUCTURE_INCONSISTENCY = "structure_inconsistency"
    WORKSPACE_COLLISION = "workspace_collision"
    QUALITY_DEGRADATION = "quality_degradation"

class CoordinationContractChecker:
    """协同契约检查器 - 负责在特定场景下调用钩子进行契约检查"""
    
    def __init__(self):
        self.state_manager = COMMON_STATE_MANAGER
        self.violation_log = []
        self.lock = threading.Lock()
        
        # 定义契约检查规则
        self.contract_rules = {
            "temp_file_management": {
                "description": "临时文件管理契约",
                "checker": self._check_temp_file_contract,
                "critical": True,  # 关键契约，违反则阻塞操作
                "auto_fix": True   # 是否支持自动修复
            },
            "context_chain_integrity": {
                "description": "上下文链完整性契约",
                "checker": self._check_context_chain_contract,
                "critical": True,
                "auto_fix": False
            },
            "security_constraint": {
                "description": "安全约束契约",
                "checker": self._check_security_contract,
                "critical": True,
                "auto_fix": False
            },
            "directory_structure_consistency": {
                "description": "目录结构一致性契约",
                "checker": self._check_directory_structure_contract,
                "critical": False,  # 靚性契约，违反则警告
                "auto_fix": True
            },
            "quality_maintenance": {
                "description": "质量维护契约",
                "checker": self._check_quality_contract,
                "critical": False,
                "auto_fix": False
            }
        }
    
    def check_contract_before_execution(self, skill_name: str, args: Dict[str, Any]) -> Tuple[bool, str]:
        """执行前契约检查"""
        with self.lock:
            violations = []
            
            for rule_name, rule_config in self.contract_rules.items():
                try:
                    is_compliant, message = rule_config["checker"](
                        skill_name=skill_name,
                        args=args,
                        phase="before"
                    )
                    
                    if not is_compliant:
                        violation_type = self._map_rule_to_violation_type(rule_name)
                        self._log_violation(violation_type, skill_name, message, "before")
                        
                        if rule_config["critical"]:
                            return False, f"❌ 关键契约违规: {message}"
                        else:
                            violations.append(message)
                
                except Exception as e:
                    self._log_internal_error("contract_check", f"契约检查异常: {str(e)}")
                    if rule_config["critical"]:
                        return False, f"❌ 契约检查系统错误: {str(e)}"
            
            if violations:
                return False, f"⚠️  靚性契约违规: {'; '.join(violations)}"
            
            return True, "✅ 契约检查通过"
    
    def check_contract_after_execution(self, skill_name: str, result: str, 
                                     original_args: Dict[str, Any] = None) -> str:
        """执行后契约检查"""
        with self.lock:
            for rule_name, rule_config in self.contract_rules.items():
                try:
                    is_compliant, message = rule_config["checker"](
                        skill_name=skill_name,
                        result=result,
                        original_args=original_args,
                        phase="after"
                    )
                    
                    if not is_compliant:
                        violation_type = self._map_rule_to_violation_type(rule_name)
                        self._log_violation(violation_type, skill_name, message, "after")
                        
                        if rule_config["critical"]:
                            # 关键契约违反，拒绝结果
                            return f"❌ 执行后契约检查失败: {message}\n原始结果已被拒绝"
                        
                        # 靚性契约违反，添加警告
                        result += f"\n⚠️  {message}"
                
                except Exception as e:
                    self._log_internal_error("post_contract_check", f"执行后契约检查异常: {str(e)}")
                    # 即使异常也不阻止结果返回
            
            return result
    
    def _check_temp_file_contract(self, skill_name: str, args: Dict[str, Any] = None, 
                                result: str = None, phase: str = "before") -> Tuple[bool, str]:
        """检查临时文件管理契约"""
        if skill_name in ["git_operations", "git_operations_constitutional"]:
            if phase == "before" and args:
                operation = args.get("operation", "")
                
                if operation in ["smart-commit", "commit-file", "add-commit"]:
                    # 检查是否试图提交临时文件
                    temp_files = set(self.state_manager.get_state("temp_workspace", "temp_files") or [])
                    
                    if temp_files:
                        return False, f"禁止提交仍在临时工作区的文件: {', '.join(list(temp_files)[:5])}{'...' if len(temp_files) > 5 else ''}"
            
            elif phase == "after" and result:
                # 检查执行结果是否提到临时文件处理
                if "临时文件" in result or "temp" in result.lower():
                    return True, ""
        
        # 检查临时工作区技能
        elif skill_name in ["temp_workspace", "temp_workspace_constitutional"]:
            if phase == "before":
                # 确保临时工作区操作与当前状态一致
                active_session = self.state_manager.get_state("temp_workspace", "active_session")
                session_arg = args.get("session_id") if args else None
                
                if session_arg and active_session and session_arg != active_session:
                    return False, f"工作区会话冲突: 当前会话 {active_session}, 请求会话 {session_arg}"
        
        return True, ""
    
    def _check_context_chain_contract(self, skill_name: str, args: Dict[str, Any] = None,
                                    result: str = None, phase: str = "before") -> Tuple[bool, str]:
        """检查上下文链完整性契约"""
        if skill_name in ["context_analysis", "context_analysis_constitutional"]:
            # 分析技能通常不需要检查，因为它们是链的起点
            return True, ""
        
        elif skill_name in ["context_optimization", "context_optimization_constitutional"]:
            if phase == "before":
                # 检查是否有上游分析结果
                current_analysis = self.state_manager.get_state("context_chain", "current_analysis")
                if not current_analysis:
                    return False, "上下文链断裂：缺少上游分析结果，无法执行优化"
        
        elif skill_name in ["cognitive_template", "cognitive_template_constitutional"]:
            if phase == "before":
                # 检查是否有上下文可用
                current_analysis = self.state_manager.get_state("context_chain", "current_analysis")
                context_arg = args.get("context") if args else None
                input_arg = args.get("input") if args else None
                
                if not any([current_analysis, context_arg, input_arg]):
                    return False, "无可用上下文：无法执行认知模板处理"
        
        return True, ""
    
    def _check_security_contract(self, skill_name: str, args: Dict[str, Any] = None,
                               result: str = None, phase: str = "before") -> Tuple[bool, str]:
        """检查安全约束契约"""
        try:
            from .constitutional_validator import validate_constitutional_compliance
        except ImportError:
            # 如果宪法验证器不可用，跳过安全检查
            return True, ""
        
        if phase == "before" and args:
            # 验证输入参数
            try:
                arg_str = str(args)
                validation = validate_constitutional_compliance(arg_str, "cognitive_convenience")
                if not validation["compliant"]:
                    return False, f"输入参数宪法验证失败: {validation['feedback']}"
            except Exception:
                # 验证失败时只记录，不阻止执行
                pass
        
        elif phase == "after" and result:
            # 验证执行结果
            try:
                validation = validate_constitutional_compliance(result, "all")
                if not validation["compliant"]:
                    return False, f"执行结果宪法验证失败: {validation['feedback']}"
            except Exception:
                # 验证失败时只记录，不阻止执行
                pass
        
        return True, ""
    
    def _check_directory_structure_contract(self, skill_name: str, args: Dict[str, Any] = None,
                                          result: str = None, phase: str = "before") -> Tuple[bool, str]:
        """检查目录结构一致性契约"""
        if skill_name in ["progressive_disclosure", "progressive_disclosure_constitutional",
                         "git_operations", "git_operations_constitutional"]:
            if phase == "after" and result:
                # 检查结果是否包含目录结构信息
                if any(keyword in result.lower() for keyword in ["structure", "directory", "folder", "path"]):
                    # 更新目录结构状态
                    self.state_manager.update_state("directory_structure", "last_verification_time", datetime.now().isoformat())
        
        return True, ""
    
    def _check_quality_contract(self, skill_name: str, args: Dict[str, Any] = None,
                              result: str = None, phase: str = "after") -> Tuple[bool, str]:
        """检查质量维护契约"""
        if phase == "after" and result:
            # 检查结果质量，例如长度、结构等
            if len(result.strip()) == 0:
                return False, "输出结果为空，质量不合格"
            
            if len(result) < 10 and skill_name not in ["liveness", "health_check"]:  # 假设存在健康检查技能
                return False, "输出结果过短，可能质量不合格"
        
        return True, ""
    
    def _map_rule_to_violation_type(self, rule_name: str) -> ContractViolation:
        """将规则名称映射到违规类型"""
        mapping = {
            "temp_file_management": ContractViolation.TEMP_FILE_COMMIT_VIOLATION,
            "context_chain_integrity": ContractViolation.CONTEXT_CHAIN_BREAK,
            "security_constraint": ContractViolation.SECURITY_BYPASS,
            "directory_structure_consistency": ContractViolation.STRUCTURE_INCONSISTENCY,
            "quality_maintenance": ContractViolation.QUALITY_DEGRADATION
        }
        return mapping.get(rule_name, ContractViolation.STRUCTURE_INCONSISTENCY)
    
    def _log_violation(self, violation_type: ContractViolation, skill_name: str, 
                      message: str, phase: str):
        """记录违约"""
        violation_record = {
            "timestamp": datetime.now().isoformat(),
            "violation_type": violation_type.value,
            "skill_name": skill_name,
            "message": message,
            "phase": phase
        }
        self.violation_log.append(violation_record)
        
        # 保持违约记录在合理大小
        if len(self.violation_log) > 500:
            self.violation_log = self.violation_log[-250:]  # 保持最近250条
    
    def _log_internal_error(self, checker_name: str, error_message: str):
        """记录内部错误"""
        error_record = {
            "timestamp": datetime.now().isoformat(),
            "checker": checker_name,
            "type": "internal_error",
            "message": error_message
        }
        self.violation_log.append(error_record)
    
    def get_violation_report(self) -> Dict[str, Any]:
        """获取违约报告"""
        with self.lock:
            total_violations = len([v for v in self.violation_log if v.get("type") != "internal_error"])
            return {
                "total_violations": total_violations,
                "violation_types": {
                    vt.name: len([v for v in self.violation_log 
                                if v.get('violation_type') == vt.value and v.get("type") != "internal_error"])
                    for vt in ContractViolation
                },
                "recent_violations": self.violation_log[-10:],  # 最近10条
                "critical_violations": len([v for v in self.violation_log 
                                          if v.get("type") != "internal_error" 
                                          and any(cv.name in v.get("message", "") for cv in [ContractViolation.TEMP_FILE_COMMIT_VIOLATION, ContractViolation.CONTEXT_CHAIN_BREAK, ContractViolation.SECURITY_BYPASS])])
            }

# 全局契约检查器实例
CONTRACT_CHECKER = CoordinationContractChecker()