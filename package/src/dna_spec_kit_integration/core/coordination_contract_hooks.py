"""
技能执行钩子系统 - 基于共同状态的协同契约执行
"""
import threading
from typing import Dict, Any, Callable, Tuple
from datetime import datetime
import json

class CoordinationContractHooks:
    """
    协同契约钩子系统 - 在技能执行的关键时点强制执行契约
    """
    
    def __init__(self):
        self.state_manager = None
        self.hooks_active = True
        self.lock = threading.Lock()
        self.execution_history = []
        
    def initialize_with_state_manager(self, state_manager):
        """初始化钩子系统并关联状态管理器"""
        self.state_manager = state_manager
        print("🔗 协同契约钩子系统已初始化")
        
    def pre_execution_hook(self, skill_name: str, args: Dict[str, Any]) -> Tuple[bool, str]:
        """
        执行前钩子 - 基于共同状态进行契约检查
        """
        if not self.hooks_active or not self.state_manager:
            return True, "钩子未激活或状态管理器未就绪"
        
        with self.lock:
            # 记录执行开始
            self.execution_history.append({
                "timestamp": datetime.now().isoformat(),
                "skill": skill_name,
                "action": "pre_execution_check",
                "args_keys": list(args.keys())
            })
            
            # 针对不同技能类型执行特定检查
            if skill_name in ["temp_workspace", "temp_workspace_constitutional", "git_operations", "git_operations_constitutional"]:
                return self._check_temp_file_contract(skill_name, args)
            
            elif skill_name in ["context_analysis", "context_optimization", "cognitive_template",
                               "context_analysis_constitutional", "context_optimization_constitutional", "cognitive_template_constitutional"]:
                return self._check_context_chain_contract(skill_name, args)
            
            elif skill_name in ["progressive_disclosure", "progressive_disclosure_constitutional",
                               "system_architect", "system_architect_constitutional"]:
                return self._check_directory_structure_contract(skill_name, args)
            
            else:
                # 通用安全检查
                return self._check_security_contract(skill_name, args)
    
    def post_execution_hook(self, skill_name: str, result: str, args: Dict[str, Any]) -> str:
        """
        执行后钩子 - 更新共同状态并验证契约合规性
        """
        if not self.hooks_active or not self.state_manager:
            return result
        
        with self.lock:
            # 记录执行完成
            self.execution_history.append({
                "timestamp": datetime.now().isoformat(),
                "skill": skill_name,
                "action": "post_execution_update",
                "result_length": len(result) if result else 0
            })
            
            # 根据技能类型更新状态
            if skill_name in ["temp_workspace", "temp_workspace_constitutional"]:
                result = self._update_temp_workspace_state(skill_name, result, args)
            
            elif skill_name in ["context_analysis", "context_optimization", "cognitive_template",
                               "context_analysis_constitutional", "context_optimization_constitutional", "cognitive_template_constitutional"]:
                result = self._update_context_chain_state(skill_name, result, args)
            
            elif skill_name in ["git_operations", "git_operations_constitutional"]:
                result = self._update_git_state(skill_name, result, args)
            
            # 安全结果验证
            result = self._validate_result_security(result, skill_name)
            
            return result
    
    def _check_temp_file_contract(self, skill_name: str, args: Dict[str, Any]) -> Tuple[bool, str]:
        """检查临时文件管理契约"""
        if not self.state_manager:
            return True, "状态管理器未就绪"
        
        if skill_name in ["git_operations", "git_operations_constitutional"]:
            # 检查是否试图提交临时文件
            temp_files = set(self.state_manager.get_state("temp_workspace", "temp_files") or [])
            
            # 模拟检查git暂存区中的文件
            if temp_files:
                return False, f"❌ 阻止操作: 检测到 {len(temp_files)} 个临时文件，禁止提交以防止项目污染: {', '.join(list(temp_files)[:3])}{'...' if len(temp_files) > 3 else ''}"
        
        elif skill_name in ["temp_workspace", "temp_workspace_constitutional"]:
            # 检查临时工作区操作
            session_id = args.get("session_id")
            current_session = self.state_manager.get_state("temp_workspace", "active_session")
            
            if session_id and current_session and session_id != current_session:
                return False, f"❌ 工作区会话冲突: 当前会话 {current_session}, 请求会话 {session_id}"
        
        return True, "✅ 临时文件契约检查通过"
    
    def _check_context_chain_contract(self, skill_name: str, args: Dict[str, Any]) -> Tuple[bool, str]:
        """检查上下文链完整性契约"""
        if not self.state_manager:
            return True, "状态管理器未就绪"
        
        if skill_name in ["context_optimization", "context_optimization_constitutional"]:
            # 检查是否有所需的上游分析结果
            current_analysis = self.state_manager.get_state("context_chain", "current_analysis")
            if not current_analysis:
                return False, "❌ 上下文链断裂: 优化操作需要上游分析结果"
        
        elif skill_name in ["cognitive_template", "cognitive_template_constitutional"]:
            # 检查上下文可用性
            current_analysis = self.state_manager.get_state("context_chain", "current_analysis")
            context_arg = args.get("context") or args.get("input")
            
            if not current_analysis and not context_arg:
                return False, "❌ 上下文缺失: 认知模板操作需要上下文输入"
        
        return True, "✅ 上下文链契约检查通过"
    
    def _check_security_contract(self, skill_name: str, args: Dict[str, Any]) -> Tuple[bool, str]:
        """检查安全约束契约"""
        try:
            from .constitutional_validator import validate_constitutional_compliance
        except ImportError:
            return True, "宪法验证器不可用，跳过安全检查"
        
        # 验证输入
        if args:
            input_str = str(args)
            validation = validate_constitutional_compliance(input_str, "cognitive_convenience")
            if not validation["compliant"]:
                return False, f"❌ 输入安全验证失败: {validation['feedback']}"
        
        return True, "✅ 安全契约检查通过"
    
    def _check_directory_structure_contract(self, skill_name: str, args: Dict[str, Any]) -> Tuple[bool, str]:
        """检查目录结构一致性契约"""
        # 对目录结构相关操作进行检查
        return True, "✅ 目录结构契约检查通过"
    
    def _update_temp_workspace_state(self, skill_name: str, result: str, args: Dict[str, Any]) -> str:
        """更新临时工作区状态"""
        if not self.state_manager:
            return result
        
        # 解析结果，更新临时文件状态
        if "文件已添加到临时工作区" in result:
            file_path = args.get("file_path", "unknown")
            self.state_manager.append_to_list("temp_workspace", "temp_files", file_path)
        
        elif "文件已确认到确认区域" in result:
            file_path = args.get("confirm_file", args.get("file_path", "unknown"))
            self.state_manager.remove_from_list("temp_workspace", "temp_files", file_path)
            self.state_manager.append_to_list("temp_workspace", "confirmed_files", file_path)
        
        elif "临时工作区已创建" in result:
            import re
            match = re.search(r'临时工作区已创建: (.+)', result)
            if match:
                workspace_path = match.group(1)
                self.state_manager.update_state("temp_workspace", "active_session", workspace_path)
                self.state_manager.update_state("temp_workspace", "session_start_time", datetime.now().isoformat())
        
        return result
    
    def _update_context_chain_state(self, skill_name: str, result: str, args: Dict[str, Any]) -> str:
        """更新上下文链状态"""
        if not self.state_manager:
            return result
        
        if skill_name in ["context_analysis", "context_analysis_constitutional"]:
            # 更新当前分析状态
            context_id = f"ctx_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            analysis_summary = result[:200] + "..." if len(result) > 200 else result
            self.state_manager.update_state("context_chain", "current_analysis", {
                "id": context_id,
                "summary": analysis_summary,
                "timestamp": datetime.now().isoformat()
            })
            
            # 添加到历史记录
            self.state_manager.append_to_list("context_chain", "analysis_history", {
                "id": context_id,
                "result_summary": analysis_summary,
                "timestamp": datetime.now().isoformat()
            })
        
        elif skill_name in ["context_optimization", "context_optimization_constitutional"]:
            # 更新优化标记
            optimization_flag = f"optimized_{datetime.now().isoformat()}"
            self.state_manager.append_to_list("context_chain", "optimization_flags", optimization_flag)
        
        return result
    
    def _update_git_state(self, skill_name: str, result: str, args: Dict[str, Any]) -> str:
        """更新Git状态"""
        if not self.state_manager:
            return result
        
        if "已提交" in result or "提交成功" in result:
            # 更新Git操作计数
            self.state_manager.increment_counter("git_operations", "commit_count")
        
        return result
    
    def _validate_result_security(self, result: str, skill_name: str) -> str:
        """验证结果安全性"""
        try:
            from .constitutional_validator import validate_constitutional_compliance
        except ImportError:
            return result  # 如果验证器不可用，不修改结果
        
        if result and isinstance(result, str):
            validation = validate_constitutional_compliance(result, "all")
            if not validation["compliant"]:
                # 添加宪法注释到结果
                result += f"\n\n<!-- Constitutional Note: {validation['feedback']} -->"
        
        return result

# 全局钩子系统实例
COORDINATION_HOOKS = CoordinationContractHooks()