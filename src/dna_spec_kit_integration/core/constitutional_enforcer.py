"""
核心宪法执行系统 - 只对生成目录、文件、脚本的技能进行宪法验证
作为系统的基本法，只针对需要生成内容的技能强制宪法检查
"""
from typing import Dict, Any
import importlib
import os
import sys
from pathlib import Path

class ConstitutionalExecutor:
    """宪法执行器 - 智能宪法约束机制"""

    def __init__(self):
        self.constitutional_validator = self._load_constitutional_validator()
        # 需要宪法验证的技能类型
        self.construction_skills = {
            'temp_workspace', 'progressive_disclosure', 'git_operations',
            'system_architect', 'cognitive_template', 'context_analysis',
            'task_decomposer', 'architect', 'constraint_generator',
            'modulizer_independent', 'agent_creator_independent',
            'temp_workspace_constitutional', 'progressive_disclosure_constitutional',
            'git_operations_constitutional', 'agent_creator_constitutional'
        }

    def _load_constitutional_validator(self):
        """加载宪法验证器"""
        try:
            # 尝试从标准位置加载宪法验证器
            from .constitutional_validator import validate_constitutional_compliance
            return validate_constitutional_compliance
        except ImportError:
            # 如果在技能包内加载失败，尝试绝对导入
            try:
                from src.dna_spec_kit_integration.skills.constitutional_validator import validate_constitutional_compliance
                return validate_constitutional_compliance
            except ImportError:
                # 如果都失败，返回一个简单的验证函数（备用）
                return self._default_constitutional_validator

    def _default_constitutional_validator(self, content: str, principle: str = "all"):
        """备用宪法验证器 - 简单验证"""
        # 这是一个简化版本，在实际环境中应该使用正式的验证器
        compliant = len(content.strip()) > 5  # 简单长度检查
        return {
            "compliant": compliant,
            "feedback": "内容长度足够" if compliant else "内容过短",
            "principle": principle
        }

    def execute_skill_with_constitutional_check(self, skill_name: str, args: Dict[str, Any]) -> str:
        """
        执行技能并根据技能类型决定是否进行宪法检查
        只针对生成目录、文件、脚本的技能才进行宪法验证
        """
        # 只对需要建设的技能进行宪法验证
        if skill_name in self.construction_skills:
            # 1. 预执行宪法验证 - 验证输入参数
            args_str = str(args)
            input_validation = self.constitutional_validator(args_str, "cognitive_convenience")
            if not input_validation["compliant"]:
                return f"❌ 输入宪法验证失败: {input_validation['feedback']}"

        # 2. 动态加载技能模块
        skill_module = self._load_skill_module(skill_name)
        if skill_module is None:
            return f"❌ 技能模块不存在: {skill_name}"

        # 3. 检查技能是否通过宪法验证（如果技能本身是宪法级的）
        skill_function = getattr(skill_module, 'execute', None)
        if skill_function is None:
            return f"❌ 技能模块缺少execute函数: {skill_name}"

        # 4. 执行技能
        try:
            result = skill_function(args)

            # 只对需要建设的技能进行输出验证
            if skill_name in self.construction_skills:
                output_validation = self.constitutional_validator(result, "all")
                if not output_validation["compliant"]:
                    return f"❌ 输出宪法验证失败: {output_validation['feedback']}\n原始结果: {result}"

            return result

        except Exception as e:
            return f"❌ 技能执行异常: {str(e)}"

    def _load_skill_module(self, skill_name: str):
        """安全地加载技能模块"""
        try:
            # 构建技能模块路径
            skills_path = Path(__file__).parent / "skills"
            skill_file = skills_path / f"{skill_name}.py"

            # 检查技能文件是否存在
            if not skill_file.exists():
                # 尝试寻找宪法级变体
                constitutional_skill_file = skills_path / f"{skill_name}_constitutional.py"
                if constitutional_skill_file.exists():
                    skill_file = constitutional_skill_file
                else:
                    # 尝试其他可能的变体
                    possible_files = [
                        f"{skill_name}_constitutational.py",
                        f"{skill_name}_const.py",
                        f"constitutional_{skill_name}.py"
                    ]
                    for possible_file in possible_files:
                        alt_path = skills_path / possible_file
                        if alt_path.exists():
                            skill_file = alt_path
                            break

            if not skill_file.exists():
                return None

            # 动态导入模块
            import importlib.util
            spec = importlib.util.spec_from_file_location(skill_name, skill_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

        except Exception:
            return None

# 全局宪法执行器实例
CONSTITUTIONAL_EXECUTOR = ConstitutionalExecutor()

def execute_with_constitutional_enforcement(skill_name: str, args: Dict[str, Any]) -> str:
    """
    通过宪法强制执行机制执行技能
    只对建设类技能执行宪法检查
    """
    return CONSTITUTIONAL_EXECUTOR.execute_skill_with_constitutional_check(skill_name, args)