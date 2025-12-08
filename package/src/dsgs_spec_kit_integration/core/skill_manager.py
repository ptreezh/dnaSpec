
import importlib

class SkillManager:
    """最小化的技能管理器，用于加载和执行技能。"""

    def __init__(self, skills_base_path="dnaspec_spec_kit_integration.skills"):
        self.skills_base_path = skills_base_path

    def execute_skill(self, skill_name: str, args: dict) -> str:
        """
        根据技能名称动态加载并执行技能。
        """
        try:
            # 构建技能模块的完整路径
            skill_module_path = f"{self.skills_base_path}.{skill_name}"
            
            # 动态导入模块
            skill_module = importlib.import_module(skill_module_path)
            
            # 调用模块内的execute函数
            return skill_module.execute(args)
        except ModuleNotFoundError:
            raise ValueError(f"Skill '{skill_name}' not found.")
        except AttributeError:
            raise ValueError(f"Skill '{skill_name}' does not have an 'execute' function.")

