"""
集成验证器模块
验证DSGS技能与AI CLI工具的集成状态
"""
import time
import os
from typing import Dict, Any, List
from .skill_executor import SkillExecutor
from .python_bridge import PythonBridge
from .skill_mapper import SkillMapper


class IntegrationValidator:
    """
    DSGS集成验证器
    验证DSGS技能与AI CLI工具的集成状态
    """
    
    def __init__(self, skill_executor: SkillExecutor = None):
        """
        初始化验证器
        
        Args:
            skill_executor: 技能执行器实例
        """
        self.skill_executor = skill_executor or SkillExecutor()
    
    def validate_platform_integration(self, platform_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证特定平台的集成状态
        
        Args:
            platform_name: 平台名称
            config: 配置字典
            
        Returns:
            验证结果字典
        """
        # 查找平台配置
        platform = None
        for p in config.get('platforms', []):
            if p['name'] == platform_name:
                platform = p
                break
        
        if not platform or not platform.get('enabled', False):
            return {
                'valid': False,
                'error': f'Platform {platform_name} not enabled or not found',
                'platform': platform_name
            }
        
        # 验证配置路径是否存在（非必须验证）
        config_path = platform.get('configPath')
        config_path_exists = False
        if config_path:
            try:
                import os
                config_path_exists = os.path.exists(config_path)
            except Exception:
                # 如果无法检查路径，继续验证其他部分
                config_path_exists = False

        # 注意：配置路径不存在不应导致验证失败，
        # 因为工具可能已安装但尚未创建配置目录
        
        # 验证技能是否可用
        skills_valid = self._validate_skills(platform)
        if not skills_valid['valid']:
            return skills_valid

        # 执行基本技能测试
        skill_test = self._test_basic_skill()

        return {
            'valid': skill_test['success'],  # 验证成功主要取决于技能是否可执行
            'platform': platform_name,
            'configPath': config_path,
            'configPathExists': config_path_exists,  # 添加配置路径是否存在的信息
            'skills': skills_valid.get('skills', []),
            'testResult': skill_test,
            'timestamp': self._get_timestamp()
        }
    
    def _validate_skills(self, platform: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证平台配置的技能
        
        Args:
            platform: 平台配置字典
            
        Returns:
            技能验证结果
        """
        try:
            # 检查技能是否在技能执行器中可用
            available_skills = self.skill_executor.get_available_skills()
            configured_skills = list(platform.get('skills', {}).keys())
            
            existing_skills = []
            missing_skills = []
            
            for skill in configured_skills:
                if skill in available_skills:
                    existing_skills.append(skill)
                else:
                    missing_skills.append(skill)
            
            return {
                'valid': len(missing_skills) == 0,
                'skills': existing_skills,
                'missing': missing_skills,
                'total': len(configured_skills)
            }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def _test_basic_skill(self) -> Dict[str, Any]:
        """
        测试基本技能功能
        
        Returns:
            技能测试结果
        """
        start_time = time.time()
        
        try:
            # 测试架构师技能
            result = self.skill_executor.execute('architect', 'test system')
            response_time = time.time() - start_time
            
            return {
                'success': result['success'],
                'responseTime': round(response_time * 1000, 2),  # 毫秒
                'result': result.get('result', ''),
                'skill': 'architect'
            }
        except Exception as e:
            response_time = time.time() - start_time
            return {
                'success': False,
                'responseTime': round(response_time * 1000, 2),
                'error': str(e)
            }
    
    def run_performance_test(self, iterations: int = 5) -> Dict[str, Any]:
        """
        运行性能测试
        
        Args:
            iterations: 测试迭代次数
            
        Returns:
            性能测试结果
        """
        results = []
        start_time = time.time()
        
        for i in range(iterations):
            iteration_start = time.time()
            try:
                result = self.skill_executor.execute('architect', f'test system {i}')
                iteration_time = time.time() - iteration_start
                
                results.append({
                    'iteration': i,
                    'success': result['success'],
                    'time': round(iteration_time * 1000, 2),  # 毫秒
                    'error': result.get('error')
                })
            except Exception as e:
                iteration_time = time.time() - iteration_start
                results.append({
                    'iteration': i,
                    'success': False,
                    'time': round(iteration_time * 1000, 2),
                    'error': str(e)
                })
        
        total_time = time.time() - start_time
        successful_tests = len([r for r in results if r['success']])
        success_rate = successful_tests / iterations if iterations > 0 else 0
        average_time = total_time / iterations if iterations > 0 else 0
        
        return {
            'iterations': iterations,
            'successful': successful_tests,
            'successRate': success_rate,
            'averageResponseTime': round(average_time * 1000, 2),  # 毫秒
            'totalTime': round(total_time * 1000, 2),
            'details': results
        }
    
    def validate_all_integrations(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证所有平台的集成状态
        
        Args:
            config: 配置字典
            
        Returns:
            所有验证结果字典
        """
        results = {}
        
        for platform in config.get('platforms', []):
            if platform.get('enabled', False):
                results[platform['name']] = self.validate_platform_integration(
                    platform['name'],
                    config
                )
        
        return results
    
    def generate_report(self, validation_results: Dict[str, Any]) -> str:
        """
        生成验证报告
        
        Args:
            validation_results: 验证结果字典
            
        Returns:
            验证报告字符串
        """
        report = '# DNASPEC Integration Validation Report\n\n'
        report += f'Generated at: {self._get_timestamp()}\n\n'
        
        for platform_name, result in validation_results.items():
            report += f'## {platform_name.upper()} Integration\n'
            
            if result['valid']:
                report += '✅ Status: Valid\n'
                if result.get('configPath'):
                    report += f'📁 Config Path: {result["configPath"]}\n'
                if result.get('skills'):
                    report += f'📊 Skills: {len(result["skills"])} skills configured\n'
                if result.get('testResult'):
                    test_result = result['testResult']
                    if test_result.get('success'):
                        report += f'⚡ Test: Passed (Response time: {test_result.get("responseTime", 0)}ms)\n'
            else:
                report += '❌ Status: Invalid\n'
                report += f'📝 Error: {result.get("error", "Unknown error")}\n'
            
            report += '\n'
        
        return report
    
    def save_report(self, report: str, file_path: str) -> bool:
        """
        保存验证报告到文件
        
        Args:
            report: 验证报告字符串
            file_path: 文件路径
            
        Returns:
            保存是否成功
        """
        try:
            # 确保目录存在
            directory = os.path.dirname(file_path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            return True
        except Exception as e:
            print(f'Failed to save report: {str(e)}')
            return False
    
    def _get_timestamp(self) -> str:
        """
        获取当前时间戳
        
        Returns:
            ISO格式时间戳字符串
        """
        import datetime
        return datetime.datetime.now().isoformat()
    
    def validate_skill_execution(self, skill_name: str, test_params: str = "validation test") -> Dict[str, Any]:
        """
        验证特定技能的执行能力
        
        Args:
            skill_name: 技能名称
            test_params: 测试参数
            
        Returns:
            技能执行验证结果
        """
        start_time = time.time()
        
        try:
            result = self.skill_executor.execute(skill_name, test_params)
            response_time = time.time() - start_time
            
            return {
                'valid': result['success'],
                'skill': skill_name,
                'responseTime': round(response_time * 1000, 2),
                'result': result.get('result', ''),
                'error': result.get('error') if not result['success'] else None
            }
        except Exception as e:
            response_time = time.time() - start_time
            return {
                'valid': False,
                'skill': skill_name,
                'responseTime': round(response_time * 1000, 2),
                'error': str(e)
            }