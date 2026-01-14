"""
宪法级基类技能 - 智能应用宪法原则
只对生成目录、文件、脚本的技能强制宪法约束
"""
from typing import Dict, Any, Callable
from abc import ABC, abstractmethod

class ConstitutionalBaseSkill(ABC):
    """
    宪法级基类技能 - 智能宪法约束
    只对生成目录、文件、脚本的技能强制宪法约束
    """

    def __init__(self, name: str, description: str, needs_constitutional_check: bool = True):
        self.name = name
        self.description = description
        self.needs_constitutional_check = needs_constitutional_check
        self.validator = self._load_constitutional_validator()

        # 需要宪法验证的技能类型
        self.construction_skills = {
            'temp_workspace', 'progressive_disclosure', 'git_operations',
            'system_architect', 'cognitive_template', 'context_analysis',
            'task_decomposer', 'architect', 'constraint_generator',
            'modulizer_independent', 'agent_creator_independent',
            'temp_workspace_constitutional', 'progressive_disclosure_constitutional',
            'git_operations_constitutional', 'agent_creator_constitutional'
        }

        # 检查是否需要宪法约束
        if name in self.construction_skills:
            self.needs_constitutional_check = True

    def _load_constitutional_validator(self):
        """加载宪法验证器"""
        try:
            from ..skills.constitutional_validator import validate_constitutional_compliance
            return validate_constitutional_compliance
        except ImportError:
            try:
                from src.dna_spec_kit_integration.skills.constitutional_validator import validate_constitutional_compliance
                return validate_constitutional_compliance
            except ImportError:
                # 备用验证器
                return lambda content, principle="all": {
                    "compliant": True,
                    "feedback": "验证器不可用",
                    "principle": principle
                }

    def execute(self, args: Dict[str, Any]) -> str:
        """
        执行技能 - 智能宪法约束
        只对需要生成内容的技能进行宪法验证
        """
        # 1. 预执行宪法验证 (只对需要的技能)
        if self.needs_constitutional_check:
            input_validation = self.validator(str(args), "cognitive_convenience")
            if not input_validation["compliant"]:
                return f"❌ 输入宪法验证失败: {input_validation['feedback']}"

        # 2. 执行具体的技能逻辑
        try:
            result = self._execute_skill_logic(args)

            # 3. 后执行宪法验证 (只对需要的技能)
            if self.needs_constitutional_check:
                output_validation = self.validator(result, "all")
                if not output_validation["compliant"]:
                    return f"❌ 输出宪法验证失败: {output_validation['feedback']}\n原始结果: {result}"

            return result

        except Exception as e:
            error_msg = f"❌ 技能执行异常: {str(e)}"
            # 只对需要的技能验证错误消息
            if self.needs_constitutional_check:
                error_validation = self.validator(error_msg, "cognitive_convenience")
                if not error_validation["compliant"]:
                    error_msg += f" (宪法验证: {error_validation['feedback']})"
            return error_msg

    @abstractmethod
    def _execute_skill_logic(self, args: Dict[str, Any]) -> str:
        """
        执行具体的技能逻辑 - 子类必须实现
        """
        pass

class ConstitutionalSkillWrapper:
    """
    宪法技能包装器 - 为现有技能智能添加宪法约束
    只对生成目录、文件、脚本的技能添加宪法约束
    """

    def __init__(self, skill_function: Callable, skill_name: str = ""):
        self.skill_function = skill_function
        self.skill_name = skill_name
        self.validator = self._load_constitutional_validator()

        # 需要宪法验证的技能类型
        self.construction_skills = {
            'temp_workspace', 'progressive_disclosure', 'git_operations',
            'system_architect', 'cognitive_template', 'context_analysis',
            'task_decomposer', 'architect', 'constraint_generator',
            'modulizer_independent', 'agent_creator_independent',
            'temp_workspace_constitutional', 'progressive_disclosure_constitutional',
            'git_operations_constitutional', 'agent_creator_constitutional'
        }

        # 检查是否需要宪法约束
        self.needs_constitutional_check = skill_name in self.construction_skills

    def _load_constitutional_validator(self):
        """加载宪法验证器"""
        try:
            from ..skills.constitutional_validator import validate_constitutional_compliance
            return validate_constitutional_compliance
        except ImportError:
            try:
                from src.dna_spec_kit_integration.skills.constitutional_validator import validate_constitutional_compliance
                return validate_constitutional_compliance
            except ImportError:
                return lambda content, principle="all": {
                    "compliant": True,
                    "feedback": "验证器不可用",
                    "principle": principle
                }

    def execute(self, args: Dict[str, Any]) -> str:
        """
        宪法包装的执行 - 智能宪法验证
        只对需要生成内容的技能进行宪法验证
        """
        # 预验证 (只对需要的技能)
        if self.needs_constitutional_check:
            input_validation = self.validator(str(args), "cognitive_convenience")
            if not input_validation["compliant"]:
                return f"❌ 输入宪法验证失败: {input_validation['feedback']}"

        # 执行原技能
        result = self.skill_function(args)

        # 后验证 (只对需要的技能)
        if self.needs_constitutional_check:
            output_validation = self.validator(result, "all")
            if not output_validation["compliant"]:
                return f"❌ 输出宪法验证失败: {output_validation['feedback']}\n原始结果: {result}"

        return result

def constitutional_skill(skill_func: Callable, skill_name: str = "") -> ConstitutionalSkillWrapper:
    """
    宪法技能装饰器 - 智能宪法约束
    只对建设类技能应用宪法约束
    """
    return ConstitutionalSkillWrapper(skill_func, skill_name)