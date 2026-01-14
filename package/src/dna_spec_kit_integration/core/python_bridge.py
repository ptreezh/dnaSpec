"""
Enhanced Python桥接器模块
负责调用Python实现的DNASPEC技能
扩展了模块查找功能以支持多路径查找
"""
import importlib
import sys
from typing import Dict, Any, Optional
from pathlib import Path


class PythonBridge:
    """
    Python桥接器
    负责调用Python实现的DNASPEC技能
    """

    def __init__(self, skills_base_path: Optional[str] = None):
        """
        初始化Python桥接器

        Args:
            skills_base_path: 技能模块的基础路径
        """
        self.skills_base_path = skills_base_path or "dna_spec_kit_integration.skills"
        self._imported_modules = {}

    def execute_skill(self, skill_name: str, params: str, original_skill_name: str = None) -> Dict[str, Any]:
        """
        执行Python技能

        Args:
            skill_name: 技能名称（如 'dnaspec-architect'）
            params: 技能参数
            original_skill_name: 原始技能名称，用于正确映射Claude工具名称

        Returns:
            执行结果字典
        """
        try:
            # Import required modules at function start to avoid local variable issues
            import importlib
            import importlib.util
            import sys
            import os

            # 首先尝试直接导入claude_skills模块，这是最常见的情况
            module = None
            full_module_path = None
            
            # 尝试多种导入方式，确保能找到已安装的包
            # 方式1：直接导入
            try:
                import claude_skills.claude_skill as claude_module
                module = claude_module
                full_module_path = "claude_skills.claude_skill"
                self._imported_modules[full_module_path] = module
                print(f"Successfully imported: {full_module_path}")  # 调试信息
            except ImportError as e:
                print(f"Failed to import claude_skills.claude_skill: {e}")  # 调试信息
                # 方式2：使用importlib导入
                try:
                    module = importlib.import_module("claude_skills.claude_skill")
                    full_module_path = "claude_skills.claude_skill"
                    self._imported_modules[full_module_path] = module
                    print(f"Successfully imported via importlib: {full_module_path}")  # 调试信息
                except ImportError as e2:
                    print(f"Failed to import via importlib: {e2}")  # 调试信息
                    # 如果直接导入失败，尝试其他路径
                    # 将技能名称规范化为模块名称
                    # 例如 'dnaspec-architect' -> 'architect'
                    module_name = skill_name.replace('dnaspec-', '')

                    # 定义要尝试的模块路径列表
                    # 按优先级排序：
                    # 1. Claude技能路径 (claude_skills) - 优先使用Claude标准
                    # 2. 标准路径 (dna_spec_kit_integration.skills.{module_name})
                    # 3. 上下文工程路径 (dna_context_engineering.{module_name})
                    # 4. 模块名本身 (如果模块名已是完整路径)
                    module_paths_to_try = [
                        f"claude_skills.claude_skill",  # Claude skills path - HIGHEST PRIORITY
                        f"claude_skills.main",  # Claude main module
                        f"{self.skills_base_path}.{module_name}",  # Standard path: dna_spec_kit_integration.skills.{module_name}
                        f"dna_context_engineering.{module_name}",  # Context engineering path
                        f"{module_name}"  # Module name directly (could be full path)
                    ]

                    # 尝试导入技能模块 - 按顺序尝试不同路径
                    error_messages = []

                    for module_path in module_paths_to_try:
                        try:
                            module = importlib.import_module(module_path)
                            # 更新模块路径以使用找到的路径
                            full_module_path = module_path  # Set the correct path that worked
                            self._imported_modules[module_path] = module  # Cache the successful import
                            print(f"Successfully imported via importlib: {full_module_path}")  # 调试信息
                            break  # Stop if successful
                        except ImportError as e:
                            error_messages.append(f"{module_path}: {str(e)}")
                            continue  # Try next path

                    # 如果标准路径都没有找到模块，尝试在项目根目录下查找
                    if module is None:
                        # 获取项目根目录
                        current_file_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
                        project_root = os.path.dirname(current_file_dir)  # Go up one more level to project root
                        if project_root not in sys.path:
                            sys.path.insert(0, project_root)

                        # 尝试直接从 claude_skills 目录导入
                        claude_skills_dir = os.path.join(project_root, "claude_skills")
                        if os.path.exists(claude_skills_dir):
                            if claude_skills_dir not in sys.path:
                                sys.path.insert(0, claude_skills_dir)

                            try:
                                # 尝试导入统一技能模块
                                module = importlib.import_module("claude_skill")
                                full_module_path = "claude_skill"
                                self._imported_modules[full_module_path] = module
                                print(f"Found unified skill module: {full_module_path}")
                            except ImportError as e:
                                error_messages.append(f"claude_skill (from claude_skills): {str(e)}")

                                # 最后尝试导入main模块
                                try:
                                    main_path = os.path.join(claude_skills_dir, "main.py")
                                    if os.path.exists(main_path):
                                        spec = importlib.util.spec_from_file_location("main_skill", main_path)
                                        if spec and spec.loader:
                                            module = importlib.util.module_from_spec(spec)
                                            spec.loader.exec_module(module)
                                            full_module_path = "main_skill"
                                            self._imported_modules[full_module_path] = module
                                            print(f"Imported from main.py: {full_module_path}")
                                except Exception as e2:
                                    error_messages.append(f"main.py import: {str(e2)}")
                        else:
                            error_messages.append("claude_skills directory does not exist")

                    # 如果所有路径都失败，返回错误
                    if module is None:
                        return {
                            'success': False,
                            'error': f'Failed to import skill module from any location:\n' + '\n'.join(error_messages),
                            'skill': skill_name
                        }

            # 验证模块是否包含execute函数
            if not hasattr(module, 'execute'):
                return {
                    'success': False,
                    'error': f'Skill module {full_module_path} does not have execute function',
                    'skill': skill_name
                }

            # 准备参数字典
            # 使用原始技能名称来正确映射Claude工具名称
            actual_skill_name = original_skill_name if original_skill_name else skill_name
            skill_for_claude = actual_skill_name.replace('dnaspec-', '').replace('_', '-')
            # 映射到Claude技能中支持的工具名称
            tool_name_mapping = {
                'context-analysis': 'context-analyzer',
                'context-analyzer': 'context-analyzer', 
                'context-optimization': 'context-optimizer',
                'context-optimizer': 'context-optimizer',
                'cognitive-template': 'cognitive-templater',
                'cognitive-templater': 'cognitive-templater',
                'agent-creator': 'agent-creator',
                'task-decomposer': 'task-decomposer',
                'constraint-generator': 'constraint-generator',
                'architect': 'architect',
                'simple-architect': 'architect',
                'system-architect': 'architect',
                'api-checker': 'context-analyzer',  # 使用上下文分析作为基础
                'git-operations': 'context-analyzer',  # 使用上下文分析作为基础
                'temp-workspace': 'context-analyzer',  # 使用上下文分析作为基础
                'liveness': 'context-analyzer',  # 使用上下文分析作为基础
                'dnaspec-init': 'dnaspec-init',
                'temp-workspace-skill': 'context-analyzer'  # 使用上下文分析作为基础
            }
            
            claude_tool_name = tool_name_mapping.get(skill_for_claude, skill_for_claude)
            
            args = {
                'inputs': [{'input': params, 'skill': actual_skill_name}],
                'tool_name': claude_tool_name
            }

            # 执行技能
            result = module.execute(args)

            return {
                'success': True,
                'result': result,
                'skill': skill_name,
                'module_path': full_module_path
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'skill': skill_name,
                'stack': str(e.__traceback__) if e.__traceback__ else None
            }

    def execute_skill_with_json_params(self, skill_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用JSON参数执行Python技能

        Args:
            skill_name: 技能名称
            params: JSON参数字典

        Returns:
            执行结果字典
        """
        try:
            # 将技能名称规范化为模块名称
            module_name = skill_name.replace('dnaspec-', '')

            # 定义要尝试的模块路径列表
            module_paths_to_try = [
                f"{self.skills_base_path}.{module_name}",  # Standard path
                f"dna_context_engineering.{module_name}",  # Context engineering path
                f"{module_name}"  # Direct path
            ]

            # 尝试导入技能模块 - 按顺序尝试不同路径
            module = None
            error_messages = []
            
            for module_path in module_paths_to_try:
                try:
                    module = importlib.import_module(module_path)
                    # 更新模块路径以使用找到的路径
                    if module_path not in self._imported_modules:
                        self._imported_modules[module_path] = module
                    full_module_path = module_path
                    break  # Stop if successful
                except ImportError as e:
                    error_messages.append(f"{module_path}: {str(e)}")
                    continue  # Try next path

            # 如果所有路径都失败，返回错误
            if module is None:
                return {
                    'success': False,
                    'error': f'Failed to import skill module from any location:\n' + '\n'.join(error_messages),
                    'skill': skill_name
                }

            # 验证模块是否包含execute函数
            if not hasattr(module, 'execute'):
                return {
                    'success': False,
                    'error': f'Skill module {full_module_path} does not have execute function',
                    'skill': skill_name
                }

            # 执行技能
            result = module.execute(params)

            return {
                'success': True,
                'result': result,
                'skill': skill_name,
                'module_path': full_module_path
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'skill': skill_name,
                'stack': str(e.__traceback__) if e.__traceback__ else None
            }