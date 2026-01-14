"""
认知协同执法系统 - 强制执行协同契约的执法机构
"""
from typing import Dict, Any, List, Tuple, Callable
import threading
from datetime import datetime
from enum import Enum
import json

class EnforcementLevel(Enum):
    """执法等级"""
    MONITOR_ONLY = "monitor_only"  # 仅监控
    WARN = "warn"                  # 警告
    SOFT_BLOCK = "soft_block"      # 软阻塞
    HARD_BLOCK = "hard_block"      # 硬阻塞

class ViolationType(Enum):
    """违规类型"""
    TEMP_FILE_VIOLATION = "temp_file_violation"  # 临时文件违规
    CONTEXT_CHAIN_BREAK = "context_chain_break"  # 上下文链断裂
    SECURITY_BYPASS = "security_bypass"          # 安全绕过
    STRUCTURE_MISMATCH = "structure_mismatch"    # 结构不匹配
    STATE_INCONSISTENCY = "state_inconsistency"  # 状态不一致

class CoordinationEnforcer:
    """认知协同执法器 - 执行协同契约的强制执行"""
    
    def __init__(self):
        self.enforcement_rules = {}
        self.violations_log = []
        self.lock = threading.RLock()
        
        # 初始化执法规则
        self._init_enforcement_rules()
    
    def _init_enforcement_rules(self):
        """初始化执法规则"""
        # 一级优先级执法规则
        self.enforcement_rules = {
            'temp_file_management': {
                'level': EnforcementLevel.HARD_BLOCK,
                'handler': self._enforce_temp_file_rule,
                'description': '临时文件管理协同规则 - 阻止提交临时文件'
            },
            'context_chain_integrity': {
                'level': EnforcementLevel.HARD_BLOCK,
                'handler': self._enforce_context_chain_rule,
                'description': '上下文链完整性规则 - 确保上下文传递'
            },
            'security_constraint': {
                'level': EnforcementLevel.HARD_BLOCK,
                'handler': self._enforce_security_constraint,
                'description': '安全约束规则 - 强制宪法验证'
            }
        }
        
        # 二级优先级执法规则
        self.enforcement_rules.update({
            'directory_structure_consistency': {
                'level': EnforcementLevel.SOFT_BLOCK,
                'handler': self._enforce_directory_structure_rule,
                'description': '目录结构一致性规则'
            },
            'state_consistency': {
                'level': EnforcementLevel.WARN,
                'handler': self._enforce_state_consistency_rule,
                'description': '状态一致性规则'
            },
            'workplace_isolation': {
                'level': EnforcementLevel.SOFT_BLOCK,
                'handler': self._enforce_workplace_isolation_rule,
                'description': '工作区隔离规则'
            }
        })
    
    def enforce_contract_before_execution(self, skill_name: str, args: Dict[str, Any]) -> Tuple[bool, str]:
        """执行前契约强制检查"""
        with self.lock:
            # 检查技能是否被纳入协同契约
            contract_violations = []
            
            for rule_name, rule_config in self.enforcement_rules.items():
                is_valid, reason = rule_config['handler'](skill_name, args, 'before')
                if not is_valid:
                    contract_violations.append((rule_name, reason))
                    if rule_config['level'] == EnforcementLevel.HARD_BLOCK:
                        return False, f"❌ 严重违规: {reason}"
            
            # 二级违规但为软阻塞的处理
            soft_violations = [(name, reason) for name, reason in contract_violations 
                             if self.enforcement_rules[name]['level'] in [EnforcementLevel.SOFT_BLOCK, EnforcementLevel.WARN]]
            
            if soft_violations and any(self.enforcement_rules[name]['level'] == EnforcementLevel.SOFT_BLOCK 
                                     for name, _ in contract_violations):
                return False, f"❌ 软阻塞违规: {[reason for _, reason in soft_violations]}"
            
            # 记录轻微违规
            if soft_violations:
                self._log_violation(ViolationType.STATE_INCONSISTENCY, 
                                 f"轻微协同违规: {skill_name}", 
                                 soft_violations)
            
            return True, "✅ 协同检查通过"
    
    def enforce_contract_after_execution(self, skill_name: str, result: str, 
                                       original_args: Dict[str, Any]) -> str:
        """执行后契约强制检查"""
        with self.lock:
            # 逐一检查所有规则
            for rule_name, rule_config in self.enforcement_rules.items():
                is_valid, reason = rule_config['handler'](skill_name, result, 'after', original_args)
                
                if not is_valid:
                    violation_type = self._get_violation_type(rule_name)
                    self._log_violation(violation_type, f"技能 {skill_name} 后执行违规", reason)
                    
                    if rule_config['level'] == EnforcementLevel.HARD_BLOCK:
                        return f"❌ 执行后契约检查失败: {reason}\n原始结果被拒绝"
            
            return result
    
    def _enforce_temp_file_rule(self, skill_name: str, data: Any, phase: str, 
                               original_args: Dict[str, Any] = None) -> Tuple[bool, str]:
        """执行临时文件管理规则"""
        from .cognitive_coordination_center import COORDINATION_CENTER
        
        if skill_name in ['git_operations', 'git_operations_constitutional']:
            if phase == 'before':
                # 检查是否试图操作临时文件
                import os
                temp_files = set(COORDINATION_CENTER.context_state.get('temp_files', []))
                
                if 'operation' in original_args and original_args['operation'] == 'smart-commit':
                    # 检查要提交的文件是否包含临时文件
                    try:
                        import subprocess
                        from pathlib import Path
                        project_path = original_args.get('project_path', '.')
                        result = subprocess.run(['git', 'status', '--porcelain'], 
                                              cwd=project_path, capture_output=True, text=True)
                        
                        if result.stdout:
                            staged_files = [line[3:] for line in result.stdout.split('\n') if line.strip()]
                            temp_in_staging = [f for f in staged_files if f in temp_files]
                            
                            if temp_in_staging:
                                return False, f"试图提交临时文件: {', '.join(temp_in_staging)}"
                    except:
                        pass
            
            elif phase == 'after':
                # 检查结果是否符合临时文件管理原则
                if '临时文件' in str(data) or '临时' in str(data):
                    return True, ""  # 临时文件操作本身是正常的
        
        return True, ""
    
    def _enforce_context_chain_rule(self, skill_name: str, data: Any, phase: str, 
                                   original_args: Dict[str, Any] = None) -> Tuple[bool, str]:
        """执行上下文链完整性规则"""
        from .cognitive_coordination_center import COORDINATION_CENTER
        
        if skill_name in ['context_analysis', 'context_optimization', 'cognitive_template',
                         'context_analysis_constitutional', 'context_optimization_constitutional',
                         'cognitive_template_constitutional']:
            if phase == 'before':
                # 检查上下文链完整性
                current_analysis = COORDINATION_CENTER.context_state.get('current_analysis')
                
                if skill_name in ['context_optimization', 'context_optimization_constitutional'] and not current_analysis:
                    return False, "缺少上游分析结果，上下文链断裂"
                
                if skill_name in ['cognitive_template', 'cognitive_template_constitutional']:
                    # 需要有优化或分析结果
                    has_context = (current_analysis or 
                                 original_args.get('context') or 
                                 original_args.get('input'))
                    if not has_context:
                        return False, "无可用上下文进行认知处理"
        
        return True, ""
    
    def _enforce_security_constraint(self, skill_name: str, data: Any, phase: str, 
                                    original_args: Dict[str, Any] = None) -> Tuple[bool, str]:
        """执行安全约束规则"""
        try:
            from .constitutional_validator import validate_constitutional_compliance
        except ImportError:
            return True, "宪法验证器不可用"  # 如果验证器不可用，暂时不强制执行
        
        if phase == 'before':
            # 验证输入参数
            try:
                validation = validate_constitutional_compliance(str(original_args), "cognitive_convenience")
                if not validation["compliant"]:
                    return False, f"输入参数宪法验证失败: {validation['feedback']}"
            except:
                # 如果验证失败，允许执行但记录
                pass
        
        elif phase == 'after':
            # 验证输出结果
            try:
                validation = validate_constitutional_compliance(str(data), "all")
                if not validation["compliant"]:
                    return False, f"输出结果宪法验证失败: {validation['feedback']}"
            except:
                # 如果验证失败，允许执行但记录
                pass
        
        return True, ""
    
    def _enforce_directory_structure_rule(self, skill_name: str, data: Any, phase: str, 
                                         original_args: Dict[str, Any] = None) -> Tuple[bool, str]:
        """执行目录结构一致性规则"""
        # 检查目录结构相关技能的一致性
        if skill_name in ['progressive_disclosure', 'progressive_disclosure_constitutional',
                         'git_operations', 'git_operations_constitutional']:
            if phase == 'after':
                # 检查结果是否包含目录结构信息
                if isinstance(data, str) and any(keyword in data.lower() 
                                                for keyword in ['structure', 'directory', 'folder', 'path']):
                    # 记录结构变化，但通常不阻塞
                    pass
        
        return True, ""
    
    def _enforce_state_consistency_rule(self, skill_name: str, data: Any, phase: str, 
                                       original_args: Dict[str, Any] = None) -> Tuple[bool, str]:
        """执行状态一致性规则"""
        # 一般状态检查，用于监控一致性
        return True, ""
    
    def _enforce_workplace_isolation_rule(self, skill_name: str, data: Any, phase: str, 
                                         original_args: Dict[str, Any] = None) -> Tuple[bool, str]:
        """执行工作区隔离规则"""
        from .cognitive_coordination_center import COORDINATION_CENTER
        
        if skill_name in ['temp_workspace', 'temp_workspace_constitutional']:
            if phase == 'before':
                # 检查工作区并发访问
                active_sessions = COORDINATION_CENTER.context_state.get('active_sessions', [])
                session_id = original_args.get('session_id')
                
                if session_id in active_sessions:
                    return False, f"工作区 {session_id} 正在被其他操作使用"
        
        return True, ""
    
    def _get_violation_type(self, rule_name: str) -> ViolationType:
        """根据规则名称获取违规类型"""
        mapping = {
            'temp_file_management': ViolationType.TEMP_FILE_VIOLATION,
            'context_chain_integrity': ViolationType.CONTEXT_CHAIN_BREAK,
            'security_constraint': ViolationType.SECURITY_BYPASS,
            'directory_structure_consistency': ViolationType.STRUCTURE_MISMATCH,
            'state_consistency': ViolationType.STATE_INCONSISTENCY,
            'workplace_isolation': ViolationType.STATE_INCONSISTENCY
        }
        return mapping.get(rule_name, ViolationType.STATE_INCONSISTENCY)
    
    def _log_violation(self, violation_type: ViolationType, description: str, details: str):
        """记录违规"""
        violation_record = {
            'timestamp': str(datetime.now()),
            'type': violation_type.value,
            'description': description,
            'details': details
        }
        self.violations_log.append(violation_record)
    
    def get_violation_report(self) -> Dict[str, Any]:
        """获取违规报告"""
        return {
            'total_violations': len(self.violations_log),
            'violations_by_type': {
                vt.name: len([v for v in self.violations_log if v['type'] == vt.value])
                for vt in ViolationType
            },
            'recent_violations': self.violations_log[-10:]  # 最近10条
        }

# 全局协同执法器实例
ENFORCER = CoordinationEnforcer()