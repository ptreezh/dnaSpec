"""
系统级宪法拦截机制 - 智能拦截，只对生成目录、文件、脚本的技能执行宪法验证
确保需要生成内容的技能都经过宪法检查
"""
from typing import Dict, Any, Callable
from .constitutional_enforcer import execute_with_constitutional_enforcement
import functools

class ConstitutionalHookSystem:
    """宪法钩子系统 - 智能拦截机制"""

    def __init__(self):
        self.hooks = {}
        self.constitutional_validator = self._load_validator()
        # 需要宪法验证的技能类型
        self.construction_skills = {
            'temp_workspace', 'progressive_disclosure', 'git_operations',
            'system_architect', 'cognitive_template', 'context_analysis',
            'task_decomposer', 'architect', 'constraint_generator',
            'modulizer_independent', 'agent_creator_independent',
            'temp_workspace_constitutional', 'progressive_disclosure_constitutional',
            'git_operations_constitutional', 'agent_creator_constitutional'
        }

    def _load_validator(self):
        """加载宪法验证器"""
        try:
            from ..skills.constitutional_validator import validate_constitutional_compliance
            return validate_constitutional_compliance
        except ImportError:
            try:
                from src.dna_spec_kit_integration.skills.constitutional_validator import validate_constitutional_compliance
                return validate_constitutional_compliance
            except ImportError:
                return lambda content, principle="all": {"compliant": True, "feedback": "验证器不可用", "principle": principle}

    def install_selective_skill_hook(self):
        """
        安装选择性技能钩子 - 只拦截需要生成内容的技能
        只对生成目录、文件、脚本的技能强制通过宪法验证
        """
        import sys

        # 创建一个智能包装函数，只在需要时进行宪法验证
        def selective_constitutional_wrapper(original_func: Callable, skill_name: str) -> Callable:
            @functools.wraps(original_func)
            def wrapper(args: Dict[str, Any]) -> str:
                # 只对需要建设的技能进行验证
                if skill_name in self.construction_skills:
                    # 在执行前进行宪法验证
                    args_validation = self.constitutional_validator(str(args), "cognitive_convenience")
                    if not args_validation["compliant"]:
                        return f"❌ 输入宪法验证失败: {args_validation['feedback']}"

                # 执行原始函数
                result = original_func(args)

                # 只对需要建设的技能进行输出验证
                if skill_name in self.construction_skills:
                    result_validation = self.constitutional_validator(result, "all")
                    if not result_validation["compliant"]:
                        return f"❌ 输出宪法验证失败: {result_validation['feedback']}\n原始结果: {result}"

                return result

            return wrapper

    def enforce_constitutional_compliance(self, skill_name: str, args: Dict[str, Any]) -> str:
        """
        强制执行宪法合规性检查 - 智能判断
        只对建设类技能执行宪法检查
        """
        # 只对建设类技能进行验证
        if skill_name in self.construction_skills:
            # 输入验证
            args_validation = self.constitutional_validator(str(args), "cognitive_convenience")
            if not args_validation["compliant"]:
                return f"❌ 输入宪法验证失败: {args_validation['feedback']}"

        # 通过宪法执行器执行技能
        result = execute_with_constitutional_enforcement(skill_name, args)

        # 只对建设类技能进行输出验证
        if skill_name in self.construction_skills:
            result_validation = self.constitutional_validator(result, "all")
            if not result_validation["compliant"]:
                return f"❌ 结果宪法验证失败: {result_validation['feedback']}\n原始结果: {result}"

        return result

# 初始化全局宪法钩子系统
HOOK_SYSTEM = ConstitutionalHookSystem()
HOOK_SYSTEM.install_selective_skill_hook()

def constitutional_enforce(skill_name: str, args: Dict[str, Any]) -> str:
    """
    宪法强制执行接口 - 只对建设类技能强制宪法检查
    只对生成目录、文件、脚本的技能进行验证
    """
    return HOOK_SYSTEM.enforce_constitutional_compliance(skill_name, args)