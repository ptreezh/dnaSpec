"""
DNASPEC 技能注册器 - 确保所有技能遵循Claude Skills规范
"""
from typing import Dict, Any, Callable, List
import importlib
import inspect
from pathlib import Path
import json

class ClaudeSkillsRegistrar:
    """
    Claude Skills规范注册器
    确保所有技能遵循Claude Skills标准
    """
    
    def __init__(self):
        self.registered_skills = {}
        self.cloude_skills_standards = {
            "required_methods": ["execute"],
            "required_functions": ["execute", "get_manifest"], 
            "expected_signature": {
                "execute": ["args: Dict[str, Any]"],
                "get_manifest": []
            },
            "return_types": {
                "execute": [str, dict],  # 可以返回字符串或字典
                "get_manifest": [dict]
            },
            "file_requirements": [
                "__init__.py",
                "execute function",
                "get_manifest function"
            ]
        }
    
    def validate_skill_compliance(self, skill_path: Path) -> Dict[str, Any]:
        """验证技能是否符合Claude Skills标准"""
        try:
            # 动态导入技能模块
            spec = importlib.util.spec_from_file_location(skill_path.stem, skill_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            validation_results = {
                "skill_name": skill_path.stem,
                "file_path": str(skill_path),
                "compliant": True,
                "violations": [],
                "details": {}
            }
            
            # 1. 检查必需的函数
            for required_func in self.claude_skills_standards["required_functions"]:
                if not hasattr(module, required_func):
                    validation_results["violations"].append(f"缺少必需函数: {required_func}")
                    validation_results["compliant"] = False
                    continue
                
                func = getattr(module, required_func)
                if not callable(func):
                    validation_results["violations"].append(f"{required_func} 不是可调用函数")
                    validation_results["compliant"] = False
            
            # 2. 检查execute函数签名
            if hasattr(module, "execute"):
                execute_func = getattr(module, "execute")
                sig = inspect.signature(execute_func)
                params = list(sig.parameters.keys())
                
                if len(params) == 0 or "args" not in params:
                    validation_results["violations"].append("execute函数应接受args参数: Dict[str, Any]")
                    validation_results["compliant"] = False
            
            # 3. 检查get_manifest函数
            if hasattr(module, "get_manifest"):
                manifest_func = getattr(module, "get_manifest")
                try:
                    manifest = manifest_func()
                    if not isinstance(manifest, dict):
                        validation_results["violations"].append("get_manifest函数应返回字典")
                        validation_results["compliant"] = False
                    else:
                        required_manifest_keys = ["name", "description", "version", "parameters"]
                        for key in required_manifest_keys:
                            if key not in manifest:
                                validation_results["violations"].append(f"技能清单缺少必需字段: {key}")
                                validation_results["compliant"] = False
                except Exception as e:
                    validation_results["violations"].append(f"get_manifest函数执行错误: {str(e)}")
                    validation_results["compliant"] = False
            
            # 4. 检查返回类型（通过调用测试）
            if hasattr(module, "execute"):
                try:
                    # 用空参数测试execute函数
                    test_result = module.execute({})
                    if not isinstance(test_result, (str, dict)):
                        validation_results["violations"].append("execute函数应返回字符串或字典")
                        validation_results["compliant"] = False
                except Exception as e:
                    validation_results["violations"].append(f"execute函数测试调用错误: {str(e)}")
                    validation_results["compliant"] = False
            
            return validation_results
            
        except Exception as e:
            return {
                "skill_name": skill_path.stem,
                "file_path": str(skill_path),
                "compliant": False,
                "violations": [f"模块导入失败: {str(e)}"],
                "details": {"exception": str(e)}
            }
    
    def register_skill(self, skill_path: Path) -> bool:
        """注册技能"""
        validation = self.validate_skill_compliance(skill_path)
        
        if validation["compliant"]:
            skill_name = skill_path.stem
            self.registered_skills[skill_name] = {
                "path": str(skill_path),
                "validation": validation,
                "status": "registered"
            }
            print(f"✅ 技能注册成功: {skill_name}")
            return True
        else:
            skill_name = skill_path.stem
            self.registered_skills[skill_name] = {
                "path": str(skill_path),
                "validation": validation,
                "status": "failed"
            }
            print(f"❌ 技能注册失败: {skill_name}")
            print(f"   违规: {', '.join(validation['violations'])}")
            return False
    
    def validate_all_skills_in_directory(self, skills_dir: str) -> Dict[str, Any]:
        """验证目录下所有技能"""
        skills_path = Path(skills_dir)
        validation_results = {
            "total_skills": 0,
            "compliant_skills": 0,
            "non_compliant_skills": 0,
            "skill_validations": []
        }
        
        for skill_file in skills_path.glob("*.py"):
            if skill_file.name.startswith("__"):
                continue
            
            validation = self.validate_skill_compliance(skill_file)
            validation_results["skill_validations"].append(validation)
            validation_results["total_skills"] += 1
            
            if validation["compliant"]:
                validation_results["compliant_skills"] += 1
            else:
                validation_results["non_compliant_skills"] += 1
        
        validation_results["compliance_rate"] = (
            validation_results["compliant_skills"] / validation_results["total_skills"] 
            if validation_results["total_skills"] > 0 else 0
        )
        
        return validation_results
    
    def get_claude_compliance_report(self, skills_dir: str) -> str:
        """获取Claude Skills合规性报告"""
        results = self.validate_all_skills_in_directory(skills_dir)
        
        report_lines = []
        report_lines.append("🏛️ DNASPEC Claude Skills 合规性报告")
        report_lines.append("=" * 50)
        report_lines.append(f"总技能数: {results['total_skills']}")
        report_lines.append(f"合规技能: {results['compliant_skills']}")
        report_lines.append(f"不合规技能: {results['non_compliant_skills']}")
        report_lines.append(f"合规率: {results['compliance_rate']:.1%}")
        report_lines.append("")
        
        if results['non_compliant_skills'] > 0:
            report_lines.append("❌ 不合规技能详情:")
            for validation in results['skill_validations']:
                if not validation['compliant']:
                    report_lines.append(f"  • {validation['skill_name']}")
                    for violation in validation['violations']:
                        report_lines.append(f"    - {violation}")
            report_lines.append("")
        
        if results['compliant_skills'] > 0:
            report_lines.append("✅ 合规技能列表:")
            for validation in results['skill_validations']:
                if validation['compliant']:
                    report_lines.append(f"  • {validation['skill_name']}")
        
        return "\n".join(report_lines)

# 全局注册器实例
CLAUDE_SKILLS_REGISTRAR = ClaudeSkillsRegistrar()

def validate_claude_skills_compliance(skills_directory: str = None) -> str:
    """验证Claude Skills合规性"""
    if skills_directory is None:
        skills_directory = Path(__file__).parent / "skills"
    
    return CLAUDE_SKILLS_REGISTRAR.get_claude_compliance_report(str(skills_directory))

def register_all_skills():
    """注册所有技能"""
    skills_dir = Path(__file__).parent / "skills"
    registrar = ClaudeSkillsRegistrar()
    
    for skill_file in skills_dir.glob("*.py"):
        if not skill_file.name.startswith("__"):
            registrar.register_skill(skill_file)

if __name__ == "__main__":
    # 当直接运行时，验证当前技能目录的合规性
    skills_dir = Path(__file__).parent / "skills"
    report = validate_claude_skills_compliance(str(skills_dir))
    print(report)