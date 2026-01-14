"""
协同执行钩子 - 向技能注入协同契约强制执行能力
"""
import os
import sys
from pathlib import Path
import importlib.util
import inspect
from typing import Dict, Any, Callable, Tuple

from .coordination_enforcer import ENFORCER

class CoordinationHooksInjector:
    """协同钩子注入器 - 为技能注入契约强制执行能力"""
    
    def __init__(self):
        self.enhanced_skills = {}
        self.contract_file = Path(__file__).parent / "CONTRACT.yaml"
        
        # 定义需要强制执行契约的技能类型
        self.mandatory_skills = {
            'temp_workspace', 'temp_workspace_constitutional',
            'context_analysis', 'context_optimization', 'cognitive_template',
            'context_analysis_constitutional', 'context_optimization_constitutional', 
            'cognitive_template_constitutional',
            'git_operations', 'git_operations_constitutional',
            'progressive_disclosure', 'progressive_disclosure_constitutional'
        }
        
        self.recommended_skills = {
            'agent_creator_independent', 'agent_creator_constitutional',
            'system_architect', 'system_architect_constitutional',
            'task_decomposer', 'task_decomposer_constitutional'
        }
    
    def inject_coordination_hooks(self, skill_name: str, skill_function: Callable) -> Callable:
        """为技能注入协同契约强制执行钩子"""
        
        def enhanced_execute(args: Dict[str, Any]) -> str:
            """增强的执行函数 - 集成协同契约强制执行"""
            
            # 1. 预执行契约检查
            is_allowed, check_message = ENFORCER.enforce_contract_before_execution(skill_name, args)
            if not is_allowed:
                return check_message
            
            # 2. 执行原始技能
            try:
                result = skill_function(args)
                
                # 3. 后执行契约验证
                validated_result = ENFORCER.enforce_contract_after_execution(skill_name, result, args)
                
                return validated_result
                
            except Exception as e:
                # 对异常情况也要进行契约检查
                error_msg = f"技能执行异常: {str(e)}"
                
                # 记录异常到违规模块
                from .coordination_enforcer import ViolationType
                ENFORCER._log_violation(ViolationType.STATE_INCONSISTENCY, 
                                     f"技能 {skill_name} 执行异常", str(e))
                
                return error_msg
        
        # 保存增强后的技能
        self.enhanced_skills[skill_name] = enhanced_execute
        
        return enhanced_execute
    
    def is_mandatory_coordination_skill(self, skill_name: str) -> bool:
        """判断是否为强制协同技能"""
        return skill_name in self.mandatory_skills or '_constitutional' in skill_name
    
    def is_recommended_coordination_skill(self, skill_name: str) -> bool:
        """判断是否为推荐协同技能"""
        return skill_name in self.recommended_skills

# 创建全局注入器实例
HOOKS_INJECTOR = CoordinationHooksInjector()


def enhance_skill_with_coordination(skill_name: str, skill_module_path: Path) -> bool:
    """增强特定技能的协同契约强制执行"""
    try:
        # 加载技能模块
        spec = importlib.util.spec_from_file_location(skill_name, skill_module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 检查是否存在execute函数
        if not hasattr(module, 'execute'):
            return False
        
        original_execute = getattr(module, 'execute')
        
        # 检查技能是否需要协同增强
        injector = HOOKS_INJECTOR
        if (injector.is_mandatory_coordination_skill(skill_name) or 
            injector.is_recommended_coordination_skill(skill_name)):
            
            # 注入协同契约强制执行
            enhanced_execute = injector.inject_coordination_hooks(skill_name, original_execute)
            
            # 将增强后的函数放回模块
            setattr(module, 'execute', enhanced_execute)
            
            # 保存模块以便重新导入
            import sys
            sys.modules[f"enhanced_{skill_name}"] = module
            
            return True
        
        return False
        
    except Exception as e:
        print(f"增强技能 {skill_name} 失败: {e}")
        return False


def enhance_all_skills_in_directory(skills_directory: str):
    """增强目录下的所有技能"""
    skills_path = Path(skills_directory)
    
    enhanced_count = 0
    total_count = 0
    
    for skill_file in skills_path.glob("*.py"):
        if skill_file.name.startswith("__"):
            continue
            
        skill_name = skill_file.stem
        total_count += 1
        
        if enhance_skill_with_coordination(skill_name, skill_file):
            enhanced_count += 1
    
    print(f"协同强化完成: {enhanced_count}/{total_count} 个技能被增强")
    return enhanced_count, total_count


# 初始化执行 - 增强所有技能
def initialize_coordination_enforcement(skills_dir: str = None):
    """初始化协同强制执行系统"""
    import os
    
    if skills_dir is None:
        # 默认技能目录
        skills_dir = os.path.join(os.path.dirname(__file__), "skills")
    
    print("🔄 初始化认知协同执法系统...")
    
    enhanced_count, total_count = enhance_all_skills_in_directory(skills_dir)
    
    print(f"✅ 协同执法系统初始化完成!")
    print(f"📊 增强技能数: {enhanced_count}/{total_count}")
    
    # 显示违规模块
    from .coordination_enforcer import ENFORCER
    report = ENFORCER.get_violation_report()
    print(f"📋 违规模块总数: {report['total_violations']}")
    
    return enhanced_count, total_count


# 自动初始化
if __name__ != "__main__":
    # 如果不是直接执行，自动初始化
    try:
        initialize_coordination_enforcement()
    except Exception as e:
        print(f"初始化协同执法系统时出错: {e}")