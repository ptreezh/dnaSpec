
import importlib
from ..skills.skill_executor import skill_executor

class SkillManager:
    """最小化的技能管理器，用于加载和执行技能。"""

    def __init__(self, skills_base_path="src.dna_spec_kit_integration.skills"):
        self.skills_base_path = skills_base_path

    def execute_skill(self, skill_name: str, args: dict) -> str:
        """
        根据技能名称动态加载并执行技能。
        """
        # Try to use the main skill executor first (which has all the registered skills)
        if skill_name in skill_executor.skill_registry:
            try:
                # Format args for the skill executor
                context = args.get('context', args.get('requirement', args.get('code', '')))
                result = skill_executor.execute_skill(skill_name, context=context, **args)
                # Handle both dict and string results
                if isinstance(result, dict):
                    return str(result.get('result', 'Skill executed successfully'))
                else:
                    return result
            except Exception:
                pass  # Fall through to the original method

        # Original method for skills that are individual modules
        try:
            # 构建技能模块的完整路径
            # Convert hyphens to underscores for Python module names
            module_name = skill_name.replace('-', '_')
            skill_module_path = f"{self.skills_base_path}.{module_name}"

            # 动态导入模块
            skill_module = importlib.import_module(skill_module_path)

            # 调用模块内的execute函数
            return skill_module.execute(args)
        except ModuleNotFoundError:
            raise ValueError(f"Skill '{skill_name}' not found.")
        except AttributeError:
            raise ValueError(f"Skill '{skill_name}' does not have an 'execute' function.")
